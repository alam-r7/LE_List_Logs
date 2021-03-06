import requests
import json
import time
import sys

ACCOUNT_KEY = sys.argv[1]

def handle_response(resp):
    hosts = []
    host_key = {}
    response = resp
    time.sleep(1)
    if response.status_code == 200:
        account_info = eval(resp.text)
        for i in account_info['list']:
            hosts.append(i['name'])
            host_key[i['name']] = i['key']
        return hosts, host_key
    if response.status_code == 202:
        continue_request(resp)
        return
    if response.status_code > 202:
        print 'Error status code ' + str(response.status_code)
        return

def make_request(provided_url=None, hosts=None):
    if hosts:
        url = "http://api.logentries.com/%s/hosts/%s/" % (ACCOUNT_KEY, hosts)
    else:
        url = "http://api.logentries.com/%s/hosts/" % ACCOUNT_KEY
    if provided_url:
        url = provided_url
    req = requests.get(url)
    return req

def print_query():
    logs = {}
    req = make_request()
    hosts, host_key = handle_response(req)
    for host in hosts:
        logs[host] = {}
    for host in hosts:
        time.sleep(1)
        req2 = make_request(hosts=host)
        data = eval(req2.text)
        for log in data['list']:
            logs[host][log['name']] = log['key']
    print "Log Keys:"
    print json.dumps(logs, sort_keys=True, indent=4, separators=(',', ': '))
    print "Log Set Keys:"
    print json.dumps(host_key, sort_keys=True, indent=4, separators=(',', ': '))

def start():
    print_query()

if __name__ == '__main__':
    start() 
