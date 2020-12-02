from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest,HttpResponseNotFound
from .models import (Delivery,Equipment,Consumption,Issued_equipment,
	Returned,Returned_equipment,Basket,Basket_equipment,Repair,Repair_equipment)
from django.template import loader
from django.db.models import F
from django.http import JsonResponse
from django.utils import timezone
import json

def main(req):
	return render(req,'main.html')

def media(req):
	from django.http import FileResponse
	import os
	path=req.path.replace('/','\\')
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	url=BASE_DIR+path
	if os.path.isfile(url):
		response = FileResponse(open(url, 'rb'))
		return response
	else:
		return HttpResponseNotFound("<h2>Файл удален</h2>")

def receiving(req):
	coming=Delivery.objects.all()
	context={'coming':coming}
	return render(req,'receiving.html',context)

def received_equipment(req,date_id):
	record=Equipment.objects.filter(delivery=date_id)
	current_delivery=Delivery.objects.get(pk=date_id)
	context={'record':record,'current_delivery':current_delivery}
	return render(req,'received_equipment.html',context)

def add_equipment(req):
	if(req.method=="POST"):
		def add_Delivery():
			obj=Delivery()
			obj.supplier=req.POST.get('supplier')
			if('file' in req.FILES):
				obj.file=req.FILES['file']
			obj.save()
		flag=True
		i = 0
		while i < len(dict(req.POST)['name']):			
			if(dict(req.POST)['name'][i].strip() and dict(req.POST)['count'][i]):
				if(flag):
					add_Delivery()
					flag=False
				obj=Equipment()
				obj.name=dict(req.POST)['name'][i]
				obj.count=dict(req.POST)['count'][i]
				obj.in_stock=dict(req.POST)['count'][i]
				obj.note=dict(req.POST)['note'][i]
				obj.delivery=Delivery.objects.all().first()
				obj.save()
			i += 1
	return HttpResponseRedirect("/delivery")

def transfer(req):
	if(req.method=="POST"):
		def add_Consumption():
			obj=Consumption()
			obj.customer=req.POST.get('supplier')
			if('file' in req.FILES):
				obj.file=req.FILES['file']
			obj.save()
		flag=True
		i = 0
		while i < len(dict(req.POST)['name']):
			obj=Issued_equipment()
			if(dict(req.POST)['name'][i].strip() and dict(req.POST)['count'][i]):
				equipment_delivery=Equipment.objects.get(pk=dict(req.POST)['pk'][i])
				if(equipment_delivery.in_stock>=int(dict(req.POST)['count'][i])):
					if(flag):
						add_Consumption()
						flag=False				
					obj.equipment=equipment_delivery
					obj.count=dict(req.POST)['count'][i]
					equipment_delivery.in_stock=equipment_delivery.in_stock-int(obj.count)
					equipment_delivery.save()
					obj.note=dict(req.POST)['note'][i]
					obj.consumption=Consumption.objects.all().first()
					obj.save()
			i += 1
	return HttpResponseRedirect("/delivery")	

def issue(req):
	consumption=Consumption.objects.all()
	context={'consumption':consumption}
	return render(req,'issue.html',context)

def issued_equipment(req,date_id):
	record=Issued_equipment.objects.filter(consumption=date_id)
	for i in record:
		i.name=Equipment.objects.get(pk=i.equipment_id)
	current_delivery=Consumption.objects.get(pk=date_id)
	context={'record':record,'current_delivery':current_delivery}
	return render(req,'issued_equipment.html',context)

def all_equipment(req):
	equipment_list=[]
	data_equipment_list=Delivery.objects.all()
	for i in data_equipment_list:
		record=Equipment.objects.filter(delivery_id=i.id).order_by('name','-in_stock')
		for j in record:
			j.supplier=i.supplier
			j.date=i.date
			equipment_list.append(j)
	context={'record':equipment_list}
	return render(req,'all_equipment.html',context)

def all_issued_equipment(req):
	equipment_list=[]
	data_equipment_list=Consumption.objects.all()
	for i in data_equipment_list:
		obj=Issued_equipment.objects.filter(consumption_id=i.id)
		for j in obj:
			name=Equipment.objects.get(id=j.equipment_id)
			j.name=name
			j.date=i.date
			j.customer=i.customer
			equipment_list.append(j)
	context={'record':equipment_list}
	return render(req,'all_issued_equipment.html',context)

def all_returned_equipment(req):
	equipment_list=[]
	data_equipment_list=Returned.objects.all()
	for i in data_equipment_list:
		obj=Returned_equipment.objects.filter(consumption_id=i.id)
		for j in obj:
			j.name=Issued_equipment.objects.get(id=j.equipment_id)
			j.date=i.date
			j.supplier=i.supplier
			equipment_list.append(j)
	context={'record':equipment_list}	
	return render(req,'all_returned_equipment.html',context)

def returned(req):
	returned=Returned.objects.all()
	context={'returned':returned}
	return render(req,'returned.html',context)

def returned_equipment(req,date_id):
	record=Returned_equipment.objects.filter(consumption=date_id)
	for i in record:
		i.name=Issued_equipment.objects.get(pk=i.equipment_id)
	current_delivery=Returned.objects.get(pk=date_id)
	context={'record':record,'current_delivery':current_delivery}
	return render(req,'returned_equipment.html',context)

