
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import instaloader
import os

# Instagram kontent yuklash funksiyasi
def download_instagram_content(url):
    try:
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        if post.is_video:
            loader.download_post(post, target="downloads")
            for file in os.listdir("downloads"):
                if file.endswith(".mp4"):
                    return os.path.join("downloads", file)
        else:
            loader.download_post(post, target="downloads")
            for file in os.listdir("downloads"):
                if file.endswith(".jpg"):
                    return os.path.join("downloads", file)
    except Exception as e:
        print(f"Error: 
              {e}")
        return None

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Instagram stilkasini yuboring, men video yoki rasmni yuklab beraman!")

# Havolani qabul qilish va qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("Iltimos, kuting. Yuklab olayapman...")

    # Kontentni yuklash
    file_path = download_instagram_content(url)
    if file_path:
        await update.message.reply_text("Mana, yuklab olindi:")
        await update.message.reply_document(document=open(file_path, 'rb'))
        # Yuklangan fayllarni o'chirish
        os.remove(file_path)
    else:
        await update.message.reply_text("Kechirasiz, yuklashda xatolik yuz berdi yoki noto‘g‘ri havola yubordingiz.")

# Tokeningizni kiriting
TOKEN = "7756735190:AAFhT2oRULXHi0gXFd3LWUraE-Fa2R5AdKQ"

if __name__ == "__main__":
    # Botni ishga tushirish
    app = ApplicationBuilder().token(TOKEN).build()

    # Komandalarni qo‘shish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()
