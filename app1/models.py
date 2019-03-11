# -*- coding: utf-8 -*-
from django.db import models
import datetime
class Contact(models.Model):
    #=======销售===========
    yonghu = models.CharField(max_length=30,verbose_name="用户单位")#用户单位
    addr = models.CharField(max_length=30,verbose_name="客户地址",null=True,blank=True)#用户单位
    channels = models.CharField(max_length=30,verbose_name="通道配置",null=True,blank=True)#用户单位
    yiqixinghao=models.CharField(max_length=30,verbose_name="仪器型号")#仪器型号
    yiqibh=models.CharField(unique=True,max_length=30,verbose_name="仪器编号")#仪器编号
    baoxiang =  models.CharField(max_length=30,verbose_name="包箱")#包箱
    shenhe =  models.CharField(max_length=30,verbose_name="审核")#审核
    yujifahuo_date = models.DateField(verbose_name="预计发货时间")#预计发货时间
    tiaoshi_date = models.DateField(null=True,blank=True,verbose_name="调试时间",default=datetime.datetime.now)#预计发货时间
    hetongbh=models.CharField(max_length=30,verbose_name="合同编号")#合同编号
    # method=models.FileField(null=True,blank=True,verbose_name="方法")
    def json(self):
        fields=type(self)._meta.fields
        dic1={}
        for f in fields:
            if f.name in ["image"]:
                pass
            else:
                exec("dic1['%s']=self.%s" %(f.name,f.name))
        dic1["_id"]=self.id
        return dic1