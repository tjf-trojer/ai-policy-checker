# Lexicon, German: the word lists a German register applies

_Last updated: 2026-10-06_

The same five sections as [`lexicon.md`](lexicon.md), with German words in them, and the tables
German needs beyond English: a negation that stands apart from its verb, the infinitive with «zu»,
article and paragraph numbers, and the present tense of a directive. The translator applies them as
written, `scripts/verify.py` reads them, and a German register writes its fixed words from the German
column of the schema's [Contract words](register-schema.md#contract-words). The Class and Filed in
columns hold the schema's own names (MUST, Register); the register writes them in German (MUSS).

Every term matches as whole words, in any case, longest first, as in English. Swiss and German
spelling are both listed where they differ: «regelmässig» and «regelmäßig».

## Language

| Setting | Value |
|---|---|
| Language | German |
| Marker share | 10% |
| Fewest words | 20 |

| Marker word |
|---|
| der |
| die |
| das |
| den |
| dem |
| und |
| ist |
| sind |
| von |
| mit |
| nicht |
| für |
| ein |
| eine |
| einer |
| eines |
| einem |
| einen |
| auf |
| auch |
| sich |
| werden |
| wird |
| oder |
| dass |
| bei |
| nach |
| aus |
| wie |
| im |
| zur |
| zum |
| vom |
| durch |
| sowie |
| diese |
| dieser |
| können |
| kann |
| muss |
| sie |
| zu |

Words that other languages share are left out: «in», «an», «so», «will» and «was» are English too,
«des» and «es» French or Spanish, «hat», «um» and «man» English words as well.

## Force

