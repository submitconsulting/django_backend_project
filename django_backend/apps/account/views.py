# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     account

Descripcion: Controladores para la apertura de la cuenta e inicia de sesión
"""
from django.http import HttpResponse,HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, render,redirect, Http404
from django.template import RequestContext
#from apps.account.forms import RegistrationForm, LoginForm

from django.contrib.auth import authenticate, login, logout

from apps.sad.security import DataAccessToken, Redirect

from apps.helpers.message import Message
from django.db import transaction
from django.contrib.auth.models import User, Group
#from apps.sad.models import *
from apps.params.models import Person
from apps.space.models import Association, Enterprise, Headquart, Solution
from apps.sad.models import Profile, Module, UserProfileAssociation, UserProfileEnterprise, UserProfileHeadquart
from apps.home.views import choice_headquart
from unicodedata import normalize
#from django.template.defaultfilters import slugify
from apps.sad.decorators import is_admin, permission_resource_required
from django.db.models import Q

#region registro cuenta OK
@login_required(login_url="/account/login/")
@transaction.commit_on_success
def add_enterprise(request):

	#data = "cáñété"´píñána+bâ"x"
	#https://github.com/django/django/blob/master/django/contrib/auth/management/__init__.py
	#print unicodedata.normalize("NFKD", u"%s"%data).encode("ascii", "ignore")
	#names = list(unicodedata.normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Association.objects.values("name","type_a").filter(name__contains="AS"))
	#print names
	#print slugify(u"%s"%data)
	#print data.encode("ascii", "ignore")
	#print normalize("NFKD", u"%s"%data).encode("ascii", "ignore")
	d = Enterprise()

	#solution_list = None
	if request.method == "POST":
		#with transaction.commit_manually():
		#transaction.set_autocommit(False)
		try:
			
			d.enterprise_name = request.POST.get("enterprise_name")
			d.enterprise_tax_id = request.POST.get("enterprise_tax_id")
			d.association_name = request.POST.get("association_name")
			d.association_type_a = request.POST.get("association_type_a")
			d.solution_id = request.POST.get("solution_id")
			
			solution=Solution.objects.get(id=d.solution_id)
			d.logo = request.POST.get("empresa_logo")
			user = request.user
			
			association = Association(name=d.association_name, type_a=d.association_type_a, solution=solution, logo=d.logo)
			#if Association.objects.filter(name=normalize("NFKD", u"%s" % d.association_name).encode("ascii", "ignore")).count()>0:
			if normalize("NFKD", u"%s" % d.association_name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Association.objects.values("name")
				):
				raise Exception( "La asociación <b>%s</b> ya existe " % (d.association_name) )
			association.save()

			enterprise = Enterprise(name=d.enterprise_name, tax_id=d.enterprise_tax_id, type_e=d.association_type_a, solution=solution, logo=d.logo)
			#if Enterprise.objects.filter(name=normalize("NFKD", u"%s" % d.enterprise_name).encode("ascii", "ignore")).count()>0:
			if normalize("NFKD", u"%s" % d.enterprise_name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Enterprise.objects.values("name")
				):
				raise Exception( "La empresa <b>%s</b> ya existe " % (d.enterprise_name) )
			if Enterprise.objects.filter(tax_id=d.enterprise_tax_id).count()>0:
				raise Exception( "La empresa con RUC <b>%s</b> ya existe " % (d.enterprise_tax_id) )
			enterprise.save()

			headquart = Headquart(name="Principal", association=association, enterprise=enterprise)
			headquart.save()
            
            #asigna permisos al usuario para manipular datos de cierta sede, empresa o asociación
			group_dist_list=[]
			for module in solution.module_set.all(): #.distinct()	
				for group in module.initial_groups.all() :
					if len(group_dist_list)==0 :
						group_dist_list.append(group.id)
						user.groups.add(group)
						
						user_profile_association=UserProfileAssociation()
						user_profile_association.user=user
						user_profile_association.association=association
						user_profile_association.group=group
						user_profile_association.save()

						user_profile_enterprise=UserProfileEnterprise()
						user_profile_enterprise.user=user
						user_profile_enterprise.enterprise=enterprise
						user_profile_enterprise.group=group
						user_profile_enterprise.save()
						
						user_profile_headquart=UserProfileHeadquart()
						user_profile_headquart.user=user
						user_profile_headquart.headquart=headquart
						user_profile_headquart.group=group
						user_profile_headquart.save()
					else :
						if group.id not in group_dist_list:
							group_dist_list.append(group.id)
							user.groups.add(group)

							user_profile_association=UserProfileAssociation()
							user_profile_association.user=user
							user_profile_association.association=association
							user_profile_association.group=group
							user_profile_association.save()

							user_profile_enterprise=UserProfileEnterprise()
							user_profile_enterprise.user=user
							user_profile_enterprise.enterprise=enterprise
							user_profile_enterprise.group=group
							user_profile_enterprise.save()
							
							user_profile_headquart=UserProfileHeadquart()
							user_profile_headquart.user=user
							user_profile_headquart.headquart=headquart
							user_profile_headquart.group=group
							user_profile_headquart.save()
			#transaction.commit()
			Message.info(request,("Empresa <b>%(name)s</b> ha sido registrado correctamente!.") % {"name":d.enterprise_name})
			return Redirect.to(request, "/home/choice_headquart/")
		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		type_a_list = Association.TYPES
		solution_list = Solution.objects.filter(is_active=True).order_by("id")
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Registro de empresa"),
		"page_title":("Agregar nueva empresa a la cuenta de <b>%(login)s</b>.") % {"login":request.user},
		"d":d,
		"solution_list":solution_list,
		"type_a_list":type_a_list,
		
		}
	return render_to_response("account/add_enterprise.html", c, context_instance = RequestContext(request))

@transaction.commit_on_success
def signup_sys(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/home/choice_headquart/")
	d = Person()
	d.first_name=""
	d.last_name=""
	if request.method == "POST":
		try:
			d.first_name = request.POST.get("first_name")
			d.last_name = request.POST.get("last_name")
			d.username = request.POST.get("login")
			d.enterprise_name = request.POST.get("enterprise_name")
			d.enterprise_tax_id = request.POST.get("enterprise_tax_id")
			d.association_name = request.POST.get("association_name")
			d.association_type_a = request.POST.get("association_type_a")
			d.solution_id = request.POST.get("solution_id")
			d.email = request.POST.get("email")
			d.photo = request.POST.get("persona_fotografia")
			#password = request.POST.get("password")
			#acept_term = request.POST.get("acept_term")
			solution=Solution.objects.get(id=d.solution_id)
			d.solution=solution
			if User.objects.filter(username = d.username).count()>0:
				raise Exception( "El usuario <b>%s</b> ya existe " % d.username )

			if User.objects.filter(email = d.email).count()>0:
				raise Exception( "El email <b>%s</b> ya existe " % d.email )

			user = User.objects.create_user(username=d.username, email = d.email, password = request.POST.get("password"))
			user.save()
			
			if Person.objects.filter(first_name=d.first_name, last_name=d.last_name).count()>0:
				raise Exception( "La persona <b>%s %s</b> ya existe " % (d.first_name, d.last_name) )
			
			person = Person(first_name=d.first_name, last_name=d.last_name, photo=d.photo)
			person.save()
			
			profile = Profile(user=user)
			profile.person=person
			profile.save()

			association = Association(name=d.association_name, type_a=d.association_type_a, solution=solution)
			if normalize("NFKD", u"%s" % d.association_name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Association.objects.values("name")
				):
				raise Exception( "La asociación <b>%s</b> ya existe " % (d.association_name) )
			association.save()

			enterprise = Enterprise(name=d.enterprise_name, tax_id=d.enterprise_tax_id, type_e=d.association_type_a, solution=solution )
			if normalize("NFKD", u"%s" % d.enterprise_name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Enterprise.objects.values("name")
				):
				raise Exception( "La empresa <b>%s</b> ya existe " % (d.enterprise_name) )
			if Enterprise.objects.filter(tax_id=d.enterprise_tax_id).count()>0:
				raise Exception( "La empresa con RUC <b>%s</b> ya existe " % (d.enterprise_tax_id) )
			enterprise.save()
			
			headquart = Headquart(name="Principal", association=association, enterprise=enterprise)
			
			headquart.save()
            
            #asigna permisos al usuario para manipular datos de cierta sede, empresa o asociación
			group_dist_list=[]
			for module in solution.module_set.all(): #.distinct()	
				for group in module.initial_groups.all() :
					if len(group_dist_list)==0 :
						group_dist_list.append(group.id)
						user.groups.add(group)
						
						user_profile_association=UserProfileAssociation()
						user_profile_association.user=user
						user_profile_association.association=association
						user_profile_association.group=group
						user_profile_association.save()

						user_profile_enterprise=UserProfileEnterprise()
						user_profile_enterprise.user=user
						user_profile_enterprise.enterprise=enterprise
						user_profile_enterprise.group=group
						user_profile_enterprise.save()
						
						user_profile_headquart=UserProfileHeadquart()
						user_profile_headquart.user=user
						user_profile_headquart.headquart=headquart
						user_profile_headquart.group=group
						user_profile_headquart.save()
					else :
						if group.id not in group_dist_list:
							group_dist_list.append(group.id)
							user.groups.add(group)

							user_profile_association=UserProfileAssociation()
							user_profile_association.user=user
							user_profile_association.association=association
							user_profile_association.group=group
							user_profile_association.save()

							user_profile_enterprise=UserProfileEnterprise()
							user_profile_enterprise.user=user
							user_profile_enterprise.enterprise=enterprise
							user_profile_enterprise.group=group
							user_profile_enterprise.save()
							
							user_profile_headquart=UserProfileHeadquart()
							user_profile_headquart.user=user
							user_profile_headquart.headquart=headquart
							user_profile_headquart.group=group
							user_profile_headquart.save()
			Message.info(request,("Cuenta <b>%(name)s</b> ha sido registrado correctamente!.") % {"name":d.username})
			if request.is_ajax():
				request.path="/account/login/" #/app/controller_path/action/$params
				return redirect("/account/login/")
				#return login_sys(request)
			else:
				return redirect("/account/login/")
		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		type_a_list = Association.TYPES
		solution_list = Solution.objects.filter(is_active=True).order_by("id")
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Crear cuenta"),
		"page_title":("Registro de la cuenta."),
		"d":d,
		"solution_list":solution_list,
		"type_a_list":type_a_list,
		
		}
	return render_to_response("account/signup.html", c, context_instance = RequestContext(request))
#endregion registro cuenta

#region login OK
@login_required(login_url="/account/login/")
def load_access(request, headquart_id, module_id):
	if request.is_ajax():
		return HttpResponse("ESTA OPERACION NO DEBE SER CARGADO CON AJAX, Presione F5")
	else:
		try:
			try:
				headquart = Headquart.objects.get(id=headquart_id)
			except:
				Message.error(request, ("Sede no seleccionado o no se encuentra en la base de datos."))
				return Redirect.to(request, "/home/choice_headquart/")
			try:
				module = Module.objects.get(id=module_id)
			except:
				Message.error(request, ("Módulo no seleccionado o no se encuentra en la base de datos."))
				return Redirect.to(request, "/home/choice_headquart/")

			if not request.user.is_superuser: #vovler a verificar si tiene permisos
				#obteniendo las sedes a la cual tiene acceso
				headquart_list = Headquart.objects.filter(userprofileheadquart__user__id = request.user.id).distinct()
				if headquart not in headquart_list:
					raise Exception(("Acceso denegado. No tiene privilegio para ingresar a esta sede: %s %s." % (headquart.enterprise.name, headquart.name)))
				#obteniendo los módulos a la cual tiene acceso
				group_list = Group.objects.filter(userprofileheadquart__headquart__id = headquart.id, userprofileheadquart__user__id = request.user.id).distinct()
				module_list = Module.objects.filter(groups__in = group_list).distinct()
				
				if module not in module_list:
					raise Exception(("Acceso denegado. No tiene privilegio para ingresar a este módulo: %s de %s %s." % (module.name, headquart.enterprise.name, headquart.name) ))
				
			#cargando permisos de datos para el usuario
			DataAccessToken.set_association_id(request, headquart.association.id)
			DataAccessToken.set_enterprise_id(request, headquart.enterprise.id)
			DataAccessToken.set_headquart_id(request, headquart.id)

			try:
				profile = Profile.objects.get(user_id=request.user.id)
				if profile.id:
					profile.last_headquart_id = headquart_id
					profile.last_module_id = module_id
					profile.save()
			except:
				person = Person(first_name=request.user.first_name, last_name=request.user.last_name)
				person.save()

				profile = Profile(user=request.user, last_headquart_id = headquart_id, last_module_id = module_id)
				profile.person=person
				profile.save()
				pass

			#Message.info(request, ("La sede %(name)s ha sido cargado correctamente.") % {"name":headquart_id} )
			if module.DBM == module.module:
				#return HttpResponseRedirect("/mod_backend/dashboard/")
				return Redirect.to(request, "/mod_backend/dashboard/")
			if module.VENTAS == module.module:
				return Redirect.to(request, "/mod_ventas/dashboard/")
			if module.PRO == module.module:
				return Redirect.to(request, "/mod_pro/dashboard/")
			
			#TODO agregue aqui su nuevo modulo

			else:
				Message.error(request, "Módulo no definido")
				return HttpResponseRedirect("/home/choice_headquart/")
		except Exception, e:
			Message.error(request, e)
		return HttpResponseRedirect("/home/choice_headquart/")
		#return HttpResponse("Ocurrió un grave error, comunique al administrador del sistema")

def login_sys(request):
	d = User()
	c = {
		"page_module":("Login"),
		"page_title":("Login."),
		"d":d,
		}

	if request.user.is_authenticated():
		try:#intentar cargar la última session
			profile = Profile.objects.get(user_id=request.user.id)
			if profile.last_headquart_id and profile.last_module_id:
				if request.is_ajax():
					request.path="/account/load_access/%s/%s/" % (profile.last_headquart_id, profile.last_module_id) #/app/controller_path/action/$params
					return load_access(request, profile.last_headquart_id, profile.last_module_id)
				else:						
					return redirect("/account/load_access/%s/%s/" % (profile.last_headquart_id, profile.last_module_id))
		except:
			pass
		return HttpResponseRedirect("/home/choice_headquart/")
	if request.method == "POST":
		
		d.username = request.POST.get("login")
		password = request.POST.get("password")
		account = authenticate(username=d.username, password=password)
		if account is not None and account.is_active is True:
			login(request, account)
			#cargando sesión para el usuario. no necesita
			#request.session["id"] = "Hola"
			Message.info(request, ("Bienvenido <b>%(name)s</b>.") % {"name":account.username} )
			try:#intentar cargar la última session
				profile = Profile.objects.get(user_id=request.user.id)
				if profile.last_headquart_id and profile.last_module_id:
					if request.is_ajax():
						request.path="/account/load_access/%s/%s/" % (profile.last_headquart_id, profile.last_module_id) #/app/controller_path/action/$params
						return load_access(request, profile.last_headquart_id, profile.last_module_id)
					else:						
						return redirect("/account/load_access/%s/%s/" % (profile.last_headquart_id, profile.last_module_id))
			except:
				pass
			return HttpResponseRedirect("/home/choice_headquart/")
		else:
			Message.error(request,("Contaseña para <b>%(name)s</b> no válido, o el usuario no existe o no está activo. ") % {"name":d.username} )
			return render_to_response("account/login.html", t, context_instance=RequestContext(request))
	else:
		""" user is not submitting the form, show the login form """
		return render_to_response("account/login.html", c, context_instance = RequestContext(request))

def logout_sys(request):
	logout(request)
	return HttpResponseRedirect("/")

@permission_resource_required
@transaction.commit_on_success
def user_profile(request):
	"""
	Actualiza perfil del usuario
	"""
	#account = request.user.get_profile
	d = None
	try:
		d = request.user
		try:
			profile = Profile.objects.get(user_id=d.id)
			if profile.id:
				d.first_name = d.profile.person.first_name
				d.last_name = d.profile.person.last_name
				d.photo = d.profile.person.photo
				d.identity_type = d.profile.person.identity_type
				d.identity_num = d.profile.person.identity_num
		except:
			pass
		
	except Exception, e:
		Message.error(request, ("Usuario no se encuentra en la base de datos. %s" % e))
		

	if request.method == "POST":
		try:
			#d.username = request.POST.get("login")
			
			#if User.objects.exclude(id = d.id).filter(username = d.username).count()>0:
			#	raise Exception( "El usuario <b>%s</b> ya existe " % d.username )

			if request.POST.get("email"):
				d.email = request.POST.get("email")
				if User.objects.exclude(id = d.id).filter(email = d.email).count()>0:
					raise Exception( "El email <b>%s</b> ya existe " % d.email )
			if request.POST.get("password"):
				d.set_password(request.POST.get("password"))
			d.save()

			try:
				person = Person.objects.get(profile=d.profile)
			except:
				person = Person()
				person.save()
				pass

			try:
				profile = Profile.objects.get(user=d)
			except:
				profile = Profile(user=d)
				profile.person=person
				profile.save()
				pass


			d.first_name = request.POST.get("first_name")
			d.last_name = request.POST.get("last_name")
			d.identity_type = request.POST.get("identity_type")
			d.identity_num = request.POST.get("identity_num")

			identity_type_display = dict((x, y) for x, y in Person.IDENTITY_TYPES)[d.identity_type]
			if Person.objects.exclude(id = person.id).filter(identity_type=d.identity_type, identity_num=d.identity_num).count()>0:
				raise Exception( "La persona con %s:<b>%s</b> ya existe " % (identity_type_display, d.identity_num) )
			
			if normalize("NFKD", u"%s %s" % (d.first_name, d.last_name)).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s %s" % (col["first_name"], col["last_name"])).encode("ascii", "ignore").lower() for col in Person.objects.values("first_name","last_name").exclude(id = person.id).filter(identity_type=d.identity_type, identity_num=d.identity_num)
				):
				raise Exception( "La persona <b>%s %s</b> y %s:<b>%s</b> ya existe " % (d.first_name, d.last_name, identity_type_display, d.identity_num) )
			
			
			person.first_name=request.POST.get("first_name")
			person.last_name=request.POST.get("last_name")
			person.identity_type = request.POST.get("identity_type")
			person.identity_num = request.POST.get("identity_num")
			person.photo = request.POST.get("persona_fotografia")

			person.save()
			d.photo = person.photo
			if d.id:
				Message.info(request,("Usuario <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.username}, True)
				return Redirect.to(request, "/home/choice_headquart/")

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
		group_perm_list = Group.objects.filter(module_set__in=module_list).order_by("-id").distinct() #trae los objetos relacionados sad.Module
		#print group_perm_list
		#print "=====================x"
		#pero hay que adornarlo de la forma Module>Group/perfil
		group_list_by_module=[]
		group_list_by_module_unique_temp=[]#solo para verificar que el Group no se repita si este está en dos o más módulos
		for module in module_list:
			for group in Group.objects.filter(module_set=module).distinct():
				if len(group_list_by_module)==0:
					group_list_by_module.append({
					"group": group,
					"module": module,
					})
					group_list_by_module_unique_temp.append(group)
				else:
					if group not in group_list_by_module_unique_temp:
						group_list_by_module.append({
						"group": group,
						"module": module,
						})
						group_list_by_module_unique_temp.append(group)
		#print group_list_by_module_unique_temp
		
		

	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Perfil del usuario"),
		"page_title":("Actualizar información del usuario."),
		"d":d,
		"user_profile_headquart_list":user_profile_headquart_list,
		"user_profile_enterprise_list":user_profile_enterprise_list,
		"user_profile_association_list":user_profile_association_list,
		"IDENTITY_TYPES":Person.IDENTITY_TYPES,
		}
	return render_to_response("account/profile.html", c, context_instance = RequestContext(request))
#endregion login
