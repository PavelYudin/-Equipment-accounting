from django.contrib import admin
import os
from equipment import views
from django.urls import path,include,re_path

urlpatterns = [
    path('admin', admin.site.urls),
    path('',include('equipment.urls')),
    re_path(r'.',views.notFound),
]
