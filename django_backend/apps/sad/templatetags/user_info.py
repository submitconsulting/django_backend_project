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

register = template.Library()

@register.simple_tag
def get_grupos(request, url):
	"""
	Genera el menú de Grupos para imprimirlo en header.html
	"""
	sede=None
	if DataAccessToken.get_headquart_id(request.session):
		sede = Headquart.objects.get(id=DataAccessToken.get_headquart_id(request.session))

	value = '' 
	w=""
	d = DataAccessToken.get_grupo_id_list(request.session)
	if sede:
		w = (u'		<a href="#" class="dropdown-toggle" data-toggle="dropdown">%s > %s %s<b class="caret"></b></a>'%(sede.enterprise.name, sede.name, value))
	
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
		enterprise = Enterprise.objects.get(id=DataAccessToken.get_enterprise_id(session))
	return enterprise.name

@register.simple_tag
def get_headquart(session):
	"""
	Imprime el nombre del headquart actual
	"""
	headquart=None
	if DataAccessToken.get_headquart_id(session):
		headquart = Headquart.objects.get(id=DataAccessToken.get_headquart_id(session))
	return headquart.name
