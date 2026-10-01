from design.plone.contenttypes.tests import test_ct_event as base
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import PLONE_VOLTO_PREVIEW_FIELDSETS
from plone import api


class TestEventSchema(base.TestEventSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_event(self):
        portal_types = api.portal.get_tool(name="portal_types")
        behaviors = []
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            # added by plone.volto >= 5.1
            behaviors.extend(["volto.preview_image_link", "volto.navtitle"])
        behaviors.extend(
            [
                "plone.eventbasic",
                "plone.leadimage",
                "volto.preview_image",
                "design.plone.contenttypes.behavior.argomenti_evento",
                "plone.eventrecurrence",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "design.plone.contenttypes.behavior.evento",
                "design.plone.contenttypes.behavior.luoghi_correlati_evento",
                "design.plone.contenttypes.behavior.address_event",
                "design.plone.contenttypes.behavior.geolocation_event",
                "design.plone.contenttypes.behavior.strutture_correlate",
                "plone.dublincore",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.relateditems",
                "plone.versioning",
                "plone.locking",
                "plone.constraintypes",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "design.plone.contenttypes.behavior.evento_v2",
            ]
        )
        self.assertEqual(portal_types["Event"].behaviors, tuple(behaviors))

    def test_event_required_fields(self):
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["title", "start", "end", "prezzo"]),
        )

    def test_event_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        expected = [
            "default",
            "cose",
            "luogo",
            "date_e_orari",
            "costi",
            "contatti",
            "informazioni",
            "correlati",
            "categorization",
            "dates",
            "settings",
            "ownership",
        ]
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.append("preview_image")
        expected.append("seo")
        self.assertEqual([x.get("id") for x in resp["fieldsets"]], expected)

    def test_event_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected = [
                "title",
                "description",
                "image",
                "image_caption",
                "tassonomia_argomenti",
                "sottotitolo",
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
                "sottotitolo",
            ]
        self.assertEqual(resp["fieldsets"][0]["fields"], expected)

    def test_event_fields_date_e_orari_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            [
                "start",
                "end",
                "whole_day",
                "open_end",
                "sync_uid",
                "recurrence",
                "orari",
            ],
        )

    def test_event_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"],
            [
                "organizzato_da_interno",
                "organizzato_da_esterno",
                "telefono",
                "fax",
                "reperibilita",
                "email",
                "web",
                "supportato_da",
            ],
        )

    def test_event_fields_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            ["ulteriori_informazioni", "patrocinato_da", "strutture_politiche"],
        )

    def test_event_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][7]["fields"],
            ["correlato_in_evidenza", "relatedItems"],
        )

    def test_event_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(resp["fieldsets"][8]["fields"], ["subjects", "language"])

    def test_event_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(resp["fieldsets"][9]["fields"], ["effective", "expires"])

    def test_event_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        expected = [
            "allow_discussion",
            "exclude_from_nav",
            "id",
            "versioning_enabled",
            "changeNote",
        ]
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            # volto.navtitle behavior, added by plone.volto >= 5.1
            expected.insert(0, "nav_title")
        self.assertEqual(resp["fieldsets"][10]["fields"], expected)

    def test_event_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][11]["fields"], ["creators", "contributors", "rights"]
        )

    def test_event_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
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
