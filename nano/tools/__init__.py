import logging
import unicodedata
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import SiteProfileNotAvailable
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.db.models import get_model

LOG_FORMAT = getattr(settings, 'NANO_LOG_FORMAT', '%(asctime)s %(name)s %(module)s:%(lineno)d %(levelname)s %(message)s')
LOG_FILE = getattr(settings, 'NANO_LOG_FILE', '/tmp/nano.log')
def getLogger(name):
    log_formatter = logging.Formatter(LOG_FORMAT)
    log_handler = logging.FileHandler(LOG_FILE, 'a+')
    log_handler.setFormatter(log_formatter)
    logger = logging.getLogger(name)
    logger.addHandler(log_handler)
    return logger
LOG = getLogger('nano.tools')

def nullfunction(return_this=None, *args, **kwargs):
    "Do-nothing dummy-function"
    return return_this

def pop_error(request):
    error = request.session.get('error', None)
    if 'error' in request.session:
        del request.session['error']
    return error

def asciify(string):
    string = unicodedata.normalize('NFKD', string)
    return string.encode('ascii', 'ignore')

def render_page(request, *args, **kwargs):
    return render_to_response(context_instance=RequestContext(request), *args, **kwargs)

def get_profile_model():
    if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
        return None
    try:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        model = get_model(app_label, model_name)
    except ImportError:
        return None
    except ImproperlyConfigured:
        raise SiteProfileNotAvailable
    return model
Profile = get_profile_model()

def get_user_model():
    app_label, model_name = getattr(settings, 'NANO_USER_MODEL', 'auth.User').split('.')
    return get_model(app_label, model_name)
User = get_user_model()

if 'nano.blog' in settings.INSTALLED_APPS:
    try:
        from nano.blog import add_entry_to_blog
    except ImportError:
        add_entry_to_blog = nullfunction
else:
    add_entry_to_blog = None
