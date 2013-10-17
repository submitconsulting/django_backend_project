# _*_ coding: utf-8 _*_
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError

from django.db import transaction, router

from apps.params.models import *
from apps.params.exceptions import *
import datetime
from django.contrib.auth.models import User

class LocalityTypeBusiness:
	@staticmethod
	def initialize():
		"""
		solo para instanciar cuando hacemos add
		"""
		return LocalityType()
	
	@staticmethod
	def get_list():# SELECT * FROM table
		return LocalityType.objects.all()

	@staticmethod
	def get_by_id(id):# SELECT * FROM table WHERE id=@id
		return LocalityType.objects.get(id=id)


class LocalityBusiness:
	@staticmethod
	def initialize():
		return Locality()

	#LocalityBusiness.get_page(p)
	#LocalityBusiness.get_page(p,'code')
	#LocalityBusiness.get_page(p,'code','001')
	@staticmethod
	def get_page(field='name', value='None', order='-id', num_rows=25, page_index=1):
		value = '' if value == 'None' else value # (cond tru)? va:va2
		print ('===Business===');
		print ('field='+field);
		print ('value='+value);
		print ('order='+order);
		print ('');
		rr=Locality.objects.all()
		for r in rr:
			print u"%s %s" % (r.name,r.is_active)

		column_contains = u"%s__%s" % (field,'contains') #SEL-- WHERE name LIKE %an%
		locality_list = Locality.objects.filter(**{ column_contains: value }).order_by(order)
		paginator = Paginator(locality_list, num_rows) # Show 25 contacts per page
		try:
			pager = paginator.page(page_index)
		except PageNotAnInteger:
			pager = paginator.page(1)
		except EmptyPage:
			pager = paginator.page(paginator.num_pages)
		return pager;

	@staticmethod
	def get_list(field='name', value='None', order='-id'):
		value = '' if value == 'None' else value
		column_contains = u"%s__%s" % (field,'contains')
		
		return Locality.objects.filter(**{ column_contains: value }).order_by(order)

	@staticmethod
	def get_by_id(id):
		#Validar id
		if id is None:
			raise LocalityIdentifierCannotBeNullOrEmptyException()

		#Obtener registro si existe
		locality = None
		try:
			locality = Locality.objects.get(id=id)
		except Exception, e:
			locality = None
		
		#Validar registro si existe
		if locality is None:
			raise LocalityNotFoundException()

		return locality

	@staticmethod
	def save(locality):
		#Validar registro que no venga nulo if locality is not None:
		if locality is None:
			raise LocalityCannotBeNullException()

		#TODO No permitir duplicar Code
		#lt=LocalityTypeBusiness.get_list()
		#if Locality.objects.filter(locality_type__in = lt).exclude(id = locality.id).count()>0:
		#	raise LocalityNameAlreadyInUseException(locality.name)

		#No permitir duplicar Name #where name = @name and id != @id
		if Locality.objects.filter(name = locality.name).exclude(id = locality.id).count()>0:
			raise LocalityNameAlreadyInUseException(locality.name) #trhow new TuException()

		locality.save()
		return locality

	@staticmethod
	def delete(id):
		#locality = get_object_or_404(Locality, id=id)
		#Validar id
		if id is None:
			raise LocalityIdentifierCannotBeNullOrEmptyException()

		#Obtener registro si existe
		locality = None
		try:
			locality = Locality.objects.get(id=id)
		except Exception, e:
			locality = None
		
		#Validar registro si existe antes de eliminar
		if locality is None:
			raise LocalityNotFoundException()
		else:
			locality.delete()
		return locality







class TipoBusiness:
	@staticmethod
	def initialize():
		return Tipo()

	@staticmethod
	def get_list():# SELECT * FROM table
		return Tipo.objects.all()

	@staticmethod
	def get_page(field='name', value='None', order='-id', num_rows=25, page_index=1):
		value = '' if value == 'None' else value # (cond tru)? va:va2
 
		column_contains = u"%s__%s" % (field,'contains') #SEL-- WHERE name LIKE %an%

		tipo_list = Tipo.objects.filter(**{ column_contains: value }).order_by(order)
		
		paginator = Paginator(tipo_list, num_rows) # Show 25 contacts per page
		try:
			pager = paginator.page(page_index)
		except PageNotAnInteger:
			pager = paginator.page(1)
		except EmptyPage:
			pager = paginator.page(paginator.num_pages)
		return pager;

	@staticmethod
	def save(tipo):
		#Validar registro que no venga nulo if locality is not None:
		if tipo is None:
			raise TypeCannotBeNullException()

		#TODO No permitir duplicar Code
		#lt=LocalityTypeBusiness.get_list()
		#if Locality.objects.filter(locality_type__in = lt).exclude(id = locality.id).count()>0:
		#	raise LocalityNameAlreadyInUseException(locality.name)

		#No permitir duplicar Name #where name = @name and id != @id
		if Tipo.objects.filter(name = tipo.name).exclude(id = tipo.id).count()>0:
			raise TypeNameAlreadyInUseException(tipo.name) #trhow new TuException()

		tipo.save()
		return tipo

	@staticmethod
	def get_by_id(id):
		#Validar id
		if id is None:
			raise TypeIdentifierCannotBeNullOrEmptyException()

		#Obtener registro si existe
		tipo = None
		try:
			tipo = Tipo.objects.get(id=id)
		except Exception, e:
			tipo = None

		return tipo
 
	@staticmethod
	def delete(id):
		#locality = get_object_or_404(Locality, id=id)
		#Validar id
		if id is None:
			raise TypeIdentifierCannotBeNullOrEmptyException()

		#Obtener registro si existe
		tipo = None
		try:
			tipo = Tipo.objects.get(id=id)
		except Exception, e:
			tipo = None
		
		#Validar registro si existe antes de eliminar
		if tipo is None:
			raise TypeNotFoundException()
		else:
			tipo.delete()
		return tipo
 


class BioTipoBusiness:
	@staticmethod
	def initialize():
		return BioTipo()
	
	@staticmethod
	def get_list():# SELECT * FROM table
		return BioTipo.objects.all()

	@staticmethod
	def get_by_id(id):# SELECT * FROM table WHERE id=@id
		return BioTipo.objects.get(id=id)



class ColorBusiness:
	@staticmethod
	def initialize():

		return Color()
	
	@staticmethod
	def get_list():# SELECT * FROM table
		return Color.objects.all()

	@staticmethod
	def get_by_id(id):# SELECT * FROM table WHERE id=@id
		return Color.objects.get(id=id)



class CalidadBusiness:
	@staticmethod
	def initialize():

		return Calidad()
	
	@staticmethod
	def get_list():# SELECT * FROM table
		return Calidad.objects.all()

	@staticmethod
	def get_by_id(id):# SELECT * FROM table WHERE id=@id
		return Calidad.objects.get(id=id)

































































