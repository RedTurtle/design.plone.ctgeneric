# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory
from design.plone.contenttypes.events import persona

_ = MessageFactory("design.plone.ctgeneric")

persona_folders = [x for x in persona.FOLDERS if x["contains"] != ("Incarico",)]
persona_folders.extend(
    [
        {"id": "compensi", "title": "Compensi", "contains": ("File",)},
        {
            "id": "importi-di-viaggio-e-o-servizi",
            "title": "Importi di viaggio e/o servizi",
            "contains": ("File",),
        },
    ]
)

persona.FOLDERS = persona_folders
