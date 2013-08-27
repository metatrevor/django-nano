.. index:: 
   double: nano.blog; blog

blog
====
A very basic blog-app.

It is also possible to convert from
``django-tagging`` to ``django-taggit`` using the management command
``migrate_tagging_to_taggit``. This will convert *all* tags, not
just those for blog entries.

.. automodule:: nano.blog

Models
------

.. autoclass:: nano.blog.models.Entry

Tools
-----

.. automodule:: nano.blog.tools
   :members:

.. index::
    double: nano.blog; settings

Changes to settings
-------------------

NANO_BLOG_USE_TAGS (optional)
    Set to True to use `django-taggit` or `django-tagging` if either is
    installed. ``django-taggit`` will be preferred if both are
    installed.

    **Default**: Not set

NANO_BLOG_SPECIAL_TAGS (optional)
    A list of tags that may be treated specially.

    **Default**: ``('pinned',)``
