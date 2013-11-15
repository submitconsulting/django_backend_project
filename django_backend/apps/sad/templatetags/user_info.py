# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Tags para mostrar los menús dinámicos en la cabecera principal del sistema
"""
from django import template
from django.template import resolve_variable, Context
import datetime
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session
from django.conf import settings
from apps.sad.security import DataAccessToken
from apps.space.models import Enterprise, Headquart
from apps.helpers.message import Message

register = template.Library()

@register.simple_tag
def get_enterprise(session):
	"""
	Imprime el nombre del enterprise actual 

	Usage::
		
		{% get_enterprise request.session %}

	Examples::

        {% get_enterprise request.session %}

	"""
	enterprise=None
	if DataAccessToken.get_enterprise_id(session):
		try:
			enterprise = Enterprise.objects.get(id=DataAccessToken.get_enterprise_id(session))
		except:
			Message.error(request, ("Empresa no se encuentra en la base de datos."))
		
	return enterprise.name

@register.simple_tag
def get_headquart(session):
	"""
	Imprime el nombre del headquart actual

	Usage::
		
		{% get_headquart request.session %}

	Examples::

        {% get_headquart request.session %}
        
	"""
	headquart=None
	if DataAccessToken.get_headquart_id(session):
		try:
			headquart = Headquart.objects.get(id=DataAccessToken.get_headquart_id(session))
		except:
			Message.error(request, ("Sede no se encuentra en la base de datos."))
		
	return headquart.name
