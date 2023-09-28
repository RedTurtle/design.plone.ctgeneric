# -*- coding: utf-8 -*-
from design.plone.ctgeneric.testing import (
    DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING,
)
from design.plone.contenttypes.tests.test_ct_news import (
    TestNewsSchema as BaseSchemaTest,
)
from plone import api


class TestNewsSchema(BaseSchemaTest):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_news(self):
        portal_types = api.portal.get_tool(name="portal_types")

        self.assertEqual(
            portal_types["News Item"].behaviors,
            (
                "plone.dublincore",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.shortname",
                "plone.excludefromnavigation",
                "plone.relateditems",
                "plone.leadimage",
                "plone.versioning",
                "plone.locking",
                "volto.preview_image",
                "plone.constraintypes",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "design.plone.contenttypes.behavior.news_v2",
                "design.plone.contenttypes.behavior.argomenti",
            ),
        )

    def test_news_item_required_fields(self):
        resp = self.api_session.get("@types/News%20Item").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                    "tipologia_notizia",
                ]
            ),
        )

    def test_news_item_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News%20Item").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "descrizione_estesa",
                "tipologia_notizia",
                "numero_progressivo_cs",
                "a_cura_di",
                "a_cura_di_persone",
                "luoghi_correlati",
                "notizie_correlate",
                "tassonomia_argomenti",
            ],
        )

    def test_news_item_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News%20Item").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["correlato_in_evidenza"],
        )
