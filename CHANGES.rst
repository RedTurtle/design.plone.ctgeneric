Changelog
=========

1.1.0 (unreleased)
------------------

- Configured the package with plone.meta; CI now only tests Plone 6.0, 6.1 and 6.2 on Python 3.11+.
  [mamico]


1.0.8 (2026-09-15)
------------------

- Removed a list-of-lists issue on the PersonaSerializer
  [fedevancin]


1.0.7 (2026-08-05)
------------------

- Fixed a bug in the Persona serializer when there are no contact points.
  [fedevancin]


1.0.6 (2025-08-05)
------------------

- Documento CT: removed field ufficio_responsabile already defined in design.plone.contenttypes.
  [daniele]

1.0.5 (2025-07-16)
------------------

- Fix controlpanel label.
  [cekk]


1.0.4 (2025-07-16)
------------------

- Fix mapping for Persona.
  [daniele]
- Remove not needed z3c.jbot dependency.
  [cekk]

1.0.3 (2024-06-24)
------------------

- Fix breaking change in SUBFOLDERS_MAPPING in design.plone.contenttypes == 6.2.11.
  [cekk]


1.0.2 (2024-04-18)
------------------

- Fix wrong release.
  [cekk]

1.0.1 (2024-04-18)
------------------

- Avoid attributerror when getting tipologia_notizia.
  [cekk]


1.0.0 (2024-04-18)
------------------

- Initial release.
  [cekk]
