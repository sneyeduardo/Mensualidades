document.addEventListener('DOMContentLoaded', () => {
    const birthDateInput = document.getElementById('fecha_nacimiento');
    const ageInput = document.getElementById('edad');
    const fotoInput = document.getElementById('foto'); 
    const fotoPreview = document.getElementById('fotoPreview');
    const previewContainer = document.getElementById('previewContainer');
    const downloadBtn = document.getElementById('downloadCsv');
    // 4. --- VALIDACIÓN ESTRICTA DE CORREO GMAIL ---
    const correoInput = document.getElementById('correo');
    // 5. --- VALIDACIÓN ESTRICTA DE SOLO NÚMEROS EN TELÉFONO ---
    const telefonoInput = document.getElementById('telefono');
    // Previsualización de la Cédula Documento
const cedulaInput = document.getElementById('cedula_documento');
const cedulaPreview = document.getElementById('cedulaPreview');
const previewCedulaContainer = document.getElementById('previewCedulaContainer');
// Previsualización del Comprobante de Pago
const pagoInput = document.getElementById('comprobante_pago');
const pagoPreview = document.getElementById('pagoPreview');
const previewPagoContainer = document.getElementById('previewPagoContainer');

if (pagoInput) {
    pagoInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                pagoPreview.src = e.target.result;
                previewPagoContainer.classList.remove('hidden');
            }
            reader.readAsDataURL(file);
        }
    });
}
if (cedulaInput) {
    cedulaInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                cedulaPreview.src = e.target.result;
                previewCedulaContainer.classList.remove('hidden');
            }
            reader.readAsDataURL(file);
        }
    });
}
    if (telefonoInput) {
        telefonoInput.addEventListener('input', function() {
            // La expresión regular /[^0-9]/g busca cualquier cosa que NO sea un número
            // y lo reemplaza por un espacio vacío al instante.
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }
    if (correoInput) {
        correoInput.addEventListener('input', function() {
            // Revisa si el campo no está vacío y si NO termina en @gmail.com
            if (this.value !== "" && !this.value.toLowerCase().endsWith('@gmail.com')) {
                // Establece el mensaje de error personalizado
                this.setCustomValidity('Obligatorio: El correo debe terminar en @gmail.com');
            } else {
                // Borra el error si está todo correcto
                this.setCustomValidity('');
            }
        });
    }
    // 1. --- CÁLCULO AUTOMÁTICO DE EDAD (Visual) ---
    if (birthDateInput && ageInput) {
        birthDateInput.addEventListener('change', () => {
            const birthDate = new Date(birthDateInput.value);
            const today = new Date();
            let age = today.getFullYear() - birthDate.getFullYear();
            const m = today.getMonth() - birthDate.getMonth();
            if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
                age--;
            }
            ageInput.value = age; // Muestra la edad en la casilla al instante
        });
    }

    // 2. --- PREVISUALIZAR LA FOTO ANTES DE SUBIRLA ---
    if (fotoInput) {
        fotoInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                // Validación rápida de peso (1MB máximo)
                if (file.size > 1048576) {
                    alert("La imagen excede 1MB. Por favor use una más ligera.");
                    fotoInput.value = "";
                    previewContainer.classList.add('hidden');
                    return;
                }
                const reader = new FileReader();
                reader.onload = function(e) {
                    fotoPreview.src = e.target.result;
                    previewContainer.classList.remove('hidden');
                }
                reader.readAsDataURL(file);
            } else {
                previewContainer.classList.add('hidden');
                fotoPreview.src = "";
            }
        });
    }

    // 3. --- EXPORTAR TABLA A EXCEL (CSV) ---
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            var table = document.getElementById("recordsTable");
            var rows = table.querySelectorAll("tr");
            var csvArray = [];

            for (var i = 0; i < rows.length; i++) {
                var row = [];
                var cols = rows[i].querySelectorAll("td, th");
                
                // Saltamos la columna 0 (la foto) porque Excel no lee imágenes en CSV
                for (var j = 1; j < cols.length; j++) {
                    var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, "").replace(/"/g, '""');
                    row.push('"' + data + '"');
                }
                csvArray.push(row.join(";")); // Separador de Excel en español
            }

            var csvString = csvArray.join("\n");
            var blob = new Blob(["\uFEFF" + csvString], { type: 'text/csv;charset=utf-8;' });
            
            var link = document.createElement("a");
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "Alumnos_Inscritos_Diplomado.csv");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }
});
// --- FUNCIÓN PARA ALTERNAR MÉTODOS DE PAGO ---
function alternarPago() {
    // 1. Capturamos los elementos del DOM
    var metodo = document.getElementById("metodo_pago").value;
    var cajaMovil = document.getElementById("caja_pago_movil");
    var cajaZelle = document.getElementById("caja_zelle");
    var cajaTransf = document.getElementById("caja_transferencia");
    
    var selectBanco = document.getElementById("banco");
    var contenedorBanco = document.getElementById("contenedor_banco");

    // 2. Apagamos todas las cajas de información por defecto
    cajaMovil.style.display = "none";
    cajaZelle.style.display = "none";
    cajaTransf.style.display = "none";

    // 3. Restauramos el select del banco por si estaba bloqueado antes
    selectBanco.style.pointerEvents = "auto";
    selectBanco.style.backgroundColor = "#ffffff";
    contenedorBanco.style.display = "block"; // Aseguramos que se vea

    // 4. Lógica según el método elegido
    if (metodo === "pago_movil") {
        cajaMovil.style.display = "block";
        
    } else if (metodo === "zelle") {
        cajaZelle.style.display = "block";
        // Si no necesitas que llenen banco para Zelle, descomenta la siguiente línea:
        // contenedorBanco.style.display = "none"; 
        
    } else if (metodo === "transferencia") {
        cajaTransf.style.display = "block";
        
        // ¡LA MAGIA DEL BLOQUEO!
        // Forzamos el valor a Banco de Venezuela
        selectBanco.value = "Banco de Venezuela"; 
        
        // Bloqueamos los clics visualmente (sin usar disabled para que Django lo lea)
        selectBanco.style.pointerEvents = "none"; 
        selectBanco.style.backgroundColor = "#e9ecef"; // Color grisáceo de campo inactivo
    }
}

// Ejecutamos la función una vez al cargar la página para que inicie correctamente
window.onload = function() {
    alternarPago();
};