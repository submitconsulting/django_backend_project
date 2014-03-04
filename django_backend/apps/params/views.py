# _*_ coding: latin-1 _*_
import json
import datetime
import locale
import time
#import re

from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404, render,redirect, Http404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import ugettext as _, ungettext 
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from apps.params.models import Locality, LocalityType
from apps.sad.views import resource_index
from apps.helpers.message import Message
#from django.views.decorators.csrf import csrf_exempt, csrf_protect
from apps.sad.decorators import is_admin, permission_resource_required
from django.template import Context, Template, loader 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from apps.sad.security import Security, SessionContext, Redirect
from unicodedata import normalize

#TODO por definirse. https://docs.djangoproject.com/en/dev/topics/i18n/translation/
def params_index(request): # solo si va tener un index para toda la app params
	outputs = _("Categories")
	outputp = _("Progress: %(percent_translated)s" ) % {"percent_translated":6} 
	outputp = outputp +"%"
	message_number=10
	output = ungettext ( #  to specify pluralized messages
		"%(hits)s/%(message_number)s message",
		"%(hits)s/%(message_number)s messages",
		message_number
	) % {
		"hits": 1, 
		"message_number": message_number
		} 
	return HttpResponse(output)

#Locality
#@csrf_exempt
#@login_required(login_url="/account/login/")
#@is_admin #para verificar si es administrador
@permission_resource_required
def locality_index(request, field="name", value="None", order="-id"):
	"""
	Página principal para locality
	"""
	#return Redirect.to_action(request,"add")

	#if SessionContext.is_administrator(request):
	#	print "USER ADMIN"
	#del request.session["id"]
	#s = SessionStore()
	#s["last_login"] = "holaaa"
	#s.save()

	#try:
	#	RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
	#	if bool(RE.search(value)):
  	#		value = datetime.datetime.strptime(value, "%d/%m/%Y")
  	#		print "d= %s " % value
	#except ValueError:
  	#	print("Invalid date!")

	#print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
	#print time.time()
	#print locale.getlocale()
	#print locale.getdefaultlocale()
	#locale.setlocale(locale.LC_ALL, "") #print locale.LC_TIME
	#print datetime.datetime.now().strftime("%a, %d %b %y")

	#settings.APP_AJAX=False

	field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
	value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()
	order = (order if not request.REQUEST.get("order") else request.REQUEST.get("order")).strip()
	#print ("field="+field);
	#print ("value="+value);
	#print ("order="+order);

	locality_page=None
	try:
		value_f = "" if value == "None" else value # (true or false) ? value1:value2
		column_contains = u"%s__%s" % (field,"contains") #SEL-- WHERE name LIKE %an%
		locality_list = Locality.objects.filter(**{ column_contains: value_f }).order_by(order)
		paginator = Paginator(locality_list, 25) # Show num_rows=25 contacts per page
		try:
			locality_page = paginator.page(request.GET.get("page"))
		except PageNotAnInteger:
			locality_page = paginator.page(1)
		except EmptyPage:
			locality_page = paginator.page(paginator.num_pages)
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":_("Locality"),
		"page_title":_("Localities list."),
		
		"locality_page":locality_page,
		"field":field,
		"value":value.replace("/", "-"),
		"order":order,
		}

	#now = datetime.datetime.now()
	#t = Template("<html><body>It is now {{ current_date }}.</body></html>")

	#tx= loader.get_template("white_page.html")
	#c2 = Context({"my_name": "Adrian"})
	#response = HttpResponse(tx.render(c),mimetype="application/xhtml+xml")
	#return HttpResponse(tx.render(c2),mimetype="application/xhtml+xml")
	return render_to_response("params/locality/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
def locality_report(request, field="name", value="None", order="-id"):
	field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
	value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()
	order = (order if not request.REQUEST.get("order") else request.REQUEST.get("order")).strip()
	
	try:
		value = "" if value == "None" else value
		column_contains = u"%s__%s" % (field,"contains")

		locality_list = Locality.objects.filter(**{ column_contains: value }).order_by(order)
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":_("Locality"),
		"page_title":_("Localities report."),
		"locality_list":locality_list,
		}
	return render_to_response("params/locality/report.html", c, context_instance = RequestContext(request))

