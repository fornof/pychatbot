from flask import Flask, render_template,request
import requests
import json
import subprocess
import urlparse
import os
import sys
import sqlite3
import re
import zlib
def main():
    print str(len(sys.argv)) + ":" + str(sys.argv)
    if "fb" in sys.argv:
        #f = open(sys.argv[2])
        #for line in f:
    #        line = re.sub('[\n]', '', line)
    #        line = line.split(' ')
    #        add_stuff_to_SQLITE(line[1],line[0])
        send_message_to_FB(sys.argv[2], sys.argv[3])
        #get_emoticon(sys.argv[2])
        #add_stuff_to_SQLITE()
    else:
        send_message_to_SLACK(sys.argv[1])

def send_message_to_FB(message, app_user):
    #print "APPuser:" + app_user
    headers = {'content-type': 'application/json' ,'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFwcF81NzkwZDdmZjRlYjRiMzQ0MDAwYWEzMDYifQ.eyJzY29wZSI6ImFwcCJ9.5aks5Q7jvTZ67YR9Km_07GJ46WnDwkRCNSGZePTTU6I'}
    payload = '{"text": "%s", "role": "appMaker"}'
    print "PAYLOAD IS:" + str(payload%message).replace('\n', ',')
    url = 'https://api.smooch.io/v1/appusers/'+ app_user + '/conversation/messages'
    r = requests.post(url = url, data = str(payload%message).replace('\n', ','), headers= headers)
    print r.status_code

def send_message_to_SLACK(message):
    headers =  {'content-type': 'application/json'}
    payload = '{"text":"%s"}'% message
    print "PAYLOAD:" + payload
    url = 'https://hooks.slack.com/services/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'
    r = requests.post(url = url, data = payload, headers= headers)
    print r.status_code
    return
def get_emoticon(key):
    conn = sqlite3.connect('sqlite_file.db')
    c = conn.cursor()
    params = (unicode(key, "utf-8"),)
    c.execute("SELECT value FROM lookup WHERE key=?", params)
    all_rows = c.fetchone()
    print all_rows[0]
def add_stuff_to_SQLITE(key, value):
    conn = sqlite3.connect('sqlite_file.db')
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
main()
