import requests
import shutil
import json
import os
import sys
import ctypes
import socket
import subprocess
from colorama import Fore, Style, init

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
try:
    if not is_admin():
        # Relaunch this script with admin rights
        script = os.path.abspath(sys.argv[0])
        # Pass all command-line arguments as well
        args = ' '.join(f'"{arg}"' for arg in sys.argv[1:])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {args}', None, 1
        )
        sys.exit()   # Exit the current non-admin process
except Exception as e:
    print(f"Error: {e}")
# Optional clipboard support
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

init(autoreset=True)

# ---------- Helper Functions ----------
def get_terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def wrap_banner_lines(banner, width):
    wrapped = []
    for line in banner.splitlines():
        if len(line) <= width:
            wrapped.append(line)
        else:
            for i in range(0, len(line), width):
                wrapped.append(line[i:i+width])
    return '\n'.join(wrapped)

def center_text(text, width):
    return '\n'.join(line.center(width) for line in text.splitlines())

ascii_banner = r"""
 _   _ _ _   _                 _         ___________   _                     _             
| | | | | | (_)               | |       |_   _| ___ \ | |                   | |            
| | | | | |_ _ _ __ ___   __ _| |_ ___    | | | |_/ / | |     ___   ___ __ _| |_ ___  _ __ 
| | | | | __| | '_ ` _ \ / _` | __/ _ \   | | |  __/  | |    / _ \ / __/ _` | __/ _ \| '__|
| |_| | | |_| | | | | | | (_| | ||  __/  _| |_| |     | |___| (_) | (_| (_| | || (_) | |   
 \___/|_|\__|_|_| |_| |_|\__,_|\__\___|  \___/\_|     \_____/\___/ \___\__,_|\__\___/|_|   
                                                                                          
                                                                                          
"""

def build_google_maps_link(lat, lon):
    if lat and lon:
        return f"https://www.google.com/maps/@{lat},{lon},15z"
    return ""

