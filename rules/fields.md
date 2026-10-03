# Fields: the Source, the row, and what the policy points to

_Last updated: 2026-10-03_

Steps 2, 5 and 6. Every field is a quotation from the input or `not in source`. The columns are
defined in [`reference/register-schema.md`](../reference/register-schema.md).

## 2. Source

Quote the title, the issuer and the date, version or document number where the input prints them.
One you know but the input does not print is `not in source`. Example 3's issuer is three
quotations: «EXECUTIVE OFFICE OF THE PRESIDENT» L1 + «OFFlCEOFMANAGEMENTANDBUDGET» L2 + «T HE
DIRECTOR» L4. Policy text records the policy's lines as spans ([sentences.md](sentences.md), the
policy's edges): `L1-L57` for a policy with nothing stapled on.

## 5. Fill the row

| Column | How |
|---|---|
| Force | The strongest term as written, and its class ([force.md](force.md)) |
| Addressee | The party the rule binds, as the rule's own quotations name it. A passive rule with no agent and an imperative name no one: `not in source` |
| Owner | The party the text makes answerable (the schema defines it). Look in the rule and its lead-in first. Then in a lead-in above the rule: a lead-in that names a party makes it answerable for everything its item requires, the item's later sentences included. Then in a sentence that assigns responsibility for the same conduct with a responsibility word from the lexicon; cite its line. An addressee is the owner when it is a named office, not when it is a crowd, and a party named only in a condition is no owner of a passive rule. Flag `(collective)` by the lexicon |
| Evidence | A record or artefact named in the rule's own quotations, lead-in included. Never from another sentence |
| When | The frequency, date, deadline or triggering event in the rule's own quotations, lead-in included, kept as written. A condition of application is not a When. Flag `(unspecified)` by the lexicon |
| Status | By the schema's rule, from the three cells as written |

| Column | Case | In the examples |
|---|---|---|
| Addressee | A passive rule names no one | Example 2, R8 «…will be deauthorized.» |
| Addressee, Owner | A party named only in a condition is not the agent of a passive rule | Example 2, R10: «Should the operator return…» names the operator; «…must be completed» names no one, so both cells are `not in source` |
| Addressee | An imperative names no one | Example 1, R1 «Never put…» |
| Owner | From another sentence that assigns responsibility for the same conduct | Example 2, R3: «its operator» L21, from «The contributions of a bot account remain the responsibility of its operator» |
| Owner | A named office the rule addresses | Example 3, R5 «the head of each agency» |
| Owner | A crowd made responsible is named and flagged | Example 1, «users» L23 (collective) on every row |
| Owner | A lead-in's party owns its item's later sentences | Example 3, R36, R40, R43: «Agency heads» L68 |
| Evidence | A thing the rule names; a verb is not a record | Example 3, R10: «notify 0MB» names no notice, so `not in source` |
| Evidence | Never from another sentence | Example 1, R2: the footnote named at L55 is not R2's evidence |
| When | A trigger counts | Example 2, R7 «upon BAG request»; Example 3, R19 «before risk acceptance» |
| When | A condition of application does not | Example 1, R5 «When using generative AI»; Example 2, R10 «Should the operator return…» |
| When | Relative timing stays relative | Example 3, R5 «Within 60 days of the issuance of this memorandum» |
| When | A moment nobody could check is flagged | Example 3, R9 «regularly» (unspecified) |

## 6. Referred elsewhere

Quote every document the policy names by title or number, once, at its first mention, parts of the
same document the input does not hold included (Example 3, «Section 4 of this memorandum» L38).
