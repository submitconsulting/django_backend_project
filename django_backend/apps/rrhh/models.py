# _*_ coding: utf-8 _*_
from django.db import models
#from django.contrib.auth.models import User
from apps.params.models import Person
from apps.space.models import Headquart #Association, Enterprise, 

class Employee(models.Model):
	"""
	Tabla que contiene los empleados de la empresa, específicamente de la sede
	"""
	codigo = models.CharField(max_length=50)
	contrato_vigente  = models.BooleanField(default=True)
	
	registered_at = models.DateTimeField(auto_now_add=True)
	modified_in = models.DateTimeField(auto_now=True)
	
	headquart = models.ForeignKey(Headquart)
	person = models.OneToOneField(Person)
	#usuario = models.ForeignKey(User)

	class Meta:
		permissions = (
			("employee", "Puede hacer TODAS las operaciones de empleados"),
			#("empleado_index", "Puede ver el index de empleados"),
			#("empleado_add", "Puede agregar empleado"),
			#("empleado_edit", "Puede actualizar empleados"),
			#("empleado_delete", "Puede eliminar empleados"),
			##("empleado_state", "Puede inactivar y reactivar contrato"),
			#("empleado_report", "Puede reportar empleados"),
		)

	def __unicode__(self):
		return "%s %s" % (self.codigo, self.contrato_vigente)
