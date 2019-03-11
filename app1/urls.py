from django.conf.urls.defaults import patterns, include, url
from mysite.app1 import views
urlpatterns = [
	url(r'^$',views.index),
	url(r'^contact$',views.contact),
	];
