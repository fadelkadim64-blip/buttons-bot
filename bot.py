from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

BOT_TOKEN = "8346106306:AAGjlzINFvNPKvng8QLUxcWJTpRwo9p6y18"
CHANNEL_ID = -1003353448874

def start(update, context):
    update.message.reply_text("أهلاً! أرسل /post لإنشاء بوست.")

def post(update, context):
    keyboard = [
        [InlineKeyboardButton("اضغط هنا", callback_data="open_link")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("هذا مثال زر", reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    query.answer()
    query.message.reply_text("تم الضغط على الزر")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("post", post))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
