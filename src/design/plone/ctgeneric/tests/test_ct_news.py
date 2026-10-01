from design.plone.contenttypes.tests import test_ct_news as base
from design.plone.ctgeneric.interfaces import IDesignPloneV2Settings
from design.plone.ctgeneric.testing import CORE_TYPES_ALLOW_DISCUSSION
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import get_fieldset_fields
from design.plone.ctgeneric.testing import PLONE_VOLTO_PREVIEW_FIELDSETS
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import json
import transaction
import unittest


class TestNewsSchema(base.TestNewsSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_news(self):
        portal_types = api.portal.get_tool(name="portal_types")
        behaviors = ["plone.dublincore", "plone.namefromtitle"]
        if CORE_TYPES_ALLOW_DISCUSSION:
            behaviors.append("plone.allowdiscussion")
        behaviors.extend(
            [
                "plone.shortname",
                "plone.excludefromnavigation",
                "plone.relateditems",
                "plone.leadimage",
                "plone.versioning",
                "plone.locking",
            ]
        )
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            # added by plone.volto >= 5.1
            behaviors.extend(["volto.preview_image_link", "volto.navtitle"])
        behaviors.extend(
            [
                "volto.preview_image",
                "design.plone.contenttypes.behavior.news",
                "design.plone.contenttypes.behavior.argomenti_news",
                "plone.constraintypes",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "design.plone.contenttypes.behavior.news_v2",
            ]
        )
        self.assertEqual(portal_types["News Item"].behaviors, tuple(behaviors))

    def test_news_item_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News%20Item").json()
        expected = [
            "default",
            "dates",
            "correlati",
            "categorization",
            "settings",
            "ownership",
        ]
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.append("preview_image")
        expected.append("seo")
        self.assertEqual([x.get("id") for x in resp["fieldsets"]], expected)

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
        expected = ["title", "description", "image", "image_caption"]
        if not PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.extend(["preview_image", "preview_caption"])
        expected.extend(
            [
                "numero_progressivo_cs",
                "a_cura_di",
                "a_cura_di_persone",
                "luoghi_correlati",
                "notizie_correlate",
                "descrizione_estesa",
                "tipologia_notizia",
                "tassonomia_argomenti",
            ]
        )
        self.assertEqual(resp["fieldsets"][0]["fields"], expected)

    def test_news_item_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News%20Item").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["relatedItems", "correlato_in_evidenza"],
        )

    def test_news_item_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News%20Item").json()
        self.assertEqual(resp["fieldsets"][3]["fields"], ["subjects", "language"])

    def test_news_item_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News%20Item").json()
        expected = ["id", "exclude_from_nav", "versioning_enabled"]
        if CORE_TYPES_ALLOW_DISCUSSION:
            expected.insert(0, "allow_discussion")
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            # volto.navtitle behavior, added by plone.volto >= 5.1
            expected.append("nav_title")
        expected.append("changeNote")
        self.assertEqual(resp["fieldsets"][4]["fields"], expected)

    def test_news_item_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News%20Item").json()
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


class TestNewsApi(unittest.TestCase):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.document = api.content.create(
            container=self.portal, type="Document", title="Document"
        )

        # we need it because of vocabularies
        api.portal.set_registry_record(
            "tipologie_notizia",
            json.dumps({"en": ["foo", "bar"]}),
            interface=IDesignPloneV2Settings,
        )
        transaction.commit()

    def tearDown(self):
        self.api_session.close()
        super().setUp()

    def test_newsitem_required_fields(self):
        response = self.api_session.post(
            self.portal_url,
            json={"@type": "News Item", "title": "Foo"},
        )
        self.assertEqual(response.status_code, 400)

        response = self.api_session.post(
            self.portal_url,
            json={"@type": "News Item", "title": "Foo", "tipologia_notizia": "foo"},
        )
        self.assertEqual(response.status_code, 201)

    def test_newsitem_substructure_created(self):
        self.api_session.post(
            self.portal_url,
            json={
                "@type": "News Item",
                "title": "Foo",
                "tipologia_notizia": "foo",
                "a_cura_di": self.document.UID(),
            },
        )

        transaction.commit()
        news = self.portal["foo"]

        self.assertEqual(["multimedia", "documenti-allegati"], news.keys())

        self.assertEqual(news["multimedia"].portal_type, "Document")
        self.assertEqual(news["multimedia"].constrain_types_mode, 1)
        self.assertEqual(news["multimedia"].locally_allowed_types, ("Image", "Link"))

        self.assertEqual(news["documenti-allegati"].portal_type, "Document")
        self.assertEqual(news["documenti-allegati"].constrain_types_mode, 1)
        self.assertEqual(
            news["documenti-allegati"].locally_allowed_types, ("File", "Image")
        )
