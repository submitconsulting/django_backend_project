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

from apps.maestros.models import Producto
from apps.params.models import Categoria

from apps.space.models import Headquart

#region producto OK
#@csrf_exempt
@login_required(login_url="/account/login/")
@permission_resource_required
def producto_index(request, field="descripcion", value="None", order="-id"):
	"""
	Página principal para trabajar con productos
	"""
	try:
		d = get_object_or_404(Headquart, id=DataAccessToken.get_headquart_id(request.session))
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
		producto_list = Producto.objects.filter(**{ column_contains: value_f }).order_by("pos").order_by(order)
		paginator = Paginator(producto_list, 125)
		try:
			producto_page = paginator.page(request.GET.get("page"))
		except PageNotAnInteger:
			producto_page = paginator.page(1)
		except EmptyPage:
			producto_page = paginator.page(paginator.num_pages)
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Gestión de productos"),
		"page_title":("Listado de productos."),
		
		"producto_page":producto_page,
		#"MODULES":dict((x, y) for x, y in Module.MODULES),
		"field":field,
		"value":value.replace("/", "-"),
		"order":order,
		}
	return render_to_response("maestros/producto/index.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def producto_add(request):
	"""
	Agrega Producto
	"""
	d = Producto()
	d.descripcion=""
	if request.method == "POST":
		try:
			
			d.codigo = request.POST.get("codigox")
			d.descripcion = request.POST.get("descripcion")
			d.precio_venta = request.POST.get("precio_venta")
			d.headquart_id = DataAccessToken.get_headquart_id(request.session)
			
			if request.POST.get("categoria_nombre"):
				d.categoria, is_created  = Categoria.objects.get_or_create(
					nombre=request.POST.get("categoria_nombre"),
					)

			if Producto.objects.filter(codigo = d.codigo).exclude(id = d.id).count()>0:
				raise Exception( "El producto <b>%s</b> ya existe " % d.codigo )
			d.save()
			if d.id:
				Message.info(request,("Producto <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.codigo}, True)
				return Redirect.to_action(request, "index")
		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	categoria_nombre_list=[]
	try:
		categoria_nombre_list = json.dumps(list(col["nombre"]+""  for col in Categoria.objects.values("nombre").filter().order_by("nombre")))
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Gestión de usuarios"),
		"page_title":("Agregar usuario."),
		"d":d,
		"categoria_nombre_list":categoria_nombre_list,
		}
	return render_to_response("maestros/producto/add.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def producto_edit(request, key):
	"""
	Actualiza Producto
	"""
	id=Security.is_valid_key(request, key, "producto_upd")
	if not id:
		return Redirect.to_action(request, "index")
	d = None
	try:
		d = get_object_or_404(Producto, id=id)
		try:
			categoria = Categoria.objects.get(id=d.categoria.id)
			if categoria.id:
				d.categoria_nombre = d.categoria.nombre
		except:
			pass
		
		
	except Exception, e:
		Message.error(request, ("Usuario no se encuentra en la base de datos. %s" % e))
		return Redirect.to_action(request, "index")

	if request.method == "POST":
		try:
			d.codigo = request.POST.get("codigox")
			d.descripcion = request.POST.get("descripcion")
			d.precio_venta = request.POST.get("precio_venta")
			d.headquart_id = DataAccessToken.get_headquart_id(request.session)
			
			if request.POST.get("categoria_nombre"):
				d.categoria, is_created  = Categoria.objects.get_or_create(
					nombre=request.POST.get("categoria_nombre"),
					)

			if Producto.objects.filter(codigo = d.codigo).exclude(id = d.id).count()>0:
				raise Exception( "El producto <b>%s</b> ya existe " % d.codigo )
			d.save()
			if d.id:
				Message.info(request,("Producto <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.codigo}, True)
				return Redirect.to_action(request, "index")

		except Exception, e:
			transaction.rollback()
			Message.error(request, e)
	categoria_nombre_list=[]
	try:
		categoria_nombre_list = json.dumps(list(col["nombre"]+""  for col in Categoria.objects.values("nombre").filter().order_by("nombre")))
	except Exception, e:
		Message.error(request, e)
	c = {
		"page_module":("Gestión de productos"),
		"page_title":("Actualizar producto."),
		"d":d,
		"categoria_nombre_list":categoria_nombre_list,
		}
	return render_to_response("maestros/producto/edit.html", c, context_instance = RequestContext(request))

@permission_resource_required
@transaction.commit_on_success
def producto_delete(reqproductoest, key):
	"""
	Elimina producto
	"""
	id=Security.is_valid_key(request, key, "producto_del")
	if not id:
		return Redirect.to_action(request, "index")
	try:
		d = get_object_or_404(Producto, id=id)
	except:
		Message.error(request, ("Producto no se encuentra en la base de datos."))
		return Redirect.to_action(request, "index")
	try:
		d.delete()
		if not d.id:
			Message.info(request,("Producto <b>%(username)s</b> ha sido eliminado correctamente.") % {"username":d.codigo}, True)
			return Redirect.to_action(request, "index")
	except Exception, e:
		Message.error(request, e)
		return Redirect.to_action(request, "index")
#endregion producto