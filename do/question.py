import sqlite3
class Question():
    dic = {}
    id = 0
    text = ''
    response_positive =''
    response_negative =''
    response_middle = ''
    response_answer=''
    type = ''
    gender= ''
    next_positive = ''
    next_negative = ''
    next_middle = ''
    def __init__(self):
        print "Added question!"
    def loadSingleQuestion(self ):
        pass
    def loadAllQuestions(self, gender):
        conn  = sqlite3.connect('data/sqlite_file.db')
        c = conn.cursor()
        where = ''
        result = []
        questions = []
        if gender =='M':
            where = 'WHERE question_gender = M '
        where = 'WHERE question_gender != \'F\' and question_type != \'SERIOUS\' '
        c.execute('SELECT * FROM question ' + where + 'ORDER BY question_id desc')
        dictionary = c.fetchall()
        names = [description[0] for description in c.description]
        for j in range(0, len(dictionary)):
            row ={}
            question = Question()
            for i in range(0,len(c.description)):
                row[c.description[i][0]] = dictionary[j][i]

            result.append(row)
            question.parseRowtoQuestion(row)
            questions.append(question)

        conn.commit()
        #conn.close()
        return questions

    # row must have a dictionary key:value pair for each column
    def createQuestion(text, rp, rn, rm, ra, types, gender):
        if text is None :
            return
        if rp is None:
            rp = "Oh okay"
        if rn is None:
            rn = "That's an interesting response"
        if ra is None:
            ra = "I like your question so much I will let Robert answer it"
        if types is None:
            types = "GENERAL"
        if gender is None:
            gender = "N"
        conn  = sqlite3.connect('data/sqlite_file.db')
        c = conn.cursor()
        var = (text,rp,rn,rm,ra,types,gender)
        questions = (len(var)*',?')[1:]
        c.execute("INSERT OR REPLACE INTO question VALUES (%s)"%questions , var)
    
    def parseRowtoQuestion(self, row):
        print row
        self.id= row[u'question_id']
        self.text = row[u'question_text']
        self.response_positive= row[u'question_response_positive']
        self.response_negative= row[u'question_response_negative']
        self.response_middle= row[u'question_response_middle']
        self.response_answer= row[u'question_response_answer']
        self.type= row[u'question_type']
        self.gender= row[u'question_gender']
        self.next_positive= row[u'question_next_positive']
        self.next_negative= row[u'question_next_negative']
        self.next_middle= row[u'question_next_middle']