| Term | Class | Filed in | Forced | Negated | Source |
|---|---|---|---|---|---|
| darf nicht | MUST NOT | Register | yes | | this lexicon |
| dürfen nicht | MUST NOT | Register | yes | | this lexicon |
| verboten | MUST NOT | Register | yes | | this lexicon |
| untersagt | MUST NOT | Register | yes | | this lexicon |
| nicht zulässig | MUST NOT | Register | yes | | this lexicon |
| nicht gestattet | MUST NOT | Register | yes | | this lexicon |
| nicht erlaubt | MUST NOT | Register | yes | | this lexicon |
| ist unzulässig | MUST NOT | Register | yes | | this lexicon |
| sind unzulässig | MUST NOT | Register | yes | | this lexicon |
| muss | MUST | Register | yes | none | [RFC 2119, 1](sources/rfc2119.txt#L37), in German |
| müssen | MUST | Register | yes | none | [RFC 2119, 1](sources/rfc2119.txt#L37), in German |
| ist verpflichtet | MUST | Register | yes | | this lexicon |
| sind verpflichtet | MUST | Register | yes | | this lexicon |
| _infinitive with «zu», below_ | MUST | Register | yes | MUST NOT, forced | this lexicon |
| ist verantwortlich für | MUST | Register | no | | this lexicon |
| sind verantwortlich für | MUST | Register | no | | this lexicon |
| ist zuständig für | MUST | Register | no | | this lexicon |
| sind zuständig für | MUST | Register | no | | this lexicon |
| obliegt | MUST | Register | no | | this lexicon |
| obliegen | MUST | Register | no | | this lexicon |
| trägt die Verantwortung | MUST | Register | no | | this lexicon |
| tragen die Verantwortung | MUST | Register | no | | this lexicon |
| liegt in der Verantwortung | MUST | Register | no | | this lexicon |
| liegt in ihrer Verantwortung | MUST | Register | no | | this lexicon |
| liegt in seiner Verantwortung | MUST | Register | no | | this lexicon |
| _present tense after an actor, below_ | MUST (present) | Register | yes | MUST NOT (present), forced | this lexicon |
| _a verb opening the sentence or its main clause, followed by «Sie»_ | MUST (imperative) | Register | no | | this lexicon |
| wird nicht | WILL NOT | Register | no | | this lexicon |
| werden nicht | WILL NOT | Register | no | | this lexicon |
| wird | WILL | Register | no | WILL NOT | this lexicon |
| werden | WILL | Register | no | WILL NOT | this lexicon |
| soll nicht | SHOULD NOT | Not rules | no | | [RFC 2119, 4](sources/rfc2119.txt#L48), in German |
| sollen nicht | SHOULD NOT | Not rules | no | | [RFC 2119, 4](sources/rfc2119.txt#L48), in German |
| sollte nicht | SHOULD NOT | Not rules | no | | [RFC 2119, 4](sources/rfc2119.txt#L48), in German |
| sollten nicht | SHOULD NOT | Not rules | no | | [RFC 2119, 4](sources/rfc2119.txt#L48), in German |
| soll | SHOULD | Not rules | no | SHOULD NOT | [RFC 2119, 3](sources/rfc2119.txt#L43), in German |
| sollen | SHOULD | Not rules | no | SHOULD NOT | [RFC 2119, 3](sources/rfc2119.txt#L43), in German |
| sollte | SHOULD | Not rules | no | SHOULD NOT | [RFC 2119, 3](sources/rfc2119.txt#L43), in German |
| sollten | SHOULD | Not rules | no | SHOULD NOT | [RFC 2119, 3](sources/rfc2119.txt#L43), in German |
| empfohlen | SHOULD | Not rules | no | | this lexicon |
| empfiehlt | SHOULD | Not rules | no | | this lexicon |
| kann | MAY | Not rules | no | none | [RFC 2119, 5](sources/rfc2119.txt#L63), in German |
| können | MAY | Not rules | no | none | [RFC 2119, 5](sources/rfc2119.txt#L63), in German |
| darf | MAY | Not rules | no | MUST NOT, forced | this lexicon |
| dürfen | MAY | Not rules | no | MUST NOT, forced | this lexicon |
| zulässig | MAY | Not rules | no | MUST NOT, forced | this lexicon |
| gestattet | MAY | Not rules | no | MUST NOT, forced | this lexicon |
| erlaubt | MAY | Not rules | no | MUST NOT, forced | this lexicon |

**Strength, Forced, imperatives:** as in [`lexicon.md`](lexicon.md). «wird» and «werden» are WILL
like "will", and like "will" the translator reads them: «Die Verwendung … wird offengelegt» commits,
«Die eingegebenen Daten werden … verwendet» describes. «werden» is also the auxiliary of the passive
(«können … verwendet werden»), where it binds nothing: a sentence holding a modal is filed by the
modal. «kann» and «können» of possibility («Antworten können falsch … sein») are statements, as
"may" of possibility is.

**Left out.** «geboten» is no term. It obliges in a statute («gesetzlich geboten»), advises in the
stock phrase «Im Umgang mit … ist Vorsicht geboten», and weighs in «ob eine Kennzeichnung … geboten
erscheint»; a term holds for every policy, so the word stays out and its sentences are statements,
the reading that claims less ([rules/posture.md](../rules/posture.md)).

**Negated.** German puts «nicht» or «kein» away from its verb: «KI-Werkzeuge dürfen insbesondere
nicht verwendet werden», «Die Eingabe darf keine Personendaten enthalten», «… nicht unreflektiert
übernommen werden dürfen». A term with a Negated class takes that class when a negation word below
stands in its clause ([Clauses](#clauses), below). «darf» becomes MUST NOT and forced, «soll» SHOULD NOT; `none` means the negated
term binds nothing and is no term at all: «kann nicht delegiert werden» is a statement, and
«muss nicht» frees, it does not oblige. The Force cell quotes the modal as written with its
negated class: `«dürfen» DARF NICHT`. Where the negation follows the verb directly, the two-word
term quotes both: `«dürfen nicht» DARF NICHT`.

| Negation word | Before the verb |
|---|---|
| nicht | no |
| kein | yes |
| keine | yes |
| keinen | yes |
| keinem | yes |
| keiner | yes |
| keines | yes |
| nie | yes |
| niemals | yes |

«nicht» before the finite verb mostly negates a word, not the verb: «Öffentlich nicht zugängliche
Daten und Informationen können … eingegeben werden» permits. So «nicht» counts only after the finite
verb (the modal; for the infinitive with «zu», its carrier; for the present tense, its verb), or
anywhere when that verb closes the clause («… die Ergebnisse nicht unreflektiert übernommen werden
dürfen»). A word marked `yes` counts anywhere in the clause: «Keine Personendaten dürfen …».

### Clauses

The negation above and the infinitive with «zu» below look inside a clause: the text between the
last comma, semicolon, colon or sentence end before a word and the first after it. Two marks bound
nothing. The full stop of an abbreviation below ends no sentence: «(z. B. Funktions-Accounts) zu
nutzen» stays in the clause of its «sind». A comma with one capitalised word between it and the next
comma or joining word joins a list of nouns, not clauses: «… sind die … Vorgaben bezüglich
Vertraulichkeit, Informationssicherheit und Datenschutz zu beachten.» is one clause. Every other
comma bounds one: in «Ziel der Meldung ist es, mögliche Auswirkungen … zu begrenzen» two words
follow it, and the infinitive stands in a clause of its own with no carrier; in «… ist abzusehen,
insbesondere, wenn …» the word is not capitalised. Spaces inside an abbreviation are optional:
«z. B.» is also «z.B.».

| Abbreviation |
|---|
| z. B. |
| d. h. |
| u. a. |
| v. a. |
| s. g. |
| bzw. |
| etc. |
| usw. |
| vgl. |
| ggf. |
| evtl. |
| inkl. |
| ca. |
| s. |
| gem. |
| Art. |
| Abs. |
| Nr. |
| Bst. |
| Ziff. |
| lit. |

### Infinitive with «zu»

«sein» or «haben» with an infinitive with «zu» obliges: «Generierte Texte … sind kritisch … zu
prüfen.», «Auf den Einsatz … ist in folgenden Fällen zu verzichten:». A clause ([Clauses](#clauses)) holding
a carrier below and an infinitive with «zu» has the term of class MUST, forced; with a negation word
in the clause, MUST NOT. The term is the infinitive with its «zu» as written: «zu prüfen», or one word
where a separable verb takes «zu» inside, «anzupassen», «abzusehen». It counts where it closes the
clause, stands right before the carrier that closes it («… zu prüfen ist»), stands before a joining
word («zu prüfen und zu bereinigen»), or opens the clause («Zu berücksichtigen sind insbesondere:»).
An infinitive with «zu» in a clause with no carrier is an ordinary word: «Um die Richtigkeit … sicherzustellen,».

| Carrier |
|---|
| ist |
| sind |
| hat |
| haben |

| Infinitive ending |
|---|
| -en |
| -ern |
| -eln |

### Present tense

A German directive often states a duty with no modal at all: «Die Angestellten prüfen die
Ergebnisse der KI-Werkzeuge auf deren Richtigkeit und Vollständigkeit.» The rule that decides when
such a sentence binds, and why, is in [`rules/force.md`](../rules/force.md), the present tense. Its
words are here. The policy is a directive when its Source Title quotation holds a directive word.
A sentence then binds by its tense when it holds no force term but «wird» or «werden», and it opens
with a determiner, at most two lower-case words, an actor (a whole word, an entry below or of the
Collective list; a compound is no actor, or «Die Weiterleitung» would be one), and a lower-case word
that is none of the words below it may not be: that word is the verb, and the Force cell quotes it, `«prüfen» MUSS (Präsens)`, or
`DARF NICHT (Präsens)` with a negation word in its clause.

| Directive word |
|---|
| richtlinie |
| richtlinien |
| weisung |
| weisungen |
| regelung |
| reglement |
| verordnung |
| erlass |
| verfügung |
| hausverfügung |
| dienstanweisung |
| anordnung |
| vorschrift |
| vorschriften |
| dienstvereinbarung |

«Leitlinien», «Merkblatt», «Empfehlungen» and «Leitfaden» are left out on purpose: they advise, and
their present tense describes.

| Determiner |
|---|
| der |
| die |
| das |
| jede |
| jeder |
| jedes |
| alle |
| sämtliche |

| Actor |
|---|
| stelle |
| amt |
| abteilung |
| departement |
| direktion |
| dezernat |
| leitung |
| informatik |
| datenschutzbeauftragte |
| datenschutzbeauftragter |

| Not a present-tense verb |
|---|
| ist |
| sind |
| war |
| waren |
| wird |
| werden |
| wurde |
| wurden |
| hat |
| haben |
| hatte |
| hatten |
| sei |
| seien |

### Imperatives and openings

An imperative in German official texts is the formal one: «Geben Sie keine Personendaten ein.» Its
Force cell quotes the verb with its «Sie», `«Geben Sie» DARF NICHT (Imperativ)` with a negation word
in its clause, `MUSS (Imperativ)` without. A verb opening a sentence with no «Sie» after it is no
imperative this lexicon knows: German opens conditions that way («Werden generative KI-Werkzeuge
genutzt, ist …», «Stellen Mitarbeitende fest, dass …»).

| Imperative follower |
|---|
| Sie |

A sentence also opens after an article or paragraph number and after a dash or bullet that marks a
list item. `<n>` is a number of up to three digits, with a letter after it or not.

| Opening marker |
|---|
| Art. <n> |
| § <n> |
| <n> |
| – |
| ▪ |

| Joining word |
|---|
| und |
| oder |
| sowie |
| aber |
| dann |
| bzw. |

**Known gaps**, filed as statements until this lexicon changes: an instruction in the infinitive
(«Keine Personendaten eingeben.»), the familiar imperative («Gib keine Personendaten ein.»), an
adjective of duty in «-pflichtig» («ist … kennzeichnungspflichtig»), a present-tense duty whose
verb comes before its actor («Bei Fragen wenden sich die Angestellten an …»), and a responsibility
sentence that puts its object first («Die Verantwortung für generierte Inhalte tragen weiterhin …
die Nutzerinnen und Nutzer»), which «tragen die Verantwortung» does not match. Its responsibility
word still lets it give another rule its owner ([rules/fields.md](../rules/fields.md)).

## Collective owners

As in English: lower-case the Owner quotation and cut it before the first cut word below that is not
its first word; the flag is set when what remains equals a crowd entry or ends with one. With
compounds on, a last word that ends in a crowd entry counts too: «Verwaltungsmitarbeitende»,
«Dienststellen». «Die zuständigen Stellen» and «Die Angestellten» are crowds; «Die Informatik» and
«das Amt für Informatik» («das amt») are not.

| Setting | Value |
|---|---|
| Compounds | yes |

| Cut word |
|---|
| von |
| vom |
| für |
| in |
| im |
| an |
| am |
| auf |
| mit |
| zu |
| zur |
| zum |
| bei |
| aus |
| nach |
| der |
| des |
| dem |
| den |
| die |
| das |
| welche |
| welcher |
| welches |
| deren |
| dessen |

German puts a participle before its noun («die KI nutzenden Mitarbeitenden»), so no ending cuts
after a crowd word.

| Participle ending |
|---|

| Collective |
|---|
| wir |
| uns |
| man |
| alle |
| jede |
| jeder |
| mensch |
| menschen |
| angestellte |
| angestellten |
| mitarbeitende |
| mitarbeitenden |
| mitarbeiter |
| mitarbeiterin |
| mitarbeiterinnen |
| beschäftigte |
| beschäftigten |
| nutzende |
| nutzenden |
| nutzer |
| nutzerin |
| nutzerinnen |
| benutzende |
| benutzenden |
| personal |
| vorgesetzte |
| vorgesetzten |
| führungskräfte |
| stellen |
| behörden |
| ämter |
| verwaltung |
| organisation |
| gemeinden |

## Timing words

A When quotation is flagged `(unspecified)`, in German `(unbestimmt)`, unless it holds one of these,
outside an unspecified phrase:

| Kind | Words |
|---|---|
| Digit | a number written in digits, not joined to letters: «30», «2025» |
| Number | eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn, elf, zwölf, zwanzig, dreissig, dreißig, vierzig, fünfzig, sechzig, neunzig, hundert |
| Frequency | jährlich, halbjährlich, vierteljährlich, quartalsweise, monatlich, wöchentlich, täglich, jede, jeden, jedes, jeder, einmal |
| Trigger | vor, nach, bevor, nachdem, innerhalb, binnen, bis, sobald, spätestens |

«nach Bedarf» holds the trigger «nach» and fixes nothing, so these phrases are taken out before the
words above are looked for. «regelmässig», «laufend» and «fortlaufend» hold none of them and carry
the flag.

| Unspecified phrase |
|---|
| nach Bedarf |
| bei Bedarf |
| nach Möglichkeit |
| nach Ermessen |

## Policy edges

| Seam marker |
|---|
| von: |
| gesendet: |
| an: |
| cc: |
| betreff: |
| ursprüngliche nachricht |
| weitergeleitete nachricht |
| schrieb: |
| allen antworten |
| eingabe: |
| prompt: |
| antwort: |

The last three open a sample of what goes into an AI tool or comes out of it, which a policy may
show and does not state («Beispiel einer Texteingabe:», «Antwort:»).

| Responsibility word |
|---|
| verantwortlich |
| verantwortliche |
| verantwortlichen |
| verantwortung |
| zuständig |
| zuständige |
| zuständigen |
| zuständigkeit |
| obliegt |
| obliegen |
| rechenschaft |
