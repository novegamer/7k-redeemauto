from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='../public')

OFFICIAL_CODES = [
    "SUNWUKONGNO1", "HAPPYNEWYEAR2026", "7S7E7V7E7N7", "DANCINGPOOKI", 
    "BRANZEBRANSEL", "GRACEOFCHAOS", "SENAHAJASENA", "CHAOSESSENCE", 
    "77EVENT77", "100MILLIONHEARTS", "KEYKEYKEY", "POOKIFIVEKINDS", 
    "LETSGO7K", "GOLDENKINGPEPE", "HALFGOODHALFEVIL", "DELLONSVSKRIS", 
    "TARGETWISH", "OBLIVION", "SENASTARCRYSTAL", "SENA77MEMORY"
]

# Headers ที่เลียนแบบการใช้งานจริงเพื่อให้ของเข้าเกม
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://coupon.netmarble.com",
    "Referer": "https://coupon.netmarble.com/tskgb",
    "Accept-Language": "th-TH,th;q=0.9"
}

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/get-codes', methods=['GET'])
def get_codes():
    return jsonify({"codes": OFFICIAL_CODES})

# ขั้นตอนสำคัญ: Inquiry เพื่อให้เซิร์ฟเวอร์ยอมรับการส่งของ
@app.route('/api/inquiry', methods=['POST'])
def inquiry():
    pid = request.json.get('pid')
    url = "https://coupon.netmarble.com/api/coupon/inquiry"
    params = {"gameCode": "tskgb", "langCd": "TH_TH", "pid": pid}
    resp = requests.get(url, params=params, headers=HEADERS)
    return jsonify(resp.json())

@app.route('/api/redeem', methods=['POST'])
def redeem():
    try:
        data = request.json
        url = "https://coupon.netmarble.com/api/coupon/reward"
        params = {
            "gameCode": "tskgb",
            "couponCode": data.get('code').strip(),
            "langCd": "TH_TH",
            "pid": data.get('pid')
        }
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        return jsonify(resp.json())
    except:
        return jsonify({"errorCode": 403, "errorMessage": "Connection Error"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
