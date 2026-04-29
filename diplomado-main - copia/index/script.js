document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registrationForm');
    const birthDateInput = document.getElementById('fecha_nacimiento');
    const ageInput = document.getElementById('edad');
    const messageDiv = document.getElementById('message');
    const tableBody = document.querySelector('#recordsTable tbody');
    const downloadBtn = document.getElementById('downloadCsv');
    const fotoInput = document.getElementById('fotoAlumno');
    const fotoPreview = document.getElementById('fotoPreview');
    const previewContainer = document.getElementById('previewContainer');

    let currentFotoBase64 = "";

    // Cargar tabla desde LocalStorage para persistencia visual en el cliente
    renderTable();

    // --- PROCESAMIENTO DE FOTO ---
    fotoInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) {
            previewContainer.classList.add('hidden');
            currentFotoBase64 = "";
            return;
        }

        if (file.size > 1048576) {
            alert("La imagen excede 1MB. Por favor use una más ligera.");
            fotoInput.value = "";
            previewContainer.classList.add('hidden');
            return;
        }

        const reader = new FileReader();
        reader.onload = (event) => {
            currentFotoBase64 = event.target.result;
            fotoPreview.src = currentFotoBase64;
            previewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    });

    // --- CÁLCULO DE EDAD ---
    birthDateInput.addEventListener('change', () => {
        const birthDate = new Date(birthDateInput.value);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const m = today.getMonth() - birthDate.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        ageInput.value = age;
    });

    // --- ENVÍO DE DATOS AL SERVIDOR ---
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        if (!currentFotoBase64) {
            alert("⚠️ La foto es obligatoria.");
            return;
        }

        const ci = document.getElementById('ci_prefix').value + document.getElementById('cedula').value;
        
        const nuevoAlumno = {
            foto: currentFotoBase64,
            cedula: ci,
            nombres: document.getElementById('nombres').value,
            apellidos: document.getElementById('apellidos').value,
            fechaNacimiento: birthDateInput.value,
            edad: ageInput.value,
            profesion: document.getElementById('profesion').value,
            direccion: document.getElementById('direccion').value,
            correo: document.getElementById('correo').value,
            telefono: document.getElementById('telefono').value,
            monto: document.getElementById('monto').value,
            banco: document.getElementById('banco').value,
            referencia: document.getElementById('referencia').value,
            fechaRegistro: new Date().toLocaleString()
        };

        // Cambiamos la descarga local por una petición al servidor (PHP)
        messageDiv.innerHTML = `<p style="color: blue;">Procesando registro...</p>`;

        fetch('guardar.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(nuevoAlumno)
        })
        .then(response => response.json())
        .then(res => {
            if(res.status === "success") {
                // Guardar localmente solo para mostrar en la tabla actual
                let records = JSON.parse(localStorage.getItem('diplomado_inscritos')) || [];
                records.push(nuevoAlumno);
                localStorage.setItem('diplomado_inscritos', JSON.stringify(records));

                renderTable();
                form.reset();
                previewContainer.classList.add('hidden');
                currentFotoBase64 = "";
                messageDiv.innerHTML = `<p style="color: green; font-weight: bold;">✅ Inscripción guardada en el servidor con éxito.</p>`;
            } else {
                messageDiv.innerHTML = `<p style="color: red;">❌ Error del servidor: ${res.message}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            messageDiv.innerHTML = `<p style="color: red;">❌ Error de conexión. Verifique que 'guardar.php' existe.</p>`;
        });
    });

    function renderTable() {
        const records = JSON.parse(localStorage.getItem('diplomado_inscritos')) || [];
        tableBody.innerHTML = records.map(r => `
            <tr>
                <td><img src="${r.foto}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;"></td>
                <td>${r.cedula}</td>
                <td>${r.nombres} ${r.apellidos}</td>
                <td>${r.correo}</td>
                <td>${r.referencia}</td>
            </tr>
        `).join('');
    }

    // Exportar CSV desde los datos locales
    downloadBtn.addEventListener('click', () => {
        const records = JSON.parse(localStorage.getItem('diplomado_inscritos')) || [];
        if (records.length === 0) return alert("No hay datos");
        const headers = ["Cedula", "Nombres", "Apellidos", "Correo", "Referencia"];
        const rows = records.map(r => [r.cedula, r.nombres, r.apellidos, r.correo, r.referencia].join(","));
        const csvContent = "data:text/csv;charset=utf-8," + headers.join(",") + "\n" + rows.join("\n");
        const link = document.createElement("a");
        link.href = encodeURI(csvContent);
        link.download = "reporte_inscritos.csv";
        link.click();
    });
});