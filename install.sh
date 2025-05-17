#!/data/data/com.termux/files/usr/bin/bash

echo "[+] Checking and installing required packages..."
pkg install -y tur-repo
pkg install -y python3.11

command -v curl >/dev/null 2>&1 || pkg install -y curl
command -v unzip >/dev/null 2>&1 || pkg install -y unzip
command -v python3.11 >/dev/null 2>&1 || pkg install -y python3.11
[ -d "$PREFIX/etc/tur" ] || pkg install -y tur-repo

echo "[+] Ensuring pip is installed for Python 3.11..."
python3.11 -m ensurepip --upgrade

echo "[+] Installing yt-dlp if not present..."
python3.11 -m pip show yt-dlp >/dev/null 2>&1 || python3.11 -m pip install yt-dlp --upgrade

pip3.11 install flask

echo "[+] Downloading offshore.zip if not already downloaded..."
[ -f offshore.zip ] || curl -L -o offshore.zip https://github.com/Educationservices/offshore/releases/download/Alpha0.02/offshore.zip

echo "[+] Unzipping offshore.zip if folder doesn't exist..."
[ -d "youtubeshortsoffline - Copy" ] || unzip offshore.zip

echo "[+] Entering extracted folder..."
cd "youtubeshortsoffline - Copy" || { echo "[!] Folder not found"; exit 1; }

echo "[+] Removing old run_selected.py if it exists..."
rm -f run_selected.py

echo "[*] Launching builder. Add channels and type 'finished' when done."
python3.11 builder.py

echo "[+] Moving and renaming run_selected.py to YTDLPSCRAP/downloader.py..."
mv run_selected.py YTDLPSCRAP/downloader.py || { echo "[!] run_selected.py not found"; exit 1; }

echo "[+] Entering YTDLPSCRAP..."
cd YTDLPSCRAP || { echo "[!] YTDLPSCRAP folder not found"; exit 1; }

echo "[+] Running downloader.py..."
python3.11 downloader.py

