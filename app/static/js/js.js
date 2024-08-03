document.addEventListener('DOMContentLoaded', (event) => {
    const password = document.getElementById('password');
    const passwordHelpBlock = document.getElementById('passwordHelpBlock');

    password.addEventListener('input', function () {
        let message = 'Ваш пароль должен содержать не менее 8 символов, включать буквы и цифры.';
        const value = password.value;

        if (value.length < 8) {
            message = 'Пароль слишком короткий. Минимум 8 символов.';
        } else if (!/[a-zA-Z]/.test(value)) {
            message = 'Пароль должен содержать хотя бы одну букву.';
        } else if (!/[0-9]/.test(value)) {
            message = 'Пароль должен содержать хотя бы одну цифру.';
        } else {
            message = 'Пароль выглядит хорошо.';
        }

        passwordHelpBlock.textContent = message;
    });
});