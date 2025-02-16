import os
import asyncio
import threading
from io import BytesIO
from dotenv import load_dotenv
from httpx import TimeoutException, NetworkError
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image
from formatter import format_data

load_dotenv()

class TelegramNotifier:
    def __init__(self):
        """Initializes the bot and its commands, starts a new loop / thread."""
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN") 
        self.chat_id = int(os.getenv("TELEGRAM_CHAT_ID"))
        self.bot = Bot(token=self.bot_token)

        self.controller = None
        
        self.application = Application.builder().token(self.bot_token).build()
        
        self.application.add_handler(CommandHandler("auto", self.auto_command))
        self.application.add_handler(CommandHandler("manual", self.manual_command))
        self.application.add_handler(CommandHandler("pause", self.pause_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("stop", self.stop_command))
        self.application.add_handler(MessageHandler(filters.TEXT, self.unknown_command))
        
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()
                
    def set_controller(self, controller):
        """Injection of the controller."""
        self.controller = controller
        
    def prepare_message(self):
        """Queries the status of 3D printer and formats it into a readable text with the formatter."""
        response = self.controller.printer.get_printer_status()
        formatted_text = format_data(response, self.controller.mode, self.controller.result, self.controller.confidence, self.controller.nok_counter)
        
        return formatted_text
    
    def is_authorized(self, chat_id):
        """Validates the messager, this function is called before every command execution."""
        return chat_id == self.chat_id
        
    async def send_notification(self, camera_image):
        """Sends a message with an image. This method is called if there is a persistent anomaly, and no notificiation has beent sent in a given time."""
        retries = 3
        for i in range(retries):
            try:
                message = "Persistent anomaly detected:"
                await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode="Markdown")

                img_buffer = BytesIO()
                camera_image.save(img_buffer, format="JPEG")
                img_buffer.seek(0)

                await self.bot.send_photo(chat_id=self.chat_id, photo=img_buffer)
                break
                
            except (TimeoutException, NetworkError) as ex:
                if i < retries - 1:
                    print(f"Retrying due to error: {ex}")
                    await asyncio.sleep(5)

            except Exception as ex:
                print(f"Failed to send Telegram notification: {ex}")
                
    async def pause_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles the /pause command. Sends the PAUSE gcode to the printer."""
        if not self.is_authorized(update.message.chat_id):
            await update.message.reply_text("You are not allowed to use this bot.")
            return
            
        retries = 3
        for i in range(retries):
            try:
                self.controller.printer.send_gcode_command(self.controller.printer.PAUSE)
                await update.message.reply_text(f"Command sent succesfully!")
                break
                
            except (TimeoutException, NetworkError) as ex:
                if i < retries - 1:
                    print(f"Retrying due to error: {ex}")
                    await asyncio.sleep(5)
                    
            except Exception as ex:
                print(f"Failed to send Telegram notification: {ex}")
                
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles the /status command. Sends an image and a few parameters."""
        if not self.is_authorized(update.message.chat_id):
            await update.message.reply_text("You are not allowed to use this bot.")
            return
        
        retries = 3
        for i in range(retries):
            try:
                message = self.prepare_message()
                frame = self.controller.get_camera_frame()
                camera_image = Image.fromarray(frame).convert("RGB")
                
                await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode="Markdown")

                img_buffer = BytesIO()
                camera_image.save(img_buffer, format="JPEG")
                img_buffer.seek(0)

                await self.bot.send_photo(chat_id=self.chat_id, photo=img_buffer)
                break

            except (TimeoutException, NetworkError) as ex:
                if i < retries - 1:
                    print(f"Retrying due to error: {ex}")
                    await asyncio.sleep(5)

            except Exception as ex:
                print(f"Failed to send Telegram notification: {ex}")

    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles the /stop command. Sends the PRINT_END gcode to the printer."""
        if not self.is_authorized(update.message.chat_id):
            await update.message.reply_text("You are not allowed to use this bot.")
            return
        if self.controller.mode:
            await update.message.reply_text("You can not send 'stop' in automatic mode!")
            return
        
        retries = 3
        for i in range(retries):
            try:
                self.controller.printer.send_gcode_command(self.controller.printer.PRINT_END)
                await update.message.reply_text(f"Command sent succesfully!")
                break
                
            except (TimeoutException, NetworkError) as ex:
                if i < retries - 1:
                    print(f"Retrying due to error: {ex}")
                    await asyncio.sleep(5)

            except Exception as ex:
                print(f"Failed to send Telegram notification: {ex}")
        
    async def auto_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles the /auto command. Sets the controller to automatic mode."""
        if not self.is_authorized(update.message.chat_id):
            await update.message.reply_text("You are not allowed to use this bot.")
            return
        
        retries = 3
        for i in range(retries):
            try:
                self.controller.mode = True
                self.controller.gui.toggle_mode_update()
                await update.message.reply_text(f"Evaluation mode is set to: {'automatic' if self.controller.mode else 'manual'}")
                break
            
            except (TimeoutException, NetworkError) as ex:
                if i < retries - 1:
                    print(f"Retrying due to error: {ex}")
                    await asyncio.sleep(5)

            except Exception as ex:
                print(f"Failed to send Telegram notification: {ex}")
        
    async def manual_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles the /manual command. Sets the controller to manual mode."""
        if not self.is_authorized(update.message.chat_id):
            await update.message.reply_text("You are not allowed to use this bot.")
            return
        
        retries = 3
        for i in range(retries):
            try:
                self.controller.mode = False
                self.controller.gui.toggle_mode_update()
                await update.message.reply_text(f"Evaluation mode is set to: {'automatic' if self.controller.mode else 'manual'}")
                break
            
            except (TimeoutException, NetworkError) as ex:
                if i < retries - 1:
                    print(f"Retrying due to error: {ex}")
                    await asyncio.sleep(5)

            except Exception as ex:
                print(f"Failed to send Telegram notification: {ex}")

    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handles any unknown commands or text received from the user."""
        await update.message.reply_text("Unknown command.")
        
    
    async def botloop_routine(self):
        """Runs the bot's polling loop to process incoming messages / commands."""
        await self.application.initialize()
        await self.application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await self.application.start()

        while True:
            await asyncio.sleep(1)
        
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()
    

    def start_bot(self):
        """Starts the bot in a separate thread."""
        tg_thread = threading.Thread(target=self.run_botloop)
        tg_thread.daemon = True
        tg_thread.start()
    
    def start_loop(self, loop):
        """Starts the asyncio event loop on the separate thread."""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def run_botloop(self):
        """Runs the bot'a event loop."""
        asyncio.run(self.botloop_starttask())
    
    async def botloop_starttask(self):
        """Start the bot loop as an asyncio task"""
        bot_routine = asyncio.create_task(self.botloop_routine())
        await bot_routine

        


