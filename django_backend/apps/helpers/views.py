# _*_ coding: utf-8 _*_
import json
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404, render,redirect
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required, permission_required


from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import ugettext as _, ungettext 

from django.contrib.sessions.backends.db import SessionStore

from django.conf import settings

import datetime
#import time
#import re

from apps.helpers.message import Message

from django.views.decorators.csrf import csrf_exempt, csrf_protect


#no usado, eliminar
def error(request):
    account = ""
    context = {"account": account}
    return render_to_response("500.html", context, context_instance=RequestContext(request))
