<?php


date_default_timezone_set("America/New_York");



error_reporting( E_ALL ); 

$enlace = mysqli_connect("127.0.0.1", "root", "", "gtfs");

if (!$enlace) {
    echo "Error: No se pudo conectar a MySQL." . PHP_EOL;
    echo "errno de depuración: " . mysqli_connect_errno() . PHP_EOL;
    echo "error de depuración: " . mysqli_connect_error() . PHP_EOL;
    exit;
}

//echo "host info  " . mysqli_get_host_info($enlace) . PHP_EOL;

$theStopid =  addslashes($_GET['stop_id']);

$sql = "select trip_id, from_unixtime(arrival_time) as arrival_time , from_unixtime(departure_time) as departure_time , stop_id , stop_sequence  from stop_times where stop_id ='".$theStopid."' order by arrival_time";

/*
//echo $sql."<br>";


if ($resultado = $enlace->query($sql)) {

    while ($obj = $resultado->fetch_object()) {
        printf ("%s %s %s %s %s  <br>", $obj->trip_id, $obj->arrival_time,$obj->departure_time, $obj->stop_id,$obj->stop_sequence );
    }

    $resultado->close();
}

 */
	$myArray = array();
	if ($result = $enlace->query($sql)) 
	{
        	$tempArray = array();
		while($row = $result->fetch_object()) 
		{
                	$tempArray = $row;
               		array_push($myArray, $tempArray);
           	 }
        	echo json_encode($myArray);
         }


mysqli_close($enlace);
?>
