from pprint import pprint
import requests
import yaml
import json


def ret_format(err_code, exp_sc, res_sc, exp_bd, res_bd, req_url, req_met, req_bd):
    return {'error': err_code, 
            'expected_sc': exp_sc, 
            'response_sc': res_sc, 
            'expected_bd': exp_bd, 
            'response_bd': res_bd,
            'request_url': req_url,
            'request_method': req_met,
            'request_bd': req_bd
            }

def assert_equal(r, exp_body, exp_sc, req_body=None):
    try:
        if r.status_code != exp_sc:
            return ret_format(1, exp_sc, r.status_code, exp_body, r.json(), r.request.url, r.request.method, req_body)
        if r.json() != exp_body:
            return ret_format(2, exp_sc, r.status_code, exp_body, r.json(), r.request.url, r.request.method, req_body)
        return ret_format(0, exp_sc, r.status_code, exp_body, r.json(), r.request.url, r.request.method, req_body)
    except ValueError:
        return ret_format(3, None, None, None, None, None, None, None)

class TestEndpoints():
    def __init__(self, baseurl):
        self.baseurl=baseurl
        with open('tests.yaml') as f:
            self.config=yaml.load(f, Loader=yaml.Loader)
       
    def validate_apis(self):
        rv={}
        for api in self.config:
            rv[api['api_name']]=self.execute_tests(api['tests'])
        return rv
    
    def execute_tests(self, tests):
        rv={}
        for t in tests:
            rv[t['title']]=self.execute_test(t)
        return rv

    def execute_test(self, t):
        t['exp_body']= None if 'exp_body' not in t.keys() else json.loads(t['exp_body'])
        t['body']= None if 'body' not in t.keys() else json.loads(t['body'])
        r=None
        if 'exp_body' not in t.keys():
            t['exp_body']=None
        if t['method']=='GET':
            r=requests.get(self.baseurl+t['url'])
        elif t['method']=='POST':
            r=requests.post(self.baseurl+t['url'], json=t['body'])
        elif t['method']=='PUT':
            r=requests.put(self.baseurl+t['url'], json=t['body'])
        elif t['method']=='DELETE':
            r=requests.delete(self.baseurl+t['url'])
        #print(t['title'])
        return assert_equal(r, t['exp_body'], t['exp_rc'], req_body=t['body'])
        


if __name__ == "__main__":
    # test = TestEndpoints('https://[YOUR_PROJECT_ID].appspot.com')
    test = TestEndpoints('http://localhost:8080')
    pprint(test.validate_apis())
    
