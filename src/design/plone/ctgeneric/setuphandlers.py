from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces import ISearchSchema
from zope.component import getUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory

import logging

logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-design.plone.ctgeneric:default"
TIPOLOGIA_NOTIZIA_TAXONOMY = "collective.taxonomy.tipologia_notizia"
TIPOLOGIA_NOTIZIA_INDEX = "tipologia_notizia"


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "design.plone.ctgeneric:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["design.plone.ctgeneric.upgrades"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    disable_searchable_types()
    remove_tipologia_notizia_taxonomy(context)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def disable_searchable_types():
    # remove some types from search enabled ones
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISearchSchema, prefix="plone")
    remove_types = [
        "Dataset",
        "Documento Personale",
        "Messaggio",
        "Pratica",
        "RicevutaPagamento",
        "Incarico",
    ]
    types = [x for x in settings.types_not_searched if x not in remove_types]
    settings.types_not_searched = tuple(types)


def remove_tipologia_notizia_taxonomy(context):
    """
    In V2 tipologia_notizia is a field of design.plone.contenttypes.behavior.news_v2
    (with a vocabulary from the control panel), so we don't need the
    collective.taxonomy one (and its index, that only knows taxonomy values).
    Remove the taxonomy and replace its index with a plain FieldIndex.
    """
    sm = api.portal.get().getSiteManager()
    taxonomy = sm.queryUtility(ITaxonomy, name=TIPOLOGIA_NOTIZIA_TAXONOMY)
    if taxonomy is not None:
        # removes the behavior from the FTIs, its index (and local indexer),
        # querystring records and generated interface
        taxonomy.unregisterBehavior()
        sm.unregisterUtility(taxonomy, ITaxonomy, name=TIPOLOGIA_NOTIZIA_TAXONOMY)
        sm.unregisterUtility(
            taxonomy, IVocabularyFactory, name=TIPOLOGIA_NOTIZIA_TAXONOMY
        )
        sm.unregisterUtility(
            taxonomy, ITranslationDomain, name=TIPOLOGIA_NOTIZIA_TAXONOMY
        )
        logger.info(f"Removed taxonomy {TIPOLOGIA_NOTIZIA_TAXONOMY}")

    # (re)create our querystring criterion: unregisterBehavior removes it
    context.runImportStepFromProfile(
        DEFAULT_PROFILE, "plone.app.registry", run_dependencies=False
    )

    # always recreate the index from catalog.xml: an existing one could be the
    # taxonomy KeywordIndex (catalog import step doesn't replace it)
    catalog = api.portal.get_tool(name="portal_catalog")
    if TIPOLOGIA_NOTIZIA_INDEX in catalog.indexes():
        catalog.delIndex(TIPOLOGIA_NOTIZIA_INDEX)
    context.runImportStepFromProfile(DEFAULT_PROFILE, "catalog")

    brains = catalog(portal_type="News Item")
    for brain in brains:
        brain.getObject().reindexObject(idxs=[TIPOLOGIA_NOTIZIA_INDEX])
    logger.info(
        f"Created index {TIPOLOGIA_NOTIZIA_INDEX} and reindexed {len(brains)} news"
    )
