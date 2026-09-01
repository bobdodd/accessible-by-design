<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (C) 2026 Bob Dodd -->

# AFDS package format

This document specifies the `.afds` package: the single-file distribution format for an Accessibility Focused Design System bundle.

It is the normative companion to the colophon decisions that adopt AFDS as a portable bundle and then adopt `.afds` as its distribution container.
Where this document and those decisions disagree, the disagreement is a defect in this document.

## 1. Scope and status

AFDS 1.0.0 is a project draft.
It is not a W3C standard, not a published industry specification, and not on any standards track.

The project intends to monitor and seek alignment with the W3C Design System Documentation Community Group, Open UI, and future Design Tokens Community Group work.
The W3C UI Specification Schema Community Group was previously named here as an alignment target; that group closed on 2026-05-21 without publishing a schema, so its charter is now read as a requirements input rather than as a vocabulary to align to.
The AFDS component-specification and evidence formats are provisional and are intended to be mapped to, or contributed as requirements for, the remaining efforts rather than to become isolated terminology.
A reader should treat every identifier and field name here as stable within this project and unstable outside it.

### 1.1 What this document specifies

This document specifies the container, the two required root artefacts, the declared package hierarchy, artefact roles, a verification algorithm, security requirements, adapter reporting, conformance profiles, and versioning behaviour.

### 1.2 What this document does not specify

This document does not specify the internal schema of a design-token file; that is the Design Tokens Format Module's business, and a package declares which version of it applies.
It does not specify the internal schema of a component specification beyond requiring that one exists and is machine-readable.
It does not specify a signature format, a package registry, an update protocol, or an editing tool.

### 1.3 Audience

The audience is the author of a tool that produces or consumes `.afds` packages, and the reviewer of a package who needs to decide whether it conforms.

## 2. Conformance language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in RFC 2119.

They are used in this document with the following force.

| Keyword | Force in this document |
| --- | --- |
| MUST, REQUIRED, SHALL | An absolute requirement. A package or tool that breaks it does not conform. |
| MUST NOT, SHALL NOT | An absolute prohibition. |
| SHOULD, RECOMMENDED | A strong expectation. Ignoring it requires a stated reason and must be understood to have consequences. |
| SHOULD NOT | A strong expectation against. Doing it anyway requires a stated reason. |
| MAY, OPTIONAL | Genuinely optional. A consumer MUST NOT assume the optional behaviour is present. |

These keywords are written in capitals throughout, and are also marked as emphasis.
The capitalisation is the signal and the emphasis is redundant reinforcement of it, so a reader or renderer that conveys no emphasis loses nothing.
No requirement depends on colour, on typographic weight, or on emphasis being perceived.
Clause 4.1 of [the AFDS specification](AFDS-SPECIFICATION.md) states this convention in full and governs it.

Two roles are used in requirements.
A **producer** is any tool or person that creates a package.
A **consumer** is any tool or person that reads a package and relies on its contents.

## 3. Container rules

A `.afds` package is a ZIP archive with a particular name, a particular pair of required entries, and a particular set of restrictions.

### 3.1 Normative container requirements

A conforming `.afds` package MUST satisfy every requirement in this table.

| Requirement | Statement |
| --- | --- |
| ZIP syntax | The file MUST use ZIP syntax and MUST be readable by an ordinary ZIP reader. |
| Extension | The file MUST use the `.afds` extension. |
| No enclosing directory | The archive MUST NOT wrap its contents in a single enclosing top-level directory. `afds-manifest.json` sits at the archive root. |
| Root manifest | The archive MUST include an entry named exactly `afds-manifest.json` at the archive root. |
| Root inventory | The archive MUST include an entry named exactly `afds-inventory.json` at the archive root. |
| Normalised relative paths | Every entry path MUST be a normalised relative path using `/` as the separator. |
| No absolute paths | Entry paths MUST NOT begin with `/` and MUST NOT contain a drive letter or UNC prefix. |
| No traversal | Entry paths MUST NOT contain a `..` path segment, and MUST NOT contain a `.` segment. |
| UTF-8 text | Text content MUST be stored as UTF-8. A producer MUST NOT emit a byte-order mark. |
| No encryption | The archive MUST NOT contain encrypted entries when it is intended for portable interchange. |

### 3.2 Notes on the container requirements

The no-enclosing-directory rule exists so that a consumer can locate the manifest without guessing.
Many archive tools add a wrapper directory by default, so a producer MUST check its output rather than trusting the tool.

The path restrictions exist for security as well as tidiness, and section 10 explains the attack they defend against.
A consumer MUST reject a non-conforming path rather than attempting to sanitise it, because sanitising silently changes what the package says.

The encryption prohibition applies to portable interchange, which is the only case this document specifies.
A producer MAY encrypt a package for private transfer by wrapping the conforming `.afds` file in some other envelope, but the `.afds` file inside that envelope MUST itself be unencrypted.

Directory entries are permitted but carry no meaning.
A consumer MUST NOT rely on the presence of an explicit directory entry, and a producer SHOULD omit them.
Directory entries MUST NOT appear in the inventory, because they have no content to digest.

## 4. Media type

The underlying registered media type is `application/zip`.

