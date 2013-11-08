# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     space

Descripcion: Base de datos para multisedes administrados por empresas y/o asociaciones
"""
from django.db import models
from django.contrib.auth.models import User
from apps.params.models import *


class Solution(models.Model):
	"""
	Tabla que contiene las soluciones o planes o servicios del sistema
	"""
	name = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	is_active  = models.BooleanField(default=True)

	class Meta:
		permissions = (
			("solution", "Puede hacer TODAS las operaciones de soluciones"),
			#("solution_index", "Puede ver el index de soluciones"),
			#("solution_add", "Puede agregar solucion"),
			#("solution_edit", "Puede actualizar soluciones"),
			#("solution_delete", "Puede eliminar soluciones"),
			#("solution_state", "Puede inactivar y reactivar soluciones"),
			#("solution_report", "Puede reportar soluciones"),
		)

	def __unicode__(self):
		return self.name

class Association(models.Model):
	"""
	Tabla que contiene las asociaciones suscritas a un plan
	"""
	GOVERMENT="GOVERMENT"
	PRIVATE="PRIVATE"
	MIXED="MIXED"
	OTHERS="OTHERS"
	TYPES = (
        (GOVERMENT, "Gobierno"),
        (PRIVATE, "Privada"),
        (MIXED, "Mixto"),
        (OTHERS, "Otros")
    )
	name = models.CharField(max_length=50)
	logo = models.ImageField(upload_to="asociaciones", verbose_name="Logo", default="asociaciones/default.png")
	type_a = models.CharField(max_length=10, choices=TYPES, default=PRIVATE)
	is_active  = models.BooleanField(default=True)

	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)

	solution = models.ForeignKey(Solution, null=True, blank=True)

	class Meta:
		permissions = (
			("association", "Puede hacer TODAS las operaciones de asociaciones"),
			#("association_index", "Puede ver el index de asociaciones"),
			#("association_add", "Puede agregar asociacion"),
			#("association_edit", "Puede actualizar asociaciones"),
			#("association_delete", "Puede eliminar asociaciones"),
			#("association_state", "Puede inactivar y reactivar asociaciones"),
			#("association_report", "Puede reportar asociaciones"),
		)

	def __unicode__(self):
		return self.name

class Enterprise(models.Model):
	"""
	Tabla que contiene las empresas suscritas a un plan
	"""
	GOVERMENT="GOVERMENT"
	PRIVATE="PRIVATE"
	MIXED="MIXED"
	OTHERS="OTHERS"
	TYPES = (
        (GOVERMENT, "Gobierno"),
        (PRIVATE, "Privada"),
        (MIXED, "Mixto"),
        (OTHERS, "Otros")
    )
	name = models.CharField(max_length=50)
	logo = models.ImageField(upload_to="empresas", verbose_name="Logo", default="empresas/default.png")
	tax_id = models.CharField(max_length=50)
	type_e = models.CharField(max_length=10, choices=TYPES, default=PRIVATE)
	is_active  = models.BooleanField(default=True)

	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)

	solution = models.ForeignKey(Solution, null=True, blank=True)

	class Meta:
		permissions = (
			("enterprise", "Puede hacer TODAS las operaciones de empresas"),
			#("enterprise_index", "Puede ver el index de empresas"),
			#("enterprise_add", "Puede agregar empresa"),
			#("enterprise_edit", "Puede actualizar empresas"),
			#("enterprise_delete", "Puede eliminar empresas"),
			#("enterprise_state", "Puede inactivar y reactivar empresas"),
			#("enterprise_report", "Puede reportar empresas"),
		)

	def __unicode__(self):
		return self.name

class Headquart(models.Model):
	"""
	Tabla que contiene las sedes de las empresas, asociadas a una Asociación
	Un Headquart o sede o sucursal, es la unidad principal del sistema
	Los accesos del sistema serán entregados a un Headquart
	"""
	name = models.CharField(max_length=50)

	phone = models.CharField(max_length=50, null=True, blank=True)

	address = models.TextField(null=True, blank=True)
	is_main  = models.BooleanField(default=True)
	is_active  = models.BooleanField(default=True)

	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)

	locality = models.ForeignKey(Locality, null=True, blank=True)
	association = models.ForeignKey(Association, null=True, blank=True)
	enterprise = models.ForeignKey(Enterprise)

	class Meta:
		permissions = (
			("headquart", "Puede hacer TODAS las operaciones de sedes"),
			#("headquart_index", "Puede ver el index de sedes"),
			#("headquart_add", "Puede agregar sede"),
			#("headquart_edit", "Puede actualizar sedes"),
			#("headquart_delete", "Puede eliminar sedes"),
			#("headquart_state", "Puede inactivar y reactivar sedes"),
			#("headquart_report", "Puede reportar sedes"),
		)

	def __unicode__(self):
		return "%s %s-%s (%s-%s)" % (self.name, self.enterprise.name, self.enterprise.solution.name,  self.association.name, self.association.solution.name)

'''
class Empleado(models.Model):
	"""
	Tabla que contiene los empleados de la empresa, implementar la app empleado
	"""
	codigo = models.CharField(max_length=50)
	contrato_vigente  = models.BooleanField(default=False)
	
	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)
	
	headquart = models.ForeignKey(Headquart)
	person = models.OneToOneField(Person)
	#usuario = models.ForeignKey(User)

	class Meta:
		permissions = (
			("empleado", "Puede hacer TODAS las operaciones de empleados"),
			("empleado_index", "Puede ver el index de empleados"),
			("empleado_add", "Puede agregar empleado"),
			("empleado_edit", "Puede actualizar empleados"),
			("empleado_delete", "Puede eliminar empleados"),
			("empleado_state", "Puede inactivar y reactivar contrato"),
			#("empleado_report", "Puede reportar empleados"),
		)

	def __unicode__(self):
		return "%s %s" % (self.codigo, self.contrato_vigente)
'''
