# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)
from plone.testing import z2

import design.plone.ctgeneric


class DesignPloneCtgenericLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=design.plone.ctgeneric)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'design.plone.ctgeneric:default')


DESIGN_PLONE_CTGENERIC_FIXTURE = DesignPloneCtgenericLayer()


DESIGN_PLONE_CTGENERIC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_CTGENERIC_FIXTURE,),
    name='DesignPloneCtgenericLayer:IntegrationTesting',
)


DESIGN_PLONE_CTGENERIC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_CTGENERIC_FIXTURE,),
    name='DesignPloneCtgenericLayer:FunctionalTesting',
)


DESIGN_PLONE_CTGENERIC_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DESIGN_PLONE_CTGENERIC_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='DesignPloneCtgenericLayer:AcceptanceTesting',
)
