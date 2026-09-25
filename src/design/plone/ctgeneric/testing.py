from design.plone.contenttypes.schema_overrides import (
    SchemaTweaks as ContenttypesSchemaTweaks,
)
from design.plone.contenttypes.testing import DesignPloneContenttypesLayer
from design.plone.contenttypes.testing import DesignPloneContenttypesRestApiLayer
from design.plone.ctgeneric.adapters.schema_tweaks import SchemaTweaks
from importlib.metadata import version
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel.model import Schema
from plone.testing import z2

import design.plone.ctgeneric
import os
import Products.CMFPlone


def package_version(name):
    return tuple(int(x) for x in version(name).split(".")[:2])


# plone.volto >= 5.1.0 moves preview_image/preview_caption (and preview link)
# fields out of the default fieldset, into their own fieldsets
PLONE_VOLTO_PREVIEW_FIELDSETS = package_version("plone.volto") >= (5, 1)

# plone.app.contenttypes < 4 (Plone 6.0) enables plone.allowdiscussion on
# Document and News Item. Since Plone 6.1 discussion is an optional add-on.
CORE_TYPES_ALLOW_DISCUSSION = package_version("plone.app.contenttypes") < (4, 0)

# getFolderContents skin script has been removed in newer Plone versions, but
# design.plone.contenttypes folder serializer still uses it
HAS_GET_FOLDER_CONTENTS = os.path.exists(
    os.path.join(
        os.path.dirname(Products.CMFPlone.__file__),
        "skins",
        "plone_scripts",
        "getFolderContents.py",
    )
)


def get_fieldset_fields(resp, fieldset_id):
    """
    Return the fields of a fieldset from a @types response, by fieldset id
    """
    for fieldset in resp["fieldsets"]:
        if fieldset["id"] == fieldset_id:
            return fieldset["fields"]
    return None


def apply_schema_tweaks():
    """
    SchemaTweaks (ours and design.plone.contenttypes ones) are ISchemaPlugin:
    plone.supermodel runs schema plugins only once, in finalizeSchemas (a zcml
    customAction executed at the end of the configuration). In a real instance
    all the zcml is loaded in a single run, but in test layers plone.supermodel
    is configured (and schemas finalized) long before these plugins are
    registered, so they are never called.
    """

    def walk(schema):
        yield schema
        for child in getattr(schema, "dependents", {}).keys():
            yield from walk(child)

    plugins = sorted(
        [SchemaTweaks, ContenttypesSchemaTweaks], key=lambda plugin: plugin.order
    )
    for schema in set(walk(Schema)):
        if IFormFieldProvider.providedBy(schema):
            for plugin in plugins:
                plugin(schema)()


class DesignPloneCtgenericLayer(DesignPloneContenttypesLayer):
    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=design.plone.ctgeneric)
        apply_schema_tweaks()

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
        applyProfile(portal, "design.plone.ctgeneric:default")


class DesignPloneCtgenericRestApiLayer(DesignPloneContenttypesRestApiLayer):
    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=design.plone.ctgeneric)
        apply_schema_tweaks()

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
        applyProfile(portal, "design.plone.contenttypes:default")
        applyProfile(portal, "design.plone.ctgeneric:default")


DESIGN_PLONE_CTGENERIC_FIXTURE = DesignPloneCtgenericLayer()
DESIGN_PLONE_CTGENERIC_API_FIXTURE = DesignPloneCtgenericRestApiLayer()

DESIGN_PLONE_CTGENERIC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_CTGENERIC_FIXTURE,),
    name="DesignPloneCtgenericLayer:IntegrationTesting",
)

DESIGN_PLONE_CTGENERIC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_CTGENERIC_FIXTURE,),
    name="DesignPloneCtgenericLayer:FunctionalTesting",
)

DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_CTGENERIC_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="DesignPloneCtgenericRestApiLayer:Functional",
)
