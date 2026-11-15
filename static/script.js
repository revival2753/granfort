        document.querySelectorAll('.faq-q').forEach(button => {
			button.addEventListener('click', () => button.parentElement.classList.toggle('open'));
		});

		document.getElementById('leadForm').addEventListener('submit', e => {
			e.preventDefault();
			document.getElementById('formNote').textContent = 'Спасибо! Заявка заполнена. С вами скоро свяжутся.';
			e.currentTarget.reset();
		});