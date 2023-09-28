# -*- coding: utf-8 -*-
from design.plone.ctgeneric.testing import (
    DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING,
)
from design.plone.contenttypes.tests.test_ct_pagina_argomento import (
    TestPaginaArgomentoSchema as BaseSchemaTest,
)


class TestPaginaArgomentoSchema(BaseSchemaTest):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
