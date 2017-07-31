#!/usr/bin/env python
#coding:utf-8

import sys
import pycurl
from io import BytesIO
#import redis

def cdn_check(url,hostip,item):
  domain= url.split('/')[2]
  http_type = url.split('/')[0].replace(':','')
  curlstring=url.replace(domain,hostip)
  hoststring="Host:{domainname}".format(domainname=domain)

  buffer=BytesIO()
  c=pycurl.Curl()
  c.setopt(c.URL,curlstring)
  c.setopt(c.TIMEOUT,5)
  c.setopt(c.USERAGENT,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36')
  c.setopt(c.HTTPHEADER,[hoststring])
  c.setopt(c.WRITEDATA,buffer)
  if http_type == "https":
    #c.setopt(c.SSL_CIPHER_LIST, 'AES256-SHA')
    c.setopt(c.SSL_VERIFYPEER, 1)
    c.setopt(c.SSL_VERIFYHOST, 0)

  try:

    c.perform()

  except pycurl.error as e:

    buffer.close()
    c.close()
    return "error {errinfo}".format(errinfo=e)


  http_code=int(c.getinfo(c.HTTP_CODE))
  total_time=c.getinfo(c.TOTAL_TIME)
  connect_time=c.getinfo(c.CONNECT_TIME)
  pretransfer_time=c.getinfo(c.PRETRANSFER_TIME)
  starttrasfer_time=c.getinfo(c.STARTTRANSFER_TIME)
  #namelookup_time=float(c.getinfo(c.NAMELOOKUP_TIME)
  download_speed=c.getinfo(c.SPEED_DOWNLOAD)

  return_json={}
  return_json['HTTP_CODE']=http_code
  return_json['TOTAL_TIME']=total_time
  #return_json['NAMELOOKUP_TIME']=namelookup_time
  return_json['CONNECT_TIME']=connect_time
  return_json['PRETRANSFER_TIME']=pretransfer_time
  return_json['STARTTRANSFER_TIME']=starttrasfer_time
  return_json['SPEED_DOWNLOAD']=download_speed

  c.close()
  return return_json[item]

url=sys.argv[1]
ip=sys.argv[2]
item=sys.argv[3]

#print (url,ip,item)
abc=cdn_check(url,ip,item)
print (abc)

'''
abc=cdn_check("http://static.baidu.com/FED/css/weixin-v2.0/base.css","192.168.0.122")
print('CODE: %d' % abc["HTTP_CODE"])
print('TOTAL_TIME: %f' % abc["TOTAL_TIME"])
print('CONNECT_TIME: %f' % abc["CONNECT_TIME"])
print('PRETRANSFER_TIME: %f' % abc["PRETRANSFER_TIME"])
print('STARTTRANSFER_TIME: %f' % abc["STARTTRANSFER_TIME"])
print ('SPEED_DOWNLOAD: %f Byte/s' % abc["SPEED_DOWNLOAD"])
redis_server=redis.StrictRedis(host='10.101.1.152',port=6379,db=0)
redis_server.set('cdn_check',abc)
getredis=redis_server.get('cdn_check')
print (type(getredis))
print (getredis)
print (eval(getredis))
'''
