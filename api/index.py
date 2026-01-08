from flask import Flask, request, jsonify, send_from_directory
import requests
import os

# ตั้งค่าโฟลเดอร์สำหรับไฟล์หน้าบ้าน
app = Flask(__name__, static_folder='../public')

OFFICIAL_CODES = [
    "SUNWUKONGNO1", "HAPPYNEWYEAR2026", "7S7E7V7E7N7", "DANCINGPOOKI", 
    "BRANZEBRANSEL", "GRACEOFCHAOS", "SENAHAJASENA", "CHAOSESSENCE", 
    "77EVENT77", "100MILLIONHEARTS", "KEYKEYKEY", "POOKIFIVEKINDS", 
    "LETSGO7K", "GOLDENKINGPEPE", "HALFGOODHALFEVIL", "DELLONSVSKRIS", 
    "TARGETWISH", "OBLIVION", "SENASTARCRYSTAL", "SENA77MEMORY"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Origin": "https://coupon.netmarble.com",
    "Referer": "https://coupon.netmarble.com/tskgb"
}

# รันหน้าหลัก
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/get-codes', methods=['GET'])
def get_codes():
    return jsonify({"codes": OFFICIAL_CODES})

@app.route('/api/check-user', methods=['POST'])
def check_user():
    try:
        pid = request.json.get('pid')
        url = "https://coupon.netmarble.com/api/coupon/inquiry"
        params = {"gameCode": "tskgb", "langCd": "TH_TH", "pid": pid}
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        return jsonify(resp.json())
    except:
        return jsonify({"errorCode": 403, "errorMessage": "IP Blocked by Netmarble"}), 200

@app.route('/api/redeem', methods=['POST'])
def redeem():
    try:
        data = request.json
        url = "https://coupon.netmarble.com/api/coupon/reward"
        params = {
            "gameCode": "tskgb", "langCd": "TH_TH", "pid": data.get('pid'),
            "couponCode": data.get('code').strip()
        }
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        return jsonify(resp.json())
    except:
        return jsonify({"errorCode": 403, "errorMessage": "IP Blocked"}), 200

if __name__ == "__main__":
    # รันบน Render หรือ Koyeb จะใช้ Port ที่ระบบกำหนด
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
