# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces import ISearchSchema
from zope.component import getUtility
from zope.interface import implementer
from plone import api
from collective.taxonomy.interfaces import ITaxonomy
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory


@implementer(INonInstallable)
class HiddenProfiles(object):
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
    delete_tipologia_notizia_taxonomy()


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


def delete_tipologia_notizia_taxonomy():
    portal = api.portal.get()
    sm = portal.getSiteManager()
    name = "collective.taxonomy.tipologia_notizia"
    utility = sm.queryUtility(ITaxonomy, name=name)
    if utility is None:
        return
    utility.unregisterBehavior()
    sm.unregisterUtility(utility, ITaxonomy, name=name)
    sm.unregisterUtility(utility, IVocabularyFactory, name=name)
    sm.unregisterUtility(utility, ITranslationDomain, name=name)
