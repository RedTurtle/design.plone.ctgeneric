from design.plone.contenttypes.tests import test_ct_servizio as base
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from design.plone.ctgeneric.testing import get_fieldset_fields
from design.plone.ctgeneric.testing import PLONE_VOLTO_PREVIEW_FIELDSETS
from plone import api


class TestServizioSchema(base.TestServizioSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_servizio(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Servizio"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.categorization",
                "plone.basic",
                "design.plone.contenttypes.behavior.descrizione_estesa_servizio",
                "plone.locking",
                "plone.leadimage",
                "volto.preview_image",
                "plone.relateditems",
                "design.plone.contenttypes.behavior.argomenti_servizio",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "design.plone.contenttypes.behavior.servizio_v2",
            ),
        )

    def test_servizio_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        expected = [
            "default",
            "cose",
            "a_chi_si_rivolge",
            "accedi_al_servizio",
            "cosa_serve",
            "costi_e_vincoli",
            "tempi_e_scadenze",
            "casi_particolari",
            "contatti",
            "documenti",
            "link_utili",
            "informazioni",
            "correlati",
            "categorization",
            "settings",
            "ownership",
            "dates",
        ]
        if PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.append("preview_image")
        expected.append("seo")
        self.assertEqual([x.get("id") for x in resp["fieldsets"]], expected)

    def test_servizio_required_fields(self):
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["title", "cosa_serve", "ufficio_responsabile"]),
        )

    def test_servizio_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        expected = [
            "title",
            "description",
            "sottotitolo",
            "stato_servizio",
            "motivo_stato_servizio",
            "image",
            "image_caption",
        ]
        if not PLONE_VOLTO_PREVIEW_FIELDSETS:
            expected.extend(["preview_image", "preview_caption"])
        expected.append("tassonomia_argomenti")
        self.assertEqual(resp["fieldsets"][0]["fields"], expected)

    def test_servizio_fields_a_chi_si_rivolge_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["a_chi_si_rivolge", "chi_puo_presentare", "copertura_geografica"],
        )

    def test_servizio_fields_accedi_al_servizio_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            [
                "come_si_fa",
                "cosa_si_ottiene",
                "procedure_collegate",
                "canale_digitale",
                "autenticazione",
                "dove_rivolgersi",
                "dove_rivolgersi_extra",
                "prenota_appuntamento",
            ],
        )

    def test_servizio_fields_tempi_e_scadenze_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            ["tempi_e_scadenze"],
        )

    def test_servizio_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"],
            ["ufficio_responsabile", "area"],
        )

    def test_servizio_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][12]["fields"],
            ["servizi_collegati", "relatedItems", "correlato_in_evidenza"],
        )

    def test_servizio_fields_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][11]["fields"], ["ulteriori_informazioni"])

    def test_servizio_fields_categorization_fieldset(self):
        """
        codice_ipa and settore_merceologico are moved here by SchemaTweaks
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][13]["fields"],
            [
                "identificativo",
                "codice_ipa",
                "settore_merceologico",
                "subjects",
                "language",
            ],
        )

    def test_servizio_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
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
