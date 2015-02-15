<?php

include_once('db_config.php');

$id = $_GET["id"];
$stmt = "SELECT problem.nrTests FROM problem INNER JOIN party ON party.current_problem = problem.id INNER JOIN user ON user.party_id = party.id WHERE user.session_id = X'$id'";
$result = mysqli_query($db,$stmt);

if (!$result) {
    die('Could not query:' . mysql_error());
}

$row = $result->fetch_array(MYSQLI_BOTH);
//var_dump($row);
echo $row[0];

?>