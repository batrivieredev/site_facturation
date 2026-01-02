document.addEventListener('DOMContentLoaded', () => {

    const templateSelect = document.getElementById('mail-template');
    const signatureSelect = document.getElementById('mail-signature');
    const subjectInput = document.getElementById('mail-subject');
    const bodyTextarea = document.getElementById('mail-body');

    let currentSignature = '';

    function escapeRegExp(text) {
        return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function removeSignature(text) {
        if (!currentSignature) return text;
        const regex = new RegExp(`\\n*${escapeRegExp(currentSignature)}$`);
        return text.replace(regex, '');
    }

    function applyTemplate() {
        const option = templateSelect.options[templateSelect.selectedIndex];
        if (!option || !option.dataset.body) return;

        subjectInput.value = option.dataset.subject || '';
        bodyTextarea.value = option.dataset.body || '';

        applySignature();
    }

    function applySignature() {
        let body = removeSignature(bodyTextarea.value);
        const option = signatureSelect.options[signatureSelect.selectedIndex];

        if (option && option.dataset.signature) {
            currentSignature = option.dataset.signature;
            body = body.replace(/\n*$/, '');
            body += '\n\n' + currentSignature;
        } else {
            currentSignature = '';
        }

        bodyTextarea.value = body;
    }

    templateSelect.addEventListener('change', applyTemplate);
    signatureSelect.addEventListener('change', applySignature);

});
