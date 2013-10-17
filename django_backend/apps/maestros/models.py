# _*_ coding: utf-8 _*_
from django.db import models
from django.contrib.auth.models import User
from apps.params.models import *
from apps.space.models import *

class Producto(models.Model):
	"""
	
	"""
	
	codigo = models.CharField(max_length=50)
	descripcion = models.TextField(null=True, blank=True)
	precio_venta = models.FloatField (null=True, blank=True)
	esta_activo  = models.BooleanField(default=True)

	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)
	categoria = models.ForeignKey(Categoria, null=True, blank=True)

	class Meta:
		permissions = (
			("producto", "Puede hacer TODAS las operaciones de productos"),
			("producto_index", "Puede ver el index de productos"),
			("producto_add", "Puede agregar producto"),
			("producto_edit", "Puede actualizar productos"),
			("producto_delete", "Puede eliminar productos"),
			("producto_report", "Puede reportar productos"),
			#Pa agregar más permissions solo vuelva a hacer >python manage.py syncdb y no tiene que borrar la db
			#("producto_list", "xPuede listar productos"),
			#("producto_list_json", "xPuede listar productos en formato JSON"),
			#("producto_edit_precio", "xPuede actualizar precio de productos"),
		)

	def __unicode__(self):
		return self.descripcion
