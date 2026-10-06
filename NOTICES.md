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
| `inputs/zuerich-ki-richtlinie.txt` | "Richtlinie über die Nutzung von generativer künstlicher Intelligenz (KI-Richtlinie)", Stadtrat von Zürich, Stadtratsbeschluss Nr. 2281 of 20 August 2025, Beilage 1. <https://www.stadt-zuerich.ch/content/dam/web/de/politik-verwaltung/politik-recht/stadtratsbeschluesse/2025/08/stzh-strb-2025-2281-beilage-1.pdf>, retrieved 6 October 2026 | No copyright: an official enactment, Swiss Copyright Act (URG) Art. 5 para. 1 lit. a. Confidence high: a directive the city executive adopted by formal decision and published with it |
| `inputs/appenzell-ki-richtlinie.txt` | "Richtlinie der Standeskommission zur Nutzung von generativen KI-Werkzeugen", Standeskommission des Kantons Appenzell I.Rh., 19 May 2026, document AI 013.12-476.4.1.2-1450793. Linked as "Richtlinie zur Nutzung von generativen KI-Werkzeugen" from <https://www.ai.ch/themen/staat-und-recht/digitale-verwaltung/ki-werkzeuge>; the download address, whose path names a different document, is <https://www.ai.ch/themen/staat-und-recht/digitale-verwaltung/ki-werkzeuge/dokument/verzeichnis-algorithmischer-systeme-appenzell-i-rh/download>, retrieved 6 October 2026 | No copyright: an official enactment, URG Art. 5 para. 1 lit. a. Confidence high: a directive of the cantonal government, published by it |
| `inputs/darmstadt-regelung-generative-ki.txt`, `inputs/darmstadt-hausverfuegung.txt` | "Regelung zum Umgang mit im Internet verfügbaren Systemen der generativen Künstlichen Intelligenz im Regierungspräsidium Darmstadt" (R 4), 8 October 2025, and the Hausverfügung of the same date that puts it in force, Regierungspräsidium Darmstadt. <https://rp-darmstadt.hessen.de/sites/rp-darmstadt.hessen.de/files/2026-03/regelung_zum_umgang_mit_generativer_ki_r_4.pdf> and <https://rp-darmstadt.hessen.de/sites/rp-darmstadt.hessen.de/files/2026-03/hv_regelungzum_umgang_mit_generativer_ki_8.pdf>, retrieved 6 October 2026 | No copyright: an official decree (amtlicher Erlass), German Copyright Act (UrhG) § 5 para. 1. Confidence medium-high: an internal administrative rule that its authority published itself |
| `inputs/st-gallen-leitlinien-chatgpt.txt` | "Leitlinien über die Verwendung von ChatGPT und ähnlichen Systemen in der Verwaltung", adopted by the board of the Vereinigung St.Galler Gemeindepräsidentinnen und Gemeindepräsidenten on 31 August 2023 and by the Regierung des Kantons St.Gallen on 5 September 2023. <https://www.sg.ch/content/dam/sgch/sicherheit/datenschutz/SK_Leitlinien_ueber_die_Verwendung_von_ChatGPT_und_aehnlichen_Systemen_in_der_Verwaltung.pdf>, retrieved 6 October 2026 | No copyright: an official enactment, URG Art. 5 para. 1 lit. a. Confidence medium-high: guidelines adopted by the cantonal government, whose binding force on the administration is weaker than a directive's |
| `tests/planted/acme-ai-use-policy.txt` | Written for this repository. The organisation and its policy are invented | MIT, like the repository's own files |
| `tests/language/ki-richtlinie.txt`, `tests/language/politique-ia.txt`, `tests/language/ai-note-with-german-quote.txt` | Written for this repository, in German, French and English. The organisations and their policies are invented | MIT, like the repository's own files |
| `tests/noisy/appenzell-degraded.txt`, `tests/noisy/appenzell-noisy.txt` | `inputs/appenzell-ki-richtlinie.txt` with lines cut out, and with an email appended; the email, its sender and its recipients are invented for this repository | No copyright for the Appenzell text, as above; MIT for the email |
| `tests/noisy/wikipedia-bot-policy-stapled-email.txt` | `inputs/wikipedia-bot-policy.txt` with an email appended; the email, its sender and its recipients are invented for this repository | CC BY-SA 4.0 for the Wikipedia text, like its source |

The licence basis of the German inputs is the exemption of official texts from copyright, not a
licence. That a Swiss internal directive counts among the "andere amtliche Erlasse" of URG Art. 5
para. 1 lit. a is the prevailing view in the literature, not settled case law; the same holds for an
internal administrative rule under UrhG § 5 para. 1. The confidence given for each is the author's
reading, not legal advice. Each text is reproduced unchanged in wording, with its source.

Changes to the English inputs, the same kind for all four: markup converted to plain text, one paragraph or list item
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

- **The German inputs.** The PDFs are born digital (Microsoft Word); none is a scan. Their text was
  extracted with PyMuPDF 1.26.5 as blocks with positions, and the blocks ship beside each PDF as
  `.blocks.txt`. The input takes the blocks of each page top to bottom, one paragraph, list item or
  heading per line with a blank line between, wrapped lines joined. A hyphen at a line end before
  a lower-case letter divides a word and goes with the break («ge-» + «nerativen» gives
  «generativen»); before a capital it belongs to the word and stays («KI-» + «Werkzeuge»). Page
  numbers, running heads and footers are removed; footnotes move to the end in order, as in OMB
  M-25-21. A bare section number or list marker on its own line is joined to its text.
- **Zürich.** The margin titles beside the articles («Gegenstand»,
  «Registrierung», «a. Zulässige Daten») stand on a line of their own before the article they sit
  beside, because the text layer puts them at the foot of each page.
- **Appenzell.** The document number, printed in the footer of every page, once at the top. The
  bullet «▪» stays with its item.
- **Darmstadt.** The text layer reads «Kl», K and lower-case L, where the page shows what reads as
  «KI», 29 times in R 4; in a sans-serif face the two look alike, and the input keeps «Kl» as the
  text layer has it, as the OMB input keeps «0MB». The Hausverfügung's addressee, set on three
  lines, is one line.
- **St. Gallen.** Section numbers joined to their headings. The boxed sample of a prompt and its
  answer stands where the page prints it, between sections 3.1.2 and 3.2; the text layer puts it at
  the end.

Example 2 in [`examples.md`](examples.md) quotes the Wikipedia text throughout and is licensed
CC BY-SA 4.0, like the text it quotes. Each file in `tests/fixtures/` is a copy of one worked
example with one defect planted by `scripts/make_fixtures.py`, and carries that example's source and
licence; so does `evidence/noisy-run-register.md`. The three fixtures generated from
`tests/language/` are MIT, like their inputs. Examples 4 and 5 and the fixtures generated from them
quote the Zürich and St. Gallen texts, and the German cold-run registers in `evidence/` the Appenzell
and Darmstadt texts, which are free of copyright as stated above.

## Originals, and how to check them

Every input and reference text above was taken from an original that ships beside it:
`inputs/originals/` and `reference/sources/originals/`. Every PDF also ships with the text layer
PyMuPDF 1.26.5 extracted from it. `python3 scripts/sources.py` checks the SHA-256 of every
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
