# -*- coding: utf-8 -*-
from django.http import HttpResponse
from mysite.app1.models import Contact
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
import datetime
import json
from django.db.models import Q
import sys
import traceback
import mysite
import django
from django.core.exceptions import ObjectDoesNotExist
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        #logging.info(obj)
        if isinstance(obj,datetime.date):
            return "%d-%02d-%02d" % (obj.year,obj.month,obj.day)
        if isinstance(obj,datetime.datetime):
            return "%d-%02d-%02d" % (obj.year,obj.month,obj.day)
        # if isinstance(obj,mysite.parts.models.Item):
        #     return obj.name
        # if isinstance(obj,FieldFile):
        #     #logging.info(dir(obj))
        #     return obj.name
        if isinstance(obj,mysite.app1.models.Contact):
            return obj.json()
        # if isinstance(obj,mysite.parts.models.Item):
        #     return obj.json()
        return json.JSONEncoder.default(self, obj)
def index(request):
    objects=Contact.objects.order_by('-yujifahuo_date').all()
    paginator= Paginator(objects, 10)#contact number per page
    page = request.GET.get('page',1)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    r=render_to_response("app1/index.html",{"user":request.user,"contacts":contacts})
    return r
def contact(request):
    logging.info("=contact==========")
    logging.info(request)
    logging.info("------------------")
    if request.method == 'GET':
        return view_contact(request)
    if request.method == 'POST':
        return create_contact(request)
    if request.method == 'PUT':
        return update_contact(request)
    if request.method == 'DELETE':
        return destroy_contact(request)
def view_contact(request):
    start=int(request.GET.get("start","0"))
    limit=int(request.GET.get("limit","20"))
    search=request.GET.get("search",'')
    baoxiang=request.GET.get("baoxiang",'')
    logging.info("search="+search)
    logging.info("baoxiang="+baoxiang)
    if search!='':
        if baoxiang!="":
            tmp=Contact.objects.filter((Q(hetongbh__icontains=search) | Q(yiqibh__icontains=search) | Q(yonghu__icontains=search)) & Q(baoxiang=baoxiang))
            total=tmp.count()
            objs =tmp.order_by('-yujifahuo_date')[start:start+limit]
        else:
            tmp=Contact.objects.filter(Q(hetongbh__icontains=search)| Q(yonghu__icontains=search) | Q(yiqibh__icontains=search))
            total=tmp.count()
            objs = tmp.order_by('-yujifahuo_date')[start:start+limit]
    else:
        if baoxiang!="":
            tmp=Contact.objects.filter(Q(baoxiang=baoxiang))
            total=tmp.count()
            objs =tmp.order_by('-yujifahuo_date')[start:start+limit]
        else:
            total=Contact.objects.count()
            objs = Contact.objects.order_by('-yujifahuo_date')[start:start+limit]
    data=[]
    for rec in objs:
        data.append(rec.json())
    #logging.info(data)
    output={"total":total,"data":data,"user":request.user.username}
    return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
