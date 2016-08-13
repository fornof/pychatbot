import sqlite3
class Question():
    conn = ""
    def __init__(self):
        #store all the variables from the database into a container so I can call later.
        self.conn = sqlite3.connect('data/sqlite_file.db')
        self.dic = {}
        self.id = 0
        self.text = ''
        self.response_positive =''
        self.response_negative =''
        self.response_middle = ''
        self.response_answer=''
        self.type = ''
        self.gender= ''
        self.next_positive = ''
        self.next_negative = ''
        self.next_middle = ''
    def loadSingleQuestion(self ):
        pass
    def loadAllQuestions(self, gender):
        c = self.conn.cursor()
        where = ''
        result = []
        questions = []
        if gender =='M':
            where = 'WHERE question_gender = M'
        c.execute('SELECT * FROM question ' + where)
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

        self.conn.commit()
        self.conn.close()
        return questions

    # row must have a dictionary key:value pair for each column
    def parseRowtoQuestion(self, row):
        print row
        self.id= row[u'question_id']
        self.text = row[u'question_text']
        self.response_positive= row[u'question_response_positive']
        self.response_negative= row[u'question_response_negative']
        self.response_middle= row[u'question_response_middle']
        self.response_answe= row[u'question_response_answer']
        self.type= row[u'question_type']
        self.gender= row[u'question_gender']
        self.next_positive= row[u'question_next_positive']
        self.next_negative= row[u'question_next_negative']
        self.next_middle= row[u'question_next_middle']
