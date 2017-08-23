# pychatbot
This is a bot built on flask, sqlite, and python 2.7
you will need ngrok to make commands to Facebook (through Smooch.io) and slack. 

1. get ngrok
2. type in:  ngrok http 5000
3. get the forwarding link : http://<your ngrok>.ngrok.io
4. put it into a slack outgoing web hook
5. setup a slack incoming webhook and put that into app.py
6. initialize the database with questions from /data using parser.py to setup a sqlite table. 

demo here:
https://youtu.be/V12Kng7srsE
