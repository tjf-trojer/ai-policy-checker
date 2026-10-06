# Lexicon: the word lists a register applies

_Last updated: 2026-10-06_

Five sections of lists for one language. The translator applies them as written and
`scripts/verify.py` reads them from this file, or from the one its `--lexicon` names. A list that is
wrong for one policy is wrong for all of them, and it changes here. A lexicon for another language
is a file beside this one with the same sections and tables and its own words in them, such as
[`lexicon-de.md`](lexicon-de.md); the register it fills has the same contract, written in that
language's [contract words](register-schema.md#contract-words).

A term matches as whole words, in any case. The longest term wins: `must not` before `must`,
`should never` before `should`, `is not permitted` before `permitted`.

## Language

The language these lists are for. An input in another language gets no register, only the refusal
in [`rules/posture.md`](../rules/posture.md): no term below would match it, and a register of it
would report no rules where the policy may hold many. `scripts/verify.py` tells the language by the
marker words below, common words of the language that carry no force: the input is in it when they
make up at least the marker share of its words. A short quotation in another language inside a
policy leaves the share where it was. An input of fewer words than the fewest is not judged.

| Setting | Value |
|---|---|
| Language | English |
| Marker share | 10% |
| Fewest words | 20 |

| Marker word |
|---|
| the |
| of |
| and |
| to |
| is |
| are |
| be |
| been |
| that |
| this |
| these |
| those |
| with |
| for |
| by |
| from |
| not |
| it |
| its |
| which |
| who |
| they |
| their |
| have |
| has |
| should |
| must |
| would |
| can |
| at |
| if |
| there |
| what |
| when |
| than |
| into |
| any |
| such |
| other |
| our |
| your |
| you |
| we |

Words that other languages share are left out: «in», «an», «will» and «so» are German too, «a»,
«on», «or» and «as» French.

## Force

