# -*- coding:UTF-8 -*-
__author__ = 'zhaoys'
import sched, time, os, datetime
from threading import Timer
from sendMail import mail
from xml.etree import ElementTree as XmlTree
import json
import sys, getopt
import re, urllib, urllib2, httplib
from httplib import HTTPException
import lxml.html
import logging, random
from random import choice
from utils.sendToMQ import sendToZW
#from utils.sendToUDP import sendToZW
from utils.DbUtil import DbOper
import socket, subprocess, signal
import threadpool

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

dbOper = DbOper('TEST')

count = 1
Accounts = {}
Accounts["roc04998@icloud.com"] = "Xx223322"
Accounts["d31p29el@icloud.com"] = "Xx223322"
Accounts["zmp7p777@icloud.com"] = "Xx223322"
Accounts["j94n1956@icloud.com"] = "Xx223322"
Accounts["or801w57@icloud.com"] = "Xx223322"
Accounts["uvw41486@uzrip.com"] = "Ceshi123"
Accounts["v1141e22@icloud.com"] = "Xx223322"
Accounts["k7qt0dm9@icloud.com"] = "Xx223322"
Accounts["x2e4v1oo@icloud.com"] = "Xx223322"
Accounts["zkk9x12b@icloud.com"] = "Xx223322"
Accounts["beh9vu5k@icloud.com"] = "Xx223322"

wrapperId = u"AppStoreHK"
wrapperName = u"iOS应用官方商店香港区"
country = u"hk"

def getTrackIDs(filepath):
	doc = XmlTree.parse(filepath)
	root = doc.getroot()
	print root.attrib, root.tag
	array = root.getchildren()[0].getchildren()
	AppIds = []
	for node in array:
		#getAppInfo(node.text) 
		AppIds.append(node.text)


	pool = threadpool.ThreadPool(30)
	requests = threadpool.makeRequests(getAppInfoJson, AppIds)
	for req in requests:  
		pool.putRequest(req)
	pool.wait()

def getAppInfoJson(text):
	html = getHtml(text)
	#print 'html:', html
	try:
		jsonStr = json.loads(html)
		print jsonStr["resultCount"], jsonStr["resultCount"] == 1
		if jsonStr["resultCount"] == 1:
			getAppInfo(jsonStr)
	except ValueError as ve:
		print ve
	except KeyError as ke:
		print ke
	except Exception as e:
		print e
        #break
	time.sleep(2)

def getCNAccount():
	global Accounts
	return choice(Accounts.keys())
	#print choice(Accounts.keys()), Accounts[choice(Accounts.keys())]
	#print choice(Accounts.keys()), Accounts[choice(Accounts.keys())]

def getAppInfo(jsonStr):
	global count
	global wrapperId
	global wrapperName
	app_information = {}
	try:
		app_information["wrapperId"] = wrapperId
		app_information["wrapperName"] = wrapperName
		app_information["url"] = jsonStr['results'][0]['trackViewUrl']
		app_information["size"] = str(int(jsonStr['results'][0]['fileSizeBytes']) / 1000 / 1000) + "M"
		app_information["osVersion"] = jsonStr['results'][0]['minimumOsVersion']
		app_information["updatedTime"] = jsonStr['results'][0]['currentVersionReleaseDate']
		app_information["appName"] = jsonStr['results'][0]['trackName']
		app_information["appVersion"] = jsonStr['results'][0]['version']
		app_information["downloadUrl"] = jsonStr['results'][0]['trackId']
		app_information["category"] = jsonStr['results'][0]['primaryGenreName']
		app_information["osType"] = "iOS"
		app_information["description"] = jsonStr['results'][0]['description']
		app_information["downloadFloor"] = ""
		app_information["snapshotUrlList"] = jsonStr['results'][0]['screenshotUrls']
		app_information["developerName"] = jsonStr['results'][0]['sellerName']
		app_information["title_pic"] = ""
		app_information["country"] = app_information["url"].split("/")[3]
		app_information["price"] = jsonStr['results'][0]['price']

		appIdstr = md5(wrapperId + app_information["url"] + app_information["appVersion"])
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ App Begin @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
		print wrapperId, 'app spider have found', count, 'apps!'
		print "url:", app_information["url"]
		print "size:", app_information["size"]
		print "osVersion:", app_information["osVersion"]
		print "updatedTime:", app_information["updatedTime"]
		print "appName:", app_information["appName"]
		print "appVersion:", app_information["appVersion"]
		print "downloadUrl:", app_information["downloadUrl"]
		print "category:", app_information["category"]
		print "osType:", app_information["osType"]
		print "description:", app_information["description"]
		print "snapshotUrlList:", app_information["snapshotUrlList"]
		print "developerName:", app_information["developerName"]
		print "country:", app_information["country"]
		print "price:", app_information["price"]
		print "appIdstr:", appIdstr
		app_information["appIdstr"] = appIdstr
		
		#downloadTitlePic(appIdstr, app_information["url"])
		#sendToZW(wrapperId, wrapperName, appIdstr, app_information)
		dbOper.insertIosAppDB(app_information)
		#downloadIpa(appIdstr, app_information)
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ App End @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
		count = count + 1
	except UnicodeEncodeError, e:
		print e.message
	except OSError:
		print OSError
	except Exception as e:
		print e

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

