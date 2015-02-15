<?php
error_reporting(E_ALL ^ E_NOTICE); ini_set('display_errors', 1); ini_set('display_startup_errors', 1);
$name = "../execution/" . $_POST["id"] . ".txt";
echo $name;
echo "\r\n";
$r = file_put_contents($name, $_POST["contents"]) or die("can't open file");
?>