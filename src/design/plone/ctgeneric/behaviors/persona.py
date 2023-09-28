# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from design.plone.contenttypes.interfaces.persona import IPersona
from plone.app.dexterity import textindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IPersonaV2(model.Schema):
    ruolo = schema.Choice(
        title=_("ruolo_label", default="Ruolo"),
        description=_(
            "ruolo_help",
            default="Seleziona il ruolo della persona tra quelli disponibili.",
        ),
        vocabulary="design.plone.contenttypes.RuoliPersona",
        required=True,
    )

    data_conclusione_incarico = schema.Date(
        title=_(
            "data_conclusione_incarico_label",
            default="Data conclusione incarico",
        ),
        description=_(
            "data_conclusione_incarico_help",
            default="Data di conclusione dell'incarico.",
        ),
        required=False,
    )

    tipologia_persona = schema.Choice(
        title=_("tipologia_persona_label", default="Tipologia persona"),
        description=_(
            "tipologia_persona_help",
            default="Seleziona la tipologia di persona: politica,"
            " amministrativa o di altro tipo.",
        ),
        vocabulary="design.plone.contenttypes.TipologiaPersona",
        required=True,
    )

    data_insediamento = schema.Date(
        title=_("data_insediamento_label", default="Data insediamento"),
        description=_(
            "data_insediamento_help",
            default="Solo per persona politica: specificare la data di"
            " insediamento.",
        ),
        required=False,
    )

    telefono = schema.List(
        title=_("telefono_persona_label", default="Numero di telefono"),
        description=_(
            "telefono_persona_help",
            default="Contatto telefonico della persona. E' possibile inserire "
            'più di un numero. Premendo "Invio" o "tab" si può passare al '
            "successivo da inserire.",
        ),
        value_type=schema.TextLine(),
        missing_value=[],
        default=[],
        required=False,
    )
    fax = schema.TextLine(
        title=_("fax_persona_label", default="Fax"),
        description=_("fax_persona_help", default="Indicare un numero di fax."),
        required=False,
    )
    email = schema.List(
        title=_("email_persona_label", default="Indirizzo email"),
        description=_(
            "email_persona_help",
            default="Contatto mail della persona. E' possibile inserire più"
            ' di un indirizzo. Premendo "Invio" o "tab" si può passare al '
            "successivo da inserire.",
        ),
        value_type=schema.TextLine(),
        missing_value=[],
        default=[],
        required=False,
    )

    curriculum_vitae = field.NamedBlobFile(
        title=_("curriculum_vitae_label", default="Curriculum vitae"),
        required=False,
        description=_(
            "curriculum_vitae_help",
            default="Allega un file contenente il curriculum vitae della persona. "
            "Se ha più file da allegare, utilizza questo campo per quello principale "
            'e gli altri mettili dentro alla cartella "Curriculum vitae" che troverai dentro alla Persona.',
        ),
    )

    atto_nomina = field.NamedFile(
        title=_("atto_nomina_label", default="Atto di nomina"),
        required=False,
        description=_(
            "atto_nomina_help",
            default="Inserire un file contenente l'atto di nomina della" " persona.",
        ),
    )

    # custom fieldsets
    model.fieldset(
        "ruolo",
        label=_("ruolo_label", default="Ruolo"),
        fields=[
            "ruolo",
            "data_conclusione_incarico",
            "tipologia_persona",
            "data_insediamento",
        ],
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["telefono", "fax", "email"],
    )
    model.fieldset(
        "documenti",
        label=_("documenti_label", default="Documenti"),
        fields=["curriculum_vitae", "atto_nomina"],
    )
    # SearchableText fields
    textindexer.searchable("ruolo")
    textindexer.searchable("tipologia_persona")
    textindexer.searchable("telefono")
    textindexer.searchable("fax")
    textindexer.searchable("email")


@implementer(IPersonaV2)
@adapter(IPersona)
class PersonaV2(object):
    """"""

    def __init__(self, context):
        self.context = context
