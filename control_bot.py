import os
import shutil
from datetime import datetime

from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# Env vars
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")

OWNER_ID = int(os.getenv("API_OWNER_ID", "8302512047"))  # tumhara owner id

# Mongo
mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
db = mongo_client["AbhiXApi"]
cache_col = db["yt_cache"]

app = Client(
    "abhix_api_control_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)


def format_size(bytes_val: int) -> str:
    bytes_val = float(bytes_val)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} PB"


@app.on_message(filters.private & filters.user(OWNER_ID) & filters.command(["start", "help"]))
async def start_handler(client, message):
    text = (
        "👋 **AbhiXApi Control Panel**\n\n"
        "/api_stats - API overall stats\n"
        "/api_cache - Cache info (count & last 5 entries)\n"
        "/api_space - Disk usage (full + downloads)\n"
        "/api_purge - Delete ALL files in downloads (temp clear)\n"
    )
    await message.reply_text(text)


@app.on_message(filters.private & filters.user(OWNER_ID) & filters.command("api_stats"))
async def api_stats(client, message):
    total_cache = await cache_col.count_documents({})
    latest = await cache_col.find().sort("created_at", -1).limit(1).to_list(1)
    if latest:
        last_time = latest[0]["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        last_title = latest[0].get("title") or "Unknown"
    else:
        last_time = "N/A"
        last_title = "N/A"

    text = (
        "📊 **API Stats**\n\n"
        f"• Cached entries: `{total_cache}`\n"
        f"• Last cache time: `{last_time}`\n"
        f"• Last title: `{last_title}`\n"
    )
    await message.reply_text(text)


@app.on_message(filters.private & filters.user(OWNER_ID) & filters.command("api_cache"))
async def api_cache(client, message):
    total_cache = await cache_col.count_documents({})
    last_five = await cache_col.find().sort("created_at", -1).limit(5).to_list(5)

    lines = [f"📦 Total cache entries: `{total_cache}`", "⏱ Last 5:"]
    for doc in last_five:
        t = doc.get("title") or "Unknown"
        s = (doc.get("source_id") or "")[-11:]
        created = doc.get("created_at").strftime("%Y-%m-%d %H:%M")
        lines.append(f"• `{created}` - {t} (`{s}`)")

    await message.reply_text("\n".join(lines))


@app.on_message(filters.private & filters.user(OWNER_ID) & filters.command("api_space"))
async def api_space(client, message):
    # Disk usage for whole filesystem
    total, used, free = shutil.disk_usage("/")
    # Only downloads folder size
    downloads_size = 0
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for f in files:
            fp = os.path.join(root, f)
            try:
                downloads_size += os.path.getsize(fp)
            except FileNotFoundError:
                pass

    text = (
        "💾 **Disk Usage**\n\n"
        f"• Total: `{format_size(total)}`\n"
        f"• Used: `{format_size(used)}`\n"
        f"• Free: `{format_size(free)}`\n"
        f"• Downloads folder: `{format_size(downloads_size)}`\n"
    )
    await message.reply_text(text)


@app.on_message(filters.private & filters.user(OWNER_ID) & filters.command("api_purge"))
async def api_purge(client, message):
    # Delete all files in downloads
    if not os.path.exists(DOWNLOAD_DIR):
        return await message.reply_text("downloads/ folder not found.")

    removed = 0
    for fname in os.listdir(DOWNLOAD_DIR):
        path = os.path.join(DOWNLOAD_DIR, fname)
        if os.path.isfile(path):
            try:
                os.remove(path)
                removed += 1
            except Exception:
                pass

    await message.reply_text(f"🧹 Purged `{removed}` files from downloads folder.")


print(">> AbhiXApi Control Bot started. Use /start in PM (owner only).")
app.run()
