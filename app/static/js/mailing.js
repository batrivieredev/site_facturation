// Mailing filters and history placeholder
function filterMailing(status, type) {
    // Implement AJAX filter and DOM update
    console.log('Filtering mailing:', status, type);
}

// Recherche instantanée dans la modale de mailing
const searchModalInput = document.getElementById('search-modal-client');
const recipientsSelect = document.getElementById('mail-recipients');
if (searchModalInput && recipientsSelect) {
    searchModalInput.addEventListener('input', function() {
        const val = searchModalInput.value.toLowerCase();
        for (const option of recipientsSelect.options) {
            const text = option.textContent.toLowerCase();
            option.style.display = text.includes(val) ? '' : 'none';
        }
    });
}

// Sélection/désélection par clic sur le nom (amélioration UX)
if (recipientsSelect) {
    for (const option of recipientsSelect.options) {
        option.addEventListener('mousedown', function(e) {
            e.preventDefault();
            option.selected = !option.selected;
            return false;
        });
    }
}

// Autofill subject and body when selecting mail type or signature
const mailTemplateSelect = document.getElementById('mail-template');
const mailSignatureSelect = document.getElementById('mail-signature');
const mailSubjectInput = document.getElementById('mail-subject');
const mailBodyTextarea = document.getElementById('mail-body');

// Store template data for quick lookup
let templateData = {};
if (mailTemplateSelect) {
    for (const option of mailTemplateSelect.options) {
        if (option.value) {
            templateData[option.value] = {
                subject: option.getAttribute('data-subject') || '',
                body: option.getAttribute('data-body') || ''
            };
        }
    }
}
// Store signature data for quick lookup
let signatureData = {};
if (mailSignatureSelect) {
    for (const option of mailSignatureSelect.options) {
        if (option.value) {
            signatureData[option.value] = option.getAttribute('data-signature') || '';
        }
    }
}

function updateMailFieldsFromTemplate() {
    const selected = mailTemplateSelect.value;
    if (selected && templateData[selected]) {
        if (mailSubjectInput) mailSubjectInput.value = templateData[selected].subject;
        if (mailBodyTextarea) {
            let signature = '';
            const sigSelected = mailSignatureSelect && mailSignatureSelect.value;
            if (sigSelected && signatureData[sigSelected]) {
                signature = '\n' + signatureData[sigSelected];
            }
            mailBodyTextarea.value = templateData[selected].body + signature;
        }
    }
    // Trigger input events for live updates (if needed by frameworks)
    if (mailSubjectInput) mailSubjectInput.dispatchEvent(new Event('input'));
    if (mailBodyTextarea) mailBodyTextarea.dispatchEvent(new Event('input'));
}
function updateSignatureInBody() {
    const sigSelected = mailSignatureSelect.value;
    let body = mailBodyTextarea.value;
    // Remove any existing signature (assume signature is always at the end, separated by \n)
    for (const sig of Object.values(signatureData)) {
        if (body.endsWith('\n' + sig)) {
            body = body.slice(0, -sig.length - 1);
        } else if (body.endsWith(sig)) {
            body = body.slice(0, -sig.length);
        }
    }
    if (sigSelected && signatureData[sigSelected]) {
        // Remove trailing newlines before appending
        body = body.replace(/\n+$/, '');
        body = body + '\n' + signatureData[sigSelected];
    }
    mailBodyTextarea.value = body;
}
if (mailTemplateSelect) {
    mailTemplateSelect.addEventListener('change', updateMailFieldsFromTemplate);
}
if (mailSignatureSelect) {
    mailSignatureSelect.addEventListener('change', updateSignatureInBody);
}
