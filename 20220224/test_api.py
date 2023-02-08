import requests

basePath = 'http://localhost:8080'
api = 'api/v1'

rsp = requests.get(f'{basePath}/{api}/garden/plant/2022-02-23/Bonsai')
print(rsp.status_code, rsp.json())

rsp = requests.get(f'{basePath}/{api}/garden/plant/20220223/Bonsai')
print(rsp.status_code, rsp.json())

rsp = requests.post(
	f'{basePath}/{api}/garden/plant/2023-01-01/Happy%20New%20Year',
	json={
		'plant': {
			'name': 'Happy New Year',
			'sprout-time': '1 week',
			'full-growth': '1 year',
			'edible': False
		},
		'num': 1
	}
)
print(rsp.status_code)

rsp = requests.get(f'{basePath}/{api}/garden/plant/2022-02-23/Bonsai/sprout-time')
print(rsp.status_code, rsp.json())
