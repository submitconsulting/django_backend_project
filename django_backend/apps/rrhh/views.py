# _*_ coding: utf-8 _*_
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
#from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from apps.sad.decorators import is_admin, permission_resource_required
from apps.sad.security import Security, DataAccessToken, Redirect
from apps.helpers.message import Message

from apps.params.models import Person
from django.contrib.auth.models import User, Group, Permission 
from django.contrib.contenttypes.models import ContentType
from apps.space.models import Headquart
from apps.sad.models import Module, Menu, UserProfileAssociation, UserProfileEnterprise, UserProfileHeadquart
from apps.space.models import Solution
#from apps.home.views import choice_headquart
from django.db.models import Q

from apps.rrhh.models import Employee
from apps.params.models import Categoria

from apps.space.models import Headquart
from unicodedata import normalize
from django.http import HttpResponse

#region employee OK
def employee_json_by_filter(request): 
	filters = ('' if request.REQUEST.get('filter') == None else request.REQUEST.get('filter')).strip()
	#print ('filters=%s'%(True if filters else False));
	list_db= Employee.objects.filter(
		Q(codigo__contains=filters) | Q(person__first_name__contains=filters) | Q(person__last_name__contains=filters) | Q( id__isnull= True if filters else False ),
		headquart= DataAccessToken.get_headquart_id(request.session),
		) 
	data = list()
	for d in list_db:
		id_key=Security.get_key(d.id, "employee_upd")
		data.append({ 'id': id_key, 'codigo': d.codigo, 'descripcion': "%s %s" % (d.person.first_name,d.person.last_name) , 'precio_venta': d.contrato_vigente })
	return HttpResponse(
		json.dumps(data ),
			content_type="application/json; charset=uft8"
		)

@login_required(login_url="/account/login/")
@permission_resource_required(template_denied_name="denied_mod_pro.html")
def employee_index(request, field="codigo", value="None", order="-id"):
	"""
	Página principal para trabajar con employees
	"""
	try:
		headquart = get_object_or_404(Headquart, id=DataAccessToken.get_headquart_id(request.session))
	except:
		Message.error(request, ("Sede no seleccionado o no se encuentra en la base de datos."))
		return Redirect.to(request, "/home/choice_headquart/")

	field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
	value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()
	order = (order if not request.REQUEST.get("order") else request.REQUEST.get("order")).strip()

	menu_page=None
	try:
		value_f = "" if value == "None" else value
		column_contains = u"%s__%s" % (field,"contains")
		employee_list = Employee.objects.filter(headquart=headquart, **{ column_contains: value_f }).order_by("pos").order_by(order)
		paginator = Paginator(employee_list, 100)
		try:
			employee_page = paginator.page(request.GET.get("page"))
		except PageNotAnInteger:
			employee_page = paginator.page(1)
		except EmptyPage:
			employee_page = paginator.page(paginator.num_pages)
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Gestión de employees"),
		"page_title":("Listado de employees."),
		
		"employee_page":employee_page,
		#"MODULES":dict((x, y) for x, y in Module.MODULES),
		"field":field,
		"value":value.replace("/", "-"),
		"order":order,
		}
	return render_to_response("rrhh/employee/index.html", c, context_instance = RequestContext(request))