def returns_add(req):
	def add_Returned():# добавляем в главную таблицу по возвратам
		obj=Returned()
		obj.supplier=req.POST.get('supplier')
		if('file' in req.FILES):
			obj.file=req.FILES['file']
		obj.save()

	def change_count(input_checkbox):#изменяем кол-во в таблице принятых и выданных
		Issued_equipment.objects.filter(pk=dict(req.POST)['pk'][i]).update(return_count = F("return_count") + dict(req.POST)['count'][i])
		if(input_checkbox==False):
			obj=Issued_equipment.objects.get(pk=dict(req.POST)['pk'][i])
			obj=Equipment.objects.get(pk=obj.equipment_id)			
			Equipment.objects.filter(pk=obj.pk).update(in_stock = F("in_stock") + dict(req.POST)['count'][i])
			
	if(req.method=="POST"):
		i = 0
		flag=True	
		while i < len(dict(req.POST)['pk']):
			if(dict(req.POST)['name'][i].strip() and dict(req.POST)['count'][i]):
				if(flag): 
					add_Returned()
					flag=False
				input_checkbox=json.loads(dict(req.POST)['input_checkbox'][i])
				change_count(input_checkbox)
				obj=Returned_equipment()
				obj.repair=input_checkbox
				obj.count=dict(req.POST)['count'][i]
				obj.note=dict(req.POST)['note'][i]
				obj.consumption=Returned.objects.all().first()				
				obj.equipment=Issued_equipment.objects.get(pk=dict(req.POST)['pk'][i])
				obj.save()
			i+=1

	return HttpResponseRedirect("/issue")	

def repair_add(req):
	def change_count():#изменяем кол-во в таблице принятых и выданных
		Returned_equipment.objects.filter(pk=dict(req.POST)['pk'][i]).update(count = F("count") - dict(req.POST)['count'][i])
	if(req.method=="POST"):
		def add_Repair():
			obj=Repair()
			obj.service_center=req.POST.get('service_center')
			if('file' in req.FILES):
				obj.file_from=req.FILES['file']
			obj.save()
		flag=True
		i=0
		while i < len(dict(req.POST)['name']):			
			if(dict(req.POST)['name'][i].strip() and dict(req.POST)['count'][i]):
				if(flag):
					add_Repair()
					flag=False
				change_count()
				obj=Repair_equipment()
				obj.count=dict(req.POST)['count'][i]
				obj.note=dict(req.POST)['note'][i]
				obj.key=Repair.objects.all().first()
				obj.equipment=Returned_equipment.objects.get(pk=dict(req.POST)['pk'][i])
				obj.save()
			i += 1		
	return HttpResponseRedirect("/returned")	

def out_of_repair(req):
	if(req.method=="POST"): 
		pk=dict(req.POST)['pk'][0]	
		obj=Repair.objects.get(id=pk)
		if('file' in req.FILES):
			obj.file_from=req.FILES['file']
		obj.date_back=timezone.now()
		obj.save()
		obj=Repair_equipment.objects.filter(key_id=pk)
		for i in obj:
			s1=Returned_equipment.objects.filter(id=i.equipment_id)
			s2=Issued_equipment.objects.filter(id=s1[0].equipment_id)
			Equipment.objects.filter(id=s2[0].equipment_id).update(in_stock = F("in_stock") + i.count)		
	return JsonResponse({"url": "/repair"})


def repair(req):
	coming=Repair.objects.all()
	context={'coming':coming}
	return render(req,'repair.html',context)

def repair_equipment(req,date_id):
	record=Repair_equipment.objects.filter(key_id=date_id)
	for i in record:
		i.name=Returned_equipment.objects.get(pk=i.equipment_id)
	current_delivery=Repair.objects.get(pk=date_id)
	context={'record':record,'current_delivery':current_delivery}
	return render(req,'repair_equipment.html',context)

def basket_add(req):
	def change_count():#изменяем кол-во в таблице принятых и выданных
		Returned_equipment.objects.filter(pk=dict(req.POST)['pk'][i]).update(count = F("count") - dict(req.POST)['count'][i])
	if(req.method=="POST"):
		def add_Basket():
			obj=Basket()
			if('file' in req.FILES):
				obj.file=req.FILES['file']
			obj.save()
		flag=True
		i=0
		while i < len(dict(req.POST)['name']):			
			if(dict(req.POST)['name'][i].strip() and dict(req.POST)['count'][i]):
				if(flag):
					add_Basket()
					flag=False
				change_count()
				obj=Basket_equipment()
				obj.count=dict(req.POST)['count'][i]
				obj.note=dict(req.POST)['note'][i]
				obj.key=Basket.objects.all().first()
				obj.equipment=Returned_equipment.objects.get(pk=dict(req.POST)['pk'][i])
				obj.save()
			i += 1
	return HttpResponseRedirect("/returned")

def basket(req):
	coming=Basket.objects.all()
	context={'coming':coming}
	return render(req,'basket.html',context)

def basket_equipment(req,date_id):
	record=Basket_equipment.objects.filter(key_id=date_id)
	for i in record:
		i.name=Returned_equipment.objects.get(pk=i.equipment_id)
	current_delivery=Basket.objects.get(pk=date_id)
	context={'record':record,'current_delivery':current_delivery}
	return render(req,'basket_equipment.html',context)

def all_basket_equipment(req):
	equipment_list=[]
	data_equipment_list=Basket.objects.all()
	for i in data_equipment_list:
		obj=Basket_equipment.objects.filter(key_id=i.id)
		for j in obj:
			j.name=Returned_equipment.objects.get(id=j.equipment_id)
			j.date=i.date
			equipment_list.append(j)
	context={'record':equipment_list}	
	return render(req,'all_basket_equipment.html',context)

def notFound(req):
    return HttpResponseNotFound("<h2>Not Found</h2>")