import random
from datetime import datetime, timedelta

# Configuration for fake logs
num_logs = 200  
ips = ["123.45.67.89", "185.220.101.4", "104.26.10.233", "8.8.8.8", "1.1.1.1", "45.137.22.9"]
ports = [22, 80, 443, 3306, 3389, 21, 23, 8080]
protocols = ["TCP", "UDP"]

start_time = datetime.now() - timedelta(days=1)

# Notice the "w" - this overwrites the old 9 lines with fresh data
with open("sample_logs.txt", "w") as f:
    for _ in range(num_logs):
        start_time += timedelta(seconds=random.randint(5, 300))
        timestamp = start_time.strftime("%b %d %H:%M:%S")
        ip = random.choice(ips)
        port = random.choice(ports)
        proto = random.choice(protocols)
        
        log_line = f"{timestamp} kali ufw: [BLOCK] IN=eth0 SRC={ip} DST=192.168.1.5 DPT={port} PROTO={proto}\n"
        f.write(log_line)

print(f"Successfully generated {num_logs} logs!")
