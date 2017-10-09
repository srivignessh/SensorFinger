from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse
from .models import Acm,Ace,Accmeter,Calibrat
from datetime import datetime
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
import math
import random
import numpy as np
import operator
from sklearn import neighbors

def classify(request):
    vid=request.GET['vid'];
    X_train=[];
    objects=Calibrat.objects.all()
    t=Calibrat.objects.get(vid=vid)
    test=[t.Sx,t.Sy,t.Sz,t.Ox,t.Oy,t.Oz]
    y_train=[];
    for obj in objects:
    	if(obj.vid!=vid):
    		data=[obj.Sx,obj.Sy,obj.Sz,obj.Ox,obj.Oy,obj.Oz]
    		X_train.append(data)
    		y_train.append(obj.uid)
	knn= neighbors.KNeighborsClassifier(n_neighbors=1)
	knn.fit(X_train,y_train)
	res=knn.predict(test)
	print X_train
	print y_train
	return HttpResponse(res)

def fcn2min(params, xm,ym,zm, data):
	""" model decaying sine wave, subtract data"""
	sx=params['Sx']
	sy=params['Sy']
	sz=params['Sz']
	ox=params['Ox']
	oy=params['Oy']
	oz=params['Oz']

	model=((xm-ox)/(sx))**2+((ym-oy)/(sy))**2+((zm-oz)/(sz))**2

	return model - data

def init_params():
	params = Parameters()
	params.add('Sx', value=1, min=0.9, max=1.1)
	params.add('Sy', value= 1, min=0.9, max=1.1)
	params.add('Sz', value= 1, min=0.9, max=1.1)
	params.add('Ox', value= 0, min=-1, max=1)
	params.add('Oy', value= 0, min=-1, max=1)
	params.add('Oz', value= 0, min=-1, max=1)
	return params

def saveit(request):
	vid=request.GET['vid'];

	if (Calibrat.objects.get(vid=vid)):
		return HttpResponse("Saved");
	else:
		return HttpResponse("Save Error"); 

def calibrat(request):
	data = 9.80665**2;
	vid=request.GET['vid']
	print vid
	objects=Accmeter.objects.filter(vid=vid)
	xm=[];ym=[];zm=[];
	for obj in objects:
		uid=obj.uid;
		xm.append(obj.X)
		ym.append(obj.Y)
		zm.append(obj.Z)

	params=init_params();
	# do fit, here with leastsq model
	minner = Minimizer(fcn2min, params, fcn_args=(xm,ym,zm,data))
	result = minner.minimize(method='cg')
	V=result.params;

	output={"Sx": V['Sx'].value , "Sy": V['Sy'].value, "Sz": V['Sz'].value , "Ox": V['Ox'].value,"Oy": V['Oy'].value , "Oz": V['Oz'].value }

	try:
		calibe=Calibrat.objects.get(vid=vid)
	except:
		calibe=Calibrat();
	calibe.uid=uid;
	calibe.vid=vid;
	calibe.Sx=V['Sx'].value;
	calibe.Sy=V['Sy'].value;
	calibe.Sz=V['Sz'].value;
	calibe.Ox=V['Ox'].value;
	calibe.Oy=V['Oy'].value;
	calibe.Oz=V['Oz'].value;
	calibe.timestamp=datetime.now();
	calibe.save();
	return JsonResponse(output)

# Create your views here.s
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request))

def arb(request):
	template = loader.get_template('arb.html')
	return HttpResponse(template.render(request))

def arbit(request):

	if request.method=='GET':
		cm=Accmeter();
		uid=request.GET['uid'];
		cm.uid=uid;
		cm.vid=request.GET['vid'];
		cm.X=request.GET['X'];
		cm.Y=request.GET['Y'];
		cm.Z=request.GET['Z'];
		cm.timestamp=datetime.now();
		cm.save();
		return HttpResponse("Recorded")

def push(request):

    if request.method=='GET':
		cm=Acm();
		cm.uid=request.GET['uid'];
		cm.vid=request.GET['vid'];
		cm.pos=request.GET['pos'];
		cm.X=request.GET['X'];
		cm.Y=request.GET['Y'];
		cm.Z=request.GET['Z'];
		cm.timestamp=datetime.now();
		cm.save();
		return HttpResponse("Recorded")

def calib(request):

	if request.method=='GET':
		ce=Ace();
		ce.uid=request.GET['uid'];
		ce.vpq=request.GET['vpq'];
		ce.pos=request.GET['pos'];
		ce.Sz=request.GET["Sz"];
		ce.Oz=request.GET["Oz"];
		ce.timestamp=datetime.now();
		ce.save();
		return HttpResponse("Calibrated")

def plot(request):
	template = loader.get_template('disp.html')
	return HttpResponse(template.render(request))

def value(request):
	objects=Ace.objects.all()
	new=Ace.objects.all().last()
	array=[];
	ordered = sorted(objects, key=operator.attrgetter('uid'))
	for obj in ordered:
		if(obj.vpq != new.vpq):
			data={"uid":obj.uid,"vid":obj.vpq, "Sz": obj.Sz, "Oz": obj.Oz }
			array.append(data)
		else:
			ndata={"uid":obj.uid,"vid":obj.vpq, "Sz": obj.Sz, "Oz": obj.Oz }
	array.append(ndata)
	return JsonResponse(array,safe=False)

def dele(request):
	Accmeter.objects.all().delete()
	template = loader.get_template('dele.html')
	return HttpResponse(template.render(request))

def delete(request):
	vid=request.GET['vid'];
	elem=Ace.objects.filter(vpq=vid)
	elem.delete();
	return JsonResponse("Deleted",safe=False)
