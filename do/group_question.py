import sqlite3
class GroupQuestion():
    id= ''
    begin= ''
    end= ''
    all= ''
    none= ''
    single= ''
    def __init__(self):
        pass
    def loadAllQuestions(self):
        conn  = sqlite3.connect('data/sqlite_file.db')
        c = conn.cursor()
        where = ''
        result = []
        questions = []
        c.execute('SELECT * FROM gr_questions ' + where + 'ORDER BY gr_id desc')
        dictionary = c.fetchall()
        names = [description[0] for description in c.description]
        for j in range(0, len(dictionary)):
            row ={}
            question = GroupQuestion()
            for i in range(0,len(c.description)):
                row[c.description[i][0]] = dictionary[j][i]

            result.append(row)
            question.parseRowtoQuestion(row)
            questions.append(question)

        conn.commit()
        #conn.close()
        return questions
    def parseRowtoQuestion(self,row):
        self.id= row[u'gr_id']
        self.begin= row[u'gr_begin']
        self.end= row[u'gr_end']
        self.all= row[u'gr_all']
        self.none= row[u'gr_none']
        self.single= row[u'gr_single']
