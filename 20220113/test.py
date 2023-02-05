import requests

basePath = 'http://localhost:8080/api/v1'
# basePath = 'https://rbenassi-sac-20220113.nw.r.appspot.com/api/v1'

print(requests.get(f'{basePath}/slot/1').json())

requests.post(
	f'{basePath}/slot/2',
	json={
		'label': {
			'name': 'RandomRedWine',
			'type': 'red',
			'producer': 'Secret',
			'year': 2020,
			'price': 30.0
		},
		'quantity': 6,
		'minimum': 4
	}
)

print(requests.get(f'{basePath}/slot/2').json())

print(requests.get(f'{basePath}/labels/red').json())
