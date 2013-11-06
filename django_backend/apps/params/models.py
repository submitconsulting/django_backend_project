# _*_ coding: utf-8 _*_
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

#Se crea el modelo tipos de localidades
class LocalityType(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		permissions = (
			
			("localitytype", "Puede hacer TODAS las oper. de tipos d localidades"),
			#("localitytype_index", "Puede ver el index de tipos de localidades"),
			#("localitytype_add", "Puede agregar tipo de localidad"),
			#("localitytype_edit", "Puede actualizar tipos de localidades"),
			#("localitytype_delete", "Puede eliminar tipos de localidades"),
			#("localitytype_report", "Puede reportar tipos de localidades"),
		)

	def __unicode__(self):
		return self.name

#Se crea el modelo para las localidades
class Locality(models.Model):
	"""
	comentario de varias
	líneas
	"""
	name = models.CharField(max_length=50)
	location = models.TextField(blank=True)
	utm = models.CharField(max_length=50, null=True, blank=True)
	msnm = models.FloatField(max_length=50, null=True, blank=True)
	is_active  = models.BooleanField(default=True)
	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)
	locality_type = models.ForeignKey(LocalityType, null=True, blank=True)

	class Meta:
		permissions = (
			("locality", "Puede hacer TODAS las operaciones de localidades"),
			("locality_index", "Puede ver el index de localidades"),
			("locality_add", "Puede agregar localidad"),
			("locality_edit", "Puede actualizar localidades"),
			("locality_delete", "Puede eliminar localidades"),
			("locality_report", "Puede reportar localidades"),
			("locality_state", "Puede inactivar y reactivar localidades"),
			#("locality_change_status", "xPuede cambiar el estado de las localidades"),
			#("locality_close", "xPuede inactivar el estado de las localidades"),
		)

	def __unicode__(self):
		return "%s %s" % (self.name, self.location)
	
	@staticmethod
	def calculatex(a):
		return a

class Person(models.Model):

	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	photo = models.ImageField(upload_to='personas', verbose_name='Foto',default="personas/default.png")
	
	last_headquart_id= models.CharField(max_length=50, null=True, blank=True)
	last_module_id= models.CharField(max_length=50, null=True, blank=True)

	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)

	user = models.OneToOneField(User)

	class Meta:
		permissions = (
			("person", "Puede hacer TODAS las operaciones de personas"),
			#("person_index", "Puede ver el index de personas"),
			#("person_add", "Puede agregar persona"),
			#("person_edit", "Puede actualizar personas"),
			#("person_delete", "Puede eliminar personas"),
			#("person_report", "Puede reportar personas"),
			#("person_list", "xPuede listar personas"),
		)

	def __unicode__(self):
		return self.first_name

	def create_user_profile(sender, instance, created, **kwargs):
		if created :
			Person.objects.create(user=instance)
		post_save.connect(create_user_profile, sender=User)

#mis params tables
class Categoria(models.Model):
	nombre = models.CharField(max_length=50)

	class Meta:
		permissions = (
			("categoria", "Puede hacer TODAS las operaciones de categorias"),
			#("categoria_index", "Puede ver el index de categorias"),
			#("categoria_add", "Puede agregar categoria"),
			#("categoria_edit", "Puede actualizar categorias"),
			#("categoria_delete", "Puede eliminar categorias"),
			#("categoria_report", "Puede reportar categorias"),
		)

	def __unicode__(self):
		return self.nombre
"""
G:\dev\apps\django_backend_project\django_backend>python manage.py syncdb
Creating tables ...
Creating table params_categoria
Creating table maestros_producto
The following content types are stale and need to be deleted:

    sad | resource
    sad | user
    sad | group

Any objects related to these content types by a foreign key will also
be deleted. Are you sure you want to delete these content types?
If you're unsure, answer 'no'.

    Type 'yes' to continue, or 'no' to cancel: no
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)

G:\dev\apps\django_backend_project\django_backend>

y se agregarán las nuevas tablas con sus permissions previamente definidos
"""
