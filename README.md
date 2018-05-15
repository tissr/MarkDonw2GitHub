- 简书天然支持Markdown格式, 而Github仓库中的README.md也天然支持Markdown格式
- 简书后台支持一键下载所有写过的Markdown的文章, Github提供了脚本创建仓库的Api
- 我们从简书后台获取所有写过的Markdown文章, 然后运行一个脚本, Github将会新建一个仓库, 作为我们博客的新地址

#### 运行效果:
###### 本地目录
> ![本地目录](https://upload-images.jianshu.io/upload_images/3203841-d2ba7362090e04b0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
###### GitHub新仓库
> ![github新仓库](https://upload-images.jianshu.io/upload_images/3203841-155e8dcbc7f77bfe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
> ![新仓库细节](https://upload-images.jianshu.io/upload_images/3203841-fd7967501d35308a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


> ## 脚本的说明:
> - **仓库的英文名,是怎么来的?**
> 仓库的英文名由原markdown的名字通过google翻译而来
> - **如何认证github用户名和密码?**
> 用户名和密码被分离了出来, 放在了单独的配置文件中 
> - **程序如何获取本地markdown文档的位置?**
> 程序会通过递归方法, 将脚本所在的同级目录和子目录下所有的以`.md`结尾的所有文件读取出来, 这些.md结尾的文档都会被建立为Github仓库
> - **简书支持这种行为么?**
> 简书并不反对这种行为, 我写过一篇手动迁移简书markdown的细则: [简书文章发布到GitHub](https://www.jianshu.com/p/7167122783b5), 简叔打赏了我10颗糖,至今难忘...
> - **为什么写这个脚本 ?**
> 关于[简书文章发布到GitHub](https://www.jianshu.com/p/7167122783b5), 里面详细介绍了手动迁移的整个过程, 后来有读者评论:
> ![评论](https://upload-images.jianshu.io/upload_images/3203841-236429d855a41b8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
> 为了回应读者的热情, 我完成了这个脚本
> - **脚本适用于所有本markdown文档一键发布到github么?**
- 是的, 这里用简书做例子, 只是因为简书打包下载的文档包,很适合做说明, 任何本地的md文档,只要在脚本的同级目录或者子目录, 都可以一键迁移到GitHub
> **- 脚本依赖的环境:**
> 安装了git, 安装了curl, 安装了python3, 在GitHub中添加了公钥

## 运行脚本之前需要在GitHub添加公钥
- 在本地生成一对秘钥(以Ubuntu为例), 进入到.ssh目录下

```
cd ~/.ssh/
```

- 生成一对秘钥

```
ssh-keygen -t rsa -C "lijianzhao1208@gmail.com"
```
- 为秘钥起个名字(可直接回车跳过)
> ![秘钥起个名字](http://upload-images.jianshu.io/upload_images/3203841-426d50f5264e17d3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- 将公钥内容添加到github(实现免密向远程仓库提交代码)

>复制公钥(github.pub)内容

>![复制公钥(github.pub)内容](http://upload-images.jianshu.io/upload_images/3203841-e9e69d9c09781d83.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


>登录github,并粘贴公钥内容

>![github主页](http://upload-images.jianshu.io/upload_images/3203841-2f1aff077bb3c1df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>![添加容器](http://upload-images.jianshu.io/upload_images/3203841-4fc9d7c4ccb626b3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>![添加公钥](http://upload-images.jianshu.io/upload_images/3203841-cf2b8e6e202f4f1f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>![添加完成](http://upload-images.jianshu.io/upload_images/3203841-446131a4982b976d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 源码
###### 主逻辑脚本
```python
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
	# 依次创建仓库
	for info in all_whole_rep_info:
		CreateRepository(info)
		GetRepository(info)
		FillRepository(info)
		PushRepository(info)

if __name__ == '__main__':
	main()
```
###### 配置脚本
```
{
	# 用户名
	"GitHubUserName": "zhaoolee", 
	# 用户密码
	"GitHubPassWord": "github"
}
```

> 总结:
> 这不是一篇独立的文章, 如果你想了解更多, 可以参考我以前写过相关的两篇:
> - 手动迁移markdonw文档,[简书文章发布到GitHub](https://www.jianshu.com/p/7167122783b5)
> - 将附带静态资源的markdown文档, 一键迁移到github, [Github变身网络硬盘](https://www.jianshu.com/p/7167122783b5)
> ###### 这个脚本已经可以用了,但还不完美, 欢迎在文章底部提出改进建议