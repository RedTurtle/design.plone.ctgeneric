from design.plone.contenttypes.restapi.serializers.venue import (
    VenueSerializer as BaseSerializer,
)
from design.plone.contenttypes.interfaces.persona import IPersona
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from design.plone.ctgeneric.interfaces import IDesignPloneCtgenericLayer
from plone.restapi.serializer.converters import json_compatible


@implementer(ISerializeToJson)
@adapter(IPersona, IDesignPloneCtgenericLayer)
class VenusSerializer(BaseSerializer):
    def __call__(self, version=None, include_items=True):
        result = super().__call__(version=version, include_items=include_items)

        result["contact_info"] = self.get_contacts_v2()
        return result

    def get_contacts_v2(self):
        pdc = []
        for field in ["telefono", "fax", "email"]:
            value = getattr(self.context, field, "")
            if value:
                pdc.append({"pdc_type": field, "pdc_value": value})

        return [
            [
                {
                    "value_punto_contatto": pdc,
                }
            ]
        ]
