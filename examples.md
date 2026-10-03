# Worked registers

_Last updated: 2026-10-03_

Real policies, translated. Each register cites its input in [`inputs/`](inputs/) by line, and
`python3 scripts/verify.py` checks every register on this page against its input in its default
run. Sources and licences are in [`NOTICES.md`](NOTICES.md).

# Example 1: UK guidance to civil servants on generative AI (2023, since superseded)

Guidance written almost entirely as advice. The summary's «Never put sensitive information or
personal data into these tools.» (L11) is a rule; the body's «You should never put sensitive
information or personal data into these tools.» (L43) is a recommendation. The register files each
where its own words put it and says nothing about the difference. Every owner it finds is the
collective «users», from L23, and the register keeps the flag.

## Source

| Field | Entry |
|---|---|
| Title | «Guidance to civil servants on use of generative AI» L1 |
| Issued by | not in source |
| Date or version | not in source |
| Policy text | L1-L57 |
| Input | `inputs/uk-civil-service-generative-ai-guidance.txt` |

## Register

| ID | Rule | Force | Addressee | Owner | Evidence | When | Status |
|---|---|---|---|---|---|---|---|
| R1 | «Never put sensitive information or personal data into these tools.» L11 | «Never» MUST NOT (imperative) | not in source | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |
| R2 | «Output from generative AI is susceptible to bias and misinformation, they need to be checked and cited appropriately.» L17 | «need to» MUST | not in source | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |
| R3 | «This guidance will be subject to a review after six months, to address emerging practices and better understanding of the use cases for this technology.» L19 | «will» WILL | not in source | not in source | not in source | «after six months» L19 | intention: owner, evidence |
| R4 | «As with all digital systems, users are responsible for their own actions when using such tools and are reminded of their obligations under GDPR.» L23 | «are responsible for» MUST | «users» L23 | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |
| R5 | «When using generative AI, consider the three Hows:» L45 + «How your question will be used by the system.» L47 | «consider» MUST (imperative) | not in source | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |
| R6 | «Just as you would not share work documents on social media sites, do not input such material into generative AI tools.» L47 | «do not» MUST NOT (imperative) | not in source | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |
| R7 | «When using generative AI, consider the three Hows:» L45 + «How answers from generative AI can mislead.» L49 | «consider» MUST (imperative) | not in source | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |
| R8 | «Therefore, be aware of the potential for misinformation from these systems.» L49 | «be aware» MUST (imperative) | not in source | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |
| R9 | «Always apply the high standards of rigour you would to anything you produce, and reference where you have sourced output from one of these tools.» L49 | «Always» MUST (imperative) | not in source | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |
| R10 | «When using generative AI, consider the three Hows:» L45 + «How generative AI operates.» L51 | «consider» MUST (imperative) | not in source | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |
| R11 | «Always treat with caution the outputs these tools produce and challenge the outputs using your own judgement and knowledge.» L51 | «Always» MUST (imperative) | not in source | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |
| R12 | «Accounts: When using generative AI for one of the appropriate uses described in this guidance, you can use your gov.uk email address, but be aware of what you are entering (based on the content of this guidance).» L57 | «be aware» MUST (imperative) | not in source | «users» L23 (collective) | not in source | not in source | intention: owner, evidence, when |

## Not rules

