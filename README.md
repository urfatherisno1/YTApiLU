━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎧⚡ 𝗔 𝗕 𝗛 𝗜 𝗫   ✘   𝗔 𝗣 𝗜 ⚡🎧  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 PREMIUM YOUTUBE → TELEGRAM AUDIO / VIDEO API  
👑 Owner & Developer: @UR_Father  
🖼 Banner: https://te.legra.ph/file/95b3ca7993bbfaf993dcb.jpg  
🌐 GitHub: https://github.com/urfatherisno1/YTApiLU  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ PREMIUM FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

► Ultra Fast YouTube → Audio / Video Downloader (yt-dlp + FastAPI)  
► Smart MP3 Cache via Telegram Log Channel  
► Same Song Repeat → 🚀 INSTANT CACHE HIT  
► Auto Cleanup → 30 Minutes Me VPS Clean  
► Only ≤ 50MB MP3 Upload To Log Channel  
► /vplay Mode → User Gets Video, Channel Gets ❌ NOTHING  
► API Key Protected System  
► Multi Concurrent Downloads  
► Heavy Load Music Bot Ready  
► Premium Cookies Based Bypass  
► Telegram User Account Based Upload (No 2GB Limit Issue)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠 FULL VPS SETUP GUIDE (UBUNTU 20.04 / 22.04)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install python3-pip ffmpeg git tmux -y

sudo pip3 install -U pip

cd ~

git clone https://github.com/urfatherisno1/YTApiLU.git

cd YTApiLU

pip3 install -r requirements.txt

nano .env

ABHIX_API_KEY=INFLEX93454428D
MONGO_DB_URI=mongodb+srv://USER:PASS@cluster.mongodb.net/?appName=AbhiXApi
API_ID=18290252
API_HASH=82de8e0388f6f3524ab15002c2154986
USER_SESSION=PASTE_YOUR_PYROGRAM_SESSION
CACHE_CHANNEL=@Desi_Beat
DOWNLOAD_DIR=downloads
COOKIES_FILE=/home/ubuntu/YTApiLU/cookies.txt
MAX_CONCURRENT_DOWNLOADS=4
AUDIO_TG_UPLOAD_LIMIT_MB=50
BOT_TOKEN=YOUR_CONTROL_BOT_TOKEN
OWNER_ID=8302512047

CTRL + X → Y → ENTER

export $(grep -v '^#' .env | xargs)

./start.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧱 BACKGROUND MODE (TMUX – PREMIUM WAY)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

tmux new -s abhixapi

export $(grep -v '^#' .env | xargs)

./start.sh

CTRL + B → D   (Detach)

tmux attach -t abhixapi   (Reattach)

CTRL + C  (Stop API)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎛 API USAGE (FOR MUSIC BOTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POST http://YOUR_SERVER_IP:8000/download

HEADER:
X-API-KEY: INFLEX93454428D

BODY:
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "type": "audio"
}

type:
audio → MP3 + Telegram Cache  
video → MP4 Stream Only (NO Log Upload)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 PREMIUM SYSTEM WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIRST AUDIO REQUEST:
YouTube → MP3 → Telegram Log Channel → MongoDB Cache

SECOND SAME AUDIO:
Direct Telegram Cache Hit → ⚡ INSTANT PLAY

VIDEO REQUEST:
YouTube → MP4 → Direct Stream → ❌ No Channel Upload

LOCAL VPS FILES:
Auto Deleted After 30 Minutes (Auto Cleanup)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ COMMON PREMIUM FIXES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FFmpeg Error:
sudo apt-get install ffmpeg -y

Peer ID Invalid:
- USER account ko channel ka ADMIN banao
- USER se channel me ek message bhejo
- API restart karo

API 500 Error:
- API KEY bot aur API dono me SAME ho
- USER_SESSION valid ho
- MongoDB URI sahi ho

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 PREMIUM SUPPORT & CONTACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👑 Developer: https://t.me/UR_Father  
💬 Support Group: https://t.me/imagine_iq  
▶️ YouTube: https://youtube.com/@imagineiq  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BUILT WITH ❤️ BY GOD FATHER (@UR_Father)
🔥 POWERED BY ABHIX API PREMIUM ENGINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
