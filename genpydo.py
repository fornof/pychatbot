import sqlite3
import sys
import io
#genpydo.py
tablename = 'no_tablename_given'
def main():
    tablename = sys.argv[1].title()
    #sys.argv[2]
    conn = sqlite3.connect("data/sqlite_file.db")
    c = conn.cursor()
    c.execute("SELECT * from " + tablename + " limit 1")
    dictionary = c.fetchall()
    names = [description[0] for description in c.description]
    f = open(tablename+"stuff", "w+")
    print f.name
    writer(f,"import sqlite3",0 )
    writer(f,"class " + tablename + "():",0)
    tab = 1
    for name in names:
        char = name.index('_')
        writer(f,"self." +name[char+1:] +"= '' ",tab)
    writer(f,"def __init__(self):",tab)
    tab = 2
    writer(f,"\tpass\n",tab)
    tab = 1
    writer(f,"def parse"+tablename.title() ,tab)
    tab = 2
    print tablename
    writer(f, "passeroonie", tab)
    f.close()
def writer(file,message,tab_count):
    tabs ='    '
    if tab_count > 1:
        tabs = tabs*(tab_count)
    else:
        tabs = ''

    file.write( tabs + message +"\n")


main()
