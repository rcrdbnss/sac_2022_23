import requests

basePath = 'http://localhost:8080'
api = 'api/v1'

rsp = requests.get(f'{basePath}/{api}/car/111')
print(rsp.status_code, rsp.json())

rsp = requests.get(f'{basePath}/{api}/car/121')
print(rsp.status_code)

# rsp = requests.post(f'{basePath}/{api}/car/333', json={
# 			'make': 'Fiat',
# 			'model': 'Panda',
# 			'cc': 2200,
# 			'cv': 160,
# 			'engine': 'petrol',
# 			'price': 11000.,
# 			'used': False
# })
# print(rsp.status_code)

rsp = requests.post(f'{basePath}/{api}/user/selling', json={
			'name': 'Jane',
			'surname': 'Doe',
			'email': 'janedoe@gmail.com',
			'selling': [
				{
					'car_id': '333',
					'car_details': {
						'make': 'Fiat',
						'model': 'Panda',
						'cc': 2200,
						'cv': 160,
						'engine': 'petrol',
						'price': 11000.,
						'used': False
					}
				}
			]
})
print(rsp.status_code)
