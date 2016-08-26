import smtplib
import requests
import json, sys
import base64
from kik import KikApi, Configuration
def prompt(prompt):
    return raw_input(prompt).strip()
def main():
    if "setup" in sys.argv:
        setup_kik('http://d14dd9ff.ngrok.io/')
        #kik_setup_python()
        print "setup kik"
    else:
        print "getting settings"
        get_args()


def get_args():

    r= requests.get(
    'https://api.kik.com/v1/config',
    auth=('ratachat','e9dbcaf7-5d17-4ab7-b078-5fbd8a5a244d'))

    #r =  requests.get(
    #'https://api.kik.com/v1/config',
    #auth=('bitfiddle', 'e9dbcaf7-5d17-4ab7-b078-5fbd8a5a244d')
    #)
    data = r.json()
    print data


def setup_kik(webhook):
    print requests.post(
        'https://api.kik.com/v1/config',
        auth=('ratachat', 'e9dbcaf7-5d17-4ab7-b078-5fbd8a5a244d'),
        headers={
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            "webhook": webhook,
            "features": {
                "manuallySendReadReceipts": False,
                "receiveReadReceipts": False,
                "receiveDeliveryReceipts": False,
                "receiveIsTyping": False
            }
        })
    )

def kik_setup_python(webhook):
    BOT_USERNAME = 'ratachat'
    BOT_API_KEY = 'e9dbcaf7-5d17-4ab7-b078-5fbd8a5a244d'
    kik = KikApi(BOT_USERNAME, BOT_API_KEY)
    config = Configuration(webhook=webhook)
    kik.set_configuration(config)
def mailer():
    fromaddr = prompt("From: ")
    toaddrs  = prompt("To: ").split()
    print "Enter message, end with ^D (Unix) or ^Z (Windows):"

    # Add the From: and To: headers at the start!
    msg = ("From: %s\r\nTo: %s\r\n\r\n"
           % (fromaddr, ", ".join(toaddrs)))
    while 1:
        try:
            line = raw_input()
        except EOFError:
            break
        if not line:
            break
        msg = msg + line

    print "Message length is " + repr(len(msg))

    server = smtplib.SMTP('ssrs.reachmail.net')
    server.login('THECOMPA2', 'charlessf')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

main()
