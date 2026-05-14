from flask import Flask, render_template
from datetime import datetime
import psutil
import subprocess

SERVERS = ["127.0.0.1", "8.8.8.8", "1.1.1.1"]

app = Flask(__name__)

# CPU Usage
def get_cpu():
    return psutil.cpu_percent(interval=1)

# Memory Usage
def get_memory():
    memory = psutil.virtual_memory()
    return memory.percent

# Disk Usage
def get_disk():
    disk = psutil.disk_usage('/')
    return disk.percent

# Ping Google (Internet Check)
def ping_server(ip):
    result = subprocess.run(["ping", "-c", "1", ip], capture_output=True)
    return "UP" if result.returncode == 0 else "DOWN"

@app.route("/")
def health_check():
    server_status = {}

    for server in SERVERS:
        server_status[server] = ping_server(server)

    data = {
        "cpu": get_cpu(),
        "memory": get_memory(),
        "disk": get_disk(),
        "servers": server_status,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
