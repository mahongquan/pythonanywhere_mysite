# -*- coding: utf-8 -*-
from django.contrib import admin
from mysite.app1.models import Contact
class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'tiaoshi_date'
    list_display =  ('hetongbh','yiqibh','yiqixinghao', 'yonghu')
    list_filter = ('baoxiang','yiqixinghao')
    search_fields = ('hetongbh', 'yonghu','yiqibh')
    list_per_page=10
admin.site.register(Contact,ContactAdmin)