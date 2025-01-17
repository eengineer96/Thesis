import customtkinter as ctk
from customtkinter import CTkImage
from picamera2 import Picamera2
from PIL import Image, ImageTk
from model_evaluator import ModelEvaluator

MODEL_EVALUATION_INTERVAL = 1000
CAMERA_UPDATE_INTERVAL = 100

class CameraApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Anomaly Detection")
        self.geometry("800x600")
        self.pack_propagate(False)
        
        self.camera = Picamera2()
        self.camera_config = self.camera.create_still_configuration(main={"size": (640, 480)})
        self.camera.configure(self.camera_config)
        self.camera.start()
        
        model_path = '/home/LaszloPota/Desktop/Thesis/app/model.pth'
        self.model_evaluator = ModelEvaluator(model_path)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        
        self.camera_label = ctk.CTkLabel(self, text="", image=None, width=640, height=480)
        self.camera_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.result_label = ctk.CTkLabel(self, text="Prediction: ", font=("Arial", 16))
        self.result_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.close_button = ctk.CTkButton(self, text="Close", command=self.close_app)
        self.close_button.grid(row=2, column=0, padx=20, pady=10)
        
        self.update_camera_feed()
        
        self.evaluate_model()

    def update_camera_feed(self):
        frame = self.camera.capture_array()

        frame_image = Image.fromarray(frame)
        frame_image = frame_image.convert("RGB")
        
        #frame_tk = ImageTk.PhotoImage(frame_image)
        frame_ctk_image = CTkImage(light_image=frame_image, size=(640, 480))
        self.camera_label.configure(image=frame_ctk_image)
        self.camera_label.image = frame_ctk_image
        
        self.after(CAMERA_UPDATE_INTERVAL, self.update_camera_feed)

    def evaluate_model(self):
        frame = self.camera.capture_array()
        frame_image = Image.fromarray(frame)
        frame_image = frame_image.convert("RGB")
        
        result, confidence = self.model_evaluator.evaluate(frame_image)
        result_color = 'green' if result == "OK" else 'red'
        self.result_label.configure(text=f'Prediction: {result}\nConfidence: {confidence:.2f}%', text_color=result_color)

        self.after(MODEL_EVALUATION_INTERVAL, self.evaluate_model)
    
    def close_app(self):
        self.camera.stop()
        self.destroy()

if __name__ == "__main__":
    app = CameraApp()
    app.mainloop()
