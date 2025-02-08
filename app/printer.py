import requests
from formatter import format_data

class Printer:
	
	PRINTER_HOSTNAME = "pota.local"
	BASE_URL = f"http://{PRINTER_HOSTNAME}"
	# Konstansoknak fel lehetne sorolni a különböző commandokat amire szükség lehet.
	M119 = "M119" # Endstop státusz lekérdezés.
	HOMEALL= "M98 P\"homeall.g"
	PRINT_END = "M98 P\"Print_end.g\""
	PAUSE = "M98 P\"pause.g"
	
	def get_printer_status(self):
		try:
			response = requests.get(f"{self.BASE_URL}/rr_status?type=1")
			response.raise_for_status()
			#status_data = response.json()
			formatted_text = format_data(response.json())
			return formatted_text
		except requests.RequestException as ex:
			# Ehelyett kell egy msgbox vagy valamit meghívni a GUI-n, hogy sikertelen
			print(f"Error fetching printer status: {ex}")
			return None
			
	def send_gcode_command(self, command):
		try:
			response = requests.get(f"{self.BASE_URL}/rr_gcode?gcode={command}")
			response.raise_for_status();
			print(f"Command '{command}' sent succesfully!")
			response = requests.get(f"{self.BASE_URL}/rr_reply")
			return response.text.strip()
		except requests.RequestException as ex:
			print(f"Error sending G-code command: {ex}")
		
	
