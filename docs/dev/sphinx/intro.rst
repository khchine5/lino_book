===========================
Getting started with Sphinx
===========================

Read the `reStructuredText Primer
<http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__
to get an introduction to the syntax.

If you have an example of what you want to get in the web version of
the book, then look at the source code of that page via the *Show
Source* link at the bottom of each page.


Referencing to something
========================

When you remain within one doctree (i.e. link to another page of the
book) and you want to refer to a whole page, use the `\:doc:
<http://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-doc>`__
role.

When you want an intersphinx link (e.g. a link from your blog to the
book), use the `\:ref\:
<http://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-ref>`__
role.


To link to a Python object that is part of Lino, use the following
roles:

- :rst:role:`mod` to link to a module.  e.g. :mod:`lino.core.actions`
  
- :rst:role:`func` to link to a function
  e.g. :func:`lino.utils.join_words`
     
- :rst:role:`class`  to link to a class.
  Example :class:`lino.core.model.Model`
  
- :rst:role:`meth`  to link to a method.
  Example :meth:`lino.core.model.Model.get_data_elem`
     
Generated API docs versus prosa
===============================

The Lino book contains "API docs" and "Specifications".  These are two
fundamentally different beasts.  The main difference is that API docs
are automatically generated using autodoc which extracts the
docstrings from source code while the Specifications are written in
prosa style.
  
Plugins generally cannot be documented using autodoc because they are
extensible and because Django would refuse to import two variants of a
same plugin within a same Sphinx build process.  So prosa style is
needed for plugins.

Prosa style documentation has the advantage of being more readable
since the author can decide about the documents' structure.  The
challenge with prosa style is that it needs extra care when some code
changes.

When referring to Django application code, there is an additional
thing to know: many plugins are documented using *prosa* style instead
of having their docs generated with autodoc.  The plugin itself (the
:xfile:`__init__.py` file) is documented using
autodoc. e.g. :mod:`lino.modlib.users`.  Models and everything below
top-level is documented in a :file:`/specs` page which uses the
:rst:dir:`currentmodule` directive to tell Sphinx that it is going to
document Python code objects.  That's why you can refer e.g. to a
model by saying e.g. :class:`lino.modlib.users.User` (with autodoc you
would have to write :class:`lino.modlib.users.models.User`).

This is valid not only for models but also for

- choicelists :class:`lino.modlib.users.UserTypes`
- model fields field: :attr:`lino.modlib.users.User.username`
- model methods, e.g. :meth:`lino.modlib.users.User.get_full_name`
- actions, e.g. :class:`lino.modlib.users.ChangePassword`
- user roles, e.g. :class:`lino.modlib.users.Helper`
- other plugin classes, e.g.
  :class:`lino.modlib.users.UserType`
  
  
Of course above works only for plugins that have been converted to
prosa style (:ticket:`1869`).
