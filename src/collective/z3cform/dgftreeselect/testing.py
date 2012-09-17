from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.z3cform.dgftreeselect


COLLECTIVE_Z3CFORM_DGFTREESELECT = PloneWithPackageLayer(
    zcml_package=collective.z3cform.dgftreeselect,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.z3cform.dgftreeselect:testing',
    name="COLLECTIVE_Z3CFORM_DGFTREESELECT")

COLLECTIVE_Z3CFORM_DGFTREESELECT_INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_Z3CFORM_DGFTREESELECT, ),
    name="COLLECTIVE_Z3CFORM_DGFTREESELECT_INTEGRATION")

COLLECTIVE_Z3CFORM_DGFTREESELECT_FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_Z3CFORM_DGFTREESELECT, ),
    name="COLLECTIVE_Z3CFORM_DGFTREESELECT_FUNCTIONAL")
