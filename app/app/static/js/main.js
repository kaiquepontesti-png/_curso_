function formatPriceInput(value) {
  const digitsOnly = (value || '').replace(/\D/g, '');

  if (!digitsOnly) {
    return '';
  }

  if (digitsOnly.length === 1) {
    return `0,0${digitsOnly}`;
  }

  if (digitsOnly.length === 2) {
    return `0,${digitsOnly}`;
  }

  const integerPart = digitsOnly.slice(0, -2).replace(/^0+(?=\d)/, '');
  const decimalPart = digitsOnly.slice(-2).padStart(2, '0');
  const normalizedInteger = integerPart || '0';
  const formattedInteger = normalizedInteger.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

  return `${formattedInteger},${decimalPart}`;
}

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

  const priceInputs = document.querySelectorAll('input[name="preco"]');

  priceInputs.forEach((input) => {
    input.setAttribute('inputmode', 'numeric');
    input.setAttribute('autocomplete', 'off');

    const applyPriceFormat = () => {
      const nextValue = formatPriceInput(input.value);
      if (nextValue !== input.value) {
        input.value = nextValue;
      }
    };

    input.addEventListener('input', applyPriceFormat);
    input.addEventListener('blur', () => {
      if (!input.value) {
        input.value = '0,00';
      }
    });
  });
});
