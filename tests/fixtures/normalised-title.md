<!-- expect: trace -->
# Fixture: normalised-title

## Source

| Field | Entry |
|---|---|
| Title | «Wikipedia:Bot Policy» L1 |
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
