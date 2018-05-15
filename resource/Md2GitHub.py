import os
import json
import re
from googletrans import Translator

def getAllMd (file_dir):
# 获取当前目录下所有的css文件路径
	all_whole_path_files = []
	for root, dirs, files in os.walk(file_dir):
		for file in files:
			try:
				if file[-3:] == ".md":
					file_info = [root+'/', file]
					all_whole_path_files.append(file_info)
			except Exception as e:
				print(e)
	print(all_whole_path_files)
	return all_whole_path_files


def getRepName(zhCnName):
	translator = Translator()
	enName = translator.translate(zhCnName, dest='en').text
	enNameList = enName.split(' ')
	enName = ''
	for en in enNameList:
		if re.match('[a-zA-Z]+' ,en):
			en = en.capitalize()
			enName += en
	# 将当前获得的字符串拆分
	enStrList = [e for e in enName]
	# 符合要求的列表索引
	indexList = []
	for index, enStr in enumerate(enStrList):
		if re.match('[a-zA-Z]' ,enStr):
			indexList.append(index)
		else:
			pass

	rep_name = ''

	for index in indexList:
		rep_name += enStrList[index]


	# 如果翻译的仓库名长度大于100,则截断
	if len(rep_name) > 100:
		rep_name = rep_name[0:101]

	return rep_name

def getInfo(whole_path_file):
	info = {}
	with open("./inputInfo.txt", 'r') as f:
		jsonStr = ''
		lines = f.readlines()
		# 过滤注释, 生成json格式
		for line in lines:
			if '#' not in line:
				jsonStr += line
		info = json.loads(jsonStr)
		RepName = getRepName(whole_path_file[1][:-3])
		info['GitHubRepositoryName'] = RepName

	return info

# 在github创建远程仓库
def CreateRepository(info):
	GitHubUserName = info['GitHubUserName']
	GitHubPassWord = info['GitHubPassWord']
	GitHubRepositoryName = info['GitHubRepositoryName']
	# 这里有详细的参数说明: https://developer.github.com/v3/repos/#create
	new_command = 'curl -i -u ' + '\'' +GitHubUserName + ':' + GitHubPassWord + '\'' +' -d ' + '\''+ '{"name": ' + '\"'+GitHubRepositoryName +'\"'+ ', ' + '"auto_init": ' + 'true, ' + '"private": ' + 'false, ' + '"gitignore_template": ' + '"nanoc"}' + '\'' + ' https://api.github.com/user/repos'
	result = os.popen(new_command).readlines()
	if ('HTTP/1.1 201 Created\n' in result):
		print("创建成功")
		return True
	else:
		return False
	
def GetRepository(info):
	GetAllRepCommand = 'curl -i -u ' + '\'' + info['GitHubUserName'] + ':' + info['GitHubPassWord'] +'\'' + ' https://api.github.com/user/repos'
	print(GetAllRepCommand)
	result = os.popen(GetAllRepCommand).readlines()
	keyWord = info['GitHubUserName']+'/'+info['GitHubRepositoryName']
	# 判断仓库是否创建成功
	if not (keyWord in str(result)):
		return
	# 获取仓库到同级目录下
	# git@github.com:zhaoolee/ChatRoom.git
	GetRepCommand = 'git clone git@github.com:' +  keyWord + '.git'

	# 将仓库获取到本地
	result = os.popen(GetRepCommand).readlines()

# 将资源文件放入仓库
def FillRepository(info):
	AllFileName = os.listdir('./')
	PreReadMeFile = info['file_info'][0] + info['file_info'][1]

	# 将md文件替换原有的README.md
	ReplaceMdFileCommand = 'cp ./' + PreReadMeFile + ' ./'+ info['GitHubRepositoryName'] + '/README.md'
	print("==>", ReplaceMdFileCommand, "<==")
	result = os.popen(ReplaceMdFileCommand).readlines()

# 将文件提交到仓库
def PushRepository(info):
	inputRepository = 'cd ' + info['GitHubRepositoryName']
	addCommand = 'git add .'
	result = os.popen(inputRepository+'\n'+addCommand).readlines()
	commitCommand = 'git commit -m "完成项目的初始化"'
	result = os.popen(inputRepository+'\n'+commitCommand).readlines()
	pushCommand = 'git push'
	result = os.popen(inputRepository+'\n'+pushCommand).readlines()
	print("完成")


# 获取新建仓库所需的完整信息
def GetAllWholeRepInfo(all_whole_path_files):
	# 包含所有仓库信息
	all_whole_rep_info = []
	for whole_path_file in all_whole_path_files:
		# 包含新建仓库所需的完整信息
		whole_rep_info = getInfo(whole_path_file)
		whole_rep_info['file_info'] = whole_path_file
		all_whole_rep_info.append(whole_rep_info)
	return all_whole_rep_info

def main():
	all_whole_path_files = getAllMd('./')
	all_whole_rep_info = GetAllWholeRepInfo(all_whole_path_files)
	print(all_whole_rep_info)
	for info in all_whole_rep_info:
		CreateRepository(info)
		GetRepository(info)
		FillRepository(info)
		PushRepository(info)

if __name__ == '__main__':
	main()