# coding:utf-8
from urllib import unquote
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# load 反序列化 针对文件句柄f->dict loads 针对内存对象 str->dict
# dump 序列化 dict -> f    dumps   dict->str


# 将str转化为字典
def _loads(data, sep1, sep2):
    dic = {}
    list1 = data.split(sep1)
    for i in list1:
        list2 = i.split(sep2)
        key = list2[0].strip()
        value = list2[1].strip()
        dic[key] = value
    return dic


# 解析data字典
def _dumps(data_dict):
    data = ''
    for key in data_dict:
        data = data + "&" + key + "=" + json.dumps(data_dict[key])
    data = data[1:]
    print data
    return data


def _load(f):
    request_dict = {"method": '', "uri": '', "version": '',
                    "headers": {}, "cookies": {}, "data": {}}
    lines = f.readlines()

    # first line: method/uri/version
    items = lines[0][:-1].split()
    request_dict['method'] = items[0].strip()
    request_dict['uri'] = items[1].strip()
    request_dict['version'] = items[2].strip()

    def load_headers(lines):
        dic = {}
        for line in lines:
            line = line[:-1]
            key = line.split(":", 1)[0].strip()
            value = line.split(":", 1)[1].strip()
            dic[key] = value
        return dic

    # cookies
    item = lines[-3][:-1].split(":", 1)
    key = item[0].strip()
    if key.lower() == 'cookie':
        request_dict['cookies'] = _loads(item[1], ";", "=")
        # headers
        request_dict['headers'] = load_headers(lines[1:-4])
    else:
        request_dict['headers'] = load_headers(lines[1:-3])

    # data
    request_dict['data'] = _loads(lines[-1], "&", "=")
    items = _loads(lines[-1], "&", "=")
    json_data = items['req']
    req_json = json.loads(unquote(json_data))
    del request_dict['data']['req']
    request_dict['data']['req'] = req_json
    return request_dict


def convert(infile, outfile):
    with open(infile) as f:
        request_dict = _load(f)
        with open(outfile, 'w') as f2:
            json.dump(request_dict, f2, ensure_ascii=False)
            f2.write('\n')


def send(file_path):
    with open(file_path) as f:
        request_dict = _load(f)

    method = request_dict["method"]
    uri = request_dict["uri"]
    headers = request_dict["headers"]
    cookies = request_dict["cookies"]
    data = _dumps(request_dict["data"])

    if request_dict['method'].lower() == 'post':
        res = requests.post(uri, data=data, headers=headers, cookies=cookies)
        print res.text
        if res.json()['errno'] == '0':
            print "Success!"
        else:
            print res.json()['errmsg']


if __name__ == '__main__':
	with open "raw_request_sample.txt" as f:
    	print _load(f)
    convert("create_price.txt",'1.json')
    # send("create_price.txt")
