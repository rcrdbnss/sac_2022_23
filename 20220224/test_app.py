import requests

basePath = 'http://localhost:8081'

rsp = requests.get(f'{basePath}/garden/plants')
print(rsp.json())
