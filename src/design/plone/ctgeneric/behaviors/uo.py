# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer


@provider(IFormFieldProvider)
class IUnitaOrganizzativaV2(model.Schema):
    tipologia_organizzazione = schema.Choice(
        title=_("tipologia_organizzazione_label", default="Tipologia organizzazione"),
        # vocabolario di rif sara' la lista delle tipologie di organizzazione
        vocabulary="" "design.plone.vocabularies.tipologie_unita_organizzativa",
        description=_(
            "tipologia_organizzazione_help",
            default="Specificare la tipologia di organizzazione: politica,"
            " amminsitrativa o di altro tipo.",
        ),
        required=True,
    )
    competenze = BlocksField(
        title=_("uo_competenze_label", default="Competenze"),
        description=_(
            "uo_competenze_help",
            default="Descrizione dei compiti assegnati alla struttura.",
        ),
        required=False,
    )

    sede = RelationList(
        title=_("sede_label", default="Sede principale"),
        default=[],
        description=_(
            "sede_help",
            default="Seleziona il Luogo in cui questa struttura ha sede. "
            "Se non è presente un contenuto di tipo Luogo a cui far "
            "riferimento, puoi compilare i campi seguenti. Se selezioni un "
            "Luogo, puoi usare comunque i campi seguenti per sovrascrivere "
            "alcune informazioni.",
        ),
        value_type=RelationChoice(
            title=_("Sede"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    contact_info = BlocksField(
        title=_("contact_info_label", default="Informazioni di contatto generiche"),
        required=False,
        description=_(
            "uo_contact_info_description",
            default="Inserisci eventuali informazioni di contatto aggiuntive "
            "non contemplate nei campi precedenti. "
            "Utilizza questo campo se ci sono dei contatti aggiuntivi rispetto"
            " ai contatti della sede principale. Se inserisci un collegamento "
            'con un indirizzo email, aggiungi "mailto:" prima dell\'indirizzo'
            ", per farlo aprire direttamente nel client di posta.",
        ),
    )


@implementer(IUnitaOrganizzativaV2)
@adapter(IUnitaOrganizzativa)
class UnitaOrganizzativaV2(object):
    """"""

    def __init__(self, context):
        self.context = context
