import requests

basePath = 'http://localhost:8080'
# basePath = 'https://api-dot-rbenassi-20220614.nw.r.appspot.com'
api = 'api/v1'

rsp = requests.get(f'{basePath}/{api}/league/SerieAMinuscola')
print(rsp.status_code, rsp.json())

rsp = requests.get(f'{basePath}/{api}/league/BundesLigabue')
print(rsp.status_code)

rsp = requests.post(
	f'{basePath}/{api}/league/G7League', json={
		'start_date': '2023-02-12',
		'teams': [
			'Italy',
			'France',
			'Germany',
			'United Kingdom',
			'United States',
			'Japan',
			'Canada',
			'European Union'
		]
	}
)
print(rsp.status_code, rsp.json())

rsp = requests.post(
	f'{basePath}/{api}/league/G7League/Italy', json={
		'players': [
			{
				'name': 'Italy1',
				'role': 'keeper'
			},
			{
				'name': 'Italy2',
				'role': 'volante'
			},
			{
				'name': 'Italy3',
				'role': 'volante'
			},
			{
				'name': 'Italy4',
				'role': 'volante'
			},
			{
				'name': 'Italy5',
				'role': 'volante'
			},
			{
				'name': 'Italy6',
				'role': 'volante'
			},
			{
				'name': 'Italy7',
				'role': 'volante'
			},
			{
				'name': 'Italy8',
				'role': 'volante'
			},
			{
				'name': 'Italy9',
				'role': 'volante'
			},
			{
				'name': 'Italy10',
				'role': 'volante'
			}
		],
		'captain': 'Italy9'
	}
)
print(rsp.status_code)