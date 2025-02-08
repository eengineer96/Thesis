from controller import Controller
from gui import GUIApp
from telegram_notifier import TelegramNotifier

if __name__ == "__main__":
	controller = Controller()
	telegram_notifier = TelegramNotifier(controller)
	app = GUIApp(controller, telegram_notifier)
	app.mainloop()
