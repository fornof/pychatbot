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
from do.group_question import GroupQuestion
from do.action import Action

reload(sys)
sys.setdefaultencoding('utf-8')
#import future
app = Flask(__name__)
count = 0
dic = {}
command_history= {}
lastMessage = []
wait_time = 20  # amount of time in seconds to wait before reshowing message - used if repeat messages are passed.
wait_time_command = 15
say = "say"
questions = []
group_questions = []
actions = []
cur_question_index = 0
current_question = Question()
current_group = GroupQuestion()
current_action = Action()
name = "Awesome person"
mode = "GAME"
introduction = "Hello there! I am Mr. Mac the talking blue Jay Bee ell speaker.,,, I want to play an icebreaker trivia game with you.,,, If you want to play, please continue to hold onto my speaker.,,,"
introduction2 = "If a question is too difficult for you, or you would prefer to not answer,,, say the keyphrases, PASS QUESTION, or NEXT QUESTION ."
introduction3 = "are you ready to play this fantastic icebreaker trivia game?"

game_introduction = "HELLO and welcome to the Monkey HEAR Monkey Doo game,, I ask questions and you answer by performing an action,,,its kind of like the hokee pokee but a bunch simpler. if you're ready to play, then say , Ready to play!"
@app.route('/' , methods=['GET', 'POST'] )
def index():
    global mode
    #mode= 'GAME'
    if request.method  =='POST':
        #print "printing JSON"
        data = request.get_json()
        if data is None :
            data = request.get_data();
            #result = data.split('&')
            result = urlparse.parse_qs(data)
            text = result['text'][0] #remove first char which is !
            print "RESULT FROM SLACK:" + str(text)
            if mode == 'GAME':
                game_do(text,None)
            else:
                message_do(text, None )
        else:
            message =  data[u'messages'][0][u'text']
            app_user = data[u'appUser'][u'_id']
            print message

            if mode == 'GAME':
                game_do(message, app_user)
            else:
                message_do(message,app_user)
        #POST /v1/appusers/{smoochId|userId}/conversation/messages
        #appUser
        #print "data userid is "
        return "Hello world !"

    return render_template('index.html')
    #return 'Hello World'

# input message like #hello or hello , this trims that first char if special, and returns the message.
def trim(message):
    if len(message) > 1:
        if"#" == message[0] or "!" == message[0]:
            return message[1:]
        else:
            return message
def getNextQuestion():
    global questions
    return questions.pop()

def getNextAction():
    global actions
    if len(actions) ==0 :
        a = Action()
        actions = a.loadAllActions()
    return actions.pop()

def game_do(message, app_user):
    global current_question
    global current_action
    global mode

    msg_len = len(message)
    mes = message
    if " " in message:
        mes = message.split(' ')
        #print mes
        #message =mes[0]
        #args = mes[1]
    if message[0] == '~':
        print "IGNORING"
        return
    if "!" in message[0] :
        print "In exclamation"
        if '!mode' in message:
            if 'game'.lower() in message:
                mode = "GAME"
                print "THE MODE IS NOW GAME! "
            else:
                mode = "CHAT"
        if ('!g' in message.lower() and len(message) <=3 ) or "!group" in message.lower():
            global command_history
            if isRepeat(message,command_history,60):
                print "repeated " + message
                repeated = True
                return
            global group_questions
            print "empty questions!"
            q = GroupQuestion()
            #global dic
            #dic = {}
            group_questions = q.loadAllQuestions()
            actions = current_action.loadAllActions()
            command(say, game_introduction )
            print questions[0].begin
    elif message[0].lower() == "q":
        if isRepeat(message,command_history,7):
            print "repeated command" +message
            return
        #current_question = question.next
        current_group = getNextQuestion()
        current_action = getNextAction()
        commandNoRepeat(say, parseActionifExists(current_group.begin, current_action.begin*2))
    elif message[0].lower() == "a":
        if isRepeat(message,command_history,7):
            print "repeated command" +message
            return
        response = parseActionifExists(current_question.end, current_action.end)
        if msg_len > 1 :
            if message[1].lower() =='a':
                response = parseNameifExists(current_question.all)
                print response, message
        command(say, str(response))
    message_common_do(message, app_user)

