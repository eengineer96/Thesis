from picamera2 import Picamera2
from PIL import Image
import asyncio
import time
import threading

class Controller:
    NOTIFICATION_RESET_TIME = 300000
    MODEL_EVALUATION_INTERVAL = 3000
    CAMERA_UPDATE_INTERVAL = 100
    
    def __init__(self, telegram_notifier, gui, printer, model_evaluator):
        """Initializes the Controller class with the camera, the provided telegram notifier, GUI, printer, and model evaluator."""
        self.camera = Picamera2()
        self.camera_config = self.camera.create_still_configuration(main={"size": (640, 480)})
        self.camera.configure(self.camera_config)
        self.camera.start()

        self.model_evaluator = model_evaluator
        self.printer = printer
        self.telegram_notifier = telegram_notifier
        self.gui = gui
        
        self.telegram_notifier.start_bot()

        self._tolerance = 90
        self._persistence = 10
        self._mode = False
        self._nok_counter = 0
        self._result = ""
        self._confidence = 0
        self._persistent_anomaly = 0
        self._notification_sent_flag = False
        self._stop_sent_flag = False
    
    
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
        
    @property
    def result(self):
        return self._result
        
    @result.setter	
    def result(self, value):
        self._result = value
    
    @property
    def confidence(self):
        return self._confidence
        
    @confidence.setter	
    def confidence(self, value):
        self._confidence = float(value)
        
    @property
    def persistent_anomaly(self):
        return self._persistent_anomaly
        
    @persistent_anomaly.setter	
    def persistent_anomaly(self, value):
        self._persistent_anomaly = value
    
    @property
    def nok_counter(self):
        return self._nok_counter
        
    @nok_counter.setter	
    def nok_counter(self, value):
        self._nok_counter = value

    @property
    def stop_sent_flag(self):
        return self._stop_sent_flag
        
    @stop_sent_flag.setter	
    def stop_sent_flag(self, value):
        self._stop_sent_flag = value
        print(f"Stop sent flag set to: {value}")
        
    def reset_counter(self):
        """Resets the NOK counter to zero."""
        self.nok_counter = 0
    
    def reset_notification_flag(self):
        """Resets the notification sent flag after the given time period."""
        self._notification_sent_flag = False
    
    def get_camera_frame(self):
        """Captures a frame from the camera."""
        return self.camera.capture_array()
        
    def evaluate_model(self):
        """Evalutes the current frame with the model and checks the result with other helper methods."""
        frame = self.get_camera_frame()
        frame_image = Image.fromarray(frame)
        frame_image = frame_image.convert("RGB")
        
        if not self._stop_sent_flag:
            self.result, self.confidence = self.model_evaluator.evaluate(frame_image)
        
            self.calculate_nok_counter()
        
            self.evaluate_anomaly_persistence(frame_image)
        
            self.gui.update_evaluation_values(self.result, self.confidence)
        self.gui.after(self.MODEL_EVALUATION_INTERVAL, self.evaluate_model)
    
    def calculate_nok_counter(self):
        """Updates the NOK counter based on the evaluation result."""
        if self.result != "OK" and self.confidence >= self.tolerance:
            self.nok_counter += 1
        else:
            self.nok_counter = 0
    
    def evaluate_anomaly_persistence(self, frame_image):
        """Checks if an anomaly has persisted long enough to trigger the notification and stop the printer."""
        self.persistent_anomaly = self.nok_counter >= self.persistence
        
        if self.persistent_anomaly:
            self.send_notification(frame_image)
            if self.mode:
                self.stop_printer()
                self.stop_sent_flag = True
    
    def send_notification(self, frame_image):
        """Sends a notification via telegram with an image if an anomaly persists."""
        if not self._notification_sent_flag:
            self._notification_sent_flag = True
            self.gui.after(self.NOTIFICATION_RESET_TIME, self.reset_notification_flag)
            asyncio.run_coroutine_threadsafe(
                self.telegram_notifier.send_notification(frame_image),
                self.telegram_notifier.loop
            )

    def stop_printer(self):
        """Stops the printer if an anomaly has persisted long enough and if it is not stopped recently."""
        try:
            self.printer.send_gcode_command(self.printer.PRINT_END) 
        except Exception as ex:
            print(f"Failed to stop the printer: {ex}")
    

    def shutdown(self):
        """Stops the camera when shutting down the application."""
        self.camera.stop()
