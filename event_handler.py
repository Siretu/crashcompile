import os
import sys
import json

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket

def save_code(code, uid):
    with open("execution/%s.txt" % uid, "w") as myfile:
        myfile.write(code)


def run_docker(uid):
    os.system("docker run --volume /var/www/crashcompile/execution/%s.txt:/student.py student_test python /student.py >/var/www/crashcompile/execution/results_%s.txt 2>&1" % (uid,uid))
    
def read_result(uid):
    with open("execution/results_%s.txt" % uid) as myfile:
        return myfile.read()


class MainHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        message = {"event":"result","data":"This is the result"}
        self.write_message(json.dumps(message))

    def check_origin(self, origin):
        return True # Potentially bad? should probably fix at some point

    def on_message(self, message):
        print message
        js = json.loads(message)
        print js["event"]
        if js["event"] == "run":
            self.run_code(js)

    def on_close(self):
        pass

    def run_code(js):
        save_code(js["data"], js["id"])
        run_code(js["id"])
        result = read_result(js["id"])
        reply = {"event":"result","data":result}
        self.write_message(json.dumps(reply))



application = tornado.web.Application([
        (r"/", MainHandler),
])

http_server = tornado.httpserver.HTTPServer(application)

if __name__ == "__main__":
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
