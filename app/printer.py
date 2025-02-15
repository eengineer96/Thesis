import os
import requests
from dotenv import load_dotenv

load_dotenv()

class Printer:
	PRINTER_HOSTNAME = os.getenv("PRINTER_HOSTNAME")
	BASE_URL = f"http://{PRINTER_HOSTNAME}"
	HOMEALL= "M98 P\"homeall.g"
	PRINT_END = "M98 P\"Print_end.g\""
	PAUSE = "M98 P\"pause.g\""
	
	def get_printer_status(self):
		try:
			response = requests.get(f"{self.BASE_URL}/rr_status?type=1")
			response.raise_for_status()
			return response.json()

		except requests.RequestException as ex:
			return(f"Error fetching printer status: {ex}")
			
	def send_gcode_command(self, command):
		try:
			response = requests.get(f"{self.BASE_URL}/rr_gcode?gcode={command}")
			response.raise_for_status();
			print(f"Command '{command}' sent succesfully!")
			response = requests.get(f"{self.BASE_URL}/rr_reply")
			return response.text.strip()
			
		except requests.RequestException as ex:
			return(f"Error sending G-code command: {ex}")
		
	
