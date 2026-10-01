"""Setup tests for this package."""

from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import HAS_GET_FOLDER_CONTENTS
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit

import unittest


class TestBaseSerializer(unittest.TestCase):
    """"""

    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def tearDown(self):
        self.api_session.close()

    @unittest.skipIf(
        not HAS_GET_FOLDER_CONTENTS,
        "design.plone.contenttypes folder serializer uses getFolderContents, "
        "removed in this Plone version",
    )
    def test_design_italia_meta_type_news_with_tipologia(self):
        """
        News should return the news type (tipologia_notizia field)
        Other types should return their own portal_type.
        """
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="TestNews",
            tipologia_notizia="Foo",
        )
        commit()
        resp = self.api_session.get(news.absolute_url() + "?fullobjects")
        self.assertEqual(
            resp.json()["design_italia_meta_type"],
            news.tipologia_notizia,
        )

    @unittest.skipIf(
        not HAS_GET_FOLDER_CONTENTS,
        "design.plone.contenttypes folder serializer uses getFolderContents, "
        "removed in this Plone version",
    )
    def test_design_italia_meta_type_news_without_tipologia(self):
        """
        News should return the news type (tipologia_notizia field)
        Other types should return their own portal_type.
        """
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="TestNews",
        )
        commit()
        resp = self.api_session.get(news.absolute_url() + "?fullobjects")
        self.assertEqual(
            resp.json()["design_italia_meta_type"],
            "Notizie e comunicati stampa",
        )

    @unittest.skipIf(
        not HAS_GET_FOLDER_CONTENTS,
        "design.plone.contenttypes folder serializer uses getFolderContents, "
        "removed in this Plone version",
    )
    def test_design_italia_meta_type_with_type_different_from_news(self):
        """
        News should return the news type (tipologia_notizia field)
        Other types should return their own portal_type.
        """
        service = api.content.create(
            container=self.portal, type="Servizio", title="TestService"
        )
        commit()
        resp = self.api_session.get(service.absolute_url() + "?fullobjects")
        self.assertEqual(
            resp.json()["design_italia_meta_type"],
            "Servizio",
        )
