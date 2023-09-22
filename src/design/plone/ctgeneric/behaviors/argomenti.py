# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from design.plone.contenttypes.behaviors.argomenti import IArgomentiSchema
from design.plone.contenttypes.interfaces.documento import IDocumento
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IArgomentiDocumentoV2(IArgomentiSchema):
    """ """

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["correlato_in_evidenza"],
    )
    form.order_after(correlato_in_evidenza="IRelatedItems.relatedItems")
    form.order_after(tassonomia_argomenti="IDublinCore.title")


@implementer(IArgomentiDocumentoV2)
@adapter(IDocumento)
class ArgomentiDocumentoV2(object):
    def __init__(self, context):
        self.context = context
