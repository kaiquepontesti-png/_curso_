document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('form:not(.item-toggle-form)');

  forms.forEach((form) => {
    const submitButton = form.querySelector('button[type="submit"]:not(.item-check-toggle)');
    if (!submitButton) return;

    const originalText = submitButton.textContent.trim();

    form.addEventListener('submit', () => {
      submitButton.disabled = true;
      submitButton.textContent = 'Salvando...';
      submitButton.dataset.originalText = originalText;
    });
  });
});
