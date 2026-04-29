<?php
// Recibir los datos enviados por el JavaScript
$data = json_decode(file_get_contents('php://input'), true);

if ($data) {
    $cedula = $data['cedula'];
    
    // Crear carpeta 'registros' si no existe
    if (!file_exists('registros')) {
        mkdir('registros', 0777, true);
    }

    // 1. Guardar JSON
    $jsonFile = "registros/registro_" . $cedula . ".json";
    file_put_contents($jsonFile, json_encode($data, JSON_PRETTY_PRINT));

    // 2. Guardar TXT
    $txtFile = "registros/registro_" . $cedula . ".txt";
    $contenidoTxt = "INSCRIPCIÓN IA GENERATIVA\n";
    $contenidoTxt .= "Fecha: " . $data['fechaRegistro'] . "\n";
    $contenidoTxt .= "Cédula: " . $data['cedula'] . "\n";
    $contenidoTxt .= "Nombre: " . $data['nombres'] . " " . $data['apellidos'] . "\n";
    $contenidoTxt .= "Correo: " . $data['correo'] . "\n";
    $contenidoTxt .= "Referencia: " . $data['referencia'] . "\n";
    
    file_put_contents($txtFile, $contenidoTxt);

    echo json_encode(["status" => "success", "message" => "Archivos guardados en el servidor"]);
} else {
    echo json_encode(["status" => "error", "message" => "No se recibieron datos"]);
}
?>