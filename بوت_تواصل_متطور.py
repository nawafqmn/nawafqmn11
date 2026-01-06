#by @A_L1_J

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

TOKEN = ""
ADMIN_ID = 6812207579  

bot = telebot.TeleBot(TOKEN)


DATA_FILE = 'data.json'




def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"خطأ في حفظ البيانات: {e}")

def load_data():
    default_data = {
        "admins": [ADMIN_ID],
        "channels": [],
        "users": [],
        "force_subscribe_channels": [],
        "bot_status": "on",
        "banned": []
    }

    if not os.path.exists(DATA_FILE):
        save_data(default_data)
        return default_data

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                save_data(default_data)
                return default_data

            data = json.loads(content)

            
            for key, default_value in default_data.items():
                if key not in data or not isinstance(data[key], type(default_value)):
                    data[key] = default_value

            save_data(data)
            return data

    except Exception as e:
        print(f"⚠️ خطأ في قراءة البيانات: {e}")
        save_data(default_data)
        return default_data


bot_data = load_data()


def is_admin(user_id):
	return user_id in bot_data['admins']
	
def get_admin_menu():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("👥 إدارة المستخدمين", callback_data="users"),
        InlineKeyboardButton("📢 إرسال إذاعة", callback_data="admin_broadcast")
    )
    markup.add(
        InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")
    )
    markup.add(
        InlineKeyboardButton("❌ إيقاف البوت", callback_data="bot_off"),
        InlineKeyboardButton("✅ تشغيل البوت", callback_data="bot_on")
    )
    markup.add(
        InlineKeyboardButton("🔗 الاشتراك الإجباري", callback_data="subscribed")
    )
    return markup
    

def get_force_subscribe_keyboard():
    markup = InlineKeyboardMarkup()
    for channel in bot_data.get('force_subscribe_channels', []):
        markup.add(InlineKeyboardButton(
            text=f"📲 اشترك في {channel}",
            url=f"https://t.me/{channel.replace('@', '')}"
        ))
    markup.add(InlineKeyboardButton(
        text="✅ تحقق",
        callback_data="check_subscription"
    ))
    return markup
    
    
def subscribed_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ إضافة قناة", callback_data="add_channel"),
        InlineKeyboardButton("📋 عرض القنوات", callback_data="list_channels"),
        InlineKeyboardButton('رجوع للبداية', callback_data='back')
    )
    return markup
    
    
def users_menu():
	markup = InlineKeyboardMarkup(row_width=2)
	markup.add(
        InlineKeyboardButton("🔒 حظر عضو", callback_data="ban_user"),
        InlineKeyboardButton("🔓 فك الحظر", callback_data="unban_user")
    )
	
	markup.add(
        InlineKeyboardButton("➕ إضافة أدمن", callback_data="add_admin"),
        InlineKeyboardButton("🗑️ حذف أدمن", callback_data="remove_admin"),
        InlineKeyboardButton('رجوع للبداية', callback_data='back')
    )
    
	return markup

   
   
   
    
    
    
    
@bot.message_handler(commands=['admin'])
def admin_commands(msg):
    name = msg.from_user.first_name
    if not is_admin(msg.from_user.id):
        bot.send_message(msg.chat.id, 'هذا الامر مخصص للادمن فقط')
        return

    bot.send_message(
        msg.chat.id,
        "━━━━━━━━━━━━━━━━━━━━\n"
                "✨ *لوحة تحكم الأدمن* ✨\n"
                '━━━━━━━━━━━━━━━━━━━━\n',
        reply_markup=get_admin_menu()
    )
    
    
    
    

@bot.message_handler(commands=['start'])
def start_commands(msg):
    user = msg.from_user.first_name
    user_id = msg.from_user.id

   
    if user_id in bot_data.get("banned", []):
        bot.send_message(msg.chat.id, "🚫 لقد تم حظرك من استخدام هذا البوت.")
        return

    
    if user_id not in bot_data['users']:
        bot_data['users'].append(user_id)
        save_data(bot_data)

    
    if bot_data.get("bot_status", "on") != "on" and not is_admin(user_id):
        bot.send_message(msg.chat.id, "🚫 البوت متوقف حاليًا.")
        return

    
    not_subscribed = []
    for channel in bot_data['force_subscribe_channels']:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                not_subscribed.append(channel)
        except Exception as e:
            print(f"⚠️ خطأ في التحقق من {channel}: {e}")
            not_subscribed.append(channel)

    if not_subscribed:
        bot.send_message(
            msg.chat.id,
            "🔒 يجب عليك الاشتراك في القنوات التالية لاستخدام البوت:",
            reply_markup=get_force_subscribe_keyboard()
        )
        return

    
    
    bot.send_message(msg.chat.id, text= f"اهلا عزيزي {user} ارسل رسالتك وسيتم الرد عليك قريبا")
	
	

