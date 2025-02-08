def format_data(status):
	axes_homed = status['coords']['axesHomed']
	fanpercent = status['params']['fanPercent'][0]
	bed_temp = status['temps']['extra'][0]['temp']
	hotend_temp = status['temps']['extra'][1]['temp']
	chamber_temp = status['temps']['extra'][2]['temp']
	chamber_hum = status['temps']['extra'][3]['temp']
	electronics_temp = status['temps']['extra'][4]['temp']
	electronics_hum = status['temps']['extra'][5]['temp']

	# Creating a readable text string
	formatted_text = (
		f"Status of 3D printer: \n\n"
		f"Axes Homed: {axes_homed}\n"
		f"Fan Percentage: {fanpercent}%\n"
		f"Bed Temperature: {bed_temp}C\n"
		f"Hotend Temperature: {hotend_temp}C\n"
		f"Chamber Temperature: {chamber_temp}C\n"
		f"Chamber Humidity: {chamber_hum}%\n"
		f"Electronics Temperature: {electronics_temp}C\n"
		f"Electronics Humidity: {electronics_hum}%\n"
	)

	return formatted_text
