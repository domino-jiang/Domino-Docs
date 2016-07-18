#!/usr/bin/env python
#-*- coding:utf-8 -*-

import argparse,os
import pymysql.cursors as pycursors
import pymysql

def add_to_releaser(project_name,prs_releaser_list):
  project_id=""
  dbcon=pymysql.connect(host='127.0.0.1',user='xxxx',password='xxxx',db='prs',charset='utf8mb4',cursorclass=pycursors.DictCursor)

  try:
    with dbcon.cursor() as cursor:
      #检查项目是否存在
      sql = "select project_id from prs_project where project_name=%s"
      cursor.execute(sql,project_name)
      result=cursor.fetchone()
      if result:
        project_id=result['project_id']
      else:
        print("检查项目名称，没有找到你输入的项目名")
        exit(1)
      #检查用户是否存在
      sql = "select user_name from prs_user where user_name=%s"
      for user_name in prs_releaser_list:
        cursor.execute(sql,user_name)
        result=cursor.fetchone()
        if not result:
          print("用户 {user} 不存在".format(user=user_name))
          exit(1)

      #插入prs_releaser表，给用户增加分发权限
      sql = "insert into  prs_releaser (project_id,user_name) values (%s,%s)"
      for adduser in prs_releaser_list:
        cursor.execute(sql,(project_id,adduser))
        dbcon.commit()
        print ("Add user {username} ok!".format(username=adduser))
      #列出添加后的记录
      sql = "select * from prs_releaser where project_id=%s"
      cursor.execute(sql,project_id)
      for row in cursor:
        print(row)


  finally:
    dbcon.close()

def del_to_releaser(project_name,prs_releaser_list):
  project_id=""
  dbcon=pymysql.connect(host='127.0.0.1',user='xxxx',password='xxxx',db='prs',charset='utf8mb4',cursorclass=pycursors.DictCursor)
  
  try:
    with dbcon.cursor() as cursor:
      #检查项目是否存在
      sql = "select project_id from prs_project where project_name=%s"
      cursor.execute(sql,project_name)
      result=cursor.fetchone()
      if result:
        project_id=result['project_id']
      else:
        print("检查项目名称，没有找到你输入的项目名")
        exit(1)
      #检查用户是否存在
      sql = "select user_name from prs_user where user_name=%s"
      for user_name in prs_releaser_list:
        cursor.execute(sql,user_name)
        result=cursor.fetchone()
        if not result:
          print("用户 {user} 不存在".format(user=user_name))
          exit(1)

      #插入prs_releaser表，给用户增加分发权限
      sql = "delete from prs_releaser where project_id=%s and user_name=%s"
      for deluser in prs_releaser_list:
        cursor.execute(sql,(project_id,deluser))
        dbcon.commit()
        print ("Delete user {username} ok!".format(username=deluser))
      #列出添加后的记录
      sql = "select * from prs_releaser where project_id=%s"
      cursor.execute(sql,project_id)
      for row in cursor:
        print(row)


  finally:
    dbcon.close()


myparser=argparse.ArgumentParser(description="批量给项目做用户分发授权")
#op限定增加或者删除，使用了choices
myparser.add_argument('--op',required=True,choices=["add","del"],help="选择删除或者增加")
myparser.add_argument('--projectname',required=True,help="项目名称")
myparser.add_argument('--releaser_list',required=True,help="授权用户列表，用逗号分开")
myargs=myparser.parse_args()

project_name=myargs.projectname
releaser_list=myargs.releaser_list.split(",")
operation=myargs.op

if operation == "add":
  add_to_releaser(project_name,releaser_list)

if operation == "del":
   del_to_releaser(project_name,releaser_list)
