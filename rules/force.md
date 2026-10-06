# Force: filing each entry

_Last updated: 2026-10-06_

Step 4. An entry outside the Policy text is filed `outside the policy` and nothing else, whatever
its words. Every other entry is filed by its strongest force term: the terms, their classes and
where each counts are in [`reference/lexicon.md`](../reference/lexicon.md), and the filings it
leads to are defined in [`reference/register-schema.md`](../reference/register-schema.md), section
3. MUST, WILL, an imperative and a German directive's present tense (below) go to the Register;
SHOULD and MAY go to Not rules.

| Case | Decided by | In the examples |
|---|---|---|
| One rule at two forces | Each sentence is filed by its own words; the register does not reconcile them | Example 1: R1 «Never put…» L11 is a rule; «You should never put…» L43 is a recommendation |
| A conditional "should" | The schema, `statement` | Example 2, R10 «Should the operator return…» is filed by its «must» |
| A "will" that commits | [posture.md](posture.md), calls the words cannot settle | Example 1, R3 «This guidance will be subject to a review…»; Example 3, R38 «0MB will provide templates…» |
| A "will" that describes | The schema, `statement` | Example 1, «A generative AI tool, such as a LLM, will answer your question…» L51 |
| A "may" of possibility | The schema, `statement`; a "may" that permits is `optional` | Example 2: «…stronger methods of verification may be required.» L39 is a statement; «Bot operators may wish to redirect…» L23 is optional |
| An imperative opening a main clause | The lexicon, Imperatives | Example 1, R6 «…, do not input…»; R8 «Therefore, be aware…» |
| An item that completes its lead-in | The lexicon, Imperatives | `inputs/uk-generative-ai-framework-governance.txt` L39 + L41: «The inventory should be regularly kept up to date with the following details:» + «Describe each system’s purpose…» is a recommendation ([cold run 3](../evidence/cold-run.md)) |
| "do not" inside a clause | The lexicon, Forced | Example 3, footnote 23 «…so long as they do not conflict…», a recommendation by its «encouraged» |
| A verb that points or asks | The lexicon, Imperatives | Example 2, «Note that high-speed…» L15; Example 1, «…please contact…» L7 |
| A responsibility sentence | The lexicon, «is responsible for» | Example 2, R5; Example 1, R4 |
| A normative phrase the lexicon lacks | The lexicon decides; «it is important to» is a statement until the lexicon changes | Example 1, «References: … it is important to make clear…» L55 |
| A question | The lexicon, Forced | Example 1, «Does that information need to be entered in that system?» L35 |
| A stapled email's «must» | [sentences.md](sentences.md), the policy's edges | [noisy run](../evidence/noisy-run.md): «We must…» in the email is filed `outside the policy` |
| A negation away from its modal | The lexicon, Negated | Example 4, R8 to R15: «KI-Werkzeuge dürfen insbesondere nicht verwendet werden für:» is `«dürfen» DARF NICHT` |
| A «nicht» on a word, not on the modal | The lexicon, Negation word | Example 4: «Öffentlich nicht zugängliche Daten und Informationen können …» L53 permits, `Option «können»` |
| An infinitive with «zu» | The lexicon, Infinitive with «zu» | Example 5, R4 «… sind kritisch auf Qualität und Korrektheit zu prüfen.» |
| A German duty in the present tense | Below, the present tense | Example 4, R1 to R3, R16, R21, R22 |

## The present tense

A Swiss or German directive states most duties with no modal at all: «Die Angestellten prüfen die
Ergebnisse der KI-Werkzeuge auf deren Richtigkeit und Vollständigkeit.» (Example 4, R16). Read by
its modals alone, the Zürich directive of Example 4 holds 16 rules; it states 22. The force of such a
sentence comes from the genre, not from a word, so the register takes it only where the genre and
the form are both on the page, and says so in the row:

1. The policy is a directive: its Source Title quotation holds a directive word of the lexicon
   («Richtlinie», «Weisung», «Regelung»). Guidelines and leaflets («Leitlinien», «Merkblatt») are
   not, and their present tense describes.
2. The sentence holds no force term, or only «wird» or «werden».
3. It opens with a determiner, an actor of the lexicon and the verb right after it: «Die
   Angestellten prüfen», «Die zuständigen Stellen setzen».

Such a sentence is a rule of class MUST (present), MUST NOT (present) with a negation word on its
verb, and the Force cell quotes the verb: `«prüfen» MUSS (Präsens)`. It is forced: it is never filed
under Not rules. Every other sentence in the present tense is a statement. A lexicon that lists no
actors declares no present tense: the English one does not, so an English register never holds the
class.

Why a class and not a reading: the class shows in every row that the force is the genre's, not the
policy's words, so a reader who weighs a directive's present tense differently sees which rows to
weigh; `scripts/verify.py` recomputes each condition; and outside the three conditions the reading
claims less, as everywhere else. What the form cannot tell, the row keeps visible:

| Case | Filed | In the examples |
|---|---|---|
| An actor and its verb open the sentence | Rule, MUST (present) | Example 4, R1 «Die zuständigen Stellen setzen …», R16 |
| A consequence stated as a duty is | Rule, MUST (present): the form is a duty's, and the class shows where its force comes from | Example 4, R21 and R22 «Die Angestellten tragen allfällige … Folgen für:» |
| A passive in the present tense | Filed by its «wird», a WILL the translator reads (a "will" that commits) | Example 4, R17 «… wird offengelegt, sofern …» |
| No actor opens the sentence | Statement | Example 4, «Art. 1 Diese Richtlinie regelt …» L9 |
| The present tense of guidelines | Statement: no directive word in the title | Example 5, «ChatGPT und ähnliche Systeme eignen sich lediglich für einfache, standardmässige Anfragen.» L69 |
| A modal in the sentence | Filed by the modal | Example 4, «Art. 8 1 KI-Werkzeuge können verwendet werden, …» L63 |
