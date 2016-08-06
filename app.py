from __future__ import unicode_literals
from flask import Flask, render_template,request
import requests
import json
import subprocess
import urlparse
import os
import sqlite3,binascii
import urllib
import sys
import time
import thread
reload(sys)
sys.setdefaultencoding('utf-8')
#import future
app = Flask(__name__)
count = 0
dic = {}
wait_time = 60  # amount of time in seconds to wait before reshowing message - used if repeat messages are passed.
@app.route('/' , methods=['GET', 'POST'] )
def index():
    if request.method  =='POST':
        print "printing JSON"
        data = request.get_json()
        if data is None :
            data = request.get_data();
            #result = data.split('&')
            result = urlparse.parse_qs(data)
            text = str(result['text'])[3:-2] #remove first char which is !
            print "RESULT FROM SLACK:" + text
            message_do(text, None )
        else:
            message =  data[u'messages'][0][u'text']
            app_user = data[u'appUser'][u'_id']
            print message
            message_do(message,app_user)
        #POST /v1/appusers/{smoochId|userId}/conversation/messages
        #appUser
        print "data userid is "
        return "Hello world !"

    return render_template('index.html')
    #return 'Hello World'
def message_do(message, app_user):
    msg = message
    banned_words = ["rm","shutdown","restart","sudo","su ", "vi", "vim", "nano", "emacs"]
    message = ' '.join([w for w in msg.split() if w not in banned_words])
    if message == 'hello':
        msg = "hi there!"
    elif "emoticon" in message:
        try:
            char = message.index(' ')

            msg = get_emoticon(message[(char+1):])
            print "MESSGE is : " + msg
            #msg = subprocess.Popen("echo %s"% msg, shell=True, stdout=subprocess.PIPE).stdout.read()
            msg = msg.replace('\n','')
        except ValueError:
            #print "no emoticon!"
            msg = "no emoticon"
    elif "#" in message:
        if is_repeat(message):
            print "repeated " +count + "times: "+ message
            return
        char = message.index('#')
        print message.replace("'","\\'")
        thread.start_new_thread(threadCommand, message, "say" )
        #subprocess.Popen("say \"%s\""%message[(char+1):], shell=True, stdout=subprocess.PIPE).stdout.read()
    elif "/" in message:
        if "rm" in message:
            msg = "ooopsies!"
        elif "shutdown" in message:
            msg = "ooopsies!"
        else:
            char = message.index('/')
            #msg= os.system(message[char:])
            thread.start_new_thread(threadCommand, message, "echo" )
            #msg = subprocess.Popen("echo $(%s)"%message[(char+1):], shell=True, stdout=subprocess.PIPE).stdout.read()

    print "MESSAGE:" + msg
    if app_user is None:
        send_message_to_SLACK(msg)
        #subprocess.Popen("python apptalk.py '%s'"%msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    else:
        #subprocess.Popen("python apptalk.py fb %s '%s'"% (app_user,msg), shell=True, stdout=subprocess.PIPE).stdout.read()
        send_message_to_FB(msg,app_user)
    return

def threadCommand(message,cmd):
    subprocess.Popen("cmd"+" \"%s\""%message[(char+1):], shell=True, stdout=subprocess.PIPE).stdout.read()
    return


def isRepeat(message):
     try:
         prev_time = dic[message]
     except KeyError:
         dic[message] = time.gmtime()
         return False
    cur_time =time.gmtime(time.time()-wait_time)
    if prev_time < cur_time:
        dic[message] = time.gmtime()
        return True

    return False


def send_to_email(message, subject,to_mail):
    pass

def send_message_to_FB(message, app_user):
    #print "APPuser:" + app_user
    headers = {'content-type': 'application/json' ,'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFwcF81NzkwZDdmZjRlYjRiMzQ0MDAwYWEzMDYifQ.eyJzY29wZSI6ImFwcCJ9.5aks5Q7jvTZ67YR9Km_07GJ46WnDwkRCNSGZePTTU6I'}
    payload = '{"text": "%s", "role": "appMaker"}'
    print "PAYLOAD IS:" + str(payload%message).replace('\n', ',')
    url = 'https://api.smooch.io/v1/appusers/'+ app_user + '/conversation/messages'
    r = requests.post(url = url, data = str(payload%message).replace('\n', ','), headers= headers)
    print r.status_code

def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

def get_emoticon(key):
    conn = sqlite3.connect('sqlite_file.db')
    c = conn.cursor()
    params = (key,)
    c.execute("SELECT value FROM lookup WHERE key=? LIMIT 1", params)
    all_rows = c.fetchone()
    if all_rows is None:
        return "No emoticon"
    print  all_rows[0]
    return all_rows[0]


if __name__ == '__main__' :
    app.run(debug=True, host ='0.0.0.0')