def getHtml(trackID):
	global country
	url = "http://itunes.apple.com/lookup?id=" + trackID + "&country=" + country
	print 'trackUrl:', url
	html = ''
	try:
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
		headers = {'User-Agent' : user_agent}

		req = urllib2.Request(url)
		req.add_header('User-Agent', user_agent)
		#req.add_header("Host", "appstore.huawei.com")
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

def downloadTitlePic(appIdstr, url):
	filePath = './ImgTmp/' + appIdstr + '.jpg'
	if os.path.exists(filePath):
		print filePath, 'exists, dont need download any more!!'
		return
	try:
		page = urllib.urlopen(url)
		html = page.read()
		if "正在连接到" in html or "Connecting to the iTunes Store" in html or "div" not in html:
			return
		#print html
		doc = lxml.html.fromstring(html)
		title_pic = doc.xpath('//div[@id="left-stack"]/div/a/div/meta/@content')

		if len(title_pic) > 0:
			print 'icon image url:', title_pic[0]
			urllib.urlretrieve(title_pic[0],'./ImgTmp/' + appIdstr + '.jpg')
	except urllib2.URLError, e:
		#print "ee", e.code
		print "ee", e.reason
		#print "ee", e.geturl()
		#print "ee", e.read()
	except urllib2.HTTPError, e:  
		print e.code
	except HTTPException,e:
		print e.code

def downloadIpa(appIdstr, app_information):
	downloadURL = ''
	filePath = './ipas/' + appIdstr + '.ipa'
	if os.path.exists(filePath):
		print filePath, 'exists, dont need download any more!!'
		return

	if app_information["country"] in ['cn', 'us'] and "Games" not in app_information["category"] and "Music" not in app_information["category"]:
		key = getCNAccount()
		cmd1 = 'iTunes.exe ' + str(app_information["downloadUrl"]) + ' ' + str(key) + ' ' + str(Accounts[key])
		start = datetime.datetime.now()
		print cmd1
		#fp = os.popen(cmd1)
		#downloadURL = fp.read()
		process = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
		while process.poll() is None:  
			time.sleep(0.2)  
			now = datetime.datetime.now()
			#print "(now - start).seconds:", (now - start).seconds
			if (now - start).seconds > 300:  
				#os.kill(process.pid, signal.SIGKILL)  
				#os.waitpid(-1, os.WNOHANG)  
				return
		
		downloadURL = process.stdout.readlines()
		
	try:
		print 'downloadURL:', downloadURL, len(downloadURL)
		if len(downloadURL) == 1 and "http://" in downloadURL[0]:
			urllib.urlretrieve(downloadURL[0], filePath)
	except socket.timeout as e:  
		print("-----socket timout:", downloadURL[0]) 
	except urllib2.URLError, e:
		#print "ee", e.code
		print "ee", e.reason
		#print "ee", e.geturl()
		#print "ee", e.read()
	except urllib2.HTTPError, e:  
		print e.code

#main function
if __name__ == '__main__':
	socket.setdefaulttimeout(300)
	dirname = u"香港term"
	wrapperId = u"AppStoreHK"
	wrapperName = u"iOS应用官方商店香港区"
	country = u"hk"
	print 'country:', country
	files = os.listdir(dirname)
	for file in files:
		if os.path.isfile(dirname + "/" + file) and "ok" not in file:
			getTrackIDs(dirname + "/" + file)
			os.rename(dirname + "/" + file , dirname + "/ok_" + file)

	dirname = u"中国term"
	wrapperId = u"AppStoreCN"
	wrapperName = u"iOS应用官方商店中国区"
	country = u"cn"
	files = os.listdir(dirname)
	for file in files:
		if os.path.isfile(dirname + "/" + file) and "ok" not in file:
			getTrackIDs(dirname + "/" + file)
			os.rename(dirname + "/" + file , dirname + "/ok_" + file)

	dirname = u"台湾term"
	wrapperId = u"AppStoreTW"
	wrapperName = u"iOS应用官方商店台湾区"
	country = u"tw"
	files = os.listdir(dirname)
	for file in files:
		if os.path.isfile(dirname + "/" + file) and "ok" not in file:
			getTrackIDs(dirname + "/" + file)
			os.rename(dirname + "/" + file , dirname + "/ok_" + file)
