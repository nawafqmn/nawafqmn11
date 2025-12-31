import telebot
import re

token = ""
naq = telebot.TeleBot(token)

@naq.message_handler(commands=["start"])
def start_message(m):
    name = m.from_user.first_name
    naq.send_message(m.chat.id, f"أهلاً {name}! أرسل العملية الحسابية مباشرة.\nمثال: 5 + 5 أو 10 * 2")

@naq.message_handler(func=lambda m: True)
def calculate(m):
    text = m.text.replace('×', '*').replace('÷', '/').replace(' ', '')
    
    pattern = r'^([-+]?\d*\.?\d+)([\+\-\*/])([-+]?\d*\.?\d+)$'
    match = re.match(pattern, text)
    
    if match:
        num1 = float(match.group(1))
        op = match.group(2)
        num2 = float(match.group(3))
        
        if op == '+': result = num1 + num2
        elif op == '-': result = num1 - num2
        elif op == '*': result = num1 * num2
        elif op == '/':
            if num2 == 0:
                naq.reply_to(m, "خطأ: لا يمكن القسمة على صفر")
                return
            result = num1 / num2
        
        naq.reply_to(m, f"النتيجة: {result:g}")
    else:
        naq.reply_to(m, "عذراً، أرسل العملية بشكل صحيح (رقم أول، رمز العملية، رقم ثاني)")

naq.infinity_polling()
