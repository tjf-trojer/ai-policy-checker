# The register: the output contract

_Last updated: 2026-10-06_

Every translation is one register with five sections, in this order, whatever the policy looks
like. `scripts/verify.py` fails a register that breaks anything on this page. An input in a
language no lexicon covers is not translated: it gets the one-line refusal in
[`rules/posture.md`](../rules/posture.md) instead. The words below are English; a register in
another language writes the same contract in that language's words, [Contract words](#contract-words).

| # | Heading | Holds |
|---|---|---|
| 1 | `## Source` | What the policy says about itself |
| 2 | `## Register` | One row per rule: force, addressee, owner, evidence, timing, status |
| 3 | `## Not rules` | Every other sentence of the input, filed |
| 4 | `## Referred elsewhere` | Documents the policy names and the register did not receive |
| 5 | `## Tally` | Counts derived from sections 2 and 3 |

Every sentence of the input sits in section 2 or in section 3, never in both. Title lines, headings
and the omission mark `[...]` sit in section 3, even when section 1 quotes them too. A sentence
outside the Policy text sits in section 3, filed `outside the policy`, whatever its words say.

## Quotations

- A quotation is the input's text between `«` and `»`, a space, and the line it sits on:
  `«Bots must edit only while logged into their account.» L19`. A span over lines is `L12-L14`.
  Line numbers count every line of the input from 1, blank lines included. A span starts on the
  line where the quotation starts and ends on the line where it ends.
- The text is the input's, character for character: its spelling, capitals, typing and OCR errors.
  Two differences are tolerated. A run of whitespace, including a line break inside a span, counts
  as one space. Typographic quotes and apostrophes match their straight forms.
- Several quotations in one cell are joined by ` + `. A `|` inside a quotation is written `\|`.
- A field the input does not fill is `not in source`, in lower case, and nothing else.

Everything else in a register is envelope, derived by a rule on this page or in
[`lexicon.md`](lexicon.md): IDs, force classes, the two flags, statuses, filings, counts, the
Policy text spans and the input's path. The envelope never states a fact about the policy that a quotation does not carry.

## 1. Source

```
| Field | Entry |
|---|---|
| Title | quotation, or not in source |
| Issued by | quotation, or not in source |
| Date or version | quotation(s) of a date, version or document number, or not in source |
| Policy text | the lines that are the policy, as spans: L1-L57, or L1-L40 + L52-L60, or none |
| Input | the input's path from the repository root in backticks, or the word pasted |
```

**Policy text** marks where the policy ends and anything stapled to it begins: a forwarded or
replied-to email, a signature, a note to a colleague. Every quotation in the register cites lines
inside it, except the quotations of entries filed `outside the policy`, which cite lines outside it.
A block outside it in the middle of the input opens on a line holding a seam marker from the
lexicon. With nothing stapled on, the Policy text is the whole input.

## 2. Register

```
| ID | Rule | Force | Addressee | Owner | Evidence | When | Status |
```

| Column | Entry | What it holds |
|---|---|---|
| ID | `R1`, `R2`, and on | Rows run in the order of the line where each rule's own text ends: a list item's line, not its lead-in's |
| Rule | quotation(s) | A sentence whose strongest force term files it in the Register ([`lexicon.md`](lexicon.md)). A list item is quoted with its lead-in: `«CAI Os, in coordination with appropriate agency officials, must:» L26 + «J. support agency efforts to track AI spending.» L56` |
| Force | `«term» CLASS` | The strongest force term in the rule as written, and its class from the lexicon. For an imperative outside the lexicon, its opening verb phrase |
| Addressee | quotation(s), or `not in source` | Whom the rule binds, as the rule's own quotations name them. An imperative names no one |
| Owner | quotation(s) with `(collective)` where the lexicon says so, or `not in source` | The role, person or body the text makes answerable for the rule being met: named as responsible or accountable for it, as the one who approves, maintains, reviews, enforces or ensures it, or as a named office the rule is addressed to. It is the only attribute that may come from another sentence: a lead-in above the rule, or a sentence that assigns responsibility for the same conduct and holds a responsibility word from the lexicon; the quotation then carries that sentence's line. A collective addressee is not an owner by being addressed, and a name in a condition («Should the operator return») is not the agent of a passive rule |
| Evidence | quotation(s), or `not in source` | An artefact or record the rule's own quotations name that would show the rule was met: a register, inventory, list, log, plan, report, notice, approval, request, flag, page, publication |
| When | quotation(s) with `(unspecified)` where the lexicon says so, or `not in source` | A frequency, date, deadline or triggering event the rule's own quotations fix for meeting or reviewing it. A condition of application ("when using the tool") is not a When |
| Status | `control`, or `intention: ` and the missing attributes | `control` when Owner is filled and not collective, Evidence is filled, and When is filled and not unspecified. Otherwise `intention: ` followed by what is missing, in the order `owner, evidence, when` |

### What the three attributes answer

The status tests three attributes because published governance texts ask for the same three.

