from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rss.fetcher import (
    fetch_menu_all_news,
    fetch_menu_company_news,
    fetch_menu_digests
)

TOKEN = "7550975205:AAH7_-8ZsBBUXJxX-8uqijihGN5_XKFvv3E"  # замените на реальный токен

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else "—"
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    user_id = user.id

    print(f"[USER] {full_name} ({username}), ID: {user_id} начал работу с ботом.")

    await update.message.reply_text(
        "Привет! Я новостной бот. Используй /help для списка команд."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — запустить бота\n"
        "/help — список команд\n"
        "/all — все свежие новости\n"
        "/company — новости по компаниям\n"
        "/digest — тематический дайджест"
    )

async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = fetch_menu_all_news()
    for item in news:
        await update.message.reply_text(f"📰 {item['заголовок']}\n🔗 {item['ссылка']}")

async def send_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = fetch_menu_company_news()
    for item in news:
        await update.message.reply_text(f"🏢 {item['заголовок']}\n🔗 {item['ссылка']}")

async def send_digest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = fetch_menu_digests()
    for item in news:
        await update.message.reply_text(f"📌 {item['заголовок']}\n🔗 {item['ссылка']}")
        
async def send_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Бот автоматически собирает и фильтрует свежие экономические новости из проверенных источников: "
        "РБК, Коммерсант, Finam, SmartLab и Тинькофф-журнал. Поддерживает команды: /all — общая лента, /digest — ключевые события, "
        "/company — новости по компаниям из списка. Ориентирован на инвесторов и аналитиков. Автор: @Yury_Anatolich, 2025."
    )
    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("all", send_all))
    app.add_handler(CommandHandler("company", send_company))
    app.add_handler(CommandHandler("digest", send_digest))
    app.add_handler(CommandHandler("about", send_about))
    
    print("[INFO] Бот успешно запущен. Ожидаю команды...")    # <–– добавим это
    
    app.run_polling()

if __name__ == "__main__":
    main()
