import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

"""
Will host this script on PythonAnywhere

"""

# --- Initialize Supabase Client ---

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Other config ---

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not all([TELEGRAM_TOKEN, SUPABASE_URL, SUPABASE_KEY]):
    raise ValueError("Missing required environment variables. Please check your .env file or server configuration.")


# --- Bot commands ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text(
        "Welcome to the Course Tracker Bot!\n\n"
        "Use the command /track <DEPT> <CRN> to start tracking a course.\n"
        "Example: /track ICS 202"
    )


async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Makes a tracking request entry in the supabase database for this chatter"""

    chat_id = update.message.chat_id

    try:
        dept = dept = context.args[0].upper()
        crn = context.args[1]

        data, count = supabase.table('tracking_requests').insert({
            "user_chat_id": chat_id,
            "department_code": dept,
            "crn": crn
        }).execute()

        await update.message.reply_text(f"✅ Success! I am now tracking {dept} {crn} for you.")

    except (IndexError, ValueError):
        await update.message.reply_text("❌ Invalid format. Please use: /track <DEPT> <CRN>\nExample: /track ICS 202")


def main():
    """Start the bot"""

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("track", track))

    print("Bot is running...")
    application.run_polling()



if __name__ == '__main__':
    main()