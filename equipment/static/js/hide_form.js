document.addEventListener('keydown', function(event) {
	if (event.code == 'Escape') {
		input=form.querySelector('input[name=supplier]');
		if (input) input.value="";
		div_record=form.querySelectorAll("div[name=div_add]");
		[...div_record].forEach(elem => elem.remove());
  		form.style.display="none";
  	}
});