AFDS has no dedicated IANA media-type registration.
Until it has one, `application/zip` is the correct type to serve a `.afds` file with, and the `.afds` extension together with the root `afds-manifest.json` entry identify the format.

A consumer MUST NOT rely on a media type of `application/afds+zip` or similar being present, because no such type is registered.
A consumer SHOULD identify a package by opening it and finding a parseable root manifest whose `afdsFormat` field is `afds-package`.
A producer MAY additionally advertise `application/afds+zip` in a private context where both ends agree, but MUST NOT treat that as a registered type.

Obtaining an IANA registration is recorded as an open question in section 15.

## 5. Declared package hierarchy

A package declares a fixed hierarchy so that a consumer knows where each kind of artefact lives without consulting a directory listing.

### 5.1 The hierarchy described

At the archive root sit exactly two required files.
`afds-manifest.json` states what the package is and where its canonical sources are.
`afds-inventory.json` states what the package contains, byte for byte.

Beneath the root sit up to nine directories.
`tokens/` holds design-token files.
`components/` holds one subdirectory per component, each containing a machine-readable contract and a human-readable specification.
`patterns/` holds multi-component flow documentation.
`manifests/` holds generated interface manifests such as a Custom Elements Manifest.
`evidence/` holds assistive-technology evidence records and known-limitations prose.
`adapters/` holds one subdirectory per adapter target, each with a declaration, a transform report, and, for an export adapter, the generated output.
`docs/` holds package documentation.
`schemas/` holds JSON Schema documents for the package's own machine-readable artefacts.
`stories/` holds executable examples and fixtures.

A licence summary, `LICENSES.md`, MAY sit at the root.
No other root-level file is defined by this document, and a producer SHOULD NOT add one.

### 5.2 The hierarchy as a table

| Path | Kind | Required | Contents |
| --- | --- | --- | --- |
| `afds-manifest.json` | File | REQUIRED | Package identity, version, licences, profile, and canonical source declarations |
| `afds-inventory.json` | File | REQUIRED | One record per package entry except itself, with length, media type, role, and digest |
| `tokens/` | Directory | REQUIRED in every profile | Design-token files validating against the declared Design Tokens Format Module version |
| `components/` | Directory | REQUIRED in the components and full profiles | One subdirectory per component |
| `patterns/` | Directory | OPTIONAL | Multi-component flow and guidance documentation |
| `manifests/` | Directory | OPTIONAL | Generated interface manifests, for example a Custom Elements Manifest |
| `evidence/` | Directory | REQUIRED in the full profile | Engine-qualified evidence records and known-limitations prose |
| `adapters/` | Directory | OPTIONAL | Adapter declarations, transform reports, and export output |
| `docs/` | Directory | RECOMMENDED | Human-readable package documentation |
| `schemas/` | Directory | OPTIONAL | JSON Schema documents for the package's machine-readable artefacts |
| `stories/` | Directory | OPTIONAL | Executable examples and test fixtures |
| `LICENSES.md` | File | RECOMMENDED | Human-readable statement of the licensing arrangement |

### 5.3 Rules about the hierarchy

A producer MUST NOT place a canonical token file outside `tokens/`.
A producer MUST NOT place a component contract outside `components/`.
A producer MUST NOT place adapter output or a transform report outside `adapters/`.

An empty optional directory carries no information.
A producer SHOULD omit an optional directory rather than shipping it empty, and MUST declare the absence in the manifest where the manifest has a corresponding field.
An empty array in the manifest is a positive declaration of absence and is preferable to omitting the field.

## 6. Artefact roles

Every inventoried entry has exactly one role.
The role records who owns the fact the entry carries, which is the mechanism that keeps the accessibility contract portable.

### 6.1 The six roles

| Role | Meaning |
| --- | --- |
| `canonical` | The authoritative source of the facts it carries. Nothing else in the package may contradict it. |
| `derived` | Generated from one or more canonical artefacts and reproducible from them. |
| `adapter` | Produced by an adapter for a specific external target, and shaped by that target's limits. |
| `evidence` | A record of observation: what was tested, on which engine and assistive technology, on what date, with what result. |
| `documentation` | Human-readable prose explaining canonical artefacts. Explanatory, not authoritative. |
| `schema` | A machine-readable schema that other artefacts in the package validate against. |

### 6.2 The ownership rule

A `derived` or `adapter` artefact MUST NOT be the only source of a fact owned by a `canonical` artefact.

The rule follows from what each role means.
A token value is owned by the canonical token file.
A component's semantic model, derivation, keyboard contract, Reflow behaviour, WCAG mapping, guarantees, non-guarantees, assertions, and uncertainty are owned by the canonical component contract.
An observation of assistive-technology behaviour is owned by an evidence record.
A guarantee's substantiation status is owned by neither, because it is computed from the two together and MUST NOT be written into either, as clause 14.3 of [the AFDS specification](AFDS-SPECIFICATION.md) requires.

If a fact exists only in a generated stylesheet, a design-tool library, or a platform resource bundle, then the fact has left the portable bundle.
At that point the package no longer carries the accessibility contract, which is the exact failure the format exists to prevent.

Two testable consequences follow.

