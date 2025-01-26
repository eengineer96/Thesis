import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
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
        self.controller = controller
        self.notifier = Notifier()
        self.tolerance = 70.0  
        self.persistence = 10
        self.nok_counter = 0
        self.auto_mode = False  

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

        self.tolerance_slider = ctk.CTkSlider(self.left_panel, from_=50, to=100, command=self.update_tolerance)
        self.tolerance_slider.set(self.tolerance)
        self.tolerance_slider.grid(row=0, column=0, padx=10, pady=10)
        self.tolerance_label = ctk.CTkLabel(self.left_panel, text=f"Confidence Tolerance: {self.tolerance:.1f}%")
        self.tolerance_label.grid(row=1, column=0, padx=10, pady=5)

        self.persistence_slider = ctk.CTkSlider(self.left_panel, from_=1, to=20, command=self.update_persistence)
        self.persistence_slider.set(self.persistence)
        self.persistence_slider.grid(row=2, column=0, padx=10, pady=10)
        self.persistence_label = ctk.CTkLabel(self.left_panel, text=f"Persistence Tolerance: {self.persistence}")
        self.persistence_label.grid(row=3, column=0, padx=10, pady=5)

        self.mode_toggle = ctk.CTkSwitch(
            self.left_panel, text="Automatic Mode", command=self.toggle_mode
        )
        self.mode_toggle.grid(row=4, column=0, padx=10, pady=10)

        self.gcode_textbox = ctk.CTkTextbox(self.left_panel, width=100, height=100)
        self.gcode_textbox.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        
        self.send_button = ctk.CTkButton(self.left_panel, text="Send G-code", command=self.send_gcode)
        self.send_button.grid(row=6, column=0, padx=10, pady=5)
        
        self.notify_button = ctk.CTkButton(self.left_panel, text="Send Notification", command=self.send_notification)
        self.notify_button.grid(row=7, column=0, padx=10, pady=5)
        
        self.close_button = ctk.CTkButton(self.left_panel, text="Close", command=self.close_app)
        self.close_button.grid(row=8, column=0, padx=10, pady=10, sticky="s")
        
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
        result, confidence, persistent_anomaly = self.controller.evaluate_model()
        result_color = 'green' if result == "OK" else 'red'
        self.result_label.configure(
            text=f'Prediction: {result}\nConfidence: {confidence:.2f}%', text_color=result_color
        )

        if persistent_anomaly:
                self.notifier.send_notification(self.controller.get_printer_status(), self.controller.get_camera_frame())
                if self.auto_mode:
                        self.controller.stop_printer()
                
                self.controller.reset_counter()

        self.after(self.MODEL_EVALUATION_INTERVAL, self.evaluate_model)

    def update_tolerance(self, value):
        self.controller.tolerance = float(value)
        self.tolerance_label.configure(text=f"Confidence Tolerance: {self.controller.tolerance:.1f}%")

    def update_persistence(self, value):
        self.controller.persistence = int(value)
        self.persistence_label.configure(text=f"Persistence Tolerance: {self.controller.persistence}")

    def toggle_mode(self):
        self.auto_mode = not self.auto_mode
        mode_text = "Automatic Mode" if self.auto_mode else "Manual Mode"
        self.mode_toggle.configure(text=mode_text)

    def send_gcode(self):
        gcode_command = self.gcode_textbox.get("1.0", "end").strip()
        if gcode_command:
            self.controller.send_gcode(gcode_command)
            self.gcode_textbox.delete("0.0", "end")

    def send_notification(self):
        printer_status = self.controller.printer.get_printer_status()
        frame = self.controller.get_camera_frame()
        frame_image = Image.fromarray(frame).convert("RGB")
        self.notifier.send_notification(printer_status, frame_image)

    def close_app(self):
        self.controller.shutdown()
        self.destroy()
