#!/usr/bin/env python2.7
# encoding: utf-8
# -*- coding: utf8 -*-
import urllib
import urllib2
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import os
corpid="ww3a7da140a1da4c3b"
secrect="UEhNijhPIWshadnfGEPpg9xBNyauHgf3uWQXQvG6-Mk"
def get_access_token(cid,sct):
    access_token_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+corpid+"&corpsecret="+secrect
    res_data = urllib2.urlopen(access_token_url)
    access_token=json.loads(res_data.read())["access_token"]
    return access_token
if os.path.exists("/tmp/weixinalarm"):
    with open("/tmp/weixinalarm","r+") as fd:
	result_info=fd.read().split("^")
        timestamp=result_info[1]
        if time.time()-int(timestamp) <7200:
            access_token=result_info[0]
        else:
            access_token=get_access_token(corpid,secrect)
else:
    print "file is not exists"
    access_token=get_access_token(corpid,secrect)
    timestamp=time.time()
    tokentime=access_token+"^"+str(timestamp).split(".")[0]
    with open("/tmp/weixinalarm","w") as fd:
        fd.write(tokentime)
send_url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+access_token
send_info={
		"touser" : "@all",
		"msgtype" : "text",
		"agentid" : 1000003,
		"text" : {
			"content":"娱乐站报警"
			}
		}
#send_info_urlencode = urllib.urlencode(send_info)
#send_info_urlencode = json.dumps(send_info,False,False)
send_info_urlencode = json.dumps(send_info,ensure_ascii=False)
print send_info_urlencode
req=urllib2.Request(url = send_url,data =send_info_urlencode)
response=urllib2.urlopen(req)
res_info=response.read()
print res_info
