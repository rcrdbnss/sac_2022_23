import requests

basePath = 'http://localhost:8080/api/v1'
# basePath = 'https://api-dot-rbenassi-20220614.nw.r.appspot.com/api/v1'

rsp = requests.get(f'{basePath}')
print(rsp.status_code, rsp.json())

rsp = requests.post(
	f'{basePath}',
	json={

	})
print(rsp.status_code)

rsp = requests.get(f'{basePath}')
print(rsp.status_code, rsp.json())
