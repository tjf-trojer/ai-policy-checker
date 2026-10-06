# Notices: third-party text and its licences

_Last updated: 2026-10-06_

This repository's own files are MIT ([`LICENSE`](LICENSE)). The texts below are other people's,
under their own terms. None of their authors endorses this repository.

## Inputs

| File | Source | Licence |
|---|---|---|
| `inputs/uk-civil-service-generative-ai-guidance.txt` | "Guidance to civil servants on use of generative AI", Cabinet Office, Government Digital Service and Central Digital and Data Office, GOV.UK, first published 29 June 2023, updated 29 January 2024, since superseded by the Generative AI Framework for HMG. <https://www.gov.uk/government/publications/guidance-to-civil-servants-on-use-of-generative-ai/guidance-to-civil-servants-on-use-of-generative-ai>, retrieved 24 September 2026 through the GOV.UK Content API | Open Government Licence v3.0. Contains public sector information licensed under the Open Government Licence v3.0 |
| `inputs/wikipedia-bot-policy.txt` | "Wikipedia:Bot policy", English Wikipedia, revision 1371001773 of 24 August 2026, by Wikipedia contributors. <https://en.wikipedia.org/w/index.php?oldid=1371001773>, retrieved 24 September 2026 through the MediaWiki parse API | CC BY-SA 4.0 |
| `inputs/omb-m-25-21-section-3.txt` | Office of Management and Budget, Memorandum M-25-21, "Accelerating Federal Use of AI through Innovation, Governance, and Public Trust", 3 April 2025. <https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf>, retrieved 24 September 2026 | Public domain, a work of the United States Government (17 U.S.C. 105) |
| `inputs/uk-generative-ai-framework-governance.txt` | "Generative AI Framework for HMG", Cabinet Office, Government Digital Service and Central Digital and Data Office, GOV.UK, 18 January 2024, section "Governance". <https://www.gov.uk/government/publications/generative-ai-framework-for-hmg/generative-ai-framework-for-hmg-html>, retrieved 25 September 2026 through the GOV.UK Content API | Open Government Licence v3.0. Contains public sector information licensed under the Open Government Licence v3.0 |
| `tests/planted/acme-ai-use-policy.txt` | Written for this repository. The organisation and its policy are invented | MIT, like the repository's own files |
| `tests/language/ki-richtlinie.txt`, `tests/language/politique-ia.txt`, `tests/language/ai-note-with-german-quote.txt` | Written for this repository, in German, French and English. The organisations and their policies are invented | MIT, like the repository's own files |
| `tests/noisy/wikipedia-bot-policy-stapled-email.txt` | `inputs/wikipedia-bot-policy.txt` with an email appended; the email, its sender and its recipients are invented for this repository | CC BY-SA 4.0 for the Wikipedia text, like its source |

Changes, the same kind for all four: markup converted to plain text, one paragraph or list item
per line with a blank line between; a heading's level shown by leading `#` marks; omitted passages
marked `[...]` on a line of their own. Wording, spelling and errors are unchanged.

- **UK Framework.** The title, then the section "Governance" to the end of the document.
- **UK guidance.** The title line and the superseded notice, then the text from "This guidance
  outlines" to the end of "Practicalities of using generative AI in your role". Omitted: the
  introduction before that, the section on the government's approach and the annex of examples.
- **Wikipedia.** The page title, then the sections "Bot usage" to "Bot requirements", up to the
  subsection "Performance". Omitted: the shortcut boxes and every other section.
- **OMB M-25-21.** The PDF is a scan: page images from a RICOH IM C6010 with an OCR text layer
  added by Adobe Acrobat's Paper Capture. The input is that text layer as extracted, its OCR errors
  kept («OFFlCEOFMANAGEMENTANDBUDGET», «0MB», «CAI Os», «govemmentwide», «11.» for ii.). The page
  images print "OFFICE OF MANAGEMENT AND BUDGET" and "OMB"; where the two differ, the input follows
  the text layer, because that is the text a translator receives. The letterhead,
  date, number, addressee and subject lines of page 1; then section 3 to the end of 3(b)(v), then
  footnotes 20 to 23 from the foot of those pages. Omitted: the FROM block, a signature
  image, and everything between the subject line and section 3. Page numbers and running heads are
  removed, wrapped lines joined, and the line-end hyphen in "high-impact" joined.

Example 2 in [`examples.md`](examples.md) quotes the Wikipedia text throughout and is licensed
CC BY-SA 4.0, like the text it quotes. Each file in `tests/fixtures/` is a copy of one worked
example with one defect planted by `scripts/make_fixtures.py`, and carries that example's source and
licence; so does `evidence/noisy-run-register.md`. The three fixtures generated from
`tests/language/` are MIT, like their inputs.

## Originals, and how to check them

Every input and reference text above was taken from an original that ships beside it:
`inputs/originals/` and `reference/sources/originals/`. The two PDFs also ship with the text layer
PyMuPDF 1.26.5 extracted from them. `python3 scripts/sources.py` checks the SHA-256 of every
original, rebuilds each input from its original byte for byte, and matches each reference excerpt
word for word, in order, against its original; `--pdf` re-extracts the text layers and `--fetch`
downloads the originals again. The AI Act original is a text extraction of the official PDF, made
on 25 June 2026 with pdfminer.six for the author's own working corpus, which is not public; EUR-Lex
refuses scripted downloads, so that one hash cannot be compared live.

## Reference sources

| File | Source | Licence |
|---|---|---|
| `reference/sources/nist-ai-rmf-govern.txt` | NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0), January 2023, section 5.1 and Table 1. <https://doi.org/10.6028/NIST.AI.100-1> | Public domain, a work of the United States Government |
| `reference/sources/eu-ai-act-excerpts.txt` | Regulation (EU) 2024/1689 (Artificial Intelligence Act), OJ L, 12.7.2024, Articles 4, 9(1) to 9(2), 17(1), 26(1) to 26(2). <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>. © European Union | Reuse under Commission Decision 2011/833/EU, source acknowledged |
| `reference/sources/rfc2119.txt` | S. Bradner, RFC 2119, "Key words for use in RFCs to Indicate Requirement Levels", March 1997. <https://www.rfc-editor.org/rfc/rfc2119.txt> | "Distribution of this memo is unlimited." Unmodified |

Changes to the first two: text extracted from the official PDF, lines unwrapped, end-of-line
hyphens removed, paragraph numbers restored to their paragraphs, page furniture removed. In the NIST
file Table 1's two columns are written as one line per category and subcategory. In the AI Act file
the points of Article 9(2) are omitted and marked `[...]`. Each file opens with a one-line header
and a rule; the wording below the rule is unchanged.

ISO/IEC 42001 is named in [`reference/register-schema.md`](reference/register-schema.md) by clause
number only. Its text is copyrighted and is not in this repository.
