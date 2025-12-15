
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

BOT_TOKEN = "8522939406:AAEGI-qLm8YGN4Tnz9qySXUY-kZMkzr6HL8"
CHANNEL_ID = -1003353448874

def start(update, context):
    update.message.reply_text("أهلاً! أرسل /post لإنشاء بوست.")

def post(update, context):
    keyboard = [
        [InlineKeyboardButton("اضغط هنا", callback_data="open_link")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="هذا مثال لبوست مع زر بدون إظهار الرابط عند الضغط المطوّل.",
        reply_markup=reply_markup
    )

def button(update, context):
    query = update.callback_query
    query.answer()

    if query.data == "open_link":
        query.message.reply_text("http://t.me/mynebbb_bot/f8g7dr37h8k2b9v0n9a5xi3l7s6")

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
