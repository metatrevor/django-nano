from random import choice, sample
import string

from django.contrib import auth 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from nano.tools import *
from nano.user.forms import *

Profile = get_profile_model()

class NanoUserError(Exception):
    pass

class NanoUserExistsError(NanoUserError):
    pass

def pop_error(request):
    error = request.session.get('error', None)
    if 'error' in request.session:
        del request.session['error']
    return error

def random_password():
    sample_space = string.letters + string.digits + r'!#$%&()*+,-.:;=?_'
    outlist = []
    for i in xrange(1,8):
        chars = sample(sample_space, 2)
        outlist.extend(chars)
    return ''.join(outlist)

def make_user(username, password):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # make user
        user = User(username=username)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True
        user.save()
        if Profile:
            profile = Profile.objects.create(user=user)
            profile.save()
        if add_entry_to_blog:
            blog_template = getattr(settings, 'NANO_USER_BLOG_TEMPLATE', 'blog/new_user.html')
            test_users = getattr(settings, 'NANO_USER_TEST_USERS', ())
            if not user.username in test_users:
                add_entry_to_blog(user, '%s just joined' % user.username, blog_template, date_field='date_joined')
        user.message_set.create(message="You're now registered, as '%s'" % username)
        return user
    else:
        raise NanoUserExistsError, "The username '%s' is already in use by somebody else" % username

def signup(request, *args, **kwargs):
    me = 'people'
    error = pop_error(request)
    data = {
            'me': me, 
            'error': error, 
            'form': SignupForm()
    }
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email'].strip() or ''
            user = make_user(username, password)
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            request.session['error'] = None
            return HttpResponseRedirect('/signup/done/')
    return render_page(request, 'signup.html', data)

@login_required
def password_change(request, *args, **kwargs):
    error = pop_error(request)
    template_name = 'password_change_form.html'
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data[u'password2']
            user = request.user
            user.set_password(password)
            user.save()
            request.session['error'] = None
            return HttpResponseRedirect('/password/change/done/')
    else:
        form = PasswordChangeForm()
    data = { 'form': form,
            'error': error,}
    return render_page(request, template_name, data)

def password_reset(request, project_name='Nano', *args, **kwargs):
    error = pop_error(request)
    template = 'password_reset_form.html'
    e_template = 'password_reset.txt'
    help_message = None
    e_subject = '%s password assistance' % project_name
    e_message = """Your new password is: 

%%s

It is long deliberately, so change it to 
something you'll be able to remember.


%s' little password-bot
""" % project_name
    e_from = getattr(settings, 'NANO_USER_EMAIL_SENDER', '')
    form = PasswordResetForm()
    if e_from and request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, username=form.cleaned_data['username'])
            if user.email:
                tmp_pwd = random_password()
                user.set_password(tmp_pwd)
                result = send_mail(subject=e_subject, from_email=e_from, message=e_message % tmp_pwd, recipient_list=(user.email,))
                user.save()
                request.session['error'] = None
                return HttpResponseRedirect('/password/reset/sent/')
            else:
                error = """There's no email-address registered for '%s', 
                        the password can't be reset."""
                request.session['error'] = error
                
    data = {'form': form,
            'help_message': help_message,
            'error':error}
    return render_page(request, template, data)

