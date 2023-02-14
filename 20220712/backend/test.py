import requests

basePath = 'http://localhost:8080'
# basePath = 'https://api-dot-rbenassi-20220614.nw.r.appspot.com'
api = 'api/v1'

rsp = requests.get(f'{basePath}/{api}/pool/000/2023-02-10')
print(rsp.status_code, rsp.json())

rsp = requests.post(
	f'{basePath}/{api}/pool/002/2023-02-10',
	json={
		"time": "08-10"
	})
print(rsp.status_code)

rsp = requests.get(f'{basePath}/{api}/pool/rsvs/2023-02-10/08-10')
print(rsp.status_code, rsp.json())
