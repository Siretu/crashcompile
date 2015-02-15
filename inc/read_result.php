<?php
$file = passthru('cat /var/www/crashcompile/execution/student_results.txt');
echo($file);
?>