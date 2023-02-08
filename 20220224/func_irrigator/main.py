def hand_irrigator(data, context):
	print("Manual irrigator running for", data['value']['fields']['seconds']['integerValue'], 'seconds')


def humidity_update(data, context):
	humidity = data['value']['fields']['humidity']['doubleValue']
	if humidity < 0.30:
		print("Irrigator automatically activared by a reported humidity value below 30%")
	else:
		print("Irrigator OFF")
