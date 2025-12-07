import os
import re
import time
import asyncio
import subprocess
from datetime import datetime

from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yt_dlp
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client

# ================= CONFIG ================= #

API_KEY = os.getenv("ABHIX_API_KEY")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
COOKIES_FILE = os.getenv("COOKIES_FILE")
MONGO_DB_URI = os.getenv("MONGO_DB_URI")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
USER_SESSION = os.getenv("USER_SESSION")

CACHE_CHANNEL = os.getenv("CACHE_CHANNEL")  # @Desi_Beat jaisa

MAX_CONCURRENT_DOWNLOADS = int(os.getenv("MAX_CONCURRENT_DOWNLOADS", "4"))
download_semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

# audio cache upload size limit (MB)
AUDIO_TG_UPLOAD_LIMIT_MB = float(os.getenv("AUDIO_TG_UPLOAD_LIMIT_MB", "50"))

if not API_KEY:
    raise RuntimeError("ABHIX_API_KEY missing")
if not MONGO_DB_URI:
    raise RuntimeError("MONGO_DB_URI missing")
if not API_ID or not API_HASH:
    raise RuntimeError("API_ID/API_HASH missing")
if not USER_SESSION:
    raise RuntimeError("USER_SESSION missing")
if not CACHE_CHANNEL:
    raise RuntimeError("CACHE_CHANNEL missing (use @username or t.me link)")

# ================= FASTAPI ================= #

app = FastAPI(title="AbhiXApi (Audio cache, Video serve, MP3 logs)")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
app.mount("/files", StaticFiles(directory=DOWNLOAD_DIR), name="files")

mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
db = mongo_client["AbhiXApi"]
cache_col = db["yt_cache"]

user_client = Client(
    "abhix_user_uploader",
    session_string=USER_SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
)

CACHE_CHAT = None


class DownloadRequest(BaseModel):
    url: str
    type: str  # "audio" | "video"


# ================= HELPERS ================= #

def safe_filename(title: str, ext: str, fallback: str) -> str:
    base = re.sub(r"[^\w\-. ]+", "", title or fallback).strip()
    if not base:
        base = fallback or "track"
    return f"{base}.{ext}"


def cleanup_downloads():
    """30 min se purani files hata do"""
    now = time.time()
    max_age = 30 * 60
    try:
        for fname in os.listdir(DOWNLOAD_DIR):
            path = os.path.join(DOWNLOAD_DIR, fname)
            if not os.path.isfile(path):
                continue
            try:
                st = os.stat(path)
            except FileNotFoundError:
                continue
            if now - st.st_mtime > max_age:
                try:
                    os.remove(path)
                    print("[CLEANUP] Removed:", fname)
                except Exception:
                    pass
    except FileNotFoundError:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def run_yt_download(url: str, opts: dict):
    """yt-dlp download (no duration limit)"""
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
    return info, filepath


def convert_to_mp3(src_path: str, out_path: str):
    """ffmpeg se src ko mp3 me convert karo"""
    # ffmpeg -y -i input -vn -acodec libmp3lame -ab 192k output
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        src_path,
        "-vn",
        "-acodec",
        "libmp3lame",
        "-ab",
        "192k",
        out_path,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ================= TELEGRAM AUDIO CACHE ================= #

async def cache_to_telegram_audio_only(filepath: str, title: str, duration: int, doc_id):
    global CACHE_CHAT
    try:
        if not CACHE_CHAT:
            CACHE_CHAT = await user_client.get_chat(CACHE_CHANNEL)
            print(f"[CACHE] Using channel: {CACHE_CHAT.title} ({CACHE_CHAT.id})")

        msg = await user_client.send_audio(
            chat_id=CACHE_CHAT.id,
            audio=filepath,
            title=title or "",
            duration=duration or 0,
        )

        await cache_col.update_one(
            {"_id": doc_id},
            {"$set": {"tg_file_id": msg.audio.file_id}},
        )

        print("[CACHE] ✅ AUDIO uploaded to log channel")

    except Exception as e:
        print("[CACHE] ❌ Upload failed:", e)


# ================= STARTUP / SHUTDOWN ================= #

@app.on_event("startup")
async def on_startup():
    global CACHE_CHAT
    print("[START] Connecting user client...")
    await user_client.start()
    me = await user_client.get_me()
    print(f"[START] Logged in as: {me.id} {me.first_name} (@{me.username})")
    try:
        CACHE_CHAT = await user_client.get_chat(CACHE_CHANNEL)
        print(f"[START] Cache channel: {CACHE_CHAT.title} ({CACHE_CHAT.id})")
    except Exception as e:
        CACHE_CHAT = None
        print("[START] Cache channel resolve error:", e)
    print("[START] Startup complete ✅")


@app.on_event("shutdown")
async def on_shutdown():
    print("[STOP] Stopping user client...")
    await user_client.stop()
    print("[STOP] Shutdown complete.")


