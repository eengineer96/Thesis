import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image

class GUI(ctk.CTk):
    CAMERA_UPDATE_INTERVAL = 100

    def __init__(self):
        """Initializes the GUI, sets window properties, and configures layout."""
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Anomaly Detection")
        self.geometry("1000x600")
        self.controller = None
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        

    def set_controller(self, controller):
        """Injection of the controller, initializing GUI elements and camera feed."""
        self.controller = controller
        self.setup_gui()
        self.update_camera_feed()
        self.controller.evaluate_model()
            
    def setup_gui(self):
        """Creates and places GUI elements: sliders, buttons, and labels."""
        self.left_panel = ctk.CTkFrame(self, width=200)
        self.left_panel.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.left_panel.columnconfigure(0, weight=1)

        self.tolerance_slider = ctk.CTkSlider(self.left_panel, from_=50, to=100, command=self.update_tolerance)
        self.tolerance_slider.set(self.controller.tolerance)
        self.tolerance_slider.grid(row=0, column=0, padx=10, pady=1)
        self.tolerance_label = ctk.CTkLabel(self.left_panel, text=f"Confidence: {self.controller.tolerance:.1f}%")
        self.tolerance_label.grid(row=1, column=0, padx=10, pady=5)

        self.persistence_slider = ctk.CTkSlider(self.left_panel, from_=1, to=20, command=self.update_persistence)
        self.persistence_slider.set(self.controller.persistence)
        self.persistence_slider.grid(row=2, column=0, padx=10, pady=10)
        self.persistence_label = ctk.CTkLabel(self.left_panel, text=f"Persistence: {self.controller.persistence}")
        self.persistence_label.grid(row=3, column=0, padx=10, pady=5)

        self.mode_toggle = ctk.CTkSwitch(self.left_panel, command=self.toggle_mode)
        self.mode_toggle.grid(row=4, column=0, padx=10, pady=10)
        self.toggle_mode_update()
        
        self.left_panel.grid_rowconfigure(5, weight=1)
        
        self.reset_button = ctk.CTkButton(self.left_panel, text="Reset anomaly flag", command=self.reset_stop_flag)
        self.reset_button.grid(row=6, column=0, padx=10, pady=5, sticky="ew")
        
        self.close_button = ctk.CTkButton(self.left_panel, text="Close", command=self.close_app)
        self.close_button.grid(row=7, column=0, padx=10, pady=10, sticky="sew")
        
        self.camera_label = ctk.CTkLabel(self, text="", image=None, width=640, height=480)
        self.camera_label.grid(row=0, column=1, padx=20, pady=20, sticky="sew")

        self.result_label = ctk.CTkLabel(self, text="Prediction: ", font=("Arial", 16))
        self.result_label.grid(row=1, column=1, padx=20, pady=10)

    def update_camera_feed(self):
        """Updates the camera feed in every interval described seconds"""
        frame = self.controller.get_camera_frame()
        frame_image = Image.fromarray(frame).convert("RGB")
        frame_ctk_image = CTkImage(light_image=frame_image, size=(640, 480))
        self.camera_label.configure(image=frame_ctk_image)
        self.camera_label.image = frame_ctk_image
        self.after(self.CAMERA_UPDATE_INTERVAL, self.update_camera_feed)

    def update_evaluation_values(self, result, confidence):
        """Updates the result label with prediction status and confidence."""
        result_color = 'green' if result == "OK" else 'red'
        self.result_label.configure(text=f'Prediction: {result}\nConfidence: {confidence:.2f}%', text_color=result_color)
    
    def update_tolerance(self, value):
        """Updates the confidence threshold based on slider value."""
        self.controller.tolerance = float(value)
        self.tolerance_label.configure(text=f"Confidence Tolerance: {self.controller.tolerance:.1f}%")

    def update_persistence(self, value):
        """Updates the persistence threshold for anomaly detection."""
        self.controller.persistence = int(value)
        self.persistence_label.configure(text=f"Persistence Tolerance: {self.controller.persistence}")

    def toggle_mode(self):
        """Toggles between automatic and manual modes."""
        self.controller.mode = not self.controller.mode
        self.toggle_mode_update()

    def toggle_mode_update(self):
        """Updates the mode toggle's label based on the current mode."""
        if self.controller.mode:
                mode_text = "Automatic"
                self.mode_toggle.select()
        else:
                mode_text = "Manual"
                self.mode_toggle.deselect()

        self.mode_toggle.configure(text=mode_text)
    
    def reset_stop_flag(self):
        """Resets the anomaly stop flag"""
        self.controller.stop_sent_flag = False

    def close_app(self):
        self.controller.shutdown()
        self.destroy()
