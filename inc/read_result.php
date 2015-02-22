<?php
$id = $_GET["id"];

$command = 'cat /var/www/crashcompile/execution/results_' . $id . '.txt';

$file = passthru($command);
echo($file);
?>