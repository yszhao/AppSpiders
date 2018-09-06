#-*- coding: utf-8 -*-
import json
import pika
import time

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
    
    # 连接rabbitmq，
    credentials = pika.PlainCredentials('root', 'toor') 
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.3.219', 5672, '/', credentials))#172.18.22.2
    #connection = pika.BlockingConnection(pika.ConnectionParameters('172.18.22.2'))
    channel = connection.channel()

    channel.queue_bind(exchange='internal_hub', queue='external_BUPTSEND', routing_key='dynamicToInner')

    # 对要发送的json串分段发送
    step = 200 #段长

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
            print '[mq last]:', message
            channel.basic_publish(exchange='internal_hub', routing_key='dynamicex', body=message)  #发送
            print "last"
        else:
            # allowable stores: AndroidStore/googleplay/plugins/AppStore
            sendmessage = {'syb':'crawl_bupt', 'seq':'general', 'store':storeName, 'content': gen_seg, 'spider': spiderName, 'n' : x}   #构造普通段发送结构体，head标志用于中转区分，seq标志用于表示此段为普通段
            message = json.dumps(sendmessage)  #转为json格式
            print '[mq general]:', message
            channel.basic_publish(exchange='internal_hub', routing_key='dynamicex', body=message)  #发送
            print "general"
            
        time.sleep(0.2) # sleep 5毫秒(根据网络实际情况调整)，必须sleep,否则会串包或丢包

    if (remainder != 0):
        last_seg = encodejson[end:]
        # allowable stores: AndroidStore/googleplay/plugins/AppStore
        sendmessage = {'syb':'crawl_bupt', 'seq':'last', 'store':storeName, 'content': last_seg, 'spider': spiderName, 'n' : segnum}   #此为末段,seq标记为last
        message = json.dumps(sendmessage)
        print '[mq remainder]:', message
        channel.basic_publish(exchange='internal_hub', routing_key='dynamicToInner', body=message) #发送
        print "last"
    print "[x] Sent"

    connection.close()

# if __name__ == '__main__':
#     subject = "测试邮件"
#     msg = "测试一下"$ip
#     sendmail(subject,msg)
