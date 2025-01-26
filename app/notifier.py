import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

# telegram-bot vagy ilyesmi megközelítés?

class Notifier:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')

    def send_notification(self, printer_status, camera_image):
        try:

            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = self.recipient_email
            msg["Subject"] = "3D Printer Notification"


            body = f"Printer Status:\n\n{printer_status}"
            msg.attach(MIMEText(body, "plain"))


            img_buffer = BytesIO()
            camera_image.save(img_buffer, format="JPEG")
            img_buffer.seek(0)

            part = MIMEBase("application", "octet-stream")
            part.set_payload(img_buffer.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f"attachment; filename=camera_image.jpg"
            )
            msg.attach(part)


            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
            
            print("Email notification sent!")
        
        except Exception as ex:
            print(f"Failed to send email: {ex}")
