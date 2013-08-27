.. index:: 
   double: nano.user; user

user
====

Doesn't have any models so just hook up the views in an urls.py:

.. automodule:: nano.user.views
   :members:

- ``signup()``
- ``password_change()``
- ``password_reset()``

.. index:: 
   double: nano.user; settings

Changes to settings
-------------------

NANO_USER_EMAIL_SENDER
    The From:-address on a password-reset email. If unset, no
    email is sent.

    **Default:** Not set

NANO_USER_TEST_USERS
    Special-cased usernames for live testing.

    **Default:** ``()``

NANO_USER_BLOG_TEMPLATE
    Template used for auto-blogging new users. 

    **Default:** ``blog/new_user.html``


.. automodule:: nano.user
    :members:
    :undoc-members:

