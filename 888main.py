from googletrans import Translator
import telebot
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import pyttsx3

# إنشاء مترجم
translator = Translator()

# تحميل نموذج GPT-3 مدرب مسبقًا
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")

# بدء البوت
bot = telebot.TeleBot("7120326643:AAG1Hrcthb1ot9fZjY5ub5GiTP40djBIIyk")

# إنشاء محرك Text-to-Speech
engine = pyttsx3.init()

# قائمة الوظائف
functions_list = [
    "1. ترجمة الرسائل من اللغة المستهدفة إلى الإنجليزية",
    "2. توليد ردود باستخدام GPT-3",
    "3. ترجمة الردود من الإنجليزية إلى اللغة المستهدفة",
    "4. تحويل النص إلى كلام",
    "5. إضافة المزيد من الوظائف ..."
]

@bot.message_handler(commands=['start', 'help'])
def send_functions_list(message):
    functions_text = "\n".join(functions_list)
    bot.reply_to(message, f"قائمة الوظائف:\n{functions_text}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # تحديد اللغة وترجمة النص
    translated_message = translator.translate(message.text, dest='en').text
    
    # إعداد النص للموديل
    input_ids = tokenizer.encode(translated_message, return_tensors="pt")
    
    # توليد الرد
    output = model.generate(input_ids, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # ترجمة الرد إلى لغة المستخدم
    translated_response = translator.translate(response, dest='ar').text
    
    # تحويل النص إلى كلام وإرساله
    speak(translated_response)
    bot.reply_to(message, translated_response)

def speak(text):
    # تحويل النص إلى كلام
    engine.say(text)
    engine.runAndWait()

bot.polling()
