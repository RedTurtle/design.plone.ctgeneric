from design.plone.contenttypes.tests import test_ct_persona as base
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest


class TestPersonaSchema(base.TestPersonaSchema):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_persona(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Persona"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.relateditems",
                "plone.categorization",
                "plone.basic",
                "plone.locking",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "plone.constraintypes",
                "design.plone.contenttypes.behavior.persona_v2",
            ),
        )

    def test_persona_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "ruolo",
                "contatti",
                "documenti",
                "informazioni",
                "correlati",
                "categorization",
                "dates",
                "ownership",
                "settings",
                "seo",
            ],
        )

    def test_persona_required_fields(self):
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["title", "ruolo", "tipologia_persona"]),
        )

    def test_persona_fields_ruolo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            [
                "ruolo",
                "organizzazione_riferimento",
                "data_conclusione_incarico",
                "competenze",
                "deleghe",
                "tipologia_persona",
                "data_insediamento",
                "biografia",
            ],
        )

    def test_persona_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(resp["fieldsets"][2]["fields"], ["telefono", "fax", "email"])

    def test_persona_fields_documenti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            [
                "curriculum_vitae",
                "emolumenti_a_carico_della_finanza_pubblica",
                "dichiarazioni_di_insussistenza_e_incompatibilita",
                "atto_nomina",
            ],
        )

    def test_persona_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(resp["fieldsets"][5]["fields"], ["relatedItems"])

    def test_persona_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(resp["fieldsets"][6]["fields"], ["subjects", "language"])

    def test_persona_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(resp["fieldsets"][7]["fields"], ["effective", "expires"])

    def test_persona_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"], ["creators", "contributors", "rights"]
        )

    def test_persona_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][9]["fields"],
            [
                "allow_discussion",
                "exclude_from_nav",
                "id",
                "versioning_enabled",
                "changeNote",
            ],
        )

    def test_persona_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
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

    @unittest.skip("ctgeneric removes incarichi folder and incarichi_persona field")
    def test_atto_di_nomina_incarico(self):
        pass

    @unittest.skip("ctgeneric removes incarichi folder and incarichi_persona field")
    def test_delete_incarico_and_call_persona(self):
        pass

    @unittest.skip("ctgeneric removes incarichi folder and incarichi_persona field")
    def test_unauthorized_on_subfolder(self):
        pass


class TestPersonaEndpoint(unittest.TestCase):
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

        self.persona = api.content.create(
            container=self.portal, type="Persona", title="John Doe"
        )
        intids = getUtility(IIntIds)

        self.persona_ref = RelationValue(intids.getId(self.persona))
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_persona_strutture_correlate(self):
        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO 1",
            persone_struttura=[self.persona_ref],
        )
        commit()
        response = self.api_session.get(self.persona.absolute_url())
        res = response.json()

        self.assertIn("strutture_correlate", list(res.keys()))
        self.assertEqual(len(res["strutture_correlate"]), 1)
        self.assertEqual(res["strutture_correlate"][0]["title"], uo.title)

    def test_persona_responsabile_di(self):
        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO 1",
            responsabile=[self.persona_ref],
        )
        commit()
        response = self.api_session.get(self.persona.absolute_url())
        res = response.json()

        self.assertIn("responsabile_di", list(res.keys()))
        self.assertEqual(len(res["responsabile_di"]), 1)
        self.assertEqual(res["responsabile_di"][0]["title"], uo.title)

    def test_persona_assessore_di(self):
        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO 1",
            assessore_riferimento=[self.persona_ref],
        )
        commit()
        response = self.api_session.get(self.persona.absolute_url())
        res = response.json()

        self.assertIn("assessore_di", list(res.keys()))
        self.assertEqual(len(res["assessore_di"]), 1)
        self.assertEqual(res["assessore_di"][0]["title"], uo.title)

    def test_persona_substructure_created(self):
        self.api_session.post(
            self.portal_url,
            json={"@type": "Persona", "title": "John"},
        )

        commit()
        persona = self.portal["john"]
        self.assertEqual(
            [
                "foto-e-attivita-politica",
                "curriculum-vitae",
                "situazione-patrimoniale",
                "dichiarazione-dei-redditi",
                "spese-elettorali",
                "variazione-situazione-patrimoniale",
                "altre-cariche",
                "altri-documenti",
                "dichiarazione-insussistenza-cause-di-inconferibilita-e-incompatibilita",  # noqa
                "emolumenti-complessivi-percepiti-a-carico-della-finanza-pubblica",
                "compensi",
                "importi-di-viaggio-e-o-servizi",
            ],
            persona.keys(),
        )
