import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

token = ""
FlashBytesTeam = telebot.TeleBot(token)

user_data = {}

def reset_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("إعادة اللعب 🔄", callback_data="reset"))
    return markup

@FlashBytesTeam.message_handler(commands=['start'])
def start(m):
    user_id = m.chat.id
    user_data[user_id] = {
        'number': random.randint(1, 100),
        'attempts': 0
    }
    FlashBytesTeam.send_message(user_id, "أهلاً بك! لقد اخترت رقماً بين 1 و 100. حاول تخمينه الآن!")

@FlashBytesTeam.callback_query_handler(func=lambda call: call.data == "reset")
def reset_game(call):
    user_id = call.message.chat.id
    user_data[user_id] = {
        'number': random.randint(1, 100),
        'attempts': 0
    }
    FlashBytesTeam.answer_callback_query(call.id, "تم بدء لعبة جديدة!")
    FlashBytesTeam.edit_message_text("تم بدء جولة جديدة! اختر رقماً من 1 إلى 100.", user_id, call.message.message_id)

@FlashBytesTeam.message_handler(func=lambda m: m.text.isdigit())
def guess(m):
    user_id = m.chat.id
    
    if user_id not in user_data:
        user_data[user_id] = {
            'number': random.randint(1, 100),
            'attempts': 0
        }
        
    user_data[user_id]['attempts'] += 1
    correct_number = user_data[user_id]['number']
    attempts = user_data[user_id]['attempts']
    user_guess = int(m.text)
    
    if user_guess == correct_number:
        FlashBytesTeam.send_message(
            user_id, 
            f"✅ مبروك! الرقم {user_guess} هو الصحيح.\nلقد استغرقت {attempts} محاولات!", 
            reply_markup=reset_markup()
        )
        del user_data[user_id]
    elif user_guess < correct_number:
        FlashBytesTeam.send_message(user_id, f"الرقم الصحيح أكبر ⬆️\nمحاولاتك حتى الآن: {attempts}")
    else:
        FlashBytesTeam.send_message(user_id, f"الرقم الصحيح أصغر ⬇️\nمحاولاتك حتى الآن: {attempts}")

FlashBytesTeam.infinity_polling()
