# -*- coding:UTF-8 -*-
__author__ = 'zhaoys'
import sched, time, os, datetime
from threading import Timer
from sendMail import mail
from xml.etree import ElementTree as XmlTree
import json
import sys, getopt
import re, urllib, urllib2, socket
import lxml.html
import logging
from utils.sendToMQ import sendToZW
#from utils.sendToUDP import sendToZW

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='iTunesCrawler.log',
                filemode='a')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

count = 1  

def getAppInfo(html):
	jsonStr = json.loads(html)
	global count
	wrapperId = "weibo"
	wrapperName = "新浪应用商店"
	app_information = {}
	file_obj = open('weiboVpnList.txt', 'a+')
	try:
		for app in jsonStr['info']['list']:
			app_information["url"] = "http://mapp.uve.weibo.com/appdetail.php?appID=" + app['appID']
			app_information["size"] = str(int(app['size'])) + "M"
			app_information["osVersion"] = ""
			app_information["updatedTime"] = ""
			app_information["appName"] = app['name']
			app_information["appVersion"] = app['name']
			app_information["downloadUrl"] = app['name']
			app_information["category"] = app['category']
			app_information["osType"] = "Android"
			app_information["description"] = app['name_cut']
			app_information["downloadFloor"] = app['downloadTimes']
			app_information["snapshotUrlList"] = ""
			app_information["developerName"] = ""
			app_information["title_pic"] = app['iconUrl']

			appIdstr = md5(wrapperId + app_information["url"] + app_information["appVersion"])
			m = re.search('vpn', app_information["appName"], re.IGNORECASE)
			if ("加速器" in app_information["appName"] and ("上网" in app_information["appName"] 
				or "网络" in app_information["appName"] or "互联网" in app_information["appName"])) or bool(m):
				print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ App Begin @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
				print wrapperId, 'app spider have found', count, 'apps!'
				print "url:", app_information["url"]
				#print "size:", app_information["size"]
				#print "osVersion:", app_information["osVersion"]
				#print "updatedTime:", app_information["updatedTime"]
				print "appName:", app_information["appName"]
				#print "appVersion:", app_information["appVersion"]
				#print "downloadUrl:", app_information["downloadUrl"]
				#print "category:", app_information["category"]
				#print "osType:", app_information["osType"]
				#print "description:", app_information["description"]
				#print "snapshotUrlList:", app_information["snapshotUrlList"]
				#print "developerName:", app_information["developerName"]
				#print "appIdstr:", appIdstr
				print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ App End @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
				file_obj.write(app_information["appName"] + '\t' + app_information["url"] + '\n')
        
			#downloadTitlePic(appIdstr, app_information["url"])
			#sendToZW(wrapperId, wrapperName, appIdstr, app_information)
		
			count = count + 1
		file_obj.close()
	except UnicodeEncodeError, e:
		print e.message
	except OSError:
		print OSError

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


#根据给定的网址来获取网页详细信息，得到的html就是网页的源代码
def getHtml(cat, secondcat, offset, num):
	html = ''
	try:
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
		headers = {'User-Agent' : user_agent}
		test_data = {'cat':cat,'secondcat':secondcat,'offset':offset,'num':num}
		test_data_urlencode = urllib.urlencode(test_data)
		req = urllib2.Request("http://mapp.uve.weibo.com/ajax_catlist.php", data=test_data_urlencode)
		req.add_header('User-Agent', user_agent)
		#req.add_header("Host", "appstore.huawei.com")
		response = urllib2.urlopen(req)
		response.geturl()
		html = response.read()
		#print html
		getAppInfo(html)
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

def getTotal():
	Total = 0
	try:
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
		headers = {'User-Agent' : user_agent}
		req = urllib2.Request("https://androidappsapk.co/search/vpn/")
		req.add_header('User-Agent', user_agent)
		response = urllib2.urlopen(req)
		response.geturl()
		html = response.read()
		doc = lxml.html.fromstring(html)
		print html
		Total_text = doc.xpath('//div[@class="page-content"]/div[1]/p/text()')
		print Total_text
		
	except urllib2.URLError, e:
		#print "ee", e.code
		print "ee", e.reason
		#print "ee", e.geturl()
		#print "ee", e.read()
		return Total
	except urllib2.HTTPError, e:  
		print e.code
    	return Total

	return Total

#main function
if __name__ == '__main__':
	offset = 0
	num = 5000
	total = getTotal()
	
	
