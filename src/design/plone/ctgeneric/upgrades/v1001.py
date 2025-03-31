# -*- coding: utf-8 -*-
from design.plone.ctgeneric.setuphandlers import delete_tipologia_notizia_taxonomy
from plone import api

import logging

logger = logging.getLogger(__name__)


def upgrade(setup_tool=None):
    """ """
    delete_tipologia_notizia_taxonomy()

    setup_tool.runAllImportStepsFromProfile("design.plone.ctgeneric.upgrades:1001")

    brains = api.content.find(portal_type="News Item")
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info(f"Processing {i} of {tot}")
        obj = brain.getObject()
        if getattr(obj, "tipologia_notizia", ""):
            obj.reindexObject(idxs=["tipologia_notizia"])
