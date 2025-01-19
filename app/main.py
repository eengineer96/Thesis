from controller import Controller
from gui import GUIApp
from notifier import Notifier

if __name__ == "__main__":
    notifier = Notifier()
    controller = Controller()
    app = GUIApp(controller)
    app.mainloop()
