#from .widget import prepare_tree_selection
#from .widget import prepare_tree_selection

from collective.z3cform.datagridfield.datagridfield import DataGridField


class TreeFormMixin(object):
    """
    Forms having DGF tree selection must mix in with this base class.
    """

    def getTreeDataURL(self, subform, widgets, widget):
        raise NotImplementedError("Subclass must implement")

    def datagridInitialise(self, subform, field):
        """ Callback to customize the datagridfield

        :param field: DataGridField instance

        :param subform: DataGridFieldObjectSubForm instance
        """
        pass

    def datagridUpdateWidgets(self, subform, widgets, widget):
        """
        """


