import sqlite3
class Question():
    conn = ""
    def __init__(self):
        self.conn = sqlite3.connect('data/sqlite_file.db')
        self.dic = {}
        self.id = 0
        self.question = ''
        self.name = ''
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

        if gender =='M':
            where = 'WHERE question_gender = M'
        c.execute('SELECT * FROM question ' + where)
        dictionary = c.fetchall()
        names = [description[0] for description in c.description]
        for j in range(0, len(dictionary)):
            row ={}
            for i in range(0,len(c.description)):
                row[c.description[i][0]] = dictionary[j][i]

            result.append(row)

        self.conn.commit()
        self.conn.close()
        print "RESULT IS :" + str(result[0])
