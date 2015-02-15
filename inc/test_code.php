<?php

include_once('db_config.php');

error_reporting(E_ALL ^ E_NOTICE); ini_set('display_errors', 1); ini_set('display_startup_errors', 1);
$id = $_POST["id"];

$stmt = "SELECT party.current_problem, problem.nrTests FROM user INNER JOIN party ON user.party_id = party.id INNER JOIN problem ON party.current_problem = problem.id WHERE user.session_id = X'$id'";

$result = mysqli_query($db,$stmt);
$row = $result->fetch_array(MYSQLI_BOTH);
echo $row[0];
echo "\r\n";
echo $row[1];
echo "\r\n";

$command = "python ../execution/test_docker.py " . $id . " " . $row[0] . " " . $row[1];
echo $command;
//$output = exec("ls");
$output = exec($command);
echo "\r\n";
echo $output;
?>