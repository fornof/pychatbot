import sys
import subprocess
import sqlite3
import xlrd
import xlwt
from do.question import Question

conn = sqlite3.connect('data/sqlite_file.db')

def main():
    parseQuestions(sys.argv[1])
    #q = Question()
    #questions = q.loadAllQuestions(None)
    #print "questions are " + str(questions)

def parseQuestions(file):
    content =""

    print "FILE IS : " + file
    book=xlrd.open_workbook(filename=file, logfile=None ,verbosity=0, use_mmap=1, file_contents=None, encoding_override=None, formatting_info=False, on_demand=False, ragged_rows=False)
    sheets = book.sheets()


    #tablename = 'question'
    #rows= book.sheet_by_name('question').get_rows(
    for sheet in sheets:
        sheet_table_maker(sheet)
    #sheet = book.sheet_by_name(tablename)
    #book = open_workbook('forum.xlsx')
    #sheet = book.sheet_by_index(3)

    # read header values into the list


def sheet_table_maker(sheet):
    print "SHEET IS :" + sheet.name
    tablename = str(sheet.name)
    drop_db(conn, tablename)

    full_keys = [sheet.cell(0, col_index).value for col_index in xrange(sheet.ncols)]
    keys = [sheet.cell(0, col_index).value.split(' ', 1)[0] for col_index in xrange(sheet.ncols)]
    dict_list = []
    key_str = ','.join(full_keys)
    initialize_db(conn, tablename, key_str)

    for row_index in xrange(1, sheet.nrows):
        d = {keys[col_index]: sheet.cell(row_index, col_index).value
            for col_index in xrange(sheet.ncols)}
        dict_list.append(d)

    print dict_list
    for row in dict_list:
        post_row(conn, tablename, row)
    #for word in dict_list[0].items():
    #    print word[0],word[1]



    #post_row(conn,tablename, dict_list )
    #with open(file, 'rb') as csvfile:
    #    reader = csv.DictReader(csvfile)
    #    for row in reader:
    #        post_row(,) row

    #for row in reader:
    #    words = row.split(',')
    #    print ', '.join(row)
        #command("say", row)
    #    i += 1
def question_exists(conn,tablename, column, arg):
    if type(arg) is str:
        arg = "'%s'",arg
    elif type(arg) is int:
        arg = str(arg)
    return conn.execute('SELECT * FROM '+tablename + 'WHERE ' + column + '=' + arg )

def post_row(conn, tablename, rec):
    keys = ','.join(rec.keys())
    question_marks = ','.join(list('?'*len(rec)))
    values = tuple(rec.values())
    conn.execute('INSERT INTO '+tablename+' ('+keys+') VALUES ('+question_marks+')', values)
    print "added" +str(rec)
    conn.commit()

def drop_db(conn, tablename ):
    # grab the type
    conn.execute('DROP TABLE IF EXISTS ' +tablename)
    print "Dropped table"
    conn.commit()

def initialize_db(conn, tablename, key_str ):
    # grab the type
    conn.execute('CREATE TABLE IF NOT EXISTS ' +tablename +'(' + key_str + ')')
    print "CREATED TABLE"
    conn.commit()

def add_stuff_to_SQLITE(key, value):
    conn = sqlite3.connect('data/sqlite_file.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lookup(key text UNIQUE NOT NULL, value text NOT NULL)''')
    try:
        var = (unicode(key, "utf-8"), unicode(value, "utf-8"))
        c.execute("INSERT INTO lookup VALUES (?,?)", (var))
    except sqlite3.IntegrityError:
        print "already exists, updating"
        c.execute("UPDATE OR ABORT lookup SET value = ? where key = ?", (var))
    conn.commit()
    conn.close()


def command(cmd, message, args):

    subprocess.Popen(cmd+" \"%s\""%message +" " +args, shell=True, stdout=subprocess.PIPE).stdout.read()
    return



main()
