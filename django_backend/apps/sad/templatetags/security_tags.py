# -*- coding: utf-8 -*-
# método para mostrar en los template
from django import template
from django.template import resolve_variable, Context
import datetime
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session
from django.conf import settings
from apps.sad.security import DataAccessToken
from apps.space.models import Enterprise, Headquart

from django.template.defaultfilters import stringfilter

from apps.helpers.message import Message
from apps.sad.security import Security

register = template.Library()

@register.filter
#@stringfilter
def key(id, action_name):
	"""
	Muestra la llave de seguridad generada por la clase Security del componente SAD
	"""
	
	return Security.get_key(id, action_name)

@register.filter(name='get_dict_value')
def get_dict_value(dictionary, key):
	"""
	devuelve el valor del key de un dict
	"""
	try:
		return dictionary[key]
	except:
		return ""