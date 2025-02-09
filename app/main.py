from controller import Controller
from gui import GUIApp
from telegram_notifier import TelegramNotifier
from printer import Printer
from model_evaluator import ModelEvaluator

if __name__ == "__main__":
	telegram_notifier = TelegramNotifier()
	gui = GUIApp()
	printer = Printer()
	model_evaluator = ModelEvaluator()
	controller = Controller(telegram_notifier, gui, printer, model_evaluator)
	gui.set_controller(controller)
	telegram_notifier.set_controller(controller)
		
	gui.mainloop()
