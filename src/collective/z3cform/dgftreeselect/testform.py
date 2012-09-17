"""

    Manual test form of the thingy.

"""

import json

from zope import schema
from zope import interface
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot

from five import grok

from plone.directives import form

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from .widget import DGFTreeSelectFieldWidget


SAMPLE_DATA = [
    {
        "id": "a",
        "name": "A",
        "children": [
            {
                "id": "aa",
                "name": "AA",
                "children": [
                    {
                        "id ": "aaa",
                        "name ": "AAA",
                    }
                ]
            },

            {
                "id": "ab",
                "name": "AB",
                "children": [
                    {
                        "id": "aba",
                        "name": "ABA",
                    },

                    {
                        "id": "abb",
                        "name": "ABB",
                    }

                ]
            },

        ]
    },

    {
        "id": "b",
        "name": "B",
        "children": [
            {
                "id": "ba",
                "name": "BA",
                "children": [
                    {
                        "id ": "baa",
                        "name ": "BAA",
                    }
                ]
            },

            {
                "id": "bb",
                "name": "BB",
                "children": [
                    {
                        "id": "bba",
                        "name": "BBA",
                    },

                    {
                        "id": "bbb",
                        "name": "BBB",
                    }

                ]
            },

        ]
    },
]


class ITableRowSchema(interface.Interface):
    one = schema.TextLine(title=u"Level 1", required=False)
    two = schema.TextLine(title=u"Level 2", required=False)
    three = schema.TextLine(title=u"Level 3", required=False)


class IFormSchema(form.Schema):

    form.widget(table=DataGridFieldFactory)
    table = schema.List(title=u"Nested selection tree test",
        value_type=DictRow(title=u"tablerow", schema=ITableRowSchema))


class EditForm(form.SchemaForm):
    grok.context(ISiteRoot)
    grok.name("dgftreeselect-test")
    grok.require('zope2.View')

    ignoreContext = True
    schema = IFormSchema

    label = u"Tree selection demo and manual testing"

    def datagridInitialise(self, subform, field):
        """ Callback to customize the datagridfield

        :param field: DataGridField instance

        :param subform: DataGridFieldObjectSubForm instance
        """

        # Turn all fields in the table to use custom election widgets
        for field in subform.fields.values():
            field.widgetFactory = DGFTreeSelectFieldWidget

        # CReate

    def datagridUpdateWidgets(self, subform, widgets, widget):
        """
        """

        # Set tree-mapping master-slace relationships between
        # widgets in the row

        widgets["one"].master = None
        widgets["one"].slave = "two"

        widgets["two"].master = "one"
        widgets["two"].slave = "three"

        widgets["three"].master = "two"
        widgets["three"].slave = None

        context = self.context.aq_inner
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')

        # AJAX will load tree source data from this URL
        sourceURL = portal_state.portal_url() + "/dgftreeselect-test-data"

        for widget in widgets.values():
            widget.sourceURL = sourceURL


class DataSource(grok.CodeView):
    """
    Generate JSON array needed to populate the fields
    """
    grok.context(ISiteRoot)
    grok.name("dgftreeselect-test-data")

    def render(self):
        self.request.response.setHeader("Content-type", "application/json")
        return json.dumps(SAMPLE_DATA)
