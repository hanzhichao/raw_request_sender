# coding:utf-8
from urllib import unquote
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# load 反序列化 针对文件句柄 loads 针对内存对象
# dump 序列化

def load(f):
	request_dict = {"method":'',"uri":'',"version":'',"headers":{},"cookies":{},"data":{}}
	lines = f.readlines()

	# first line: method/uri/version
	items = lines[0][:-1].split()
	# print items
	request_dict['method'] = items[0].strip()
	request_dict['uri'] = items[1].strip()
	request_dict['version'] = items[2].strip()
	# print request_dict

	def load_headers(lines):
		dic = {}
		for line in lines:
			line=line[:-1]
			key = line.split(":", 1)[0].strip()
			value = line.split(":", 1)[1].strip()
			dic[key] = value
		return dic

	# cookies
	item = lines[-3][:-1].split(":", 1)
	key = item[0].strip()
	if key.lower() == 'cookie':
		request_dict['cookies'] = _dict(item[1], ";","=")
		# headers
		request_dict['headers'] = load_headers(lines[1:-4])
	else:
		request_dict['headers'] = load_headers(lines[1:-3])
		
	# data
	data = lines[-1]
	# print json.loads(data)
	request_dict['data'] = _dict(lines[-1],"&","=")
	items = _dict(lines[-1],"&","=")
	json_data = items['req']
	req_json = json.loads(unquote(json_data))
	del request_dict['data']['req']
	request_dict['data']['req']=req_json
	#request_dict['data'] = lines[-1]
	# print request_dict['data']
	return request_dict

def _dict(data,sep1,sep2):
	#print data,sep1,sep2
	dic ={}
	list1 = data.split(sep1)
	for i in list1:
		list2 = i.split(sep2)
		key = list2[0].strip()
		value = list2[1].strip()
		dic[key]=value
	return dic



def dump(data_dict):
	data = ''
	for key in data_dict:
		data = data + "&" + key + "=" + data_dict[key]
	data = data[1:]
	return data


def save(infile, outfile):
	with open(infile) as f:
		request_dict = load(f)
		with open(outfile,'w') as f2:  
		    json.dump(request_dict,f2,ensure_ascii=False)  
		    f2.write('\n') 


def send(file_path):
	f = open(file_path)
	request_dict = load(f)
	f.close()
	# print request_dict

	method = request_dict["method"]
	uri = request_dict["uri"]
	headers=request_dict["headers"]
	cookies=request_dict["cookies"]
	# data = request_dict['data']
	data = dump(request_dict["data"])
	data = unquote(data)
	# print data
	# print unquote(data)
	# data = json.dumps(data)
	# print data

	
	if request_dict['method'].lower() == 'post':
		pass
		# data2 = unquote(data)
		# with open('data.json', 'w') as h:
		#  	h.write(json.dumps(data2))
		# print cookies
		# data = "req={\"type\":\"PInfo\",\"op_type\":\"add\",\"obj_info\":{\"state\":1,\"price_name\":\"标杆maxwv-1\",\"price_type\":\"auth_basic_pt\",\"fee_name\":\"标杆价\",\"pm_id\":\"28\"}%7"
		# res = requests.post(uri, data=data,headers=headers,cookies=cookies)
		# print res.text
		# if res.json()['errno'] == '0':
		# 	print "Success!"
		# else:
		# 	print res.json()['errmsg']
	

if __name__ == '__main__':
	#print load("raw_request_sample.txt")
	save("create_price.txt",'1.json')
	# send("create_price.txt")

