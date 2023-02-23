import requests

# basePath = 'http://localhost:8080/api/v1'
basePath = 'https://api-dot-rcbns-20230223.nw.r.appspot.com/api/v1'

rsp = requests.post(f'{basePath}/clean')
print(rsp.status_code) #, rsp.json() if rsp is not None else "None")


rsp = requests.get(f'{basePath}')
print(rsp.status_code, rsp.json() if rsp is not None else "None")

rsp = requests.post(
	f'{basePath}',
	json={

	})
print(rsp.status_code)

rsp = requests.get(f'{basePath}')
print(rsp.status_code, rsp.json() if rsp is not None else "None")
