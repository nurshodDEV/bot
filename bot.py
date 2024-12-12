from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
import requests
import logging
import os

# O'zgarmas qiymatlar
BOT_TOKEN = os.getenv("BOT_TOKEN") or "7586606989:AAEd3T366ZJhz8uTLaIneDuqJ8cy5M3vLXs"
CHANNEL_USERNAME = "https://t.me/+mVMqgMKazRs4MDFi"  # Ochiq kanal uchun foydalanuvchi nomi
GROUP_CHAT_ID = -1002346907503  # Yopiq guruh yoki kanal uchun chat ID

# Loglar sozlamalari
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


# 1. START KOMANDASI
async def start(update: Update, context: CallbackContext):
    """Start komandasi - xush kelibsiz xabar va tugmalar."""
    user_id = update.effective_user.id

    # Kanalga obuna bo'lishini tekshirish
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
    params = {"chat_id": GROUP_CHAT_ID if GROUP_CHAT_ID else CHANNEL_USERNAME, "user_id": user_id}

    try:
        response = requests.get(url, params=params).json()
        logging.info(f"API Response: {response}")

        # Foydalanuvchi holatini tekshirish
        status = response.get("result", {}).get("status", "not_in_channel")

        if status in ["member", "administrator", "creator"]:
            # Agar foydalanuvchi kanalga obuna bo'lsa
            keyboard = [
                [InlineKeyboardButton("Siz allaqachon obuna bo'lgansiz", callback_data="already_subscribed")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            message = "✅"
            await update.message.reply_text(message, reply_markup=reply_markup)
        else:
            # Agar foydalanuvchi kanalga obuna bo'lmasa
            keyboard = [
                [InlineKeyboardButton("1-kanal", url=f"https://t.me/+AwJB0NXCX6Q3MDMy")],
                [InlineKeyboardButton("2-kanal", url="https://instagram.com/rukhwonm_pg")],
                [InlineKeyboardButton("✅Tasdiqlash", callback_data="check_subscription")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            message = (
               " ❌ Kechirasiz botimizdan foydalanishdan oldin ushbu kanallarga a'zo bo'lishingiz kerak. "           )
            await update.message.reply_text(message, reply_markup=reply_markup)

    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        await update.message.reply_text("Obunangizni tekshirishda xatolik yuz berdi. Keyinroq qayta urinib ko‘ring.")


# 2. OBUNANI TEKSHIRISH FUNKSIYASI
async def check_subscription_callback(update: Update, context: CallbackContext):
    """Obunani tekshirish va natijani qaytarish."""
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()  # Tugma bosilgani haqida javob

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
    params = {"chat_id": GROUP_CHAT_ID if GROUP_CHAT_ID else CHANNEL_USERNAME, "user_id": user_id}

    try:
        response = requests.get(url, params=params).json()
        logging.info(f"API Response: {response}")

        # Foydalanuvchi holati
        status = response.get("result", {}).get("status", "not_in_channel")

        if status in ["member", "administrator", "creator"]:
            await query.edit_message_text("Obuna bo'lganingiz uchun tashakkur!")
        else:
            await query.edit_message_text(
                "Siz hali kanalga qo'shilmaganga o'xshaysiz. Qo'shiling va qaytadan urinib ko'ring."            )
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        await query.edit_message_text("Obunangizni tekshirishda xatolik yuz berdi. Keyinroq qayta urinib ko‘ring.")


# 3. ASOSIY BOT FUNKSIYASINI ISHLATISH
def main():
    """Botni ishga tushirish."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Komanda va tugmalarni sozlash
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="check_subscription"))

    # Botni ishga tushirish
    application.run_polling()


if __name__ == "__main__":
    main()
