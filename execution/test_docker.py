import sys
import os

id = sys.argv[1]
testid = int(sys.argv[2])
nrTests = int(sys.argv[3])

f = open("../execution/unique","w")
f.write(str(sys.argv))
f.close()

result = ""
for x in range(1,nrTests+1):
    print "Running test %d-%d" % (testid,x)
    os.system("docker run -v /var/www/crashcompile/execution/%s.txt:/student.py -v /var/www/crashcompile/tests/%d/in%d:/test.txt student_test >/var/www/crashcompile/execution/results_%s.txt 2>&1" % (id,testid,x,id))
    diff = os.popen("diff /var/www/crashcompile/tests/%d/out%d /var/www/crashcompile/execution/results_%s.txt" % (testid,x,id))
    output = diff.read()
    if not output:
        result += "1"
    else:
        result += "0"

print result
