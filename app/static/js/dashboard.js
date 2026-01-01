// Refresh CA (revenue) stats every 10 seconds
setInterval(function() {
    fetch('/api/dashboard_stats')
        .then(response => response.json())
        .then(stats => {
            document.getElementById('ca-day').textContent = stats.day.toFixed(2);
            document.getElementById('ca-week').textContent = stats.week.toFixed(2);
            document.getElementById('ca-month').textContent = stats.month.toFixed(2);
            document.getElementById('ca-year').textContent = stats.year.toFixed(2);
        });
}, 10000);

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
