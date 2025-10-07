from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import db_sqllite as db # Per SQLite
#import db as db # Per MySQL
from fastapi import FastAPI,Request
import uvicorn
import asyncio
import os
from dotenv import load_dotenv


app_fastapi = FastAPI()
load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_name = user.first_name
    welcome_message = f"Ciao, {user_name}! Benvenuto nel bot. Usa /help per vedere i comandi disponibili."
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """Comandi disponibili:\n
/start - Avvia il bot e ricevi un messaggio di benvenuto.
/help - Mostra questo messaggio di aiuto.
/list - Mostra la tua lista della spesa.
/add <prodotto> - Aggiungi un prodotto alla tua lista della spesa.
/remove <prodotto> - Rimuovi un prodotto dalla tua lista della spesa.
/remove_all - Rimuovi tutti i prodotti dalla tua lista della spesa."""
    await update.message.reply_text(help_text)

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    user_id = user.id  # Using Telegram user ID as a unique identifier
    cnx = db.create_connection()
    if not cnx:
        await update.message.reply_text("Errore di connessione al database.")
        return
    cursor = cnx.cursor()
    items = db.lista(cursor, user_id)
    if not items:
        await update.message.reply_text("La tua lista della spesa è vuota.")
    else:
        item_list = "\n".join(f"- {item}" for item in items)
        await update.message.reply_text(f"La tua lista della spesa:\n{item_list}")
    db.close_connection(cnx)

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    nome = user.first_name
    user_id = user.id  # Using Telegram user ID as a unique identifier
    if len(context.args) == 0:
        await update.message.reply_text("Per favore, specifica il prodotto da aggiungere. Esempio: /add latte")
        return
    product = " ".join(context.args)
    cnx = db.create_connection()
    if not cnx:
        await update.message.reply_text("Errore di connessione al database.")
        return
    cursor = cnx.cursor()
    message = db.add(cursor, user_id, product,nome)
    cnx.commit()
    await update.message.reply_text(message)
    db.close_connection(cnx)

async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id  # Using Telegram user ID as a unique identifier
    if len(context.args) == 0:
        await update.message.reply_text("Per favore, specifica il prodotto da rimuovere. Esempio: /remove latte")
        return
    product = " ".join(context.args)
    cnx = db.create_connection()
    if not cnx:
        await update.message.reply_text("Errore di connessione al database.")
        return
    cursor = cnx.cursor()
    message = db.remove(cursor, user_id, product)
    cnx.commit()
    await update.message.reply_text(message)
    db.close_connection(cnx)

async def remove_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id  # Using Telegram user ID as a unique identifier
    cnx = db.create_connection()
    if not cnx:
        await update.message.reply_text("Errore di connessione al database.")
        return
    cursor = cnx.cursor()
    message = db.remove_all(cursor, user_id)
    cnx.commit()
    await update.message.reply_text(message)
    db.close_connection(cnx)

@app_fastapi.post("/webhook")
async def webhook(request: Request):
    update = Update.de_json(await request.json(), telegram_app_instance.bot)
    await telegram_app_instance.process_update(update)
    return {"status": "ok"}




def telegram_app():
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_command))
    app.add_handler(CommandHandler("add", add_command))
    app.add_handler(CommandHandler("remove", remove_command))
    app.add_handler(CommandHandler("remove_all", remove_all_command))
    return app

telegram_app_instance = telegram_app()

async def setup():
    WEBSITE_URL = os.getenv("WEBSITE_URL")
    if not WEBSITE_URL:
        raise ValueError("WEBSITE_URL is not set in environment variables.")
        
    webhook_url = f"{WEBSITE_URL}/webhook"
    await telegram_app_instance.initialize()
    await telegram_app_instance.bot.set_webhook(webhook_url)
    print(f"Webhook set to {webhook_url}")



if __name__ == '__main__':
    asyncio.run(setup())


    uvicorn.run(app_fastapi, host="0.0.0.0", port=8000)