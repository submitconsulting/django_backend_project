# _*_ coding: utf-8 _*_
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
from django.db.models import Avg, Max, Min, Count

from unicodedata import normalize

from apps.sad.decorators import is_admin, permission_resource_required
from apps.sad.security import Security, DataAccessToken
from apps.helpers.message import Message
from apps.home.views import choice_headquart
#from django.contrib.auth.models import User, Group, Permission 

from django.contrib.contenttypes.models import ContentType
from apps.space.models import Solution, Association, Enterprise, Headquart
from apps.params.models import Locality
#from itertools import chain
from apps.sad.upload import Upload

#region headquart OK
@permission_resource_required
def headquart_index(request):
	"""
	Página principal para trabajar con sedes
	"""
	try:
		enterprise = get_object_or_404(Enterprise, id=DataAccessToken.get_enterprise_id(request.session))
	except:
		Message.error(request, ("Empresa no seleccionada o no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/home/choice_headquart/" #/app/controller_path/action/$params
			return choice_headquart(request)
		else:
			return redirect("/home/choice_headquart/")

	try:
		headquart_list = Headquart.objects.filter(enterprise_id=DataAccessToken.get_enterprise_id(request.session)).order_by("-id")
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Cuenta"),
		"page_title":("Listado de sedes de la empresa."),
		"headquart_list":headquart_list,
		}
	return render_to_response("space/headquart/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def headquart_add(request):
	"""
	Agrega sede
	"""
	d = Headquart()
	d.phone=""
	d.address=""
	#d.locality_name
	if request.method == "POST":
		try:
			d.name = request.POST.get("name")
			d.phone = request.POST.get("phone")
			d.address = request.POST.get("address")
			d.is_main = False
			d.locality_name = request.POST.get("locality_name")
			if request.POST.get("locality_name"):
				d.locality, is_locality_created  = Locality.objects.get_or_create(
					name=request.POST.get("locality_name"), #name__iexact
					)
			d.association_id = DataAccessToken.get_association_id(request.session)
			d.enterprise_id = DataAccessToken.get_enterprise_id(request.session)

			if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Headquart.objects.values("name").exclude(id = d.id).filter(enterprise_id=d.enterprise_id)
				):
				raise Exception( "La sede <b>%s</b> ya existe " % (d.name) )
			d.save()
			if d.id:
				Message.info(request,("Sede <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.name})
				if request.is_ajax():
					request.path="/space/headquart/index/" #/app/controller_path/action/$params
					return headquart_index(request)
				else:
					return redirect("/space/headquart/index/")
		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		locality_name_list = json.dumps(list(col["name"]+""  for col in Locality.objects.values("name").filter().order_by("name")))
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Cuenta"),
		"page_title":("Agregar sede."),
		"d":d,
		"locality_name_list":locality_name_list,
		}
	return render_to_response("space/headquart/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def headquart_edit(request, key):
	"""
	Actualiza sede
	"""
	id=Security.is_valid_key(request, key, "headquart_upd")
	if not id:
		if request.is_ajax():
			request.path="/space/headquart/index/" #/app/controller_path/action/$params
			return headquart_index(request)
		else:
			return redirect("/space/headquart/index/")
	d = None

	try:
		d = get_object_or_404(Headquart, id=id)
		if d.locality:
			d.locality_name = d.locality.name
	except:
		Message.error(request, ("Sede no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/space/headquart/index/" #/app/controller_path/action/$params
			return headquart_index(request)
		else:
			return redirect("/space/headquart/index/")

	if request.method == "POST":
		try:
			d.name = request.POST.get("name")
			d.phone = request.POST.get("phone")
			d.address = request.POST.get("address")
			d.locality_name = request.POST.get("locality_name")
			if request.POST.get("locality_name"):
				d.locality, is_locality_created  = Locality.objects.get_or_create(
					name=request.POST.get("locality_name"), #name__iexact
					)
			if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Headquart.objects.values("name").exclude(id = d.id).filter(enterprise_id=d.enterprise_id)
				):
				raise Exception( "La sede <b>%s</b> ya existe " % (d.name) )

			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Sede <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})
				if request.is_ajax():
					request.path="/space/headquart/index/" #/app/controller_path/action/$params
					return headquart_index(request)
				else:
					return redirect("/space/headquart/index/")

		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		locality_name_list = json.dumps(list(col["name"]+""  for col in Locality.objects.values("name").filter().order_by("name")))
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Cuenta"),
		"page_title":("Actualizar sede."),
		"d":d,
		"locality_name_list":locality_name_list,
		}
	return render_to_response("space/headquart/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
def headquart_delete(request, key):
	"""
	Elimina sede
	"""
	id=Security.is_valid_key(request, key, "headquart_del")
	if not id:
		if request.is_ajax():
			request.path="/space/headquart/index/" #/app/controller_path/action/$params
			return headquart_index(request)
		else:
			return redirect("/space/headquart/index/")
	try:
		d = get_object_or_404(Headquart, id=id)
	except:
		Message.error(request, ("Sede no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/space/headquart/index/" #/app/controller_path/action/$params
			return headquart_index(request)
		else:
			return redirect("/space/headquart/index/")
	try:
		if d.enterprise.headquart_set.count() == 1:
			raise Exception( ("Empresa <b>%(name)s</b> no puede quedar sin ninguna sede.") % {"name":d.enterprise.name} )
		d.delete()
		if not d.id:
			Message.info(request,("Sede <b>%(name)s</b> ha sido eliminado correctamente.") % {"name":d.name}, True)
			if request.is_ajax():
				request.path="/space/headquart/index/" #/app/controller_path/action/$params
				return headquart_index(request)
			else:
				return redirect("/space/headquart/index/")
	except Exception, e:
		Message.error(request, e)
		if request.is_ajax():
			request.path="/space/headquart/index/" #/app/controller_path/action/$params
			return headquart_index(request)
		else:
			return redirect("/space/headquart/index/")
#endregion headquart

#region enterprise OK
@permission_resource_required
def enterprise_index(request):
	"""
	Página principal para trabajar con empresas
	"""
	try:
		d = get_object_or_404(Association, id=DataAccessToken.get_association_id(request.session))
	except:
		Message.error(request, ("Asociación no seleccionada o no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/home/choice_headquart/" #/app/controller_path/action/$params
			return choice_headquart(request)
		else:
			return redirect("/home/choice_headquart/")
	enterprise_list=None
	try:
		subq = "SELECT COUNT(*) as count_sedes FROM space_headquart WHERE space_headquart.enterprise_id = space_enterprise.id" #mejor usar {{ d.headquart_set.all.count }} y listo, trate de no usar {{ d.num_sedes_all }}
		#enterprise_list = Enterprise.objects.filter(headquart__association_id=DataAccessToken.get_association_id(request.session)).annotate(num_sedes=Count("headquart")).order_by("-id").distinct().extra(select={"num_sedes_all": subq})
		enterprise_list = Enterprise.objects.filter(headquart__association_id=DataAccessToken.get_association_id(request.session)).annotate(num_sedes=Count("headquart")).order_by("-id").distinct()
		#enterprise_list2= Enterprise.objects.filter(headquart__enterprise_id=DataAccessToken.get_enterprise_id(request.session)).annotate(num_sedes_all=Count("headquart")).distinct()
		#enterprise_list =enterprise_list1.add(num_sedes_all="e")
		#enterprise_list = chain(enterprise_list1, enterprise_list2)
		#enterprise_list= [s.id for s in sets.Set(enterprise_list1).intersection(sets.Set(enterprise_list2))]
		#enterprise_list=enterprise_list.distinct()
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Cuenta"),
		"page_title":("Listado de empresas con sedes vinculadas a la asociación."),
		"enterprise_list":enterprise_list,
		}
	return render_to_response("space/enterprise/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def enterprise_add(request):
	"""
	Agrega empresa dentro de una asociación, para ello deberá agregarse con una sede Principal
	"""
	d = Enterprise()
	d.sede="Principal"
	#d.locality_name
	if request.method == "POST":
		try:
			d.name = request.POST.get("name")
			d.tax_id = request.POST.get("tax_id")
			d.type_e = request.POST.get("type_e")
			d.solution_id = request.POST.get("solution_id")
			#solution=Solution.objects.get(id=d.solution_id) #no es necesario

			if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Enterprise.objects.values("name").exclude(id = d.id)
				):
				raise Exception( ("Empresa <b>%(name)s</b> ya existe.") % {"name":d.name} )

			if Enterprise.objects.exclude(id = d.id).filter(tax_id=d.tax_id).count()>0:
				raise Exception( "La empresa con RUC <b>%s</b> ya existe " % (d.tax_id) )

			

			d.save()

			headquart = Headquart()
			headquart.name=request.POST.get("sede")
			headquart.association_id=DataAccessToken.get_association_id(request.session)
			headquart.enterprise=d

			if normalize("NFKD", u"%s" % headquart.name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Headquart.objects.values("name").exclude(id = headquart.id).filter(enterprise_id=headquart.enterprise_id)
				):
				raise Exception( "La sede <b>%s</b> ya existe " % (headquart.name) )

			headquart.save()

			if d.id:
				Message.info(request,("Empresa <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.name})
				if request.is_ajax():
					request.path="/space/enterprise/index/" #/app/controller_path/action/$params
					return enterprise_index(request)
				else:
					return redirect("/space/enterprise/index/")
		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		solution_list = Solution.objects.all().order_by("id")
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Cuenta"),
		"page_title":("Agregar empresa dentro de la asociación."),
		"d":d,
		"TYPES":Enterprise.TYPES,
		"solution_list":solution_list,
		}
	return render_to_response("space/enterprise/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def enterprise_edit(request, key):
	"""
	Actualiza empresa
	"""
	id=Security.is_valid_key(request, key, "enterprise_upd")
	if not id:
		if request.is_ajax():
			request.path="/space/enterprise/index/" #/app/controller_path/action/$params
			return enterprise_index(request)
		else:
			return redirect("/space/enterprise/index/")
	d = None

	try:
		d = get_object_or_404(Enterprise, id=id)
	except:
		Message.error(request, ("Empresa no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/space/enterprise/index/" #/app/controller_path/action/$params
			return enterprise_index(request)
		else:
			return redirect("/space/enterprise/index/")

	if request.method == "POST":
		try:
			d.name = request.POST.get("name")
			d.tax_id = request.POST.get("tax_id")
			d.type_e = request.POST.get("type_e")
			d.solution_id = request.POST.get("solution_id")
			#solution=Solution.objects.get(id=d.solution_id) #no es necesario

			if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Enterprise.objects.values("name").exclude(id = d.id)
				):
				raise Exception( ("Empresa <b>%(name)s</b> ya existe.") % {"name":d.name} )

			if Enterprise.objects.exclude(id = d.id).filter(tax_id=d.tax_id).count()>0:
				raise Exception( "La empresa con RUC <b>%s</b> ya existe " % (d.tax_id) )

			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Empresa <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})
				if request.is_ajax():
					request.path="/space/enterprise/index/" #/app/controller_path/action/$params
					return enterprise_index(request)
				else:
					return redirect("/space/enterprise/index/")

		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		solution_list = Solution.objects.all().order_by("id")
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Cuenta"),
		"page_title":("Actualizar sede."),
		"d":d,
		"TYPES":Enterprise.TYPES,
		"solution_list":solution_list,
		}
	return render_to_response("space/enterprise/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def enterprise_delete(request, key):
	"""
	Elimina empresa con todas sus sedes
	"""
	id=Security.is_valid_key(request, key, "enterprise_del")
	if not id:
		if request.is_ajax():
			request.path="/space/enterprise/index/" #/app/controller_path/action/$params
			return enterprise_index(request)
		else:
			return redirect("/space/enterprise/index/")
	try:
		d = get_object_or_404(Enterprise, id=id)
	except:
		Message.error(request, ("Empresa no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/space/enterprise/index/" #/app/controller_path/action/$params
			return enterprise_index(request)
		else:
			return redirect("/space/enterprise/index/")
	try:
		association=Association.objects.get(id=DataAccessToken.get_association_id(request.session))
		if Enterprise.objects.filter(headquart__association_id=DataAccessToken.get_association_id(request.session)).count() == 1:
			raise Exception( ("Asociación <b>%(name)s</b> no puede quedar sin ninguna sede asociada.") % {"name":association.name} )		
		d.delete()
		if not d.id:
			Message.info(request,("Empresa <b>%(name)s</b> ha sido eliminado correctamente.") % {"name":d.name}, True)
			if request.is_ajax():
				request.path="/space/enterprise/index/" #/app/controller_path/action/$params
				return enterprise_index(request)
			else:
				return redirect("/space/enterprise/index/")
	except Exception, e:
		transaction.rollback()
		Message.error(request, e)
		if request.is_ajax():
			request.path="/space/enterprise/index/" #/app/controller_path/action/$params
			return enterprise_index(request)
		else:
			return redirect("/space/enterprise/index/")

@permission_resource_required
@transaction.commit_on_success
def enterprise_edit_current(request):
	"""
	Actualiza datos de la empresa a la que ingresó el usuario
	"""
	d = Enterprise()
	try:
		d = get_object_or_404(Enterprise, id=DataAccessToken.get_enterprise_id(request.session))
	except:
		Message.error(request, ("Empresa no seleccionada o no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/home/choice_headquart/" #/app/controller_path/action/$params
			return choice_headquart(request)
		else:
			return redirect("/home/choice_headquart/")

	if request.method == "POST":
		try:
			d.name = request.POST.get("name")
			d.tax_id = request.POST.get("tax_id")
			d.type_e = request.POST.get("type_e")
			d.solution_id = request.POST.get("solution_id")
			d.logo = request.POST.get("empresa_logo")
			#solution=Solution.objects.get(id=d.solution_id) #no es necesario

			if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Enterprise.objects.values("name").exclude(id = d.id)
				):
				raise Exception( ("Empresa <b>%(name)s</b> ya existe.") % {"name":d.name} )

			if Enterprise.objects.exclude(id = d.id).filter(tax_id=d.tax_id).count()>0:
				raise Exception( "La empresa con RUC <b>%s</b> ya existe " % (d.tax_id) )

			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Empresa <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})

		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		solution_list = Solution.objects.all().order_by("id")
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Cuenta"),
		"page_title":("Información de la empresa."),
		"d":d,
		"TYPES":Enterprise.TYPES,
		"solution_list":solution_list,
		}
	return render_to_response("space/enterprise/edit_current.html", c, context_instance = RequestContext(request))

@csrf_exempt
def enterprise_upload(request):
	"""
	Sube logo
	"""
	data = {}
	try:
		filename = Upload.save_file(request.FILES["logo"],"empresas/")
		data ["name"] = "%s"%filename
	except Exception, e:
		Message.error(request, e)
	return HttpResponse(json.dumps(data))
#endregion enterprise

#region association OK
@permission_resource_required
@transaction.commit_on_success
def association_edit_current(request):
	"""
	Actualiza datos de la asociación a la que ingresó el usuario
	"""
	d = Association()
	try:
		d = get_object_or_404(Association, id=DataAccessToken.get_association_id(request.session))
	except:
		Message.error(request, ("Asociación no seleccionada o no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/home/choice_headquart/" #/app/controller_path/action/$params
			return choice_headquart(request)
		else:
			return redirect("/home/choice_headquart/")

	if request.method == "POST":
		try:
			d.name = request.POST.get("name")
			d.type_a = request.POST.get("type_a")
			d.solution_id = request.POST.get("solution_id")
			#solution=Solution.objects.get(id=d.solution_id) #no es necesario
			d.logo = request.POST.get("asociacion_logo")
			if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
				normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Association.objects.values("name").exclude(id = d.id)
				):
				raise Exception( ("Asociación <b>%(name)s</b> ya existe.") % {"name":d.name} )

			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Asociación <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})

		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	try:
		solution_list = Solution.objects.all().order_by("id")
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Cuenta"),
		"page_title":("Información de la asociación."),
		"d":d,
		"TYPES":Association.TYPES,
		"solution_list":solution_list,
		}
	return render_to_response("space/association/edit_current.html", c, context_instance = RequestContext(request))

@csrf_exempt
def association_upload(request):
	"""
	Sube logo
	"""
	data = {}
	try:
		filename = Upload.save_file(request.FILES["logo"],"asociaciones/")
		data ["name"] = "%s"%filename
	except Exception, e:
		Message.error(request, e)
	return HttpResponse(json.dumps(data))
#endregion association

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
		"page_module":("Gestión de soluciones"),
		"page_title":("Listado de soluciones del sistema."),
		"solution_list":solution_list,
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
			d.name = request.POST.get("name")
			d.description = request.POST.get("description")
			if Solution.objects.exclude(id = d.id).filter(name = d.name).count() > 0:
				raise Exception( ("Solución <b>%(name)s</b> ya existe.") % {"name":d.name} )
			d.save()
			if d.id:
				Message.info(request,("Solución <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.name})
				if request.is_ajax():
					request.path="/space/solution/index/" #/app/controller_path/action/$params
					return solution_index(request)
				else:
					return redirect("/space/solution/index/")
		except Exception, e:
			Message.error(request, e)
	c = {
		"page_module":("Gestión de soluciones"),
		"page_title":("Agregar solución."),
		"d":d,
		}
	return render_to_response("space/solution/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
def solution_edit(request, key):
	"""
	Actualiza solución
	"""
	id=Security.is_valid_key(request, key, "solution_upd")
	if not id:
		if request.is_ajax():
			request.path="/space/solution/index/" #/app/controller_path/action/$params
			return solution_index(request)
		else:
			return redirect("/space/solution/index/")
	d = None

	try:
		d = get_object_or_404(Solution, id=id)
	except:
		Message.error(request, ("Solución no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/space/solution/index/" #/app/controller_path/action/$params
			return solution_index(request)
		else:
			return redirect("/space/solution/index/")

	if request.method == "POST":
		try:
			d.name = request.POST.get("name")
			d.description = request.POST.get("description")
			if Solution.objects.exclude(id = d.id).filter(name = d.name).count() > 0:
				raise Exception( ("Solución <b>%(name)s</b> ya existe.") % {"name":d.name} )

			#salvar registro
			d.save()
			if d.id:
				Message.info(request,("Solución <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})
				if request.is_ajax():
					request.path="/space/solution/index/" #/app/controller_path/action/$params
					return solution_index(request)
				else:
					return redirect("/space/solution/index/")

		except Exception, e:
			Message.error(request, e)
	c = {
		"page_module":("Gestión de soluciones"),
		"page_title":("Actualizar solución."),
		"d":d,
		}
	return render_to_response("space/solution/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
def solution_delete(request, key):
	"""
	Elimina solución
	"""
	id=Security.is_valid_key(request, key, "solution_del")
	if not id:
		if request.is_ajax():
			request.path="/space/solution/index/" #/app/controller_path/action/$params
			return solution_index(request)
		else:
			return redirect("/space/solution/index/")
	try:
		d = get_object_or_404(Solution, id=id)
	except:
		Message.error(request, ("Solución no se encuentra en la base de datos."))
		if request.is_ajax():
			request.path="/space/solution/index/" #/app/controller_path/action/$params
			return solution_index(request)
		else:
			return redirect("/space/solution/index/")
	try:
		#rastreando dependencias
		if d.module_set.count() > 0:
			raise Exception( ("Solución <b>%(name)s</b> tiene módulos asignados.") % {"name":d.name} )
		if d.association_set.count() > 0:
			raise Exception( ("Solución <b>%(name)s</b> está asignado en asociaciones.") % {"name":d.name} )
		if d.enterprise_set.count() > 0:
			raise Exception( ("Solución <b>%(name)s</b> está asignado en empresas.") % {"name":d.name} )
		d.delete()
		if not d.id:
			Message.info(request,("Solución <b>%(name)s</b> ha sido eliminado correctamente.") % {"name":d.name}, True)
			if request.is_ajax():
				request.path="/space/solution/index/" #/app/controller_path/action/$params
				return solution_index(request)
			else:
				return redirect("/space/solution/index/")
	except Exception, e:
		Message.error(request, e)
		if request.is_ajax():
			request.path="/space/solution/index/" #/app/controller_path/action/$params
			return solution_index(request)
		else:
			return redirect("/space/solution/index/")
#endregion solution