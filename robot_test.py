# coding=gbk
#coding=utf8
import werobot
# 环境配置
robot = werobot.WeRoBot(token='robot')	
client=robot.client
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.config["APP_ID"] = "不告诉你"
robot.config["APP_SECRET"] = "不告诉你"	

# 版本
@robot.filter("版本")
def versiong(message):
	reply='离娄最后更新于2018.8.30'
	return reply

# 信息处理
@robot.handler
def hello(message):
	return 'Hello world'

# 关注提示
@robot.subscribe
def subscribe(message):
	reply = '感谢关注！\n有任何需要请使用菜单栏！'
	return reply	
# 菜单反馈
@robot.key_click("bdjw")
def bdjw(message):
    return '你点击了“绑定教务”按钮'

@robot.key_click("cjcx")
def cjcx(message):
    return '你点击了“成绩查询”按钮'

@robot.key_click("hqsh")
def hqsh(message):
    return '你点击了“后勤生活”按钮'

@robot.key_click("cp")
def cp(message):
    return '你点击了“晨跑”按钮'

@robot.key_click("ljwm")
def ljwm(message):
    return '你点击了“了解我们”按钮'

@robot.key_click("xl")
def xl(message):
    return '你点击了“校历”按钮'
	
@robot.key_click("map")
def map(message):
    return '你点击了“地图”按钮'
# 菜单
client.create_menu({
	"button":[
		{
			"name":"教务",
			"sub_button":[
				{
					"type":"click",
					"name":"绑定教务",
					"key":"bdjw"
				},
				{
					"type":"click",
					"name":"成绩查询",
					"key":"cjcx"
				},
			]
		},
		{
			"name":"生活",
			"sub_button":[
				{
					"type":"click",
					"name":"后勤生活",
					"key":"hqsh"
				},
				{
					"type":"click",
					"name":"晨跑",
					"key":"cp"
				},
			]
		},
		{
			"name":"更多",
			"sub_button":[
				{
					"type":"click",
					"name":"了解我们",
					"key":"ljwm"
				},
				{
					"type":"click",
					"name":"校历",
					"key":"xl"
				},
				{
					"type":"click",
					"name":"地图",
					"key":"map"
				}
			]
		}
	]})


robot.run()
