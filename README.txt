.. contents::

Introduction
============

Nested choice trees with z3c.form and data grid widget.

* Multiple answers, one per data grid field line

* Input a tree of multi-selection choices as nestd Python dictionary structure

* Data is loaded to the widget via AJAX / JSON, so that even very big decision
  trees don't add extra payload on your form page

Usage
=====

* Possible value map is created in a nested dictionary structure which nicely serializes
  to JSON

* Applies to zope.schema-TextLine field. Note that we cannot use zope.schema.Choice, becaues
  of tree-like data would be very difficult to validate per cell

* All fields in the nested tree structure must be non-required

* `See example form how to build your own tree selecter <https://github.com/miohtama/collective.z3cform.dgftreeselect/blob/master/src/collective/z3cform/dgftreeselect/testform.py>`_

Further info
=============

* A ``plone.app.cacing`` ruleset in provided in ``cache.zcml``. You can apply
  this to make your tree JSON view responses cached in the browser.

