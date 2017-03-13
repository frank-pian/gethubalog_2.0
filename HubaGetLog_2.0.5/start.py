# encoding:utf-8

import os
import sys
import shutil
import copy
import subprocess

#str_update_path="//192.168.2.1/深圳飞马/胡巴/测试/HubaGetLog2_0"#升级位置
str_update_path="F:/hubatest"
str_local_path=sys.path[0]#脚本所在文件夹

#将字符串列表整体转换为整形列表
def strlist_To_Intlist(str_list):
	int_list = []
	for n in str_list:
		int_list.append(int(n))
	return int_list


#比较版本号str，version1 > version2 return 1 ;version1 = version2 return 0 ;version1 < version2 return -1
def compare_Version(version1, version2):
	list_version1 = []
	list_version2 = []
	#删除文件名开通'HubaGetLog_',并且拆分变为int列表
	try:
		list_version1 = strlist_To_Intlist(version1.lstrip('HubaGetLog_').split('.'))
		list_version2 = strlist_To_Intlist(version2.lstrip('HubaGetLog_').split('.'))
	except:
		return print("版本号格式错误！")
	#print(list_version1)
	#print(list_version2)

	if list_version1[0] > list_version2[0]:
		return 1
	elif list_version1[0] < list_version2[0]:
		return -1
	else:
		if list_version1[1] > list_version2[1]:
			return 1
		elif list_version1[1] < list_version2[1]:
			return -1
		else:
			if list_version1[2] > list_version2[2]:
				return 1
			elif list_version1[2] < list_version2[2]:
				return -1
			else:
				return 0

#输入位置，筛选版本列表，无文件返回1，无升级位置返回2，有文件返回列表
def get_Version_List(path):
	if os.path.exists(path):
		path_list = []

		path_list = os.listdir(path)
		temp_list = copy.deepcopy(path_list)
		for n in temp_list:#列表内剔除其他文件字符串
			if n.find('HubaGetLog_') < 0:
			#不存在子串"HubaGetLog_"
				path_list.remove(n)
		if len(path_list) == 0:
			return 1#没有文件
		else:
			return path_list
	else:
		return 2#没有文件位置

#返回版本列表最大版本号，没有最大返回1
def get_Best_Version(v_list):
		temp_version = "HubaGetLog_0.0.0"

		for i in v_list:
			if compare_Version(temp_version,i) >= 0:
				pass
			else:
				temp_version = i

		if temp_version == "HubaGetLog_0.0.0":
			return 1
		else:
			return temp_version

#print(get_Best_Version(get_Version_List(str_local_path)))


def start_Local_Version():
	start_version = get_Best_Version(get_Version_List(str_local_path))
	#print("python " + str_local_path + "/" + start_version + "/" + "main.py")
	os.system("python " + str_local_path + "/" + start_version + "/" + "main.py")


################################################开始
if __name__ == '__main__':
	local_version = "HubaGetLog_0.0.0"
	update_version = "HubaGetLog_0.0.0"

	if get_Version_List(str_local_path) == 1:
		print("本地未检查到软件！")

	elif get_Version_List(str_local_path) == 2:
		print("本地路径异常！")
		sys.exit()
	else:
		if get_Best_Version(get_Version_List(str_local_path)) == 1:
			print ("本地版本号异常！")
			sys.exit()
		else:
			local_version = get_Best_Version(get_Version_List(str_local_path))
	
	if get_Version_List(str_update_path) == 1:
		print("服务器未检查到软件！")

	elif get_Version_List(str_update_path) == 2:
		print("服务器路径异常！")

	else:
		if get_Best_Version(get_Version_List(str_update_path)) == 1:
			print ("服务器版本号异常！")
		else:
			update_version = get_Best_Version(get_Version_List(str_update_path))

	#比较本地与服务器版本号
	if compare_Version(local_version,update_version) >= 0:#不升级版本
		if local_version == "HubaGetLog_0.0.0":
			print("本地版本号异常！")
			os.system('pause')
		else:
			start_Local_Version()#直接运行

	else:#升级版本
		if update_version == "HubaGetLog_0.0.0":
			if local_version == "HubaGetLog_0.0.0":
				print("云端和本地版本号异常！")
				os.system('pause')
			else:
				start_Local_Version()#直接运行

		else:
			try:
				shutil.rmtree(str_local_path + "/" + local_version)#删除本地版本
			except:
				print("删除时，本地无文件！")
			try:
				shutil.copytree(str_update_path+"/"+update_version, str_local_path+"/"+update_version)
			except:
				print("升级失败！")
				if local_version == "HubaGetLog_0.0.0":
					print("本地无文件")
					os.system('pause')
				
	start_Local_Version()#直接运行
