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
		"""Retrieves the current status of the 3D printer."""
		try:
			response = requests.get(f"{self.BASE_URL}/rr_status?type=1")
			return response.json()

		except requests.RequestException as ex:
			print(f"Error requesting printer status: {ex}")
			
	def send_gcode_command(self, command):
		"""Sends a G-code command to the printer."""
		try:
			requests.get(f"{self.BASE_URL}/rr_gcode?gcode={command}")
			
		except requests.RequestException as ex:
			print(f"Error sending G-code command: {ex}")
		
	
