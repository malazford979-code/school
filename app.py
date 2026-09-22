import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# توكن البوت الخاص بك الثابت والمشغل للمجموعات
BOT_TOKEN = "8734244240:AAF4LvrGYBhNsQPgykM9M5hdN7NmV9hIod4"
TELEGRAM_API_URL = f"https://telegram.org{BOT_TOKEN}/sendMessage"

@app.route('/proxy', methods=['POST'])
def telegram_proxy():
    try:
        # استقبال البيانات القادمة من السيرفر المحلي للمدرسة
        data = request.get_json()
        
        if not data or 'chat_id' not in data or 'text' not in data:
            return jsonify({"status": "error", "message": "بيانات ناقصة"}), 400
            
        chat_id = data['chat_id']
        text = data['text']
        
        # بث التقرير المجمع من السيرفر السحابي المفتوح إلى تليجرام فوراً
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        result = response.json()
        
        if result.get("ok"):
            return jsonify({"status": "success", "message": "تم البث بنجاح عبر السيرفر السحابي"}), 200
        else:
            return jsonify({"status": "error", "message": result.get("description")}), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # التشغيل المتوافق مع خوادم السحاب
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
