import sys
import subprocess
import sqlite3
import xlrd
import xlwt
import sys
import time
#reload(sys)
#sys.setdefaultencoding('utf-8')
from do.question import Question
def main():
    filename = "output.xlsx"
    try:
        filename = sys.argv[1]
    except Exception:
        #filename = "output.xlsx"
        pass

    tables_to_excel(filename)
def tables_to_excel(filename):
    conn  = sqlite3.connect('data/sqlite_file.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'");
    tables = c.fetchall()
    workbook = xlwt.Workbook()
    for table in tables:
        table_to_excel(table,workbook)

    workbook.save(filename)
    print "workbook saved to" + filename
    conn.close()


def table_to_excel(tablename,workbook):
    tablename = str(tablename[0])
    conn  = sqlite3.connect('data/sqlite_file.db')
    c = conn.cursor()
    #where = ''
    #result = []
    #questions = []
    #if gender =='M':
    #    where = 'WHERE question_gender = M '
    #where = 'WHERE question_gender != \'F\' and question_type != \'SERIOUS\' '
    c.execute('SELECT * FROM ' + tablename )
    dictionary = c.fetchall()
    names = [description[0] for description in c.description]
    for j in range(0, len(dictionary)):
        row ={}
        #question = Question()
        for i in range(0,len(c.description)):
            row[c.description[i][0]] = dictionary[j][i]


    #data = [sheet.cell_value(0, col) for col in range(sheet.ncols)]

    sheet = workbook.add_sheet(tablename,cell_overwrite_ok=True)
    #write headers
    i = 0
    for header in names:
        if "_id" in header:
            header = header + " " +"INTEGER PRIMARY KEY "
        elif "_date" in header:
            header = header + " " + "INTEGER"
        else:
            header = header +" "+ "TEXT"
        sheet.write(0, i ,header)
        i += 1

    r = 1
    i = 0
    for row in dictionary:
        c = 0
        for item in row:
            if type(item) == type(0):
                sheet.write(r,c, item)
            elif type(item) == type(""):
                sheet.write(r,c, item)
            else:
                #print (type(item))
                sheet.write(r,c,item)
            c +=1

        r += 1
    #    c = 0
    #    for i in tuple:
    #        sheet.write(r,c, "blah")
    #        c += 1
    #    r += 1

    conn.close()


main()
