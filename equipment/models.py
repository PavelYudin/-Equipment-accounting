from django.db import models
from .validators import validate_file_extension
from django.utils import timezone
import os

class Delivery(models.Model):
	date=models.DateField(default=timezone.now,db_index=True,verbose_name='Поступления оборудования')
	supplier=models.CharField(max_length=50,verbose_name='Поставщик')
	file = models.FileField(upload_to="equipment_files/coming/%Y/%m/%d",blank=True, validators=[validate_file_extension])
	def __str__(this):
		return this.supplier
	class Meta:
		verbose_name_plural='Поступления'
		verbose_name='поступление'
		ordering=['-id']

class Equipment(models.Model):
	name=models.CharField(max_length=100,db_index=True,verbose_name='Наименование')
	count=models.PositiveSmallIntegerField(verbose_name='Количество')
	in_stock=models.PositiveSmallIntegerField(verbose_name='В наличии')
	note=models.CharField(max_length=200,blank=True,verbose_name='Примечание')
	delivery=models.ForeignKey(Delivery,on_delete=models.CASCADE,verbose_name='Поставщик')
	class Meta:
		verbose_name_plural='Принятое оборудование'
		verbose_name='Принятое оборудование'
	def __str__(this):
		return this.name

class Consumption(models.Model):
	date=models.DateField(default=timezone.now,db_index=True,verbose_name='Выдача оборудования')
	customer=models.CharField(max_length=50,verbose_name='Клиент')
	file=models.FileField(upload_to="equipment_files/consumption/%Y/%m/%d",blank=True, validators=[validate_file_extension])
	def __str__(this):
		return this.customer
	class Meta:
		verbose_name_plural='Расход'
		verbose_name='Расход'
		ordering=['-id']

class Issued_equipment(models.Model):
	return_count=models.PositiveSmallIntegerField(default=0, verbose_name='Возвращено')
	count=models.PositiveSmallIntegerField(verbose_name='Количество')
	note=models.CharField(max_length=200,blank=True,verbose_name='Примечание')
	consumption=models.ForeignKey(Consumption,on_delete=models.CASCADE,verbose_name='Клиент')
	equipment=models.ForeignKey(Equipment,on_delete=models.CASCADE,db_index=True,verbose_name='Оборудование')
	class Meta:
		verbose_name_plural='Выданное оборудование'
		verbose_name='Выданное оборудование'
	def __str__(this):
		return this.equipment.name

class Returned(models.Model):
	date=models.DateField(default=timezone.now,db_index=True,verbose_name='Возврат оборудования')
	supplier=models.CharField(max_length=50,verbose_name='Поставщик')
	file = models.FileField(upload_to="equipment_files/returns/%Y/%m/%d",blank=True, validators=[validate_file_extension])
	def __str__(this):
		return this.supplier
	class Meta:
		verbose_name_plural='Возврат оборудования'
		verbose_name='Возврат оборудования'
		ordering=['-id']

class Returned_equipment(models.Model):
	repair=models.BooleanField(verbose_name='В ремонт')
	count=models.PositiveSmallIntegerField(verbose_name='Количество')
	note=models.CharField(max_length=200,blank=True,verbose_name='Примечание')
	consumption=models.ForeignKey(Returned,on_delete=models.CASCADE,verbose_name='Поставщик')
	equipment=models.ForeignKey(Issued_equipment,on_delete=models.CASCADE,db_index=True,verbose_name='Оборудование')
	class Meta:
		verbose_name_plural='Возвращенное оборудование'
		verbose_name='Возвращенное оборудование'
	def __str__(this):
		return this.equipment.__str__()

class Basket(models.Model):
	date=models.DateField(default=timezone.now,db_index=True,verbose_name='Списанное оборудование')
	file = models.FileField(upload_to="equipment_files/basket/%Y/%m/%d",blank=True, validators=[validate_file_extension])
	class Meta:
		verbose_name_plural='Списание'
		ordering=['-id']
	def __str__(this):
		return this.date.__str__()

class Basket_equipment(models.Model):
	count=models.PositiveSmallIntegerField(verbose_name='Количество')
	note=models.CharField(max_length=200,blank=True,verbose_name='Примечание')
	key=models.ForeignKey(Basket,on_delete=models.CASCADE,verbose_name='Дата')
	equipment=models.ForeignKey(Returned_equipment,on_delete=models.CASCADE,db_index=True,verbose_name='Оборудование')
	class Meta:
		verbose_name_plural='Списанное оборудование'

class Repair(models.Model):
	service_center=models.CharField(max_length=50,verbose_name='Сервисный центр')
	date_from=models.DateField(default=timezone.now,db_index=True,verbose_name='Дата передачи в ремонт')
	date_back=models.DateField(blank=True,null=True,verbose_name='Дата возвращения из ремонта')
	file_from = models.FileField(upload_to="equipment_files/repair/from/%Y/%m/%d",blank=True, validators=[validate_file_extension])
	file_back = models.FileField(upload_to="equipment_files/repair/back/%Y/%m/%d",blank=True, validators=[validate_file_extension])
	class Meta:
		verbose_name_plural='В ремонте'
		ordering=['-id']
	def __str__(this):
		return this.date_from.__str__()

class Repair_equipment(models.Model):
	count=models.PositiveSmallIntegerField(verbose_name='Количество')
	note=models.CharField(max_length=200,blank=True,verbose_name='Примечание')
	key=models.ForeignKey(Repair,on_delete=models.CASCADE,verbose_name='Дата передачи в ремонт')
	equipment=models.ForeignKey(Returned_equipment,on_delete=models.CASCADE,db_index=True,verbose_name='Оборудование')
	class Meta:
		verbose_name_plural='Оборудование в ремонте'

		