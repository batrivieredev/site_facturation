// Test SMTP/IMAP connection
function testMailConnection() {
    const form = document.getElementById('mail-settings-form');
    const formData = new FormData(form);
    fetch('/settings/test_mail', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.success ? 'Connexion réussie !' : 'Échec de la connexion.');
    })
    .catch(() => alert('Erreur lors du test de connexion.'));
}

document.addEventListener('DOMContentLoaded', function() {
    const testBtn = document.getElementById('test-mail-btn');
    if (testBtn) {
        testBtn.addEventListener('click', function(e) {
            e.preventDefault();
            testMailConnection();
        });
    }
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

    // Attachments upload/delete AJAX
    const uploadForm = document.getElementById('attachment-upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(uploadForm);
            fetch('/settings/upload_attachment', {
                method: 'POST',
                body: formData
            })
            .then(response => window.location.reload())
            .catch(() => alert('Erreur lors de l\'upload.'));
        });
    }
    document.querySelectorAll('#attachment-table form[action="/settings/delete_attachment"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            fetch('/settings/delete_attachment', {
                method: 'POST',
                body: formData
            })
            .then(response => window.location.reload())
            .catch(() => alert('Erreur lors de la suppression.'));
        });
    });
    // Edit mail template modal
    document.querySelectorAll('.edit-mail-template-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const row = btn.closest('tr');
            const id = btn.getAttribute('data-id');
            const name = row.querySelector('td:nth-child(1)').textContent.trim();
            const subject = row.querySelector('td:nth-child(2)').textContent.trim();
            const body = row.querySelector('td:nth-child(3)').textContent.trim();
            document.getElementById('edit-template-id').value = id;
            document.getElementById('edit-template-name').value = name;
            document.getElementById('edit-template-subject').value = subject;
            document.getElementById('edit-template-body').value = body;
            const form = document.getElementById('edit-mail-template-form');
            form.action = `/edit_mail_template/${id}`;
            var modal = new bootstrap.Modal(document.getElementById('editMailTemplateModal'));
            modal.show();
        });
        // Auto-fill mail template and signature with no default selection
        const mailTemplateSelect = document.getElementById('mail-template-select');
        const mailSignatureSelect = document.getElementById('mail-signature-select');
        const mailSubjectInput = document.getElementById('mail-subject');
        const mailBodyTextarea = document.getElementById('mail-body');

        if (mailTemplateSelect && mailSignatureSelect && mailSubjectInput && mailBodyTextarea) {
            mailTemplateSelect.selectedIndex = -1; // No default selection
            mailSignatureSelect.selectedIndex = -1; // No default selection

            mailTemplateSelect.addEventListener('change', function() {
                const selectedTemplate = mailTemplateSelect.options[mailTemplateSelect.selectedIndex];
                mailSubjectInput.value = selectedTemplate.getAttribute('data-subject');
                mailBodyTextarea.value = selectedTemplate.getAttribute('data-body');
            });

            mailSignatureSelect.addEventListener('change', function() {
                const selectedSignature = mailSignatureSelect.options[mailSignatureSelect.selectedIndex];
                mailBodyTextarea.value += '\n\n' + selectedSignature.getAttribute('data-signature');
                // Auto-append mail template and signature text
                const mailTemplateSelect = document.getElementById('mail-template-select');
                const mailSignatureSelect = document.getElementById('mail-signature-select');
                const mailSubjectInput = document.getElementById('mail-subject');
                const mailBodyTextarea = document.getElementById('mail-body');

                if (mailTemplateSelect && mailSignatureSelect && mailSubjectInput && mailBodyTextarea) {
                    mailTemplateSelect.selectedIndex = -1; // No default selection
                    mailSignatureSelect.selectedIndex = -1; // No default selection

                    mailTemplateSelect.addEventListener('change', function() {
                        const selectedTemplate = mailTemplateSelect.options[mailTemplateSelect.selectedIndex];
                        mailSubjectInput.value = selectedTemplate.getAttribute('data-subject');
                        mailBodyTextarea.value += '\n\n' + selectedTemplate.getAttribute('data-body');
                    });

                    mailSignatureSelect.addEventListener('change', function() {
                        const selectedSignature = mailSignatureSelect.options[mailSignatureSelect.selectedIndex];
                        mailBodyTextarea.value += '\n\n' + selectedSignature.getAttribute('data-signature');
                    });
                }
            });
        }
    });
    // Edit mail signature modal
    document.querySelectorAll('.edit-mail-signature-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const row = btn.closest('tr');
            const id = btn.getAttribute('data-id');
            const name = row.querySelector('td:nth-child(1)').textContent.trim();
            const signature = row.querySelector('td:nth-child(2)').textContent.trim();
            document.getElementById('edit-signature-id').value = id;
            document.getElementById('edit-signature-name').value = name;
            document.getElementById('edit-signature-body').value = signature;
            const form = document.getElementById('edit-mail-signature-form');
            form.action = `/edit_mail_signature/${id}`;
            var modal = new bootstrap.Modal(document.getElementById('editMailSignatureModal'));
            modal.show();
        });
    });
    // Auto-fill mail template and signature
    const mailTemplateSelect = document.getElementById('mail-template-select');
    const mailSignatureSelect = document.getElementById('mail-signature-select');
    const mailSubjectInput = document.getElementById('mail-subject');
    const mailBodyTextarea = document.getElementById('mail-body');

    if (mailTemplateSelect && mailSignatureSelect && mailSubjectInput && mailBodyTextarea) {
        mailTemplateSelect.addEventListener('change', function() {
            const selectedTemplate = mailTemplateSelect.options[mailTemplateSelect.selectedIndex];
            mailSubjectInput.value = selectedTemplate.getAttribute('data-subject');
            mailBodyTextarea.value = selectedTemplate.getAttribute('data-body');
        });

        mailSignatureSelect.addEventListener('change', function() {
            const selectedSignature = mailSignatureSelect.options[mailSignatureSelect.selectedIndex];
            mailBodyTextarea.value += '\n\n' + selectedSignature.getAttribute('data-signature');
        });
    }
});
