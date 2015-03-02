import os
import sys
import json
import MySQLdb
import threading
import uuid
import datetime

from config import *

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket

def log_print(s):
    message = datetime.datetime.now().isoformat(" ") + " " + str(s)
    print message
    with open("server.log","a") as myfile:
        myfile.write(message+"\n")


def save_code(code, uid):
    with open("execution/%s.txt" % uid, "w") as myfile:
        myfile.write(code)


def run_docker(uid):
    os.system("docker run --net none --volume /var/www/crashcompile/execution/%s.txt:/student.py student_test python /student.py >/var/www/crashcompile/execution/results_%s.txt 2>&1" % (uid,uid))
    
def read_result(uid):
    with open("execution/results_%s.txt" % uid) as myfile:
        return myfile.read()

def get_user_info(uid):
    log_print("Got USER ID: " + uid)
    query = "SELECT party.current_problem, problem.nrTests, party.id FROM user INNER JOIN party ON user.party_id = party.id INNER JOIN problem ON party.current_problem = problem.id WHERE user.session_id = X%s"
    log_print(query % uid)
    cur.execute(query,uid)
    result = cur.fetchall()
    log_print("Got result: " + str(result))
    return result

def new_session():
    uid = str(uuid.uuid4()).replace("-","")
    log_print("Creating new session: " + uid)
    query = "INSERT INTO user VALUES (default, X%s, 3, '')"
    log_print("Query: " + query % uid)
    cur.execute(query,uid)
    return uid


class MainHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def check_origin(self, origin):
        return True # Potentially bad? should probably fix at some point

    def on_message(self, message):
        log_print(message)
        js = json.loads(message)
        log_print(js["event"])
        if js["event"] == "run":
            self.run_code(js)
        elif js["event"] == "test":
            self.test_code(js)
        elif js["event"] == "init":
            if not js["id"]:
                js["id"] = new_session()
                self.write_message(json.dumps({"event":"newid","data":js["id"]}))
            self.initProblemDesc(js)

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
        result = get_user_info(js["id"])[0]
        self.run_tests(js,result)
                                                        
        
    def run_tests(self,js,result):
        uid = js["id"]
        problemid = int(result[0])
        nrTests = int(result[1])
        partyid = int(result[2])
        for x in range(1,nrTests+1):
            t = threading.Thread(target=self.test,args=(uid,problemid,partyid,x))
            t.start()
            #self.test(uid,problemid,partyid,x)

    def test(self, uid, problemid, partyid, x):
        log_print("Running test %d-%d" % (problemid,x))
        cmd = "docker run --net none -v /var/www/crashcompile/execution/%s.txt:/student.py -v /var/www/crashcompile/tests/%d/in%d:/test.txt student_test >/var/www/crashcompile/execution/results_%s_%d.txt 2>&1" % (uid,problemid,x,uid,x)
        os.system(cmd)
        cmd2 = "diff /var/www/crashcompile/tests/%d/out%d /var/www/crashcompile/execution/results_%s_%d.txt" % (problemid,x,uid,x)
        diff = os.popen(cmd2)
        output = diff.read()
        log_print("Got diff: " + str(output))
        result = {"event": "testresult","testid":x, "id": uid}
        if not output:
            result["data"] = 1
        else:
            result["data"] = 0
        self.write_message(json.dumps(result))
    

    def initProblemDesc(self,js):
        log_print("initing")
        log_print("Got id: " + str(js["id"]))
        info = get_user_info(js["id"])
        if info:
            result = [int(x) for x in info[0]]
            log_print(result)
            head = content = ""
            with open("/var/www/crashcompile/tests/%d/content.html" % result[0]) as myfile:
                content = myfile.read()
            with open("/var/www/crashcompile/tests/%d/head.html" % result[0]) as myfile:
                head = myfile.read()
            reply = {"event":"problemdesc","id":js["id"],"content":content,"head":head,"tests":result[1]}
            self.write_message(json.dumps(reply))


application = tornado.web.Application([
        (r"/", MainHandler),
])

http_server = tornado.httpserver.HTTPServer(application)

if __name__ == "__main__":
    db = MySQLdb.connect(host=db_host,user=db_user,passwd=db_password,db=db_database)
    db.get_conn().ping(True)
    db.autocommit(True)
    cur = db.cursor()
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