| Text | Filed as |
|---|---|
| «Guidance to civil servants on use of generative AI» L1 | heading |
| «This page has been superseded by the Generative AI Framework for HMG» L3 | statement |
| «[...]» L5 | heading |
| «This guidance outlines the expectation for how civil servants should approach the use of Large Language Models.» L7 | statement |
| «New tools are emerging all the time.» L7 | statement |
| «If civil servants see something that they think has potential to improve our work in government then please contact cddo@digital.cabinet-office.gov.uk.» L7 | statement |
| «Summary of guidance:» L9 | heading |
| «With appropriate care and consideration generative AI can be helpful and assist with your work.» L13 | statement |
| «However, you should be cautious and circumspect in your approach, noting the guidance provided here.» L13 | recommendation «should» |
| «You should never input information that is classified, sensitive or reveals the intent of government (that may not be in the public domain) into any of these tools.» L15 | recommendation «should never» |
| «You should have regard to the principles of GDPR.» L15 | recommendation «should» |
| «This guidance covers general principles for civil servants, how these apply to use of LLMs, the practicalities of using LLMs, and the government’s wider approach to generative AI.» L21 | statement |
| «Examples of how to use and how not to use generative AI in your role are included below.» L25 | statement |
| «General principles for Civil Service working» L27 | heading |
| «Civil servants should be inquisitive about new technologies, including generative AI tools.» L29 | recommendation «should» |
| «However, we should always exercise caution when using and sharing sensitive information or information which contains personal data.» L29 | recommendation «should» |
| «This includes being cautious about the sort of information that is entered into LLMs like ChatGPT.» L29 | statement |
| «The following general guidance always applies to the systems we use:» L31 + «You should always be aware of what information you have access to, what rights and restrictions apply to that information (from either private or government sources) and the conditions under which that information can or should be shared.» L33 | recommendation «should» |
| «The following general guidance always applies to the systems we use:» L31 + «You should always be mindful of any systems into which you enter information.» L35 | recommendation «should» |
| «Does that information need to be entered in that system?» L35 | statement |
| «What will be done with the information once it has left your possession?» L35 | statement |
| «What rights are being given away in placing the information elsewhere?» L35 | statement |
| «How this applies to generative AI» L37 | heading |
| «Generative AI tools are evolving at pace.» L39 | statement |
| «We have experience of already using predecessors of this technology in both the government and NHS.» L39 | statement |
| «However, new products such as the latest version of ChatGPT and Google’s Bard product are a leap forward in publicly available generative AI tools.» L39 | statement |
| «We encourage you to explore this technology and consider the implications for your organisations and the services you provide.» L41 | recommendation «encourage» |
| «However, there are some ground rules you should keep in mind.» L41 | recommendation «should» |
| «You should never put sensitive information or personal data into these tools.» L43 | recommendation «should never» |
| «Beyond existing data protection laws, government has no oversight over how data, which is entered into web-based generative AI tools, is then used.» L43 | statement |
| «Therefore, you should not put information into generative AI tools that, if compromised or lost, could have damaging consequences for individuals, groups of individuals, an organisation or for government more generally.» L43 | recommendation «should not» |
| «These systems learn based on the information you enter.» L47 | statement |
| «These tools can produce credible looking output.» L49 | statement |
| «They can also offer different responses to the same question if it is posed more than once, and they may derive their answers from sources you would not trust in other contexts.» L49 | statement |
| «A generative AI tool, such as a LLM, will answer your question by probabilistically choosing words from a series of options it classifies as plausible.» L51 | statement |
| «These tools can not understand context or bias.» L51 | statement |
| «Practicalities of using generative AI in your role» L53 | heading |
| «References: Whether using the outputs from generative AI either verbatim or with minor alterations, it is important to make clear to those reading that one of these tools has been used.» L55 | statement |
| «To do this the tools should be cited in a footnote, with its URL and any sources used as inputs.» L55 | recommendation «should» |

## Referred elsewhere

| Reference |
|---|
| «Generative AI Framework for HMG» L3 |
| «GDPR» L15 |

## Tally

| Count | Value |
|---|---|
| Rules | 12 |
| Controls | 0 |
| Intentions | 12 |
| Owner named, not collective | 0 |
| Evidence named | 0 |
| When named, not unspecified | 1 |
| Not rules | 39 |
| Outside the policy | 0 |

---

# Example 2: Wikipedia bot policy (English Wikipedia, revision 1371001773)

A community's rules for automated agents. «Should the operator return» (L31) is a condition, so
its sentence is filed by its «must». The passive rules at L31 («will be deauthorized», «will be
removed») name no one who acts, and the register does not supply the bureaucrat a reader would expect.
The one control is R7: an office, a record and a trigger, all in one sentence.

## Source

| Field | Entry |
|---|---|
| Title | «Wikipedia:Bot policy» L1 |
| Issued by | not in source |
| Date or version | not in source |
| Policy text | L1-L65 |
| Input | `inputs/wikipedia-bot-policy.txt` |

## Register

