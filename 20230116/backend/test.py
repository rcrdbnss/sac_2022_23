import requests

basePath = 'http://localhost:8080/api/v1'
# basePath = 'https://api-dot-rbenassi-20220614.nw.r.appspot.com/api/v1'

rsp = requests.get(f'{basePath}/consumi/10-02-2023')
print(rsp.status_code, rsp.json())

rsp = requests.get(f'{basePath}/consumi/16-02-2023')
print(rsp.status_code, rsp.json())

rsp = requests.get(f'{basePath}/consumi/10022023')
print(rsp.status_code)

rsp = requests.post(
	f'{basePath}/consumi/10-03-2023',
	json={
		'value': 135
	})
print(rsp.status_code, rsp.json())

rsp = requests.post(
	f'{basePath}/consumi/10-03-2023',
	json={
		'value': "135"
	})
print(rsp.status_code, rsp.json())
