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
        download_folder = "downloads"
        if not os.path.exists(download_folder):
            os.mkdir(download_folder)

        loader.download_post(post, target=download_folder)
        
        files = [os.path.join(download_folder, f) for f in os.listdir(download_folder) if f.endswith(('.mp4', '.jpg'))]
        return files
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
        file_paths = download_instagram_content(url)
        if file_paths:
            for file_path in file_paths:
                await update.message.reply_document(document=open(file_path, 'rb'))
                os.remove(file_path)  # Yuklangan faylni o‘chirish
            
            # Papkani tozalash
            download_folder = "downloads"
            if os.path.exists(download_folder) and not os.listdir(download_folder):
                os.rmdir(download_folder)
        else:
            await update.message.reply_text("Kechirasiz, yuklashda xatolik yuz berdi yoki noto‘g‘ri havola yubordingiz.")
    else:
        await update.message.reply_text("Bu Instagram havolasiga o‘xshamaydi. Iltimos, to‘g‘ri havola yuboring.")

# Telegram bot tokeni
TOKEN = "7921541272:AAEOGb_5kK2oOo5jTfP9Wr5WSts4beGizEM"

if __name__ == "__main__":
    # Botni ishga tushirish
    app = ApplicationBuilder().token(TOKEN).build()

    # /start komandasi uchun handler
    app.add_handler(CommandHandler("start", start))
    
    # Oddiy xabarlar uchun handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()