| ID | Rule | Force | Addressee | Owner | Evidence | When | Status |
|---|---|---|---|---|---|---|---|
| R1 | «The operation of unapproved bots, or use of approved bots in ways outside their approved conditions of operation, is prohibited and may in some cases lead to blocking of the user account and possible sanctions for the operator.» L15 | «is prohibited» MUST NOT | not in source | «the operator» L15 | «their approved conditions of operation» L15 | not in source | intention: when |
| R2 | «If in doubt, check.» L15 | «check» MUST (imperative) | not in source | not in source | not in source | not in source | intention: owner, evidence, when |
| R3 | «Bots must edit only while logged into their account.» L19 | «must» MUST | «Bots» L19 | «its operator» L21 | not in source | not in source | intention: evidence, when |
| R4 | «The contributions of a bot account remain the responsibility of its operator, whose registered account (i.e., not a temporary account) must be prominently identifiable on its user page.» L21 | «must» MUST | «its operator» L21 | «its operator» L21 | «its user page» L21 | not in source | intention: when |
| R5 | «In particular, the bot operator is responsible for the repair of any damage caused by a bot which operates incorrectly.» L21 | «is responsible for» MUST | «the bot operator» L21 | «the bot operator» L21 | not in source | not in source | intention: evidence, when |
| R6 | «To ensure compliance with WP:BOTCOMM, unregistered users wishing to operate a bot must first register an account before operating a bot.» L21 | «must» MUST | «unregistered users wishing to operate a bot» L21 | not in source | «an account» L21 | «before operating a bot» L21 | intention: owner |
| R7 | «Bot accounts will be marked by a bureaucrat as being in the "bot" user group upon BAG request.» L27 | «will» WILL | «a bureaucrat» L27 | «a bureaucrat» L27 | «the "bot" user group» L27 | «upon BAG request» L27 | control |
| R8 | «Bot accounts that have had no logged actions or edits for two years, where the listed operator has also had no logged actions or edits for two years, will be deauthorized.» L31 | «will» WILL | not in source | not in source | not in source | «for two years» L31 | intention: owner, evidence |
| R9 | «Following a one-week notification period on the bots noticeboard, and the operator's talk page, prior task approvals will be considered expired and bot flags will be removed.» L31 | «will» WILL | not in source | not in source | «a one-week notification period on the bots noticeboard, and the operator's talk page» L31 | «Following a one-week notification period» L31 | intention: owner |
| R10 | «Should the operator return and wish to reactivate the bot, a new request for approval (BRFA) must be completed.» L31 | «must» MUST | not in source | not in source | «a new request for approval (BRFA)» L31 | not in source | intention: owner, when |
| R11 | «However, it can be permissible to instead make these edits via a bot account (particularly if necessary due to the actions being privileged), provided the following conditions are met:» L35 + «Disclosure: The identity of the Wikipedia user directing the edit/action must be publicly disclosed, typically by linking the username in the edit summary.» L37 | «must» MUST | not in source | not in source | «the edit summary» L37 | not in source | intention: owner, when |
| R12 | «However, it can be permissible to instead make these edits via a bot account (particularly if necessary due to the actions being privileged), provided the following conditions are met:» L35 + «Verification: The identity of the Wikipedia user must be reliably verified to the bot in a manner not easily faked, bypassed or avoided.» L39 | «must» MUST | not in source | not in source | not in source | not in source | intention: owner, evidence, when |
| R13 | «However, it can be permissible to instead make these edits via a bot account (particularly if necessary due to the actions being privileged), provided the following conditions are met:» L35 + «Competence: All users directing a bot must have the required skill and knowledge to ensure their actions are within community consensus.» L41 | «must» MUST | «All users directing a bot» L41 | not in source | not in source | not in source | intention: owner, evidence, when |

## Not rules

