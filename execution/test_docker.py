import sys
import os

id = sys.argv[1]
problemid = int(sys.argv[2])
nrTests = int(sys.argv[3])
partyid = int(sys.argv[4])

#f = open("../execution/unique","w")
#f.write(str(sys.argv))
#f.close()

result = ""
for x in range(1,nrTests+1):
    #print "Running test %d-%d" % (problemid,x)
    os.system("docker run -v /var/www/crashcompile/execution/%s.txt:/student.py -v /var/www/crashcompile/tests/%d/in%d:/test.txt student_test >/var/www/crashcompile/execution/results_%s.txt 2>&1" % (id,problemid,x,id))
    diff = os.popen("diff /var/www/crashcompile/tests/%d/out%d /var/www/crashcompile/execution/results_%s.txt" % (problemid,x,id))
    output = diff.read()
    message = "T#%s#%d#" % (id,x)
    if not output:
        result += "1"
        message += "S\n"
    else:
        #print output
        result += "0"
        message += "F\n"
    with open("/var/www/crashcompile/parties/%d" % partyid,"a") as myfile:
        myfile.write(message)

print result
