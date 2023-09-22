# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.behaviors.evento import IEvento
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IEventoV2(IEvento):
    """
    Campi custom solo per la v2
    """

    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa", default="Descrizione estesa"),
        required=False,
        description=_(
            "descrizione_estesa_help",
            default="Descrizione dettagliata e completa.",
        ),
    )

    descrizione_destinatari = BlocksField(
        title=_("a_chi_si_rivolge_label", default="A chi è rivolto"),
        required=False,
        description=_(
            "a_chi_si_rivolge_help",
            default="Descrizione testuale dei principali destinatari dell'Evento",
        ),
    )

    persone_amministrazione = RelationList(
        title="Persone dell'amministrazione che partecipano all'evento",
        default=[],
        value_type=RelationChoice(
            title=_("Persona dell'amministrazione"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "persone_amministrazione_help",
            default="Elenco delle persone dell'amministrazione che"
            " parteciperanno all'evento.",
        ),
        required=False,
    )

    telefono = schema.TextLine(
        title=_("telefono_event_help", default="Telefono"),
        description=_(
            "telefono_event_label",
            default="Indicare un riferimento telefonico per poter contattare"
            " gli organizzatori.",
        ),
        required=False,
    )
    fax = schema.TextLine(
        title=_("fax_event_help", default="Fax"),
        description=_("fax_event_label", default="Indicare un numero di fax."),
        required=False,
    )
    reperibilita = schema.TextLine(
        title=_("reperibilita", default="Reperibilità organizzatore"),
        required=False,
        description=_(
            "reperibilita_help",
            default="Indicare gli orari in cui l'organizzatore è"
            " telefonicamente reperibile.",
        ),
    )
    email = schema.TextLine(
        title=_("email_event_label", default="E-mail"),
        description=_(
            "email_event_help",
            default="Indicare un indirizzo mail per poter contattare"
            " gli organizzatori.",
        ),
        required=False,
    )

    web = schema.TextLine(
        title=_("web_event_label", default="Sito web"),
        description=_(
            "web_event_help",
            default="Indicare un indirizzo web di riferimento a " "questo evento.",
        ),
        required=False,
    )

    # custom tabs
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=[
            "telefono",
            "fax",
            "reperibilita",
            "email",
            "web",
        ],
    )
    model.fieldset(
        "informazioni",
        label=_("informazioni_label", default="Ulteriori informazioni"),
        fields=["patrocinato_da"],
    )


@implementer(IEventoV2)
@adapter(IDexterityContent)
class EventoV2(object):
    """ """

    def __init__(self, context):
        self.context = context
