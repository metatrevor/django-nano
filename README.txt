==========
Nano tools
==========

This is a set of nano-size tools and apps for Django 1.0 and later.

Currently included:

user
    A very basic user-registration- and password-handling app/tool

blog
    A very basic blog-app 

tools
    Utility-functions used by the above apps

Installation
------------

See INSTALL.txt for installation-instructions and TODO.txt for what's
missing.

Usage
-----

The apps and tools are in the namespace ``nano``.

blog:
    Append ``nano.blog`` to your INSTALLED_APPS

user:
    Doesn't have any models so just hook up the views in an urls.py:

    - ``signup()``
    - ``password_change()``
    - ``password_reset()``

Settings
--------

NANO_USER_EMAIL_SENDER
    The From:-address on a password-reset email. If unset, no email is
    sent.

    **Default:** Not set

NANO_USER_TEST_USERS
    Special-cased usernames for testing.

    **Default:** ``()``

NANO_USER_BLOG_TEMPLATE
    Template used for auto-blogging new users. 

    **Default:** ``blog/new_user.html``

NANO_LOG_FORMAT
    Format for logs, see Python's ``logging``-module

    **Default:** ``'%(asctime)s %(name)s %(module)s:%(lineno)d %(levelname)s %(message)s'``

NANO_LOG_FILE
    File to log to, see Python's ``logging``-module

    **Default:** ``'/tmp/nano.log'``


:Version: 0.1
