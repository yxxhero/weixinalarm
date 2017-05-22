#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf8 -*-
import urllib
import urllib2
import json
import sys
import time
import os
reload(sys)
sys.setdefaultencoding('utf8')
class weixinalarm:
    def __init__(self,corpid,secrect):
        self.corpid=corpid
	self.secrect=secrect
    def get_access_token(self):
        access_token_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+self.corpid+"&corpsecret="+self.secrect
        res_data = urllib2.urlopen(access_token_url)
        access_token=json.loads(res_data.read())["access_token"]
        return access_token
    def check_token(self):
        if os.path.exists("/tmp/weixinalarm"):
            with open("/tmp/weixinalarm","r+") as fd:
	        result_info=fd.read().split("^")
                timestamp=result_info[1]
                if time.time()-int(timestamp) <7200:
                    access_token=result_info[0]
		    return access_token
                else:
                    access_token=self.get_access_token()
		    return access_token
        else:
            print "file is not exists"
            access_token=self.get_access_token()
            timestamp=time.time()
            tokentime=access_token+"^"+str(timestamp).split(".")[0]
            with open("/tmp/weixinalarm","w") as fd:
                fd.write(tokentime)
	    return access_token
    def sendmsg(self,title,description):
	access_token=self.check_token()
        send_url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+access_token
        send_info={
		"touser" : "@all",
		"msgtype" : "news",
		"agentid" : 1000004,
                "news":{
                "articles" : [
                 {
               "title" : title,
               "description" : description,
               "url" : "http://www.yslongbi.com/category/star_news/?starId=22",
               "picurl" : "http://bimg.tubaba.com.cn/http://img5.imgtn.bdimg.com/it/u=3850328790,3088893369&fm=23&gp=0.jpg"
                   }
                 ]
                 }
		}
        send_info_urlencode = json.dumps(send_info,ensure_ascii=False)
        req=urllib2.Request(url = send_url,data =send_info_urlencode)
        response=urllib2.urlopen(req)
        res_info=response.read()
