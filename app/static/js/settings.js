// Test SMTP/IMAP connection placeholder
function testMailConnection() {
    // Implement AJAX call to backend for mail connection test
    console.log('Testing mail connection...');
}

document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.edit-rdv-type-btn');
    editButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const row = btn.closest('tr');
            const id = btn.getAttribute('data-id');
            const name = row.querySelector('td:nth-child(1)').textContent.trim();
            const description = row.querySelector('td:nth-child(2)').textContent.trim();
            const price = row.querySelector('td:nth-child(3)').textContent.trim().replace(' €','');
            document.getElementById('edit-type-id').value = id;
            document.getElementById('edit-type-name').value = name;
            document.getElementById('edit-type-description').value = description;
            document.getElementById('edit-type-price').value = price;
            const form = document.getElementById('edit-rdv-type-form');
            form.action = `/settings/edit_appointment_type/${id}`;
            var modal = new bootstrap.Modal(document.getElementById('editRdvTypeModal'));
            modal.show();
        });
    });
});
