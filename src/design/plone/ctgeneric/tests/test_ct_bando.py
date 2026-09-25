from design.plone.contenttypes.tests import test_ct_bando as base
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import get_fieldset_fields
from design.plone.ctgeneric.testing import PLONE_VOLTO_PREVIEW_FIELDSETS


class TestBandoSchema(base.TestBandoSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_bando_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        expected = [
            "default",
            "correlati",
            "settings",
            "categorization",
            "dates",
            "ownership",
            "seo",
        ]
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.append("preview_image")
        self.assertEqual([x.get("id") for x in resp["fieldsets"]], expected)

    def test_bando_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        expected = [
            "title",
            "description",
            "cig",
            "text",
            "tipologia_bando",
            "destinatari",
            "ente_bando",
            "apertura_bando",
            "scadenza_domande_bando",
            "scadenza_bando",
            "chiusura_procedimento_bando",
            "riferimenti_bando",
            "update_note",
        ]
        if not PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.extend(["preview_image", "preview_caption"])
        self.assertEqual(resp["fieldsets"][0]["fields"], expected)

    def test_bando_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            [
                "area_responsabile",
                "ufficio_responsabile",
                "relatedItems",
                "tassonomia_argomenti",
                "correlato_in_evidenza",
            ],
        )

    def test_bando_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
        self.assertEqual(resp["fieldsets"][3]["fields"], ["subjects", "language"])

    def test_bando_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Bando").json()
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
