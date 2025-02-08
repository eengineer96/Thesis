import os
import asyncio
import threading
from io import BytesIO
from dotenv import load_dotenv
from httpx import TimeoutException, NetworkError
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image

load_dotenv()

class TelegramNotifier:
    def __init__(self, controller):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Add to .env
        self.chat_id = int(os.getenv("TELEGRAM_CHAT_ID"))  # Convert to int
        self.bot = Bot(token=self.bot_token)
        
        self.controller = controller
        
        self.application = Application.builder().token(self.bot_token).build()

        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("stop", self.stop_command))
        self.application.add_handler(CommandHandler("auto", self.auto_command))
        self.application.add_handler(CommandHandler("manual", self.manual_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.unknown_command))
        
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()
        
    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def send_notification(self, printer_status, camera_image):
        retries = 3
        for i in range(retries):
            try:
                message = f"? 3D Printer Notification ?\n\n? *Status:*\n{printer_status}"
                await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode="Markdown")

                img_buffer = BytesIO()
                camera_image.save(img_buffer, format="JPEG")
                img_buffer.seek(0)

                await self.bot.send_photo(chat_id=self.chat_id, photo=img_buffer, caption="? Camera Snapshot")
                print("? Telegram notification sent!")
                break

            except (TimeoutException, NetworkError) as e:
                if i < retries - 1:
                    print(f"Retrying due to error: {e}")
                    await asyncio.sleep(2)  # Wait before retrying
                else:
                    print(f"Failed after {retries} attempts: {e}")

            except Exception as ex:
                print(f"? Failed to send Telegram notification: {ex}")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles the /start command."""
        if update.message.chat_id == self.chat_id:
            await update.message.reply_text("? Bot is online! Send /status to check printer status.")
        else:
            await update.message.reply_text("? You are not authorized to use this bot.")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles the /status command to check printer status."""
        printer_status = self.controller.printer.get_printer_status() + f"Evaluation mode: {'automatic' if self.controller.mode else 'manual'}" # Adjust according to your method to get status
        frame = self.controller.get_camera_frame()  # Get the camera frame (replace with your actual method)
        camera_image = Image.fromarray(frame).convert("RGB")  # Convert frame to image
        
        retries = 3
        for i in range(retries):
            try:
                await self.bot.send_message(chat_id=self.chat_id, text=printer_status, parse_mode="Markdown")

                img_buffer = BytesIO()
                camera_image.save(img_buffer, format="JPEG")
                img_buffer.seek(0)

                await self.bot.send_photo(chat_id=self.chat_id, photo=img_buffer)
                print("Telegram notification sent!")
                break

            except (TimeoutException, NetworkError) as e:
                if i < retries - 1:
                    print(f"Retrying due to error: {e}")
                    await asyncio.sleep(2)  # Wait before retrying
                else:
                    print(f"Failed after {retries} attempts: {e}")

            except Exception as ex:
                print(f"? Failed to send Telegram notification: {ex}")

    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles the /stop command to stop the printer."""
        if update.message.chat_id == self.chat_id:
            response = self.controller.printer.send_gcode_command(self.controller.printer.PRINT_END)
            await update.message.reply_text(f"Printer's response: {response}")
        else:
            await update.message.reply_text("? You are not authorized to use this bot.")

    async def auto_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat_id == self.chat_id:
            self.controller.mode = True
            await update.message.reply_text(f"Evaluation mode is set to: {'automatic' if self.controller.mode else 'manual'}")
        else:
            await update.message.reply_text("? You are not authorized to use this bot.")
        
    async def manual_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat_id == self.chat_id:
            self.controller.mode = False
            await update.message.reply_text(f"Evaluation mode is set to: {'automatic' if self.controller.mode else 'manual'}")
        else:
            await update.message.reply_text("? You are not authorized to use this bot.")

    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles unknown commands."""
        await update.message.reply_text("Unknown command.")

    async def botloop_routine(self):
        """Run bot polling in an asyncio coroutine."""
        # Initialize the application (bot)
        await self.application.initialize()
        await self.application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await self.application.start()

        # Keep the bot running by continually checking
        while True:
            # This ensures the bot remains alive and responsive to commands.
            await asyncio.sleep(1)
        
        # When the loop exits, shut down the bot
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()

    async def botloop_starttask(self):
        """Start the bot loop task"""
        bot_routine = asyncio.create_task(self.botloop_routine())
        await bot_routine

    def start_bot(self):
        """Start the bot in a separate thread."""
        tg_thread = threading.Thread(target=self.run_botloop)
        tg_thread.daemon = True
        tg_thread.start()

    def run_botloop(self):
        """Start the asyncio bot loop in a new event loop for the thread."""
        asyncio.run(self.botloop_starttask())
        


