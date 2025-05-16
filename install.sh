#!/data/data/com.termux/files/usr/bin/bash

echo "[+] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[+] Installing tur-repo..."
pkg install tur-repo -y

echo "[+] Installing Python 3.11..."
pkg install python3.11 -y

echo "[+] Installing unzip and curl..."
pkg install unzip curl -y

echo "[+] Downloading offshore.zip..."
curl -L -o offshore.zip https://github.com/Educationservices/offshore/releases/download/Alpha/offshore.zip

echo "[+] Unzipping offshore.zip..."
unzip offshore.zip

echo "[+] Entering extracted folder..."
cd "youtubeshortsoffline - Copy" || { echo "[!] Folder not found"; exit 1; }

echo "[+] Removing old run_selected.py if it exists..."
rm -f run_selected.py

echo "[*] Launching builder. Add channels and type 'finished' when done."
python3.11 builder.py

echo "[+] Moving generated script to YTDLPSCRAP..."
cp run_selected.py ../YTDLPSCRAP || { echo "[!] run_selected.py not found"; exit 1; }

echo "[+] Entering YTDLPSCRAP..."
cd ../YTDLPSCRAP || { echo "[!] YTDLPSCRAP folder not found"; exit 1; }

echo "[+] Deleting old downloader.py..."
rm -f downloader.py

echo "[+] Renaming run_selected.py to downloader.py..."
mv run_selected.py downloader.py

echo "[+] Running downloader.py..."
python3.11 downloader.py
