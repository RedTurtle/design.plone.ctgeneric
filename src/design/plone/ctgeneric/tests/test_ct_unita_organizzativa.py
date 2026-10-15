from design.plone.contenttypes.tests import test_ct_unita_organizzativa as base
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import HAS_GET_FOLDER_CONTENTS
from design.plone.ctgeneric.testing import PLONE_VOLTO_PREVIEW_FIELDSETS
from plone import api
from transaction import commit

import unittest


class TestUOSchema(base.TestUOSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_uo_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        expected = [
            "default",
            "cosa_fa",
            "struttura",
            "persone",
            "contatti",
            "correlati",
            "categorization",
            "informazioni",
            "settings",
            "ownership",
            "dates",
        ]
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.append("preview_image")
        expected.append("seo")
        self.assertEqual([x.get("id") for x in resp["fieldsets"]], expected)

    def test_uo_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected = [
                "title",
                "description",
                "image",
                "image_caption",
                "tassonomia_argomenti",
            ]
        else:
            expected = [
                "title",
                "description",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "tassonomia_argomenti",
            ]
        self.assertEqual(resp["fieldsets"][0]["fields"], expected)

    def test_uo_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][-1]["fields"],
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

    def test_behaviors_enabled_for_uo(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["UnitaOrganizzativa"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.categorization",
                "plone.basic",
                "plone.locking",
                "plone.leadimage",
                "volto.preview_image",
                "plone.relateditems",
                "design.plone.contenttypes.behavior.argomenti",
                "plone.textindexer",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "collective.taxonomy.generated.tipologia_organizzazione",
                "design.plone.contenttypes.behavior.unita_organizzativa_v2",
                "design.plone.contenttypes.behavior.address_uo",
                "design.plone.contenttypes.behavior.contatti_uo_v2",
            ),
        )

    def test_uo_required_fields(self):
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["title", "tipologia_organizzazione"]),
        )

    def test_uo_fields_struttura_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            [
                "legami_con_altre_strutture",
                "responsabile",
                "assessore_riferimento",
                "tipologia_organizzazione",
            ],
        )

    def test_uo_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            [
                "sede",
                "sedi_secondarie",
                "contact_info",
                "nome_sede",
                "street",
                "zip_code",
                "city",
                "quartiere",
                "circoscrizione",
                "country",
                "geolocation",
                "telefono",
                "fax",
                "email",
                "pec",
                "web",
                "orario_pubblico",
            ],
        )

    def test_uo_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"],
            ["relatedItems", "correlato_in_evidenza"],
        )

    def test_uo_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            ["subjects", "language"],
        )


class TestUO(base.TestUO):
    """"""

    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_cant_patch_uo_that_has_no_required_fields(self):
        """
        in V3 you get a 400, but here you can
        """
        uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="Foo"
        )
        commit()
        resp = self.api_session.patch(
            uo.absolute_url(),
            json={
                "title": "Foo modified",
            },
        )
        self.assertEqual(resp.status_code, 204)

    @unittest.skipIf(
        not HAS_GET_FOLDER_CONTENTS,
        "design.plone.contenttypes folder serializer uses getFolderContents, "
        "removed in this Plone version",
    )
    def test_uo_sede_data(self):
        super().test_uo_sede_data()

    @unittest.skipIf(
        not HAS_GET_FOLDER_CONTENTS,
        "design.plone.contenttypes folder serializer uses getFolderContents, "
        "removed in this Plone version",
    )
    def test_uo_service_related_service_show_only_services(self):
        super().test_uo_service_related_service_show_only_services()