The first is that any `derived` or `adapter` artefact MUST be regenerable from the canonical artefacts in the same package alone.
If regeneration loses a fact, the fact was only in the derived artefact and the package does not conform.
Section 11.4 states the single exception, which is an import report, because an import reads a source that lies outside the package by definition.

The second is that a consumer MAY discard every `derived` and `adapter` entry and still hold a complete design system.
A verifier can approximate this check by confirming that no `canonical` artefact references a `derived` or `adapter` path as its source.

### 6.3 Documentation is not authoritative

A `documentation` artefact explains a canonical artefact and MUST NOT introduce a normative fact of its own.
Where prose and contract disagree, the contract wins and the prose is a defect to be corrected.
This is stated because a reader naturally trusts the readable file over the machine-readable one, and in this format that instinct is wrong.

## 7. `afds-manifest.json`

The manifest states what the package is, who may use it and under what terms, which profile it claims, and where every canonical source lives.

### 7.1 Field specification

Nesting is shown with dotted paths.
A field marked REQUIRED MUST be present; a field marked OPTIONAL MAY be omitted, and a consumer MUST NOT infer a default beyond the one stated.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `afdsFormat` | String | REQUIRED | Format identifier. MUST be the exact string `afds-package`. |
| `afdsVersion` | String | REQUIRED | Version of this package format, as semantic versioning. `1.0.0` for this document. |
| `packageId` | String | REQUIRED | Stable identifier for the package, unique within its publisher's namespace. Reverse-DNS form is RECOMMENDED. |
| `packageVersion` | String | REQUIRED | Semantic version of the package payload, independent of `afdsVersion`. |
| `title` | String | REQUIRED | Human-readable package title. |
| `description` | String | REQUIRED | Prose description of what the package contains and is for. |
| `created` | String | REQUIRED | Creation date of this package version, as an ISO 8601 date. |
| `conformanceProfile` | String | REQUIRED | Declared profile identifier from section 12. |
| `licences.code` | String | REQUIRED | SPDX identifier for code and machine-readable artefacts. |
| `licences.documentation` | String | REQUIRED | SPDX identifier for prose. |
| `publisher.name` | String | REQUIRED | Name of the person or organisation publishing the package. |
| `publisher.project` | String | OPTIONAL | Project the package belongs to. |
| `publisher.uri` | String | OPTIONAL | Publisher URI. Informational only; it proves nothing about provenance. |
| `tokens.dtcgVersion` | String | REQUIRED | Version of the Design Tokens Format Module that the token files validate against. |
| `tokens.canonicalSources` | Array of source objects | REQUIRED | Canonical token files. MUST contain at least one entry in every profile. |
| `components.canonicalSources` | Array of component objects | REQUIRED in the components and full profiles | Canonical component declarations. |
| `patterns.canonicalSources` | Array of source objects | OPTIONAL | Canonical pattern documentation. An empty array declares absence. |
| `evidence.canonicalSources` | Array of source objects | REQUIRED in the full profile | Canonical evidence records. |
| `schemas.canonicalSources` | Array of source objects | OPTIONAL | Schema documents shipped in the package. |
| `documentation.sources` | Array of source objects | OPTIONAL | Documentation artefacts worth enumerating. |
| `adapters` | Array of adapter objects | REQUIRED | Declared adapters. An empty array declares that the package ships none. |
| `stories` | Array of source objects | OPTIONAL | Executable examples and fixtures. |
| `notes` | Array of strings | OPTIONAL | Statements a consumer should read before relying on the package. |

A **source object** has the following fields.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `id` | String | REQUIRED | Identifier unique within its array. |
| `path` | String | REQUIRED | Package-relative path to the artefact. MUST appear in the inventory. |
| `role` | String | REQUIRED | One of the six roles in section 6. |
| `description` | String | RECOMMENDED | What the artefact carries. |

A **component object** replaces `path` with two paths, because a component always has both a contract and a prose specification.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `id` | String | REQUIRED | Stable component identifier. |
| `name` | String | REQUIRED | Human-readable component name. |
| `kind` | String | REQUIRED | Component kind, for example `layout-primitive` or `interactive-component`. |
| `specification` | String | REQUIRED | Path to the machine-readable contract. |
| `documentation` | String | REQUIRED | Path to the human-readable specification. |
| `role` | String | REQUIRED | MUST be `canonical`. |

An **adapter object** is specified in section 11.

### 7.2 Worked example

The example below is the complete manifest of the sample package that accompanies this document, with the `adapters` array shown empty because that package ships no adapters.
Read it alongside the field table: every REQUIRED field appears, and every optional array that is absent from the payload is present as an empty array rather than omitted.

