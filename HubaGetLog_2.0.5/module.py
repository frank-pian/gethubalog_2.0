import subprocess
import os

DATAPATH = "/data/log/"
DATALOG = "/data/log/*"
FCLOG = "/data/log/top-secret*.bin"
GPSLOG = "/sdcard/mtklog/gpsdbglog"
STR_FCLOGEXIST = "/data/log/top-secret*: No such file or directory\n"

#打开GPS记录开关
def startGps():
	os.system("adb shell am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name set_auto_start_1 --ei cmd_target 16")

#删除DATALOG下所有文件
def clearLog():
	os.system("adb shell rm -r "+DATALOG)
#GPSLOG下所有文件
def clearGpslog():
	os.system("adb shell rm -r "+GPSLOG+"/*")

#返回飞控top-secret日志个数(int)
def fcLognumber():
	return int(subprocess.getoutput(r'adb shell "ls ' + FCLOG + r'|wc -l"'))

#返回飞控top-secret日志sn码(list)
def fcLoglist(snumber):
	list_fclog=[]
	str_temp=subprocess.getoutput("adb shell ls "+FCLOG)
	head=21
	for i in range(fcLognumber()):
		list_fclog.append(str_temp[head:head+5])
		head=head+snumber#windows多一个/n 32 linux为31
	return list_fclog

#下载指定SN码全部日志到指定路径
def downloadSnlog(str_sn,str_localpath):
	os.system("adb shell mkdir /data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+"top-secret_"+str_sn+"*.bin"+" "+"/data/log/TEMP")
	os.system("adb shell cp -R "+DATAPATH+"top-secret_"+str_sn+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+"battery_"+str_sn+"*"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+"gimbal_"+str_sn+"*"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+"gps_"+str_sn+"*"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+"optical_flow_"+str_sn+"*"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+"optical_flow_listener_"+str_sn+"*"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+str_sn+"*"+"_normal_rx_from_cm4.txt"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+str_sn+"*"+"_normal_rx_from_ground.txt"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+str_sn+"*"+"_normal_tx_to_cm4.txt"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+str_sn+"*"+"_normal_tx_to_ground.txt"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+str_sn+"*"+"_test_rx_from_cm4.txt"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+str_sn+"*"+"_test_rx_from_ground.txt"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+str_sn+"*"+"_test_tx_to_cm4.txt"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+str_sn+"*"+"_test_tx_to_ground.txt"+" "+"/data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+"cpu_info_"+str_sn+"*"+" "+"/data/log/TEMP")
	os.system("adb pull /data/log/TEMP "+str_localpath)
	os.system("adb shell rm -r /data/log/TEMP")

#下载指定SN码飞控日志到指定路径
def downloadSnfclog(str_sn,str_localpath):
	os.system("adb shell mkdir /data/log/TEMP")
	os.system("adb shell cp "+DATAPATH+"top-secret_"+str_sn+"*.bin "+"/data/log/TEMP")
	os.system("adb pull /data/log/TEMP "+str_localpath)
	os.system("adb shell rm -r /data/log/TEMP")

#下载GPS日志到指定路径
def downloadGpslog(str_localpath):
	os.system("adb pull "+GPSLOG+" "+str_localpath)

#判断FCLOG是否存在飞控日志(1无日志，0有日志)
def fcLogexist():
	if (subprocess.getoutput("adb shell ls "+DATAPATH)==''):
		return 1
	else:
		return 0
def rootHuba():
	os.system("adb root")

#提取文件时间
def getGpstime(str_path):
	str_reverse_line=''
	str_gps_time=''
	f=open(str_path,'rt',encoding="windows-1252",errors='ignore')
	lines=f.readlines()
	for str_reverse_line in lines[-1::-1]:
		if str_reverse_line.startswith('$GNGGA'):
			break
	f.close()
	str_gps_time=str_reverse_line[7:13]
	int_gps_time=int(str_gps_time[0:2])+8
	if int_gps_time>24:
		int_gps_time=int_gps_time-24
	str_gps_time=str(int_gps_time)+str_gps_time[2:6]
	return str_gps_time
