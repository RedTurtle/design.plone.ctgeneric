from design.plone.contenttypes.tests import test_ct_luogo as base
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import get_fieldset_fields
from design.plone.ctgeneric.testing import HAS_GET_FOLDER_CONTENTS
from design.plone.ctgeneric.testing import PLONE_VOLTO_PREVIEW_FIELDSETS
from plone import api
from transaction import commit
from uuid import uuid4

import unittest


class TestLuogoSchema(base.TestLuogoSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_luogo(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Venue"].behaviors,
            (
                "plone.app.content.interfaces.INameFromTitle",
                "plone.app.dexterity.behaviors.id.IShortName",
                "plone.app.dexterity.behaviors.metadata.IBasic",
                "plone.app.dexterity.behaviors.metadata.ICategorization",
                "plone.excludefromnavigation",
                "plone.relateditems",
                "plone.leadimage",
                "volto.preview_image",
                "design.plone.contenttypes.behavior.luogo",
                "design.plone.contenttypes.behavior.argomenti",
                "design.plone.contenttypes.behavior.address_venue",
                "design.plone.contenttypes.behavior.geolocation_venue",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "design.plone.contenttypes.behavior.luogo_v2",
                "design.plone.contenttypes.behavior.contatti_venue_v2",
            ),
        )

    def test_luogo_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        expected = [
            "default",
            "descrizione",
            "accesso",
            "dove",
            "orari",
            "contatti",
            "informazioni",
            "settings",
            "correlati",
            "categorization",
        ]
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.append("preview_image")
        expected.append("seo")
        self.assertEqual([x.get("id") for x in resp["fieldsets"]], expected)

    def test_luogo_required_fields(self):
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                ]
            ),
        )

    def test_luogo_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        expected = ["title", "description", "image", "image_caption"]
        if not PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.extend(["preview_image", "preview_caption"])
        expected.extend(["nome_alternativo", "tassonomia_argomenti"])
        self.assertEqual(resp["fieldsets"][0]["fields"], expected)

    def test_luogo_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"],
            [
                "struttura_responsabile_correlati",
                "struttura_responsabile",
                "riferimento_telefonico_struttura",
                "riferimento_fax_struttura",
                "riferimento_mail_struttura",
                "riferimento_pec_struttura",
                "telefono",
                "fax",
                "email",
                "pec",
                "web",
            ],
        )

    def test_luogo_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"],
            ["relatedItems", "correlato_in_evidenza"],
        )

    def test_luogo_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][9]["fields"],
            ["subjects", "language", "identificativo_mibac"],
        )

    def test_luogo_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            get_fieldset_fields(resp, "seo"),
            [
                "seo_title",
                "seo_description",
                "seo_noindex",
                "seo_canonical_url",
                "opengraph_title",
                "opengraph_description",
                "opengraph_image",
            ],
        )


class TestLuogoApi(base.TestLuogoApi):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    @unittest.skipIf(
        not HAS_GET_FOLDER_CONTENTS,
        "design.plone.contenttypes folder serializer uses getFolderContents, "
        "removed in this Plone version",
    )
    def test_venue_services(self):
        super().test_venue_services()

    @unittest.skipIf(
        not HAS_GET_FOLDER_CONTENTS,
        "design.plone.contenttypes folder serializer uses getFolderContents, "
        "removed in this Plone version",
    )
    def test_venue_news(self):
        super().test_venue_news()

    def test_venue_geolocation_deserializer_right_structure(self):
        venue = api.content.create(
            container=self.portal, type="Venue", title="Example venue"
        )

        commit()
        self.assertEqual(venue.geolocation, None)

        text_uuid = str(uuid4())
        response = self.api_session.patch(
            venue.absolute_url(),
            json={
                "@type": "Venue",
                "title": "Foo",
                "geolocation": {"latitude": 11.0, "longitude": 10.0},
                "modalita_accesso": {
                    "blocks": {
                        text_uuid: {
                            "@type": "text",
                            "text": {"blocks": [{"text": "Test", "type": "paragraph"}]},
                        }
                    },
                    "blocks_layout": {"items": [text_uuid]},
                },
            },
        )
        self.assertEqual(response.status_code, 204)
