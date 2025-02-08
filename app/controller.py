from picamera2 import Picamera2
from printer import Printer
from model_evaluator import ModelEvaluator
from PIL import Image
from telegram_notifier import TelegramNotifier

class Controller:
    def __init__(self):
        self.camera = Picamera2()
        self.camera_config = self.camera.create_still_configuration(main={"size": (640, 480)})
        self.camera.configure(self.camera_config)
        self.camera.start()

        model_path = '/home/LaszloPota/Desktop/Thesis/app/model.pth'
        self.model_evaluator = ModelEvaluator(model_path)
        self.printer = Printer()
        #self.telegram_notifier = TelegramNotifier()

        self._tolerance = 80
        self._persistence = 10
        self._mode = False
        self._nok_counter = 0
    
    
    @property
    def mode(self):
        return self._mode
        
    @mode.setter       
    def mode(self, value):
        self._mode = value
        
    @property
    def nok_counter(self):
        return self._nok_counter
        
    @nok_counter.setter       
    def nok_counter(self, value):
        self._nok_counter = int(value)
    
    @property
    def tolerance(self):
        return self._tolerance

    @tolerance.setter
    def tolerance(self, value):
        self._tolerance = float(value)

    @property
    def persistence(self):
        return self._persistence
        
    @persistence.setter	
    def persistence(self, value):
        self._persistence = int(value)
        
    def reset_counter(self):
        self.nok_counter = 0
    
    def get_camera_frame(self):
        return self.camera.capture_array()

    def evaluate_model(self):
        frame = self.get_camera_frame()
        frame_image = Image.fromarray(frame)
        frame_image = frame_image.convert("RGB")
        result, confidence = self.model_evaluator.evaluate(frame_image)
        
        if result != "OK" and confidence >= self.tolerance:
            self.nok_counter += 1
        else:
            self.nok_counter = 0
			
        persistent_anomaly = self.nok_counter >= self.persistence
        
        if persistent_anomaly:
            self.stop_printer()
        
        return result, confidence, persistent_anomaly
        
    def stop_printer(self):
        try:
            self.printer.send_gcode_command(self.printer.PRINT_END) 
            print("Printer stopped due to anomaly detection.")
        except Exception as ex:
            print(f"Failed to stop the printer: {ex}")

    def send_gcode(self, command):
        self.printer.send_gcode_command(command)

    def shutdown(self):
        self.camera.stop()
