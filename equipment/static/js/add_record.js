function add_record(){	
	div=document.createElement('div');
	div.setAttribute("name","div_add")
	label_name=document.createElement('label');
	label_name.innerHTML="Наименование: ";
	label_name.setAttribute('for','supplier');
	input_name=document.createElement('input');
	input_name.setAttribute('type','text');
	input_name.setAttribute('name','name');
	input_name.setAttribute('size','30');
	label_count=document.createElement('label');
	label_count.innerHTML=" Количество: ";
	label_count.setAttribute('for','count');
	input_count=document.createElement('input');
	input_count.setAttribute('type','number');
	input_count.setAttribute('name','count');
	input_count.setAttribute('size','1');
	input_count.setAttribute('value','1');
	input_count.setAttribute('max','32767');
	input_count.setAttribute('min','1');
	label_note=document.createElement('label');
	label_note.innerHTML=" Примечание: ";
	label_note.setAttribute('for','note');
	input_note=document.createElement('textarea');
	input_note.setAttribute('name','note');
	input_note.setAttribute('cols',35);
	div.append(label_name,input_name,label_count,input_count,label_note,input_note);
	if(arguments.length){
		let args;
		if(Object.prototype.toString.call(arguments[arguments.length-1]) == '[object Function]'){
			div.append(...arguments[arguments.length-1]());
			arg=[].slice.call(arguments,0,arguments.length-1);
			input_count.setAttribute('max',arguments[1])
		}else{
			arg=[].slice.call(arguments);
			input_count.setAttribute('max',arguments[1])
		}
		function fill(){
			[...arguments].forEach((elem,i)=>{elem.value=arg[i];})
		}
		
		input_name.setAttribute('readonly',true);
		
		input_pk=document.createElement('input');
		input_pk.style.display='none';
		input_pk.setAttribute('name','pk');
		div.prepend(input_pk);
		fill(input_name,input_count,input_note,input_pk);
	}
	return div;
}
