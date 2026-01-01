// Refresh next appointment every 2 minutes
setInterval(function() {
    fetch('/api/next_appointment')
        .then(response => response.json())
        .then(data => {
            // Update DOM with next appointment info
            document.getElementById('next-appointment').innerHTML =
                `<strong>Prochain RDV :</strong><br>Date : ${data.date}<br>Heure : ${data.time}<br>Type : ${data.type}<br>Client : ${data.client}`;
        });
}, 120000);
