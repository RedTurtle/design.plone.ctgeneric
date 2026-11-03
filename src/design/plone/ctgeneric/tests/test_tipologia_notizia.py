from collective.taxonomy.interfaces import ITaxonomy
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_INTEGRATION_TESTING
from design.plone.ctgeneric.upgrades.upgrades import to_1002
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility

import unittest


class TestTipologiaNotizia(unittest.TestCase):
    layer = DESIGN_PLONE_CTGENERIC_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.catalog = api.portal.get_tool(name="portal_catalog")
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_taxonomy_removed(self):
        self.assertIsNone(
            queryUtility(ITaxonomy, name="collective.taxonomy.tipologia_notizia")
        )
        self.assertNotIn(
            "collective.taxonomy.generated.tipologia_notizia",
            api.portal.get_tool(name="portal_types")["News Item"].behaviors,
        )

    def test_querystring_criterion_uses_controlpanel_vocabulary(self):
        self.assertEqual(
            api.portal.get_registry_record(
                "plone.app.querystring.field.tipologia_notizia.vocabulary"
            ),
            "design.plone.vocabularies.tipologie_notizia",
        )
        self.assertTrue(
            api.portal.get_registry_record(
                "plone.app.querystring.field.tipologia_notizia.enabled"
            )
        )

    def test_index_is_a_field_index(self):
        index = self.catalog._catalog.getIndex("tipologia_notizia")
        self.assertEqual(index.meta_type, "FieldIndex")
        self.assertIn("tipologia_notizia", self.catalog.schema())

    def test_news_indexed_with_vocabulary_value(self):
        api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            tipologia_notizia="Comunicato stampa",
        )
        brains = self.catalog(tipologia_notizia="Comunicato stampa")
        self.assertEqual(len(brains), 1)
        self.assertEqual(brains[0].tipologia_notizia, "Comunicato stampa")

    def test_upgrade_step_can_be_run_again(self):
        api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            tipologia_notizia="Avviso",
        )
        to_1002(api.portal.get_tool(name="portal_setup"))

        index = self.catalog._catalog.getIndex("tipologia_notizia")
        self.assertEqual(index.meta_type, "FieldIndex")
        self.assertEqual(len(self.catalog(tipologia_notizia="Avviso")), 1)
        self.assertEqual(
            api.portal.get_registry_record(
                "plone.app.querystring.field.tipologia_notizia.vocabulary"
            ),
            "design.plone.vocabularies.tipologie_notizia",
        )
