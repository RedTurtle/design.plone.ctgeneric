from design.plone.contenttypes.tests import test_ct_cartella_modulistica as base
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import get_fieldset_fields
from design.plone.ctgeneric.testing import PLONE_VOLTO_PREVIEW_FIELDSETS


class TestCartellaModulisticaSchema(base.TestCartellaModulisticaSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_cartella_modulistica_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/CartellaModulistica").json()
        expected = [
            "default",
            "settings",
            "ownership",
            "dates",
            "categorization",
            "preview_image",
            "layout",
            "seo",
        ]
        if not PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.remove("preview_image")
        self.assertEqual([x.get("id") for x in resp["fieldsets"]], expected)

    def test_cartella_modulistica_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/CartellaModulistica").json()
        expected = ["title", "description", "visualize_files", "image", "image_caption"]
        if not PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.extend(["preview_image", "preview_caption"])
        self.assertEqual(resp["fieldsets"][0]["fields"], expected)

    def test_cartella_modulistica_fields_layout_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/CartellaModulistica").json()
        self.assertEqual(
            get_fieldset_fields(resp, "layout"), ["blocks", "blocks_layout"]
        )

    def test_cartella_modulistica_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/CartellaModulistica").json()
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
