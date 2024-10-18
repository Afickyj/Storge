document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#registrationForm');
    const password1 = form.querySelector('#id_password1');
    const password2 = form.querySelector('#id_password2');

    form.addEventListener('submit', function(event) {
        // Kontrola shody hesel
        if (password1.value !== password2.value) {
            event.preventDefault();
            alert('Hesla se neshodují.');
            password2.focus();
        }
    });
});
