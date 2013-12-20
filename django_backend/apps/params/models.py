# _*_ coding: utf-8 _*_
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class LocalityType(models.Model):
	"""
	Tabla params_localitytype para tipos de localidades. 
	P.e: Departamento, Provincia, Distrito, etc.
	"""
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

class Locality(models.Model):
	"""
	Tabla que contiene localidades o ciudades
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
		)

	def __unicode__(self):
		return "%s %s" % (self.name, self.location)
	
	@staticmethod
	def calculatex(a):
		return a

class Person(models.Model):
	"""
	Tabla que amplía la información de los usuarios del sistema
	"""
	DEFAULT="DNI"
	CE="CE"
	PART_NAC="PART_NAC"
	OTHERS="OTHERS"
	IDENTITY_TYPES = ( # esta variable no está syncdb
        (DEFAULT, "D.N.I."),
        (CE, "C.E."),
        (PART_NAC, "P.NAC."),
        (OTHERS, "Otro.")
    )
	identity_type = models.CharField(max_length=10, choices=IDENTITY_TYPES, default=DEFAULT)# este campo no está syncdb
	identity_num = models.CharField(max_length=20, null=True, blank=True) # este campo no está syncdb
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	photo = models.ImageField(upload_to="personas", verbose_name="Foto",default="personas/default.png")
	
	#is_admin  = models.BooleanField(default=False)
	#last_headquart_id= models.CharField(max_length=50, null=True, blank=True)
	#last_module_id= models.CharField(max_length=50, null=True, blank=True)

	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)

	#user = models.OneToOneField(User, null=True, blank=True)

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

	#def create_user_profile(sender, instance, created, **kwargs):
	#	if created :
	#		Person.objects.create(user=instance)
	#	post_save.connect(create_user_profile, sender=User)

#mis params tables SHOMWARE
class Categoria(models.Model):
	"""
	Tabla para las categorías de los productos del proyecto SHOMWARE
	"""
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
If you"re unsure, answer "no".

    Type "yes" to continue, or "no" to cancel: no
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)

G:\dev\apps\django_backend_project\django_backend>

y se agregarán las nuevas tablas con sus permissions previamente definidos
luego ejecute 
delete from auth_permission where codename like 'add_%'or  codename like 'change_%' or codename like 'delete_%'
"""
