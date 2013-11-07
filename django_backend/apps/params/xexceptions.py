# _*_ coding: utf-8 _*_
from django.utils.translation import ugettext as _

# Locality exceptions class A extends Exception { .. }
class LocalityCannotBeNullException(Exception):
	def __init__(self):
		self.parameter = _("Locality cannot be null.")
	def __str__(self):
		return self.parameter

class LocalityIdentifierCannotBeNullOrEmptyException(Exception):
	def __init__(self):
		self.parameter = _("Locality identifier cannot be null.")
	def __str__(self):
		return self.parameter

class LocalityNotFoundException(Exception):
	def __init__(self):
		self.parameter = _("Locality not found in the database.")
	def __str__(self):
		return self.parameter

class LocalityCodeAlreadyInUseException (Exception):
	def __init__(self, code):
		self.parameter = _("Locality %(code)s code's already in use.") % {'code':code}
	def __str__(self):
		return self.parameter

class LocalityNameAlreadyInUseException (Exception):
	def __init__(self, name):
		self.parameter = _("Locality %(name)s name's already in use.") % {'name':name}
	def __str__(self):
		return self.parameter

class LocalityCouldNotBeDeletedException(Exception):
	def __init__(self, name):
		self.parameter = _("Locality %(name)s could not be deleted because it has associated records.") % {'name':name}
	def __str__(self):
		return self.parameter

class LocalityOtherException(Exception):
	def __init__(self):
		self.parameter = _("Locality other exception.")
	def __str__(self):
		return self.parameter

# Fin Locality exceptions

# class CustomException(Exception):
# 	def __init__(self, value, value2):
# 		self.parameter = "El %s no se puede save %s" % (value,value2)
# 	def __str__(self):
# 		return self.parameter

# Desarrolle aquí tus exceptions

