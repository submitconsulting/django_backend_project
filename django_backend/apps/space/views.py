# _*_ coding: utf-8 _*_
#import datetime
#import re
#import json
#from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.http import HttpResponse,HttpResponseRedirect
#from django.utils.encoding import force_text, smart_text
#from django.utils.html import conditional_escape, format_html
#from django.utils.translation import ugettext as _, ungettext 
#from django.template import Context
#from django.template.defaultfilters import capfirst
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from apps.sad.decorators import is_admin, permission_resource_required
from apps.sad.security import Security
from apps.helpers.message import Message

#from django.contrib.auth.models import User, Group, Permission 
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType
from apps.space.models import Solution



def enterprise_edit(request):
	
	t = {
		'page_module':("enterprise_edit"),
		'page_title':("enterprise_edit page."),
		}
	return render_to_response("enterprise/edit.html", t, context_instance = RequestContext(request))


#region solution OK
@permission_resource_required
def solution_index(request):
	"""
	Página principal para trabajar con soluciones
	"""
	try:
		solution_list = Solution.objects.all().order_by("-id")
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de soluciones"),
		'page_title':("Listado de soluciones del sistema."),
		'solution_list':solution_list,
		}
	return render_to_response("space/solution/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
def solution_add(request):
	"""
	Agrega solución
	"""
	d = Solution()
	d.description=""
	if request.method == "POST":
		try:
			d.name = request.POST.get('name')
			d.description = request.POST.get('description')
			if Solution.objects.filter(name = d.name).exclude(id = d.id).count() > 0:
				raise Exception( ("Solución <b>%(name)s</b> ya existe.") % {'name':d.name} )
			d.save()
			if d.id:
				Message.info(request,("Solución <b>%(name)s</b> ha sido registrado correctamente.") % {'name':d.name})
				if request.is_ajax():
					request.path="/space/solution/index/" #/app/controller_path/action/$params
					return solution_index(request)
				else:
					return redirect('/space/solution/index/')
		except Exception, e:
			Message.error(request, e)
	c = {
		'page_module':("Gestión de soluciones"),
		'page_title':("Agregar solución."),
		'd':d,
		}
	return render_to_response("space/solution/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
def solution_edit(request, key):
	"""
	Actualiza solución
	"""
	id=Security.is_valid_key(request, key, 'solution_upd')
	if not id:
		if request.is_ajax():
			request.path="/space/solution/index/" #/app/controller_path/action/$params
			return solution_index(request)
		else:
			return redirect('/space/solution/index/')
	d = None

	try:
		d = get_object_or_404(Solution, id=id)
	except:
		Message.error(request, ("Solución no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/space/solution/index/" #/app/controller_path/action/$params
			return solution_index(request)
		else:
			return redirect('/space/solution/index/')

	if request.method == "POST":
		try:
			d.name = request.POST.get('name')
			d.description = request.POST.get('description')
			if Solution.objects.filter(name = d.name).exclude(id = d.id).count() > 0:
				raise Exception( ("Solución <b>%(name)s</b> ya existe.") % {'name':d.name} )

			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Solución <b>%(name)s</b> ha sido actualizado correctamente.") % {'name':d.name})
				if request.is_ajax():
					request.path="/space/solution/index/" #/app/controller_path/action/$params
					return solution_index(request)
				else:
					return redirect('/space/solution/index/')

		except Exception, e:
			Message.error(request, e)
	c = {
		'page_module':("Gestión de soluciones"),
		'page_title':("Actualizar solución."),
		'd':d,
		}
	return render_to_response("space/solution/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
def solution_delete(request, key):
	"""
	Elimina solución
	"""
	id=Security.is_valid_key(request, key, 'solution_del')
	if not id:
		if request.is_ajax():
			request.path="/space/solution/index/" #/app/controller_path/action/$params
			return solution_index(request)
		else:
			return redirect('/space/solution/index/')
	try:
		d = get_object_or_404(Solution, id=id)
	except:
		Message.error(request, ("Solución no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/space/solution/index/" #/app/controller_path/action/$params
			return solution_index(request)
		else:
			return redirect('/space/solution/index/')
	try:
		d.delete()
		if not d.id:
			Message.info(request,("Solución <b>%(name)s</b> ha sido eliminado correctamente.") % {'name':d.name}, True)
			if request.is_ajax():
				request.path="/space/solution/index/" #/app/controller_path/action/$params
				return solution_index(request)
			else:
				return redirect('/space/solution/index/')
	except Exception, e:
		Message.error(request, e)

#endregion solution