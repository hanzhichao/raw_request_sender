# coding=utf-8
import requests
import json
from common import get_conf, get_json


def change_waybill_number():
    req = get_json("create_waybill.json")
    req['order_num'] = "dz17050058"
    return req


def create_waybill():
    #env_url = get_conf("env.conf", "default", "env_url")
    api_res = "api/Order/Order/coHandle/"
    uri = env_url+api_res

    headers = get_json("header.json")
    cookies = get_json("cookies.json")
    # req = get_json("create_waybill.json")
    req = get_json("data.json")
    # req = change_waybill_number()

    data ='from=pc&req='+ json.dumps(req)
    print type(uri)
    print type(cookies)
    print type(headers)
    r=requests.post(uri, data=data, headers=headers, cookies=cookies)
    print r.text
    if r.json()['errno'] != '0':
        print "fail " + r.json()['errmsg']
    else:
        print "success"


if __name__ == "__main__":
    create_waybill()