@bot.message_handler(func= lambda m: m.from_user.id != ADMIN_ID)
def message_handler(m):
	user_id = m.from_user.id
	username = m.from_user.username or "بدون معرف"
	text = m.text
	
	
	bot.send_message(ADMIN_ID, f"📩 رسالة من\n @{username}\n (ID: {user_id}):\n\n{text}")
	bot.send_message(m.chat.id, "✅ تم إرسال رسالتك للإدارة، سيتم الرد عليك قريبًا.")
	
	
@bot.message_handler(func= lambda m: m.from_user.id == ADMIN_ID and m.reply_to_message)
def admin_reply(m):
	original_text = m.reply_to_message.text
	try:
		lines = original_text.splitlines()
		for line in lines:
			if 'ID:' in line:
				user_id = int(line.split('ID:')[1].strip().replace(")", "").replace(":", ""))
				bot.send_message(user_id, f"📬 رد الإدارة:\n{m.text}")
				bot.send_message(ADMIN_ID, "✅ تم إرسال الرد للمستخدم.")
				return
				
		bot.send_message(ADMIN_ID, "❗ لم يتم العثور على ID في الرسالة الأصلية.")
		
	except Exception as e:
		bot.send_message(ADMIN_ID, f"❌ حدث خطأ أثناء استخراج ID: {e}")
		
		
        
@bot.message_handler(func= lambda m: m.from_user.id == ADMIN_ID and not m.reply_to_message)
def warn_admin(m):
	bot.send_message(ADMIN_ID, "❗ للرد على المستخدم، اسحب رسالته لليسار ثم اكتب ردك.")


    
    
    
    
@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    user_id = call.from_user.id
    data = call.data

    if not is_admin(user_id) and data != "check_subscription":
        bot.answer_callback_query(call.id, "❌ هذا الخيار مخصص للإداريين فقط.", show_alert=True)
        return
        

    if data == "users":
        bot.edit_message_text(
    chat_id=call.message.chat.id,
    message_id=call.message.message_id,
    text="👥 إدارة المستخدمين:",
    reply_markup=users_menu()
)
        
        
    elif data == "ban_user":
    	msg = bot.send_message(call.message.chat.id, "🚫 أرسل الآن ID العضو الذي تريد حظره:")
    	bot.register_next_step_handler(msg, process_ban_user)

    elif data == "unban_user":
    	msg = bot.send_message(call.message.chat.id, "✅ أرسل الآن ID العضو الذي تريد فك حظره:")
    	bot.register_next_step_handler(msg, process_unban_user)

    elif data == "add_admin":
    	msg = bot.send_message(call.message.chat.id, "👑 أرسل ID العضو الذي تريد ترقيته إلى أدمن:")
    	bot.register_next_step_handler(msg, process_add_admin)

    elif data == "remove_admin":
    	msg = bot.send_message(call.message.chat.id, "🗑️ أرسل ID الأدمن الذي تريد حذفه:")
    	bot.register_next_step_handler(msg, process_remove_admin)
        
        
        

    elif data == "admin_broadcast":
        msg = bot.send_message(call.message.chat.id, "📝 أرسل الرسالة التي تريد إذاعتها الآن:")
        bot.register_next_step_handler(msg, broadcast_message)

    elif data == "stats":
        total_users = len(bot_data['users'])
        total_channels = len(bot_data['force_subscribe_channels'])
        bot_status = bot_data.get("bot_status", "on")
        bot.send_message(call.message.chat.id, f"📊 الإحصائيات:\n\n👥 المستخدمون: {total_users}\n📡 القنوات: {total_channels}\n⚙️ الحالة: {'✅ يعمل' if bot_status == 'on' else '❌ متوقف'}")

    elif data == "bot_off":
        bot_data["bot_status"] = "off"
        save_data(bot_data)
        bot.send_message(call.message.chat.id, "❌ تم إيقاف البوت.")

    elif data == "bot_on":
        bot_data["bot_status"] = "on"
        save_data(bot_data)
        bot.send_message(call.message.chat.id, "✅ تم تشغيل البوت.")
        
    
    elif data == "subscribed":
        msg = bot.edit_message_text(
    chat_id=call.message.chat.id,
    message_id=call.message.message_id,
    text="🔗 إدارة الاشتراك الإجباري:",
    reply_markup=subscribed_menu()
)
        
    elif data == "add_channel":
    	msg = bot.send_message(call.message.chat.id, "📝 أرسل اسم المستخدم الخاص بالقناة (مثال: @channel):")
    	bot.register_next_step_handler(msg, process_channel_add)
    
    
    elif data == "list_channels":
    	channels = bot_data.get("force_subscribe_channels", [])
    	if not channels:
    		bot.send_message(call.message.chat.id, "📭 لا توجد قنوات حالياً.")
    	else:
            markup = InlineKeyboardMarkup()
            for ch in channels:
            	markup.add(InlineKeyboardButton(f"🗑️ حذف {ch}", callback_data=f"delch|{ch}"))
            	bot.send_message(call.message.chat.id, "📋 القنوات الحالية:", reply_markup=markup)
            	
    elif data.startswith("delch|"):
    	ch = data.split("|")[1]
    	if ch in bot_data['force_subscribe_channels']:
    	 bot_data['force_subscribe_channels'].remove(ch)
    	 save_data(bot_data)
    	 bot.answer_callback_query(call.id, f"🗑️ تم حذف {ch}")
    	 bot.edit_message_text("✅ تم حذف القناة.", call.message.chat.id, call.message.message_id)
    	else:
        	bot.answer_callback_query(call.id, "⚠️ القناة غير موجودة.")
    

    elif data == "check_subscription":
        not_subscribed = []
        for channel in bot_data['force_subscribe_channels']:
            try:
                member = bot.get_chat_member(channel, user_id)
                if member.status not in ['member', 'administrator', 'creator']:
                    not_subscribed.append(channel)
            except Exception as e:
                print(f"⚠️ خطأ في التحقق من {channel}: {e}")
                not_subscribed.append(channel)

        if not_subscribed:
            bot.answer_callback_query(call.id, "❗ لم تشترك في جميع القنوات بعد.", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "✅ تم التحقق من الاشتراك بنجاح!", show_alert=True)
            bot.send_message(call.message.chat.id, "🎉 شكرًا لاشتراكك! يمكنك الآن استخدام البوت.")
            
    
    elif data == "back":
    	if is_admin(user_id):
    		bot.send_message(
        		call.message.chat.id,
        "━━━━━━━━━━━━━━━━━━━━\n"
                "✨ *لوحة تحكم الأدمن* ✨\n"
                '━━━━━━━━━━━━━━━━━━━━\n',
        reply_markup=get_admin_menu()
    )
    	

    
        
        
        
