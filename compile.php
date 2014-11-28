<?php
$r = file_put_contents("execution/input.txt", $_POST["contents"]) or die("can't open file");

$output = exec('execution/run_docker.sh');
?>