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

from apps.sad.security import DataAccessToken

from apps.helpers.message import Message
from django.db import transaction
from django.contrib.auth.models import User
#from apps.sad.models import *
from apps.params.models import Person
from apps.space.models import Association, Enterprise, Headquart, Solution
from apps.sad.models import  Module, UserProfileAssociation, UserProfileEnterprise, UserProfileHeadquart
from apps.home.views import choice_headquart
from unicodedata import normalize
#from django.template.defaultfilters import slugify

@login_required
def profile(request): #TODO sin uso, borrar o terminar
    if not request.user.is_authenticated():
        return HrttpResponseRedirect('/login/')
    account = request.user.get_profile
    context = {'account': account}
    return render_to_response('home/dashboard.html', context, context_instance=RequestContext(request))


@transaction.commit_on_success
def add_enterprise(request):

	#data = "cáñété'´píñána+bâ'x"
	#https://github.com/django/django/blob/master/django/contrib/auth/management/__init__.py
	#print unicodedata.normalize('NFKD', u"%s"%data).encode('ascii', 'ignore')
	#names = list(unicodedata.normalize('NFKD', u"%s" % col['name']).encode('ascii', 'ignore').lower() for col in Association.objects.values('name','type_a').filter(name__contains="AS"))
	#print names
	#print slugify(u"%s"%data)
	#print data.encode('ascii', 'ignore')
	#print normalize('NFKD', u"%s"%data).encode('ascii', 'ignore')
	d = Enterprise()

	#solution_list = None
	if request.method == "POST":
		#with transaction.commit_manually():
		#transaction.set_autocommit(False)
		try:
			
			d.enterprise_name = request.POST.get('enterprise_name')
			d.enterprise_tax_id = request.POST.get('enterprise_tax_id')
			d.association_name = request.POST.get('association_name')
			d.association_type_a = request.POST.get('association_type_a')
			d.solution_id = request.POST.get('solution_id')
			
			solution=Solution.objects.get(id=d.solution_id)
			user = request.user
			
			association = Association(name=d.association_name, type_a=d.association_type_a, solution=solution)
			#if Association.objects.filter(name=normalize('NFKD', u"%s" % d.association_name).encode('ascii', 'ignore')).count()>0:
			if normalize('NFKD', u"%s" % d.association_name).encode('ascii', 'ignore').lower() in list(
				normalize('NFKD', u"%s" % col['name']).encode('ascii', 'ignore').lower() for col in Association.objects.values('name')
				):
				raise Exception( "La asociación <b>%s</b> ya existe " % (d.association_name) )
			association.save()

			enterprise = Enterprise(name=d.enterprise_name, tax_id=d.enterprise_tax_id, type_e=d.association_type_a, solution=solution )
			#if Enterprise.objects.filter(name=normalize('NFKD', u"%s" % d.enterprise_name).encode('ascii', 'ignore')).count()>0:
			if normalize('NFKD', u"%s" % d.enterprise_name).encode('ascii', 'ignore').lower() in list(
				normalize('NFKD', u"%s" % col['name']).encode('ascii', 'ignore').lower() for col in Enterprise.objects.values('name')
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
			Message.info(request,("Empresa %(name)s ha sido registrado correctamente!.") % {'name':d.enterprise_name})
			if request.is_ajax():
				request.path="/home/choice_headquart/" #/app/controller_path/action/$params
				return choice_headquart(request)
			else:
				return redirect('/home/choice_headquart/')
		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
		#else:
		#	transaction.commit()
        #	Message.info(request, "Loa cuenta se ha registrado correctamente!" )
		#finally:
		#	transaction.set_autocommit(True)
	try:
		type_a_list = Association().TYPES
		solution_list = Solution.objects.all().order_by("id")
	except Exception, e:
		Message.error(request, e)
	t = {
		'page_module':("Registro de empresa"),
		'page_title':("Agregar empresa de la cuenta %(login)s.") % {'login':request.user},
		'd':d,
		'solution_list':solution_list,
		'type_a_list':type_a_list,
		
		}
	return render_to_response("account/add_enterprise.html", t, context_instance = RequestContext(request))


@transaction.commit_on_success
def signup_sys(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home/choice_headquart/')
	d = Person()
	d.last_name=""
	if request.method == "POST":
		try:
			d.first_name = request.POST.get('first_name')
			d.last_name = request.POST.get('last_name')
			d.username = request.POST.get('login')
			d.enterprise_name = request.POST.get('enterprise_name')
			d.enterprise_tax_id = request.POST.get('enterprise_tax_id')
			d.association_name = request.POST.get('association_name')
			d.association_type_a = request.POST.get('association_type_a')
			d.solution_id = request.POST.get('solution_id')
			d.email = request.POST.get('email')
			#password = request.POST.get('password')
			#acept_term = request.POST.get('acept_term')
			solution=Solution.objects.get(id=d.solution_id)
			d.solution=solution
			if User.objects.filter(username = d.username).count()>0:
				raise Exception( "El usuario <b>%s</b> ya existe " % d.username )

			if User.objects.filter(email = d.email).count()>0:
				raise Exception( "El email <b>%s</b> ya existe " % d.email )

			user = User.objects.create_user(username=d.username, email = d.email, password = request.POST.get('password'))
			user.save()
			
			if Person.objects.filter(first_name=d.first_name, last_name=d.last_name).count()>0:
				raise Exception( "La persona <b>%s %s</b> ya existe " % (d.first_name, d.last_name) )
			
			person = Person(user=user, first_name=d.first_name, last_name=d.last_name)
			person.save()
			association = Association(name=d.association_name, type_a=d.association_type_a, solution=solution)
			if normalize('NFKD', u"%s" % d.association_name).encode('ascii', 'ignore').lower() in list(
				normalize('NFKD', u"%s" % col['name']).encode('ascii', 'ignore').lower() for col in Association.objects.values('name')
				):
				raise Exception( "La asociación <b>%s</b> ya existe " % (d.association_name) )
			association.save()

			enterprise = Enterprise(name=d.enterprise_name, tax_id=d.enterprise_tax_id, type_e=d.association_type_a, solution=solution )
			if normalize('NFKD', u"%s" % d.enterprise_name).encode('ascii', 'ignore').lower() in list(
				normalize('NFKD', u"%s" % col['name']).encode('ascii', 'ignore').lower() for col in Enterprise.objects.values('name')
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
			Message.info(request,("Cuenta <b>%(name)s</b> ha sido registrado correctamente!.") % {'name':d.username})
			if request.is_ajax():
				#print "AJAX"
				request.path="/account/login/" #/app/controller_path/action/$params
				return login_sys(request)
			else:
				#print "NO AJAX"
				return redirect('/account/login/')
		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
		#else:
		#	transaction.commit()
        #	Message.info(request, "Loa cuenta se ha registrado correctamente!" )
		#finally:
		#	transaction.set_autocommit(True)
	try:
		type_a_list = Association().TYPES
		solution_list = Solution.objects.all().order_by("id")
	except Exception, e:
		Message.error(request, e)
	t = {
		'page_module':("Crear cuenta"),
		'page_title':("Registro de la cuenta."),
		'd':d,
		'solution_list':solution_list,
		'type_a_list':type_a_list,
		
		}
	return render_to_response("account/signup.html", t, context_instance = RequestContext(request))

@login_required
def load_access(request, headquart_id, module_id):
	if request.is_ajax():
		return HttpResponse('ESTA OPERACION NO DEBE SER CARGADO CON AJAX, Presione F5')
	else:
		try:
			headquart = Headquart.objects.get(id=headquart_id)
			#cargando permisos de datos para el usuario
			DataAccessToken.set_association_id(request, headquart.association.id)
			DataAccessToken.set_enterprise_id(request, headquart.enterprise.id)
			DataAccessToken.set_headquart_id(request, headquart.id)

			try:
				person = Person.objects.get(user_id=request.user.id)
				if person.id:
					person.last_headquart_id = headquart_id
					person.last_module_id = module_id
					person.save()
			except:
				person = Person(user=request.user, first_name=request.user.first_name, last_name=request.user.last_name, last_headquart_id = headquart_id, last_module_id = module_id)
				person.save()
				pass

			if headquart:
				module = Module.objects.get(id=module_id)
				#Message.info(request, ("La sede %(name)s ha sido cargado correctamente.") % {'name':headquart_id} )
				if module.DBM == module.module:
					return HttpResponseRedirect('/mod_backend/dashboard/')
				else:
					return HttpResponseRedirect('/mod_ventas/dashboard/')
			else:
				return HttpResponse('Sede no se encuentra')
		except Exception, e:
			Message.error(request, e)
		return HttpResponse('Ocurrió un grave error, comunique al administrador del sistema')

def login_sys(request):
	d = User()
	t = {
		'page_module':("Login"),
		'page_title':("Login."),
		'd':d,
		}

	if request.user.is_authenticated():
		return HttpResponseRedirect('/home/choice_headquart/')
	if request.method == 'POST':
		
		d.username = request.POST.get('login')
		password = request.POST.get('password')
		account = authenticate(username=d.username, password=password)
		if account is not None and account.is_active is True:
			login(request, account)
			#cargando sesión para el usuario. no necesita
			#request.session['id'] = "Hola"
			Message.info(request, ("Bienvenido <b>%(name)s</b>.") % {'name':account.username} )
			try:#intentar cargar la última session
				person = Person.objects.get(user_id=request.user.id)
				if person.last_headquart_id and person.last_module_id:
					if request.is_ajax():
						request.path="/account/load_access/%s/%s/" % (person.last_headquart_id, person.last_module_id) #/app/controller_path/action/$params
						return load_access(request, person.last_headquart_id, person.last_module_id)
					else:						
						return redirect('/account/load_access/%s/%s/' % (person.last_headquart_id, person.last_module_id))
			except:
				pass
			return HttpResponseRedirect('/home/choice_headquart/')
		else:
			Message.error(request,("Contaseña para <b>%(name)s</b> no válido, o el usuario no existe o no está activo. ") % {'name':d.username} )
			return render_to_response('account/login.html', t, context_instance=RequestContext(request))
	else:
		''' user is not submitting the form, show the login form '''

		return render_to_response("account/login.html", t, context_instance = RequestContext(request))

def logout_sys(request):
	logout(request)
	return HttpResponseRedirect('/')
