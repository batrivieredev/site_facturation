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