@permission_resource_required(template_denied_name="denied_mod_pro.html")
@transaction.commit_on_success
def employee_add(request):
	"""
	Agrega Employee
	"""
	d = Employee()
	d.photo="personas/default.png"
	if request.method == "POST":
		try:
			
			d.first_name = request.POST.get("first_name")
			d.last_name = request.POST.get("last_name")
			d.photo = request.POST.get("persona_fotografia")
			d.identity_type = request.POST.get("identity_type")
			d.identity_num = request.POST.get("identity_num")
			identity_type_display = dict((x, y) for x, y in Person.IDENTITY_TYPES)[d.identity_type]

			d.codigo = request.POST.get("codigox")
			d.headquart_id = DataAccessToken.get_headquart_id(request.session)

			if Person.objects.filter(identity_type=d.identity_type, identity_num=d.identity_num).count()>0:
				raise Exception( "La persona con %s:<b>%s</b> ya existe " % (identity_type_display, d.identity_num) )
			
			if normalize("NFKD", u"%s %s" % (d.first_name, d.last_name)).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s %s" % (col["first_name"], col["last_name"])).encode("ascii", "ignore").lower() for col in Person.objects.values("first_name","last_name").exclude(id = d.id).filter(identity_type=d.identity_type, identity_num=d.identity_num)
				):
				raise Exception( "La persona <b>%s %s</b> con %s:<b>%s</b> ya existe " % (d.first_name, d.last_name, identity_type_display, d.identity_num) )
			person = Person(first_name=d.first_name, last_name=d.last_name, identity_type=d.identity_type, identity_num=d.identity_num, photo=d.photo)
			person.save()
			d.person=person


			if Employee.objects.filter(codigo = d.codigo).exclude(id = d.id).count()>0:
				raise Exception( "El employee <b>%s</b> ya existe " % d.codigo )
			d.save()
			if d.id:
				Message.info(request,("Employee <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.codigo}, True)
				request.session['id_personal'] = d.id
				request.path="/rrhh/employee/edit/"
				c = {
					"page_module":("Gestión de employees"),
					"page_title":("Actualizar employee."),
					"d":d,
					"IDENTITY_TYPES":Person.IDENTITY_TYPES,
					}
				return render_to_response("rrhh/employee/edit.html", c, context_instance = RequestContext(request))

		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	#categoria_nombre_list=[]
	try:
		print ""
		#categoria_nombre_list = json.dumps(list(col["nombre"]+""  for col in Categoria.objects.values("nombre").filter().order_by("nombre")))
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Gestión de empleados"),
		"page_title":("Agregar empleado."),
		"d":d,
		"IDENTITY_TYPES":Person.IDENTITY_TYPES,
		}
	return render_to_response("rrhh/employee/add.html", c, context_instance = RequestContext(request))

@permission_resource_required(template_denied_name="denied_mod_pro.html")
def employee_choice(request, key):
	"""
	Elige Employee
	"""
	#print key
	id=Security.is_valid_key(request, key, "employee_upd")
	request.session['id_personal']=id
	return Redirect.to_action(request, "edit")


@permission_resource_required(template_denied_name="denied_mod_pro.html")
@transaction.commit_on_success
def employee_edit(request):
	"""
	Actualiza Employee
	"""
	#print key
	#id=Security.is_valid_key(request, key, "employee_upd")
	id=request.session['id_personal']
	#print id
	if not id:
		return Redirect.to_action(request, "index")
	#print id
	d = None
	try:
		d = get_object_or_404(Employee, id=id)
		try:
			person = Person.objects.get(employee=d.id)
			if person.id:
				d.first_name = d.person.first_name
				d.last_name = d.person.last_name
				d.photo = d.person.photo
				d.identity_type = d.person.identity_type
				d.identity_num = d.person.identity_num
		except:
			pass
		
	except Exception, e:
		Message.error(request, ("Employee no se encuentra en la base de datos. %s" % e))
		return Redirect.to_action(request, "index")

	if request.method == "POST":
		try:
			d.codigo = request.POST.get("codigox")

			if Employee.objects.filter(codigo = d.codigo).exclude(id = d.id).count()>0:
				raise Exception( "El employee <b>%s</b> ya existe " % d.codigo )
			d.save()
			try:
				person = Person.objects.get(employee=d)
			except:
				person = Person(employee=d)
				person.save()
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
				raise Exception( "La persona <b>%s %s</b> con %s:<b>%s</b> ya existe " % (d.first_name, d.last_name, identity_type_display, d.identity_num) )
			
			
			person.first_name=request.POST.get("first_name")
			person.last_name=request.POST.get("last_name")
			person.identity_type = request.POST.get("identity_type")
			person.identity_num = request.POST.get("identity_num")

			person.photo = request.POST.get("persona_fotografia")
			person.save()
			d.photo = person.photo
			if d.id:
				Message.info(request,("Employee <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.codigo}, True)
				#return Redirect.to_action(request, "index")

		except Exception, e:
			transaction.rollback()
			Message.error(request, e)

	c = {
		"page_module":("Gestión de employees"),
		"page_title":("Actualizar employee."),
		"d":d,
		"IDENTITY_TYPES":Person.IDENTITY_TYPES,
		}
	return render_to_response("rrhh/employee/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required(template_denied_name="denied_mod_pro.html")
@transaction.commit_on_success
def employee_delete(request, key):
	"""
	Elimina employee
	"""
	id=Security.is_valid_key(request, key, "employee_del")
	if not id:
		return Redirect.to_action(request, "index")
	try:
		d = get_object_or_404(Employee, id=id)
	except:
		Message.error(request, ("Employee no se encuentra en la base de datos."))
		return Redirect.to_action(request, "index")
	try:
		d.delete()
		if not d.id:
			Message.info(request,("Employee <b>%(codigo)s</b> ha sido eliminado correctamente.") % {"codigo":d.codigo}, True)
			return Redirect.to_action(request, "index")
	except Exception, e:
		Message.error(request, e)
		return Redirect.to_action(request, "index")


@permission_resource_required(template_denied_name="denied_mod_pro.html")
@transaction.commit_on_success
def employee_add_all(request):
	"""
	Agrega Employee
	"""
	d = Employee()
	n=1010
	i=10
	k=i
	while i<=n:
		print i
		d = Employee()
		d.codigo = "00%s"%i
		d.headquart_id = DataAccessToken.get_headquart_id(request.session)
		person = Person(first_name="NOMB%s"%i, last_name="APELL%s"%i, identity_num="00%s0"%i)
		person.save()
		d.person=person
		d.save()
		i=i+1
	return HttpResponse("%s registros insertados " % (n-k))
#endregion employee