def message_do(message, app_user):
    global dic
    global current_question
    global mode
    repeated = False
    msg = str(message)
    banned_words = ["rm","shutdown","restart","sudo","su ", "vi", "vim", "nano", "emacs"]
    message = ' '.join([w for w in msg.split() if w not in banned_words])
    msg_len = len(message)
    args = ''
    mes = ''

    if " " in message:
        mes = message.split(' ')
        #print mes
        #message =mes[0]
        #args = mes[1]
    if message[0] == '~':
        print "IGNORING"
        return
    if message[0] == '!':
        print "exclaimation"
        if '!mode' in message:
            if 'game' in mes[1].lower():
                print "it's a game start mode!"
                mode = "GAME"
            else:
                mode = "CHAT"

        if ('!q' in message.lower() and len(message) <=3 ) or "!start" in message.lower():
            global command_history
            if isRepeat(message,command_history,60):
                print "repeated " + message
                repeated = True
                return
            global questions
            print "empty questions!"
            q = Question()
            #global dic
            #dic = {}
            questions = q.loadAllQuestions(None)
            #current_question = getNextQuestion()
            #command(say, introduction )
            #command(say, introduction2 )
            command(say, introduction3 )
            print "MY QUESTIONS ARE: " + str(questions)
            #command(say , current_question)
            #print "questions are " + str(questions)
            #msg = questions[0]

        if '!question' in message.lower():
            q = Question()
            msg = message.split('|')
            for i in range (1, len(msg)):
                var = msg[i].split['=']
                if var[0].trim() == "text":
                    q.text = var[1]
                if var[0] == "rp":
                    q.response_positive = var[1]



        elif message[0].lower() == "q":
            if isRepeat(message,command_history,4):
                print "repeated command" +message
                return
            #current_question = question.next
            current_question = getNextQuestion()
            print "cur question:" + current_quesition.text()
            commandNoRepeat(say, parseNameifExists(current_question.text))
        elif message[0].lower() == "a":
            if isRepeat(message,command_history,7):
                print "repeated command" +message
                return
            response = parseNameifExists(current_question.response_positive)
            if msg_len > 1 :
                if message[1].lower() =='a':
                    response = parseNameifExists(current_question.response_answer)
                    print response, message
                elif message[1].lower() =='n':
                    response = parseNameifExists(current_question.response_negative)
                elif message[1].lower() =='p':
                    response = parseNameifExists(current_question.response_positive)
            command(say, str(response))
            print "ARGS ARE:" +args
        elif message[0].lower() == "n":
            if msg_len > 2:
                global name
                char = message.index(' ')
                name = message[char:]
                print "name is:" + name

    print "MESSAGE:" + msg
    result = message_common_do(message, app_user)


def message_common_do(message,app_user):
    msg = str(message)
    msg_len = len(message)
    if "#" in message:
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
            #thread.start_new_thread(threadCommand, (message, say) )
        command(say, message)
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

    elif  msg_len > 0:

        if message[0].lower() == 'r':
            if isRepeat(message,command_history,7):
                print "repeated command"
                #return
            if msg_len > 1 :
                if message[1].lower() =='q':
                    commandNoRepeat(say, 'I am sorry but I did not understand. Could you repeat that?')
                    #return
            #repeat last message by pulling it from the dic
            print "Saying last message" + str(lastMessage[-1])
            commandNoRepeat(say, str(lastMessage[-1]))
            #return

    elif message[0].lower() == "g":
        response = "Well, That's all the time I have for today. it was nice to meet you %s, If you have any suggestions on how to make my programming better.\
        please tell Robert when you can. "%name
        if msg_len > 2:
            message[1].lower() == 'g'
            response = "That's all the questions I have. please let me know how my programming can be better"

        command(say, str(response))

    if app_user is None:
        send_message_to_SLACK(msg)
        #subprocess.Popen("python apptalk.py '%s'"%msg, shell=True, stdout=subprocess.PIPE).stdout.read()
    else:
        #subprocess.Popen("python apptalk.py fb %s '%s'"% (app_user,msg), shell=True, stdout=subprocess.PIPE).stdout.read()
        send_message_to_FB(msg,app_user)
    return


def parseActionifExists(message, action):
    try:
        result = message%action
    except:
        result = message
    return result

def parseNameifExists(message):
    global name
    try:
        result = message%name
    except:
        result = message
    return result

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
    lastMessage.append(message)
    subprocess.Popen(cmd+" \"%s\""%message, shell=True, stdout=subprocess.PIPE).stdout.read()

    return


def isRepeat(message,history_dic,wait_time):
    print "history dictionary is:" + str(history_dic)
    message = trim(message)
    #print "about to isrepeat"
    if history_dic is None:
        history_dic = {}
    else:
        #print "dic is:" + str(history_dic) + " message is :" + message
        prev_time = history_dic.get(message,None)
    if prev_time is None:
        #print "IS NONE"
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
    message = trim(message)
    if message is None :
        message = ''
    message = str("~" + message)
    headers =  {'content-type': 'application/json'}
    payload = '{"text":"%s"}'% message
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

def __unicode__(self):
   return unicode(self.some_field) or u''

if __name__ == '__main__' :
    app.run(debug=True, host ='0.0.0.0')
