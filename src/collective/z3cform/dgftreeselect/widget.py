import time

import zope.interface

from z3c.form import interfaces

from z3c.form.widget import FieldWidget
from z3c.form.browser.text import TextWidget


start_time = time.time()


def initialize_url_provider(widget):
    """
    :param subform: collective.z3cform.datagridfield.datagridfield.DataGridFieldObjectSubForm

    :param dbf: DataGridWidget instance with tree selection widgets

    :param source_url: Where to load tree JSON
    """

    subform = widget.form

    dgfFieldObject = subform._parent
    dgf = dgfFieldObject.__parent__

    initialized = getattr(dgf, "_tree_select_has_url", False)
    if initialized:
        return

    # Create master-slave chain ids
    #
    # Set widget.master and widget.slave attributes
    # to column ids to build the tree structure in Javascript
    #
    #

    schema = subform.schema
    context = subform.context
    request = subform.request

    # See comments about the registration in testform.py
    urlProvider = schema.queryTaggedValue("TreeSelectURLProvider")
    if not urlProvider:
        raise RuntimeError("No registered tree select sourceURL provider for %s" % schema)

    sourceURL = urlProvider(schema, widget, subform, context, request)
    if not sourceURL:
        raise RuntimeError("URL provider acting funnily %s" % sourceURL)

    # Update data grid field to know about our attributes
    dgf.extra = sourceURL + "?%f" % start_time

    dgf._tree_select_has_url = True


def initialize_slave_chain(widget):
    """
    """
    subform = widget.form
    dgfFieldObject = subform._parent
    dgf = dgfFieldObject.__parent__

    initialized = getattr(dgf, "_tree_select_slave_chain", False)
    if initialized:
        return

    master = None

    for widget in subform.widgets.values():

        if not isinstance(widget, DGFTreeSelectWidget):
            # Not part of the grid
            continue

        if master:
            # Wid
            widget.master = master.field.getName()
            master.slave = widget.field.getName()
        else:
            widget.master = None

        master = widget

    dgf.__tree_select_slave_chain = True


class DGFTreeSelectWidget(TextWidget):
    """
    A data grid widget which does nested master-slave
    drop down menus using <select>.
    """

    klass = u'dgf-tree-select-widget'

    def __init__(self, request):
        super(DGFTreeSelectWidget, self).__init__(request)

        # Dynamically generated by Javascript
        self.terms = []

    @property
    def items(self):
        return []

    def update(self):
        """
        """
        super(DGFTreeSelectWidget, self).update()
        initialize_url_provider(self)

    def render(self):
        """
        """
        initialize_slave_chain(self)
        return super(DGFTreeSelectWidget, self).render()


@zope.interface.implementer(interfaces.IFieldWidget)
def DGFTreeSelectFieldWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    return FieldWidget(field, DGFTreeSelectWidget(request))
