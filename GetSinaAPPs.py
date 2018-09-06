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

def getTotal(cat, secondcat, offset, num):
	Total = 0
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
		jsonStr = json.loads(html)
		if jsonStr.has_key('info') and jsonStr['info'].has_key('total'):
			Total = int(jsonStr['info']['total'])
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
	cat = '100'
	#secondCat = ['104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115']
	secondCat = ['114'] #101,102,103,104,105,109,110,111
	offset = 0
	num = 5000
	for sec in secondCat:
		total = getTotal(cat, sec, offset, num)
		mod = total % num
		print '****cat:', cat, ', secondCat:', sec, ', total', total, ', mod:', mod
		offset = 0
		for offset in range(0, total, num):
			if offset + num > total:
				print '#cat:', cat, ', secondCat:', sec, ', offset:', offset, ', num:', mod
				getHtml(cat, sec, offset, mod)
				break
			print 'cat:', cat, ', secondCat:', sec, ', offset:', offset
			getHtml(cat, sec, offset, num)

	'''
	cat1 = '200'
	#secondCat1 = ['201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212']
	secondCat1 = ['212'] #201,202,203,204,205,206,207,208,209,210,211
	offset1 = 0
	num1 = 5000
	for sec1 in secondCat1:
		total = getTotal(cat1, sec1, offset1, num1)
		mod = total % num1
		print '****cat1:', cat1, ', secondCat1:', sec1, ', total', total, ', mod:', mod
		offset1 = 0
		for offset1 in range(0, total, num1):
			if offset1 + num1 > total:
				print '#cat1:', cat1, ', secondCat1:', sec1, ', offset1:', offset1, ', num:', mod
				getHtml(cat1, sec1, offset1, mod)
				break
			print 'cat1:', cat1, ', secondCat1:', sec1, ', offset1:', offset1
			getHtml(cat1, sec1, offset1, num1)

		
