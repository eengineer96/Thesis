import requests

class Printer:
	
	PRINTER_HOSTNAME = "pota.local"
	BASE_URL = f"http://{PRINTER_HOSTNAME}"
	# Konstansoknak fel lehetne sorolni a különböző commandokat amire szükség lehet.
	M119 = "M119" # Endstop státusz lekérdezés.
	
	def get_printer_status(self):
		try:
			response = requests.get(f"{self.BASE_URL}/rr_status?type=1")
			response.raise_for_status()
			status_data = response.json()
			return status_data
		except requests.RequestException as ex:
			# Ehelyett kell egy msgbox vagy valamit meghívni a GUI-n, hogy sikertelen
			print(f"Error fetching printer status: {ex}")
			return None
			
	def send_gcode_command(self, command):
		try:
			response = requests.get(f"{self.BASE_URL}/rr_gcode?gcode={command}")
			response.raise_for_status();
			print(f"Command '{command}' sent succesfully!")
		except requests.RequestException as ex:
			print(f"Error sending G-code command: {ex}")
		
	