```json
{
  "afdsFormat": "afds-package",
  "afdsVersion": "1.0.0",
  "packageId": "com.a11ybob.abd.afds-sample",
  "packageVersion": "1.0.0",
  "title": "AFDS Sample",
  "description": "A minimal but complete Accessibility Focused Design System package.",
  "created": "2026-08-29",
  "conformanceProfile": "afds-components",
  "licences": {
    "code": "GPL-3.0-only",
    "documentation": "CC-BY-SA-4.0"
  },
  "publisher": {
    "name": "Bob Dodd",
    "project": "Accessible by Design",
    "uri": "https://a11ybob.com/"
  },
  "tokens": {
    "dtcgVersion": "2025.10",
    "canonicalSources": [
      {
        "id": "core",
        "path": "tokens/core.tokens.json",
        "role": "canonical",
        "description": "Core spacing, typography, measure, and colour tokens."
      }
    ]
  },
  "components": {
    "canonicalSources": [
      {
        "id": "stack",
        "name": "Stack",
        "kind": "layout-primitive",
        "specification": "components/stack/stack.spec.json",
        "documentation": "components/stack/stack.md",
        "role": "canonical"
      }
    ]
  },
  "patterns": { "canonicalSources": [] },
  "evidence": {
    "canonicalSources": [
      {
        "id": "at-matrix",
        "path": "evidence/at-matrix.json",
        "role": "evidence",
        "description": "Engine-qualified evidence records. All results are placeholders."
      }
    ]
  },
  "schemas": { "canonicalSources": [] },
  "adapters": [],
  "stories": [],
  "notes": [
    "AFDS 1.0.0 is a project draft, not a W3C standard.",
    "Inventory integrity is not a digital signature and does not prove provenance."
  ]
}
```

Three details in the example are worth naming.
The `dtcgVersion` field is what makes token validation possible at all, because a validator otherwise has to guess which version of the token format applies.
The `notes` array carries the two statements a consumer most needs before trusting the package.
The empty `adapters` array is a positive declaration, not an oversight, and section 5.3 requires it in preference to omitting the field.

## 8. `afds-inventory.json`

The inventory is what makes a package verifiable.
It lists every entry with enough information to detect any change between production and consumption.

### 8.1 What the inventory covers

The inventory MUST contain exactly one record for every entry in the archive, with one exception: it MUST NOT contain a record for itself.

The exclusion is necessary rather than stylistic.
A record of the inventory inside the inventory could never hold a correct digest, because writing the digest would change the bytes it describes.
Directory entries are also excluded, as section 3.2 states, because they have no content.

A consumer MUST verify the inventory before relying on any package content.
This means before parsing a token file, before reading a component contract, and before extracting anything to disk.

### 8.2 Field specification

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `afdsFormat` | String | REQUIRED | MUST be the exact string `afds-inventory`. |
| `afdsVersion` | String | REQUIRED | Package-format version, matching the manifest. |
| `packageId` | String | REQUIRED | MUST match the manifest's `packageId`. |
| `packageVersion` | String | REQUIRED | MUST match the manifest's `packageVersion`. |
| `digestAlgorithm` | String | REQUIRED | MUST be the exact string `SHA-256`. |
| `digestEncoding` | String | REQUIRED | MUST be the exact string `lowercase-hex`. |
| `excludesSelf` | Boolean | REQUIRED | MUST be `true`, stating explicitly that the inventory omits itself. |
| `entryCount` | Number | REQUIRED | Number of records. MUST equal the length of `records`. |
| `description` | String | RECOMMENDED | Prose statement of what the inventory does and does not prove. |
| `records` | Array of record objects | REQUIRED | One record per inventoried entry. |

Each **record object** has five REQUIRED fields.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `path` | String | REQUIRED | Package-relative normalised path of the entry. |
| `mediaType` | String | REQUIRED | Media type of the entry's content, including a charset parameter for text. |
| `byteLength` | Number | REQUIRED | Exact uncompressed length of the entry in bytes. |
| `role` | String | REQUIRED | One of the six roles in section 6. |
| `sha256` | String | REQUIRED | SHA-256 digest of the entry's exact uncompressed bytes, as lowercase hexadecimal. |

Records SHOULD be sorted by `path` in ascending byte order.
Sorting is a review convenience: a rebuilt inventory then produces a diff that shows only genuine changes.

### 8.3 Worked example

The example below is an abridged inventory from the sample package.
Two of the nine records are shown; the omitted records have the same shape.

```json
{
  "afdsFormat": "afds-inventory",
  "afdsVersion": "1.0.0",
  "packageId": "com.a11ybob.abd.afds-sample",
  "packageVersion": "1.0.0",
  "digestAlgorithm": "SHA-256",
  "digestEncoding": "lowercase-hex",
  "excludesSelf": true,
  "entryCount": 9,
  "description": "Inventory of every entry except this inventory itself. These digests detect transfer changes; they are not a digital signature.",
  "records": [
    {
      "path": "afds-manifest.json",
      "mediaType": "application/json",
      "byteLength": 2767,
      "role": "canonical",
      "sha256": "b480866e44ae0d66..."
    },
    {
      "path": "tokens/core.tokens.json",
      "mediaType": "application/json",
      "byteLength": 3055,
      "role": "canonical",
      "sha256": "b45bb732e28f4c3f..."
    }
  ]
}
```

The digests in the example are truncated for readability.
In a real inventory a `sha256` value MUST be the full 64 lowercase hexadecimal characters, and a consumer MUST reject a truncated, uppercase, or base-64 digest rather than attempting to interpret it.

## 9. Verification algorithm

A conforming consumer implements the following procedure.
The steps are ordered so that a cheap check never runs after an expensive one it could have prevented, and so that nothing is parsed before the container is known to be safe.

1. **Open as ZIP.**
   Open the file using ZIP syntax.
   If it is not a readable ZIP archive, report a container failure and stop.
2. **Check paths.**
   For every entry, confirm the path is a normalised relative path, contains no `..` or `.` segment, does not begin with `/`, and carries no drive letter or UNC prefix.
   Confirm no single enclosing top-level directory wraps the contents.
   Report each violation and stop, and do not sanitise.
3. **Check encryption and limits.**
   Confirm no entry is encrypted.
   Apply the configured limits from section 10 for entry count, total compressed size, total uncompressed size, per-entry decompression ratio, nesting depth, and path length.
   Report each violation and stop.
4. **Locate and parse the manifest.**
   Confirm `afds-manifest.json` exists at the archive root, decode it as UTF-8, parse it as JSON, and confirm `afdsFormat` is `afds-package`.
   Read `afdsVersion` and apply the version rules in section 13.
5. **Locate and parse the inventory.**
   Confirm `afds-inventory.json` exists at the archive root, decode it as UTF-8, and parse it as JSON.
   Confirm `afdsFormat` is `afds-inventory`, `digestAlgorithm` is `SHA-256`, `digestEncoding` is `lowercase-hex`, and `excludesSelf` is `true`.
   Confirm `packageId` and `packageVersion` match the manifest.
6. **Confirm completeness in both directions.**
   Confirm that every archive entry other than the inventory itself and other than directory entries has exactly one inventory record, and that every inventory record names an entry that exists.
   Confirm the inventory holds no record for itself.
   Confirm `entryCount` equals the number of records.
   Report every unmatched name in both directions.
7. **Compare byte lengths.**
   For each record, compare the entry's uncompressed length with `byteLength`.
   Report every mismatch.
8. **Recompute and compare digests.**
   For each record, compute the SHA-256 digest of the entry's exact uncompressed bytes and compare it with `sha256` as lowercase hexadecimal.
   Report every mismatch.
   If any digest fails, the consumer MUST NOT rely on any package content.
9. **Validate token files.**
   For each canonical token source named in the manifest, decode it as UTF-8, parse it as JSON, and validate it against the Design Tokens Format Module version declared in `tokens.dtcgVersion`.
   Report every validation failure.
   A consumer that cannot validate against the declared version MUST report that it did not validate, rather than passing the step silently.
10. **Report.**
    Emit a single report giving a pass or fail verdict, the count of entries checked, and every individual problem found.
    A consumer MUST NOT report a pass when any step failed, and MUST distinguish "checked and passed" from "not checked".

Two properties of the procedure are deliberate.

Steps 2 and 3 run before anything is parsed or extracted, so a hostile archive is rejected before its content is touched.
Steps 6 to 9 gather all problems rather than stopping at the first, because a partial report causes a producer to fix one defect at a time.

## 10. Security requirements

A package arrives from somewhere else, so a consumer must treat it as untrusted input.

### 10.1 Path traversal

A ZIP archive stores a path for each entry, and nothing in ZIP syntax prevents that path being absolute or containing `..` segments.
A naive extractor that joins the entry path onto an output directory can therefore be made to write outside that directory, overwriting arbitrary files.

A consumer MUST reject any entry whose path is absolute, contains a `..` or `.` segment, or is not normalised.
A consumer MUST perform this check before extracting anything.
A consumer MUST NOT rewrite an offending path into a safe one, because that silently changes what the package says and hides the attack.

### 10.2 Decompression limits

A small archive can expand to an enormous volume of data, exhausting memory or disk.
This is the zip-bomb class of attack, and nesting archives inside archives multiplies it.

A consumer MUST enforce configured limits and MUST fail rather than continuing when a limit is reached.

| Limit | Purpose | Suggested default |
| --- | --- | --- |
| Entry count | Bound the number of records and file handles | 5000 entries |
| Total compressed size | Bound the input read | 32 MiB |
| Total uncompressed size | Bound memory and disk consumption | 256 MiB |
| Per-entry decompression ratio | Detect a single highly compressible entry | 200 to 1 |
| Nesting depth | Bound path recursion and nested archives | 16 path segments |
| Path length | Bound filesystem interaction | 255 characters |

The defaults above are suggestions, not requirements.
A consumer MUST make its limits configurable and MUST report which limit was exceeded, so that a legitimately large package can be handled by raising a named limit rather than by disabling the checks.

A consumer SHOULD compute the uncompressed total from the archive's own metadata first and reject an over-large package before decompressing anything, then enforce the same limit again during decompression, because the declared metadata may lie.

### 10.3 Integrity is not authenticity

Inventory integrity is not a digital signature.

SHA-256 digests detect that content changed between the moment the inventory was written and the moment it was verified.
That is genuinely useful: it catches truncated downloads, corrupted media, accidental edits, and careless repackaging.

It does not do any of the following, and a consumer MUST NOT claim otherwise.

| Property | Provided by the inventory? |
| --- | --- |
| Detects accidental or in-transit change | Yes |
| Detects a change made after the inventory was written | Yes |
| Identifies who produced the package | No |
| Proves the package came from the claimed publisher | No |
| Prevents an attacker rewriting content and rebuilding the inventory | No |
| Establishes a chain of custody | No |

The reason is simply that an attacker who can alter the content can also recompute the digests and rewrite the inventory.
Nothing in the package binds it to a key, so nothing in it can be attributed.
The `publisher` object in the manifest is a claim, not evidence.

