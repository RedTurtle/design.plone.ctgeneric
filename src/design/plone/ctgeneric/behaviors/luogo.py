# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.behaviors.luogo import ILuogoBase
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class ILuogoV2(ILuogoBase):
    modalita_accesso = BlocksField(
        title=_("modalita_accesso", default="Modalita' di accesso"),
        description=_(
            "help_modalita_accesso",
            default="Indicare tutte le informazioni relative alla modalità di"
            " accesso al luogo",
        ),
        required=False,
    )
    riferimento_telefonico_struttura = schema.TextLine(
        title=_(
            "riferimento_telefonico_struttura",
            default="Telefono della struttura responsabile",
        ),
        description=_(
            "help_riferimento_telefonico_struttura",
            default="Indicare il riferimento telefonico per poter contattare"
            " i referenti della struttura responsabile.",
        ),
        required=False,
    )
    riferimento_fax_struttura = schema.TextLine(
        title=_(
            "riferimento_fax_struttura",
            default="Fax della struttura responsabile",
        ),
        description=_(
            "help_riferimento_fax_struttura",
            default="Indicare un numero di fax della struttura responsabile.",
        ),
        required=False,
    )
    riferimento_mail_struttura = schema.TextLine(
        title=_(
            "riferimento_mail_struttura",
            default="E-mail struttura responsabile",
        ),
        description=_(
            "help_riferimento_mail_struttura",
            default="Indicare un indirizzo mail per poter contattare"
            " i referenti della struttura responsabile.",
        ),
        required=False,
    )

    riferimento_pec_struttura = schema.TextLine(
        title=_(
            "riferimento_pec_struttura",
            default="Pec della struttura responsabile",
        ),
        description=_(
            "help_riferimento_pec_struttura",
            default="Indicare un indirizzo pec per poter contattare"
            " i referenti della struttura responsabile.",
        ),
        required=False,
    )

    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=[
            "struttura_responsabile_correlati",
            "struttura_responsabile",
            "riferimento_telefonico_struttura",
            "riferimento_fax_struttura",
            "riferimento_mail_struttura",
            "riferimento_pec_struttura",
        ],
    )


@implementer(ILuogoV2)
@adapter(IDexterityContent)
class LuogoV2(object):
    """ """

    def __init__(self, context):
        self.context = context
