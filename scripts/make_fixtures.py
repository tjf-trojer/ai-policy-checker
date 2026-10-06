#!/usr/bin/env python3
"""Write tests/fixtures/: copies of the worked registers, each with one planted defect.

  python3 scripts/make_fixtures.py          replace every .md file in tests/fixtures/
  python3 scripts/make_fixtures.py --help   print this and write nothing

Every fixture keeps its derived fields (status, tally) consistent with the defect, so that it fails
in exactly the check its first line names; `python3 scripts/verify.py` fails unless it does. The
fixtures are generated from examples.md, evidence/noisy-run-register.md and tests/language/, never
edited by hand: change a worked register or an input, then run this again.
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


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def register(text):
    """The five sections of one register, from its Source heading on."""
    body = text[text.index("## Source"):]
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


def count(text, name):
    return int(re.search(r"(?m)^\| %s \| (\d+) \|$" % re.escape(TALLY[name]), text).group(1))


def tally(text, **delta):
    for name, d in delta.items():
        label = TALLY[name]
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
    f["english-policy-refused"] = ("language", sub(
        read("tests/language/ki-richtlinie-refusal.md"), "`tests/language/ki-richtlinie.txt`",
        "`tests/language/ai-note-with-german-quote.txt`"))
    return f


def main(argv=None):
    argparse.ArgumentParser(prog="make_fixtures.py", description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter).parse_args(argv)
    os.makedirs(OUT, exist_ok=True)
    for old in os.listdir(OUT):
        if old.endswith(".md"):
            os.remove(os.path.join(OUT, old))
    made = fixtures()
    for name, (gate, text) in sorted(made.items()):
        with open(os.path.join(OUT, name + ".md"), "w", encoding="utf-8") as fh:
            fh.write("<!-- expect: %s -->\n# Fixture: %s\n\n%s" % (gate, name, text))
    print("%d fixtures written to tests/fixtures/" % len(made))


if __name__ == "__main__":
    main()
