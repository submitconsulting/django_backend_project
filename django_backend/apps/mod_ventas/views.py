# _*_ coding: utf-8 _*_
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404, render,redirect
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from apps.space.models import Headquart

#@csrf_exempt
def mod_ventas_dashboard(request):
	
	c = {
		"page_module":("mod_ventas_dashboard"),
		"page_title":("mod_ventas_dashboard page."),
		}
	return render_to_response("mod_ventas/dashboard.html", c, context_instance = RequestContext(request))
