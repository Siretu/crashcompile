import os
import sys
import json
import MySQLdb
from config import *

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
        elif js["event"] == "test":
            self.test_code(js)

    def on_close(self):
        pass

    def run_code(self,js):
        uid = js["id"]
        save_code(js["data"], uid)
        run_docker(uid)
        result = read_result(uid)
        reply = {"event":"result","data":result, "id":uid}
        self.write_message(json.dumps(reply))

    def test_code(self,js):
        save_code(js["data"], js["id"])
        cur.execute("SELECT party.current_problem, problem.nrTests, party.id FROM user INNER JOIN party ON user.party_id = party.id INNER JOIN problem ON party.current_problem = problem.id WHERE user.session_id = X'%s'" % js["id"])
        result = cur.fetchall()[0]
        print result
        self.run_tests(js,result)
        
    def run_tests(self,js,result):
        uid = js["id"]
        problemid = int(result[0])
        nrTests = int(result[1])
        partyid = int(result[2])
        for x in range(1,nrTests+1):
            print "Running test %d-%d" % (problemid,x)
            cmd = "docker run -v /var/www/crashcompile/execution/%s.txt:/student.py -v /var/www/crashcompile/tests/%d/in%d:/test.txt student_test >/var/www/crashcompile/execution/results_%s.txt 2>&1" % (uid,problemid,x,uid)
            os.system(cmd)
            cmd2 = "diff /var/www/crashcompile/tests/%d/out%d /var/www/crashcompile/execution/results_%s.txt" % (problemid,x,uid)
            diff = os.popen(cmd2)
            output = diff.read()
            print "Got diff: " + str(output)
            result = {"event": "testresult","testid":x, "id": uid}
            if not output:
                result["data"] = 1
            else:
                result["data"] = 0
            self.write_message(json.dumps(result))


application = tornado.web.Application([
        (r"/", MainHandler),
])

http_server = tornado.httpserver.HTTPServer(application)

if __name__ == "__main__":
    db = MySQLdb.connect(host=db_host,user=db_user,passwd=db_password,db=db_database)
    cur = db.cursor()
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
