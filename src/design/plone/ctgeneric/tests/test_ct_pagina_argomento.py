from design.plone.contenttypes.tests import test_ct_pagina_argomento as base
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import get_fieldset_fields
from design.plone.ctgeneric.testing import PLONE_VOLTO_PREVIEW_FIELDSETS


class TestPaginaArgomentoSchema(base.TestPaginaArgomentoSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_pagina_argomento_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        expected = [
            "default",
            "informazioni",
            "correlati",
            "categorization",
            "dates",
            "settings",
            "layout",
            "ownership",
        ]
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.append("preview_image")
        expected.append("seo")
        self.assertEqual([x.get("id") for x in resp["fieldsets"]], expected)

    def test_pagina_argomento_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        expected = [
            "title",
            "description",
            "icona",
            "unita_amministrative_responsabili",
            "image",
            "image_caption",
        ]
        if not PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.extend(["preview_image", "preview_caption"])
        self.assertEqual(resp["fieldsets"][0]["fields"], expected)

    def test_pagina_argomento_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(resp["fieldsets"][2]["fields"], ["relatedItems"])

    def test_pagina_argomento_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(resp["fieldsets"][3]["fields"], ["subjects", "language"])

    def test_pagina_argomento_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(resp["fieldsets"][4]["fields"], ["effective", "expires"])

    def test_pagina_argomento_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"],
            [
                "allow_discussion",
                "exclude_from_nav",
                "id",
                "versioning_enabled",
                "changeNote",
            ],
        )

    def test_pagina_argomento_fields_layout_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(resp["fieldsets"][6]["fields"], ["blocks", "blocks_layout"])

    def test_pagina_argomento_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
        self.assertEqual(
            resp["fieldsets"][7]["fields"], ["creators", "contributors", "rights"]
        )

    def test_pagina_argomento_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Pagina%20Argomento").json()
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
