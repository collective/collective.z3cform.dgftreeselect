"""

    Manual test form of the thingy.

"""

import json

from zope.app.component.hooks import getSite
from zope import schema
from zope import interface
from zope import component
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot
from zope.interface import Invalid
from zope.schema.vocabulary import SimpleVocabulary
from five import grok


from z3c.form import button
from z3c.form.interfaces import ActionExecutionError
import z3c.form.interfaces


from plone.directives import form

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from .form import TreeFormMixin
from .widget import DGFTreeSelectFieldWidget


class ITableRowSchema(form.Schema):

    # These fields are linked together by tree select

    form.widget(one=DGFTreeSelectFieldWidget)
    one = schema.TextLine(title=u"Level 1", required=False)

    form.widget(two=DGFTreeSelectFieldWidget)
    two = schema.TextLine(title=u"Level 2", required=False)

    form.widget(three=DGFTreeSelectFieldWidget)
    three = schema.TextLine(title=u"Level 3", required=False)

    # This field is independent from the rest of the fields

    independent = schema.Bool(
        title=u"Check me",
        description=u"Do not take part to the decision tree",
        required=False)

    choices = schema.Choice(
        title=u"Independent select",
        description=u"Do not take part to the decision tree",
        required=False,
        vocabulary="plone.app.vocabularies.Workflows")


class IDeviceProperty(form.Schema):
    """
    One of the rows in a device matrix.

    These rows are prepopulated.
    """

    form.widget(choice1=DGFTreeSelectFieldWidget)
    choice1 = schema.TextLine(
        title=u"Select 1",
        required=False)

    form.widget(choice2=DGFTreeSelectFieldWidget)
    choice2 = schema.TextLine(
        title=u"Select 2",
        description=u"Do not take part to the decision tree",
        required=False)


@component.adapter(schema.interfaces.IField, z3c.form.interfaces)
@interface.implementer(z3c.form.interfaces.IFieldWidget)
def FeatureMatrixGridFactory(field, request):
    """
    A special widget constructor setting up widget parameters for DGF.
    """
    widget = DataGridFieldFactory(field, request)
    widget.allow_insert = False
    widget.allow_delete = False
    widget.allow_reorder = False
    widget.auto_append = False
    return widget


class IDeviceModelRow(form.Schema):

    # These fields are linked together by tree select

    deviceModel = schema.Choice(
        title=u"Device model",
        required=False,
        vocabulary=SimpleVocabulary.fromValues([
                "Model Red",
                "Model Blue",
                "Model Gold",
            ]))

    form.widget(featureMatrix=FeatureMatrixGridFactory)
    featureMatrix = schema.List(title=u"Features",
        value_type=DictRow(title=u"featurerow", schema=IDeviceProperty))


FEATURE_MATRIX_ROWS = [
    dict(choice1="a", choice2="aa"),
    dict(choice1="b", choice2="ba"),
]


@form.default_value(field=IDeviceModelRow['featureMatrix'])
def getDefaultFeatureMatrixValue(data):
    # Clone the source template
    return FEATURE_MATRIX_ROWS[:]


@component.adapter(schema.interfaces.IField, z3c.form.interfaces)
@interface.implementer(z3c.form.interfaces.IFieldWidget)
def DeviceModelRowFactory(field, request):
    """
    A special widget constructor setting up widget parameters for DGF.
    """
    widget = DataGridFieldFactory(field, request)
    widget.allow_insert = True
    widget.allow_delete = True
    widget.allow_reorder = False
    widget.auto_append = False
    return widget


class IFormSchema(form.Schema):
    """
    An example form with two tree selections.


    - One nested inside another datagridfield

    """

    form.widget(table=DataGridFieldFactory)
    table = schema.List(
        title=u"Tree select",
        value_type=DictRow(title=u"tablerow", schema=ITableRowSchema),
        description=u"Normal decision tree. The last columns are independent of decision tree values."
        )

    foobar = schema.Bool(title=u"Just another field")

    # Insert yo dawg joke here

    form.widget(table2=DeviceModelRowFactory)
    table2 = schema.List(
        title=u"Feature matrix: nested fixed DGF inside a DataGridField",
        value_type=DictRow(title=u"devicerow", schema=IDeviceModelRow),
        description=u"A decision tree nested inside a DGF cell. Very useful for products' feature sets' kind of data input",
        )


@form.default_value(field=IFormSchema['table2'])
def getEmptyFeatureMatrix(data):
    """
    The initial population of feature matrix example
    """
    return [dict(deviceModel="", featureMatrix=getDefaultFeatureMatrixValue(data))]


# We register the provider in this perverted way, because
# http://stackoverflow.com/questions/12529587/querying-adapters-against-plone-directives-form-schema
def TreeSourceURL(schema, widget, form, context, request):
    """
    context get passed in as None...
    """
    context = getSite()
    portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
    # AJAX will load tree source data from this URL
    sourceURL = portal_state.portal_url() + "/++resource++collective.z3cform.dgftreeselect/demochoices.json"
    return sourceURL

IDeviceProperty.setTaggedValue("TreeSelectURLProvider", TreeSourceURL)
ITableRowSchema.setTaggedValue("TreeSelectURLProvider", TreeSourceURL)


class EditForm(TreeFormMixin, form.SchemaForm):
    """
    Edit form for our model.

    We got one dummy button which allows us to manually inspect the data postback values.
    """
    grok.context(ISiteRoot)
    grok.name("dgftreeselect-test")
    grok.require('zope2.View')

    ignoreContext = True
    schema = IFormSchema

    label = u"Tree selection demo and manual testing"

    @button.buttonAndHandler(u'Turbo boost')
    def handleApply(self, action):

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        raise ActionExecutionError(Invalid(u"Please see that data stays intact over postback"))


