from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import instaloader
import os

# Instagram kontentni yuklash funksiyasi
def download_instagram_content(url):
    try:
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        
        # Yuklangan fayllarni saqlash uchun papka yaratish
        if not os.path.exists("downloads"):
            os.mkdir("downloads")

        if post.is_video:  # Agar video bo'lsa
            loader.download_post(post, target="downloads")
            for file in os.listdir("downloads"):
                if file.endswith(".mp4"):
                    return os.path.join("downloads", file)
        else:  # Agar rasm bo'lsa
            loader.download_post(post, target="downloads")
            for file in os.listdir("downloads"):
                if file.endswith(".jpg"):
                    return os.path.join("downloads", file)
    except Exception as e:
        print(f"Error: {e}")
        return None

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men Instagramdan video yoki rasm yuklab bera olaman.\n"
        "Iltimos, post havolasini yuboring."
    )

# Havolani qabul qilish va qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if "instagram.com" in url:  # Havola Instagramdan ekanligini tekshirish
        await update.message.reply_text("Iltimos, kuting. Yuklab olayapman...")
        file_path = download_instagram_content(url)
        if file_path:
            await update.message.reply_text("Mana, yuklab olindi:")
            await update.message.reply_document(document=open(file_path, 'rb'))
            
            # Yuklangan faylni o'chirish
            os.remove(file_path)
        else:
            await update.message.reply_text("Kechirasiz, yuklashda xatolik yuz berdi yoki noto‘g‘ri havola yubordingiz.")
    else:
        await update.message.reply_text("Bu Instagram havolasiga o‘xshamaydi. Iltimos, to‘g‘ri havola yuboring.")

# Telegram bot tokeni
TOKEN = "7756735190:AAFhT2oRULXHi0gXFd3LWUraE-Fa2R5AdKQ"

if __name__ == "__main__":
    # Botni ishga tushirish
    app = ApplicationBuilder().token(TOKEN).build()

    # /start komandasi uchun handler
    app.add_handler(CommandHandler("start", start))
    
    # Oddiy xabarlar uchun handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()
