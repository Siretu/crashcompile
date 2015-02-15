<?php
/**
 * Parses the given .ini file and returns a hash-array containing the
 * different values from the .ini file. It is guaranteed that the following
 * keys are defined in the returned array:
 *
 * db_host - The address to the host to the database
 * db_user - The user that will be logged in to in the host
 * db_password - The password to the database for the host and user
 * db_database - The name of the database to be used
 *
 * An exception is thrown if any of the above keys are not specified in the
 * .ini file.
 */
error_reporting(E_ALL);
ini_set('display_errors', 'on');

function db_config() {
	 $ini_file = "config.ini";
	 $db_config = parse_ini_file($ini_file);
	 // $expect is a function which takes a key and checks if it was parsed from
         // the given .ini file. If the key was not defined, the function will
         // throw an exception.
         $expect = function ($key) use ($db_config, $ini_file) {
         	 if (!array_key_exists($key, $db_config)) {
         	    throw new Exception($key . " was not specified in " . $ini_file);
        	 }
	 };
    $expect('db_host');
    $expect('db_user');
    $expect('db_password');
    $expect('db_database');
    // When this line is reached we know that the required keys are defined.
    return $db_config;
}

$foo = db_config();

$db = new mysqli($foo["db_host"],$foo["db_user"],$foo["db_password"],$foo["db_database"]);

if ($db->connect_errno) {
    echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
}

/*//mysqli_query($db, "INSERT INTO user values (default, X'0123456789abcdef0123456789abcdef', 'abc')");

//$db->query("INSERT INTO user values (default, default, default)");
$res = $db->query("SELECT id FROM user");


while ($row = $res->fetch_assoc()) {
    echo " id = " . $row['id'] . "\n";
}

$stmt = $db->prepare("INSERT INTO user values (default, X'0123456789abcdef0123456789abcdea', ?);");
$id = 5;
$stmt->bind_param('i',$id);
$stmt->execute();
$stmt->close();*/
?>