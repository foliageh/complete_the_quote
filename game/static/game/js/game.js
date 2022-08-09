document.addEventListener('DOMContentLoaded', function() {
	document.querySelector('#check').onclick = () => checkQuote();
	document.querySelector('#next').onclick = () => loadQuote();
	loadQuote();
});

function checkQuote() {
	const quote = JSON.parse(localStorage.getItem('quote'));
	let word_index=0;
	document.querySelectorAll('.word-input').forEach(field => {
		const word = field.value;
		const right_word = quote.hided_words[word_index];
		if (word === right_word) {
			field.classList.add('right-word');
		}
		else {
			field.parentElement.setAttribute('data-bs-content', right_word);
			const popover = new bootstrap.Popover(field.parentElement);
			popover.show();
			field.classList.add('wrong-word');
		}
		field.setAttribute('disabled', '');
		word_index += 1
	});

	const check_btn = document.querySelector('#check');
	const next_btn = document.querySelector('#next');
    check_btn.style.animationPlayState = 'running';
    check_btn.addEventListener('animationend', () => {
		check_btn.setAttribute('hidden', '');
		next_btn.style.animation = 'none';
		next_btn.offsetHeight;
		next_btn.style.animation = null;
		next_btn.style.animationPlayState = 'running';
		next_btn.removeAttribute('hidden');
		check_btn.style.animation = 'none';
  		check_btn.offsetHeight;
  		check_btn.style.animation = null;
    });
}
function loadQuote(){
	document.querySelector('#next').setAttribute('hidden', '');
	document.querySelectorAll('[data-bs-toggle="popover"]')
    .forEach(field => {
		const popover = bootstrap.Popover.getOrCreateInstance(field);
		popover.hide();
    })

	document.querySelector('#quote-author').innerHTML = 'Loading...';
	document.querySelector('#masked-quote').innerHTML = 'Loading...';
	document.querySelector('#quote-translation').innerHTML = 'Загрузка...';
	fetch(`/api/get_quote`)
	.then(response => response.json())
    .then(quote => {
		document.querySelector('#quote-author').innerHTML = quote.author;
		document.querySelector('#quote-translation').innerHTML = quote.translation;
		localStorage.setItem('quote', JSON.stringify(quote));

		let masked_quote_html = '';
		quote.masked_quote.forEach(word => {
			if (word === '___')
				masked_quote_html += `<span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-placement="top" data-bs-trigger="hover focus" data-bs-custom-class="custom-popover">
									  	<input class="word-input">
									  </span>`
			else
				masked_quote_html += word;
		});
		document.querySelector('#masked-quote').innerHTML = masked_quote_html;
		document.querySelector('#check').removeAttribute('hidden');
    });
}