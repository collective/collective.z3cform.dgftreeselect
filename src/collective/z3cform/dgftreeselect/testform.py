"""

    Manual test form of the thingy.

"""

import json

from zope import schema
from zope import interface
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot
from z3c.form import button

from five import grok

from plone.directives import form

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from .widget import DGFTreeSelectFieldWidget, prepare_tree_selection
from .form import TreeFormMixin

SAMPLE_DATA = [
    {
        "id": "unknown",
        "label": "Unknown"
    },

    {
        "id": "a",
        "label": "A",
        "children": [

            {
                "id": "unknown",
                "label": "Unknown"
            },

            {
                "id": "aa",
                "label": "AA",
                "children": [
                    {
                        "id": "aaa",
                        "label": "AAA",
                    }
                ]
            },

            {
                "id": "ab",
                "label": "AB",
                "children": [
                    {
                        "id": "aba",
                        "label": "ABA",
                    },

                    {
                        "id": "abb",
                        "label": "ABB",
                    }

                ]
            },

        ]
    },

    {
        "id": "b",
        "label": "B",
        "children": [
            {
                "id": "ba",
                "label": "BA",
                "children": [
                    {
                        "id ": "baa",
                        "name ": "BAA",
                    }
                ]
            },

            {
                "id": "bb",
                "label": "BB",
                "children": [
                    {
                        "id": "bba",
                        "label": "BBA",
                    },

                    {
                        "id": "bbb",
                        "label": "BBB",
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


class EditForm(TreeFormMixin, form.SchemaForm):
    grok.context(ISiteRoot)
    grok.name("dgftreeselect-test")
    grok.require('zope2.View')

    ignoreContext = True
    schema = IFormSchema

    label = u"Tree selection demo and manual testing"

    def getTreeDataURL(self, subform):
        context = self.context.aq_inner
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')

        # AJAX will load tree source data from this URL
        sourceURL = portal_state.portal_url() + "/dgftreeselect-test-data"
        return sourceURL

    @button.buttonAndHandler(u'Turbo boost')
    def handleApply(self, action):
        pass


class DataSource(grok.CodeView):
    """
    Generate JSON array needed to populate the fields
    """
    grok.context(ISiteRoot)
    grok.name("dgftreeselect-test-data")

    def render(self):
        self.request.response.setHeader("Content-type", "application/json")
        return json.dumps(SAMPLE_DATA)
