document.addEventListener('DOMContentLoaded', () => {
  const confirmButtons = document.querySelectorAll('[data-confirm]');

  confirmButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
      const message = button.getAttribute('data-confirm') || 'Deseja confirmar esta ação?';
      const shouldContinue = window.confirm(message);
      if (!shouldContinue) {
        event.preventDefault();
      }
    });
  });
});
