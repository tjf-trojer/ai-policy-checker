#!/usr/bin/env python3
"""Write tests/fixtures/: copies of the worked registers, each with one planted defect.

  python3 scripts/make_fixtures.py          replace every .md file in tests/fixtures/
  python3 scripts/make_fixtures.py --help   print this and write nothing

Every fixture keeps its derived fields (status, tally) consistent with the defect, so that it fails
in exactly the check its first line names; `python3 scripts/verify.py` fails unless it does. The
fixtures are generated from examples.md, evidence/noisy-run-register.md, the German cold-run
registers in evidence/ and tests/language/, never edited by hand: change a worked register or an
input, then run this again.
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tests", "fixtures")
TALLY = {"rules": "Rules", "controls": "Controls", "intentions": "Intentions",
         "owner": "Owner named, not collective", "evidence": "Evidence named",
         "when": "When named, not unspecified", "notrules": "Not rules",
         "outside": "Outside the policy"}
ZAEHLUNG = {"rules": "Regeln", "controls": "Kontrollen", "intentions": "Absichten",
            "owner": "Verantwortlich benannt, nicht kollektiv", "evidence": "Nachweis benannt",
            "when": "Zeitpunkt benannt, nicht unbestimmt", "notrules": "Keine Regeln",
            "outside": "Ausserhalb der Richtlinie"}
NICHT = "nicht in der Quelle"


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def register(text):
    """The five sections of one register, from its Source heading on."""
    body = text[re.search(r"(?m)^## (Source|Quelle)$", text).start():]
    return body.rstrip("\n-").rstrip() + "\n"


def examples():
    out = {}
    for part in re.split(r"(?m)^(?=# Example )", read("examples.md")):
        m = re.match(r"# Example (\d+)", part)
        if m:
            out[m.group(1)] = register(part)
    return out


def sub(text, old, new):
    if old not in text:
        sys.exit("make_fixtures: the worked register no longer holds: %s" % old[:80])
    return text.replace(old, new, 1)


def labels(text):
    """The tally's row names in the register's language."""
    return ZAEHLUNG if "## Zählung" in text else TALLY


def count(text, name):
    return int(re.search(r"(?m)^\| %s \| (\d+) \|$" % re.escape(labels(text)[name]), text).group(1))


def renumber(text):
    """IDs R1, R2, … in the order the rows stand, after a row is added or removed."""
    n = [0]

    def next_id(m):
        n[0] += 1
        return "| R%d |" % n[0]
    return re.sub(r"(?m)^\| R\d+ \|", next_id, text)


def tally(text, **delta):
    for name, d in delta.items():
        label = labels(text)[name]
        text = re.sub(r"(?m)^\| %s \| \d+ \|$" % re.escape(label),
                      "| %s | %d |" % (label, count(text, name) + d), text)
    return text


def statements(rel):
    """A register of a policy in another language as the English lexicon reads it: every line a
    heading (no closing full stop) or a statement, no rules. Every gate but language passes it."""
    lines = read(rel).rstrip("\n").split("\n")
    rows = []
    for n, line in enumerate(lines, 1):
        if line.strip():
            kind = "statement" if re.search(r"[.!?][\"'»“”)\]]*$", line.strip()) else "heading"
            rows.append("| «%s» L%d | %s |" % (line.strip().replace("|", "\\|"), n, kind))
    tally_rows = [(TALLY[k], 0) for k in ("rules", "controls", "intentions", "owner", "evidence", "when")]
    tally_rows += [(TALLY["notrules"], len(rows)), (TALLY["outside"], 0)]
    return "\n".join([
        "## Source", "", "| Field | Entry |", "|---|---|",
        "| Title | «%s» L1 |" % lines[0].strip(), "| Issued by | not in source |",
        "| Date or version | not in source |", "| Policy text | L1-L%d |" % len(lines),
        "| Input | `%s` |" % rel, "",
        "## Register", "", "| ID | Rule | Force | Addressee | Owner | Evidence | When | Status |",
        "|---|---|---|---|---|---|---|---|", "",
        "## Not rules", "", "| Text | Filed as |", "|---|---|"] + rows + [
        "", "## Referred elsewhere", "", "No references in source.", "",
        "## Tally", "", "| Count | Value |", "|---|---|"] +
        ["| %s | %d |" % r for r in tally_rows]) + "\n"


def fixtures():
    ex = examples()
    uk, wp, omb = ex["1"], ex["2"], ex["3"]
    f = {}

    # trace: an owner the policy never names
    f["invented-owner"] = ("trace", tally(sub(
        wp, "| not in source | not in source | «for two years» L31 | intention: owner, evidence |",
        "| «the Bot Approvals Group» L31 | not in source | «for two years» L31 | intention: evidence |"),
        owner=1))
    # trace: a review frequency the policy never states
    f["invented-frequency"] = ("trace", tally(sub(
        wp, "| «a new request for approval (BRFA)» L31 | not in source | intention: owner, when |",
        "| «a new request for approval (BRFA)» L31 | «annually» L31 | intention: owner |"), when=1))
    # trace: the title spelled the usual way instead of as written
    f["normalised-title"] = ("trace", sub(wp, "| Title | «Wikipedia:Bot policy» L1 |",
                                          "| Title | «Wikipedia:Bot Policy» L1 |"))
    # trace: a true quotation pinned to the wrong line
    f["wrong-line"] = ("trace", sub(wp, "| «Bots» L19 | «its operator» L21 |", "| «Bots» L19 | «its operator» L19 |"))
    # trace: evidence paraphrased
    f["paraphrased-evidence"] = ("trace", sub(
        wp, "«a one-week notification period on the bots noticeboard, and the operator's talk page» L31",
        "«a one-week notice on the bots noticeboard» L31"))
    # trace: an OCR error repaired
    f["repaired-ocr"] = ("trace", sub(omb, "| «will» WILL | «0MB» L72 | «0MB» L72 |",
                                      "| «will» WILL | «0MB» L72 | «OMB» L72 |"))

    # force: an obligation filed as advice
    t = sub(wp, "| R3 | «Bots must edit only while logged into their account.» L19 | «must» MUST | «Bots» L19 "
                "| «its operator» L21 | not in source | not in source | intention: evidence, when |\n", "")
    for i in range(4, 14):
        t = sub(t, "| R%d |" % i, "| R%d |" % (i - 1))
    t = sub(t, "| «Tools not considered to be bots",
            "| «Bots must edit only while logged into their account.» L19 | recommendation «must» |\n"
            "| «Tools not considered to be bots")
    f["must-filed-as-advice"] = ("force", tally(t, rules=-1, intentions=-1, owner=-1, notrules=1))
    # force: a class the lexicon does not give the term
    f["wrong-class"] = ("force", sub(wp, "| «will» WILL | «a bureaucrat» L27 |", "| «will» MUST | «a bureaucrat» L27 |"))
    # force: an item's verb taken as a command when its lead-in carries the force
    f["item-verb-as-command"] = ("force", sub(
        omb, "through a governance and oversight process;» L28 | «must» MUST |",
        "through a governance and oversight process;» L28 | «promote» MUST (imperative) |"))

    # flags: a vague moment without its flag
    f["unflagged-vague-when"] = ("flags", sub(
        wp, "| «their approved conditions of operation» L15 | not in source | intention: when |",
        "| «their approved conditions of operation» L15 | «in some cases» L15 | intention: when |"))
    # flags: a crowd as owner without its flag
    f["unflagged-collective"] = ("flags", sub(
        uk, "| «Never» MUST NOT (imperative) | not in source | «users» L23 (collective) |",
        "| «Never» MUST NOT (imperative) | not in source | «users» L23 |"))
    # status: a control reported as an intention
    f["wrong-status"] = ("status", tally(sub(wp, "| «upon BAG request» L27 | control |",
                                             "| «upon BAG request» L27 | intention: when |"),
                                         controls=-1, intentions=1))
    # tally: a count that does not add up
    f["wrong-tally"] = ("tally", tally(wp, controls=1))

    # coverage: a sentence dropped
    f["dropped-sentence"] = ("coverage", tally(sub(
        wp, "| «Edits by such accounts are hidden by default within recent changes.» L27 | statement |\n", ""),
        notrules=-1))
    # coverage: a rule filed twice
    f["double-filed"] = ("coverage", tally(sub(
        wp, "| «This flag reduces",
        "| «Bot accounts will be marked by a bureaucrat as being in the \"bot\" user group upon BAG "
        "request.» L27 | statement |\n| «This flag reduces"), notrules=1))
    # coverage: a lead-in filed on its own, its items quoted without it
    lead = ("«However, it can be permissible to instead make these edits via a bot account (particularly "
            "if necessary due to the actions being privileged), provided the following conditions are met:» L35")
    t = wp.replace(lead + " + ", "")
    t = sub(t, "| «Suitable methods include", "| %s | optional «permissible» |\n| «Suitable methods include" % lead)
    f["lead-in-alone"] = ("coverage", tally(t, notrules=1))

    # shape: a section missing
    f["missing-section"] = ("shape", re.sub(r"(?s)## Referred elsewhere\n.*?(?=## Tally)", "", wp))
    # shape: an empty field left blank instead of not in source
    f["blank-field"] = ("shape", sub(
        wp, "avoided.» L39 | «must» MUST | not in source | not in source | not in source |",
        "avoided.» L39 | «must» MUST | not in source | not in source |  |"))
    # shape: a judgement slipped into a cell
    f["judgement-in-cell"] = ("shape", sub(
        wp, "| «Bots» L19 | «its operator» L21 | not in source | not in source | intention: evidence, when |",
        "| «Bots» L19 | «its operator» L21 | not in source (the policy should name a log) | not in source "
        "| intention: evidence, when |"))

    # scope: evidence taken from a neighbouring sentence
    f["evidence-from-elsewhere"] = ("scope", tally(sub(
        wp, "| «Bots» L19 | «its operator» L21 | not in source | not in source | intention: evidence, when |",
        "| «Bots» L19 | «its operator» L21 | «its user page» L21 | not in source | intention: when |"),
        evidence=1))
    # scope: an owner borrowed from a line that assigns no responsibility
    f["borrowed-owner"] = ("scope", tally(sub(
        wp, "| «will» WILL | not in source | not in source | not in source | «for two years» L31 | intention: owner, evidence |",
        "| «will» WILL | not in source | «a bureaucrat» L27 | not in source | «for two years» L31 | intention: evidence |"),
        owner=1))
    # scope: a crowd the rule only addresses made its owner
    f["addressed-crowd-as-owner"] = ("scope", sub(
        omb, "| «agencies» L18 | not in source | not in source | not in source | intention: owner, evidence, when |",
        "| «agencies» L18 | «agencies» L18 (collective) | not in source | not in source "
        "| intention: owner, evidence, when |"))
    # scope: a hole cut in the middle of the policy with no seam
    t = sub(wp, "| Policy text | L1-L65 |", "| Policy text | L1-L28 + L30-L65 |")
    t = sub(t, "| «Activity requirements» L29 | heading |", "| «Activity requirements» L29 | outside the policy |")
    f["hole-without-seam"] = ("scope", tally(t, outside=1))

    noisy_path = os.path.join(ROOT, "evidence", "noisy-run-register.md")
    if os.path.exists(noisy_path):
        noisy = register(read("evidence/noisy-run-register.md"))
        email = "We must remember to book the room before the 14th, or we lose it."
        row = next(l for l in noisy.split("\n") if email in l and l.startswith("| «"))
        quote = row.split(" | ")[0][2:]
        n_rules = count(noisy, "rules")
        last = re.findall(r"(?m)^\| (R\d+) \|", noisy)[-1]
        rule = ("| R%d | %s | «must» MUST | not in source | not in source | not in source | not in source "
                "| intention: owner, evidence, when |" % (n_rules + 1, quote))
        t = sub(noisy, row + "\n", "")
        i = t.index("\n", t.index("| %s |" % last)) + 1
        t = t[:i] + rule + "\n" + t[i:]
        # scope: the stapled email's «must» filed as a rule of the policy
        f["email-as-rule"] = ("scope", tally(t, rules=1, intentions=1, notrules=-1, outside=-1))
        span = re.search(r"(?m)^\| Policy text \| (.+) \|$", noisy)
        last_line = len(read("tests/noisy/wikipedia-bot-policy-stapled-email.txt").rstrip("\n").split("\n"))
        # scope: the Policy text swallows the stapled email
        f["policy-swallows-email"] = ("scope", sub(noisy, span.group(0), "| Policy text | L1-L%d |" % last_line))

    # language: a German policy filed sentence by sentence as statements, and the register finds no rules
    f["german-policy-as-statements"] = ("language", statements("tests/language/ki-richtlinie.txt"))
    # language: the same for a French policy that quotes with «…» itself
    f["french-policy-as-statements"] = ("language", statements("tests/language/politique-ia.txt"))
    # language: an English policy refused as if it were in another language
    german(ex["4"], ex["5"], f)
    german_cold(f)
    f["english-policy-refused"] = ("language", sub(
        read("tests/language/politique-ia-refusal.md"), "`tests/language/politique-ia.txt`",
        "`tests/language/ai-note-with-german-quote.txt`"))
    return f


def german(zh, sg, f):
    """Defects planted in the German registers of Examples 4 (Zürich) and 5 (St. Gallen)."""
    art9 = "| «dürfen» DARF NICHT | %s |" % NICHT
    r16 = ("| R16 | «Art. 10 Die Angestellten prüfen die Ergebnisse der KI-Werkzeuge auf deren Richtigkeit und "
           "Vollständigkeit.» L101 | «prüfen» MUSS (Präsens) |")
    # force: a prohibition filed under the class of an obligation
    f["german-wrong-class"] = ("force", sub(zh, "politischen Geschäften;» L81 " + art9,
                                            "politischen Geschäften;» L81 | «dürfen» MUSS | %s |" % NICHT))
    # force: a duty in the present tense without its (Präsens)
    f["present-tense-unflagged"] = ("force", sub(zh, r16, r16.replace("MUSS (Präsens)", "MUSS")))
    # scope: a crowd the rule only addresses made its owner
    f["german-addressed-crowd-as-owner"] = ("scope", sub(
        zh, r16 + " «Die Angestellten» L101 | %s |" % NICHT,
        r16 + " «Die Angestellten» L101 | «Die Angestellten» L101 (kollektiv) |"))
    # force: the same duty filed as a statement
    row = next(l for l in zh.split("\n") if l.startswith(r16))
    t = renumber(sub(zh, row + "\n", ""))
    t = sub(t, "| «Verwendung» L103 | Überschrift |",
            "| «Art. 10 Die Angestellten prüfen die Ergebnisse der KI-Werkzeuge auf deren Richtigkeit und "
            "Vollständigkeit.» L101 | Feststellung |\n| «Verwendung» L103 | Überschrift |")
    f["present-tense-as-statement"] = ("force", tally(t, rules=-1, intentions=-1, notrules=1))
    # force: a present-tense rule in a policy whose title names no directive
    f["present-tense-without-directive"] = ("force", sub(
        zh, "| Titel | «Richtlinie über die Nutzung von generativer künstlicher Intelligenz (KI-Richtlinie)» L1 |",
        "| Titel | «STRB Nr. 2281 vom 20. August 2025» L3 |"))
    # trace: an owner the directive never names
    r4 = "ist verboten.» L41 | «verboten» DARF NICHT | %s | %s | %s | %s | Absicht: Verantwortlich, Nachweis, Zeitpunkt |" % ((NICHT,) * 4)
    f["german-invented-owner"] = ("trace", tally(sub(zh, r4, r4.replace(
        "| %s | %s | %s | %s | Absicht: Verantwortlich, Nachweis, Zeitpunkt |" % ((NICHT,) * 4),
        "| %s | «die Informatikdienste» L41 | %s | %s | Absicht: Nachweis, Zeitpunkt |" % ((NICHT,) * 3))),
        owner=1))
    # shape: the marker for an empty field misspelt
    f["german-marker-misspelt"] = ("shape", sub(zh, "politischen Geschäften;» L81 " + art9,
                                                "politischen Geschäften;» L81 | «dürfen» DARF NICHT | nicht in Quelle |"))
    # shape: an English contract word in a German register
    f["german-register-english-word"] = ("shape", sub(zh, "politischen Geschäften;» L81 " + art9,
                                                      "politischen Geschäften;» L81 | «dürfen» DARF NICHT | not in source |"))
    # force: a modal sentence filed as a statement
    r7 = next(l for l in sg.split("\n") if l.startswith("| R7 | «Es muss geprüft werden"))
    t = renumber(sub(sg, r7 + "\n", ""))
    t = sub(t, "| «1 Verabschiedet vom", "| «Es muss geprüft werden, ob ein Text diskriminierend wirkt.» L93 "
            "| Feststellung |\n| «1 Verabschiedet vom")
    f["german-modal-as-statement"] = ("force", tally(t, rules=-1, intentions=-1, notrules=1))
    # scope: the sample prompt filed as a rule of the guidelines
    prompt = ("«Nenne mir die drei wichtigsten Punkte, die den Kanton St.Gallen als modernen und "
              "zukunftsgerichteten Kanton beschreiben, und gib eine kurze Erklärung.» L73")
    t = sub(sg, "| %s | ausserhalb der Richtlinie |\n" % prompt, "")
    r3 = next(l for l in t.split("\n") if l.startswith("| R3 |"))
    t = sub(t, r3 + "\n", r3 + "\n| R0 | %s | «Nenne» MUSS (Imperativ) | %s | %s | %s | %s | Absicht: "
            "Verantwortlich, Nachweis, Zeitpunkt |\n" % ((prompt,) + (NICHT,) * 4))
    f["sample-prompt-as-rule"] = ("scope", tally(renumber(t), rules=1, intentions=1, notrules=-1, outside=-1))


def german_cold(f):
    """Defects planted in the German cold-run registers: the clause an infinitive with «zu» needs."""
    az = register(read("evidence/cold-run-de-appenzell-register.md"))
    da = register(read("evidence/cold-run-de-darmstadt-register.md"))
    nis4 = " | ".join([NICHT] * 4)
    # force: «zu beachten» whose «sind» stands before a list of nouns, filed as a statement
    r16 = next(l for l in az.split("\n") if l.startswith("| R16 |"))
    quote = r16.split(" | ")[1]
    t = renumber(sub(az, r16 + "\n", ""))
    t = sub(t, "| «2.4 Rechtliche Vorgaben» L61 | Überschrift |\n",
            "| «2.4 Rechtliche Vorgaben» L61 | Überschrift |\n| %s | Feststellung |\n" % quote)
    f["zu-across-noun-list-as-statement"] = ("force", tally(t, rules=-1, intentions=-1, notrules=1))
    # force: «zu nutzen» whose «sind» stands before «z. B.», filed as a statement
    r21 = next(l for l in da.split("\n") if l.startswith("| R21 |"))
    quote = r21.split(" | ")[1]
    t = renumber(sub(da, r21 + "\n", ""))
    t = sub(t, "| «Sofern weitere Daten", "| %s | Feststellung |\n| «Sofern weitere Daten" % quote)
    f["zu-across-abbreviation-as-statement"] = ("force", tally(t, rules=-1, intentions=-1, notrules=1))
    # force: an infinitive with «zu» after «ist es,», in a clause with no carrier, filed as a rule
    goal = ("«Ziel der Meldung ist es, mögliche Auswirkungen soweit möglich zu begrenzen und aus dem "
            "Vorfall zu lernen.» L83")
    t = sub(az, "| %s | Feststellung |\n" % goal, "")
    r23 = next(l for l in t.split("\n") if l.startswith("| R23 |"))
    t = sub(t, r23 + "\n", r23 + "\n| R24 | %s | «zu begrenzen» MUSS | %s | Absicht: Verantwortlich, "
            "Nachweis, Zeitpunkt |\n" % (goal, nis4))
    f["zu-in-clause-without-carrier-as-rule"] = ("force", tally(t, rules=1, intentions=1, notrules=-1))


def main(argv=None):
    argparse.ArgumentParser(prog="make_fixtures.py", description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter).parse_args(argv)
    made = fixtures()
    os.makedirs(OUT, exist_ok=True)
    for old in os.listdir(OUT):
        if old.endswith(".md"):
            os.remove(os.path.join(OUT, old))
    for name, (gate, text) in sorted(made.items()):
        with open(os.path.join(OUT, name + ".md"), "w", encoding="utf-8") as fh:
            fh.write("<!-- expect: %s -->\n# Fixture: %s\n\n%s" % (gate, name, text))
    print("%d fixtures written to tests/fixtures/" % len(made))


if __name__ == "__main__":
    main()
