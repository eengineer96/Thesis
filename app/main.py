from controller import Controller
from gui import GUIApp
from telegram_notifier import TelegramNotifier

if __name__ == "__main__":
    telegram_notifier = TelegramNotifier()
    controller = Controller()
    app = GUIApp(controller)
    app.mainloop()
