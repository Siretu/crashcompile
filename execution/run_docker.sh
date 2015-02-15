#rm /var/wwwstudent_results.txt
docker run --volume /var/www/crashcompile/execution/$1.txt:/student.py student_test python /student.py >/var/www/crashcompile/execution/student_results.txt 2>&1