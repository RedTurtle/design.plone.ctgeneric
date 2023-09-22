# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces.servizio import IServizio
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IServizioV2(model.Schema):
    a_chi_si_rivolge = BlocksField(
        title=_("a_chi_si_rivolge_label", default="A chi è rivolto"),
        required=False,
        description=_(
            "a_chi_si_rivolge_help",
            default="A chi si rivolge questo servizio e chi può usufruirne.",
        ),
    )
    come_si_fa = BlocksField(
        title=_("come_si_fa", default="Come fare"),
        required=False,
        description=_(
            "come_si_fa_help",
            default="Descrizione della procedura da seguire per poter"
            " usufruire del servizio.",
        ),
    )
    cosa_si_ottiene = BlocksField(
        title=_("cosa_si_ottiene", default="Cosa si ottiene"),
        description=_(
            "cosa_si_ottiene_help",
            default="Indicare cosa si può ottenere dal servizio, ad esempio"
            " 'carta di identità elettronica', 'certificato di residenza'.",
        ),
        required=False,
    )

    autenticazione = BlocksField(
        title=_("autenticazione", default="Autenticazione"),
        description=_(
            "autenticazione_help",
            default="Indicare, se previste, le modalità di autenticazione"
            " necessarie per poter accedere al servizio.",
        ),
        required=False,
    )

    tempi_e_scadenze = BlocksField(
        title=_("tempi_e_scadenze", default="Tempi e scadenze"),
        required=False,
        description=_(
            "tempi_e_scadenze_help",
            default="Descrivere le informazioni dettagliate riguardo eventuali tempi"
            " e scadenze di questo servizio.",
        ),
    )

    # custom fieldsets
    model.fieldset(
        "a_chi_si_rivolge",
        label=_("a_chi_si_rivolge_label", default="A chi si rivolge"),
        fields=[
            "a_chi_si_rivolge",
            "cosa_si_ottiene",
        ],
    )

    model.fieldset(
        "accedi_al_servizio",
        label=_("accedi_al_servizio_label", default="Accedere al servizio"),
        fields=[
            "come_si_fa",
        ],
    )


@implementer(IServizioV2)
@adapter(IServizio)
class ServizioV2(object):
    """"""

    def __init__(self, context):
        self.context = context