| Text | Filed as |
|---|---|
| «Wikipedia:Bot policy» L1 | heading |
| «[...]» L3 | heading |
| «Bot usage» L5 | heading |
| «Because bots:» L7 + «are potentially capable of editing far faster than humans can; and» L9 + «have a lower level of scrutiny on each edit than a human editor; and» L11 + «may cause severe disruption if they malfunction or are misused;» L13 + «the community expects bots to meet high standards before they are approved for use on designated tasks.» L15 | statement |
| «Note that high-speed semi-automated editing may effectively be considered bots in some cases (see WP:MEATBOT), even if performed by a human editor.» L15 | statement |
| «Bot accounts» L17 | heading |
| «Contributors should create a separate account in order to operate a bot.» L19 | recommendation «should» |
| «The account's name should identify the bot function (e.g. <Task>Bot), or the operator's main account (e.g. <Username>Bot).» L19 | recommendation «should» |
| «In all cases, it should be immediately clear that the edits are made by an automated account, which is usually achieved by including Bot at the end of the account name.» L19 | recommendation «should» |
| «Tools not considered to be bots do not require a separate account, but some users do choose to make separate accounts for non-bot but high-speed editing.» L19 | statement |
| «All policies apply to a bot account in the same way as to any other user account.» L21 | statement |
| «Bot accounts are considered alternative accounts of their operator.» L21 | statement |
| «Bot accounts should not be used for contributions that do not fall within the scope of the bot's designated tasks.» L23 | recommendation «should not» |
| «In particular, bot operators should not use a bot account to respond to messages related to the bot.» L23 | recommendation «should not» |
| «Bot operators may wish to redirect a bot account's discussion page to their own.» L23 | optional «may» |
| «The "bot" flag» L25 | heading |
| «This flag reduces some of the technical limits imposed by the MediaWiki software.» L27 | statement |
| «Edits by such accounts are hidden by default within recent changes.» L27 | statement |
| «Bot accounts may also be added to the "copyviobot" user group upon BAG request; this flag allows use of the API to add metadata to edits for use in the new pages feed.» L27 | optional «may» |
| «Activity requirements» L29 | heading |
| «Bots directed to edit by other users» L33 | heading |
| «Some bots allow other editors to direct the bot to make an edit or other action.» L35 | statement |
| «It is recommended and preferable to use OAuth to make the edit on the user's account directly.» L35 | recommendation «recommended» |
| «Suitable methods include a non-trivial password, IP restrictions, wiki login or IRC hostname.» L39 | statement |
| «If the bot is used to make sensitive actions, stronger methods of verification may be required.» L39 | statement |
| «Bot requirements» L43 | heading |
| «In order for a bot to be approved, its operator should demonstrate that it:» L45 + «is harmless» L47 | recommendation «should» |
| «In order for a bot to be approved, its operator should demonstrate that it:» L45 + «is useful» L49 | recommendation «should» |
| «In order for a bot to be approved, its operator should demonstrate that it:» L45 + «does not consume resources unnecessarily» L51 | recommendation «should» |
| «In order for a bot to be approved, its operator should demonstrate that it:» L45 + «performs only tasks for which there is consensus» L53 | recommendation «should» |
| «In order for a bot to be approved, its operator should demonstrate that it:» L45 + «carefully adheres to relevant policies and guidelines» L55 | recommendation «should» |
| «In order for a bot to be approved, its operator should demonstrate that it:» L45 + «uses appropriate, informative wording in all edit summaries and messages left for users» L57 | recommendation «should» |
| «The bot account's user page should identify the bot using the {{bot}} tag.» L59 | recommendation «should» |
| «On both the bot account's userpage and in the approval request, the following information should be provided:» L59 + «Details of the bot's task(s)» L61 | recommendation «should» |
| «On both the bot account's userpage and in the approval request, the following information should be provided:» L59 + «Whether the bot is manually assisted or runs automatically» L63 | recommendation «should» |
| «On both the bot account's userpage and in the approval request, the following information should be provided:» L59 + «Whether it runs continuously, intermittently, or at specified intervals, and at what rate» L65 | recommendation «should» |

## Referred elsewhere

| Reference |
|---|
| «WP:MEATBOT» L15 |
| «WP:BOTCOMM» L21 |

## Tally

| Count | Value |
|---|---|
| Rules | 13 |
| Controls | 1 |
| Intentions | 12 |
| Owner named, not collective | 5 |
| Evidence named | 7 |
| When named, not unspecified | 4 |
| Not rules | 36 |
| Outside the policy | 0 |

---

# Example 3: OMB Memorandum M-25-21, section 3 (April 3, 2025)

A government mandate, read from the OCR text layer of a scanned PDF. The page image prints OMB; the
text layer, and so the input, says «0MB» and «OFFlCEOFMANAGEMENTANDBUDGET», and the register keeps
what its input says. Owners here are named offices
(«CAI Os», «Agency heads»), and three rules carry a record and a moment as well: the compliance
plans (R36), the policy update (R40) and the use-case inventory (R43). Where a lead-in says
«Agency heads must:» and the item's own sentence says «each agency must», the lead-in supplies the
owner. A fresh session produced this register from the folder alone; `evidence/cold-run.md` lists
the owner cells corrected afterwards and why.

