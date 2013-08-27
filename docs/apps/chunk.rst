.. index:: 
   double: nano.chunk; chunk

chunk
=====

A chunk is a template that is stored in the database.

It has a unique name, the ``slug``, and some ``content``, which is whatever
you'd put in an ordinary template.

You use it by setting the template_name to the slug of the chunk, or by
{% include %}-ing it directly.

If the chunk uses non-builtin template tags, remember to {% load %} the
template tag library in the chunk.

There's a model and a template loader:

.. automodule:: nano.chunk

Models
------

.. autoclass:: nano.chunk.models.Chunk

Chunks can be created, updated and deleted via the django admin.

.. index::
    double: nano.chunk; settings

Changes to settings
-------------------

Add ``'nano.chunk.loader.Loader'`` to ``TEMPLATE_LOADERS``.
