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

def _archive(user, recipient, msgids):
    if recipient != user:
        raise Http404
    if not msgids:
        raise Http404
    pms = PM.objects.filter(recipient=user, id__in=msgids)
    pms.update(recipient_archived=True)

@login_required
def move_to_archive(request, *args, **kwargs):
    recipient = get_user(request, **kwargs)
    msgid = int(kwargs.get(u'msgid', None))
    _archive(request.user, recipient, (msgid,))
    return HttpResponseRedirect('.')

def _delete(user, msgids):
    if not msgids:
        raise Http404
    pms = PM.objects.filter(id__in=msgids)
    rpms = pms.filter(recipient=user).update(recipient_deleted=True)
    spms = pms.filter(sender=user).update(sender_deleted=True)
    pms.delete()

@login_required
def delete(request, *args, **kwargs):
    msgid = int(kwargs.get(u'msgid', None))
    _delete(request.user, (msgid,))
    return HttpResponseRedirect('.')

@login_required
def show_pms(request, *args, **kwargs):
    recipient = get_user(request, **kwargs)
    if recipient != request.user:
        raise Http404
    ACTIONS = {
        u'archive': PM.objects.archived,
        u'sent': PM.objects.sent,
        u'received': PM.objects.received,
    }
    actionstr = kwargs.get(u'action', None) or u'received'
    action = ACTIONS[actionstr]
    messages = action(request.user)
    if request.method == 'POST':
        msgids = request.POST.getlist(u'msgid')
        action = request.POST.get(u'submit')
        #assert False, '%s %s' % (action, msgids)
        if action == u'delete':
            _delete(request.user, msgids)
        elif action == u'archive':
            _archive(request.user, recipient, msgids)
    template = 'privmsg/archive.html'
    data = {'pms': messages,
            'action': actionstr,
            }
    return render_page(request, template, data)

@login_required
def add_pm(request, template='privmsg/add.html', *args, **kwargs):
    form = PMForm()
    recipient = get_user(request, **kwargs)
    if request.method == 'POST':
        form = PMForm(data=request.POST)
        if form.is_valid():
            pm = form.save(commit=False)
            pm.sender = request.user
            pm.recipient = recipient
            pm.save()
            return HttpResponseRedirect('.')
    data = {
            'pms': PM.objects.all(),
            'form': PMForm(),
            'recipient': recipient,
            }

    return render_page(request, template, data)
