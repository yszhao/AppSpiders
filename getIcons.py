# -*- coding:UTF-8 -*-
__author__ = 'zhaoys'

import sys, os
import xlrd
import urllib, urllib2, lxml.html

reload(sys)
sys.setdefaultencoding('utf-8')

def getHtml(url):
	html = ''
	try:
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		headers = {'User-Agent' : user_agent}

		req = urllib2.Request(url)
		req.add_header('User-Agent', user_agent)
		req.add_header("Host", "itunes.apple.com:443")
		response = urllib2.urlopen(req)
		response.geturl()
		html = response.read()
	except urllib2.URLError, e:
		#print "ee", e.code
		print "ee", e.reason
		#print "ee", e.geturl()
		#print "ee", e.read()
		return html
	except urllib2.HTTPError, e:  
		print e.code
    	return html

	return html

def downloadTitlePic(appInfo):
	appIdstr = appInfo[1]
	url = appInfo[2]

	if "google" in url:
		return

	filePath = './icons/' + appIdstr + '.jpg'
	if os.path.exists(filePath):
		#print filePath, 'exists, dont need download any more!!'
		return

	print 'url:', url, ', appIdstr:', appIdstr
	title_pic = getIconUrl(url)

	if len(title_pic) > 0:
		print 'icon image url:', title_pic[0]
		urllib.urlretrieve(title_pic[0], './icons/' + appIdstr + '.jpg')

def getIconUrl(url):
	title_pic = []
	xpath = ''
	#page = urllib.urlopen(url)
	html = getHtml(url)

	#print 'html:', html
	if "正在连接到" in html or "Connecting to the iTunes Store" in html or "div" not in html:
		return title_pic

	if "android.myapp.com" in url:
		xpath = '//div[@id="det-icon"]/img/@src'
	elif "itunes.apple.com" in url:
		xpath = '//div[@id="left-stack"]/div/a/div/meta/@content'
	elif "app.appvv.com" in url:
		xpath = '//div[@class="icon"]/img/@src'
	elif "app.lenovo.com" in url:
		xpath = '//div[@class="detailIcon pr fl"]/img/@src'
	elif "app.meizu.com" in url:
		xpath = '//div[@class="app_download download_container"]/img/@src'
	elif "app.mi.com" in url:
		xpath = '//div[@class="app-info"]/img/@src'
	elif "app.taobao.com" in url:
		xpath = '//div[@id="J_DailyAppContent"]/div/a/img/@src'
	elif "app.tongbu.com" in url:
		xpath = '//div[@class="app-icon165"]/img/@src'
	elif "shouji.baidu.com" in url:
		xpath = '//div[@class="app-pic"]/img/@src'
	elif "sj.zol.com.cn" in url:
		xpath = '//div[@class="soft-div"]/span/img/@src'
	elif "www.anzhi.com" in url:
		xpath = '//div[@class="detail_icon"]/img/@src'
		doc = lxml.html.fromstring(html)
		picurl = "http://" + "www.fpwap.com" + doc.xpath(xpath)[0]
		title_pic.extend(picurl)
		return title_pic
	elif "www.appchina.com" in url:
		xpath = '//div[@class="app-detail"]/div/img/@src'
	elif "www.fpwap.com" in url:
		xpath = '//div[@class="gameinfor-left"]/dl/dd/img/@src'
		doc = lxml.html.fromstring(html)
		picurl = "http://" + "www.fpwap.com" + doc.xpath(xpath)[0]
		if "smallpic" in picurl:
			return []
		print 'picurl:', picurl
		title_pic.append(picurl)
		return title_pic
	elif "zhushou.360.cn" in url:
		xpath = '//div[@id="app-info-panel"]/div/dl/dt/img/@src'
	elif "app.appvv.com" in url:
		xpath = '//div[@class="icon"]/img/@src'
	elif "ios.kuchuan.com" in url:
		xpath = '//div[@class="left_icon"]/img/@src'
	elif "google" in url:
		return []

	
	#print html
	doc = lxml.html.fromstring(html)
	title_pic = doc.xpath(xpath)

	return title_pic


#main function
if __name__ == '__main__':
	files = os.listdir("./")
	for file in files:
		if os.path.isfile(file) and "py" not in file:
			print '########################filename#####################:', file
			data = xlrd.open_workbook(file) # 打开xls文件
			table = data.sheets()[0] # 打开第一张表
			nrows = table.nrows # 获取表的行数
			print '$$$$$$$$$$$nrows:', nrows
			for i in range(nrows): # 循环逐行打印
				if i == 0: # 跳过第一行
					continue
				#print table.row_values(i)[:3] # 取前三列
				downloadTitlePic(table.row_values(i)[:3])