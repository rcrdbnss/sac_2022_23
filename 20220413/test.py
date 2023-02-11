import requests

basePath = 'http://localhost:8080'
# basePath = 'https://api-dot-rbenassi-20220413.nw.r.appspot.com'
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

rsp = requests.post(f'{basePath}/{api}/user/selling', json={
			'name': 'Mario',
			'surname': 'Rossi',
			'email': 'mariorossi@gmail.com',
			'selling': [
				{
					'car_id': '330',
					'car_details': {
						'make': 'Fiat',
						'model': 'Panda',
						'cc': 2200,
						'cv': 160,
						'engine': 'petrol',
						'price': 10500.,
						'used': False
					}
				}
			]
})
print(rsp.status_code)

rsp = requests.post(f'{basePath}/{api}/user/selling', json={
			'name': 'Luigi',
			'surname': 'Verdi',
			'email': 'luigiverdi@gmail.com',
			'selling': [
				{
					'car_id': '110',
					'car_details': {
						'make': 'Alfa Romeo',
						'model': 'Giulia',
						'cc': 2200,
						'cv': 160,
						'engine': 'diesel',
						'price': 38000,
						'used': False
					}
				}
			]
})
print(rsp.status_code)
