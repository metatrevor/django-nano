from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('nano.privmsg.views',
    (r'^add$',          'add_pm'),
    (r'^(?P<msgid>[1-9][0-9]*)/archive/$', 'move_to_archive'),
    (r'^(?P<msgid>[1-9][0-9]*)/delete/$', 'delete'),
    (r'^(?:(?P<action>(archive|sent))/?)?$', 'show_pms'),
)

