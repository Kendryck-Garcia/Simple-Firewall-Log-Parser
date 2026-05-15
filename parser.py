import os
import re
import requests
import plotly.graph_objects as go
from collections import Counter
from dotenv import load_dotenv

# --- CONFIGURATION & SECURITY ---
# Load the hidden .env file
load_dotenv()

# Safely fetch the key from your environment
API_KEY = os.getenv("IPGEOLOCATION_API_KEY")
logfile = "sample_logs.txt"

# --- 1. SERVICE MAPPING ---
# This fulfills the "Protocol and Service Analysis" requirement
PORT_MAP = {
    "22": "SSH",
    "80": "HTTP",
    "443": "HTTPS",
    "3306": "MySQL",
    "3389": "RDP",
    "53": "DNS",
    "21": "FTP"
}

ip_list = []
port_list = []
service_list = []

print("--- Starting Advanced Log Analysis ---")

# --- 2. ROBUST MULTI-FORMAT PARSING ---
try:
    with open(logfile, "r") as file:
        for line in file:
            # Enhanced Regex to catch both UFW and standard iptables formats
            src_ip = re.search(r"SRC=([\d\.]+)", line)
            dest_port = re.search(r"DPT=(\d+)", line)

            if src_ip and dest_port:
                ip = src_ip.group(1)
                port = dest_port.group(1)
                
                ip_list.append(ip)
                port_list.append(port)
                
                # Map the port to a service name, or "Unknown" if not in our list
                service_name = PORT_MAP.get(port, f"Unknown ({port})")
                service_list.append(service_name)
except FileNotFoundError:
    print(f"Error: {logfile} not found.")
    exit()

ip_counts = Counter(ip_list)
service_counts = Counter(service_list)

# --- 3. ENRICHMENT ---
def get_ip_info(ip):
    if API_KEY == "YOUR_API_KEY_HERE": return "No API Key"
    try:
        url = f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}"
        data = requests.get(url, timeout=5).json()
        return f"{data.get('country_name')}, {data.get('isp')}"
    except: return "Lookup Failed"

# --- 4. ENHANCED REPORTING ---
print(f"\n[SERVICE ANALYSIS]")
for service, count in service_counts.items():
    print(f"- {service}: {count} hits")

print(f"\n[TOP ATTACKERS]")
for ip, count in ip_counts.items():
    location = get_ip_info(ip)
    print(f"- {ip} ({location}): {count} attempts")

# --- 5. VISUAL DASHBOARD (Service Distribution) ---
if service_counts:
    fig = go.Figure([go.Pie(
        labels=list(service_counts.keys()), 
        values=list(service_counts.values()),
        hole=.3 # Makes it a Donut Chart for extra style
    )])

    fig.update_layout(
        title="Distribution of Targeted Services",
        template="plotly_dark"
    )

    fig.write_html("security_report.html")
    print(f"\n[SUCCESS] Updated Dashboard generated: security_report.html")
