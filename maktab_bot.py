import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ===== SOZLAMALAR =====
TELEGRAM_TOKEN = "8691786506:AAFusRN4LyIyNx3EKxnEAQJTojmR5bTCKHk"
GEMINI_API_KEY = "AIzaSyD_IzRyp9MD-xPqXYHyxBEuUWDfDxpMYyk"

# Gemini sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ===== BUYRUQLAR =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = """
👋 *Assalomu alaykum! Men maktab yordamchi botiman!*

📚 Quyidagi buyruqlardan foydalaning:

📝 /daras — Dars ishlanma tuzish
📊 /prezentatsiya — Prezentatsiya strukturasi
✅ /test — Test savollari tuzish
❓ /savol — Har qanday savolga javob
ℹ️ /help — Yordam

*Misol:* `/daras Suv aylanishi tabiatda`
    """
    await update.message.reply_text(matn, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = """
📖 *Buyruqlar qo'llanmasi:*

📝 `/daras [mavzu]`
Misol: `/daras Kasrlar`

📊 `/prezentatsiya [mavzu]`
Misol: `/prezentatsiya Insoniyat tarixi`

✅ `/test [mavzu]`
Misol: `/test Algebra`

❓ `/savol [savol]`
Misol: `/savol Fotosintez nima?`
    """
    await update.message.reply_text(matn, parse_mode="Markdown")


async def daras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Mavzuni kiriting!\nMisol: /daras Kasrlar")
        return

    mavzu = " ".join(context.args)
    await update.message.reply_text(f"⏳ *{mavzu}* mavzusida dars ishlanma tayyorlanmoqda...", parse_mode="Markdown")

    prompt = f"""
Sen tajribali o'zbek maktab o'qituvchisisang.
"{mavzu}" mavzusida maktab uchun to'liq dars ishlanma tuzing.

Quyidagi tartibda yoz:
1. 📌 Mavzu: {mavzu}
2. 🎯 Maqsad (ta'limiy, tarbiyaviy, rivojlantiruvchi)
3. ⏰ Dars vaqti: 45 daqiqa
4. 📚 Jihozlar
5. 🔄 Dars bosqichlari:
   - Tashkiliy qism (3 daqiqa)
   - O'tilgan mavzuni takrorlash (7 daqiqa)
   - Yangi mavzu bayoni (20 daqiqa)
   - Mustahkamlash (10 daqiqa)
   - Baholash va uy vazifasi (5 daqiqa)
6. 📝 Uy vazifasi

O'zbek tilida yoz. Aniq va tushunarli bo'lsin.
"""
    try:
        response = model.generate_content(prompt)
        natija = response.text
        # Telegram 4096 belgidan ko'p qabul qilmaydi
        if len(natija) > 4000:
            natija = natija[:4000] + "\n\n... (davomi bor)"
        await update.message.reply_text(f"📝 *Dars ishlanma:*\n\n{natija}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")
        logging.error(f"Daras xatosi: {e}")


async def prezentatsiya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Mavzuni kiriting!\nMisol: /prezentatsiya Suv")
        return

    mavzu = " ".join(context.args)
    await update.message.reply_text(f"⏳ *{mavzu}* uchun prezentatsiya tayyorlanmoqda...", parse_mode="Markdown")

    prompt = f"""
"{mavzu}" mavzusida maktab o'quvchilari uchun prezentatsiya strukturasi tuzing.

10 ta slayd uchun:
- Har bir slayd nomi
- Slayddagi asosiy fikrlar (3-4 ta bullet point)
- Rasm/grafik tavsiyasi

O'zbek tilida yoz. Oddiy va tushunarli qil.
"""
    try:
        response = model.generate_content(prompt)
        natija = response.text
        if len(natija) > 4000:
            natija = natija[:4000] + "\n\n... (davomi bor)"
        await update.message.reply_text(f"📊 *Prezentatsiya strukturasi:*\n\n{natija}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")
        logging.error(f"Prezentatsiya xatosi: {e}")


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Mavzuni kiriting!\nMisol: /test Algebra")
        return

    mavzu = " ".join(context.args)
    await update.message.reply_text(f"⏳ *{mavzu}* bo'yicha test tayyorlanmoqda...", parse_mode="Markdown")

    prompt = f"""
"{mavzu}" mavzusida maktab o'quvchilari uchun 10 ta test savoli tuzing.

Har bir savol uchun:
- Savol matni
- 4 ta variant (A, B, C, D)
- To'g'ri javob

Oxirida to'g'ri javoblar kaliti.
O'zbek tilida yoz.
"""
    try:
        response = model.generate_content(prompt)
        natija = response.text
        if len(natija) > 4000:
            natija = natija[:4000] + "\n\n... (davomi bor)"
        await update.message.reply_text(f"✅ *Test savollari:*\n\n{natija}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")
        logging.error(f"Test xatosi: {e}")


async def savol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Savolni kiriting!\nMisol: /savol Fotosintez nima?")
        return

    savol_matni = " ".join(context.args)
    await update.message.reply_text(f"⏳ Javob tayyorlanmoqda...", parse_mode="Markdown")

    prompt = f"""
Sen maktab o'qituvchisisang. O'quvchiga quyidagi savolga oddiy va tushunarli javob ber:

Savol: {savol_matni}

O'zbek tilida, o'quvchiga mos tilda javob ber. Misollar keltir.
"""
    try:
        response = model.generate_content(prompt)
        natija = response.text
        if len(natija) > 4000:
            natija = natija[:4000] + "\n\n... (davomi bor)"
        await update.message.reply_text(f"💡 *Javob:*\n\n{natija}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")
        logging.error(f"Savol xatosi: {e}")


async def oddiy_xabar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buyruqsiz yozilgan xabarlarga javob"""
    xabar = update.message.text

    prompt = f"""
Sen maktab yordamchi botisan. O'quvchi yoki o'qituvchi sog'a yozdi:
"{xabar}"

Qisqa va foydali javob ber. O'zbek tilida.
Agar ta'lim bilan bog'liq bo'lsa to'liq javob ber.
"""
    try:
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("❌ Xatolik. /help buyrug'ini ko'ring.")
        logging.error(f"Xabar xatosi: {e}")


# ===== BOTNI ISHGA TUSHIRISH =====
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Buyruqlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("daras", daras))
    app.add_handler(CommandHandler("prezentatsiya", prezentatsiya))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("savol", savol))

    # Oddiy xabarlar
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, oddiy_xabar))

    print("✅ Bot ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()
