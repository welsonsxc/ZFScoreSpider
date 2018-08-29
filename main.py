import requests
import re
from html.parser import *
import urllib
import os
import csv
import urllib
import urllib.parse
import split
def littlecat():
	x=[]
	state=[]
	website=r"http://qjjwgl.hznu.edu.cn/webserver/"
	#userxh=input("输入你的学号:")
	#password=input("输入你的密码:")
	userxh='2017830402024'
	password='SCjiaowu287486.'
	class Scraper(HTMLParser):
		def handle_starttag(self,tag,attrs):
			if tag=='img':#验证码
				attrs=dict(attrs)
				if(attrs.__contains__('id')):
					x.append(attrs["src"])
			if tag=='input':#viewstate
				attrs=dict(attrs)
				if attrs.__contains__('name'):
					if attrs['name']=='__VIEWSTATE':
						state.append(attrs['value'])

	#登陆系统
	webpage=requests.get(url=website+"default2.aspx")
	#获取网页cookies
	Cookie=webpage.cookies
	date=webpage.text
	parser=Scraper()
	parser.feed(date)
	headers={
		'User-Agent':r'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0;  TheWorld 7)',
		}
		
	while True:
		#获取验证码
		url=website+"CheckCode.aspx"
		pic=requests.get(url,cookies=Cookie,headers=headers)
		if os.path.exists(r'd://yanzheng.jpg'):
			os.remove(r'd://yanzheng.jpg')
		with open(r'd://yanzheng.jpg','wb')as f:
			f.write(pic.content)
			f.close()
		#输入验证码
		os.startfile(r'd:yanzheng.jpg')
		ycode=input("输入弹出的验证码: ")
		#登陆
		payload={
				 '__VIEWSTATE':state[0],
				 'txtusername':userxh,
				 'TextBox2':password,
				 'txtSecretCode':ycode,
				 'RadioButtonList1':'%D1%A7%C9%FA',
				 'Button1':"",
				 'lbLanguage':'',
				 'hidPdrs':'',
				 'hidsc':'',
				}
		Log_in=website+"default2.aspx"
		r=requests.post(url=Log_in,data=payload,headers=headers,cookies=Cookie)
		#判断登陆状态
		pat=r'<title>(.*?)</title>'
		x=re.findall(pat,r.text)
		if(x[0]=="欢迎使用正方教务管理系统！请登录"):
			print("登陆失败")
		else:
			print("登陆成功")
			#抓取名字
			catch='<span id="xhxm">(.*?)</span></em>'
			name=re.findall(catch,r.text)
			name=name[0]
			name=name[:-2]
			print(name)
			username=urllib.parse.quote(name.encode("gb2312"))
			break
	 
	#成绩查询 
	lheaders={
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Referer':website+'xscjcx.aspx?xh='+userxh+"&xm="+username+"&gnmkdm=N121605",
		'Upgrade-Insecure-Requests': '1'
		}
	html=requests.get(website+"xscjcx.aspx?xh="+userxh+"&xm="+username+"&gnmkdm=N121605",cookies=Cookie,headers=lheaders)
	catch='<input type="hidden" name="__VIEWSTATE" value="(.*?)" />'
	state=re.findall(catch,html.text)
	state=state[0]
	payload={
			'__EVENTTARGET':'',
			'__EVENTARGUMENT':'',
			'__VIEWSTATE':state,
			'hidLanguage':'',
			'ddlXN':'',
			'ddlXQ':'',
			'ddl_kcxz':'',
			'btn_zcj':'%C0%FA%C4%EA%B3%C9%BC%A8'
				}
	Log_in=website+"xscjcx.aspx?xh="+userxh+"&xm="+username+"&gnmkdm=N121605"
	r=requests.post(url=Log_in,data=payload,headers=lheaders,cookies=Cookie)

	#保存表格
	catch='<td>(.*?)</td>'*15
	table=re.findall(catch,r.text)

	f=open("table.txt","w")
	for each_line in table:
		#each_line.split(,);
		if each_line != table[0]:
			f.write(str(each_line)+'\n')
	f.close()

	#分割表格并输出
	split.Splittable("table.txt")

	#结束程序
	input("爬虫完成")
if __name__=="__main__":
	littlecat()