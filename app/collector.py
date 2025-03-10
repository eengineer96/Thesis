import customtkinter as ctk
from picamera2 import Picamera2
from datetime import datetime
from PIL import Image

class Collector(ctk.CTk):
    PICTURE_TAKING_INTERVAL = 60000
    
    def __init__(self):
        """Initializes the camera, layout, and widgets, and schedules the camera frame updates."""
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Data collector")
        self.geometry("800x600")
        
        self.camera = Picamera2()
        self.camera_config = self.camera.create_still_configuration(main={"size": (640, 480)})
        self.camera.configure(self.camera_config)
        self.camera.start()
        
        self.automatic_mode = False  
        self.auto_picture_event = None
        
        self.frame_label = ctk.CTkLabel(self, text="", width=640, height=480)
        self.frame_label.pack(pady=10)
        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)
        
        self.button_take_photo = ctk.CTkButton(button_frame, text="Take Photo", command=self.take_picture)
        self.button_take_photo.pack(side="left", padx=10)
        
        self.button_toggle_mode = ctk.CTkButton(button_frame, text="Switch to Auto", command=self.toggle_mode)
        self.button_toggle_mode.pack(side="left", padx=10)
        
        self.button_close_session = ctk.CTkButton(button_frame, text="Close Session", fg_color="red", command=self.close_session)
        self.button_close_session.pack(side="left", padx=10)
        
        self.update_frame()
    
    def update_frame(self):
        """Updates the displayed camera feed with the latest frame."""
        frame = self.camera.capture_array()
        image = Image.fromarray(frame)
        ctk_image = ctk.CTkImage(light_image=image, size=(640, 480))
        
        self.frame_label.configure(image=ctk_image)
        self.frame_label.image = ctk_image
        
        self.after(40, self.update_frame)
    
    def take_picture(self):
        """Captures an image with a timestamped filename"""
        filename = f"Images/IMG_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        self.camera.capture_file(filename)
        
        if self.automatic_mode:
            self.auto_picture_event = self.after(self.PICTURE_TAKING_INTERVAL, self.take_picture)
    
    def toggle_mode(self):
        """Toggles between the modes and manages the text on the button."""
        if self.automatic_mode:
            self.automatic_mode = False
            self.button_toggle_mode.configure(text="Switch to Auto")
            if self.auto_picture_event:
                self.after_cancel(self.auto_picture_event)
        else:
            self.automatic_mode = True
            self.button_toggle_mode.configure(text="Switch to Manual")
            self.take_picture()
    
    def close_session(self):
        """Stops the camera and closes the application with the button."""
        self.camera.stop()
        self.destroy()

if __name__ == "__main__":
    app = Collector()
    app.mainloop()
