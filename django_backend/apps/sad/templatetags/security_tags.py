# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Filtros se seguridad de la información

"""
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

	Usage::

		{% url 'controller_name' id_value|key:'action_name' %}

	Example::

		{% url 'locality_edit' d.id|key:'locality_upd' %}

	"""
	
	return Security.get_key(id, action_name)

@register.filter(name='get_dict_value')
def get_dict_value(dictionary, key):
	"""
	Devuelve el VALUE buscado por su KEY de un dict

	Usage::

		{{ DICT_LIST|get_dict_value:key_dict }}
		mejor use {{ d.get_<colum>_display }}

	Example::

		{{ MODULES|get_dict_value:d.module }}
		mejor use {{ d.get_module_display }}
	"""
	try:
		return dictionary[key]
	except:
		return ""