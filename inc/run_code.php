<?php
error_reporting(E_ALL ^ E_NOTICE); ini_set('display_errors', 1); ini_set('display_startup_errors', 1);

$command = "../execution/run_docker.sh " . $_POST["id"];
echo $command;
$output = exec($command);
?>