def broadcast_message(message):
    if not is_admin(message.from_user.id):
        return
    count = 0
    for user_id in bot_data['users']:
        try:
            bot.send_message(user_id, message.text)
            count += 1
        except:
            continue
    bot.send_message(message.chat.id, f"✅ تم إرسال الإذاعة إلى {count} مستخدم.")
    


def process_channel_add(message):
    if not is_admin(message.from_user.id):
        return
    username = message.text.strip()
    if not username.startswith("@"):
        bot.reply_to(message, "❗ يجب أن يبدأ اسم المستخدم بـ @")
        return
    if username in bot_data['force_subscribe_channels']:
        bot.reply_to(message, "⚠️ القناة موجودة بالفعل.")
    else:
        bot_data['force_subscribe_channels'].append(username)
        save_data(bot_data)
        bot.reply_to(message, f"✅ تمت إضافة القناة {username} بنجاح.")
        



def process_ban_user(message):
    try:
        user_id = int(message.text.strip())
        if user_id not in bot_data.get("banned", []):
            bot_data.setdefault("banned", []).append(user_id)
            save_data(bot_data)
            bot.reply_to(message, f"🚫 تم حظر المستخدم {user_id}.")
        else:
            bot.reply_to(message, "⚠️ المستخدم محظور بالفعل.")
    except:
        bot.reply_to(message, "❗ تأكد من كتابة ID صحيح.")

def process_unban_user(message):
    try:
        user_id = int(message.text.strip())
        if user_id in bot_data.get("banned", []):
            bot_data["banned"].remove(user_id)
            save_data(bot_data)
            bot.reply_to(message, f"✅ تم فك الحظر عن المستخدم {user_id}.")
        else:
            bot.reply_to(message, "⚠️ هذا المستخدم غير محظور.")
    except:
        bot.reply_to(message, "❗ تأكد من كتابة ID صحيح.")

def process_add_admin(message):
    try:
        user_id = int(message.text.strip())
        if user_id not in bot_data['admins']:
            bot_data['admins'].append(user_id)
            save_data(bot_data)
            bot.reply_to(message, f"👑 تم إضافة {user_id} كأدمن.")
        else:
            bot.reply_to(message, "⚠️ هذا المستخدم أدمن بالفعل.")
    except:
        bot.reply_to(message, "❗ تأكد من كتابة ID صحيح.")

def process_remove_admin(message):
    try:
        user_id = int(message.text.strip())
        if user_id == ADMIN_ID:
            bot.reply_to(message, "❌ لا يمكن حذف الأدمن الرئيسي.")
            return
        if user_id in bot_data['admins']:
            bot_data['admins'].remove(user_id)
            save_data(bot_data)
            bot.reply_to(message, f"🗑️ تم حذف الأدمن {user_id}.")
        else:
            bot.reply_to(message, "⚠️ هذا المستخدم ليس أدمن.")
    except:
        bot.reply_to(message, "❗ تأكد من كتابة ID صحيح.")
		
		

		

        
		
	



bot.polling()