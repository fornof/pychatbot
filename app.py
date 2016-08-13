 # coding=utf-8
from __future__ import unicode_literals
from flask import Flask, render_template,request
import requests
import urlparse
import json
import subprocess
import os
import sqlite3,binascii
import sys
import time
from do.question import Question
reload(sys)
sys.setdefaultencoding('utf-8')
#import future
app = Flask(__name__)
count = 0
dic = {}
command_history= {}
lastMessage = []
wait_time = 60  # amount of time in seconds to wait before reshowing message - used if repeat messages are passed.
wait_time_command = 1
say = "say"
q = Question()
current_question = Question()
@app.route('/' , methods=['GET', 'POST'] )
def index():
    if request.method  =='POST':
        #print "printing JSON"
        data = request.get_json()
        if data is None :
            data = request.get_data();
            #result = data.split('&')
            result = urlparse.parse_qs(data)
            text = result['text'][0] #remove first char which is !
            print "RESULT FROM SLACK:" + str(text)
            message_do(text, None )
        else:
            message =  data[u'messages'][0][u'text']
            app_user = data[u'appUser'][u'_id']
            print message
            message_do(message,app_user)
        #POST /v1/appusers/{smoochId|userId}/conversation/messages
        #appUser
        #print "data userid is "
        return "Hello world !"

    return render_template('index.html')
    #return 'Hello World'

# input message like #hello or hello , this trims that first char if special, and returns the message.
def trim(message):
    if"#" == message[0] or "!" == message[0]:
        return message[1:]
    else:
        return message

def message_do(message, app_user):
    repeated = False
    msg = str(message)
    banned_words = ["rm","shutdown","restart","sudo","su ", "vi", "vim", "nano", "emacs"]
    message = ' '.join([w for w in msg.split() if w not in banned_words])
    msg_len = len(message)
    if message[0] == '~':
        print "IGNORING"
        return
    if '!q' in message.lower()or "!start" in message.lower():

        questions = q.loadAllQuestions(None)
        print "questions are " + str(questions)
        msg = questions[0].text
    elif "#" in message:
        if isRepeat(message,dic,wait_time):
            print "repeated "
            repeated = True
            return

        char = message.index('#')
        message= message.replace("'","\'")
        message = str(message[(char+1):])
        #if "#" in message:
        #    #if ## , change voice to Bruce, use the next index
        #    message = message[(char+1):]
        #    print "using 2 #:, should be no # ::" + message
        #    commandNoRepeat("say -v Agnes", message)
        #else:
            #thread.start_new_thread(threadCommand, (message, "say") )
        command("say", message)
    elif "/" in message:
        if "rm" in message:
            msg = "ooopsies!"
        elif "shutdown" in message:
            msg = "ooopsies!"
        else:
            char = message.index('/')
            #msg= os.system(message[char:])
            message = message[(char+1):]
            #thread.start_new_thread(threadCommand, (message, "echo") )
            msg = subprocess.Popen("echo $(%s)"%message[(char+1):], shell=True, stdout=subprocess.PIPE).stdout.read()

    elif msg_len < 3 and msg_len > 0:
        if message[0].lower() == 'r':
            if msg_len > 1 :
                if message[1].lower() =='q':
                    commandNoRepeat("say", 'I am sorry but I did not understand. Could you repeat that?')
                    return
            #repeat last message by pulling it from the dic
            print "Saying last message" + str(lastMessage[-1])
            commandNoRepeat("say", str(lastMessage[-1]))
            return
        if message[0].lower() == "q":
            #current_question = question.next
            command("say" ,"question.text")
    print "MESSAGE:" + msg
    if app_user is None:
        send_message_to_SLACK(msg)
        #subprocess.Popen("python apptalk.py '%s'"%msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    else:
        #subprocess.Popen("python apptalk.py fb %s '%s'"% (app_user,msg), shell=True, stdout=subprocess.PIPE).stdout.read()
        send_message_to_FB(msg,app_user)
    return
def command(cmd,message):

    if isRepeat(message,dic,wait_time):
        print "repeated "
        logMessage(message)
        return
    commandNoRepeat(cmd, message)
    return
def logMessage(message):
    #lastMessage = message
    dic[message] = float(time.time())

def commandNoRepeat(cmd, message):
    logMessage(message)
    subprocess.Popen(cmd+" \"%s\""%message, shell=True, stdout=subprocess.PIPE).stdout.read()
    print "LAST MESSAGE ADDING:" + message
    lastMessage.append(message)
    return


def isRepeat(message,history_dic,wait_time):
    message = trim(message)
    #print "about to isrepeat"
    print "dic is:" + str(history_dic) + " message is :" + message
    prev_time = history_dic.get(message,None)
    if prev_time is None:
        print "IS NONE"
        #dic[message] = float(time.time())
        return False
    else:

        cur_time =float(time.time())
        print "curtime is : "+ str(time.time())
        print "prev time is : " + str(prev_time)
        print "dic is :" +str(history_dic)
        if  cur_time-prev_time < wait_time:
            print "curtime is less than prev time:" + str(cur_time)
            #dic[message] = float(time.time())
            repeated = True
            return True
        else:
            print " curtime is not less than prev time, FALSE"
            #dic[message] = float(time.time())
    return False


def send_to_email(message, subject,to_mail):
    pass


def send_message_to_SLACK(message):
    headers =  {'content-type': 'application/json'}
    payload = '{"text":"%s"}'% str("~"+trim(message))
    print "PAYLOAD:" + payload
    url = 'https://hooks.slack.com/services/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'
    r = requests.post(url = url, data = payload, headers= headers)
    print r.status_code
    return

def send_message_to_FB(message, app_user):
    #print "APPuser:" + app_user
    headers = {'content-type': 'application/json' ,'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFwcF81NzkwZDdmZjRlYjRiMzQ0MDAwYWEzMDYifQ.eyJzY29wZSI6ImFwcCJ9.5aks5Q7jvTZ67YR9Km_07GJ46WnDwkRCNSGZePTTU6I'}
    payload = '{"text": "%s", "role": "appMaker"}'
    print "PAYLOAD IS:" + str(payload%message).replace('\n', ',')
    url = 'https://api.smooch.io/v1/appusers/'+ app_user + '/conversation/messages'
    r = requests.post(url = url, data = str(payload%str("~"+message)).replace('\n', ','), headers= headers)
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
