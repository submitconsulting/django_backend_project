# _*_ coding: utf-8 _*_
from django.db import models
from django.contrib.auth.models import User, Group, Permission 
from apps.space.models import Solution, Enterprise, Headquart
from apps.space.models import Association, Empleado
# Create your models here.
class Module(models.Model):
	"""
	Módulos del sistema
	"""
	WEB ='WEB'
	VENTAS ='VENTAS'
	DBM ='DBM'
	MODULES = (
        (WEB, 'Web informativa'),
        (VENTAS, 'Ventas'),
        (DBM, 'Backend Manager'),
    )
	module = models.CharField(max_length=50, choices=MODULES, default=DBM)
	name = models.CharField(max_length=50)
	is_active  = models.BooleanField(default=True)
	icon = models.TextField(max_length=50, null=True, blank=True)
	description = models.TextField(max_length=50, null=True, blank=True)
	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)

	solutions = models.ManyToManyField(Solution,verbose_name='solutions',null=True,  blank=True)
	groups = models.ManyToManyField(Group,related_name='groups',verbose_name='groups',null=True,  blank=True)
	initial_groups = models.ManyToManyField(Group,related_name='initial_groups',verbose_name='initial_groups',null=True,  blank=True)
	#user = models.ForeignKey(User) #para saber quien registró

	class Meta:
		permissions = (
			("module", "Puede hacer TODAS las operaciones de modulos"),
			("module_index", "Puede ver el index de modulos"),
			("module_add", "Puede agregar modulo"),
			("module_edit", "Puede actualizar modulos"),
			("module_delete", "Puede eliminar modulos"),
			#("module_report", "Puede reportar modulos"),
			("module_plans_edit", "Puede configurar planes basado en modulos"),
		)

	def __unicode__(self):
		return "%s %s" % (self.module, self.name)



class Menu(models.Model):
	"""
	Menús del sistema. 
	"""
	WEB ='WEB'
	VENTAS ='VENTAS'
	DBM ='DBM'
	MODULES = (
        (WEB, 'Web informativa'),
        (VENTAS, 'Ventas'),
        (DBM, 'Backend Manager'),
    )
	module = models.CharField(max_length=50, choices=MODULES, default=DBM)
	title = models.CharField(max_length=50)
	url = models.CharField(max_length=150,default='#')
	pos = models.IntegerField(max_length=50,default=0)
	icon = models.TextField(max_length=50, null=True, blank=True)
	is_active  = models.BooleanField(default=True)
	description = models.TextField(max_length=50, null=True, blank=True)

	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)
	permission = models.ForeignKey(Permission,null=True,  blank=True)
	parent = models.ForeignKey('Menu',verbose_name='parent',null=True,  blank=True) #related_name='parent',
	#user = models.ForeignKey(User) #para saber quien registró
	class Meta:
		permissions = (
			("menu", "Puede hacer TODAS las operaciones de menús"),
			("menu_index", "Puede ver el index de menús"),
			("menu_add", "Puede agregar menú"),
			("menu_edit", "Puede actualizar menús"),
			("menu_delete", "Puede eliminar menús"),
			#("menu_report", "Puede reportar menús"),
		)

	def __unicode__(self):
		return "%s %s" % (self.module, self.title)



class UserProfileEnterprise(models.Model):
	"""
	Permisos a nivel de empresa
	"""
	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)

	user = models.ForeignKey(User)
	group = models.ForeignKey(Group)
	enterprise = models.ForeignKey(Enterprise)

	class Meta:
		permissions = (
			("userprofileenterprise", "Puede hacer TODAS las operaciones de userprofileenterprise"),
			#("userprofileenterprise_view", "Puede ver userprofileenterprise"),
			#("userprofileenterprise_add", "Puede agregar userprofileenterprise"),
			#("userprofileenterprise_edit", "Puede actualizar userprofileenterprise"),
			#("userprofileenterprise_delete", "Puede eliminar userprofileenterprise"),
		)

	def __unicode__(self):
		return "%s %s - %s" % (self.user.username, self.group.name, self.enterprise.name)

class UserProfileHeadquart(models.Model):
	"""
	Permisos a nivel de sede
	"""
	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)

	user = models.ForeignKey(User)
	group = models.ForeignKey(Group)
	headquart = models.ForeignKey(Headquart)

	class Meta:
		permissions = (
			("userprofileheadquart", "Puede hacer TODAS las operaciones de userprofileheadquart"),
			#("userprofileheadquart_view", "Puede ver userprofileheadquart"),
			#("userprofileheadquart_add", "Puede agregar userprofileheadquart"),
			#("userprofileheadquart_edit", "Puede actualizar userprofileheadquart"),
			#("userprofileheadquart_delete", "Puede eliminar userprofileheadquart"),
		)

	def __unicode__(self):
		return "%s %s - %s" % (self.user.username, self.group.name, self.headquart.name)

#others
class UserProfileAssociation(models.Model):
	"""
	Permisos a nivel de association
	"""
	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)

	user = models.ForeignKey(User)
	group = models.ForeignKey(Group)
	association = models.ForeignKey(Association)

	class Meta:
		permissions = (
			("userprofileassociation", "Puede hacer TODAS las operaciones de userprofileassociation"),
			#("userprofileassociation_view", "Puede ver userprofileassociation"),
			#("userprofileassociation_add", "Puede agregar userprofileassociation"),
			#("userprofileassociation_edit", "Puede actualizar userprofileassociation"),
			#("userprofileassociation_delete", "Puede eliminar userprofileassociation"),
		)

	def __unicode__(self):
		return "%s %s - %s" % (self.user.username, self.group.name, self.association.name)




