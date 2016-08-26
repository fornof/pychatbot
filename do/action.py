import sqlite3
class Action():
    id= ''
    begin= ''
    end= ''
    def __init__(self):
        pass
    def loadAllActions(self):
        conn  = sqlite3.connect('data/sqlite_file.db')
        c = conn.cursor()
        where = ''
        result = []
        actions = []
        c.execute('SELECT * FROM action ' + where + 'ORDER BY act_id desc')
        dictionary = c.fetchall()
        names = [description[0] for description in c.description]
        for j in range(0, len(dictionary)):
            row ={}
            action = Action()
            for i in range(0,len(c.description)):
                row[c.description[i][0]] = dictionary[j][i]

            result.append(row)
            action.parseRowtoAction(row)
            actions.append(action)

        conn.commit()
        #conn.close()
        return actions

    def parseRowtoAction(self,row):
        self.id= row[u'act_id']
        self.begin= row[u'act_begin']
        self.end= row[u'act_end']
