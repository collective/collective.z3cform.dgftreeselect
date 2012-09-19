import time

import zope.interface

from z3c.form import interfaces

from z3c.form.browser.select import SelectWidget
from z3c.form.widget import FieldWidget
from z3c.form.browser.text import TextWidget

start_time = time.time()

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


@zope.interface.implementer(interfaces.IFieldWidget)
def DGFTreeSelectFieldWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    return FieldWidget(field, DGFTreeSelectWidget(request))


def prepare_tree_selection(subform, dgf, source_url):
    """

    :param dbf: DataGridWidget instance with tree selection widgets

    :param source_url: Where to load tree JSON
    """

    # Create master-slave chain ids
    #
    # Set widget.master and widget.slave attributes
    # to column ids to build the tree structure in Javascript

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

    dgf.extra = source_url + "?%f" % start_time
