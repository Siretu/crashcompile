<?php

include_once('db_config.php');
include_once('uuid.php');

error_reporting(E_ALL);
ini_set('display_errors', 'on');

$id = uuid_version4();
$stmt = "INSERT INTO user values (default, X'$id', 3, '')";

mysqli_query($db,$stmt);

echo $id;

?>