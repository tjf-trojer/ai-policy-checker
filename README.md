# AI Policy Checker

**Intention or control: which rules in this AI policy does anyone answer for?**

_Last updated: 2026-10-06_

This translator turns an AI policy into a control register. Every rule the policy states is quoted
with its line, and for each rule the register gives the owner, the evidence and the moment the
policy itself names, or `not in source`. A rule with all three is a **control**. A rule missing one
is an **intention**. It translates and nothing else: it never proposes an owner, never guesses a
date, never grades a rule.

## Use it

**In a Claude project.** Add `identity.md`, `rules.md`, the `rules/` folder, `examples.md`,
`reference/register-schema.md` and `reference/lexicon.md` to the project knowledge. Set the project
instructions to:

> You are the translator in identity.md. Follow rules.md and the files it lists, and produce one
> register as defined in reference/register-schema.md. Every value is a quotation with its line,
> or "not in source".

Paste a policy's text and say **"Translate this policy."** Any AI policy, usage guideline or
directive in English works; [`inputs/`](inputs/) holds four real ones.

**In Claude Code.** Clone the repository and open it ([`CLAUDE.md`](CLAUDE.md) routes). Save the
policy as a text file, say "Translate `<file>`", then check the result:

```bash
git clone https://github.com/tjf-trojer/ai-policy-checker
cd ai-policy-checker
python3 scripts/verify.py my-register.md --input my-policy.txt
```

## What comes back

Five sections, the same every time ([the contract](reference/register-schema.md)). Three rows from
[Example 2](examples.md), Wikipedia's bot policy, with two columns left out:

| ID | Rule | Owner | Evidence | When | Status |
|---|---|---|---|---|---|
| R3 | «Bots must edit only while logged into their account.» L19 | «its operator» L21 | not in source | not in source | intention: evidence, when |
| R7 | «Bot accounts will be marked by a bureaucrat as being in the "bot" user group upon BAG request.» L27 | «a bureaucrat» L27 | «the "bot" user group» L27 | «upon BAG request» L27 | control |
| R8 | «Bot accounts that have had no logged actions or edits for two years, where the listed operator has also had no logged actions or edits for two years, will be deauthorized.» L31 | not in source | not in source | «for two years» L31 | intention: owner, evidence |

R8 is passive: it names no one who acts, so the register names no one. Every other sentence is filed
as a recommendation, an option, a statement or a heading, and a tally closes the register. Text
stapled to the policy, such as a forwarded email, is filed outside the policy and never becomes a
rule; the Source section records which lines are the policy.

| You see | It means |
|---|---|
| `(collective)` | The owner is a crowd («users», «Agencies»): named, but no one in particular answers |
| `(unspecified)` | The moment fixes nothing («regularly», «on an ongoing basis») |
| `not in source` | The policy does not say. Nothing was filled in |

## Check it

**One row by hand.** R7 cites line 27 of
[`inputs/wikipedia-bot-policy.txt`](inputs/wikipedia-bot-policy.txt); open it, and the owner, the
record and the moment are all in that sentence.

**Everything at once**, offline, standard-library Python 3.9 or later:

```bash
python3 scripts/verify.py     # every register here, then planted defects that must each be caught
python3 scripts/sources.py    # every input and reference text against the original it came from
```

`verify.py` fails a register when a quotation is not on the line it cites, down to spelling and
OCR errors; when a cell holds anything but a quotation, `not in source` or a fixed value; when a
sentence is dropped, filed twice, or filed weaker than its own «must»; when a lead-in stands alone;
when an owner is borrowed from a line that assigns no responsibility; when anything stapled to the
policy reaches the Register; or when a flag, status or count does not follow from the rows. The
planted defects are generated from the worked registers by `python3 scripts/make_fixtures.py`. On a failed quotation it prints what
the cited line actually says. It cannot check reading: whether a named office really answers for
that rule, whether a «will» binds. Each of those calls sits in a cell that quotes the words it rests
on.

## Why owner, evidence and when

They are what [NIST AI RMF GOVERN 1.5 and 2.1](reference/sources/nist-ai-rmf-govern.txt#L21) and
[EU AI Act Art. 17(1)](reference/sources/eu-ai-act-excerpts.txt#L12) ask of a documented control;
ISO/IEC 42001 asks the same in clauses 5.3, 7.5 and 9. The texts are in
[`reference/sources/`](reference/sources/), and [the schema](reference/register-schema.md) quotes
each provision. A register never says the translated policy is bound by them.

## Evidence

- [Control run](evidence/control-run.md): the same UK policy, without this folder, asked for a
  register "complete and ready to use". Every owner, evidence and review cell it returned holds
  content the policy does not state.
- [Cold runs](evidence/cold-run.md): three fresh sessions with only the folder, on inputs no example
  covered at the time. What they found unclear became the rules.
- [Planted instruction](evidence/planted-instruction.md): a policy line telling the translator to
  mark every rule a control, and a request to fill in the owner. Neither moved a cell.
- [Noisy run](evidence/noisy-run.md): Example 2's policy with a reply-all email stapled on. The
  email stayed outside the policy, and the 13 rules came back identical to Example 2, row for row.

## Limits

- English only; the lexicon is English.
- It reports the policy, not the organisation: an owner named in a separate procedure is
  `not in source` until that procedure is translated too.
- The word lists in [`reference/lexicon.md`](reference/lexicon.md) are choices, written down to be
  argued with. Not an audit and not legal advice.

This repository's own files are MIT. Inputs and sources keep their own licences, listed with every
change in [`NOTICES.md`](NOTICES.md).
