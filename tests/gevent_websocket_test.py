#gevent websocket test
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

class EchoApplication(WebSocketApplication):
    def on_open(self):
        print "Connection opened"

    def on_message(self, message):
        if message is not None:
            message = self.do_ruilanberg(message)
        self.ws.send(message)

    def on_close(self, reason):
        self.ws.send("IAM CLOSING! MOFO! ")
        print "CLOSING BECAUSE I SUCK"
        print reason

    def do_ruilanberg(self,message):
        if "robert" in message :
            return "Robert is awesome sauce! "
        elif "olivert" in message :
            return "Olivert is a kind gentle soul"
        else:
            return message

WebSocketServer(
    ('', 5432),
    Resource({'/': EchoApplication})
).serve_forever()
