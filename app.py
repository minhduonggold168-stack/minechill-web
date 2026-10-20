import time
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Thông tin máy chủ Minechill Network
SERVER_INFO = {
    "name": "Minechill Network",
    "ip_java": "play.minechill.vn",
    "ip_bedrock": "pe.minechill.vn",
    "port_bedrock": 19132,
    "port_java": 25565,
    "version": "1.20.x - 1.21.x",
    "discord": "https://discord.gg/minechill",
    "facebook": "https://facebook.com/minechill.vn",
}

# Cache kết quả API để tránh rate limit mcsrvstat
cache_data = None
last_cache_time = 0
CACHE_DURATION = 30  # 30 giây

def fetch_server_status():
    global cache_data, last_cache_time
    now = time.time()
    
    if cache_data and (now - last_cache_time < CACHE_DURATION):
        return cache_data
    
    api_url = f"https://api.mcsrvstat.us/3/{SERVER_INFO['ip_java']}"
    status_result = {
        "online": False,
        "ip_java": SERVER_INFO["ip_java"],
        "ip_bedrock": SERVER_INFO["ip_bedrock"],
        "port_bedrock": SERVER_INFO["port_bedrock"],
        "version": SERVER_INFO["version"],
        "players": {
            "online": 0,
            "max": 500,
            "list": []
        },
        "motd": "Minechill Network • Máy chủ Minecraft Sinh Tồn Đỉnh Cao",
        "icon": None,
        "ping": 18,
        "cached": False,
        "timestamp": int(now)
    }

    try:
        response = requests.get(
            api_url,
            headers={"User-Agent": "MinechillShowcase/1.0"},
            timeout=4
        )
        if response.status_code == 200:
            data = response.json()
            is_online = data.get("online", False)
            status_result["online"] = is_online
            
            if is_online:
                players_data = data.get("players", {})
                status_result["players"]["online"] = players_data.get("online", 0)
                status_result["players"]["max"] = players_data.get("max", 500)
                status_result["players"]["list"] = players_data.get("list", [])
                
                version_info = data.get("version", SERVER_INFO["version"])
                status_result["version"] = version_info
                
                motd_data = data.get("motd", {})
                if "clean" in motd_data and motd_data["clean"]:
                    status_result["motd"] = " ".join(motd_data["clean"])
                
                if "icon" in data:
                    status_result["icon"] = data["icon"]
            else:
                # Nếu API mcsrvstat báo false (có thể server đang bảo trì hoặc DNS SRV đang trỏ)
                # Ta vẫn giữ cấu trúc phản hồi sạch sẽ
                status_result["motd"] = "Minechill Network • Hệ Thống Đang Bảo Trì Hoặc Cập Nhật"
            
            cache_data = status_result
            last_cache_time = now
            return status_result
    except Exception as e:
        print(f"[Warning] Không thể lấy trạng thái từ mcsrvstat: {e}")

    # Fallback nếu gọi API thất bại
    if cache_data:
        return cache_data
    return status_result

@app.route("/")
def index():
    status = fetch_server_status()
    return render_template("index.html", server=SERVER_INFO, status=status)

@app.route("/api/status")
def api_status():
    status = fetch_server_status()
    return jsonify(status)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Khởi động Flask Server Minechill Showcase tại port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
