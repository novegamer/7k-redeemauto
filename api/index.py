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

# ใช้ Headers แบบ Mobile ตามที่คุณต้องการ เพื่อลดการตรวจจับ
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://coupon.netmarble.com/tskgb",
    "Origin": "https://coupon.netmarble.com"
}

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/get-codes', methods=['GET'])
def get_codes():
    return jsonify({"codes": OFFICIAL_CODES})

# แก้ไขฟังก์ชัน Inquiry ให้ปลอดภัยจากการ Crash
@app.route('/api/inquiry', methods=['POST'])
def inquiry():
    try:
        data = request.get_json()
        pid = data.get('pid')
        url = "https://coupon.netmarble.com/api/coupon/inquiry"
        params = {"gameCode": "tskgb", "langCd": "TH_TH", "pid": pid}
        
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        
        # ตรวจสอบสถานะการตอบกลับก่อน parse JSON
        if resp.status_code != 200:
            return jsonify({"errorCode": 403, "errorMessage": "เซิร์ฟเวอร์เกมปฏิเสธการเชื่อมต่อ"}), 200
        
        try:
            return jsonify(resp.json())
        except:
            return jsonify({"errorCode": 500, "errorMessage": "ข้อมูลที่ได้รับไม่ใช่ JSON"}), 200
            
    except Exception as e:
        return jsonify({"errorCode": 500, "errorMessage": str(e)}), 200

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
        
        try:
            return jsonify(resp.json())
        except:
            return jsonify({"errorCode": 403, "errorMessage": "ไม่สามารถอ่านผลการเติมได้"}), 200
            
    except Exception as e:
        return jsonify({"errorCode": 500, "errorMessage": "ระบบขัดข้อง"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
