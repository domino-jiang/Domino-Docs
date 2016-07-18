#/usr/bin/env python
#-*- coding:utf-8 -*-


import argparse
import os,sys
import re

def create_dist(domain,server_list):
  mydomain=domain
  myserverlist=""
  for i in server_list:
    myserverlist=myserverlist+" "+i

  mymodule_name=domain.replace('.','_')

  My_project_path ="/data1/vhosts/"
  my_check_path=My_project_path+mydomain

  #获取www用户的uid和gid
  www_uid=80
  www_gid=80
  try:
    fp=open('/etc/passwd','r')
    for line in fp.readlines():
      #m=re.search(r'www:x:(\d+):(\d+):.*',i)
      if 'www' in line:
        www_uid=line.split(':')[2]
        www_gid=line.split(':')[3]
    fp.close()
  except IOError as ioerr:
    print "Sorry!I got a IOerror:{info}".format(info=ioerr)

  #检查目录是否存在，如果没有就创建目录
  if not os.path.exists(my_check_path):
    os.mkdir(my_check_path)
    os.chown(my_check_path,www_uid,www_gid)
    os.mkdir(my_check_path+"/htdocs")
    os.chown(my_check_path+"/htdocs",www_uid,www_gid)
  else:
    print "This {my_check_path} is exists.".format(my_check_path=my_check_path)

  #检查rsyncd.conf文件中是否已经有了需要创建的模块，如果没有就创建
  need_add=False
  myfp=open('/etc/rsyncd.conf','r')
  for i in myfp.readlines():
      m=re.search(mymodule_name,i)

      if m:
        need_add=False

      else:
        need_add=True
  else:
        need_add=True

  myfp.close()

  #根据need_add增加模块到rsyncd
  if need_add:
    myfp=open('/etc/rsyncd.conf','a')
    myfp.write("["+mymodule_name+"]\n")
    myfp.write("path="+my_check_path+"/htdocs\n")
    myfp.write("read only=no\n")
  myfp.close()

  #检查publish_logger.conf里是否有要添加的模块
  myfp=open("/usr/local/etc/publish_logger.conf",'r')
  for i in myfp.readlines():
      m=re.search(mymodule_name,i)
      if m:
        need_add=False
      else:
        need_add=True
  else:
        need_add=True

  myfp.close()

  myfp=open("/usr/local/etc/publish_logger.conf",'a')
  if need_add:
    myfp.write("["+mymodule_name+"]\n")
    myfp.write("mailto=xxx@xxx.com\n")
    myfp.write("hosts="+str(myserverlist)+"\n")
    myfp.write("modules="+mymodule_name+"\n")
  myfp.close()


#配置命令传入参数
myparser = argparse.ArgumentParser(description="创建分发模块")
myparser.add_argument('--domain',required=True,help="需要创建的项目名称")
myparser.add_argument('--serverlist',required=True,help="需要分发的服务器列表")

myargs=myparser.parse_args()


module_name = myargs.domain
server_list =  myargs.serverlist.split(',')


#调用分发配置程序

create_dist(module_name,server_list)