import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestChat, KeyboardButtonRequestUsers

token = ""
naq = telebot.TeleBot(token)

def nwaf_main_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn_user = KeyboardButton(
        "👤 ايدي مستخدم",
        request_users=KeyboardButtonRequestUsers(request_id=1, user_is_bot=False, max_quantity=1)
    )

    btn_channel = KeyboardButton(
        "📢 ايدي قناة",
        request_chat=KeyboardButtonRequestChat(request_id=2, chat_is_channel=True)
    )

    btn_group = KeyboardButton(
        "👥 ايدي مجموعة",
        request_chat=KeyboardButtonRequestChat(request_id=3, chat_is_channel=False)
    )

    btn_bot = KeyboardButton(
        "🤖 ايدي بوت",
        request_users=KeyboardButtonRequestUsers(request_id=4, user_is_bot=True, max_quantity=1)
    )

    markup.add(btn_user, btn_channel, btn_group, btn_bot)
    return markup

@naq.message_handler(commands=["start"])
def st(m):
    id_user = m.from_user.id
    welcome_text = f"أهلاً بك في بوت استخراج المعرفات\n\nالايدي الخاص بك هو: `{id_user}`"
    naq.send_message(m.chat.id, text=welcome_text, parse_mode="Markdown", reply_markup=nwaf_main_markup())

@naq.message_handler(content_types=['chat_shared', 'users_shared'])
def handle_shared_data(m):
    
    try:
        if m.content_type == 'chat_shared':
            final_id = m.chat_shared.chat_id
            
        else:
            data = m.users_shared.user_ids[0]
            final_id = data.get('user_id') if isinstance(data, dict) else getattr(data, 'user_id', data)

        naq.send_message(m.chat.id, f"{final_id}", parse_mode="Markdown")
        
    except Exception:
        naq.send_message(m.chat.id, "Error")
        
        

naq.polling()