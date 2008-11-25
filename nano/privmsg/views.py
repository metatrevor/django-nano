from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from nano.tools import getLogger, pop_error, render_page, get_user_model
from nano.privmsg.models import PM
from nano.privmsg.forms import *

def get_user(request, **kwargs):
    User = get_user_model()
    username = kwargs.get(u'username', None) or request.REQUEST.get(u'username', None)
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        pass
    user = kwargs.get(u'user', None) or request.REQUEST.get(u'user', None)
    object_id = kwargs.get(u'object_id', None) or request.REQUEST.get(u'object_id', None)
    uid = filter(None, (user, object_id))[0]
    try:
        return User.objects.get(id=int(uid))
    except User.DoesNotExist:
        return None

@login_required
def move_to_archive(request, *args, **kwargs):
    recipient = get_user(request, **kwargs)
    if recipient != request.user:
        raise Http404
    msgid = kwargs.get(u'msgid', None)
    if not msgid:
        raise Http404
    try:
        pm = PM.objects.get(recipient=request.user, id=int(msgid))
    except PM.DoesNotExist:
        raise Http404
    pm.recipient_archived = True
    pm.save()
    return HttpResponseRedirect('./archive/')

@login_required
def delete(request, *args, **kwargs):
    recipient = get_user(request, **kwargs)
    msgid = kwargs.get(u'msgid', None)
    if not msgid:
        assert False, 'msgid'
        raise Http404
    try:
        pm = PM.objects.get(id=int(msgid))
    except PM.DoesNotExist:
        assert False, 'pm missing'
        raise Http404
    if request.user not in (recipient, pm.sender):
        assert False, 'not authorized'
        raise Http404
    if pm.recipient == request.user:
        pm.recipient_deleted = True
    elif pm.sender == request.user:
        pm.sender_deleted = True
    else:
        assert False, 'else'
    pm.save()
    pm.delete()
    return HttpResponseRedirect('/')

@login_required
def show_pms(request, *args, **kwargs):
    recipient = get_user(request, **kwargs)
    if recipient != request.user:
        raise Http404
    ACTIONS = {
        u'archive': PM.objects.archived,
        u'sent': PM.objects.sender,
        u'received': PM.objects.recipient,
    }
    actionstr = kwargs.get(u'action', None) or u'received'
    action = ACTIONS[actionstr]
    messages = action(request.user)
    template = 'privmsg/archive.html'
    data = {'pms': messages,
            'action': actionstr,
            }
    return render_page(request, template, data)

@login_required
def add_pm(request, *args, **kwargs):
    template = 'privmsg/add.html'
    form = PMForm()
    recipient = get_user(request, **kwargs)
    if request.method == 'POST':
        form = PMForm(data=request.POST)
        if form.is_valid():
            pm = form.save(commit=False)
            pm.sender = request.user
            pm.recipient = recipient
            pm.save()
    data = {
            'pms': PM.objects.all(),
            'form': PMForm(),
            'recipient': recipient,
            }
    return render_page(request, template, data)