## Source

| Field | Entry |
|---|---|
| Title | «Accelerating Federal Use of AI through Innovation, Governance, and Public Trust» L12 |
| Issued by | «EXECUTIVE OFFICE OF THE PRESIDENT» L1 + «OFFlCEOFMANAGEMENTANDBUDGET» L2 + «T HE DIRECTOR» L4 |
| Date or version | «April 3, 2025» L6 + «M-25-21» L8 |
| Policy text | L1-L86 |
| Input | `inputs/omb-m-25-21-section-3.txt` |

## Register

| ID | Rule | Force | Addressee | Owner | Evidence | When | Status |
|---|---|---|---|---|---|---|---|
| R1 | «To that end, agencies must identify key officials to lead agency AI adoption and promote the sharing of best practices, empowering the entire Federal workforce to leverage AI in fulfilling their mission.» L18 | «must» MUST | «agencies» L18 | not in source | not in source | not in source | intention: owner, evidence, when |
| R2 | «Consistent with these goals, agencies must undertake the following:» L18 | «must» MUST | «agencies» L18 | not in source | not in source | not in source | intention: owner, evidence, when |
| R3 | «To support this adoption and use, senior agency leaders must effectively distribute responsibilities and accountability, collaborating with agency officials in AI and AI-enabling roles.» L22 | «must» MUST | «senior agency leaders» L22 | not in source | not in source | not in source | intention: owner, evidence, when |
| R4 | «In support of these objectives and consistent with Executive Order 13960 and Executive Order 14179, agency heads are responsible for establishing the following:» L22 + «1. Chief AI Officers.» L24 | «are responsible for» MUST | «agency heads» L22 | «agency heads» L22 | not in source | not in source | intention: evidence, when |
| R5 | «Within 60 days of the issuance of this memorandum, the head of each agency must retain or designate a Chief AI Officer (CAIO).» L24 | «must» MUST | «the head of each agency» L24 | «the head of each agency» L24 | not in source | «Within 60 days of the issuance of this memorandum» L24 | intention: evidence |
| R6 | «CAI Os will promote AI innovation, adoption, and governance, in coordination with appropriate agency officials.» L24 | «will» WILL | «CAI Os» L24 | «CAI Os» L24 | not in source | not in source | intention: evidence, when |
| R7 | «For CFO Act agencies, the CAIO must hold a position at the Senior Executive Service, Scientific and Professional, or Senior Leader level, or equivalent.» L26 | «must» MUST | «the CAIO» L26 | «the CAIO» L26 | not in source | not in source | intention: evidence, when |
| R8 | «For other agencies, the CAIO must be at or above Grade 14 of the General Schedule (GS), or the equivalent for agencies that do not use the GS classification system.» L26 | «must» MUST | «the CAIO» L26 | «the CAIO» L26 | not in source | not in source | intention: evidence, when |
| R9 | «CAIOs must have the necessary authority to perform the responsibilities in this section and must be positioned highly enough to engage regularly with other agency leadership, to include the Deputy Secretary or equivalent.» L26 | «must» MUST | «CAIOs» L26 | «CAIOs» L26 | not in source | «regularly» L26 (unspecified) | intention: evidence, when |
| R10 | «Agencies must notify 0MB within 30 days when the designated CAIO changes or the position is vacant.» L26 | «must» MUST | «Agencies» L26 | «agency heads» L22 | not in source | «within 30 days when the designated CAIO changes or the position is vacant» L26 | intention: evidence |
| R11 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «A. promote agency-wide responsible AI innovation and adoption in accordance with this memorandum through a governance and oversight process;» L28 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R12 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «B. coordinate with other responsible agency officials to ensure that the agency's use of AI complies with applicable law and govemmentwide guidance;» L30 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R13 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «C. serve as the senior advisor on AI to the head of the agency and within their agency's executive decision-making forums;» L32 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R14 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «D. represent their agency in and collaborate with coordination bodies related to their agency's AI activities, including external forums such as AI-related councils, standard-setting bodies, relevant governance boards, or international bodies;» L34 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R15 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «E. maintain the agency's AI Use Case Inventory;20» L36 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | «the agency's AI Use Case Inventory» L36 | not in source | intention: when |
| R16 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «F. ensure processes are in place for the agency's high-impact AI use, consistent with Section 4 of this memorandum, by:» L38 + «1. establishing a process for determining and documenting AI use cases as high-impact;» L40 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R17 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «F. ensure processes are in place for the agency's high-impact AI use, consistent with Section 4 of this memorandum, by:» L38 + «2. establishing processes to measure, monitor, and evaluate the ongoing performance and effectiveness of the agency's high-impact AI applications;» L42 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R18 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «F. ensure processes are in place for the agency's high-impact AI use, consistent with Section 4 of this memorandum, by:» L38 + «3. overseeing agency compliance with requirements to manage risks from the use of AI, including those established in this memorandum and in relevant law and policy;» L44 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R19 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «F. ensure processes are in place for the agency's high-impact AI use, consistent with Section 4 of this memorandum, by:» L38 + «4. establishing a process for an independent review of high-impact use cases before risk acceptance, consistent with Section 4;» L46 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | «before risk acceptance» L46 | intention: evidence |
| R20 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «F. ensure processes are in place for the agency's high-impact AI use, consistent with Section 4 of this memorandum, by:» L38 + «5. centrally tracking high-impact use cases and use case determinations;» L48 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R21 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «G. advise on the transformation of the agency's workforce into an AI-ready workforce;» L50 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R22 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «H. ensure that custom-developed AI code and the data used to develop and test AI are appropriately inventoried, shared, and released in agency code and data repositories, in coordination with their agency's relevant officials;» L52 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | «agency code and data repositories» L52 | not in source | intention: when |
| R23 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «I. provide guidance on AI investments to the agency head and agency CFO related to resourcing requirements necessary to implement this memorandum; and» L54 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R24 | «CAI Os, in coordination with appropriate agency officials, must:» L26 + «J. support agency efforts to track AI spending.» L56 | «must» MUST | «CAI Os» L26 | «CAI Os» L26 | not in source | not in source | intention: evidence, when |
| R25 | «In support of these objectives and consistent with Executive Order 13960 and Executive Order 14179, agency heads are responsible for establishing the following:» L22 + «11. Agency AI Governance Board.» L58 | «are responsible for» MUST | «agency heads» L22 | «agency heads» L22 | not in source | not in source | intention: evidence, when |
| R26 | «Within 90 days of the issuance of this memorandum, each CFO Act agency must convene its relevant agency officials to coordinate and govern issues related to the use of AI within the Executive Branch.» L58 | «must» MUST | «each CFO Act agency» L58 | «agency heads» L22 | not in source | «Within 90 days of the issuance of this memorandum» L58 | intention: evidence |
| R27 | «Agencies are responsible for ensuring that agency AI governance boards:» L58 + «A. include a chair, at the Deputy Secretary level or equivalent, and a vice-chair who is the agency CAIO.» L60 | «are responsible for» MUST | «Agencies» L58 | «Agencies» L58 (collective) | not in source | not in source | intention: owner, evidence, when |
| R28 | «Working through this Board, CAIOs will support their respective Deputy Secretaries in coordinating agency AI activities;» L60 | «will» WILL | «CAIOs» L60 | «CAIOs» L60 | not in source | not in source | intention: evidence, when |
| R29 | «Agencies are responsible for ensuring that agency AI governance boards:» L58 + «B. include appropriate representation from key stakeholder offices or components, including those responsible for addressing IT, cybersecurity, data, budget, statistics, legal counsel, privacy, civil rights, and civil liberties.» L62 | «are responsible for» MUST | «Agencies» L58 | «Agencies» L58 (collective) | not in source | not in source | intention: owner, evidence, when |
| R30 | «When relevant, AI governance boards must include representatives from the following disciplines: agency management, human capital, procurement, customer experience, program evaluation, and officials responsible for implementing AI within an agency's program office(s); and» L62 | «must» MUST | «AI governance boards» L62 | «AI governance boards» L62 | not in source | not in source | intention: evidence, when |
| R31 | «Agencies are responsible for ensuring that agency AI governance boards:» L58 + «C. consult external experts, as needed and appropriate, to broaden the perspective of the designated governance board and to integrate sector-specific expertise, including recommendations on innovative agency AI use cases.» L64 | «are responsible for» MUST | «Agencies» L58 | «Agencies» L58 (collective) | not in source | «as needed» L64 (unspecified) | intention: owner, evidence, when |
| R32 | «Agencies must enable responsible AI governance and ensure innovative and appropriate use of AI agency-wide.» L68 | «must» MUST | «Agencies» L68 | not in source | not in source | not in source | intention: owner, evidence, when |
| R33 | «Agency heads must:» L68 + «1. Empower Agency AI Leaders.» L70 | «must» MUST | «Agency heads» L68 | «Agency heads» L68 | not in source | not in source | intention: evidence, when |
| R34 | «Agencies must enable trained and accountable agency officials at the lowest appropriate level21 to identify, assess, mitigate, and accept risk for AI use cases.22» L70 | «must» MUST | «Agencies» L70 | «Agency heads» L68 | not in source | not in source | intention: evidence, when |
| R35 | «Agency heads must:» L68 + «11. Develop Compliance Plans.» L72 | «must» MUST | «Agency heads» L68 | «Agency heads» L68 | «Compliance Plans» L72 | not in source | intention: when |
| R36 | «Consistent with Section 104( c) and ( d) of the AI in Government Act of 2020, within 180 days of the issuance of this memorandum or any update to this memorandum, and every two years thereafter until 2036, each agency must submit to 0MB and post publicly on the agency's website either a plan to achieve consistency with this memorandum, or a written determination that the agency does not use and does not anticipate using covered AL» L72 | «must» MUST | «each agency» L72 | «Agency heads» L68 | «a plan to achieve consistency with this memorandum» L72 + «a written determination» L72 + «the agency's website» L72 | «within 180 days of the issuance of this memorandum or any update to this memorandum, and every two years thereafter until 2036» L72 | control |
| R37 | «Agencies must also include plans to update any existing internal AI principles and guidelines to ensure consistency with this memorandum.23» L72 | «must» MUST | «Agencies» L72 | «Agency heads» L68 | «plans to update any existing internal AI principles and guidelines» L72 | not in source | intention: when |
| R38 | «0MB will provide templates for these compliance plans.» L72 | «will» WILL | «0MB» L72 | «0MB» L72 | «templates for these compliance plans» L72 | not in source | intention: when |
| R39 | «Agency heads must:» L68 + «m. Update Agency Policies.» L74 | «must» MUST | «Agency heads» L68 | «Agency heads» L68 | «Agency Policies» L74 | not in source | intention: when |
| R40 | «Within 270 days of the issuance of this memorandum, agencies must revisit and update where necessary their internal policies on IT infrastructure ( e.g., software tools, use of open source software, libraries, and code for AI development, software deployment and platform modernization), data (e.g., data inventory; making quality data available for use by AI; lawful access to agency data, third-party data, and publicly available data, where appropriate; representativeness), cybersecurity (e.g., information system authorizations, continuous monitoring, continuous authorizations for Al), and privacy to align with this memorandum, Executive Order 14179, Executive Order 13960, and with applicable law.» L74 | «must» MUST | «agencies» L74 | «Agency heads» L68 | «their internal policies» L74 | «Within 270 days of the issuance of this memorandum» L74 | control |
| R41 | «Agency heads must:» L68 + «1v. Develop Generative AI Policy.» L76 | «must» MUST | «Agency heads» L68 | «Agency heads» L68 | «Generative AI Policy» L76 | not in source | intention: when |
| R42 | «Agency heads must:» L68 + «v. Update AI Use Case Inventories.» L78 | «must» MUST | «Agency heads» L68 | «Agency heads» L68 | «AI Use Case Inventories» L78 | not in source | intention: when |
| R43 | «Each agency (except for the Department of Defense and the Intelligence Community) must inventory its AI use cases at least annually, submit the inventory to 0MB, and post a public version on the agency's website.» L78 | «must» MUST | «Each agency (except for the Department of Defense and the Intelligence Community)» L78 | «Agency heads» L68 | «the inventory» L78 + «a public version on the agency's website» L78 | «at least annually» L78 | control |
| R44 | «0MB will issue detailed instructions to agencies regarding the inventory and its scope.» L78 | «will» WILL | «0MB» L78 | «0MB» L78 | «detailed instructions to agencies regarding the inventory and its scope» L78 | not in source | intention: when |

