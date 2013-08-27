.. index::
   double: nano.tools; tools

tools
=====
Utility-functions used by some of the other apps.

.. automodule:: nano.tools
   :members:

Models
------

Tree
++++

.. autoclass:: nano.tools.models.UnorderedTreeManager
   :members:

.. autoclass:: nano.tools.models.UnorderedTreeMixin
   :members:

Denoramlized text-field
+++++++++++++++++++++++

.. autoclass:: nano.tools.models.AbstractText
   :members:

Model with one generic foreign key
++++++++++++++++++++++++++++++++++

.. autoclass:: nano.tools.models.GenericForeignKeyAbstractModel
   :members:

Template tags
-------------

Either import the tags into some other templatetags-library. or add
``'nano.tools'`` to ``INSTALLED_APPS``.

.. automodule:: nano.tools.templatetags.nano_tags
   :members:
   :undoc-members:

