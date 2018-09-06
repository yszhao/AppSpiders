#-*- coding: utf-8 -*-
import json
import pika
import time
import socket
import re

def toHH(n):
    a = n & 0xff
    b = n >> 8 & 0xff
    c = n >> 16 & 0xff
    d = n >> 24 & 0xff
    return bytearray([d,c,b,a])

def sendToZW(wrapperId, wrapperName, appIdstr, app_information):
    country = ''
    price = ''
    if app_information.has_key('country'):
        country = app_information["country"]
        print country
    if app_information.has_key('price'):
        price = app_information["price"]
        print price
    sendstr =  {'wrapperId':wrapperId, 
                'wrapperName':wrapperName, 
                'appIdstr':appIdstr,
                'appurl': app_information["url"], 
                'appsize': app_information["size"],
                'osVersionstr': app_information["osVersion"],
                'updatetime': app_information["updatedTime"],
                'appNamestr': app_information["appName"], 
                'appVersionstr': app_information["appVersion"],
                'downloadUrlstr': app_information["downloadUrl"], 
                'categorystr': app_information["category"], 
                'osTypestr': app_information["osType"], 
                'description': app_information["description"], 
                'downnumber': app_information["downloadFloor"], 
                'imageurl': ";".join(app_information["snapshotUrlList"]),
                'developer': app_information["developerName"],
                'title_picture': app_information["title_pic"],
                'recommend': '',
                'country' : country,
                'price' : price,
                'device' :'',}
            
    encodejson = json.dumps(sendstr)

    length =  len(encodejson)  #要发送的json串长度

    print 'encodejson length:', length  #打印json串长度
    #print encodejson
    
    # 创建socket，udp send config V to Z, V网隔离机：10.199.126.251/56506
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #clientSock.connect(('10.199.126.251', 56506))这个是建立TCP连接！
    addr = ('10.199.126.251', 56506)
    
    # 对要发送的json串分段发送
    step = 3000 #段长

    segnum = length / step  #分的段数
    print '分的段数:', segnum

    remainder = length % step  #剩余的字符数

    storeName = 'AppStore'
    spiderName = 'iTunesAlone'
        
    begin = 0  #起始坐标
    end = 0    #终点坐标
    for x in range(0, segnum):
        beg = end
        end = beg + step
        gen_seg = encodejson[beg:end]   #每次以一个步长构造一个json发送段
        if (end == length):
            # allowable stores: AndroidStore/googleplay/plugins/AppStore
            sendmessage = {'syb':'crawl_bupt', 'seq':'last', 'store':storeName, 'content': gen_seg, 'spider': spiderName, 'n' : x}   #为末段,seq标记为last
            message = json.dumps(sendmessage)  #转为json格式
            print '[udp last]:', message
            sign = bytearray('ctdk', 'utf-8')  
            ip = toHH(6492)
            msg = bytearray(message, 'utf-8')
            ss = sign + ip + msg
            print 'len(ss):', len(ss)
            clientSock.sendto(ss, addr)  #发送
            print "last"

        else:
            # allowable stores: AndroidStore/googleplay/plugins/AppStore
            sendmessage = {'syb':'crawl_bupt', 'seq':'general', 'store':storeName, 'content': gen_seg, 'spider': spiderName, 'n' : x}   #构造普通段发送结构体，head标志用于中转区分，seq标志用于表示此段为普通段
            #print sendmessage
            message = json.dumps(sendmessage)  #转为json格式
            print '[udp general]:', message
            sign = bytearray('ctdk', 'utf-8')  
            ip = toHH(6492)
            msg = bytearray(message, 'utf-8')
            ss = sign + ip + msg
            print 'len(ss):', len(ss)
            clientSock.sendto(ss, addr)  #发送
            print "general"
            
        time.sleep(0.2) # sleep 5毫秒(根据网络实际情况调整)，必须sleep,否则会串包或丢包

    if (remainder != 0):
        last_seg = encodejson[end:]
        # allowable stores: AndroidStore/googleplay/plugins/AppStore
        sendmessage = {'syb':'crawl_bupt', 'seq':'last', 'store':storeName, 'content': last_seg, 'spider': spiderName, 'n' : segnum}   #此为末段,seq标记为last
        message = json.dumps(sendmessage)
        print '[udp remainder]:', message
        sign = bytearray('ctdk', 'utf-8')  
        ip = toHH(6492)
        msg = bytearray(message, 'utf-8')
        ss = sign + ip + msg
        print 'len(ss):', len(ss)
        clientSock.sendto(ss, addr)  #发送
        print "last"

    print "[x] Sent"

    clientSock.close()

# if __name__ == '__main__':
#     subject = "测试邮件"
#     msg = "测试一下"
#     sendmail(subject,msg)