## Not rules

| Text | Filed as |
|---|---|
| «EXECUTIVE OFFICE OF THE PRESIDENT» L1 | heading |
| «OFFlCEOFMANAGEMENTANDBUDGET» L2 | heading |
| «WASHINGTON, D.C. 20503» L3 | heading |
| «T HE DIRECTOR» L4 | heading |
| «April 3, 2025» L6 | heading |
| «M-25-21» L8 | heading |
| «MEMORANDUM FOR THE HEADS OF EXECUTIVE DEPARTMENTS AND AGENCIES» L10 | heading |
| «SUBJECT: Accelerating Federal Use of AI through Innovation, Governance, and Public Trust» L12 | heading |
| «[...]» L14 | heading |
| «3. IMPROVING AI GOVERNANCE» L16 | heading |
| «Effective AI governance is key to accelerated innovation as it empowers professionals at all levels to align processes, establish clear policies, and foster accountability while reducing unnecessary barriers to AI adoption.» L18 | statement |
| «a. Agency Governance Roles and Bodies» L20 | heading |
| «Consistent with agency policies, the Federal workforce is encouraged to embrace AI adoption at all levels of the Federal Government and to use AI for innovation and increased efficiency.» L22 | recommendation «encouraged» |
| «Agency heads may choose to designate an existing official, such as a Chief Information Officer, Chief Data Officer, Chief Technology Officer, or similar official with relevant or complementary authorities and responsibilities, provided that individual has significant expertise in AI.» L24 | optional «may» |
| «Agencies are permitted to rely on existing governance bodies to fulfill this requirement.» L58 | optional «permitted» |
| «b. Agency Governance Responsibilities» L66 | heading |
| «Agency policies should aim to advance using models that are built with less data, require less compute, and are inherently more explainable, where possible.» L74 | recommendation «should» |
| «Within 270 days ofthe issuance of this memorandum, agencies should develop a policy that sets the terms for acceptable use of generative AI for their missions and establishes adequate safeguards and oversight mechanisms that allow generative AI to be used in the agency without posing undue risk.» L76 | recommendation «should» |
| «Agencies are encouraged to update the public versions of their inventories on an ongoing basis to reflect their current use of AI.» L78 | recommendation «encouraged» |
| «20 As required by Pub. L. No. 117-263, div. G, title LXXII, subtitle B, § 7225 (codified at 40 U.S.C. 11301 note), https://www.congress.gov/l l 7/plaws/publ263/PLAW-l l 7publ263.pdf.» L80 | statement |
| «21 Agencies are encouraged to assign these responsibilities to agency officials who are accountable for the misS:ion outcome of the AI use case.» L82 | recommendation «encouraged» |
| «22 The process for reviewing and accepting risk for AI use cases is separate from, and does not supersede, the authorization process for information systems, consistent with 0MB Circular No. A-130, Managing Information as a Strategic Resource, https:/ /bidenwhitehouse.archives.gov/wp-content/uploads/legacy drupal files/omb/circulars/ A 130/a 130revised.pdf.» L84 | statement |
| «23 Given the importance of context-specific guidance on AI, agencies are encouraged to continue implementing their agency's AI principles and guidelines, so long as they do not conflict with this memorandum.» L86 | recommendation «encouraged» |

## Referred elsewhere

| Reference |
|---|
| «Executive Order 13960» L22 |
| «Executive Order 14179» L22 |
| «Section 4 of this memorandum» L38 |
| «Section 104( c) and ( d) of the AI in Government Act of 2020» L72 |
| «Pub. L. No. 117-263, div. G, title LXXII, subtitle B, § 7225 (codified at 40 U.S.C. 11301 note)» L80 |
| «0MB Circular No. A-130, Managing Information as a Strategic Resource» L84 |

## Tally

| Count | Value |
|---|---|
| Rules | 44 |
| Controls | 3 |
| Intentions | 41 |
| Owner named, not collective | 37 |
| Evidence named | 12 |
| When named, not unspecified | 7 |
| Not rules | 23 |
| Outside the policy | 0 |