A future signature mechanism is therefore needed for trusted distribution, and section 15 records it as open.
Until such a mechanism exists, trust in a package MUST come from the channel it arrived on rather than from the package itself.

## 11. Adapters

An adapter moves information between the canonical artefacts of a package and the representation an external tool or platform uses.
Figma, Penpot, CSS custom properties, native platform resources, and Electron shells are all adapter targets.

An adapter has a direction.
An **export** adapter reads canonical artefacts and writes the representation a target expects.
An **import** adapter reads a target's representation and drafts the artefacts an AFDS package requires.

Both directions are in scope.
The reason is recorded in the project colophon: a format that can only export can be adopted only by a design system that began in it, and no established design system did.

The two directions do not carry the same obligations.
An export knows the full set of facts it is permitted to state, because it reads artefacts that own them.
An import does not, because the representation it reads was never obliged to carry an accessibility contract at all.

### 11.1 Direction

Each element of the manifest's `adapters` array MUST declare exactly one `direction`, either `export` or `import`.
A target supported in both directions MUST be declared as two adapters sharing a `target` value.

One direction per declaration is required because the two produce different artefacts and different reports.
A single object describing both would leave a consumer unable to determine which obligations had been discharged.

### 11.2 Requirements common to both directions

An adapter MUST report its mappings and its warnings, and MUST report whatever it could not carry.
An adapter MUST NOT silently flatten meaning.

Silent flattening is the more dangerous behaviour of the two, because the output looks complete.
A `ch`-based measure has no direct native analogue.
A forced-colours boundary has no equivalent in a target that has no concept of a user-forced colour palette.
A keyboard contract has no representation at all in a token pipeline.
In each case the honest output is a recorded finding, not an approximation presented as an equivalent.

No adapter in either direction may produce an artefact with the role `canonical`.
Section 6.2 gives the reason: an artefact shaped by a target's limits cannot own a fact.

### 11.3 Export adapters

Export output MUST carry the role `adapter` or `derived`, never `canonical`.
Export output MUST be regenerable from the canonical artefacts alone, as section 6.2 requires.
A producer MUST place export output under `adapters/<target>/out/`.

### 11.4 Import adapters

An import adapter MUST NOT write an artefact with the role `canonical`.

The output of an import is a draft.
A draft becomes canonical only when a person reviews it, supplies what the source could not, and accepts responsibility for the accessibility claims the artefact then makes.
This document calls that act **promotion**.
Promotion MUST be performed by a person and MUST NOT be performed by a transform, because a canonical artefact asserts a contract that somebody has to be willing to defend.

Import output is therefore not itself a package artefact.
A producer MUST NOT ship an unpromoted draft in a conforming package.
What the package retains from an import is the import report, which is the provenance of every artefact promoted from that import.

An import report MUST carry the role `adapter`, and is exempt from the regenerability consequence stated in section 6.2.
The exemption is narrow and its reason is structural: an import reads a source that lies outside the package by definition, so no package can regenerate it.
The alternative to the exemption is to discard the provenance of every imported artefact, which is a worse outcome than a stated exception.

Every `gaps` entry in an import report MUST appear in the promoted artefact as an uncertainty record or as a declared non-guarantee.
An import that could not supply a fact does not thereby excuse the package from declaring that the fact is unknown.

An import MUST be a discrete run that produces a dated report.
An import MUST NOT be a live read-through dependency on an external tool's model.
A read-through dependency makes the external tool the effective owner of whatever it supplies, which is the failure section 6.2 exists to prevent, and it leaves no report a reviewer can examine.

### 11.5 The adapter declaration

Each element of the manifest's `adapters` array is an adapter object.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `id` | String | REQUIRED | Adapter identifier, unique within the package. |
| `direction` | String | REQUIRED | Either `export` or `import`. |
| `target` | String | REQUIRED | The external tool or platform, for example `figma` or `css-custom-properties`. |
| `adapterVersion` | String | REQUIRED | Semantic version of the adapter that produced the output. |
| `declaration` | String | REQUIRED | Path to the adapter's own declaration file. |
| `report` | String | REQUIRED | Path to the transform report. |
| `inputs` | Array of strings | REQUIRED | For `export`, paths of the canonical artefacts consumed. For `import`, identifiers of the external sources read, which are not package paths. |
| `outputs` | Array of strings | REQUIRED | For `export`, paths of the generated artefacts. For `import`, an empty array, because import output is not a package artefact. |
| `promoted` | Array of strings | REQUIRED for `import` | Paths of the canonical artefacts promoted from this import. An empty array where nothing has yet been promoted. |

### 11.6 The transform report

A transform report records what the adapter did, what it could not do, and what it wants a reader to notice.

The following fields are REQUIRED in both directions.

| Field | Type | Meaning |
| --- | --- | --- |
| `adapterId` | String | Identifier of the adapter that produced this report. |
| `adapterVersion` | String | Version of the adapter. |
| `direction` | String | Either `export` or `import`, matching the adapter declaration. |
| `target` | String | The external tool or platform. |
| `runDate` | String | ISO 8601 date of the transform run. |
| `validationStatus` | String | One of `passed`, `passed-with-warnings`, or `failed`. |
| `mappings` | Array of mapping objects | One record per fact carried across. |
| `warnings` | Array of finding objects | Facts carried across with a caveat. Empty array if none. |

An export report additionally REQUIRES the following two arrays.

| Field | Type | Meaning |
| --- | --- | --- |
| `losses` | Array of finding objects | Facts the target could not accept. Empty array if none. |
| `unsupported` | Array of finding objects | Source features the target has no concept of. Empty array if none. |

An import report additionally REQUIRES the following two arrays.

| Field | Type | Meaning |
| --- | --- | --- |
| `gaps` | Array of finding objects | Facts that an AFDS artefact requires and the source could not supply. Empty array if none. |
| `unmapped` | Array of finding objects | Source content for which AFDS has no representation. Empty array if none. |

A **mapping object** has `source`, `sourceKind`, `targetName`, and `fidelity`, where `fidelity` is one of `exact`, `approximate`, or `partial`.
A **finding object** has `source`, `severity`, `statement`, and `consumerAction`, where `severity` is one of `info`, `warning`, or `error` and `consumerAction` says plainly what a person consuming the output must do about it.

Every array is REQUIRED even when empty.
An empty `losses` array is a positive claim that nothing was lost, which a reviewer can challenge; an omitted `losses` field is merely silence.
The same reasoning applies to `gaps`: an empty `gaps` array claims that the source supplied every fact an AFDS artefact requires, which is a strong claim and rarely a true one.

An export report containing a `losses` or `unsupported` entry with severity `error` MUST set `validationStatus` to `failed`.

An import report containing a `gaps` entry with severity `error` MUST set `validationStatus` to `failed`.
A `failed` import report is not a malfunction, and for most targets it is the expected result.
It states that the source cannot yield a conforming artefact without human authorship, which is information a person needs before deciding how much work an adoption will cost.

## 12. Conformance profiles

A profile lets a package say how complete it is, so that a consumer can reject a package that lacks what the consumer needs without inspecting the whole hierarchy.

The manifest's `conformanceProfile` field carries exactly one profile identifier.

| Profile | Identifier | Requires |
| --- | --- | --- |
| Tokens only | `afds-tokens` | Root manifest and inventory, and at least one canonical token file declared in `tokens.canonicalSources` |
| Components | `afds-components` | Everything in `afds-tokens`, plus at least one component with both a machine-readable contract and a human-readable specification |
| Full | `afds-full` | Everything in `afds-components`, plus canonical evidence records and a known-limitations artefact, and a declared test fixture for every component |

Three rules govern profiles.

A package MUST satisfy every requirement of the profile it declares.
A package MAY exceed its declared profile, so a consumer MUST treat the profile as a floor rather than a description.
A consumer that requires a higher profile than the package declares MUST refuse to treat the package as sufficient, even if inspection suggests the extra artefacts are present, because an undeclared artefact carries no commitment to remain present in the next version.

The `afds-full` profile requires evidence records but does not require that they contain results.
A record whose result is `not-yet-tested` conforms.
This is deliberate: recording an untested combination is the mechanism by which uncertainty becomes visible, and a profile that demanded results would create pressure to invent them.

## 13. Versioning

Two versions travel in every package and they move independently.

`afdsVersion` is the version of this package format.
`packageVersion` is the version of the design-system payload.
Both use semantic versioning: major for incompatible change, minor for backwards-compatible addition, patch for a correction that changes no meaning.

### 13.1 Format-version rules for producers

A change that adds an OPTIONAL field, an OPTIONAL directory, or a new profile is a minor change.
A change that adds a REQUIRED field, removes a field, changes a field's type, or changes the meaning of an existing field is a major change.
A change that corrects prose without altering a requirement is a patch change.

### 13.2 Consumer behaviour on an unexpected format version

| Situation | Required consumer behaviour |
| --- | --- |
| `afdsVersion` major matches, minor is known | Process normally. |
| `afdsVersion` major matches, minor is higher than the consumer knows | The consumer MUST process the package, MUST ignore fields it does not recognise, and SHOULD report that it read a newer minor version. |
| `afdsVersion` major matches, minor is lower than the consumer knows | The consumer MUST process the package and MUST NOT require a field introduced in a later minor version. |
| `afdsVersion` major is higher than the consumer supports | The consumer MUST refuse to process the package and MUST report the unsupported version. It MUST NOT attempt a partial read. |
| `afdsVersion` major is lower than the consumer supports | The consumer MAY refuse, or MAY process the package in a documented compatibility mode. It MUST state which it did. |
| `afdsVersion` is absent or unparseable | The consumer MUST treat the package as non-conforming. |

The asymmetry between higher and lower majors is deliberate.
A higher major may rely on semantics the consumer cannot know about, so guessing risks a silent misreading of an accessibility contract.
A lower major is fully knowable, so a compatibility mode is safe as long as it is declared.

### 13.3 Payload-version rules

`packageVersion` changes when the design system changes.
Removing a component, removing a token, renaming an identifier, or narrowing a guarantee is a major payload change.
Adding a component, adding a token, or adding evidence is a minor payload change.
Correcting prose or a typographic error is a patch payload change.

