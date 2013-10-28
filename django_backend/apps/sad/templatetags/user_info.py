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
def get_grupos(request, url):
	"""
	Genera el menú de Grupos para imprimirlo en header.html
	"""
	sede=None
	if DataAccessToken.get_headquart_id(request.session):
		try:
			sede = Headquart.objects.get(id=DataAccessToken.get_headquart_id(request.session))
		except:
			Message.error(request, ("Sede no se encuentra en la base de datos."))
		

	value = '' 
	w=""
	d = DataAccessToken.get_grupo_id_list(request.session)
	if sede:
		w = (u'		<a href="#" class="dropdown-toggle" data-toggle="dropdown" title ="%s">%s > %s %s<b class="caret"></b></a>'%(sede.association.name, sede.enterprise.name, sede.name, value))
	
	o = ''
	if d :
		for i in d:
			print i
			o = o + (u'<li><a href="%s?grupo=%s">%s/%s</a></li>'%(url, i, sede.name, ""))
	if sede:
		o = o + (u'<li><a href="%s?">%s/Todas las areas</a></li>'%(url, sede.name))
	a = (u'<ul class="nav">'
	u'	<li class="dropdown">'
	u'		%s'
	u'		<ul class="dropdown-menu">'%(w))

	c = (u'		</ul>'
	u'	</li>'
	u'</ul>')
	return "%s%s%s"%(a,o,c)

@register.simple_tag
def get_enterprise(session):
	"""
	Imprime el nombre del enterprise actual 
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
	"""
	headquart=None
	if DataAccessToken.get_headquart_id(session):
		try:
			headquart = Headquart.objects.get(id=DataAccessToken.get_headquart_id(session))
		except:
			Message.error(request, ("Sede no se encuentra en la base de datos."))
		
	return headquart.name
