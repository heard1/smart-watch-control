#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 15:26:03 2018

@author: lisicong
"""

from aliyunsdkcore import client
from aliyunsdkiot.request.v20180120 import RegisterDeviceRequest
from aliyunsdkiot.request.v20180120 import PubRequest
import base64

def bulb(order):
    
    accessKeyId = 'LTAIoEUkoPmOjLRN'
    accessKeySecret = 'l5XDvN8BMhdXmJzHEKHev9Ewe9fr39'
    clt = client.AcsClient(accessKeyId, accessKeySecret, 'cn-shanghai')
    
    request = PubRequest.PubRequest()
    request.set_accept_format('json')  #设置返回数据格式，默认为XML
    request.set_ProductKey('a18DjwTTbRl')
    request.set_TopicFullName('/a18DjwTTbRl/bulb/get')  #消息发送到的Topic全名
    
    message = order
    message = base64.b64encode(message.encode('utf-8'))
    
    request.set_MessageContent(message)  #hello world Base64 String
    request.set_Qos(0)
    result = clt.do_action_with_exception(request)