from design.plone.contenttypes.tests import test_ct_document as base
from design.plone.ctgeneric.testing import CORE_TYPES_ALLOW_DISCUSSION
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import get_fieldset_fields
from design.plone.ctgeneric.testing import PLONE_VOLTO_PREVIEW_FIELDSETS
from plone import api


class TestDocumentSchema(base.TestDocumentSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_document(self):
        portal_types = api.portal.get_tool(name="portal_types")
        behaviors = ["plone.namefromtitle"]
        if CORE_TYPES_ALLOW_DISCUSSION:
            behaviors.append("plone.allowdiscussion")
        behaviors.extend(
            [
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.dublincore",
                "plone.relateditems",
                "plone.locking",
            ]
        )
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            # added by plone.volto >= 5.1
            behaviors.extend(["volto.preview_image_link", "volto.navtitle"])
        behaviors.extend(
            [
                "volto.blocks",
                "plone.versioning",
                "design.plone.contenttypes.behavior.info_testata",
                "design.plone.contenttypes.behavior.argomenti_document",
                "plone.translatable",
                "design.plone.contenttypes.behavior.show_modified",
                "kitconcept.seo",
                "plone.constraintypes",
                "design.plone.contenttypes.behavior.exclude_from_search",
                "plone.leadimage",
                "volto.preview_image",
            ]
        )
        self.assertEqual(portal_types["Document"].behaviors, tuple(behaviors))

    def test_document_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        expected = [
            "default",
            "testata",
            "settings",
            "correlati",
            "categorization",
            "dates",
            "ownership",
            "layout",
        ]
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.append("preview_image")
        expected.append("seo")
        self.assertEqual([x.get("id") for x in resp["fieldsets"]], expected)

    def test_document_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        expected = ["exclude_from_nav", "id"]
        if CORE_TYPES_ALLOW_DISCUSSION:
            expected.insert(0, "allow_discussion")
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            # volto.navtitle behavior, added by plone.volto >= 5.1
            expected.append("nav_title")
        expected.extend(
            [
                "versioning_enabled",
                "show_modified",
                "exclude_from_search",
                "changeNote",
            ]
        )
        self.assertEqual(resp["fieldsets"][2]["fields"], expected)

    def test_document_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            ["relatedItems", "correlato_in_evidenza"],
        )

    def test_document_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
        self.assertEqual(resp["fieldsets"][4]["fields"], ["subjects", "language"])

    def test_document_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Document").json()
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
