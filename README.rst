.. contents::

Introduction
============

``collective.z3cform.dgftreeselect`is a nested choice tree widget
with z3c.form and data grid widget for `Plone CMS <http://plone.org>`_.

* Multiple decision tree answers, one per table line

* The choice input data is a tree structure created with nested dictionaries and lists

* Data is loaded to the widget via AJAX / JSON, so that even very big decision
  trees don't add extra payload on your form page

Use cases
===========

* Decision tree input

* Product feature matrix input

* Other complex tabular data involving dropdowns and free form text input

Usage
=====

* Decision tree data is exported to the widget as a JSON. It's a nested structure
  of dictionaries and lists. First you need to generate your JSON data
  from a spreadheet.

* Setting up the widget requires

    * Creation of a row input form as zope.interface.Schema or plone.directives.form.Schema based form

    * This form should have two or more ``DGFTreeSelectWidget`` set for ``zope.schema.TextLine`` fields

    * Setting up a main form with a data grid field where DGF uses the created row schema as row schema

    * For the row schema you need to set up a tree widget data source URL callback

* `For further details see the demo testform <https://github.com/miohtama/collective.z3cform.dgftreeselect/blob/master/src/collective/z3cform/dgftreeselect/testform.py>`_.
  This form will be available in ``/@@dgftreeselect-test`` view after installing
  this add-on.

Missing features
==================

Currently this widget offers only edit interface and no view interface.
Adding one should be a matter of writing some TAL page template and JS code.

Further tuning
===============

JSON loads are marked with an unique id. You can cache these JSON files forever
in the browser or in the front end proxy with ``plone.app.caching`` rules.

Author
============

`Mikko Ohtamaa <http://opensourcehacker.com>`_
