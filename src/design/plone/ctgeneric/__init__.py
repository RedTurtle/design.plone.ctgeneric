# -*- coding: utf-8 -*-
"""Init and utils."""
from design.plone.contenttypes.events import evento
from design.plone.contenttypes.events import persona
from design.plone.contenttypes.vocabularies import tags_vocabulary

from zope.i18nmessageid import MessageFactory

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


tags_vocabulary.TAGS_MAPPING = [
    ("anziano", _("Anziano")),
    ("fanciullo", _("Fanciullo")),
    ("giovane", _("Giovane")),
    ("famiglia", _("Famiglia")),
    ("studente", _("Studente")),
    ("associazione", _("Associazione")),
    ("istruzione", _("Istruzione")),
    ("abitazione", _("Abitazione")),
    ("animale-domestico", _("Animale domestico")),
    ("integrazione-sociale", _("Integrazione sociale")),
    ("protezione-sociale", _("Protezione sociale")),
    ("comunicazione", _("Comunicazione")),
    ("urbanistica-edilizia", _("Urbanistica ed edilizia")),
    ("formazione-professionale", _("Formazione professionale")),
    (
        "condizioni-organizzazione-lavoro",
        _("Condizioni e organizzazione del lavoro"),
    ),
    ("trasporto", _("Trasporto")),
    ("matrimonio", _("Matrimonio")),
    ("elezione", _("Elezione")),
    ("tempo-libero", _("Tempo libero")),
    ("cultura", _("Cultura")),
    ("immigrazione", _("Immigrazione")),
    ("inquinamento", _("Inquinamento")),
    ("area-parcheggio", _("Area di parcheggio")),
    ("traffico-urbano", _("Traffico urbano")),
    ("acqua", _("Acqua")),
    ("gestione-rifiuti", _("Gestione dei rifiuti")),
    ("salute", _("Salute")),
    ("sicurezza-pubblica", _("Sicurezza pubblica")),
    ("sicurezza-internazionale", _("Sicurezza internazionale")),
    ("spazio-verde", _("Spazio verde")),
    ("sport", _("Sport")),
    ("trasporto-stradale", _("Trasporto stradale")),
    ("turismo", _("Turismo")),
    ("energia", _("Energia")),
    (
        "informatica-trattamento-dati",
        _("Informatica e trattamento dei dati"),
    ),
]