# ================= MAIN API ================= #

@app.post("/download")
async def download_media(payload: DownloadRequest, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    cleanup_downloads()

    url = payload.url
    if not url.startswith("http"):
        url = f"https://www.youtube.com/watch?v={url}"

    key = {
        "source": "youtube",
        "source_id": url,
        "type": payload.type,
    }

    # -------- CACHE HIT (sirf audio ke liye) -------- #
    if payload.type == "audio":
        cached = await cache_col.find_one(key)
        if cached:
            filename = cached.get("filename")
            tg_file_id = cached.get("tg_file_id")

            if filename:
                local_path = os.path.join(DOWNLOAD_DIR, filename)
                if os.path.exists(local_path):
                    print("[CACHE] HIT (local):", filename)
                    return {
                        "status": "cached",
                        "download_url": f"/files/{filename}",
                        "title": cached.get("title"),
                        "duration": cached.get("duration"),
                    }

            if tg_file_id:
                try:
                    print("[CACHE] HIT (telegram re-download)")
                    local_path = os.path.join(DOWNLOAD_DIR, f"{cached['_id']}.mp3")
                    await user_client.download_media(tg_file_id, file_name=local_path)
                    new_name = os.path.basename(local_path)

                    await cache_col.update_one(
                        {"_id": cached["_id"]},
                        {"$set": {"filename": new_name}},
                    )

                    return {
                        "status": "cached",
                        "download_url": f"/files/{new_name}",
                        "title": cached.get("title"),
                        "duration": cached.get("duration"),
                    }
                except Exception as e:
                    print("[CACHE] TG re-download failed:", e)

    # -------- FRESH DOWNLOAD -------- #

    base_opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "noplaylist": True,
    }

    if COOKIES_FILE and os.path.exists(COOKIES_FILE):
        base_opts["cookiefile"] = COOKIES_FILE

    # yt-dlp ke liye:
    # audio request -> bestaudio
    # video request -> 720p tak video
    if payload.type == "audio":
        base_opts["format"] = "bestaudio/best"
    elif payload.type == "video":
        base_opts["format"] = "bv*[height<=720]+ba/best"
    else:
        raise HTTPException(status_code=400, detail="type must be 'audio' or 'video'")

    try:
        async with download_semaphore:
            info, raw_path = await asyncio.to_thread(run_yt_download, url, base_opts)
    except Exception as e:
        print("[DOWNLOAD] error:", e)
        raise HTTPException(status_code=400, detail=str(e))

    title = info.get("title") or "Track"
    duration = info.get("duration") or 0

    # ----- FILE PATH / CONVERSION LOGIC ----- #

    if payload.type == "audio":
        # raw_path (webm/m4a etc) -> final mp3 path
        mp3_name = safe_filename(title, "mp3", info.get("id", "track"))
        mp3_path = os.path.join(DOWNLOAD_DIR, mp3_name)

        try:
            convert_to_mp3(raw_path, mp3_path)
            try:
                os.remove(raw_path)
            except Exception:
                pass
            final_path = mp3_path
            filename = mp3_name
        except Exception as e:
            print("[FFMPEG] convert_to_mp3 failed, fallback to raw:", e)
            final_path = raw_path
            filename = os.path.basename(raw_path)

    else:
        # video: sirf title-safe rename, koi mp3 nahi
        ext = raw_path.split(".")[-1]
        filename = safe_filename(title, ext, info.get("id", "track"))
        final_path = os.path.join(DOWNLOAD_DIR, filename)
        try:
            os.replace(raw_path, final_path)
        except FileNotFoundError:
            final_path = raw_path
            filename = os.path.basename(raw_path)

    size_mb = os.path.getsize(final_path) / (1024 * 1024)
    print(f"[DOWNLOAD] {filename} ({size_mb:.2f} MB) [{payload.type}]")

    doc = {
        **key,
        "title": title,
        "duration": duration,
        "filename": filename,
        "filesize_mb": size_mb,
        "created_at": datetime.utcnow(),
    }

    ins = await cache_col.insert_one(doc)
    doc_id = ins.inserted_id

    # -------- BACKGROUND AUDIO CACHE (sirf audio & size <= limit) -------- #

    if payload.type == "audio":
        if size_mb <= AUDIO_TG_UPLOAD_LIMIT_MB:
            print(f"[CACHE] Background AUDIO upload scheduled → {filename} ({size_mb:.2f} MB)")
            loop = asyncio.get_running_loop()
            loop.create_task(
                cache_to_telegram_audio_only(final_path, title, duration, doc_id)
            )
        else:
            print(f"[CACHE] Skipping TG upload (audio too large: {size_mb:.2f} MB)")

    # video ke liye cache_to_telegram nahi, sirf serve

    return {
        "status": "success",
        "download_url": f"/files/{filename}",
        "title": title,
        "duration": duration,
    }
