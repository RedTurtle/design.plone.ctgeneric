# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.behaviors.news_additional_fields import (
    INewsAdditionalFields,
)
from plone.app.contenttypes.interfaces import INewsItem
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class INewsAdditionalFieldsV2(INewsAdditionalFields):
    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa", default="Descrizione estesa"),
        required=False,
        description=_(
            "descrizione_estesa_help",
            default="Descrizione dettagliata e completa.",
        ),
    )

    tipologia_notizia = schema.Choice(
        title=_("tipologia_notizia_label", default="Tipologia notizia"),
        description=_(
            "tipologia_notizia_help",
            default="Seleziona la tipologia della notizia.",
        ),
        required=True,
        vocabulary="design.plone.vocabularies.tipologie_notizia",
    )

    a_cura_di = RelationList(
        title=_("a_cura_di_label", default="A cura di"),
        description=_(
            "a_cura_di_help",
            default="Seleziona l'ufficio di comunicazione responsabile di "
            "questa notizia/comunicato stampa.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )

    form.order_before(tipologia_notizia="ILeadImageBehavior.image")


@implementer(INewsAdditionalFieldsV2)
@adapter(INewsItem)
class NewsAdditionalFieldsV2(object):
    """"""

    def __init__(self, context):
        self.context = context
