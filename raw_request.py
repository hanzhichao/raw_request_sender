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
	flag = 1
	for line in f:
		line = line[:-1]
		if line.split():
			if flag == 1:
				item = line.split()
				request_dict["Method"]=item[0].strip()
				request_dict["Uri"]=item[1].strip()
				request_dict["Version"]=item[2].strip()
				flag = 2
			elif flag == 2:
				item = line.split(":", 1)
				key = item[0].strip()
				value = item[1].strip()
				print key
				if key.lower() == "cookie":
					print key
					print value
					# for sub_item in value.split(";"):
					# 	sub_key = sub_item.split("=")[0].strip()
					# 	sub_value = sub_item.split("=")[1].strip()
					# 	request_dict["Cookies"][sub_key]=sub_value
					d = load2(value,";","=")
					request_dict["Cookies"]=d
					print d

				else:
					request_dict["Headers"][key]=value
			else:
				request_dict["Data"] = load2(line,"&","=")
				# params = line.split("&")
				# for param in params:
				# 	item = param.split("=",1)
				# 	key = item[0].strip()
				# 	value = item[1].strip()
				# 	request_dict["Data"][key]=value
		else:
			flag = 4
		# with open('text.json','a') as outfile:  
		#     json.dump(request_dict,outfile,ensure_ascii=False)  
		#     outfile.write('\n') 
		return request_dict

def load2(data,sep1,sep2):
	#print data,sep1,sep2
	d ={}
	list1 = data.split(sep1)
	for i in list1:
		list2 = i.split(sep2)
		key = list2[0].strip()
		value = list2[1].strip()
		d[key]=value
	return d



def dump(data_dict):
	data = ''
	for key in data_dict:
		data = data + "&" + key + "=" + data_dict[key]
	data = data[1:]
	return data


def send(file_path):
	f = open(file_path)
	request_dict = load(f)
	f.close()

	method = request_dict["Method"]
	uri = request_dict["Uri"]
	headers=request_dict["Headers"]
	cookies=request_dict["Cookies"]
	data = dump(request_dict["Data"])
	
	if method.lower() == 'post':
		# data2 = unquote(data)
		# with open('data.json', 'w') as h:
		#  	h.write(json.dumps(data2))
		print cookies
		# data = "req={\"type\":\"PInfo\",\"op_type\":\"add\",\"obj_info\":{\"state\":1,\"price_name\":\"标杆maxwv-1\",\"price_type\":\"auth_basic_pt\",\"fee_name\":\"标杆价\",\"pm_id\":\"28\"}%7"
		# res = requests.post(uri, data=data,headers=headers,cookies=cookies)
		# print res.text
		# if res.json()['errno'] == '0':
		# 	print "Success!"
		# else:
		# 	print res.json()['errmsg']
	

if __name__ == '__main__':
	#print load("raw_request_sample.txt")
	send("create_price.txt")

