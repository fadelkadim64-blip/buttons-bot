
import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# التوكن من Secrets (لا تضع التوكن هنا أبداً)
BOT_TOKEN = "8522939406:AAEGI-qLm8YGN4Tnz9qySXUY-kZMkzr6HL8"

# الأدمنز المسموح لهم
ADMINS = {
    1481797855,
    6261348215,
    8201888024
}

# قاعدة البيانات
db = sqlite3.connect("data.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT UNIQUE
)
""")
db.commit()


def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


# ===== لوحة التحكم =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    keyboard = [
        [InlineKeyboardButton("➕ إضافة قناة", callback_data="add_channel")],
        [InlineKeyboardButton("📋 عرض القنوات", callback_data="list_channels")],
        [InlineKeyboardButton("📝 نشر بوست", callback_data="post")]
    ]

    await update.message.reply_text(
        "📊 لوحة التحكم",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===== الأزرار =====
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        return

    if query.data == "add_channel":
        context.user_data["await_channel"] = True
        await query.message.reply_text(
            "أرسل معرف القناة بعد إضافة البوت أدمن:\n"
            "`-100xxxxxxxxxx`",
            parse_mode="Markdown"
        )

    elif query.data == "list_channels":
        cur.execute("SELECT chat_id FROM channels")
        rows = cur.fetchall()

        if not rows:
            await query.message.reply_text("❌ لا توجد قنوات محفوظة.")
        else:
            text = "📢 القنوات المختارة:\n\n"
            for r in rows:
                text += f"{r[0]}\n"
            await query.message.reply_text(text)

    elif query.data == "post":
        context.user_data["await_post"] = True
        await query.message.reply_text(
            "✏️ أرسل الآن:\n"
            "- نص فقط\n"
            "- أو صورة/فيديو مع نص"
        )


# ===== استقبال الرسائل =====
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    # حفظ قناة
    if context.user_data.get("await_channel"):
        chat_id = update.message.text.strip()
        cur.execute(
            "INSERT OR IGNORE INTO channels(chat_id) VALUES(?)",
            (chat_id,)
        )
        db.commit()
        context.user_data["await_channel"] = False
        await update.message.reply_text("✅ تم حفظ القناة بنجاح.")
        return

    # نشر بوست
    if context.user_data.get("await_post"):
        cur.execute("SELECT chat_id FROM channels")
        channels = [row[0] for row in cur.fetchall()]

        for ch in channels:
            if update.message.text:
                await context.bot.send_message(
                    chat_id=ch,
                    text=update.message.text,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔗 رابط", url="https://example.com")]
                    ])
                )

            elif update.message.photo:
                await context.bot.send_photo(
                    chat_id=ch,
                    photo=update.message.photo[-1].file_id,
                    caption=update.message.caption or ""
                )

            elif update.message.video:
                await context.bot.send_video(
                    chat_id=ch,
                    video=update.message.video.file_id,
                    caption=update.message.caption or ""
                )

        context.user_data["await_post"] = False
        await update.message.reply_text("🚀 تم النشر في جميع القنوات.")


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN غير موجود في Secrets")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.ALL, messages))

    app.run_polling()


if __name__ == "__main__":
    main()
