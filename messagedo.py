from do.question import Question
from do.group_question import GroupQuestion
from do.action import Action
from do.settings import Settings
def main():
    print "hello from main"
    MessageDo.message_do("!q", None)

class MessageDo():
    count = 0 # comment out .
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
    mode = "CHAT"
    introduction = "Hello there! I am Mr. Mac the talking blue Jay Bee ell speaker.,,, I want to play an icebreaker trivia game with you.,,, If you want to play, please continue to hold onto my speaker.,,,"
    introduction2 = "I really like people who use apple products. They are cool."
    introduction3 = "Anyways, Would you like me to ask you some questions?"

    game_introduction = "HELLO and welcome to the Monkey HEAR Monkey Doo game,, I ask questions and you answer by performing an action,,,its kind of like the hokee pokee but a bunch simpler. if you're ready to play, then say , Ready to play!"
    @staticmethod
    def trim(message):
        if len(message) > 1:
            if"#" == message[0] or "!" == message[0]:
                return message[1:]
            else:
                return message
    @staticmethod
    def getNextQuestion():
        global questions
        return questions.pop()
    @staticmethod
    def getNextGroupQuestion():
        global group_questions
        return group_questions.pop()
    @staticmethod
    def getNextAction():
        global actions
        if len(actions) ==0 :
            a = Action()
            actions = a.loadAllActions()
        return actions.pop()
    @staticmethod
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
                if MessageDo.isRepeat(message,MessageDo.command_history,60):
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
                MessageDo.command(MessageDo.say, game_introduction )
                print questions[0].begin
        elif message[0].lower() == "q":
            if MessageDo.isRepeat(message,MessageDo.command_history,7):
                print "repeated MessageDo.command" +message
                return
            #current_question = question.next
            current_group = MessageDo.getNextGroupQuestion()
            current_action = MessageDo.getNextAction()
            MessageDo.commandNoRepeat(MessageDo.say, MessageDo.parseActionifExists(current_group.begin, current_action.begin*2))
        elif message[0].lower() == "a":
            if MessageDo.isRepeat(message,MessageDo.command_history,7):
                print "repeated MessageDo.command" +message
                return
            response = MessageDo.parseActionifExists(current_question.end, current_action.end)
            if msg_len > 1 :
                if message[1].lower() =='a':
                    response = MessageDo.parseNameifExists(current_question.all)
                    print response, message
            MessageDo.command(MessageDo.say, str(response))
        MessageDo.message_common_do(message, app_user)


    @staticmethod
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
            print "exclamation"
            if '!mode' in message:
                if 'game' in mes[1].lower():
                    print "it's a game start mode!"
                    mode = "GAME"
                else:
                    mode = "CHAT"

            if ('!q' in message.lower() and len(message) <=3 ) or "!start" in message.lower():
                global command_history
                if MessageDo.isRepeat(message,MessageDo.command_history,60):
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
                MessageDo.command(MessageDo.say, introduction )
                MessageDo.command(MessageDo.say, introduction2 )
                MessageDo.command(MessageDo.say, introduction3 )
                print "MY QUESTIONS ARE: " + str(questions)
                #MessageDo.command(say , current_question)
                #print "questions are " + str(questions)
                #msg = questions[0]

            if '!question' in message.lower():
                q = Question()
                msg = message.split('|')
                for i in range (1, len(msg)):
                    var = msg[i].split['=']
                    if var[0].MessageDo.trim() == "text":
                        q.text = var[1]
                    if var[0] == "rp":
                        q.response_positive = var[1]

        elif message[0].lower() == "q":
            if MessageDo.isRepeat(message,MessageDo.command_history,4):
                print "repeated MessageDo.command" +message
                return
            #current_question = question.next
            current_question = MessageDo.getNextQuestion()
            #print "cur question:" + current_question.text()
            MessageDo.commandNoRepeat(MessageDo.say, MessageDo.parseNameifExists(current_question.text))
        elif message[0].lower() == "a":
            if MessageDo.isRepeat(message,MessageDo.command_history,7):
                print "repeated MessageDo.command" +message
                return
            response = MessageDo.parseNameifExists(current_question.response_positive)
            if msg_len > 1 :
                if message[1].lower() =='a':
                    response = MessageDo.parseNameifExists(current_question.response_answer)
                    print response, message
                elif message[1].lower() =='n':
                    response = MessageDo.parseNameifExists(current_question.response_negative)
                elif message[1].lower() =='p':
                    response = MessageDo.parseNameifExists(current_question.response_positive)
            MessageDo.command(MessageDo.say, str(response))
            print "ARGS ARE:" +args
        elif message[0].lower() == "n":
            if msg_len > 2:
                global name
                char = message.index(' ')
                name = message[char:]
                print "name is:" + name

        print "MESSAGE:" + msg
        #result = MessageDo.message_common_do(message, app_user)

    @staticmethod
    def message_common_do(message,app_user):
        msg = str(message)
        msg_len = len(message)
        if "#" in message:
            if MessageDo.isRepeat(message,dic,wait_time):
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
            #    MessageDo.commandNoRepeat("MessageDo.say -v Agnes", message)
            #else:
                #thread.start_new_thread(threadMessageDo.Command, (message, MessageDo.say) )
            MessageDo.command(MessageDo.say, message)
        elif "/" in message:
            if "rm" in message:
                msg = "ooopsies!"
            elif "shutdown" in message:
                msg = "ooopsies!"
            else:
                char = message.index('/')
                #msg= os.system(message[char:])
                message = message[(char+1):]
                #thread.start_new_thread(threadMessageDo.Command, (message, "echo") )
                msg = subprocess.Popen("echo $(%s)"%message[(char+1):], shell=True, stdout=subprocess.PIPE).stdout.read()

        elif  msg_len > 0:

            if message[0].lower() == 'r':
                if MessageDo.isRepeat(message,MessageDo.command_history,7):
                    print "repeated MessageDo.command"
                    #return
                if msg_len > 1 :
                    if message[1].lower() =='q':
                        MessageDo.commandNoRepeat(MessageDo.say, 'I am sorry but I did not understand. Could you repeat that?')
                        #return
                #repeat last message by pulling it from the dic
                print "Saying last message" + str(lastMessage[-1])
                MessageDo.commandNoRepeat(MessageDo.say, str(lastMessage[-1]))
                #return

            elif message[0].lower() == "g":
                response = "Well, That's all the time I have for today. it was nice to meet you %s, If you have any suggestions on how to make my programming better.\
                please tell Robert when you can. "%name
                if msg_len > 2:
                    message[1].lower() == 'g'
                    response = "That's all the questions I have. please let me know how my programming can be better"

                MessageDo.command(MessageDo.say, str(response))

        if app_user is None:
            send_message_to_SLACK(msg)
            #subprocess.Popen("python apptalk.py '%s'"%msg, shell=True, stdout=subprocess.PIPE).stdout.read()
        else:
            #subprocess.Popen("python apptalk.py fb %s '%s'"% (app_user,msg), shell=True, stdout=subprocess.PIPE).stdout.read()
            send_message_to_FB(msg,app_user)
        return

    @staticmethod
    def parseActionifExists(message, action):
        try:
            result = message%action
        except:
            result = message
        return result


    @staticmethod
    def parseNameifExists(message):
        global name
        try:
            result = message%name
        except:
            result = message
        return result
    @staticmethod
    def command(cmd,message):

        if MessageDo.isRepeat(message,dic,wait_time):
            print "repeated "
            MessageDo.logMessage(message)
            return
        MessageDo.commandNoRepeat(cmd, message)
        return
    @staticmethod
    def logMessage(message):
        #lastMessage = message
        dic[message] = float(time.time())

    @staticmethod
    def commandNoRepeat(cmd, message):
        MessageDo.logMessage(message)
        lastMessage.append(message)
        subprocess.Popen(cmd+" \"%s\""%message, shell=True, stdout=subprocess.PIPE).stdout.read()

        return

    @staticmethod
    def isRepeat(message,history_dic,wait_time):
        print "history dictionary is:" + str(history_dic)
        message = MessageDo.trim(message)
        #print "about to MessageDo.isrepeat"
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
main()
