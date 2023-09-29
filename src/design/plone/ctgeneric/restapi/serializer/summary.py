# -*- coding: utf-8 -*-
from design.plone.ctgeneric.interfaces import IDesignPloneCtgenericLayer
from plone.restapi.interfaces import ISerializeToJsonSummary
from design.plone.contenttypes.restapi.serializers.summary import (
    DefaultJSONSummarySerializer as BaseSerializer,
)
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJsonSummary)
@adapter(Interface, IDesignPloneCtgenericLayer)
class DefaultJSONSummarySerializer(BaseSerializer):
    def __call__(self, force_all_metadata=False):
        res = super().__call__(force_all_metadata=force_all_metadata)
        if self.context.portal_type == "Persona":
            res["ruolo"] = self.context.ruolo
        return res