def create_contact(request):
    try:
        logging.info(request.body)
        data = json.loads(request.body.decode("utf-8"))#extjs read data from body
        rec=Contact()
        if data.get("hetongbh")!=None:
            rec.hetongbh=data["hetongbh"]
        if data.get("yujifahuo_date")!=None:
            dt=datetime.datetime.strptime(data["yujifahuo_date"],'%Y-%m-%d')
            rec.yujifahuo_date=dt.date()
        if data.get("yonghu")!=None:
            rec.yonghu=data.get("yonghu")
        if data.get("baoxiang")!=None:
            rec.baoxiang=data.get("baoxiang")
        if data.get("yiqixinghao")!=None:
            rec.yiqixinghao=data.get("yiqixinghao")
        if data.get("yiqibh")!=None:
            rec.yiqibh=data.get("yiqibh")
        if data.get("shenhe")!=None:
            rec.shenhe=data.get("shenhe")
        if data.get("addr")!=None:
            rec.addr=data.get("addr")
        if data.get("channels")!=None:
            rec.channels=data.get("channels")
        if data.get("tiaoshi_date")!=None:
            #rec.tiaoshi_date=datetime.datetime.fromtimestamp(int(data["tiaoshi_date"]))
            dt=datetime.datetime.strptime(data["tiaoshi_date"],'%Y-%m-%d')
            rec.tiaoshi_date=dt.date()
        rec.save()
        output={"success":True,"message":"Created new User" +str(rec.id)}
        output["data"]=rec.json()#{"id":rec.id,"shenhe":rec.shenhe,"hetongbh":rec.hetongbh,"yiqibh":rec.yiqibh,"yiqixinghao":rec.yiqixinghao,"yujifahuo_date":rec.yujifahuo_date,"yonghu":rec.yonghu,"baoxiang":rec.baoxiang,"addr":rec.addr,"channels":rec.channels,"tiaoshi_date":rec.tiaoshi_date}
        return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
    except ValueError as e:
        info = sys.exc_info()
        message=""
        for file, lineno, function, text in traceback.extract_tb(info[2]):
            message+= "%s line:, %s in %s: %s" % (file,lineno,function,text)
        message+= "** %s: %s" % info[:2]
        output={"success":False,"message":message}
        return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
    except django.db.utils.IntegrityError as e:
        print(e,dir(e))
        if "hetongbh" in e.args[0]:
            message="合同编号必须唯一，不能重复！"
        elif "yiqibh" in e.args[0]:
            message="仪器编号必须唯一，不能重复！"
        else:
            info = sys.exc_info()
            message=""
            for file, lineno, function, text in traceback.extract_tb(info[2]):
                message+= "%s line:, %s in %s: %s\n" % (file,lineno,function,text)
            message+= "** %s: %s" % info[:2]
        output={"success":False,"message":message}
        return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
def update_contact(request):
    try:
        data = json.loads(request.body.decode("utf-8"))#extjs read data from body
        logging.info(data)
        id1=data.get("id")
        id1=int(id1)
        rec=Contact.objects.get(id=id1)
        rec.myupdate(data)
        rec.save()
        output={"success":True,"message":"update Contact " +str(rec.id)}
        output["data"]=rec.json()
        return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
    except ValueError as e:
        info = sys.exc_info()
        message=""
        for file, lineno, function, text in traceback.extract_tb(info[2]):
            message+= "%s line:, %s in %s: %s" % (file,lineno,function,text)
        message+= "** %s: %s" % info[:2]
        output={"success":False,"message":message}
        return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
    except django.db.utils.IntegrityError as e:
        print(e,dir(e))
        if "hetongbh" in e.args[0]:
            message="合同编号必须唯一，不能重复！"
        elif "yiqibh" in e.args[0]:
            message="仪器编号必须唯一，不能重复！"
        else:
            info = sys.exc_info()
            message=""
            for file, lineno, function, text in traceback.extract_tb(info[2]):
                message+= "%s line:, %s in %s: %s\n" % (file,lineno,function,text)
            message+= "** %s: %s" % info[:2]
        output={"success":False,"message":message}
        return HttpResponse(json.dumps(output, ensure_ascii=False,cls=MyEncoder))
def destroy_contact(request):
    data = json.loads(request.body.decode("utf-8"))
    id=data.get("id")
    if id!=None:
        try:
            id1=int(id)
            rec=Contact.objects.get(id=id1)
            rec.delete()
            output={"success":True,"message":"OK"}
            return HttpResponse(json.dumps(output, ensure_ascii=False))
        except ObjectDoesNotExist as e:
            output={"success":False,"message":str(e)}
            return HttpResponse(json.dumps(output, ensure_ascii=False))
    else:
        output={"success":False,"message":"OK"}
        return HttpResponse(json.dumps(output, ensure_ascii=False))
