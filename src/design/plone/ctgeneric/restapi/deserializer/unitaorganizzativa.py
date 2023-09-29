# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa
from design.plone.ctgeneric.interfaces import IDesignPloneCtgenericLayer
from plone.restapi.deserializer.dxcontent import DeserializeFromJson
from plone.restapi.interfaces import IDeserializeFromJson
from zope.component import adapter
from zope.interface import implementer


@implementer(IDeserializeFromJson)
@adapter(IUnitaOrganizzativa, IDesignPloneCtgenericLayer)
class DeserializeUnitaOrganizzativaFromJson(DeserializeFromJson):
    def __call__(self, validate_all=False, data=None, create=False):
        """
        Nel v3 ci sono validazioni sull'obbligatorietà
        """
        return super().__call__(validate_all=validate_all, data=data, create=create)
