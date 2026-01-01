// Instant client search
const searchInput = document.getElementById('search-client');
const clientTable = document.getElementById('client-table');
if(searchInput && clientTable) {
    searchInput.addEventListener('input', function() {
        const val = searchInput.value.toLowerCase();
        for(const row of clientTable.tBodies[0].rows) {
            const nom = row.cells[0].textContent.toLowerCase();
            const prenom = row.cells[1].textContent.toLowerCase();
            row.style.display = nom.includes(val) || prenom.includes(val) ? '' : 'none';
        }
    });
}

// Gestion des boutons modifier et voir
const editButtons = document.querySelectorAll('.edit-client-btn');
const viewButtons = document.querySelectorAll('.view-client-btn');
const clientModalEl = document.getElementById('clientModal');
const clientModal = clientModalEl ? new bootstrap.Modal(clientModalEl) : null;

editButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        const row = btn.closest('tr');
        document.getElementById('client-last-name').value = row.cells[0].textContent.trim();
        document.getElementById('client-first-name').value = row.cells[1].textContent.trim();
        document.getElementById('client-email').value = row.cells[2].textContent.trim();
        document.getElementById('client-phone').value = row.cells[3].textContent.trim();
        document.getElementById('client-address').value = row.cells[6].textContent.trim();
        document.getElementById('client-rdv-status').value = row.cells[4].textContent.trim();
        document.getElementById('client-rdv-type').value = row.cells[5].textContent.trim();
        document.getElementById('client-form').action = `/clients/edit/${btn.getAttribute('data-id')}`;
        if(clientModal) clientModal.show();
    });
});

viewButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        const row = btn.closest('tr');
        document.getElementById('client-last-name').value = row.cells[0].textContent.trim();
        document.getElementById('client-first-name').value = row.cells[1].textContent.trim();
        document.getElementById('client-email').value = row.cells[2].textContent.trim();
        document.getElementById('client-phone').value = row.cells[3].textContent.trim();
        document.getElementById('client-address').value = row.cells[6].textContent.trim();
        document.getElementById('client-rdv-status').value = row.cells[4].textContent.trim();
        document.getElementById('client-rdv-type').value = row.cells[5].textContent.trim();
        document.getElementById('client-form').action = '#';
        if(clientModal) clientModal.show();
    });
});
