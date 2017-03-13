import os
USERPATH = "D:\\"

HLOGPATH = USERPATH+"hlog"
HLOGPATH_M = USERPATH+"hlog\\"
GPSLOGPATH = HLOGPATH_M+"gpslog"

#判断是否存在hlog文件夹，没有自动创建
def pathExist():
	if os.path.exists(HLOGPATH):
		pass
	else:
		os.makedirs(HLOGPATH)

#创建SN码为名称的文件夹
def snFile(str_sn):
	os.makedirs(HLOGPATH_M+str_sn)

#判断是否安装adb
def adbExist():
	if os.system("adb")==1:
		print('ADB available')
		return 0
	else:
		print('cannot find ADB!')
		return 1

#清屏命令
def clr():
	os.system("cls")
def reset():
	os.system("cls")
def cmdSize():
	os.system("mode con cols=200 lines=60")

#更改GPSlog文件名
def changeFilename(str_path,str_time):
	os.rename(str_path,str_time)