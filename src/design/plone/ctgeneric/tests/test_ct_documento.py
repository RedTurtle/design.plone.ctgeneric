from design.plone.contenttypes.tests import test_ct_documento as base
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import get_fieldset_fields
from design.plone.ctgeneric.testing import PLONE_VOLTO_PREVIEW_FIELDSETS
from plone import api


class TestDocumentoSchema(base.TestDocumentoSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_documento(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Documento"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.dublincore",
                "plone.relateditems",
                "plone.locking",
                "plone.constraintypes",
                "plone.leadimage",
                "volto.preview_image",
                "design.plone.contenttypes.behavior.argomenti_documento",
                "design.plone.contenttypes.behavior.descrizione_estesa_documento",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "design.plone.contenttypes.behavior.documento_v2",
            ),
        )

    def test_documento_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        expected = [
            "default",
            "descrizione",
            "informazioni",
            "settings",
            "correlati",
            "categorization",
            "dates",
            "ownership",
        ]
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.append("preview_image")
        expected.append("seo")
        self.assertEqual([x.get("id") for x in resp["fieldsets"]], expected)

    def test_documento_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        expected = [
            "title",
            "description",
            "identificativo",
            "tipologia_documento",
            "image",
            "image_caption",
        ]
        if not PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.extend(["preview_image", "preview_caption"])
        expected.append("tassonomia_argomenti")
        self.assertEqual(resp["fieldsets"][0]["fields"], expected)

    def test_documento_fields_descrizione_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            [
                "ufficio_responsabile",
                "area_responsabile",
                "autori",
                "licenza_distribuzione",
                "descrizione_estesa",
            ],
        )

    def test_documento_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["relatedItems", "correlato_in_evidenza"],
        )

    def test_documento_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(resp["fieldsets"][5]["fields"], ["subjects", "language"])

    def test_documento_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
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

    def test_documento_required_fields(self):
        """
        ufficio_responsabile is not required in v2 (see SchemaTweaks)
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["tipologia_documento", "title"]),
        )