#@permission_resource_required(template_denied_name="denied_mod_backend.html")
@permission_resource_required
def locality_add(request):
	d = Locality()
	d.msnm = 0
	if request.method == "POST":
		try:
			#Aquí asignar los datos
			d.name = request.POST.get("name")
			d.msnm = request.POST.get("msnm")
			if request.POST.get("locality_type_id"):
				d.locality_type = LocalityType.objects.get(id=request.POST.get("locality_type_id"))

			if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Locality.objects.values("name").exclude(id = d.id) #puede .filter()
				):
				raise Exception(_("Locality <b>%(name)s</b> name's already in use.") % {"name":d.name}) #El nombre x para localidad ya existe.
			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Localidad <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.name}, True)
				#return Redirect.to(request, "/params/locality/index/")#usar to(...) cuando la acción está implementada en otra app, ver sad.views.user_index
				return Redirect.to_action(request, "index")#usar to_action(...) cuando la acción está implementada en este archivo
		except Exception, e:
			Message.error(request, e)
	try:
		locality_type_list = LocalityType.objects.all().order_by("name")
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":_("Locality"),
		"page_title":_("New locality."),
		"d":d,
		"locality_type_list":locality_type_list,
		}
	return render_to_response("params/locality/add.html", c, context_instance = RequestContext(request))

@transaction.non_atomic_requests
@transaction.commit_on_success #para que funcione basta poner en el except o donde sea conveniente transaction.rollback()
@permission_resource_required
def locality_edit(request, key):
	id=Security.is_valid_key(request, key, "locality_upd")
	if not id:
		return Redirect.to_action(request, "index")
	d = None
	try:
		d = get_object_or_404(Locality, id=id) #Locality.objects.get(id=id)
	except: #Locality.DoesNotExist
		Message.error(request, _("Locality not found in the database."))
		return Redirect.to_action(request, "index")

	if request.method == "POST":
		try:
			#para probar transaction 
			#locality_type=LocalityType()
			#locality_type.name="Rural4"
			#if LocalityType.objects.filter(name = locality_type.name).count() > 0:
			#	raise Exception(_("LocalityType <b>%(name)s</b> name"s already in use.") % {"name":locality_type.name}) #trhow new Exception("msg")
			#locality_type.save()
			#d.locality_type=locality_type

			#Aquí asignar los datos
			d.name = request.POST.get("name")
			d.is_active=True

			if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Locality.objects.values("name").exclude(id = d.id) #puede .filter()
				):
				raise Exception(_("Locality <b>%(name)s</b> name's already in use.") % {"name":d.name}) #trhow new Exception("msg")
			#salvar registro
			d.save()
			if d.id:
				#transaction.commit() se colocaría solo al final, pero no amerita pk ya está decorado con @transaction.commit_on_success
				Message.info(request,("Localidad <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name}, True)
				return Redirect.to_action(request, "index")
		except Exception, e:
			transaction.rollback() #para reversar en caso de error en alguna de las tablas
			Message.error(request, e)
	try:
		locality_type_list = LocalityType.objects.all().order_by("name")
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":_("Locality"),
		"page_title":_("Update locality."),
		"d":d,
		"locality_type_list":locality_type_list,
		}
	return render_to_response("params/locality/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
def locality_delete(request, key):
	id=Security.is_valid_key(request, key, "locality_del")
	if not id:
		return Redirect.to_action(request, "index")
	try:
		d = get_object_or_404(Locality, id=id) #Locality.objects.get(id=id)
	except: #Locality.DoesNotExist
		Message.error(request, _("Locality not found in the database."))
		return Redirect.to_action(request, "index")
	try:
		#rastreando dependencias
		if d.headquart_set.count() > 0:
			raise Exception( ("Localidad <b>%(name)s</b> está asignado en headquart.") % {"name":d.name} )
		
		d.delete()
		if not d.id:
			Message.info(request,("Localidad <b>%(name)s</b> ha sido eliminado correctamente.") % {"name":d.name}, True)
			return Redirect.to_action(request, "index")
	except Exception, e:
		Message.error(request, e)
		return Redirect.to_action(request, "index")

@permission_resource_required
def locality_state(request, state, key):
	"""
	Inactiva y reactiva el estado de la Localidad
	"""
	id=Security.is_valid_key(request, key, "locality_%s" % state )
	if not id:
		return Redirect.to_action(request, "index")
	try:
		d = get_object_or_404(Locality, id=id)
	except:
		Message.error(request, ("Localidad no se encuentra en la base de datos."))
		return Redirect.to_action(request, "index")
	try:
		if state == "inactivar" and d.is_active == False:
			Message.error(request, ("Localidad ya se encuentra inactivo."))
		else:
			if state == "reactivar" and d.is_active == True:
				Message.error(request, ("Localidad ya se encuentra activo."))
			else:
				d.is_active = (True if state == "reactivar" else False)
				d.save()
				if d.id:
					if d.is_active:
						Message.info(request,("Localidad <b>%(name)s</b> ha sido reactivado correctamente.") % {"name":d.name}, True)
					else:
						Message.info(request,("Localidad <b>%(name)s</b> ha sido inactivado correctamente.") % {"name":d.name}, True)
					return Redirect.to_action(request, "index")
	except Exception, e:
		Message.error(request, e)
		return Redirect.to_action(request, "index")
#Fin Locality
