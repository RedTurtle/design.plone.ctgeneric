# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from design.plone.ctgeneric.interfaces import IDesignPloneV2Settings


class DesignPloneV2ControlPanelForm(RegistryEditForm):
    schema = IDesignPloneV2Settings
    id = "design-plone-v2-control-panel"
    label = _("Impostazioni Design Plone V2")


class DesignPloneV2ControlPanelView(ControlPanelFormWrapper):
    """ """

    form = DesignPloneV2ControlPanelForm
