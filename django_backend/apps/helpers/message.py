# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     helpers

Descripcion: Registra en archivos .txt, según el tipo de mensaje, las acciones de los usuarios
"""
import logging, logging.handlers
import datetime
from django.utils.html import escape
from django.template.defaultfilters import removetags

#from django.conf import settings
from locale import setlocale, LC_ALL, LC_TIME
from apps.helpers.util import EncodingFormatter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#setlocale(LC_TIME, '') #no se puede para mié tildes, no usar aqui
#print sys.getdefaultencoding()
# create logger
logger = logging.getLogger('sistema')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)

# create file handler and set level to debug
fh = logging.FileHandler('temp/logs/audit%s.txt' % (datetime.datetime.now().strftime("%Y-%m-%d"))) #, "a", encoding = "UTF-8" 
fh.setLevel(logging.DEBUG)
#fh.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
#ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] [%(name)s] %(message)s')
#formatter = logging.Formatter('[%(asctime)s.%(msecs)d][%(levelname)s] [%(name)s] %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
#formatter = logging.Formatter('[%(asctime)s.%(msecs)d][%(levelname)s] [%(name)s] %(message)s', datefmt='%a, %d %b %y %H:%M:%S')
#formatter = EncodingFormatter('[%(asctime)s][%(levelname)s] [%(name)s] %(message)s', datefmt='%a, %d %b %y %H:%M:%S', encoding='utf-8') #, datefmt='%a, %d %b %y %H:%M:%S'
# add formatter to fh and ch
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add fh and ch to logger
logger.addHandler(fh)
logger.addHandler(ch)

class Message:
   	"""
	Clase para la gestión de mensajería instantánea del sistema

	Usage::

	    from apps.helpers.message import Message
	    Message.info(request,"message")

	"""
	content_msj = []

	@staticmethod
	def set_msg(request, name, msg, audit=False):
		"""
		Método interno, que asigna el mensaje en la variable content_msj 
	    y, deacuerdo al tipo de mensaje recibido en name, guarda en 
	    logger.info() #por ejemplo.
		"""

		try:
			d = request.session['messages']
			if d:
				Message.content_msj = request.session['messages']
		except KeyError:
			pass
		Message.content_msj.append(
			(u''
			u'<div class="alert alert-block alert-%s"><button type="button" class="close" data-dismiss="alert">×</button>%s</div>'
			u'' % (name, msg))
			)
		request.session['messages'] = Message.content_msj
		#m = __import__ ('logger')
		if audit:
			methodToCall = getattr(logger, name) #logger.debug donde name=debug p.e.
			methodToCall(("[%s][%s][%s] %s ") % (request.get_full_path(), request.user, request.META['REMOTE_ADDR'], removetags(msg,'b') ) ) #logger.debug(msg) #(str(u'%s'%msg)).encode('utf-8')

	@staticmethod
	def clean(request):
		try:
			del request.session['messages']
			Message.content_msj = []
		except KeyError:
			pass


	@staticmethod
	def debug(request, msg, audit=True):
		#logger.debug("%s - %s"%(request.user, msg))
		Message.set_msg(request, "debug", msg, audit)

	@staticmethod
	def info(request, msg, audit=False):

		#logger.info("%s - %s"%(request.user, msg))
		Message.set_msg(request, "info", msg, audit)

	@staticmethod
	def warning(request, msg, audit=True):
		#logger.warning("%s - %s"%(request.user, msg))
		Message.set_msg(request, "warning", msg, audit)

	@staticmethod
	def error(request, msg, audit=True):
		#logger.error("%s - %s"%(request.user, msg))
		Message.set_msg(request, "error", msg, audit)
		

	@staticmethod
	def critical(request, msg, audit=True):
		#logger.critical("%s - %s"%(request.user, msg))
		Message.set_msg(request, "critical", msg, audit)

