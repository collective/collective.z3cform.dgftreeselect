.. contents::

Introduction
============

Nested choice trees with z3c.form and data grid widget.

* Multiple answers, one per data grid field line

* Input a multi-selection choice tree as dictionaries

Usage
=====

* Possible value map is created in a nested dictionary structure which nicely serializes
  to JSON

* Applies to zope.schema-TextLine field. Note that we cannot use zope.schema.Choice, becaues
  of tree-like data would be very difficult to validate per cell

* All fields in the nested tree structure must be non-required

