# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Controladores para la gestión de la cuenta según el plan asignado
"""
#import datetime
#import re
import json
#from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
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
from apps.sad.security import Security, DataAccessToken
from apps.helpers.message import Message

from apps.params.models import Person
from django.contrib.auth.models import User, Group, Permission 
from django.contrib.contenttypes.models import ContentType
from apps.space.models import Headquart
from apps.sad.models import Module, Menu, UserProfileAssociation, UserProfileEnterprise, UserProfileHeadquart
from apps.space.models import Solution
from apps.home.views import choice_headquart
from django.db.models import Q
#from heapq import merge
# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
from apps.sad.upload import Upload


#region user OK
@csrf_exempt
@login_required(login_url='/account/login/')
@permission_resource_required
def user_index(request, field='username', value='None', order='-id'):
	"""
	Página principal para trabajar con usuarios
	"""
	try:
		d = get_object_or_404(Headquart, id=DataAccessToken.get_headquart_id(request.session))
	except:
		Message.error(request, ("Sede no seleccionado o no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/home/choice_headquart/" #/app/controller_path/action/$params
			return choice_headquart(request)
		else:
			return redirect('/home/choice_headquart/')

	field = (field if not request.REQUEST.get('field') else request.REQUEST.get('field')).strip()
	value = (value if not request.REQUEST.get('value') else request.REQUEST.get('value')).strip()
	order = (order if not request.REQUEST.get('order') else request.REQUEST.get('order')).strip()

	menu_page=None
	try:
		value_f = '' if value == 'None' else value
		column_contains = u"%s__%s" % (field,'contains')
		user_list = User.objects.filter(**{ column_contains: value_f }).order_by("pos").order_by(order)
		paginator = Paginator(user_list, 125)
		try:
			user_page = paginator.page(request.GET.get('page'))
		except PageNotAnInteger:
			user_page = paginator.page(1)
		except EmptyPage:
			user_page = paginator.page(paginator.num_pages)
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de usuarios"),
		'page_title':("Listado de usuarios del sistema."),
		
		'user_page':user_page,
		#'MODULES':dict((x, y) for x, y in Module.MODULES),
		'field':field,
		'value':value.replace("/", "-"),
		'order':order,
		}
	return render_to_response("sad/user/index.html", c, context_instance = RequestContext(request))



@csrf_exempt
def user_upload(request):
	"""
	Sube fotografia
	"""
	data = {}
	try:
		filename = Upload.save_file(request.FILES['fotografia'],'personas/')
		data ['name'] = "%s"%filename
	except Exception, e:
		Message.error(request, e)
	return HttpResponse(json.dumps(data))
	

@permission_resource_required
@transaction.commit_on_success
def user_add(request):
	"""
	Agrega usuario
	"""
	d = User()

	d.photo="personas/default.png"

	if request.method == "POST":
		try:
			headquart = Headquart.objects.get(id = DataAccessToken.get_headquart_id(request.session))

			d.username = request.POST.get('login')
			d.email = request.POST.get('email')
			
			d.first_name = request.POST.get('first_name')
			d.last_name = request.POST.get('last_name')
			d.photo = request.POST.get('persona_fotografia')

			print d.photo
			if User.objects.filter(username = d.username).count()>0:
				raise Exception( "El usuario <b>%s</b> ya existe " % d.username )
			if User.objects.filter(email = d.email).count()>0:
				raise Exception( "El email <b>%s</b> ya existe " % d.email )
			user = User.objects.create_user(username=d.username, email = d.email, password = request.POST.get('password'))
			user.save()

			
			if Person.objects.filter(first_name=d.first_name, last_name=d.last_name).count()>0:
				raise Exception( "La persona <b>%s %s</b> ya existe " % (d.first_name, d.last_name) )
			person = Person(user=user, first_name=d.first_name, last_name=d.last_name, photo=d.photo)
			person.save()
			d=user

			#agregando en UserProfileHeadquart
			groups_sede = request.POST.getlist('groups_sede')
			groups_sede = list(set(groups_sede))
			for value in groups_sede:
				group = Group.objects.get(id=value)
				#d.groups.add(group)
				user_profile_headquart=UserProfileHeadquart()
				user_profile_headquart.user=d
				user_profile_headquart.headquart=headquart
				user_profile_headquart.group=group
				user_profile_headquart.save()

			#agregando en UserProfileEnterprise
			groups_enterprise = request.POST.getlist('groups_enterprise')
			groups_enterprise = list(set(groups_enterprise))
			for value in groups_enterprise:
				group = Group.objects.get(id=value)
				#d.groups.add(group)
				user_profile_enterprise=UserProfileEnterprise()
				user_profile_enterprise.user=d
				user_profile_enterprise.enterprise=headquart.enterprise
				user_profile_enterprise.group=group
				user_profile_enterprise.save()

			#agregando en UserProfileAssociation
			groups_association = request.POST.getlist('groups_association')
			groups_association = list(set(groups_association))
			for value in groups_association:
				group = Group.objects.get(id=value)
				#d.groups.add(group)
				user_profile_association=UserProfileAssociation()
				user_profile_association.user=d
				user_profile_association.association=headquart.association
				user_profile_association.group=group
				user_profile_association.save()

			#agregando en user_groups
			group_dist_list=list(set(groups_sede+groups_enterprise+groups_association))
			for value in group_dist_list:
				group = Group.objects.get(id=value)
				d.groups.add(group)

			if d.id:
				Message.info(request,("Usuario <b>%(name)s</b> ha sido registrado correctamente.") % {'name':d.username}, True)
				if request.is_ajax():
					request.path="/sad/user/index/" #/app/controller_path/action/$params
					return user_index(request)
				else:
					return redirect('/sad/user/index')
		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		headquart = Headquart.objects.get(id = DataAccessToken.get_headquart_id(request.session))

		solution_enterprise=Solution.objects.get(id=headquart.enterprise.solution.id )
		solution_association=Solution.objects.get(id=headquart.association.solution.id )
		module_list = Module.objects.filter(Q(solutions = solution_enterprise) | Q(solutions = solution_association) ).distinct()
		group_perm_list = Group.objects.filter(groups__in=module_list).order_by("-id").distinct() #trae los objetos relacionados sad.Module
		#print group_perm_list
		#print "====================="
		#pero hay que adornarlo de la forma Module>Group/perfil
		group_list_by_module=[]
		group_list_by_module_unique_temp=[]#solo para verificar que el Group no se repita si este está en dos o más módulos
		for module in module_list:
			for group in Group.objects.filter(groups=module).distinct():
				if len(group_list_by_module)==0:
					group_list_by_module.append({
					'group': group,
					'module': module,
					})
					group_list_by_module_unique_temp.append(group)
				else:
					if group not in group_list_by_module_unique_temp:
						group_list_by_module.append({
						'group': group,
						'module': module,
						})
						group_list_by_module_unique_temp.append(group)
		#print group_list_by_module_unique_temp

	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de usuarios"),
		'page_title':("Agregar usuario."),
		'd':d,
		'group_perm_list':group_list_by_module,
		}
	return render_to_response("sad/user/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def user_edit(request, key):
	"""
	Actualiza user
	"""
	#print settings.MEDIA_ROOT

	id=Security.is_valid_key(request, key, 'user_upd')
	if not id:
		if request.is_ajax():
			request.path="/sad/user/index/" #/app/controller_path/action/$params
			return user_index(request)
		else:
			return redirect('/sad/user/index')
	d = None
	try:
		d = get_object_or_404(User, id=id)
		try:
			person = Person.objects.get(user_id=d.id)
			if person.id:
				d.first_name = d.person.first_name
				d.last_name = d.person.last_name
				d.photo = d.person.photo
		except:
			pass
		headquart = Headquart.objects.get(id = DataAccessToken.get_headquart_id(request.session))

		#los permisos del usuario según su espacio		
		group_id_list_by_user_and_headquart = list( col['id'] for col in Group.objects.values("id").filter(userprofileheadquart__headquart__id = headquart.id, userprofileheadquart__user__id = d.id).distinct())
		group_id_list_by_user_and_enterprise = list( col['id'] for col in Group.objects.values("id").filter(userprofileenterprise__enterprise__id = headquart.enterprise.id, userprofileenterprise__user__id = d.id).distinct())
		group_id_list_by_user_and_association = list( col['id'] for col in Group.objects.values("id").filter(userprofileassociation__association__id = headquart.association.id, userprofileassociation__user__id = d.id).distinct())

		
	except Exception, e:
		Message.error(request, ("Usuario no se encuentra en la base de datos. %s" % e))
		if request.is_ajax():
			request.path="/sad/user/index/" #/app/controller_path/action/$params
			return user_index(request)
		else:
			return redirect('/sad/user/index')

	if request.method == "POST":
		try:
			d.username = request.POST.get('login')
			
			if User.objects.filter(username = d.username).exclude(id = d.id).count()>0:
				raise Exception( "El usuario <b>%s</b> ya existe " % d.username )

			if request.POST.get('email'):
				d.email = request.POST.get('email')
				if User.objects.filter(email = d.email).exclude(id = d.id).count()>0:
					raise Exception( "El email <b>%s</b> ya existe " % d.email )
			if request.POST.get('password'):
				d.set_password(request.POST.get('password'))
			d.save()

			#form = ImageUploadForm(request.POST, request.FILES)
			#d.photo = request.FILES['imagen2']
			d.first_name = request.POST.get('first_name')
			d.last_name = request.POST.get('last_name')

			if Person.objects.filter(first_name=d.first_name, last_name=d.last_name).exclude(id = d.person.id).count()>0:
				raise Exception( "La persona <b>%s %s</b> ya existe " % (d.first_name, d.last_name) )
			person = Person.objects.get(user=d)
			person.first_name=d.first_name
			person.last_name=d.last_name
			
			#f = request.FILES.get('image')
			person.photo = request.POST.get('persona_fotografia')
			person.save()
			

			#Elimino los antiguos privilegios
			group_id_list_by_user_and_hea=list(set(group_id_list_by_user_and_headquart+group_id_list_by_user_and_enterprise+group_id_list_by_user_and_association))
			
			for group_id in group_id_list_by_user_and_headquart:
				group = Group.objects.get(id=group_id)
				user_profile_headquart=UserProfileHeadquart.objects.get(user_id=d.id, group_id=group_id,headquart_id=headquart.id)
				user_profile_headquart.delete()

			for group_id in group_id_list_by_user_and_enterprise:
				group = Group.objects.get(id=group_id)
				user_profile_enterprise=UserProfileEnterprise.objects.get(user_id=d.id, group_id=group_id,enterprise_id=headquart.enterprise.id)
				user_profile_enterprise.delete()

			for group_id in group_id_list_by_user_and_association:
				group = Group.objects.get(id=group_id)
				user_profile_association=UserProfileAssociation.objects.get(user_id=d.id, group_id=group_id,association_id=headquart.association.id)
				user_profile_association.delete()

			for group_id in  group_id_list_by_user_and_hea:
				group = Group.objects.get(id=group_id)
				d.groups.remove(group)

			#agregando en UserProfileHeadquart
			groups_sede = request.POST.getlist('groups_sede')
			groups_sede = list(set(groups_sede))
			for value in groups_sede:
				group = Group.objects.get(id=value)
				#d.groups.add(group)
				user_profile_headquart=UserProfileHeadquart()
				user_profile_headquart.user=d
				user_profile_headquart.headquart=headquart
				user_profile_headquart.group=group
				user_profile_headquart.save()

			#agregando en UserProfileEnterprise
			groups_enterprise = request.POST.getlist('groups_enterprise')
			groups_enterprise = list(set(groups_enterprise))
			for value in groups_enterprise:
				group = Group.objects.get(id=value)
				#d.groups.add(group)
				user_profile_enterprise=UserProfileEnterprise()
				user_profile_enterprise.user=d
				user_profile_enterprise.enterprise=headquart.enterprise
				user_profile_enterprise.group=group
				user_profile_enterprise.save()

			#agregando en UserProfileAssociation
			groups_association = request.POST.getlist('groups_association')
			groups_association = list(set(groups_association))
			for value in groups_association:
				group = Group.objects.get(id=value)
				#d.groups.add(group)
				user_profile_association=UserProfileAssociation()
				user_profile_association.user=d
				user_profile_association.association=headquart.association
				user_profile_association.group=group
				user_profile_association.save()

			#agregando en user_groups
			group_dist_list=list(set(groups_sede+groups_enterprise+groups_association))
			for value in group_dist_list:
				group = Group.objects.get(id=value)
				d.groups.add(group)

			if d.id:
				Message.info(request,("Usuario <b>%(name)s</b> ha sido actualizado correctamente.") % {'name':d.username}, True)
				if request.is_ajax():
					request.path="/sad/user/index/" #/app/controller_path/action/$params
					return user_index(request)
				else:
					return redirect('/sad/user/index')

		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		

		solution_enterprise=Solution.objects.get(id=headquart.enterprise.solution.id )
		solution_association=Solution.objects.get(id=headquart.association.solution.id )
		module_list = Module.objects.filter(Q(solutions = solution_enterprise) | Q(solutions = solution_association) ).distinct()
		group_perm_list = Group.objects.filter(groups__in=module_list).order_by("-id").distinct() #trae los objetos relacionados a sad.Module
		#print group_perm_list
		#print "=====================x"
		#pero hay que adornarlo de la forma Module>Group
		group_list_by_module=[]
		group_list_by_module_unique_temp=[]#solo para verificar que el Group no se repita si este está en dos o más módulos
		for module in module_list:
			for group in Group.objects.filter(groups=module).distinct():
				if len(group_list_by_module)==0:
					group_list_by_module.append({
					'group': group,
					'module': module,
					})
					group_list_by_module_unique_temp.append(group)
				else:
					if group not in group_list_by_module_unique_temp:
						group_list_by_module.append({
						'group': group,
						'module': module,
						})
						group_list_by_module_unique_temp.append(group)
		#print group_list_by_module_unique_temp
		
		

	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de usuarios"),
		'page_title':("Actualizar usuario."),
		'd':d,
		'group_perm_list':group_list_by_module,
		'group_id_list_by_user_and_headquart':group_id_list_by_user_and_headquart,
		'group_id_list_by_user_and_enterprise':group_id_list_by_user_and_enterprise,
		'group_id_list_by_user_and_association':group_id_list_by_user_and_association,
		}
	return render_to_response("sad/user/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def user_profile(request):
	"""
	Actualiza perfil del usuario
	"""
	d = None
	try:
		d = request.user
		try:
			person = Person.objects.get(user_id=d.id)
			if person.id:
				d.first_name = d.person.first_name
				d.last_name = d.person.last_name
				d.photo = d.person.photo
		except:
			pass
		
	except Exception, e:
		Message.error(request, ("Usuario no se encuentra en la base de datos. %s" % e))
		

	if request.method == "POST":
		try:
			#d.username = request.POST.get('login')
			
			#if User.objects.filter(username = d.username).exclude(id = d.id).count()>0:
			#	raise Exception( "El usuario <b>%s</b> ya existe " % d.username )

			if request.POST.get('email'):
				d.email = request.POST.get('email')
				if User.objects.filter(email = d.email).exclude(id = d.id).count()>0:
					raise Exception( "El email <b>%s</b> ya existe " % d.email )
			if request.POST.get('password'):
				d.set_password(request.POST.get('password'))
			d.save()

			d.first_name = request.POST.get('first_name')
			d.last_name = request.POST.get('last_name')
			d.photo = request.POST.get('persona_fotografia')

			if Person.objects.filter(first_name=d.first_name, last_name=d.last_name).exclude(id = d.person.id).count()>0:
				raise Exception( "La persona <b>%s %s</b> ya existe " % (d.first_name, d.last_name) )
			person = Person.objects.get(user=d)
			person.first_name=d.first_name
			person.last_name=d.last_name
			person.photo = d.photo
			person.save()
			

			

			if d.id:
				Message.info(request,("Usuario <b>%(name)s</b> ha sido actualizado correctamente.") % {'name':d.username}, True)
				if request.is_ajax():
					request.path="/home/choice_headquart/" #/app/controller_path/action/$params
					return choice_headquart(request)
				else:
					return redirect('/home/choice_headquart/')

		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		headquart = Headquart.objects.get(id = DataAccessToken.get_headquart_id(request.session))
		headquart_list_by_user_profile_headquart = Headquart.objects.filter(id__in= UserProfileHeadquart.objects.values("headquart_id").filter(user=d).distinct())

		user_profile_headquart_list = UserProfileHeadquart.objects.filter(user=d).order_by("headquart")
		user_profile_enterprise_list = UserProfileEnterprise.objects.filter(user=d).order_by("enterprise")
		user_profile_association_list = UserProfileAssociation.objects.filter(user=d).order_by("association")

		#for user_profile_headquart in user_profile_headquart_list:
		#	print user_profile_headquart.headquart
		#	print user_profile_headquart.group


		solution_enterprise=Solution.objects.get(id=headquart.enterprise.solution.id )
		solution_association=Solution.objects.get(id=headquart.association.solution.id )
		module_list = Module.objects.filter(Q(solutions = solution_enterprise) | Q(solutions = solution_association) ).distinct()
		group_perm_list = Group.objects.filter(groups__in=module_list).order_by("-id").distinct() #trae los objetos relacionados sad.Module
		#print group_perm_list
		#print "=====================x"
		#pero hay que adornarlo de la forma Module>Group/perfil
		group_list_by_module=[]
		group_list_by_module_unique_temp=[]#solo para verificar que el Group no se repita si este está en dos o más módulos
		for module in module_list:
			for group in Group.objects.filter(groups=module).distinct():
				if len(group_list_by_module)==0:
					group_list_by_module.append({
					'group': group,
					'module': module,
					})
					group_list_by_module_unique_temp.append(group)
				else:
					if group not in group_list_by_module_unique_temp:
						group_list_by_module.append({
						'group': group,
						'module': module,
						})
						group_list_by_module_unique_temp.append(group)
		#print group_list_by_module_unique_temp
		
		

	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de usuarios"),
		'page_title':("Actualizar información del usuario."),
		'd':d,
		'user_profile_headquart_list':user_profile_headquart_list,
		'user_profile_enterprise_list':user_profile_enterprise_list,
		'user_profile_association_list':user_profile_association_list,
		}
	return render_to_response("sad/user/profile.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def user_delete(request, key):
	"""
	Elimina usuario
	"""
	id=Security.is_valid_key(request, key, 'user_del')
	if not id:
		if request.is_ajax():
			request.path="/sad/user/index/" #/app/controller_path/action/$params
			return user_index(request)
		else:
			return redirect('/sad/user/index')
	try:
		d = get_object_or_404(User, id=id)
	except:
		Message.error(request, ("Usuario no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/sad/user/index/" #/app/controller_path/action/$params
			return user_index(request)
		else:
			return redirect('/sad/user/index')
	try:
		d.delete()
		if not d.id:
			Message.info(request,("Usuario <b>%(username)s</b> ha sido eliminado correctamente.") % {'username':d.username}, True)
			if request.is_ajax():
				request.path="/sad/user/index/" #/app/controller_path/action/$params
				return user_index(request)
			else:
				return redirect('/sad/user/index')
	except Exception, e:
		Message.error(request, e)
		if request.is_ajax():
			request.path="/sad/user/index/" #/app/controller_path/action/$params
			return user_index(request)
		else:
			return redirect('/sad/user/index')

def user_view(request, key):
	"""
	Visualiza información del usuario
	"""
	id=Security.is_valid_key(request, key, 'user_viw')
	if not id:
		if request.is_ajax():
			request.path="/sad/user/index/" #/app/controller_path/action/$params
			return user_index(request)
		else:
			return redirect('/sad/user/index')
	d = None
	try:
		d = get_object_or_404(User, id=id)
		try:
			person = Person.objects.get(user_id=d.id)
			if person.id:
				d.first_name = d.person.first_name
				d.last_name = d.person.last_name
		except:
			pass
		


	except Exception, e:
		Message.error(request, ("Usuario no se encuentra en la base de datos. %s" % e))
		if request.is_ajax():
			request.path="/sad/user/index/" #/app/controller_path/action/$params
			return user_index(request)
		else:
			return redirect('/sad/user/index')

	
	try:
		headquart = Headquart.objects.get(id = DataAccessToken.get_headquart_id(request.session))
		headquart_list_by_user_profile_headquart = Headquart.objects.filter(id__in= UserProfileHeadquart.objects.values("headquart_id").filter(user=d).distinct())

		user_profile_headquart_list = UserProfileHeadquart.objects.filter(user=d).order_by("headquart")
		user_profile_enterprise_list = UserProfileEnterprise.objects.filter(user=d).order_by("enterprise")
		user_profile_association_list = UserProfileAssociation.objects.filter(user=d).order_by("association")

		#for user_profile_headquart in user_profile_headquart_list:
		#	print user_profile_headquart.headquart
		#	print user_profile_headquart.group


		solution_enterprise=Solution.objects.get(id=headquart.enterprise.solution.id )
		solution_association=Solution.objects.get(id=headquart.association.solution.id )
		module_list = Module.objects.filter(Q(solutions = solution_enterprise) | Q(solutions = solution_association) ).distinct()
		group_perm_list = Group.objects.filter(groups__in=module_list).order_by("-id").distinct() #trae los objetos relacionados sad.Module
		#print group_perm_list
		#print "=====================x"
		#pero hay que adornarlo de la forma Module>Group/perfil
		group_list_by_module=[]
		group_list_by_module_unique_temp=[]#solo para verificar que el Group no se repita si este está en dos o más módulos
		for module in module_list:
			for group in Group.objects.filter(groups=module).distinct():
				if len(group_list_by_module)==0:
					group_list_by_module.append({
					'group': group,
					'module': module,
					})
					group_list_by_module_unique_temp.append(group)
				else:
					if group not in group_list_by_module_unique_temp:
						group_list_by_module.append({
						'group': group,
						'module': module,
						})
						group_list_by_module_unique_temp.append(group)
		#print group_list_by_module_unique_temp
		
		

	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de usuarios"),
		'page_title':("Información del usuario."),
		'd':d,
		'user_profile_headquart_list':user_profile_headquart_list,
		'user_profile_enterprise_list':user_profile_enterprise_list,
		'user_profile_association_list':user_profile_association_list,
		}
	return render_to_response("sad/user/view.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def user_state(request, state, key):
	"""
	Inactiva y reactiva el estado del usuario
	"""
	id=Security.is_valid_key(request, key, 'user_%s' % state )
	if not id:
		if request.is_ajax():
			request.path="/sad/user/index/" #/app/controller_path/action/$params
			return user_index(request)
		else:
			return redirect('/sad/user/index')
	try:
		d = get_object_or_404(User, id=id)
	except:
		Message.error(request, ("Usuario no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/sad/user/index/" #/app/controller_path/action/$params
			return user_index(request)
		else:
			return redirect('/sad/user/index')
	try:
		if state == "inactivar" and d.is_active == False:
			Message.error(request, ("El usuario ya se encuentra inactivo."))
		else:
			if state == "reactivar" and d.is_active == True:
				Message.error(request, ("El usuario ya se encuentra activo."))
			else:
				d.is_active = (True if state == "reactivar" else False)
				d.save()
				if d.id:
					if d.is_active:
						Message.info(request,("Usuario <b>%(username)s</b> ha sido reactivado correctamente.") % {'username':d.username}, True)
					else:
						Message.info(request,("Usuario <b>%(username)s</b> ha sido inactivado correctamente.") % {'username':d.username}, True)
					if request.is_ajax():
						request.path="/sad/user/index/" #/app/controller_path/action/$params
						return user_index(request)
					else:
						return redirect('/sad/user/index')
	except Exception, e:
		Message.error(request, e)
		if request.is_ajax():
			request.path="/sad/user/index/" #/app/controller_path/action/$params
			return user_index(request)
		else:
			return redirect('/sad/user/index')

#endregion user


#region menu OK
@csrf_exempt
@login_required(login_url='/account/login/')
@permission_resource_required
def menu_index(request, field='title', value='None', order='pos'):
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
		menu_list = Menu.objects.filter(**{ column_contains: value_f }).order_by("module",order)
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
		#'MODULES':dict((x, y) for x, y in Module.MODULES),
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
			d.url = ("#" if not request.REQUEST.get('url') else request.REQUEST.get('url')).strip()
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
	if d.id <= 16:
		Message.warning(request, ("Lo sentimos, pero este menú no se puede editar."))
		if request.is_ajax():
			request.path="/sad/menu/index/" #/app/controller_path/action/$params
			return menu_index(request)
		else:
			return redirect('/sad/menu/index')
	if request.method == "POST":
		try:
			d.title = request.POST.get('title')
			d.url = ("#" if not request.REQUEST.get('url') else request.REQUEST.get('url')).strip()
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
	if d.id <= 16:
		Message.warning(request, ("Lo sentimos, pero este menú no se puede eliminar."))
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
		if request.is_ajax():
			request.path="/sad/menu/index/" #/app/controller_path/action/$params
			return menu_index(request)
		else:
			return redirect('/sad/menu/index')
	#endregion Menu
#endregion menu




#region module OK
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

			Message.info(request, ("Los planes se han actualizados correctamente!") )
		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		module_list = Module.objects.all().order_by("module")
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
	try:
		module_list = Module.objects.all().order_by("module", "-id")
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de módulos"),
		'page_title':("Listado de módulos del sistema."),
		'module_list':module_list,
		#'MODULES':dict((x, y) for x, y in Module.MODULES),
		'html':'<b>paragraph</b>',
		}
	return render_to_response("sad/module/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
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
			transaction.rollback()
			Message.error(request, e)
	try:
		group_list = Group.objects.all().order_by("name")
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
@transaction.commit_on_success
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
			transaction.rollback()
			Message.error(request, e)
	try:
		group_list = Group.objects.all().order_by("-id")
		old_grupos_id_list = list({i.id: i for i in d.groups.all()})
		old_initial_groups_id_list = list({i.id: i for i in d.initial_groups.all()})
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
		#rastreando dependencias
		if d.solutions.count() > 0:
			raise Exception( ("Módulo <b>%(name)s</b> está asignado en planes.") % {'name':d.name} )

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
		if request.is_ajax():
			request.path="/sad/module/index/" #/app/controller_path/action/$params
			return module_index(request)
		else:
			return redirect('/sad/module/index/')
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
		'page_title':("Agregar perfil (en django.contrib.auth.models.Group)."),
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
		#rastreando dependencias
		if d.permissions.count() > 0:
			raise Exception( ("Perfil <b>%(name)s</b> tiene permisos asignados.") % {'name':d.name} )
		if d.groups.count() > 0:
			raise Exception( ("Perfil <b>%(name)s</b> está asignado en módulos.") % {'name':d.name} )
		if d.initial_groups.count() > 0:
			raise Exception( ("Perfil <b>%(name)s</b> está asignado en módulos iniciales.") % {'name':d.name} )
		if d.user_set.count() > 0:
			raise Exception( ("Perfil <b>%(name)s</b> está asignado en usuarios.") % {'name':d.name} )
		if d.userprofileassociation_set.count() > 0:
			raise Exception( ("Perfil <b>%(name)s</b> está asignado en userprofileassociation.") % {'name':d.name} )
		if d.userprofileenterprise_set.count() > 0:
			raise Exception( ("Perfil <b>%(name)s</b> está asignado en userprofileenterprise.") % {'name':d.name} )
		if d.userprofileheadquart_set.count() > 0:
			raise Exception( ("Perfil <b>%(name)s</b> está asignado en userprofileheadquart.") % {'name':d.name} )

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
		if request.is_ajax():
			request.path="/sad/group/index/" #/app/controller_path/action/$params
			return group_index(request)
		else:
			return redirect('/sad/group/index/')

@login_required(login_url='/account/login/')
@permission_resource_required
@transaction.commit_on_success
def group_permissions_edit(request):
	"""
	Actualiza permisos(recursos) por grupo(perfil) de usuario en django.contrib.auth.models.Group.permissions.add(recurso)
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
			transaction.rollback()
			Message.error(request, e)
	try:
		resource_list = Permission.objects.all().order_by("content_type__app_label","content_type__model")
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
		resource_list = Permission.objects.all().order_by("content_type__app_label","content_type__model")
	except Exception, e:
		Message.error(request, e)
	c = {
		'page_module':("Gestión de recursos"),
		'page_title':("Listado de recursos del sistema (django.contrib.auth.models.Permission)."),
		'resource_list':resource_list,
		}
	return render_to_response("sad/resource/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
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

			codename=""
			recurso="/%s/" % d.app_label.lower()
			if d.controller_view and d.action_view:
				codename="%s_%s" % (d.controller_view.lower(), d.action_view.lower())
				recurso="/%s/%s/%s/" % (d.app_label.lower(), d.controller_view.lower(), d.action_view.lower())
			if d.controller_view and not d.action_view:
				codename="%s" % (d.controller_view.lower())
				recurso="/%s/%s/" % (d.app_label.lower(), d.controller_view.lower())
			if not d.controller_view and d.action_view:
				raise Exception( ("Complete controlador para la acción <b>%(action)s</b>.") % {'action':d.action_view})
			d.codename = codename
			d.name = request.POST.get('description')
			d.content_type = content_type
			if Permission.objects.filter(codename = d.codename, content_type=content_type).exclude(id = d.id).count() > 0:
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
			transaction.rollback()
			Message.error(request, e)
	c = {
		'page_module':("Gestión de recursos"),
		'page_title':("Agregar recurso (en django.contrib.contenttypes.models.ContentType y django.contrib.auth.models.Permission)."),
		'd':d,
		}
	return render_to_response("sad/resource/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
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

	if d.id <= 19:
		Message.warning(request, ("Lo sentimos, pero este recurso no se puede editar."))
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

			codename=""
			recurso="/%s/" % d.app_label.lower()
			if d.controller_view and d.action_view:
				codename="%s_%s" % (d.controller_view.lower(), d.action_view.lower())
				recurso="/%s/%s/%s/" % (d.app_label.lower(), d.controller_view.lower(), d.action_view.lower())
			if d.controller_view and not d.action_view:
				codename="%s" % (d.controller_view.lower())
				recurso="/%s/%s/" % (d.app_label.lower(), d.controller_view.lower())
			if not d.controller_view and d.action_view:
				raise Exception( ("Complete controlador para la acción <b>%(action)s</b>.") % {'action':d.action_view})
			d.codename = codename
			d.name = request.POST.get('description')
			d.content_type = content_type

			if Permission.objects.filter(codename = d.codename, content_type=content_type).exclude(id = d.id).count() > 0:
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
			transaction.rollback()
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
		recurso="/%s/" % d.content_type.app_label
		if d.codename:
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

	if d.id <= 19:
		Message.warning(request, ("Lo sentimos, pero este recurso no se puede eliminar."))
		if request.is_ajax():
			request.path="/sad/resource/index/" #/app/controller_path/action/$params
			return resource_index(request)
		else:
			return redirect('/sad/resource/index/')
	try:
		#rastreando dependencias
		if d.group_set.count() > 0:
			raise Exception( ("Recurso <b>%(recurso)s</b> está asignado en perfiles.") % {'recurso':recurso} )
		if d.menu_set.count() > 0:
			raise Exception( ("Recurso <b>%(recurso)s</b> está asignado en menús.") % {'recurso':recurso} )
		if d.user_set.count() > 0:
			raise Exception( ("Recurso <b>%(recurso)s</b> está asignado en usuarios.") % {'recurso':recurso} )

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
		if request.is_ajax():
			request.path="/sad/resource/index/" #/app/controller_path/action/$params
			return resource_index(request)
		else:
			return redirect('/sad/resource/index/')
#endregion resource