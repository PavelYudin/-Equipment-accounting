function sorting(e){			
	sign=sign==1?-1:1;
	let header=document.querySelector('.header');
	let array_head=Array.prototype.slice.call(header.children);
	let target;
	if(e.target.tagName=='P'){
		target=e.target.parentElement;				
	}else if(e.target.tagName=='DIV'){
		target=e.target;
	}
	let index=array_head.indexOf(target);
	lines=document.getElementsByClassName('d-tr');
	array_sort=[]
	for(let i=1;i<lines.length;i++){
		let a=[];
		let pk=lines[i].getAttribute('data-pk');
		for(let j=0;j<lines[i].children.length;j++){
			let value=lines[i].children[j];
			let data_repair;
			if(value.hasAttribute('data-repair')) data_repair=value.getAttribute('data-repair');
			value=value.textContent;
			if(!isNaN(+value) && value.trim()!=='') value=+value;
			a.push(value);
			if(data_repair) a.push(data_repair)
		}
		let map=new Map();
		map.set(pk,a)
		array_sort.push(map);
	}
	function convert_date(date){
		date=date.replace(/(\w+).(\w+)/i,'$2.$1')
		return date=Date.parse(date)
	}
	function sort(a,b){
		a=a.values().next().value[index];
		b=b.values().next().value[index]
		if(!index){
			a=convert_date(a);
			b=convert_date(b);
		}
		if (a > b) return sign*1;
		if (a == b) return 0;
		if (a < b) return sign*-1; 
	}
	array_sort.sort(sort);
	for(let i=1;i<lines.length;i++){
		let pk=array_sort[i-1].keys().next().value;
		lines[i].setAttribute('data-pk',pk);
		for(let j=0;j<lines[i].children.length;j++){
			let value=lines[i].children[j];
			value.children[0].innerHTML=array_sort[i-1].values().next().value[j];
			if(value.hasAttribute('data-repair')) value.setAttribute('data-repair',array_sort[i-1].values().next().value[j+1]);
		}
	}					
}