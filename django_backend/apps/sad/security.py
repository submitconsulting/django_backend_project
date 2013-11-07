# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Clases para controlar la seguridad de la información en la nube

"""
from apps.helpers.message import Message
import datetime
import random
import sys
import hashlib
from apps.sad.models import *
from array import *

reload(sys)
sys.setdefaultencoding('utf-8')

class DataAccessToken:


	@staticmethod
	def set_association_id(request, association_id):
		request.session['association_id'] = association_id

	@staticmethod
	def get_association_id(session):
		return session.get('association_id', False)
	
	@staticmethod
	def set_enterprise_id(request, enterprise_id):
		request.session['enterprise_id'] = enterprise_id

	@staticmethod
	def get_enterprise_id(session):
		return session.get('enterprise_id', False)

	@staticmethod
	def set_headquart_id(request, headquart_id):
		request.session['headquart_id'] = headquart_id

	@staticmethod
	def get_headquart_id(session):
		return session.get('headquart_id', False)

	@staticmethod
	def set_grupo_id_list(request	, grupo_id_list):
		request.session['grupo_id_list'] = grupo_id_list

	@staticmethod
	def get_grupo_id_list(session):
		return session.get('grupo_id_list', False)

# Create your models here.
class SessionContext:
	@staticmethod
	def eeee(request, msg, audit=False):
		request.session['flash_msg'] = msg

class Security:
	"""
		Clase que permite crear llave de seguridad en las url.
	"""
	TEXT_KEY = 'lyHyRajh987r.P~CFCcJ[AvFKdz|86'

	#Método para generar las llaves de seguridad
	@staticmethod
	def get_key(id, action_name):
		key="%s%s" % (Security.TEXT_KEY, datetime.datetime.now().strftime('%Y-%m-%d'))

		m = hashlib.md5("%s%s%s" % (id, key, action_name) )
		key=m.hexdigest()
		tam = len(key)
		#    path = path[1:] #quitando / del extremo izq
        #if path.endswith("/"):
        #    path = path[:-1] #quitando / del extremo der

        #return $id.'.'.substr($key,0,6).substr($key,$tam-6, $tam);
		return u"%s.%s" % (id, key)

	#Método para verificar si la llave es válida
	@staticmethod
	def is_valid_key(request, key_value, action_name):
		key = key_value.split('.')
		id=key[0]
		valid_key=Security.get_key(id, action_name)
		valid = (True if valid_key==key_value else False)
		if not valid:
			Message.info(request,('Acceso denegado. La llave de seguridad es incorrecta.'))
			return False
		#print 'key_value(%s) = valid_key(%s)' % (key_value, valid_key)
		#Message.info(request,('key_value(%s) = valid_key(%s)' % (key_value, valid_key)))
		return id

class Menus:
	"""
		Clase que permite renderizar los menús.
	"""
	menu_module = '' #Variable para indicar el entorno
	menu_list = [] #Variable que contiene los menús 
	menu_item_list = {} #Variable que contien los items del menú

	#Método para cargar en variables los menús
	@staticmethod
	def load(request, menu_module): #TODO filtar por usuarios
		Menus.menu_module=menu_module
		print "\n\n\n"
		print "user=%s"%request.user

		menu = Menu()
		#if not Menus.menu_list:
		Menus.menu_list = Menu.objects.filter(parent_id=None, module=menu_module).order_by("pos")
		#print Menus.menu_list
		if Menus.menu_list: #not Menus.menu_item_list and 
			for menu in Menus.menu_list:
				Menus.menu_item_list[menu.title] = Menu.objects.filter(parent_id=menu.id).exclude(parent_id=None).order_by("pos") #.lower().replace(" ","_")
		#print Menus.menu_item_list


		return ""

	#Método para renderizar el menú de escritorio
	@staticmethod
	def desktop(request):
		html = ''
		route = request.path;
		if Menus.menu_list:
			html= html + '<ul class="nav">'
			
			for main in Menus.menu_list:

				active = ('active' if main.url==route else '')
				html= html + '<li class="%s">%s</li>\n' %(active,Menus.linkdf(main.url, main.title, main.icon))
			html = html + '</ul>\n'
		return html

	@staticmethod
	def linkdf(action, text, icon):#, attrs = None, icon='', loadAjax=True
		action = ('/%s' % action if action != '#' else '#')
		texti=""
		if icon:
			texti='<i class="%s icon-expand"></i>' % icon
		html = '<a href="%s"  class="dw-spinner dw-ajax main-menu-link" data-filter="sub-menu-%s" >%s %s</a>\n'%(action, text.lower().replace(" ","_"), texti, text )
		return html

	@staticmethod
	def link(action, text, icon):#, attrs = None, icon='', loadAjax=True
		action = ('/%s' % action if action != '#' else '#')
		texti=""
		if icon:
			texti='<i class="%s icon-expand"></i>' % icon
		html = '<a href="%s"  class="dw-spinner dw-ajax" >%s %s</a>\n'%(action, texti, text )
		return html

	@staticmethod
	def linknoajax(action, text, icon):#, attrs = None, icon='', loadAjax=True
		action = ('/%s' % action if action != '#' else '#')
		texti=""
		if icon:
			texti='<i class="%s icon-expand"></i>' % icon
		html = '<a href="%s"  class="dw-spinner" >%s %s</a>\n'%(action, texti, text )
		return html

	@staticmethod
	def linkphone(action, text, icon):#, attrs = None, icon='', loadAjax=True
		action = ('/%s' % action if action != '#' else '#')
		texti=""
		if icon:
			texti='<i class="%s icon-expand"></i>' % icon
		html = '<a href="%s" class="dropdown-toggle" data-toggle="dropdown">%s %s</a>\n'%(action, texti, text )
		return html

	#Método para listar los items en el backend
	@staticmethod
	def desktop_items(request):
		html = ''
		route = request.path;
		for menu,items in Menus.menu_item_list.iteritems():
			html= html + '<div id="sub-menu-%s" class="subnav hidden">\n'% menu.lower().replace(" ","_")
			html= html + '<ul class="nav nav-pills">\n'
			
			if menu in Menus.menu_item_list:
				for item in Menus.menu_item_list[menu]:
					active = ('active' if item.url==route else '')
					html= html + '<li class="%s">%s</li>\n' %(active,Menus.link(item.url, item.title, item.icon))
			html = html + '</ul>\n'
			html = html + '</div>\n'
		return html


	#Método para renderizar el menú de dispositivos móviles
	@staticmethod
	def phone(request):
		html = ''
		route = request.path;
		if Menus.menu_list:
			html= html + '<ul class="nav pull-right">\n'
			for main in Menus.menu_list:
				text ='%s<b class="caret"></b>' % main.title
				html= html + '<li class="dropdown">\n'
				html= html + Menus.linkphone('#', text, None)
				if main.title in Menus.menu_item_list:
					html= html + '<ul class="dropdown-menu">\n'
					for item in Menus.menu_item_list[main.title]:
						active = ('active' if item.url==route else '')
						html= html + '<li class="%s">%s</li>\n' %(active,Menus.link(item.url, item.title, item.icon))
					html = html + '</ul>\n'
				html = html + '</li>\n'
			html= html + '</ul>\n'
		return html