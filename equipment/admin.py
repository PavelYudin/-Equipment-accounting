from django.contrib import admin
from .models import (Delivery,Equipment,Consumption,Issued_equipment,
	Returned,Returned_equipment,Basket,Basket_equipment,Repair,Repair_equipment)

class DeliveryAdmin(admin.ModelAdmin):
	list_display=('date','supplier','file')
	search_fields=['date']

admin.site.register(Delivery,DeliveryAdmin)

class EquipmentAdmin(admin.ModelAdmin):
	list_display=('name','count','in_stock','note','delivery')
	

admin.site.register(Equipment,EquipmentAdmin)

class ConsumptionAdmin(admin.ModelAdmin):
	list_display=('date','customer','file')
	search_fields=['date']

admin.site.register(Consumption,ConsumptionAdmin)

class Issued_equipmentAdmin(admin.ModelAdmin):
	list_display=('equipment','count','note','consumption','return_count')

admin.site.register(Issued_equipment,Issued_equipmentAdmin)

class ReturnedAdmin(admin.ModelAdmin):
	list_display=('date','supplier','file')
	search_fields=['date']

admin.site.register(Returned,ReturnedAdmin)

class Returned_equipmentAdmin(admin.ModelAdmin):
	list_display=('equipment','count','note','consumption','repair')

admin.site.register(Returned_equipment,Returned_equipmentAdmin)

class BasketAdmin(admin.ModelAdmin):
	list_display=('date','file')
	search_fields=['date']

admin.site.register(Basket,BasketAdmin)

class Basket_equipmentAdmin(admin.ModelAdmin):
	list_display=('equipment','count','note','key')

admin.site.register(Basket_equipment,Basket_equipmentAdmin)

class RepairAdmin(admin.ModelAdmin):
	list_display=('date_from','file_from','date_back','file_back')
	search_fields=['date_from']

admin.site.register(Repair,RepairAdmin)

class Repair_equipmentAdmin(admin.ModelAdmin):
	list_display=('equipment','count','note','key')

admin.site.register(Repair_equipment,Repair_equipmentAdmin)