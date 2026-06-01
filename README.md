<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=35&duration=3000&pause=1000&color=FF0000&center=true&vCenter=true&width=600&lines=NULLTRACK+v1.0;Precision+Geolocation+Framework;Zero+Click+GPS+Capture" alt="NULLTRACK" />
</p>
<p align="center">
  <img src="https://img.shields.io/badge/version-1.0-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/github/stars/thisnull7/nulltrack?style=social" />
  <img src="https://img.shields.io/github/forks/thisnull7/nulltrack?style=social" />
</p>

# NULLTRACK 

**NULLTRACK** is a precision geolocation framework designed for educational security research. It generates a convincing Google Maps delivery verification page that requests GPS access from visitors. When permission is granted, precise coordinates, device fingerprints, and network information are captured in real-time. The tool includes a multi-tunnel system (Cloudflared, Serveo, localhost.run) to expose your local server publicly without port forwarding.

> **DISCLAIMER**: This tool is intended for educational purposes and authorized security testing only. The developer assumes no liability for misuse. Always obtain explicit consent before tracking any individual.

## Features

- Zero-Click Auto GPS Popup — triggers browser location permission 0.8 seconds after page load
- Device Fingerprinting — captures user agent, platform, language, screen size, color depth, timezone, CPU cores, RAM, connection type
- Real-time Coordinate Capture — logs latitude, longitude, accuracy, altitude, speed, heading
- Reverse Geocoding — converts GPS coordinates to physical addresses via OpenStreetMap Nominatim
- IP & ISP Geolocation — retrieves city, region, country, ISP, organization via ip-api.com
- Google Maps & OpenStreetMap direct links automatically generated
- Multi-Tunnel System — Cloudflared (primary, no account needed), Serveo SSH (fallback), localhost.run (fallback 2)
- Modern Glassmorphism UI — animated background orbs, pulse effects, ripple animations, dynamic domain display
- JSON Data Logging — all captures saved to structured JSON file
- Multi-Platform — Windows, Linux, macOS
- Auto-download Cloudflared binary if not present
- Auto-install dependencies with graceful fallbacks if colorama/pyfiglet missing
- Clean modern terminal interface with spinner animations, section headers, color-coded output

## 🚀 Installation For Command Prompt (CMD)

### Prerequisites

- **Python 3.8+** installed on your system
- **Git** (optional, for cloning)
- **SSH client** (optional, for Serveo/localhost.run fallback)

### Step 1 — Clone Repository

git clone https://github.com/thisnull7/nulltrack

cd nulltrack

python -m pip install requests

python -m pip install colorama

python -m pip install pyfiglet


run

python track.py

What Happens When You Run:
Stage	Description
Initialization	HTTP server starts on port 8080
Tunnel Setup	Attempts Cloudflared → Serveo → localhost.run
Public URL	Displays the link to send to target
Awaiting Hits	Listens for incoming GPS data
Data Logging	Saves all captures to nulltrack_victims.json

📊 Captured Data

When a target clicks "Allow Once", the following is captured:
json

{
  "id": "20260102153045123456",
  "timestamp": "2026-01-02T15:30:45.123456",
  "gps": {
    "latitude": -6.2088,
    "longitude": 106.8456,
    "accuracy_m": 12.5,
    "altitude": "N/A",
    "speed_mps": "N/A",
    "heading": "N/A"
  },
  "address": "Jl. MH Thamrin, Jakarta, Indonesia",
  "ip": "192.168.1.1",
  "isp": "Jakarta, Indonesia — PT Telkom Indonesia",
  "device": {
    "ua": "Mozilla/5.0 ...",
    "platform": "Win32",
    "language": "en-US",
    "screen": "1920x1080",
    "timezone": "Asia/Jakarta",
    "cpu": 8,
    "ram": 8,
    "connection": "4g"
  },
  "maps": {
    "google": "https://www.google.com/maps?q=-6.2088,106.8456",
    "osm": "https://www.openstreetmap.org/?mlat=-6.2088&mlon=106.8456"
  }
}

🌐 Landing Page Features

The phishing page is designed to look identical to Google Maps:

    🎨 Glassmorphism UI with animated background orbs

    📍 Animated location pin with pulse and ripple effects

    🔒 Privacy badge ("Encrypted & used only for this session")

    ⏱️ Auto-trigger — GPS popup appears 0.8 seconds after page load

    ✅ Success animation — Checkmark with pop-in effect

    ⚠️ Error handling — Clear messages with retry option

    🌐 Dynamic domain — Shows the actual tunnel domain in the UI

👤 Author
<p align="center"> <b>null7</b> </p><p align="center"> <a href="https://github.com/thisnull7"> <img src="https://img.shields.io/badge/GitHub-thisnull7-181717?style=for-the-badge&logo=github" /> </a> </p>
⭐ Support

If you find this project useful, consider giving it a star on GitHub.
<p align="center"> <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=18&duration=2000&pause=1000&color=FF0000&center=true&vCenter=true&width=400&lines=Made+with+%E2%9D%A4%EF%B8%8F+by+null7;For+educational+purposes+only" /> </p>
