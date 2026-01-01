// Invoice search and filtering
const invoiceSearchInput = document.getElementById('invoice-search');
if (invoiceSearchInput) {
    invoiceSearchInput.addEventListener('input', function() {
        fetch(`/api/invoices?search=${this.value}`)
            .then(response => response.json())
            .then(data => {
                // Update DOM with filtered invoices
                document.getElementById('invoice-list').innerHTML = data.map(invoice =>
                    `<div>Facture #${invoice.number} - ${invoice.date} - ${invoice.status}</div>`
                ).join('');
            });
    });
}

// Aperçu modal de la facture
const previewBtns = document.querySelectorAll('.preview-invoice-btn');
previewBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        const invoiceId = this.getAttribute('data-id');
        fetch(`/invoices/${invoiceId}?modal=1`)
            .then(response => response.text())
            .then(html => {
                document.getElementById('invoice-preview-body').innerHTML = html;
                const modal = new bootstrap.Modal(document.getElementById('invoicePreviewModal'));
                modal.show();
            });
    });
});