def resolve_domain(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def detect_hosting_vpn(org_string):
    """Check if the ISP/org string indicates a hosting provider, VPN, or proxy."""
    if not org_string:
        return "Unknown"
    keywords = [
        "Amazon", "AWS", "DigitalOcean", "OVH", "Microsoft Azure", "Google Cloud",
        "VPN", "Proxy", "Hosting", "DataCenter", "Colocation", "VPS", "Linode",
        "Hetzner", "Vultr", "Scaleway", "Cloudflare", "Akamai", "Fastly"
    ]
    for kw in keywords:
        if kw.lower() in org_string.lower():
            return f"⚠️  {kw}"
    return "✅ Residential / Business"

# ---------- API Functions ----------
def get_ipinfo_data(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        loc = data.get("loc", "")
        lat_lon = loc.split(",") if loc else [None, None]
        lat, lon = lat_lon[0], lat_lon[1] if len(lat_lon) == 2 else (None, None)
        
        org = data.get("org", "")
        return {
            "IP": data.get("ip"),
            "City": data.get("city"),
            "Region or State": data.get("region"),
            "Country": data.get("country"),
            "Coordinates": loc,
            "Google Maps": build_google_maps_link(lat, lon),
            "ISP (Internet Service Provider)": org,
            "VPN/Hosting": detect_hosting_vpn(org),
            "Timezone": data.get("timezone")
        }
    except Exception as e:
        return {"error": f"Failed to get data from ipinfo.io: {str(e)}"}

def get_ipwhois_data(ip):
    try:
        response = requests.get(f"https://ipwho.is/{ip}", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("success"):
            return {"error": "ipwho.is returned unsuccessful response"}
        
        lat = data.get("latitude")
        lon = data.get("longitude")
        loc = f"{lat},{lon}" if lat and lon else ""
        isp = data.get("connection", {}).get("isp", "")
        
        return {
            "IP": data.get("ip"),
            "City": data.get("city"),
            "Region or State": data.get("region"),
            "Country": f"{data.get('country')} {data.get('flag', {}).get('emoji', '')}".strip(),
            "Coordinates": loc,
            "Google Maps": build_google_maps_link(lat, lon),
            "ISP (Internet Service Provider)": isp,
            "VPN/Hosting": detect_hosting_vpn(isp),
            "Timezone": data.get("timezone", {}).get("id")
        }
    except Exception as e:
        return {"error": f"Failed to get data from ipwho.is: {str(e)}"}

def get_ipapi_data(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "success":
            return {"error": f"ip-api.com error: {data.get('message', 'Unknown error')}"}
        
        lat = data.get("lat")
        lon = data.get("lon")
        loc = f"{lat},{lon}" if lat and lon else ""
        isp = data.get("isp") or data.get("org", "")
        
        return {
            "IP": data.get("query"),
            "City": data.get("city"),
            "Region or State": data.get("regionName"),
            "Country": data.get("country"),
            "Coordinates": loc,
            "Google Maps": build_google_maps_link(lat, lon),
            "ISP (Internet Service Provider)": isp,
            "VPN/Hosting": detect_hosting_vpn(isp),
            "Timezone": data.get("timezone")
        }
    except Exception as e:
        return {"error": f"Failed to get data from ip-api.com: {str(e)}"}

# ---------- Display ----------
def display_result(result, title=None):
    if 'error' in result:
        print(f"\n{Fore.RED}[ERROR]{Style.RESET_ALL} {result['error']}")
        return None
    else:
        if title:
            print(f"\n{Fore.CYAN}--- {title} ---{Style.RESET_ALL}")
        else:
            print()
        for key, value in result.items():
            if value or value == 0:
                print(f"{Fore.RED}{key}:{Style.RESET_ALL} {value}")
        # Return the Google Maps link if present, for clipboard
        return result.get("Google Maps")

# ---------- Settings Loading ----------
def load_settings():
    settings_file = "Advanced_Settings.json"
    default_settings = {
        "Batch Processing": False,
        "Multi-API": False,
        "VPN Detection": False,
        "Link To Clipboard": False
    }
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
                # Handle old key names (e.g., "Batch Processing0")
                for key in list(settings.keys()):
                    if key.endswith("0"):
                        new_key = key[:-1]
                        settings[new_key] = settings.pop(key)
                # Ensure all expected keys exist
                for k in default_settings:
                    if k not in settings:
                        settings[k] = default_settings[k]
                return settings
        except:
            print("Settings file corrupted. Using defaults.")
            return default_settings
    else:
        # Create default settings file
        with open(settings_file, "w") as f:
            json.dump(default_settings, f, indent=4)
        return default_settings

# ---------- Main ----------
def main():
    # Load settings
    settings = load_settings()
    batch_mode = settings.get("Batch Processing", False)
    multi_api = settings.get("Multi-API", False)
    vpn_detect = settings.get("VPN Detection", False)   # Not used directly; we always show VPN/Hosting field now
    clipboard = settings.get("Link To Clipboard", False)

    # Banner
    width = get_terminal_width()
    red_banner = Fore.RED + center_text(wrap_banner_lines(ascii_banner, width), width)
    credit = Fore.RED + center_text("created by dzuma, Modified by @xx4naxx on YT", width)
    print(red_banner)
    print(credit + "\n")

    # ----- Batch Mode -----
    if batch_mode:
        file_path = input("Enter the path to the file containing IP addresses (one per line): ").strip()
        if not file_path:
            print("No file provided. Exiting.")
            return
        try:
            with open(file_path, 'r') as f:
                ips = [line.strip() for line in f if line.strip()]
            if not ips:
                print("The file is empty. Exiting.")
                return
            print(f"\nProcessing {len(ips)} IPs from {file_path}...\n")
            for ip in ips:
                print(f"{Fore.YELLOW}Processing IP: {ip}{Style.RESET_ALL}")
                if multi_api:
                    results = [
                        ("ipinfo.io", get_ipinfo_data(ip)),
                        ("ipwho.is", get_ipwhois_data(ip)),
                        ("ip-api.com", get_ipapi_data(ip))
                    ]
                    for title, result in results:
                        display_result(result, title=title)
                else:
                    result = get_ipinfo_data(ip)
                    display_result(result)
                print("\n" + "-"*width + "\n")
            return  # Batch done, exit
        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to read file: {str(e)}")
            return

    # ----- Single IP Mode -----
    ip_input = input("Enter IP address or domain (press Enter to auto-detect your public IP): ").strip()
    
    # Auto-detect own IP
    if not ip_input:
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text.strip()
            print(f"Auto-detected your public IP: {ip}")
        except:
            print("Could not detect your public IP. Please enter an IP manually.")
            return
    else:
        # Domain resolution
        resolved = resolve_domain(ip_input)
        if resolved:
            ip = resolved
            print(f"Resolved '{ip_input}' → {ip}")
        else:
            ip = ip_input

    # Use multi-API or single
    if multi_api:
        print("\nFetching data from multiple APIs...\n")
        results = [
            ("ipinfo.io", get_ipinfo_data(ip)),
            ("ipwho.is", get_ipwhois_data(ip)),
            ("ip-api.com", get_ipapi_data(ip))
        ]
        google_link = None
        for title, result in results:
            link = display_result(result, title=title)
            if link and not google_link:
                google_link = link
    else:
        print("\nUsing single API (ipinfo.io)...")
        result = get_ipinfo_data(ip)
        google_link = display_result(result)

    # ----- Copy to clipboard -----
    if clipboard and google_link:
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(google_link)
                print(f"\n{Fore.GREEN}✅ Google Maps link copied to clipboard!{Style.RESET_ALL}")
            except:
                print(f"\n{Fore.YELLOW}⚠️ Failed to copy to clipboard.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠️ pyperclip not installed. Install with: pip install pyperclip{Style.RESET_ALL}")
    elif clipboard and not google_link:
        print("\nNo Google Maps link available to copy.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"error: {e}")
    input("\nPress Enter to exit...")