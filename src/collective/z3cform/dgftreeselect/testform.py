"""

    Manual test form of the thingy.

"""

from zope import schema
from zope import interface
from Products.CMFCore.interfaces import ISiteRoot

from z3c.form import field

from plone.directives import form


from five import grok

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow


class ITableRowSchema(interface.Interface):
    one = schema.TextLine(title=u"Level 1")
    two = schema.TextLine(title=u"Level 2")
    three = schema.TextLine(title=u"Level 3")


class IFormSchema(form.Schema):

    four = schema.TextLine(title=u"Four")

    table = schema.List(title=u"Nested selection tree test",
        value_type=DictRow(title=u"tablerow", schema=ITableRowSchema))


class EditForm(form.SchemaForm):
    grok.context(ISiteRoot)
    grok.name("dgftreeselect-test")
    grok.require('zope2.View')

    ignoreContext = True
    schema = IFormSchema

    label = u"Tree selection demo and manual testing"

    def updateFields(self):
        form.SchemaForm.updateFields(self)
        self.fields['table'].widgetFactory = DataGridFieldFactory
        import ipdb ; ipdb.set_trace()