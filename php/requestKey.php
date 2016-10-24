<?php

function generateRandomString($length = 32) {
    // from http://stackoverflow.com/questions/4356289/php-random-string-generator
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

// Request a new session key from the server
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

$saves = glob("../saves/*.xml");

$key = "";

while ($key == "") {
    $tempKey = generateRandomString(32);
    $unique = true;
    foreach($saves as $filename)
    {
        $xml_string = file_get_contents($filename, FILE_TEXT);
        $xml_object = simplexml_load_string($xml_string);
        if ($xml_object != false) {
            if (isset($value['key']))
            {
                if ($value['key'] == $key_requested) {
                    $unique = false;
                }
            }
        }
    }
    if ($unique) {
        $key = $tempKey;
    }
}

$filename = "saves/save-".$key.".xml"
$fileHandle = fopen($filename, 'w');
if ($fileHandle == FALSE) {
    echo "<response><state>ERROR</state><key>".$key."</key></response>";
    return;
}
fclose($fileHandle);
// TODO:
//  Generate the XML Base file and save it
$doc_struct = new SimpleXMLElement('<waetresult/>');
$doc_struct->addAttribute("key",$key);
//  Add start time
//  Add IP Address information
//  Save the file
$doc_struct->asXML($filename);
echo "<response><state>OK</state><key>".$key."</key></response>";
return;
?>
