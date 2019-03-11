from django.http import HttpResponse#,HttpResponseRedirect
# import datetime
from mysite.settings import DATABASES
# from django.shortcuts import render_to_response
import sys
def home(request):
    #now=datetime.datetime.now()
    r=HttpResponse()
    r.content=DATABASES["default"]["NAME"]

    return r#render_to_response('welcome.html', {'mynow':now})
def info(request):
    r=HttpResponse()
    ps=sys.path;
    ps_str=""
    for p in ps:
        ps_str+="<p>%s</p>" % p
    r.content=ps_str;
    return r#render_to_response('welcome.html', {'mynow':now})
