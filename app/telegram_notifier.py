import os
import asyncio
from io import BytesIO
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from PIL import Image

load_dotenv()

class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Add to .env
        self.chat_id = int(os.getenv("TELEGRAM_CHAT_ID"))  # Convert to int
        self.bot = Bot(token=self.bot_token)
        telegram_notifier = TelegramNotifier()
        telegram_notifier.start_bot()

    async def send_notification(self, printer_status, camera_image):
        try:
            message = f"? 3D Printer Notification ?\n\n? *Status:*\n{printer_status}"
            await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode="Markdown")

            img_buffer = BytesIO()
            camera_image.save(img_buffer, format="JPEG")
            img_buffer.seek(0)

            await self.bot.send_photo(chat_id=self.chat_id, photo=img_buffer, caption="? Camera Snapshot")
            print("? Telegram notification sent!")

        except Exception as ex:
            print(f"? Failed to send Telegram notification: {ex}")

    async def start_command(self, update: Update, context: CallbackContext):
        """Handles the /start command."""
        if update.message.chat_id == self.chat_id:
            await update.message.reply_text("? Bot is online! Send /status to check printer status.")
        else:
            await update.message.reply_text("? You are not authorized to use this bot.")

    async def status_command(self, update: Update, context: CallbackContext):
        """Handles the /status command to check printer status."""
        if update.message.chat_id == self.chat_id:
            printer_status = "? Printer is running smoothly!"
            await update.message.reply_text(printer_status)
        else:
            await update.message.reply_text("? You are not authorized to use this bot.")

    async def stop_command(self, update: Update, context: CallbackContext):
        """Handles the /stop command to stop the printer."""
        if update.message.chat_id == self.chat_id:
            await update.message.reply_text("? Stopping printer... (Simulated)")
        else:
            await update.message.reply_text("? You are not authorized to use this bot.")

    async def unknown_command(self, update: Update, context: CallbackContext):
        """Handles unknown commands."""
        await update.message.reply_text("? Unknown command. Use /status or /stop.")

    async def start_bot(self):
        """Starts the bot and listens for commands."""
        app = Application.builder().token(self.bot_token).build()

        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("status", self.status_command))
        app.add_handler(CommandHandler("stop", self.stop_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.unknown_command))

        print("? Bot is listening for commands...")
        await app.run_polling()

