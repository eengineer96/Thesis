from controller import Controller
from gui import GUI
from telegram_notifier import TelegramNotifier
from printer import Printer
from model_evaluator import ModelEvaluator

"""
This is the main entry point for the anomaly detection application

This script initializes all the components that is necessary in the first place.
- TelegramNotifier: Sends alerts via Telegram and the user can query status from the printer.
- GUIApp: Provides a graphical user interface for tweaking the settings.
- Printer: Contains the printer's API.
- ModelEvaluator: Evaluates the model on a picture taken by the camera.
- Controller: Manages all the communication and contains the main logic.
"""


if __name__ == "__main__":
	telegram_notifier = TelegramNotifier()
	gui = GUI()
	printer = Printer()
	model_evaluator = ModelEvaluator()
	controller = Controller(telegram_notifier, gui, printer, model_evaluator)
	gui.set_controller(controller)
	telegram_notifier.set_controller(controller)
		
	gui.mainloop()
