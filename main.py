#!/usr/bin/python3
# encoding:utf-8

import os
import platform
import sys
import time
import ui
import module
import subprocess
###########################################################
#HOME主菜单
def homeMenu():
	ui.homeHead()
	ui.homeMenu()
	int_homeinput=input("输入一个选项: ")
	if int_homeinput=='1':
		if (module.fcLogexist()==1):
			ini.clr()
			ui.nologError()
			time.sleep(2)
			ini.reset()
			homeMenu()
		else:
			home_1Menu()#进入(1)子菜单		

	elif int_homeinput=='2':
		if os.path.exists(ini.GPSLOGPATH):
			pass
		else:
			os.makedirs(ini.GPSLOGPATH)
		module.downloadGpslog(ini.GPSLOGPATH)
		ini.reset()
		homeMenu()

	elif int_homeinput=='3':#清空所有日志
		module.clearLog()
		module.clearGpslog()
		ini.reset()
		homeMenu()

	elif int_homeinput=='4':#打开GPS日志记录开关
		module.startGps()
		time.sleep(2)
		ini.reset()
		homeMenu()

	elif int_homeinput=='5':#
		ui.home_5Warning()
		str_gps_log=''
		os.chdir(ini.GPSLOGPATH)
		for str_gps_log in os.listdir('.'):
			if str_gps_log.find('gpsdebug') != -1:
				ini.changeFilename(str_gps_log,module.getGpstime(str_gps_log))
		ui.home_5Sucess()
		time.sleep(2)
		ini.reset()
		homeMenu()

	elif int_homeinput=='6':#退出
		ini.reset()
		sys.exit(1)

	else:
		#输入错误字符
		ini.clr()
		ui.homeError()
		time.sleep(2)
		ini.reset()
		homeMenu()

##########################################################
def home_1Menu():
	ini.clr()
	str_fcloglist=module.fcLoglist(int_stringnumber)#存储日志SN码str,list
	print("*************************************************************************************************")
	for i in range(module.fcLognumber()):
		print("["+str(i+1)+"] ",end='')
		print(str_fcloglist[-(i+1)])
	print("*************************************************************************************************")
	print("*************************************************************************************************")
	ui.home_1Menu()
	int_home_1input=input("输入一个编号： ")
	if int_home_1input=='1':#下载所有日志(完成)***************
		for str_sn in str_fcloglist:
			if os.path.exists(ini.HLOGPATH_M+str_sn):
				pass
			else:
				ini.snFile(str_sn)#创建以sn码为名得文件夹
			module.downloadSnlog(str_sn,ini.HLOGPATH_M+str_sn)#拉取全部SN码日志
		ini.reset()
		home_1Menu()

	elif int_home_1input=='2':#下载所有飞控日志(完成)************
		for str_sn in str_fcloglist:
			if os.path.exists(ini.HLOGPATH_M+str_sn):
				pass
			else:
				ini.snFile(str_sn)#创建以sn码为名得文件夹
			module.downloadSnfclog(str_sn,ini.HLOGPATH_M+str_sn)#拉取飞控日志
		ini.reset()
		home_1Menu()

	elif int_home_1input=='3':#下载指定SN码全部日志(完成)*********
		int_home_1_3input=input("输入SN码前编号：")
		int_sn=-int(int_home_1_3input)#倒数list序号
		str_sn=str_fcloglist[int_sn]#倒数sn字符串
		if os.path.exists(ini.HLOGPATH_M+str_sn):
			pass
		else:
			ini.snFile(str_sn)#创建以sn码为名得文件夹
		module.downloadSnlog(str_sn,ini.HLOGPATH_M+str_sn)#拉取全部SN码日志
		ini.reset()
		home_1Menu()

	elif int_home_1input=='4':#下载指定SN码飞控日志（完成）********
		int_home_1_3input=input("输入SN码前编号：")
		int_sn=-int(int_home_1_3input)#倒数list序号
		str_sn=str_fcloglist[int_sn]#倒数sn字符串
		if os.path.exists(ini.HLOGPATH_M+str_sn):
			pass
		else:
			ini.snFile(str_sn)#创建以sn码为名得文件夹
		module.downloadSnfclog(str_sn,ini.HLOGPATH_M+str_sn)#拉取飞控日志
		ini.reset()
		home_1Menu()

	elif int_home_1input=='5':#删除该路径下所有日志(完成)************
		module.clearLog()
		ini.reset()
		homeMenu()

	elif int_home_1input=='6':#返回（完成）***************
		ini.reset()
		homeMenu()

	else:
		#输入错误字符
		ini.clr()
		ui.homeError()
		time.sleep(2)
		ini.reset()
		home_1Menu()

if __name__ == '__main__':
	
	#判断系统类型，windows 1,Linux 2,Mac 3,未知 0
	int_systemtype=0

	if platform.system()=='Windows':
		int_systemtype=1
		import wini
		int_stringnumber=32#module.py 34l
		ini=wini
		ini.cmdSize()
		from subprocess import CREATE_NEW_CONSOLE
		subprocess.Popen(["adb","nodaemon","server"],creationflags=CREATE_NEW_CONSOLE)
	elif platform.system()=='Linux':
		int_systemtype=2
		import lini
		int_stringnumber=31#module.py 34l
		ini=lini
	elif platform.system()=='Mac':
		int_systemtype=3
		import mini
		ini=mini
	else:
		int_systemtype=0
		print("ERR,System type unknow!")
		exit()

	#是否安装ADB
	int_adbexit=ini.adbExist()
	ini.clr()
	if int_adbexit == 1:
		print('ERR:Cannot find ADB!')
		exit()

	ini.pathExist()#本地hlog文件夹

	#等待ADB连接
	ui.adbWait()
	os.system("adb wait-for-device")
	ini.reset()
	module.rootHuba()
	homeMenu()