| Attribute | Provision | Its words |
|---|---|---|
| Owner | [NIST AI RMF, GOVERN 2.1](sources/nist-ai-rmf-govern.txt#L25) | «Roles and responsibilities and lines of communication related to mapping, measuring, and managing AI risks are documented and are clear to individuals and teams throughout the organization.» |
| Owner | [AI Act, Art. 17(1)(m)](sources/eu-ai-act-excerpts.txt#L25) | «an accountability framework setting out the responsibilities of the management and other staff» |
| Owner | [AI Act, Art. 26(2)](sources/eu-ai-act-excerpts.txt#L29) | «Deployers shall assign human oversight to natural persons» |
| Evidence | [AI Act, Art. 17(1)](sources/eu-ai-act-excerpts.txt#L12) | «documented in a systematic and orderly manner in the form of written policies, procedures and instructions» |
| Evidence | [AI Act, Art. 17(1)(k)](sources/eu-ai-act-excerpts.txt#L23) | «systems and procedures for record-keeping of all relevant documentation and information» |
| Evidence | [NIST AI RMF, section 5.1](sources/nist-ai-rmf-govern.txt#L12) | «Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.» |
| When | [NIST AI RMF, GOVERN 1.5](sources/nist-ai-rmf-govern.txt#L21) | «including determining the frequency of periodic review» |
| When | [AI Act, Art. 17(1)(d)](sources/eu-ai-act-excerpts.txt#L16) | «the frequency with which they have to be carried out» |
| When | [AI Act, Art. 9(2)](sources/eu-ai-act-excerpts.txt#L9) | «requiring regular systematic review and updating» |

ISO/IEC 42001, the certifiable standard for an AI management system, asks for the same three in
clause 5.3 (roles, responsibilities and authorities), clause 7.5 (documented information) and
clause 9 (performance evaluation). Its text is copyrighted and is not in this folder; the clause
numbers are pointers.

The provisions define the attributes. They do not say the policy under translation is bound by
them, and a register never says so either.

## 3. Not rules

```
| Text | Filed as |
```

| Filed as | When |
|---|---|
| `recommendation «term»` | The sentence recommends: its strongest binding force term has class SHOULD or SHOULD NOT |
| `optional «term»` | The sentence permits: its strongest binding force term has class MAY |
| `statement` | The sentence holds no force term, or holds one that does not bind here: a descriptive "will", a conditional "Should the operator return", a "may" of possibility |
| `heading` | A heading, a title line, or the omission mark `[...]` |
| `outside the policy` | The sentence lies outside the Policy text |

A sentence inside the Policy text that holds a forced term ([`lexicon.md`](lexicon.md)) is never
filed here, unless it ends in a question mark.

## 4. Referred elsewhere

```
| Reference |
```

One row per document the policy names by title or number, quoted as written. With none, the
section holds the single line `No references in source.`

## 5. Tally

```
| Count | Value |
|---|---|
| Rules | n |
| Controls | n |
| Intentions | n |
| Owner named, not collective | n |
| Evidence named | n |
| When named, not unspecified | n |
| Not rules | n |
| Outside the policy | n |
```

The rows, their names and their order are fixed. Every value is a count of rows in sections 2 and 3;
Outside the policy counts the Not-rules rows filed that way.

## Contract words

A register is written in the language of its policy: its fixed words are those of that language's
column below, and its quotations stay in the policy's own words. This page states every rule with
the English words; each rule holds unchanged for the words beside them. Each lexicon names its
column in its section Language, and `scripts/verify.py` reads this table.

| English | German |
|---|---|
| Source | Quelle |
| Register | Register |
| Not rules | Keine Regeln |
| Referred elsewhere | Verweise |
| Tally | Zählung |
| Field | Feld |
| Entry | Eintrag |
| Title | Titel |
| Issued by | Herausgegeben von |
| Date or version | Datum oder Version |
| Policy text | Richtlinientext |
| Input | Eingabe |
| none | keiner |
| pasted | eingefügt |
| ID | ID |
| Rule | Regel |
| Force | Verbindlichkeit |
| Addressee | Adressat |
| Owner | Verantwortlich |
| Evidence | Nachweis |
| When | Zeitpunkt |
| Status | Status |
| not in source | nicht in der Quelle |
| control | Kontrolle |
| intention | Absicht |
| owner | Verantwortlich |
| evidence | Nachweis |
| when | Zeitpunkt |
| (collective) | (kollektiv) |
| (unspecified) | (unbestimmt) |
| MUST NOT | DARF NICHT |
| MUST | MUSS |
| WILL NOT | WIRD NICHT |
| WILL | WIRD |
| SHOULD NOT | SOLL NICHT |
| SHOULD | SOLL |
| MAY | KANN |
| (imperative) | (Imperativ) |
| (present) | (Präsens) |
| Text | Text |
| Filed as | Abgelegt als |
| recommendation | Empfehlung |
| optional | Option |
| statement | Feststellung |
| heading | Überschrift |
| outside the policy | ausserhalb der Richtlinie |
| Reference | Verweis |
| No references in source. | Keine Verweise in der Quelle. |
| Count | Posten |
| Value | Wert |
| Rules | Regeln |
| Controls | Kontrollen |
| Intentions | Absichten |
| Owner named, not collective | Verantwortlich benannt, nicht kollektiv |
| Evidence named | Nachweis benannt |
| When named, not unspecified | Zeitpunkt benannt, nicht unbestimmt |
| Outside the policy | Ausserhalb der Richtlinie |
| No register: the input `<path>` is not in <languages>. | Kein Register: Die Eingabe `<path>` ist nicht auf <languages>. |
| or | oder |
| English | Englisch |
| German | Deutsch |

German fixed words keep the Swiss «ss»: «ausserhalb», never «außerhalb». The force class
`(present)` is the present-tense rule of [`rules/force.md`](../rules/force.md); the English lexicon
declares none, so an English register never holds it.
