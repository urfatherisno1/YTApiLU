#!/bin/bash

# AbhiXApi root me aa jao
cd "$(dirname "$0")"

echo "[AbhiXApi] Loading environment from .env..."
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "[AbhiXApi] .env file not found! Exiting."
  exit 1
fi

echo "[AbhiXApi] Starting API server..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &
API_PID=$!
echo "[AbhiXApi] API PID: $API_PID"

echo "[AbhiXApi] Starting Control Bot..."
python3 control_bot.py &
BOT_PID=$!
echo "[AbhiXApi] Control Bot PID: $BOT_PID"

echo ""
echo "[AbhiXApi] Sab kuch start ho chuka hai ✅"
echo "[AbhiXApi] Logs isi terminal me dikhenge (API + Control Bot mixed)."
echo "[AbhiXApi] Band karne ke liye sirf CTRL + C daba dena."
echo ""

# Dono processes ka wait – jab tak tu CTRL+C nahi marega, ye terminal busy rahega
wait