| Term | Class | Filed in | Forced | Source |
|---|---|---|---|---|
| must not | MUST NOT | Register | yes | [RFC 2119, 2](sources/rfc2119.txt#L40) |
| shall not | MUST NOT | Register | yes | [RFC 2119, 2](sources/rfc2119.txt#L40) |
| is prohibited | MUST NOT | Register | yes | this lexicon |
| are prohibited | MUST NOT | Register | yes | this lexicon |
| is not permitted | MUST NOT | Register | yes | this lexicon |
| are not permitted | MUST NOT | Register | yes | this lexicon |
| must | MUST | Register | yes | [RFC 2119, 1](sources/rfc2119.txt#L37) |
| shall | MUST | Register | yes | [RFC 2119, 1](sources/rfc2119.txt#L37) |
| is required to | MUST | Register | yes | [RFC 2119, 1](sources/rfc2119.txt#L37) |
| are required to | MUST | Register | yes | [RFC 2119, 1](sources/rfc2119.txt#L37) |
| is responsible for | MUST | Register | no | this lexicon |
| are responsible for | MUST | Register | no | this lexicon |
| need to | MUST | Register | no | this lexicon |
| needs to | MUST | Register | no | this lexicon |
| never | MUST NOT (imperative) | Register | opening | this lexicon |
| do not | MUST NOT (imperative) | Register | opening | this lexicon |
| don't | MUST NOT (imperative) | Register | opening | this lexicon |
| always | MUST (imperative) | Register | opening | this lexicon |
| _a verb opening the sentence or its main clause_ | MUST (imperative) | Register | no | this lexicon |
| will not | WILL NOT | Register | no | this lexicon; RFC 2119 does not define it |
| will | WILL | Register | no | this lexicon; RFC 2119 does not define it |
| should never | SHOULD NOT | Not rules | no | [RFC 2119, 4](sources/rfc2119.txt#L48) |
| should not | SHOULD NOT | Not rules | no | [RFC 2119, 4](sources/rfc2119.txt#L48) |
| should | SHOULD | Not rules | no | [RFC 2119, 3](sources/rfc2119.txt#L43) |
| recommended | SHOULD | Not rules | no | [RFC 2119, 3](sources/rfc2119.txt#L43) |
| encouraged | SHOULD | Not rules | no | this lexicon |
| encourage | SHOULD | Not rules | no | this lexicon |
| may | MAY | Not rules | no | [RFC 2119, 5](sources/rfc2119.txt#L63) |
| optional | MAY | Not rules | no | [RFC 2119, 5](sources/rfc2119.txt#L63) |
| permitted | MAY | Not rules | no | this lexicon |
| permissible | MAY | Not rules | no | this lexicon |

**Strength**, strongest first: MUST NOT and MUST, with their imperative forms; WILL NOT and WILL;
SHOULD NOT and SHOULD; MAY. A sentence's force is its strongest term, and the strongest term
decides where it is filed.

**Forced.** Inside the Policy text only. `yes`: a sentence holding the term is a rule, wherever the
term stands. `opening`: a
sentence the term opens, after any list marker, is a rule. Where the term opens a main clause
(«…social media sites, do not input…») it is a force term the translator reads. Anywhere else it is
an ordinary word: «so long as they do not conflict» holds no force term. `no`: the translator reads
the sentence. A descriptive "will" ("These tools will answer your question") and a conditional
"should" ("Should the operator return") are statements. A question is never forced.

**Imperatives.** An instruction whose sentence or main clause opens with a bare verb is a rule of
class MUST (imperative); `never`, `do not` and `don't` make it MUST NOT (imperative). The Force cell
quotes the lexicon term where there is one («Never», «Always», «do not»), and otherwise the opening
verb or verb phrase («be aware», «consider»). An imperative stands at an opening: the start of a
sentence, after a list marker, or after a comma, semicolon or colon, with at most one joining word
from the table below between. «Agencies are encouraged to update» holds no imperative. A list item
whose opening verb finishes a lead-in that carries a force term of its own («…should be kept up to
date with the following details:» + «Describe…») takes the lead-in's force. A verb that
only points the reader somewhere ("Note that", "See") or asks a favour ("please contact") is not
an instruction, and its sentence is a statement.

| Joining word |
|---|
| and |
| but |
| or |
| then |

## Collective owners

An Owner quotation is flagged `(collective)` when its head is a crowd. Lowercase the quotation and
cut it before the first cut word below, and before a word with a participle ending below (`-ing`)
that directly follows a crowd word. The flag is set when what remains equals a crowd entry or ends with one. «users» and
«All users directing a bot» are crowds; «the head of each agency» («the head») and «Agency heads»
are not.

| Cut word |
|---|
| of |
| for |
| in |
| on |
| at |
| to |
| with |
| who |
| whom |
| whose |
| that |
| which |

| Participle ending |
|---|
| -ing |

| Collective |
|---|
| we |
| us |
| you |
| everyone |
| everybody |
| anyone |
| staff |
| employees |
| users |
| colleagues |
| personnel |
| workforce |
| civil servants |
| contributors |
| editors |
| members |
| agency |
| agencies |
| organisation |
| organization |
| organisations |
| organizations |
| company |
| community |
| government |
| leaders |
| officials |

A collective owner names who is meant and no one in particular who answers. The register keeps the
quotation and flags it.

## Timing words

A When quotation is flagged `(unspecified)` unless it holds at least one of these:

| Kind | Words |
|---|---|
| Digit | a number written in digits, not joined to letters: «30», «2036»; not the «0» of «0MB» |
| Number | one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, twenty, thirty, forty, fifty, sixty, ninety, hundred |
| Frequency | annually, annual, yearly, monthly, weekly, daily, quarterly, every |
| Trigger | before, after, upon, prior, following, within, until, whenever |

"Regularly", "periodically", "on an ongoing basis" and "as needed" fix no moment anyone could
check, so they carry the flag.

## Policy edges

Text stapled to a policy is not the policy: a forwarded or replied-to email with its signature, a
note to a colleague. The register's Policy text row says which lines are the policy. A block of lines
outside it that sits in the middle of the input, not at its start or end, must open on a line
holding a seam marker.

| Seam marker |
|---|
| from: |
| sent: |
| to: |
| cc: |
| subject: |
| original message |
| forwarded message |
| wrote: |
| reply all |
| prompt: |
| answer: |

The last two open a sample of what goes into an AI tool or comes out of it, which a policy may show
and does not state.

An Owner quoted from a line other than the rule's own and not from a lead-in above it must come from
a line holding one of these words:

| Responsibility word |
|---|
| responsible |
| responsibility |
| accountable |
| accountability |
| answerable |
| in charge |

