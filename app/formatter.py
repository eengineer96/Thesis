def format_data(status, mode, result, confidence, nok_counter):
	"""Formats the status response got from the HTTP request and some extra data into a readable string that is sent via Telegram."""
	fanpercent = status['params']['fanPercent'][0]
	bed_temp = status['temps']['extra'][0]['temp']
	hotend_temp = status['temps']['extra'][1]['temp']
	chamber_temp = status['temps']['extra'][2]['temp']
	chamber_hum = status['temps']['extra'][3]['temp']
	electronics_temp = status['temps']['extra'][4]['temp']
	electronics_hum = status['temps']['extra'][5]['temp']

	formatted_text = (
		f"Status of 3D printer: \n\n"
		f"Fan percentage: {fanpercent}%\n"
		f"Bed temperature: {bed_temp}C\n"
		f"Hotend temperature: {hotend_temp}C\n"
		f"Chamber temperature: {chamber_temp}C\n"
		f"Chamber humidity: {chamber_hum}%\n"
		f"Electronics temperature: {electronics_temp}C\n"
		f"Electronics humidity: {electronics_hum}%\n"
		f"Evaluation mode is set to {'automatic' if mode else 'manual'}\n"
		f"Status is '{result}' with a confidence of {confidence:.2f}%\n"
		f"Anomaly is present since {nok_counter} evaluation\n"
	)

	return formatted_text
