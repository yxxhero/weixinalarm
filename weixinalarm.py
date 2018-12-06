#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf8 -*-
import urllib2
import hashlib
import json
import sys
import time
import os
import logging
reload(sys)
sys.setdefaultencoding('utf8')
#日志模式初始化
logging.basicConfig(level="DEBUG",
                format='%(asctime)s  %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='./log/status.log',
                filemode='a')
class weixinalarm(object):
    def __init__(self,corpid,secrect,agentid):
        self.corpid=corpid
        self.secrect=secrect
        self.agentid=agentid
    def get_access_token(self):
        access_token_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+self.corpid+"&corpsecret="+self.secrect
        try:
            res_data = urllib2.urlopen(access_token_url,timeout=3)
            access_token=json.loads(res_data.read())["access_token"]
        except Exception,e:
            logging.info(str(e))
            logging.info("access_token获取超时")
            return None 
        else:
            return access_token
    def check_token(self):
        if os.path.exists("/tmp/"+str(self.Md5value())):
            with open("/tmp/"+str(self.Md5value()),"r+") as fd:
	        result_info=fd.read().split("^")
                timestamp=result_info[1]
                if time.time()-int(timestamp) <7200:
                    access_token=result_info[0]
		    return access_token
                else:
                    access_token=self.get_access_token()
                    timestamp=time.time()
                    tokentime=access_token+"^"+str(timestamp).split(".")[0]
                    with open("/tmp/"+str(self.Md5value()),"w") as fd:
                        fd.write(tokentime)
		    return access_token
        else:
            access_token=self.get_access_token()
            timestamp=time.time()
            tokentime=access_token+"^"+str(timestamp).split(".")[0]
            with open("/tmp/"+str(self.Md5value()),"w") as fd:
                fd.write(tokentime)
	    return access_token
    def Md5value(self):
        m2 = hashlib.md5()
        m2.update(str(self.agentid)+str(self.corpid)+str(self.secrect))
        return m2.hexdigest()
    def sendmsg(self,title,description):
        try:
	    access_token=self.check_token()
            if access_token:
                send_url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+access_token
                send_info={
	        	"touser" : "@all",
	        	"msgtype" : "text",
	        	"agentid" : self.agentid,
                "text":{
                    "content":str(title)+":"+str(description)
                    }
	        	}
                logging.info(send_info)
                send_info_urlencode = json.dumps(send_info)
                #send_info_urlencode = json.dumps(send_info,ensure_ascii=False)
                req=urllib2.Request(url = send_url,data =send_info_urlencode)
                response=urllib2.urlopen(req,timeout=3)
                res_info=response.read()
            else:
                logging.error("no access_token")
        except Exception,e:
            logging.error(str(e))
        else:
            alarm_result=json.loads(res_info)
            if int(alarm_result["errcode"])==0:
                logging.info("报警正常")
            else:
                logging.info(alarm_result["errmsg"])
        finally:
            if response:
                response.close()
