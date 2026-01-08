from flask import Flask, request, jsonify, send_from_directory
import requests
import os

# ตั้งค่า App ให้รองรับ Render
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
    "Referer": "https://coupon.netmarble.com/tskgb",
    "Accept": "application/json"
}

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/get-codes', methods=['GET'])
def get_codes():
    return jsonify({"codes": OFFICIAL_CODES})

# แก้ไขชื่อ Endpoint ให้ตรงตามที่คุณระบุ: /api/inquiryRequest
@app.route('/api/inquiryRequest', methods=['POST'])
def inquiry_request():
    try:
        data = request.get_json()
        pid = data.get('pid')
        if not pid:
            return jsonify({"errorCode": 400, "errorMessage": "Missing PID"}), 200

        url = "https://coupon.netmarble.com/api/coupon/inquiry"
        params = {"gameCode": "tskgb", "langCd": "TH_TH", "pid": pid}
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        
        return jsonify(resp.json())
    except Exception as e:
        # แทนที่จะขึ้น 500 ให้ส่ง Error กลับไปที่หน้าเว็บแทน
        return jsonify({"errorCode": 500, "errorMessage": f"Backend Error: {str(e)}"}), 200

@app.route('/api/redeem', methods=['POST'])
def redeem():
    try:
        data = request.get_json()
        url = "https://coupon.netmarble.com/api/coupon/reward"
        params = {
            "gameCode": "tskgb",
            "couponCode": data.get('code').strip(),
            "langCd": "TH_TH",
            "pid": data.get('pid')
        }
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"errorCode": 500, "errorMessage": "Redeem Service Error"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
