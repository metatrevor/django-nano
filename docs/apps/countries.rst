.. index::
   double: nano.countries; countries

countries
=========

Drop-in, nanofied replacement for https://code.google.com/p/django-countries/ .

To use: import from ``nano.countries`` instead of ``countries``. The
primary key is the two-letter iso country code, ``name`` and
``printable_name`` points to the same thing: what was known as
``printable_name`` in ``django-countries``. 

There is an admin, there are no template tags, views, forms or fields.
 
.. automodule:: nano.countries

Models
------

.. autoclass:: nano.countries.models.Country
