━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<h2 align="center">
⚡🎧 A B H I X  ✘  A P I  –  U L T R A  P R E M I U M 🎧⚡
</h2>

<p align="center">
  <img src="https://graph.org/file/804fa956a84862b547fc5.jpg">
</p>

<p align="center">
<a href="https://github.com/urfatherisno1/YTApiLU/stargazers"><img src="https://img.shields.io/github/stars/urfatherisno1/YTApiLU?color=black&style=for-the-badge&logo=github"></a>
<a href="https://github.com/urfatherisno1/YTApiLU/network/members"><img src="https://img.shields.io/github/forks/urfatherisno1/YTApiLU?color=black&style=for-the-badge&logo=github"></a>
<a href="#"><img src="https://img.shields.io/badge/API-FastAPI-green?style=for-the-badge"></a>
<a href="#"><img src="https://img.shields.io/badge/Language-Python-orange?style=for-the-badge&logo=python"></a>
<a href="#"><img src="https://img.shields.io/badge/Status-Running-success?style=for-the-badge"></a>
</p>

<p align="center">
OWNER & DEVELOPER → <a href="https://t.me/UR_Father">@UR_Father</a>  
REPOSITORY → https://github.com/urfatherisno1/YTApiLU
</p>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 ULTRA PREMIUM FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Ultra Fast YouTube → Audio & Video API
- Smart MP3 Cache using Telegram Log Channel
- Repeat Song = Instant Cache Hit
- Auto Delete VPS Files after 30 Minutes
- Only ≤ 50MB MP3 Uploaded to Log Channel
- Video Play Supported (No Channel Upload)
- Multi Concurrent Downloads
- Heavy Load Ready
- Cookie Based YouTube Bypass
- Telegram User Account Based Unlimited Upload
- MongoDB Based Cache Storage
- API Key Protected System
- TMUX Background Runner Supported

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠 FULL VPS SETUP GUIDE (UBUNTU 20.04 / 22.04)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### System Update
```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### Install Required Packages
```bash
sudo apt-get install python3-pip ffmpeg git tmux -y
```

### Upgrade PIP
```bash
sudo pip3 install -U pip
```

### Clone Repository
```bash
cd ~
git clone https://github.com/urfatherisno1/YTApiLU.git
cd YTApiLU
```

### Install Python Requirements
```bash
pip3 install -r requirements.txt
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ ENVIRONMENT CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```bash
nano .env
```

```env
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
```

Save with:
```bash
CTRL + X
Y
ENTER
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ START API (FOREGROUND MODE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```bash
export $(grep -v '^#' .env | xargs)
./start.sh
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧱 START API IN BACKGROUND (TMUX MODE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```bash
tmux new -s abhixapi
```

```bash
export $(grep -v '^#' .env | xargs)
./start.sh
```

Detach:
```bash
CTRL + B → D
```

Reattach:
```bash
tmux attach -t abhixapi
```

Stop:
```bash
CTRL + C
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎛 API USAGE (FOR MUSIC BOTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```bash
POST http://YOUR_SERVER_IP:8000/download
```

```bash
X-API-KEY: INFLEX93454428D
```

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "type": "audio"
}
```

Type Options:
- `audio` → MP3 + Telegram Cache
- `video` → MP4 Direct Stream (No Channel Upload)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 SYSTEM WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIRST AUDIO REQUEST  
YouTube → MP3 → Telegram Cache → MongoDB → User Playback  

SECOND SAME AUDIO  
Instant Cache Hit → Direct Playback  

VIDEO REQUEST  
YouTube → MP4 → Direct Play → No Channel Upload  

LOCAL VPS FILES  
Auto Deleted After 30 Minutes  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ COMMON ERROR FIXES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FFmpeg Missing:
```bash
sudo apt-get install ffmpeg -y
```

Peer ID Invalid:
- Add USER account as ADMIN in cache channel
- Send one message from USER account
- Restart API

API 500 Error:
- API Key must be same in bot and API
- USER_SESSION must be valid
- MongoDB URI must be correct

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 SUPPORT & CONTACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Developer → https://t.me/UR_Father  
Support Group → https://t.me/imagine_iq  
YouTube → https://youtube.com/@imagineiq  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BUILT WITH ❤️ BY GOD FATHER (@UR_Father)
⚡ POWERED BY ABHIX API – ULTRA PREMIUM ENGINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
