from .widget import prepare_tree_selection
from .widget import DGFTreeSelectFieldWidget


class TreeFormMixin(object):
    """
    Forms having DGF tree selection must mix in with this base class.
    """

    def getTreeDataURL(self, subform):
        raise NotImplementedError("Subclass must implement")

    def datagridInitialise(self, subform, field):
        """ Callback to customize the datagridfield

        :param field: DataGridField instance

        :param subform: DataGridFieldObjectSubForm instance
        """

        # Turn all fields in the table to use custom election widgets
        for field in subform.fields.values():
            field.widgetFactory = DGFTreeSelectFieldWidget

    def datagridUpdateWidgets(self, subform, widgets, widget):
        """
        """

        sourceURL = self.getTreeDataURL(subform)
        prepare_tree_selection(subform, widget, sourceURL)
