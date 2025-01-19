import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from picamera2 import Picamera2
from controller import Controller
from notifier import Notifier

class GUIApp(ctk.CTk):
    MODEL_EVALUATION_INTERVAL = 1000
    CAMERA_UPDATE_INTERVAL = 100

    def __init__(self, controller):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Anomaly Detection")
        self.geometry("1000x600")
        self.controller = controller  # Controller to manage the logic
        self.notifier = Notifier()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        self.setup_gui()
        

        self.update_camera_feed()
        self.evaluate_model()

    def setup_gui(self):
        self.left_panel = ctk.CTkFrame(self, width=200)
        self.left_panel.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.left_panel.columnconfigure(0, weight=1)

        self.gcode_textbox = ctk.CTkTextbox(self.left_panel, width=100, height=100)
        self.gcode_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.send_button = ctk.CTkButton(self.left_panel, text="Send G-code", command=self.send_gcode)
        self.send_button.grid(row=1, column=0, padx=10, pady=5)

        self.close_button = ctk.CTkButton(self.left_panel, text="Close", command=self.close_app)
        self.close_button.grid(row=2, column=0, padx=10, pady=10, sticky="s")
        
        self.notify_button = ctk.CTkButton(self.left_panel, text="Send Notification", command=self.send_notification)
        self.notify_button.grid(row=3, column=0, padx=10, pady=5)


        self.camera_label = ctk.CTkLabel(self, text="", image=None, width=640, height=480)
        self.camera_label.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.result_label = ctk.CTkLabel(self, text="Prediction: ", font=("Arial", 16))
        self.result_label.grid(row=1, column=1, padx=20, pady=10)

    def update_camera_feed(self):
        frame = self.controller.get_camera_frame()
        frame_image = Image.fromarray(frame).convert("RGB")
        frame_ctk_image = CTkImage(light_image=frame_image, size=(640, 480))
        self.camera_label.configure(image=frame_ctk_image)
        self.camera_label.image = frame_ctk_image
        self.after(self.CAMERA_UPDATE_INTERVAL, self.update_camera_feed)

    def evaluate_model(self):
        result, confidence = self.controller.evaluate_model()
        result_color = 'green' if result == "OK" else 'red'
        self.result_label.configure(text=f'Prediction: {result}\nConfidence: {confidence:.2f}%', text_color=result_color)
        self.after(self.MODEL_EVALUATION_INTERVAL, self.evaluate_model)

    def send_gcode(self):
        gcode_command = self.gcode_textbox.get("1.0", "end").strip()
        if gcode_command:
            self.controller.send_gcode(gcode_command)
            self.gcode_textbox.delete("0.0", "end")
        
    def send_notification(self):
        printer_status = self.controller.printer.get_printer_status()

        frame = self.controller.get_camera_frame()
        frame_image = Image.fromarray(frame).convert("RGB")

        recipient_email = "recipient_email@example.com"
        self.notifier.send_notification(recipient_email, printer_status, frame_image)
    
    
    def close_app(self):
        self.controller.shutdown()
        self.destroy()