Withdrawing an assistive-technology guarantee is a major payload change even when nothing else moves, because a consumer may have relied on it.
Adding an evidence record that changes a claim from uncertainty to a guarantee is a minor change, because nothing that was relied upon has been taken away.

## 14. Relationship to Open Packaging Conventions

Open Packaging Conventions, standardised as ECMA-376 Part 2 and ISO/IEC 29500-2, is a formal ZIP-based multi-part container.

An OPC package holds *parts*, each with a name and a content type.
Content types are declared in a `[Content_Types].xml` part at the package root, either by file extension default or by explicit override.
Relationships between parts are declared in separate XML relationship parts under `_rels` directories, so that a consumer discovers the package's structure by walking relationships from a package-level root rather than by convention.
OOXML uses this machinery to collect the many related parts of one document — the document body, styles, numbering definitions, embedded images, themes, and so on — into a single logical file, and other formats reuse it: ECMA-388 states that the OpenXPS format requirements "are an extension of the packaging requirements described in the Open Packaging Conventions (OPC) Standard".

AFDS borrows the principle and rejects the machinery.

### 14.1 What AFDS takes from OPC

The useful idea is that a package is one logical object made of related parts.
A consumer receives one file, can identify it, and can enumerate its contents without hunting through a folder tree.
That is exactly the problem the `.afds` container solves, and OPC demonstrates that a ZIP archive is a sound basis for it.

### 14.2 What AFDS rejects and why

| OPC mechanism | AFDS position | Reason |
| --- | --- | --- |
| XML parts as the content model | Rejected | AFDS content is JSON and Markdown centred. Wrapping JSON in XML parts adds a representation nobody needs. |
| `[Content_Types].xml` | Rejected | The inventory already carries a media type per entry, in the same file that carries the digest. |
| `_rels` relationship parts | Rejected | The manifest already supplies the relationship map, in one place, in the format the rest of the package uses. |
| Part-naming grammar | Rejected | Normalised relative ZIP paths are sufficient and are what ordinary tools already show. |
| Relationship-walking discovery | Rejected | A consumer reads two known root files. Discovery by convention is simpler and easier to verify. |
| Single logical object made of related parts | Adopted | This is the principle worth keeping. |

The cost of the rejection is real and worth stating.
AFDS gains no benefit from existing OPC tooling, and a developer who already knows OPC must learn a second set of conventions.
The judgement is that OPC's XML parts and relationship model add complexity without improving a JSON and Markdown centred representation, and that a manifest a person can read in a text editor is worth more to this project than reuse of an XML relationship library.

## 15. Open questions

Four questions are unresolved.
They are recorded here rather than settled by assumption.

### 15.1 IANA media-type registration

AFDS has no registered media type, so `application/zip` is used and the `.afds` extension plus the root manifest identify the format.
An application for a dedicated registration such as `application/afds+zip` would give the format a stable identity in HTTP and in operating-system type databases.
The question is whether a project draft should seek registration before its field names are stable.

### 15.2 Signing

Section 10.3 states plainly that the inventory provides integrity and not authenticity.
A signature mechanism is needed before a package can be trusted on the strength of its own contents.
The open questions are which signature format to adopt, what exactly is signed, where the signature lives given that the inventory cannot record itself, and how key distribution works for a project with no registry.

### 15.3 Delta and patch distribution

A package is a whole-file artefact, so a small correction to one component ships as a complete replacement.
For a large system with frequent evidence updates this is wasteful, and it obscures what actually changed.
Whether AFDS should define a delta or patch package, and how such a package would interact with inventory verification and versioning, is unresolved.

### 15.4 Package-aware editing tooling

The colophon decision records the cost honestly: a package is less convenient for line-by-line collaboration than a live repository, and editing one artefact currently means unpacking, editing, rebuilding the inventory, and repacking.
Whether the project should build package-aware editing tooling, or continue to treat the repository as the working format and the package purely as a distribution artefact, is unresolved.

## 16. References

The following sources inform this document.

- Design Tokens Community Group, Design Tokens Format Module — https://tr.designtokens.org/format/
- IETF RFC 2119, Key words for use in RFCs to Indicate Requirement Levels — https://www.rfc-editor.org/rfc/rfc2119
- ECMA-376 Part 2, Open Packaging Conventions, fifth edition, December 2021 — https://ecma-international.org/publications-and-standards/standards/ecma-376/
- ISO/IEC 29500-2:2021, Office Open XML file formats — Part 2: Open Packaging Conventions, fourth edition, August 2021 — https://www.iso.org/standard/77818.html
- ECMA-388, Open XML Paper Specification (Open XPS), first edition, June 2009 — https://www.ecma-international.org/wp-content/uploads/ECMA-388_1st_edition_june_2009.pdf
- IANA Media Types registry — https://www.iana.org/assignments/media-types/media-types.xhtml
- FIPS 180-4, Secure Hash Standard — https://csrc.nist.gov/pubs/fips/180-4/upd1/final
- W3C WAI, Understanding SC 1.4.10 Reflow — https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- Project colophon decisions on the AFDS portable bundle and the `.afds` package — [COLOPHON.md](COLOPHON.md)
- Project research on design systems and accessibility — [DESIGN-SYSTEMS.md](../research/DESIGN-SYSTEMS.md)
