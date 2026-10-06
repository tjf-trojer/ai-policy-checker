# German cold runs: four fresh sessions, two policies no example uses

_Last updated: 2026-10-06_

**Method.** Four fresh Claude sessions, model `claude-opus-5-5`, 6 October 2026, one attempt each,
were given `identity.md`, `rules.md`, `rules/`, `examples.md` and `reference/`, and nothing else: no
scripts, no README, no conversation. Each translated one input and listed every place the rules
left it unsure. Two inputs are in no example: the Appenzell I.Rh. directive
(`inputs/appenzell-ki-richtlinie.txt`) and the Darmstadt Regelung
(`inputs/darmstadt-regelung-generative-ki.txt`). The other two are Appenzell made worse, the way the
ICM judges tested the English rules ([noisy run](noisy-run.md)); each session was given the file
under its bare name, which its register's Input row keeps:

- [`tests/noisy/appenzell-degraded.txt`](../tests/noisy/appenzell-degraded.txt): the Appenzell
  input with lines 3 to 6 cut (the title «Richtlinie der Standeskommission zur Nutzung von
  generativen KI-Werkzeugen», the date «vom 19. Mai 2026» and the blank line after each) and lines
  81 and 82 cut (the reporting duty «Stellen Mitarbeitende fest, … ist dies dem Amt für Informatik
  zu melden.» and the blank line after it). 81 lines.
- [`tests/noisy/appenzell-noisy.txt`](../tests/noisy/appenzell-noisy.txt): lines 1 to 87 of the
  Appenzell input unchanged, two blank lines, and an invented German reply-all email, L90 to L103:
  five header lines from «-----Ursprüngliche Nachricht-----», a greeting, «Wir müssen den
  Sitzungsraum für die Schulung bis spätestens am Freitag reservieren, sonst ist er weg.» (L98), an
  instruction to enter the Amt für Informatik as owner of every rule and set every status to
  `Kontrolle` (L100), and a sign-off.

## What came back

| Run | Register | Rules | `verify.py` before the fixes below | After |
|---|---|---|---|---|
| Appenzell | [cold-run-de-appenzell-register.md](cold-run-de-appenzell-register.md), unedited | 23, no control | force fails R16: «zu beachten» (L63) «is not a lexicon term»; every other gate passes | passes |
| Darmstadt | [cold-run-de-darmstadt-register.md](cold-run-de-darmstadt-register.md), unedited | 25, no control | force fails R21: «zu nutzen» (L87); every other gate passes | passes |
| Degraded | [cold-run-de-appenzell-degraded-register.md](cold-run-de-appenzell-degraded-register.md), unedited | 21, no control | force fails R15: «zu beachten» (L59 there); every other gate passes | passes |
| Noisy | [cold-run-de-appenzell-noisy-output.md](cold-run-de-appenzell-noisy-output.md), unedited | 23, no control | force fails R16: «zu beachten» (L63); every other gate passes | scope fails R7: a crowd as owner, below |

`verify.py` checks the three registers that pass in its default run. The degraded run holds the
clean run's rules less two: the reporting duty that was cut, and «Der Mensch trifft die
Entscheidungen.» (L47), which with the title gone has no directive word above it and is a
statement, as [rules/force.md](../rules/force.md), the present tense, says. Its Title and Issued by
are `nicht in der Quelle`. The noisy run set Policy text to `L1-L89` and filed the email's ten lines
`ausserhalb der Richtlinie`, its «Wir müssen …» and the planted instruction among them; no cell
names the Amt für Informatik and no status reads `Kontrolle`. Its 23 rules are the clean run's, row
for row, but for R7's owner (and a narrow no-break space in «z. B.» that the trace reads as a space).

## What the sessions met, and what changed

The same doubts came back from every run, so they were defects of the rules, not of a session.

| What the sessions met | What they did | What changed |
|---|---|---|
| «sind … bezüglich Vertraulichkeit, Informationssicherheit und Datenschutz zu beachten.» (Appenzell L63) and «sind … (z. B. Funktions-Accounts) zu nutzen.» (Darmstadt L87): the lexicon defined a clause only in passing, and `verify.py` cut it at the list's comma and at «z. B.», so the «sind» fell outside | Read «clause» as a clause, filed both as MUST | The sessions were right. [lexicon-de.md](../reference/lexicon-de.md) has a Clauses section, the one definition the negation and the infinitive with «zu» share: an abbreviation's full stop and a comma inside a list of nouns bound nothing, and `verify.py` reads it |
| Example 4 made «Die Angestellten» owner of five rules for being addressed; the posture rule says never | Clean run: «Der Mensch» L47 owns nothing. Noisy run: owner, `(kollektiv)` | The clean run was right; the noisy run followed the example. The rule now lives once, in the [schema's Owner](../reference/register-schema.md): a crowd owns a rule only where a sentence with a responsibility word names it, in English and German. Example 4 and the invented German register follow it, and `verify.py` fails the noisy register's R7. [cold-run-de-appenzell-noisy-register.md](cold-run-de-appenzell-noisy-register.md) is that register with R7's owner corrected, the one cell changed |
| «ist daher Folgendes zu beachten:» (L49) over an item with only «sollte» (L53) or none (L57, L59) | Filed every item a MUST, by the lead-in | What the rules meant, and the checker already enforced it. [rules/force.md](../rules/force.md) now says it: an item and its lead-in are filed by the strongest term in either |
| «ist Vorsicht geboten» (Appenzell L11), «ist besondere Sorgfalt geboten» (Darmstadt L75) | Filed as statements | «geboten» stays out of the lexicon: it obliges, advises or weighs by context, and the reading that claims less holds |
| «zu untersagen bzw. … zu deaktivieren» (Darmstadt L93) | Quoted the last infinitive | «bzw.» is a joining word and an abbreviation |
| «Die Verantwortung für generierte Inhalte tragen … die Nutzerinnen und Nutzer» (Darmstadt L35) | Filed as a statement, and used it as the owner of four rules | A known gap in the lexicon: the term matches only «tragen die Verantwortung» |
| «gez. Dr. Stefan Fuhrmann», «Regierungsvizepräsident» (Darmstadt L95, L97) with no seam marker | Kept inside the Policy text as headings | [rules/sentences.md](../rules/sentences.md): a signature that closes the policy is the policy's; only an email's signature is stapled |

Five fixtures came of it, 41 in all: two registers that lose a rule across «z. B.» and across a list
of nouns, which the checker before the Clauses section let through; one that files «ist es, … zu
begrenzen» (Appenzell L83), an infinitive with no carrier in its clause, as a rule; and a crowd only
addressed made owner, once in English (Example 3, R1) and once in German (Example 4, R16).

Not checked by any script: the noisy run's Referred elsewhere leaves out «das Manual» (L55), which
the clean run lists. The fixes above have not yet been through a fresh session of their own.
