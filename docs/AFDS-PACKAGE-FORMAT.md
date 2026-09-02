# AFDS package format

**Superseded.** The normative content of this document is now Part IV of [the AFDS specification](AFDS-SPECIFICATION.md), and this file is retained only as a pointer.

Part IV, Serialisation, carries the container rules, the media type, the declared package hierarchy, the six artefact roles, the two root artefacts, the verification algorithm, the security requirements, the adapter requirements, the completeness profiles, and the versioning rules.

| Former section | Now |
| --- | --- |
| 1. Scope and status | Clause 1, and the Status of this document |
| 2. Conformance language | Clause 4.1 |
| 3. Container rules | Clause 25 |
| 4. Media type | Clause 26 |
| 5. Declared package hierarchy | Clause 27 |
| 6. Artefact roles | Clause 28 |
| 7. `afds-manifest.json` | Clause 29 |
| 8. `afds-inventory.json` | Clause 30 |
| 9. Verification algorithm | Clause 31 |
| 10. Security requirements | Clause 32 |
| 11. Adapters | Clause 33 |
| 12. Conformance profiles | Clause 34, renamed completeness profiles |
| 13. Versioning | Clause 35 |
| 14. Relationship to Open Packaging Conventions | Annex A |
| 15. Open questions | [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) |
| 16. References | Clause 6 |

Part IV also specifies three bindings this document never carried, because the clauses that needed them did not exist when it was written: the `methodProfiles` array at clause 29.1, a locally defined method profile and its serialised provenance object at clause 29.3, and the pattern registry path at clause 29.4.

The `conformanceProfile` field keeps its name and is now described as a completeness profile, which is all it ever stated.
