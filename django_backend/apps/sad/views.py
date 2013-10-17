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
from apps.space.models import Headquart
from apps.sad.models import *



#region menu
@csrf_exempt
@login_required(login_url='/account/login/')
@permission_resource_required
def menu_index(request, field='title', value='None', order='-module'):
	"""
	Página principal para trabajar con menús dinámicos
	"""
	field = (field if not request.REQUEST.get('field') else request.REQUEST.get('field')).strip()
	value = (value if not request.REQUEST.get('value') else request.REQUEST.get('value')).strip()
	order = (order if not request.REQUEST.get('order') else request.REQUEST.get('order')).strip()

	menu_page=None
	try:
		value_f = '' if value == 'None' else value
		column_contains = u"%s__%s" % (field,'contains')
		menu_list = Menu.objects.filter(**{ column_contains: value_f }).order_by("pos").order_by(order)
		paginator = Paginator(menu_list, 125)
		try:
			menu_page = paginator.page(request.GET.get('page'))
		except PageNotAnInteger:
			menu_page = paginator.page(1)
		except EmptyPage:
			menu_page = paginator.page(paginator.num_pages)
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de menús"),
		'page_title':("Listado de menús del sistema."),
		
		'menu_page':menu_page,
		'MODULES':dict((x, y) for x, y in Module.MODULES),
		'field':field,
		'value':value.replace("/", "-"),
		'order':order,
		}
	return render_to_response("sad/menu/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
def menu_add(request):
	d = Menu()
	if request.method == "POST":
		try:
			#Aquí asignar los datos
			d.title = request.POST.get('title')
			d.url = request.POST.get('url')
			d.icon = request.POST.get('icon')
			d.pos = request.POST.get('pos')
			d.module = request.POST.get('module')
			if request.POST.get('permission_id'):
				d.permission_id = Permission.objects.get(id=request.POST.get('permission_id')).id

			if request.POST.get('parent_id'):
				d.parent_id = Menu.objects.get(id=request.POST.get('parent_id')).id

			#if Menu.objects.filter(title = d.title).exclude(id = d.id).count() > 0:
			#	raise Exception( ("Menu <b>%(name)s</b> ya existe.") % {'name':d.title} )

			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Menu <b>%(name)s</b> ha sido registrado correctamente.") % {'name':d.title}, True)
				if request.is_ajax():
					request.path="/sad/menu/index/" #/app/controller_path/action/$params
					return menu_index(request)
				else:
					return redirect('/sad/menu/index')
		except Exception, e:
			Message.error(request, e)
	try:
		parent_list = Menu.objects.filter(parent_id=None)
		permission_list = Permission.objects.all()

	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de menús"),
		'page_title':("Agregar menú."),
		'd':d,
		'MODULES':Menu.MODULES,
		'MODULES_DICT':dict((x, y) for x, y in Module.MODULES),
		'parent_list':parent_list,
		'permission_list':permission_list,
		}
	return render_to_response("sad/menu/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
def menu_edit(request, key):
	"""
	Actualiza menú
	"""
	id=Security.is_valid_key(request, key, 'menu_upd')
	if not id:
		if request.is_ajax():
			request.path="/sad/menu/index/" #/app/controller_path/action/$params
			return menu_index(request)
		else:
			return redirect('/sad/menu/index')
	d = None
	try:
		d = get_object_or_404(Menu, id=id)
	except:
		Message.error(request, ("Menu no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/sad/menu/index/" #/app/controller_path/action/$params
			return menu_index(request)
		else:
			return redirect('/sad/menu/index')

	if request.method == "POST":
		try:
			d.title = request.POST.get('title')
			d.url = request.POST.get('url')
			d.icon = request.POST.get('icon')
			d.pos = request.POST.get('pos')
			d.module = request.POST.get('module')
			if d.permission:
				d.permission=None
			if request.POST.get('permission_id'):
				d.permission_id = Permission.objects.get(id=request.POST.get('permission_id')).id

			if d.parent:
				d.parent=None
			if request.POST.get('parent_id'):
				d.parent_id = Menu.objects.get(id=request.POST.get('parent_id')).id

			#if Menu.objects.filter(title = d.title).exclude(id = d.id).count() > 0:
			#	raise Exception( ("Menu <b>%(name)s</b> ya existe.") % {'name':d.title} )

			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Menu <b>%(name)s</b> ha sido actualizado correctamente.") % {'name':d.title})
				if request.is_ajax():
					request.path="/sad/menu/index/" #/app/controller_path/action/$params
					return menu_index(request)
				else:
					return redirect('/sad/menu/index')

		except Exception, e:
			Message.error(request, e)
	try:
		parent_list = Menu.objects.filter(parent_id=None)
		permission_list = Permission.objects.all()

	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de menús"),
		'page_title':("Actualizar menú."),
		'd':d,
		'MODULES':Menu.MODULES,
		'MODULES_DICT':dict((x, y) for x, y in Module.MODULES),
		'parent_list':parent_list,
		'permission_list':permission_list,
		}
	return render_to_response("sad/menu/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
def menu_delete(request, key):
	"""
	Elimina menú
	"""
	id=Security.is_valid_key(request, key, 'menu_del')
	if not id:
		if request.is_ajax():
			request.path="/sad/menu/index/" #/app/controller_path/action/$params
			return menu_index(request)
		else:
			return redirect('/sad/menu/index')
	try:
		d = get_object_or_404(Menu, id=id)
	except:
		Message.error(request, ("Menu no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/sad/menu/index/" #/app/controller_path/action/$params
			return menu_index(request)
		else:
			return redirect('/sad/menu/index')
	try:
		d.delete()
		if not d.id:
			Message.info(request,("Menu <b>%(name)s</b> ha sido eliminado correctamente.") % {'name':d.title}, True)
			if request.is_ajax():
				request.path="/sad/menu/index/" #/app/controller_path/action/$params
				return menu_index(request)
			else:
				return redirect('/sad/menu/index')
	except Exception, e:
		Message.error(request, e)
	#endregion Menu





#region Module OK
@login_required(login_url='/account/login/')
@permission_resource_required
@transaction.commit_on_success
def module_plans_edit(request):
	if request.method == "POST":
		try:
			
			privilegios_r = request.POST.getlist('privilegios')
			old_privilegios_r = request.POST.get('old_privilegios')
			if old_privilegios_r:
				old_privilegios_r = old_privilegios_r.split(',')

			#Elimino los antiguos privilegios
			for value in  old_privilegios_r:
				data = value.split('-') #el formato es 1-4 = solution_id-module_id
				module = Module.objects.get(id=data[1])
				solution = Solution.objects.get(id=data[0])
				module.solutions.remove(solution)
			
			for value in  privilegios_r:
				data = value.split('-') #el formato es 1-4 = solution_id-module_id
				module = Module.objects.get(id=data[1])
				solution = Solution.objects.get(id=data[0])
				module.solutions.add(solution)

			Message.info(request, ("Las soluciones se han actualizados correctamente!") )
		except Exception, e:
			Message.error(request, e)
	try:
		module_list = Module.objects.all().order_by("-id")
		solution_list = Solution.objects.all().order_by("-id")

		#listar los privilegios y compararlos con los module y solution
		privilegios=[]
		for m in module_list:
			for s in m.solutions.all() :
				privilegios.append( "%s-%s" % (s.id, m.id) ) #el formato es 1-4 = solution_id-module_id

		#for i in privilegios:
		#	print u"%s" % (i)
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de planes"),
		'page_title':("Listado de planes del sistema."),
		'module_list':module_list,
		'module_list_len':len(module_list),
		'solution_list':solution_list,
		'solution_list_len':len(solution_list),
		'privilegios':privilegios,
		}
	return render_to_response("sad/module/module_plans_edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
def module_index(request):
	"""
	Página principal para trabajar con módulos del sistema (CRUD a la tabla sad_module)
	"""
	#Message.error(request, "thev '<b>ee</b>' is manu")
	try:
		module_list = Module.objects.all().order_by("module")
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de módulos"),
		'page_title':("Listado de módulos del sistema."),
		'module_list':module_list,
		'MODULES':dict((x, y) for x, y in Module.MODULES),
		'html':'<b>paragraph</b>',
		}
	return render_to_response("sad/module/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
def module_add(request):
	"""
	Agrega módulo
	"""
	d = Module()
	d.description=""
	if request.method == "POST":
		try:
			d.module = request.POST.get('module')
			d.name = request.POST.get('name')
			d.description = request.POST.get('description')
			if Module.objects.filter(name = d.name).exclude(id = d.id).count() > 0:
				raise Exception( ("Modulo <b>%(name)s</b> ya existe.") % {'name':d.name} )
			d.save()

			groups = request.POST.getlist('groups')
			for value in groups:
				group = Group.objects.get(id=value)
				d.groups.add(group)
			
			initial_groups = request.POST.getlist('initial_groups')
			for value in initial_groups:
				group = Group.objects.get(id=value)
				d.initial_groups.add(group)

			
			
			if d.id:
				Message.info(request,("Modulo <b>%(name)s</b> ha sido registrado correctamente.") % {'name':d.name})
				if request.is_ajax():
					request.path="/sad/module/index/" #/app/controller_path/action/$params
					return module_index(request)
				else:
					return redirect('/sad/module/index/')
		except Exception, e:
			Message.error(request, e)
	try:
		group_list = Group.objects.all().order_by("-id")
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de módulos"),
		'page_title':("Agregar módulo."),
		'd':d,
		'group_list':group_list,
		'MODULES':Module.MODULES,
		}
	return render_to_response("sad/module/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
def module_edit(request, key):
	"""
	Actualiza módulo
	"""
	id=Security.is_valid_key(request, key, 'module_upd')
	if not id:
		if request.is_ajax():
			request.path="/sad/module/index/" #/app/controller_path/action/$params
			return module_index(request)
		else:
			return redirect('/sad/module/index/')
	d = None
	try:
		d = get_object_or_404(Module, id=id)
	except:
		Message.error(request, ("Módulo no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/sad/module/index/" #/app/controller_path/action/$params
			return module_index(request)
		else:
			return redirect('/sad/module/index/')

	if request.method == "POST":
		try:
			d.module = request.POST.get('module')
			d.name = request.POST.get('name')
			d.description = request.POST.get('description')
			if Module.objects.filter(name = d.name).exclude(id = d.id).count() > 0:
				raise Exception( ("Modulo <b>%(name)s</b> ya existe.") % {'name':d.name} )
			d.save()

			old_grupos_id_list_r = request.POST.get('old_grupos_id_list')
			if old_grupos_id_list_r:
				old_grupos_id_list_r = old_grupos_id_list_r.split(',')

			#Elimino los antiguos privilegios
			for value in  old_grupos_id_list_r:
				group = Group.objects.get(id=value)
				d.groups.remove(group)

			groups = request.POST.getlist('groups')
			for value in groups:
				group = Group.objects.get(id=value)
				d.groups.add(group)
			
			old_initial_groups_id_list_r = request.POST.get('old_initial_groups_id_list')
			if old_initial_groups_id_list_r:
				old_initial_groups_id_list_r = old_initial_groups_id_list_r.split(',')

			#Elimino los antiguos privilegios
			for value in  old_initial_groups_id_list_r:
				group = Group.objects.get(id=value)
				d.initial_groups.remove(group)

			initial_groups = request.POST.getlist('initial_groups')
			for value in initial_groups:
				group = Group.objects.get(id=value)
				d.initial_groups.add(group)

			if d.id:
				Message.info(request,("Modulo <b>%(name)s</b> ha sido actualizado correctamente.") % {'name':d.name})
				if request.is_ajax():
					request.path="/sad/module/index/" #/app/controller_path/action/$params
					return module_index(request)
				else:
					return redirect('/sad/module/index/')

		except Exception, e:
			Message.error(request, e)
	try:
		group_list = Group.objects.all().order_by("-id")
		old_grupos_id_list = list({i.id: i for i in d.groups.all()})
		old_initial_groups_id_list = list({i.id: i for i in d.initial_groups.all()})
		#listar los privilegios y compararlos con los recursos(permisos) y perfiles(grupos)
		#privilegios=[]
		#for g in group_list:
		#	for p in g.permissions.all() :
		#		privilegios.append( "%s-%s" % (p.id, g.id) )

	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de módulos"),
		'page_title':("Actualizar módulo."),
		'd':d,
		'group_list':group_list,
		'MODULES':Module.MODULES,
		'old_grupos_id_list':old_grupos_id_list,
		'old_initial_groups_id_list':old_initial_groups_id_list,
		}
	return render_to_response("sad/module/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
def module_delete(request, key):
	"""
	Elimina módulo y sus dependencias
	"""
	id=Security.is_valid_key(request, key, 'module_del')
	if not id:
		if request.is_ajax():
			request.path="/sad/module/index/" #/app/controller_path/action/$params
			return module_index(request)
		else:
			return redirect('/sad/module/index/')
	try:
		d = get_object_or_404(Module, id=id)
	except:
		Message.error(request, ("Módulo no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/sad/module/index/" #/app/controller_path/action/$params
			return module_index(request)
		else:
			return redirect('/sad/module/index/')
	try:
		d.delete() # las dependencias grupos e initial_groups se eliminan automáticamente
		if not d.id:
			Message.info(request,("Módulo <b>%(name)s</b> ha sido eliminado correctamente.") % {'name':d.name}, True)
			if request.is_ajax():
				request.path="/sad/module/index/" #/app/controller_path/action/$params
				return module_index(request)
			else:
				return redirect('/sad/module/index/')
	except Exception, e:
		Message.error(request, e)

#endregion module







#region group OK
@permission_resource_required
def group_index(request):
	"""
	Página principal para trabajar con perfiles o grupo de usuarios (CRUD a la tabla Group de django.contrib.auth.models)
	"""
	try:
		group_list = Group.objects.all().order_by("-id")
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de perfiles"),
		'page_title':("Listado de perfiles de usuario."),
		'group_list':group_list,
		}
	return render_to_response("sad/group/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
def group_add(request):
	"""
	Agrega perfil o grupo de usuarios en django.contrib.auth.models.Group
	"""
	d = Group()

	if request.method == "POST":
		try:
			d.name = request.POST.get('name')
			if Group.objects.filter(name = d.name).exclude(id = d.id).count() > 0:
				raise Exception( ("Perfil <b>%(name)s</b> ya existe.") % {'name':d.name} )
			d.save()
			if d.id:
				Message.info(request,("Perfil <b>%(name)s</b> ha sido registrado correctamente.") % {'name':d.name})
				if request.is_ajax():
					request.path="/sad/group/index/" #/app/controller_path/action/$params
					return group_index(request)
				else:
					return redirect('/sad/group/index/')
		except Exception, e:
			Message.error(request, e)
	c = {
		'page_module':("Gestión de perfiles"),
		'page_title':("Agregar perfil (en django.contrib.contenttypes.models.ContentType y django.contrib.auth.models.Permission)."),
		'd':d,
		}
	return render_to_response("sad/group/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
def group_edit(request, key):
	"""
	Actualiza perfil o grupo de usuarios en django.contrib.auth.models.Group
	"""
	id=Security.is_valid_key(request, key, 'group_upd')
	if not id:
		if request.is_ajax():
			request.path="/sad/group/index/" #/app/controller_path/action/$params
			return group_index(request)
		else:
			return redirect('/sad/group/index/')
	d = None
	try:
		d = get_object_or_404(Group, id=id)
	except:
		Message.error(request, ("Perfil no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/sad/group/index/" #/app/controller_path/action/$params
			return group_index(request)
		else:
			return redirect('/sad/group/index/')

	if request.method == "POST":
		try:
			d.name = request.POST.get('name')
			if Group.objects.filter(name = d.name).exclude(id = d.id).count() > 0:
				raise Exception( ("Perfil <b>%(name)s</b> ya existe.") % {'name':d.name} )

			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Perfil <b>%(name)s</b> ha sido actualizado correctamente.") % {'name':d.name})
				if request.is_ajax():
					request.path="/sad/group/index/" #/app/controller_path/action/$params
					return group_index(request)
				else:
					return redirect('/sad/group/index/')

		except Exception, e:
			Message.error(request, e)
	c = {
		'page_module':("Gestión de perfiles"),
		'page_title':("Actualizar perfil."),
		'd':d,
		}
	return render_to_response("sad/group/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
def group_delete(request, key):
	"""
	Elimina perfil o grupo de usuarios de django.contrib.auth.models.Group
	"""
	id=Security.is_valid_key(request, key, 'group_del')
	if not id:
		if request.is_ajax():
			request.path="/sad/group/index/" #/app/controller_path/action/$params
			return group_index(request)
		else:
			return redirect('/sad/group/index/')
	try:
		d = get_object_or_404(Group, id=id)
	except:
		Message.error(request, ("Perfil no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/sad/group/index/" #/app/controller_path/action/$params
			return group_index(request)
		else:
			return redirect('/sad/group/index/')
	try:
		d.delete()
		if not d.id:
			Message.info(request,("Perfil <b>%(name)s</b> ha sido eliminado correctamente.") % {'name':d.name}, True)
			if request.is_ajax():
				request.path="/sad/group/index/" #/app/controller_path/action/$params
				return group_index(request)
			else:
				return redirect('/sad/group/index/')
	except Exception, e:
		Message.error(request, e)

@login_required(login_url='/account/login/')
@permission_resource_required
@transaction.commit_on_success #https://docs.djangoproject.com/en/1.5/topics/db/transactions/
def group_permissions_edit(request):
	"""
	Actualiza permisos por perfil de usuario en django.contrib.auth.models.Group.permissions.add(recurso)
	"""
	if request.method == "POST":
		try:
			
			privilegios_r = request.POST.getlist('privilegios')
			old_privilegios_r = request.POST.get('old_privilegios')
			if old_privilegios_r:
				old_privilegios_r = old_privilegios_r.split(',')

			#Elimino los antiguos privilegios
			for value in  old_privilegios_r:
				data = value.split('-') #el formato es 1-4 = recurso_id-perfil_id
				group = Group.objects.get(id=data[1])
				recur = Permission.objects.get(id=data[0])
				group.permissions.remove(recur)
			
			for value in  privilegios_r:
				data = value.split('-') #el formato es 1-4 = recurso_id-perfil_id
				group = Group.objects.get(id=data[1])
				recur = Permission.objects.get(id=data[0])
				group.permissions.add(recur)
			Message.info(request, ("Los privilegios se han actualizados correctamente!") )
		except Exception, e:
			Message.error(request, e)
	try:
		resource_list = Permission.objects.all().order_by("content_type__model").order_by("content_type__app_label")
		group_list = Group.objects.all().order_by("-id")

		#listar los privilegios y compararlos con los recursos(permisos) y perfiles(grupos)
		privilegios=[]
		for g in group_list:
			for p in g.permissions.all() :
				privilegios.append( "%s-%s" % (p.id, g.id) )
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de permisos"),
		'page_title':("Permisos y privilegios de usuarios."),
		'resource_list':resource_list,
		'resource_list_len':len(resource_list),
		'group_list':group_list,
		'group_list_len':len(group_list),
		'privilegios':privilegios,
		}
	return render_to_response("sad/permissions/group_permissions_edit.html", c, context_instance = RequestContext(request))

#endregion group








#region resource OK
@permission_resource_required
def resource_index(request):
	"""
	Página principal para trabajar con recursos (CRUD a la tabla Permission de django.contrib.auth.models)
	"""
	try:
		resource_list = Permission.objects.all().order_by("content_type__model").order_by("content_type__app_label")
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de recursos"),
		'page_title':("Listado de recursos del sistema (django.contrib.auth.models.Permission)."),
		'resource_list':resource_list,
		}
	return render_to_response("sad/resource/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
def resource_add(request):
	"""
	Agrega recurso en django.contrib.auth.models.Permission y obtiene o agrega un django.contrib.contenttypes.models.ContentType (ContentType.objects.get_or_create)
	"""
	d = Permission()

	if request.method == "POST":
		try:
			d.description = request.POST.get('description')
			d.controller_view=request.POST.get('controller_view')
			d.app_label=request.POST.get('app_label')
			d.action_view=request.POST.get('action_view')
			content_type, is_content_type_created  = ContentType.objects.get_or_create(
				name=d.controller_view.lower(), 
				model=d.controller_view.lower(), 
				app_label=d.app_label.lower(),
				)

			if d.action_view:
				codename="%s_%s" % (d.controller_view.lower(), d.action_view.lower())
				recurso="/%s/%s/%s/" % (d.app_label.lower(), d.controller_view.lower(), d.action_view.lower())
			else:
				codename="%s" % (d.controller_view.lower())
				recurso="/%s/%s/" % (d.app_label.lower(), d.controller_view.lower())
			d.codename = codename
			d.name = request.POST.get('description')
			d.content_type = content_type
			#d = Permission.objects.create(
			#	codename=codename,
			#	name=request.POST.get('description'),
			#	content_type=content_type,
			#	)
			if Permission.objects.filter(codename = d.codename).exclude(id = d.id).count() > 0:
				raise Exception( ("Recurso <b>%(recurso)s</b> ya existe.") % {'recurso':recurso})

			d.save()
			if d.id:
				Message.info(request,("Recurso %(recurso)s ha sido registrado correctamente.") % {'recurso':recurso})
				if request.is_ajax():
					request.path="/sad/resource/index/" #/app/controller_path/action/$params
					return resource_index(request)
				else:
					return redirect('/sad/resource/index/')
		except Exception, e:
			Message.error(request, e)
	c = {
		'page_module':("Gestión de recursos"),
		'page_title':("Agregar recurso (en django.contrib.contenttypes.models.ContentType y django.contrib.auth.models.Permission)."),
		'd':d,
		}
	return render_to_response("sad/resource/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
def resource_edit(request, key):
	"""
	Actualiza recurso en django.contrib.auth.models.Permission y obtiene o agrega un django.contrib.contenttypes.models.ContentType (ContentType.objects.get_or_create)
	"""
	id=Security.is_valid_key(request, key, 'resource_upd')
	if not id:
		if request.is_ajax():
			request.path="/sad/resource/index/" #/app/controller_path/action/$params
			return resource_index(request)
		else:
			return redirect('/sad/resource/index/')
	d = None
	try:
		d = get_object_or_404(Permission, id=id)
		d.controller_view=d.content_type.name
		d.app_label=d.content_type.app_label
		codename_list=d.codename.split('_',1)
		if len(codename_list) > 1:
			d.action_view=codename_list[1]
		d.description=d.name
	except:
		Message.error(request, ("Recurso no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/sad/resource/index/" #/app/controller_path/action/$params
			return resource_index(request)
		else:
			return redirect('/sad/resource/index/')

	if request.method == "POST":
		try:
			d.controller_view=request.POST.get('controller_view')
			d.app_label=request.POST.get('app_label')
			d.action_view=request.POST.get('action_view')
			content_type, is_content_type_created  = ContentType.objects.get_or_create(
				name=d.controller_view.lower(), 
				model=d.controller_view.lower(), 
				app_label=d.app_label.lower(),
				)

			if d.action_view:
				codename="%s_%s" % (d.controller_view.lower(), d.action_view.lower())
				recurso="/%s/%s/%s/" % (d.app_label.lower(), d.controller_view.lower(), d.action_view.lower())
			else:
				codename="%s" % (d.controller_view.lower())
				recurso="/%s/%s/" % (d.app_label.lower(), d.controller_view.lower())
			d.codename = codename
			d.name = request.POST.get('description')
			d.content_type = content_type

			if Permission.objects.filter(codename = d.codename).exclude(id = d.id).count() > 0:
				raise Exception( ("Recurso <b>%(recurso)s</b> ya existe.") % {'recurso':recurso})

			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Recurso <b>%(recurso)s</b> ha sido actualizado correctamente.") % {'recurso':recurso})
				if request.is_ajax():
					request.path="/sad/resource/index/" #/app/controller_path/action/$params
					return resource_index(request)
				else:
					return redirect('/sad/resource/index/')

		except Exception, e:
			Message.error(request, e)
	c = {
		'page_module':("Gestión de recursos"),
		'page_title':("Actualizar recurso."),
		'd':d,
		}
	return render_to_response("sad/resource/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
def resource_delete(request, key):
	"""
	Elimina recurso de django.contrib.auth.models.Permission
	"""
	id=Security.is_valid_key(request, key, 'resource_del')
	if not id:
		if request.is_ajax():
			request.path="/sad/resource/index/" #/app/controller_path/action/$params
			return resource_index(request)
		else:
			return redirect('/sad/resource/index/')
	try:
		d = get_object_or_404(Permission, id=id)
		recurso="/%s/%s/" % (d.content_type.app_label, d.content_type.name)
		codename_list=d.codename.split('_',1)
		if len(codename_list) > 1:
			recurso="/%s/%s/%s/" % (d.content_type.app_label, d.content_type.name, codename_list[1])
	except:
		Message.error(request, ("Recurso no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/sad/resource/index/" #/app/controller_path/action/$params
			return resource_index(request)
		else:
			return redirect('/sad/resource/index/')
	try:
		d.delete()
		if not d.id:
			Message.info(request,("Recurso <b>%(recurso)s</b> ha sido eliminado correctamente.") % {'recurso':recurso}, True)
			if request.is_ajax():
				request.path="/sad/resource/index/" #/app/controller_path/action/$params
				return resource_index(request)
			else:
				return redirect('/sad/resource/index/')
	except Exception, e:
		Message.error(request, e)
#endregion resource