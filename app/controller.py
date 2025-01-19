from picamera2 import Picamera2
from printer import Printer
from model_evaluator import ModelEvaluator
from PIL import Image

class Controller:
    def __init__(self):
        self.camera = Picamera2()
        self.camera_config = self.camera.create_still_configuration(main={"size": (640, 480)})
        self.camera.configure(self.camera_config)
        self.camera.start()

        model_path = '/home/LaszloPota/Desktop/Thesis/app/model.pth'
        self.model_evaluator = ModelEvaluator(model_path)
        self.printer = Printer()

    def get_camera_frame(self):
        return self.camera.capture_array()

    def evaluate_model(self):
        frame = self.get_camera_frame()
        frame_image = Image.fromarray(frame)
        frame_image = frame_image.convert("RGB")
        result, confidence = self.model_evaluator.evaluate(frame_image)
        return result, confidence

    def send_gcode(self, command):
        self.printer.send_gcode_command(command)

    def shutdown(self):
        self.camera.stop()
