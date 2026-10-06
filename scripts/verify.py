#!/usr/bin/env python3
"""Check that a register honours reference/register-schema.md against its input.

A register is the set of markdown tables a translation produces from one policy
text. Nine gates run on each register:

  language  the input is in the language the lexicon covers: its marker words
            make up at least the share the lexicon sets (an input shorter
            than the lexicon's fewest words is not judged)
  shape     the five sections in order, exact table headers, cell counts, IDs,
            row order, and the form of every cell
  trace     every quotation is in the input, character for character,
            starting on the first line it cites and ending on the last
  force     force terms and classes agree with the lexicon, an
            imperative stands at an opening and is not an item completing a
            lead-in that has force of its own, no rule is filed below its
            strongest term, and no sentence opened by or holding a forced
            term is filed under Not rules
  flags     "(collective)" and "(unspecified)" are set exactly where the
            lexicon says
  status    each status follows from the Owner, Evidence and When cells
  tally     the eight counts follow from the Register and Not rules sections
  coverage  every letter and digit of the input sits inside a Rule or
            Not-rules quotation, no text is quoted as both, and no lead-in
            (an entry ending in a colon) stands alone unless headings follow it
  scope     Addressee, Evidence and When quote only lines the row's Rule
            quotes; the Owner quotes those, a lead-in above them or a line
            with a responsibility word; every quotation sits inside the
            Policy text unless its entry is filed outside the policy, and
            an outside block mid-input opens with a seam marker

An input in a language no lexicon covers gets no register but the one-line
refusal of rules/posture.md. A file holding that line is checked by two gates:
shape (the line has its fixed form and stands alone) and language (the input is
in no lexicon's language, and the line names every language a lexicon covers).

The word lists are read from the lexicons on every run: the file --lexicon
names, or reference/lexicon.md in the repository and every lexicon-*.md beside
it, or, where the repository's layout is absent (files uploaded side by side),
the same files beside the register, in the working directory or beside this
script. Everything that depends on the input's language comes from a lexicon.
The register's own fixed words (section and column names, "not in source",
filings, statuses, flags, force classes, the refusal) come from the table
Contract words in reference/register-schema.md, found the same way, in the
column a lexicon's Language names. Each register is checked in one language:
the one whose section names its "## " headings use, English on a tie; a
refusal, in the language it opens with. The language gate then holds the input
to that language.

What it cannot check: it proves the quotations and every field derived from
them, not that a sentence was read correctly. It cannot tell whether a quoted
owner is really answerable for that rule, whether a quoted artefact would show
the rule was met, whether a "will" is binding or descriptive, whether a "may"
grants or only describes, whether an opening word is a verb, or whether every
document the policy names is listed under Referred elsewhere.

Usage:
  python3 scripts/verify.py                       examples.md, evidence/*register*.md,
                                                  tests/language/*.md and the fixture
                                                  self-test
  python3 scripts/verify.py PATH.md [--input F]   one file; each "# Example " block
                                                  in it if it has any
  python3 scripts/verify.py --selftest            fixtures in tests/fixtures/ only
  --lexicon PATH                                  the one lexicon to apply, instead
                                                  of choosing by the register's language

A Source Input path is looked up from the working directory first, then from the
repository root, then in tests/noisy/ (the adversarial runs' inputs, under the names their sessions
were given); --input, when given, must name the same file.

Exit status is 0 only when every register passes and every fixture fails in the
gate it declares and in no other.
"""

import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEXICON = os.path.join(ROOT, "reference", "lexicon.md")
SCHEMA = os.path.join(ROOT, "reference", "register-schema.md")
EXAMPLES = os.path.join(ROOT, "examples.md")
FIXTURES = os.path.join(ROOT, "tests", "fixtures")

GATES = ["language", "shape", "trace", "force", "flags", "status", "tally", "coverage", "scope"]
LQ = "\u00ab"
RQ = "\u00bb"
NIS = "not in source"
NO_REFS = "No references in source."
SHOWN = 5

SECTIONS = ["Source", "Register", "Not rules", "Referred elsewhere", "Tally"]
HEADERS = {
    "Source": ["Field", "Entry"],
    "Register": ["ID", "Rule", "Force", "Addressee", "Owner", "Evidence", "When", "Status"],
    "Not rules": ["Text", "Filed as"],
    "Referred elsewhere": ["Reference"],
    "Tally": ["Count", "Value"],
}
SOURCE_ROWS = ["Title", "Issued by", "Date or version", "Policy text", "Input"]
TALLY_ROWS = ["Rules", "Controls", "Intentions", "Owner named, not collective",
              "Evidence named", "When named, not unspecified", "Not rules",
              "Outside the policy"]
REGISTER_CLASSES = ["MUST NOT (imperative)", "MUST (imperative)", "MUST NOT (present)",
                    "MUST (present)", "MUST NOT", "MUST", "WILL NOT", "WILL"]
TIER = {"MUST NOT (imperative)": 3, "MUST (imperative)": 3, "MUST NOT (present)": 3,
        "MUST (present)": 3, "MUST NOT": 3, "MUST": 3,
        "WILL NOT": 2, "WILL": 2, "SHOULD NOT": 1, "SHOULD": 1, "MAY": 0}
FILINGS = {"recommendation": ("SHOULD", "SHOULD NOT"), "optional": ("MAY",)}
ATTRS = ["owner", "evidence", "when"]

QUOTE_MAP = {"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
             "\u201c": '"', "\u201d": '"', "\u201e": '"'}

QRE = re.compile(LQ + r"(.+?)" + RQ + r" L(\d+)(?:-L(\d+))?")
LANGUAGE_NAME = r"[A-Z\u00c0-\u00de][\w-]*(?: [A-Z\u00c0-\u00de][\w-]*)*"
REFUSAL_FORM = "No register: the input `<path>` is not in <languages>."
WORD = re.compile(r"[^\W\d_]+")
OUTSIDE = "outside the policy"
CONTRACT_WORDS = (SECTIONS + [h for s in SECTIONS for h in HEADERS[s]] + SOURCE_ROWS + TALLY_ROWS +
                  ["none", "pasted", NIS, NO_REFS, "control", "intention"] + ATTRS +
                  ["(collective)", "(unspecified)", "MUST NOT", "MUST", "WILL NOT", "WILL",
                   "SHOULD NOT", "SHOULD", "MAY", "(imperative)", "(present)", "recommendation",
                   "optional", "statement", "heading", OUTSIDE, REFUSAL_FORM, "or"])
SPAN_RE = re.compile(r"L(\d+)(?:-L(\d+))?")
SEPARATOR = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
RULE_LINE = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")
SENT_END = re.compile(r"[.:?!][\"')\]]*\s+")
MARKER = re.compile(r"(?:#+\s+|[-*\u2022]\s+|\(?[A-Za-z0-9]{1,4}[.)]\s+|[\"'(\[]+)")
CLAUSE_END = re.compile(r"[.!?](?=[\"')\]]*(?:\s|$))")
CLAUSE_START = re.compile(r"[,;:][\"')\]]*\s+")
DIGITS = re.compile(r"(?<![^\W_])[0-9]+(?![^\W_])")

LEX = None
C = None
LEXICONS = []   # (lexicon, its contract words), English first


# ---------------------------------------------------------------- text

def norm(s):
    """Straighten typographic quotes and collapse whitespace runs to one space."""
    out = []
    space = False
    for ch in s:
        if ch.isspace():
            if not space:
                out.append(" ")
            space = True
        else:
            out.append(QUOTE_MAP.get(ch, ch))
            space = False
    return "".join(out)


def unescape(s):
    return s.replace("\\|", "|")


def clip(s, n=70):
    s = s.replace("\n", " ")
    return s if len(s) <= n else s[:n - 3] + "..."


def words_re(words):
    alts = sorted(set(words), key=len, reverse=True)
    body = "|".join(r"\s+".join(re.escape(w) for w in t.split()) for t in alts)
    return re.compile(r"(?<!\w)(?:" + body + r")(?!\w)", re.IGNORECASE)


# ---------------------------------------------------------------- lexicon

class LexiconError(Exception):
    pass


class Lexicon(object):
    pass


def md_sections(text):
    out = {}
    cur = None
    for line in text.split("\n"):
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return out


def md_table(lines, where, name):
    """The first table in a section whose header has the column name."""
    split = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
    blocks = []
    cur = None
    for line in lines:
        if line.strip().startswith("|"):
            if cur is None:
                cur = []
                blocks.append(cur)
            cur.append(line)
        else:
            cur = None
    for block in blocks:
        if len(block) >= 2 and name in split(block[0]):
            header = split(block[0])
            return header, [split(r) for r in block[2:]]
    raise LexiconError("no table with a '%s' column under '## %s'" % (name, where))


def optional_table(lines, where, name):
    """Like md_table, or None where the section holds no such table: a feature the lexicon may leave
    out."""
    try:
        return md_table(lines, where, name)
    except LexiconError:
        return None


def words_of(lines, where, name):
    """The non-empty cells of the one-column table name, normalised and lower-cased; [] without it."""
    t = optional_table(lines, where, name)
    if t is None:
        return []
    i = column(t[0], name, where)
    return [norm(r[i]).strip("`").strip().lower() for r in t[1] if r[i].strip("`- ")]


def parse_entry(cls, filed, forced, where):
    if cls not in TIER:
        raise LexiconError("unknown class '%s' for %s" % (cls, where))
    forced = forced.lower()
    if forced not in ("yes", "no", "opening"):
        raise LexiconError("unknown Forced value '%s' for %s" % (forced, where))
    return (cls, filed, forced)


def parse_negated(cell, where):
    """A Negated cell: '', 'none', or a class with ', forced'."""
    cell = cell.strip()
    if cell in ("", "-", "\u2014"):
        return None
    if cell.lower() == "none":
        return "none"
    cls, _, flag = cell.partition(",")
    cls = cls.strip()
    return parse_entry(cls, "Register" if TIER.get(cls, 0) >= 2 else "Not rules",
                       "yes" if flag.strip().lower() == "forced" else "no", where)


def column(header, name, where):
    if name not in header:
        raise LexiconError("table under '## %s' has no column '%s'" % (where, name))
    return header.index(name)


def load_lexicon(path):
    try:
        with open(path, encoding="utf-8") as fh:
            secs = md_sections(fh.read())
    except OSError as e:
        raise LexiconError("cannot read %s: %s" % (path, e))
    for name in ("Language", "Force", "Collective owners", "Timing words", "Policy edges"):
        if name not in secs:
            raise LexiconError("no '## %s' section" % name)
    lex = Lexicon()

    header, body = md_table(secs["Language"], "Language", "Setting")
    iset, ival = column(header, "Setting", "Language"), column(header, "Value", "Language")
    settings = dict((r[iset].strip().lower(), r[ival].strip()) for r in body if len(r) > ival)
    lex.language = settings.get("language", "")
    share = settings.get("marker share", "").rstrip("%").strip()
    fewest = settings.get("fewest words", "")
    if not lex.language or not re.match(r"^\d+(\.\d+)?$", share) or not fewest.isdigit():
        raise LexiconError("the Setting table under '## Language' needs Language, Marker share "
                           "(a percentage) and Fewest words (a whole number)")
    lex.marker_share = float(share) / 100
    lex.fewest_words = int(fewest)
    header, body = md_table(secs["Language"], "Language", "Marker word")
    i = column(header, "Marker word", "Language")
    lex.markers = set(norm(r[i]).strip("`").strip().lower() for r in body if r[i].strip())
    if not lex.markers:
        raise LexiconError("the Marker word table under '## Language' is empty")

    force = secs["Force"]
    header, body = md_table(force, "Force", "Term")
    it, ic, ifi, ifo = [column(header, n, "Force") for n in ("Term", "Class", "Filed in", "Forced")]
    ineg = header.index("Negated") if "Negated" in header else None
    lex.terms = {}
    lex.negated = {}
    lex.zu_entry = lex.present_entry = None
    for row in body:
        term = row[it].strip("`").strip()
        if not term:
            continue
        where = "term '%s'" % term
        entry = parse_entry(row[ic], row[ifi], row[ifo], where)
        neg = parse_negated(row[ineg], where) if ineg is not None else None
        if term[0] in "_*":
            # a form, not a word: the lexicon's tables below say how it is found
            if "\u00abzu\u00bb" in term:
                lex.zu_entry, lex.zu_negated = entry, neg
            elif "(present)" in entry[0]:
                lex.present_entry, lex.present_negated = entry, neg
            continue
        lex.terms[norm(term).lower()] = entry
        if neg is not None:
            lex.negated[norm(term).lower()] = neg
    if not lex.terms:
        raise LexiconError("the Force table holds no terms")
    lex.term_re = words_re(lex.terms)
    header, body = md_table(secs["Force"], "Force", "Joining word")
    i = column(header, "Joining word", "Force")
    joiners = sorted(set(norm(r[i]).strip("`").strip().lower() for r in body if r[i].strip()),
                     key=len, reverse=True)
    lex.joiner_re = re.compile(r"(?:" + "|".join(r"\s+".join(re.escape(w) for w in j.split())
                                                for j in joiners) + r")\s+",
                               re.IGNORECASE) if joiners else None
    # a joining word written with its full stop («bzw.») is the word without it among the tokens
    lex.joiners = set(j.rstrip(".") for j in joiners)

    # what a lexicon may add for its language; English uses none of it
    neg = optional_table(force, "Force", "Negation word")
    lex.negation_re, lex.neg_anywhere = None, set()
    if neg:
        iw = column(neg[0], "Negation word", "Force")
        ib = column(neg[0], "Before the verb", "Force")
        words = [norm(r[iw]).strip().lower() for r in neg[1] if r[iw].strip()]
        lex.negation_re = words_re(words) if words else None
        lex.neg_anywhere = set(norm(r[iw]).strip().lower() for r in neg[1] if r[ib].strip().lower() == "yes")
    if lex.negated and not lex.negation_re:
        raise LexiconError("terms have a Negated class but '## Force' has no Negation word table")
    lex.markers_extra = [re.compile(r"\s+".join(
        re.escape(w).replace(re.escape("<n>"), r"\d{1,3}[a-z]?") for w in m.split()) + r"\s+")
        for m in (r[0] for r in (optional_table(force, "Force", "Opening marker") or ([], []))[1])
        if m.strip("`- ")]
    lex.followers = set(w for w in (r[0].strip() for r in (
        optional_table(force, "Force", "Imperative follower") or ([], []))[1]) if w)
    abbrevs = words_of(force, "Force", "Abbreviation")
    lex.abbrev_re = re.compile(r"(?<![^\W\d_])(?:" + "|".join(
        r"\s*".join(re.escape(p) for p in a.replace(" ", "").replace(".", ". ").split())
        for a in sorted(abbrevs, key=len, reverse=True)) + r")", re.IGNORECASE) if abbrevs else None
    lex.list_comma_re = re.compile(
        r",\s+[A-Z\u00c0-\u00de][\w\u2011-]*\s*(?:,|(?i:%s)(?!\w))"
        % "|".join(re.escape(j) for j in sorted(lex.joiners, key=len, reverse=True))) if lex.joiners else None
    lex.carriers = set(words_of(force, "Force", "Carrier"))
    lex.inf_endings = tuple(e.lstrip("-") for e in words_of(force, "Force", "Infinitive ending"))
    if lex.zu_entry and not (lex.carriers and lex.inf_endings):
        raise LexiconError("the «zu» infinitive needs the Carrier and Infinitive ending tables")
    lex.directive_re = None
    if lex.present_entry:
        directive = words_of(force, "Force", "Directive word")
        dets = words_of(force, "Force", "Determiner")
        lex.not_verbs = set(words_of(force, "Force", "Not a present-tense verb"))
        actors = words_of(force, "Force", "Actor")
        if not (directive and dets and actors):
            raise LexiconError("the present tense needs the Directive word, Determiner and Actor tables")
        lex.directive_re = words_re(directive)
        lex.actors = actors

    coll = secs["Collective owners"]
    header, body = md_table(coll, "Collective owners", "Collective")
    i = column(header, "Collective", "Collective owners")
    lex.collective = [norm(r[i]).lower().strip() for r in body if r[i].strip()]
    header, body = md_table(coll, "Collective owners", "Cut word")
    i = column(header, "Cut word", "Collective owners")
    lex.cut_words = set(norm(r[i]).lower().strip() for r in body if r[i].strip())
    if not lex.collective or not lex.cut_words:
        raise LexiconError("the Collective or Cut word table under '## Collective owners' is empty")
    header, body = md_table(coll, "Collective owners", "Participle ending")
    i = column(header, "Participle ending", "Collective owners")
    lex.participle_endings = tuple(norm(r[i]).strip("`").strip().lstrip("-").lower()
                                   for r in body if r[i].strip("`- "))
    t = optional_table(coll, "Collective owners", "Setting")
    settings = dict((r[0].strip().lower(), r[1].strip().lower()) for r in t[1]) if t else {}
    lex.compounds = settings.get("compounds") == "yes"
    if lex.present_entry:
        actors = sorted(set(lex.actors + lex.collective), key=len, reverse=True)
        # an actor is a whole word: with compounds, «Die Weiterleitung» would end in «leitung»
        lex.present_re = re.compile(
            r"(?i:%s)\s+(?:[a-z\u00df-\u00ff][\w-]*\s+){0,2}(?i:%s)\s+(?P<verb>[a-z\u00df-\u00ff]+)(?![\w-])"
            % ("|".join(re.escape(d) for d in words_of(secs["Force"], "Force", "Determiner")),
               "|".join(r"\s+".join(re.escape(w) for w in a.split()) for a in actors)))

    header, body = md_table(secs["Timing words"], "Timing words", "Kind")
    ik, iw = column(header, "Kind", "Timing words"), column(header, "Words", "Timing words")
    lex.digit = False
    timing = []
    for row in body:
        if row[ik].strip().lower() == "digit":
            lex.digit = True
        else:
            timing += [w.strip().lower() for w in row[iw].split(",") if w.strip()]
    lex.timing_re = words_re(timing) if timing else None
    vague = words_of(secs["Timing words"], "Timing words", "Unspecified phrase")
    lex.vague_re = words_re(vague) if vague else None

    edges = secs["Policy edges"]
    header, body = md_table(edges, "Policy edges", "Seam marker")
    i = column(header, "Seam marker", "Policy edges")
    lex.seams = [norm(r[i]).strip("`").strip().lower() for r in body if r[i].strip()]
    header, body = md_table(edges, "Policy edges", "Responsibility word")
    i = column(header, "Responsibility word", "Policy edges")
    lex.responsibility_re = words_re([norm(r[i]).strip().lower() for r in body if r[i].strip()])
    if not lex.seams:
        raise LexiconError("the Seam marker table under '## Policy edges' is empty")
    return lex


def find_lexicon(register=None):
    """reference/lexicon.md in the repository; without that layout, lexicon.md beside the
    register, in the working directory, or beside this script."""
    return find_beside(LEXICON, "lexicon.md", register)


def find_lexicons(register=None):
    """lexicon.md and every lexicon-*.md beside it, lexicon.md first."""
    first = find_lexicon(register)
    others = sorted(glob.glob(os.path.join(os.path.dirname(first), "lexicon-*.md")))
    return [first] + others


def find_beside(path, name, register=None):
    """path in the repository; without that layout, name beside the register, in the working
    directory, or beside this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [path]
    if register:
        cands.append(os.path.join(os.path.dirname(os.path.abspath(register)), name))
    cands += [os.path.join(os.getcwd(), name), os.path.join(here, name)]
    return next((p for p in cands if os.path.isfile(p)), path)


def load_contract(path):
    """The table Contract words of the schema: {language: {English word: the language's word}}."""
    try:
        with open(path, encoding="utf-8") as fh:
            secs = md_sections(fh.read())
    except OSError as e:
        raise LexiconError("cannot read %s: %s" % (path, e))
    if "Contract words" not in secs:
        raise LexiconError("no '## Contract words' section")
    header, body = md_table(secs["Contract words"], "Contract words", "English")
    out = dict((lang, {}) for lang in header)
    for row in body:
        if len(row) != len(header):
            raise LexiconError("a row under '## Contract words' has %d cells, not %d"
                               % (len(row), len(header)))
        for lang, word in zip(header, row):
            out[lang][row[0]] = word
    missing = [w for w in CONTRACT_WORDS if w not in out["English"]]
    if missing:
        raise LexiconError("the table under '## Contract words' lacks %s" % ", ".join(missing))
    return out


class Contract(object):
    """The register's fixed words in one language, and the patterns built from them."""

    def __init__(self, language, words):
        w = lambda k: words[k]
        self.language = language
        self.w = w
        self.sections = dict((s, w(s)) for s in SECTIONS)
        self.section_key = dict((w(s), s) for s in SECTIONS)
        self.headers = dict((s, [w(h) for h in HEADERS[s]]) for s in SECTIONS)
        self.source_rows = [w(r) for r in SOURCE_ROWS]
        self.source_key = dict(zip(self.source_rows, SOURCE_ROWS))
        self.tally_rows = [w(r) for r in TALLY_ROWS]
        self.tally_key = dict(zip(self.tally_rows, TALLY_ROWS))
        self.nis = w(NIS)
        self.no_refs = w(NO_REFS)
        self.none, self.pasted = w("none"), w("pasted")
        self.control, self.intention = w("control"), w("intention")
        self.attrs = [w(a) for a in ATTRS]
        self.collective, self.unspecified = w("(collective)"), w("(unspecified)")
        self.cls = {}
        for c in TIER:
            base, _, flag = c.partition(" (")
            self.cls[c] = w(base) + (" " + w("(" + flag) if flag else "")
        self.cls_key = dict((v, k) for k, v in self.cls.items())
        self.force_re = re.compile(LQ + r"(.+?)" + RQ + r" (" +
                                   "|".join(re.escape(self.cls[c]) for c in REGISTER_CLASSES) + r")")
        self.filings = dict((f, w(f)) for f in ("recommendation", "optional", "statement",
                                                "heading", OUTSIDE))
        self.filed_re = re.compile(r"(%s|%s) " % (re.escape(w("recommendation")), re.escape(w("optional")))
                                   + LQ + r"(.+?)" + RQ)
        self.filing_key = dict((v, k) for k, v in self.filings.items())
        form = w(REFUSAL_FORM)
        head, rest = form.split(" `<path>`")
        mid, end = rest.split("<languages>")
        self.refusal = head.split(":")[0] + ":"
        self.refusal_form = form
        self.joiner = " %s " % w("or")
        self.refusal_re = re.compile("^" + re.escape(head) + r"(?: `([^`\s][^`]*)`)?" + re.escape(mid) +
                                     r"(%s(?:(?:, |%s)%s)*)" % (LANGUAGE_NAME, re.escape(self.joiner),
                                                                LANGUAGE_NAME) + re.escape(end) + "$")
        self.names = words

    def show_status(self, t):
        return self.control if not t else self.intention + ": " + ", ".join(self.w(a) for a in t)

    def show_filed(self, f):
        if f is None:
            return "?"
        return self.filings[f[0]] if f[1] is None else "%s %s%s%s" % (self.filings[f[0]], LQ, f[1], RQ)


def ends_in_crowd(phrase):
    if any(phrase == c or phrase.endswith(" " + c) for c in LEX.collective):
        return True
    # a compound whose last part is a crowd: «Verwaltungsmitarbeitende»
    last = phrase.split(" ")[-1] if phrase else ""
    return LEX.compounds and any(" " not in c and last.endswith(c) for c in LEX.collective)


def owner_head(text):
    """The Owner quotation cut before its first cut word, and before a word with a
    participle ending (English: -ing) that directly follows a crowd entry."""
    kept = []
    for tok in norm(text).lower().split():
        bare = re.sub(r"^\W+|\W+$", "", tok)
        if bare in LEX.cut_words and kept:
            break
        if LEX.participle_endings and bare.endswith(LEX.participle_endings) and kept \
                and ends_in_crowd(" ".join(kept)):
            break
        if bare:
            kept.append(bare)
    return " ".join(kept)


def is_collective(text):
    return ends_in_crowd(owner_head(text))


def has_timing(text):
    t = norm(text)
    if LEX.vague_re:
        t = LEX.vague_re.sub(" ", t)
    if LEX.digit and DIGITS.search(t):
        return True
    return bool(LEX.timing_re and LEX.timing_re.search(t))


CLAUSE_BOUND = re.compile(r"[,;:]|[.!?](?=[\"')\]]*(?:\s|$))")
WORD_TOKEN = re.compile(r"[^\W\d_][\w\u2011-]*")


def clause_marks(text):
    """The marks that bound a clause, as the lexicon's Clauses defines them: a comma, semicolon,
    colon or sentence end, except the full stop of an abbreviation of the lexicon («z. B.») and a
    comma with one capitalised word between it and the next comma or joining word («Vertraulichkeit,
    Informationssicherheit und Datenschutz»), which joins a list of nouns. Only the German lexicon's
    negation and «zu» infinitive look inside clauses; English never calls this."""
    skip = set()
    if LEX.abbrev_re:
        for m in LEX.abbrev_re.finditer(text):
            skip.update(range(m.start(), m.end()))
    return [m for m in CLAUSE_BOUND.finditer(text) if m.start() not in skip
            and not (LEX.list_comma_re and LEX.list_comma_re.match(text, m.start()))]


def clause_of(text, start, end):
    """The bounds of the clause holding text[start:end]: from the last mark of clause_marks
    before it to the first after it."""
    left, right = 0, len(text)
    for m in clause_marks(text):
        if m.end() <= start:
            left = m.end()
        elif m.start() >= end:
            right = m.start()
            break
    return left, right


def negated(text, start, end, verb=None):
    """True when a negation word of the lexicon negates text[start:end] in its clause. verb is the
    finite verb's span (default: the term's own). A word the lexicon marks 'before the verb' counts
    anywhere in the clause («Keine Daten dürfen …»); any other only after the verb, or anywhere
    when the verb closes the clause («… nicht übernommen werden dürfen»), so that «nicht
    zugängliche Daten … können» negates the adjective, not the modal."""
    if not LEX.negation_re:
        return False
    a, b = clause_of(text, start, end)
    vs, ve = verb or (start, end)
    closes = not WORD_TOKEN.search(text, ve, b)
    for m in LEX.negation_re.finditer(text, a, b):
        if start <= m.start() < end:
            continue
        if m.start() >= ve or closes or norm(m.group(0)).lower() in LEX.neg_anywhere:
            return True
    return False


def scan_terms(text):
    """Force terms in text: (start, end, term, (class, filed in, forced)). Lexicon terms match
    longest first, each character used once; a term with a Negated class takes it when a negation
    word stands in its clause, and one negated to 'none' is no term. An infinitive with «zu» that
    the lexicon declares counts too."""
    hits = []
    for m in LEX.term_re.finditer(text):
        term = norm(m.group(0)).lower()
        entry = LEX.terms[term]
        if term in LEX.negated and negated(text, m.start(), m.end()):
            entry = LEX.negated[term]
            if entry == "none":
                continue
        hits.append((m.start(), m.end(), term, entry))
    if LEX.zu_entry:
        hits += zu_infinitives(text)
        hits.sort()
    return hits


def zu_infinitives(text):
    """Infinitives with «zu» in a clause that holds a carrier («ist», «sind», «hat», «haben»):
    «zu prüfen», or «zu» inside a separable verb («anzupassen»). One counts where it closes the
    clause, stands right before the carrier that closes it or before a joining word, or opens the
    clause («Zu berücksichtigen sind»)."""
    out = []
    bounds = [0] + [m.end() for m in clause_marks(text)] + [len(text)]
    for a, b in zip(bounds, bounds[1:]):
        toks = [(m.start(), m.end(), m.group(0)) for m in WORD_TOKEN.finditer(text, a, b)]
        low = [t[2].lower() for t in toks]
        if not any(w in LEX.carriers for w in low):
            continue
        n = len(toks)
        for i, (s, e, w) in enumerate(toks):
            if low[i] == "zu" and i + 1 < n:
                inf = toks[i + 1][2]
                if not (inf[0].islower() and inf.endswith(LEX.inf_endings)) or inf.lower() in LEX.cut_words:
                    continue
                first, last, span = i, i + 1, (s, toks[i + 1][1])
            elif re.match(r"^[a-z\u00df-\u00ff]{2,}zu[a-z\u00df-\u00ff]{2,}$", w) and w.endswith(LEX.inf_endings):
                first, last, span = i, i, (s, e)
            else:
                continue
            closes = last == n - 1 or (last == n - 2 and low[n - 1] in LEX.carriers)
            joined = last + 1 < n and low[last + 1] in LEX.joiners
            if closes or joined or first == 0:
                entry = LEX.zu_entry
                carrier = next(t for t, w in zip(toks, low) if w in LEX.carriers)
                if LEX.zu_negated and negated(text, span[0], span[1], carrier[:2]):
                    entry = LEX.zu_negated
                if entry != "none":
                    out.append((span[0], span[1], norm(text[span[0]:span[1]]).lower(), entry))
    return out


def present_verbs(text, starts):
    """(start, end, verb, class) for each sentence that opens with an actor of the lexicon and a
    verb in the present tense: «Die Angestellten prüfen …». The class is the lexicon's, or its
    Negated class when a negation word stands in the verb's clause."""
    if not LEX.present_entry:
        return []
    sent, _ = openings(text, starts)
    out = []
    for p in sorted(sent):
        m = LEX.present_re.match(text, p)
        if not m:
            continue
        verb = m.group("verb")
        if verb in LEX.not_verbs or verb in LEX.cut_words or verb in LEX.joiners:
            continue
        cls = LEX.present_entry[0]
        if LEX.present_negated and LEX.present_negated != "none" and negated(text, m.start("verb"), m.end("verb")):
            cls = LEX.present_negated[0]
        out.append((m.start("verb"), m.end("verb"), verb, cls))
    return out


def binding_terms(hits):
    """The hits that bind or permit: every class but WILL and WILL NOT, which German also writes as
    the passive's auxiliary."""
    return [h for h in hits if h[3][0] not in ("WILL", "WILL NOT")]


def openings(text, starts):
    """Offsets where a first word begins: (sentence openings, clause openings).
    A sentence opens at a quotation's start or after . : ? ! and any list markers;
    a clause opens after , ; : with at most one joining word from the lexicon."""
    sent = set()
    for p in list(starts) + [m.end() for m in SENT_END.finditer(text)]:
        while p < len(text) and text[p].isspace():
            p += 1
        sent.add(p)
        for _ in range(3):
            m = MARKER.match(text, p)
            if not m or m.end() == p:
                m = next((x for x in (r.match(text, p) for r in LEX.markers_extra) if x), None)
            if not m or m.end() == p:
                break
            p = m.end()
            sent.add(p)
    clause = set()
    for m in CLAUSE_START.finditer(text):
        clause.add(m.end())
        j = LEX.joiner_re and LEX.joiner_re.match(text, m.end())
        if j:
            clause.add(j.end())
    return sent, clause


def ends_in_question(text, pos):
    m = CLAUSE_END.search(text, pos)
    return m is not None and m.group(0) == "?"


def phrase_starts(text, phrase):
    pat = r"(?<!\w)" + r"\s+".join(re.escape(w) for w in phrase.split()) + r"(?!\w)"
    return [m.start() for m in re.finditer(pat, text, re.IGNORECASE)]


# ---------------------------------------------------------------- register parsing

class Quote(object):
    def __init__(self, m):
        self.raw = m.group(1)
        self.norm = norm(unescape(self.raw))
        self.start = int(m.group(2))
        self.end = int(m.group(3)) if m.group(3) else self.start
        self.written = m.group(0)

    def key(self):
        return (self.start, self.end, self.norm)

    def show(self):
        ref = self.written[self.written.rindex(RQ) + 2:]
        return LQ + clip(self.raw, 60) + RQ + " " + ref


class Cell(object):
    """A quotation cell: ok, nis (not in source), quotes, flag (suffix present)."""

    def __init__(self, text):
        self.text = text
        self.ok = False
        self.nis = False
        self.flag = False
        self.quotes = [Quote(m) for m in QRE.finditer(text)]


def parse_cell(text, allow_nis, suffix, where, errs):
    c = Cell(text)
    if text == C.nis:
        if allow_nis:
            c.ok = c.nis = True
        else:
            errs.append("%s: needs quotation(s), not '%s'" % (where, C.nis))
        return c
    if text == "" or text.lower().rstrip(" .") == C.nis.lower() or text.lower().startswith(C.nis.lower()):
        errs.append("%s: an empty field is written exactly '%s', found '%s'"
                    % (where, C.nis, clip(text, 40)))
        return c
    body = text
    if suffix and text.endswith(" " + suffix):
        body = text[:-len(suffix) - 1]
        c.flag = True
    quotes = []
    pos = 0
    while True:
        m = QRE.match(body, pos)
        if not m:
            break
        quotes.append(Quote(m))
        pos = m.end()
        if body.startswith(" + ", pos) and QRE.match(body, pos + 3):
            pos += 3
            continue
        break
    if not quotes or pos != len(body):
        stray = body[pos:] if quotes else body
        allowed = (", optionally followed by ' %s'" % suffix) if suffix else ""
        errs.append("%s: must be quotation(s) joined by ' + '%s; stray text '%s'"
                    % (where, allowed, clip(stray, 40)))
        c.flag = False
        return c
    for q in quotes:
        if not q.norm.strip():
            errs.append("%s: empty quotation %s" % (where, q.show()))
            return c
    c.quotes = quotes
    c.ok = True
    return c


def split_row(line):
    """Split a table row on '|' outside quotations; report raw '|' inside one."""
    s = line.strip()
    cells = []
    cur = []
    depth = 0
    raw_pipe = False
    i = 1
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("\\|")
            i += 2
            continue
        if ch == LQ:
            depth += 1
        elif ch == RQ and depth:
            depth -= 1
        if ch == "|":
            if depth:
                raw_pipe = True
                cur.append("\\|")
            else:
                cells.append("".join(cur).strip())
                cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    tail = "".join(cur).strip()
    if tail:
        cells.append(tail)
    return cells, raw_pipe


class Table(object):
    def __init__(self, name):
        self.name = name
        self.rows = []  # (line number, cells or None)


def read_section(name, content, errs):
    """Return (table or None, lines holding the literal no-references line)."""
    blocks = []
    cur = None
    literal = []
    in_comment = False
    for ln, text in content:
        s = text.strip()
        if in_comment:
            in_comment = "-->" not in s
            cur = None
            continue
        if s.startswith("<!--"):
            in_comment = "-->" not in s
            cur = None
            continue
        if s.startswith("|"):
            if cur is None:
                cur = []
                blocks.append(cur)
            cur.append((ln, text))
            continue
        cur = None
        if not s or RULE_LINE.match(s):
            continue
        if name == "Referred elsewhere" and s == C.no_refs:
            literal.append(ln)
            continue
        errs.append("%s, line %d: text outside the table: '%s'" % (C.w(name), ln, clip(s, 50)))
    if not blocks:
        return None, literal
    if len(blocks) > 1:
        errs.append("%s, line %d: a second table; a section holds one" % (C.w(name), blocks[1][0][0]))
    block = blocks[0]
    want = C.headers[name]
    name = C.w(name)
    table = Table(name)
    hln, htext = block[0]
    hcells, _ = split_row(htext)
    if hcells != want:
        errs.append("%s, line %d: header must be '| %s |'" % (name, hln, " | ".join(want)))
    rest = block[1:]
    if rest and SEPARATOR.match(rest[0][1].strip()):
        if len(split_row(rest[0][1])[0]) != len(want):
            errs.append("%s, line %d: separator row has the wrong number of columns"
                        % (name, rest[0][0]))
        rest = rest[1:]
    else:
        errs.append("%s, line %d: header is not followed by a separator row" % (name, hln))
    for ln, text in rest:
        cells, raw_pipe = split_row(text)
        if raw_pipe:
            errs.append("%s, line %d: a '|' inside a quotation must be written '\\|'" % (name, ln))
        if len(cells) != len(want):
            errs.append("%s, line %d: %d cells, expected %d" % (name, ln, len(cells), len(want)))
            table.rows.append((ln, None, cells))
        else:
            table.rows.append((ln, cells, cells))
    return table, literal


class RRow(object):
    pass


class Register(object):
    pass


def parse_status(s):
    if s == C.control:
        return ()
    if s.startswith(C.intention + ": "):
        parts = s[len(C.intention) + 2:].split(", ")
        if all(p in C.attrs for p in parts):
            idx = [C.attrs.index(p) for p in parts]
            if idx == sorted(set(idx)):
                return tuple(ATTRS[i] for i in idx)
    return None


def status_of(owner, owner_coll, evidence, when, when_unspec):
    missing = []
    if owner.nis or owner_coll:
        missing.append("owner")
    if evidence.nis:
        missing.append("evidence")
    if when.nis or when_unspec:
        missing.append("when")
    return tuple(missing)


def show_status(t):
    return C.show_status(t)


def parse_register(lines, errs):
    reg = Register()
    reg.cov_ok = True
    reg.all_quotes = []     # (label, Quote) for trace
    reg.cov_quotes = []     # (origin, label, Quote) for coverage
    reg.input_spec = None   # ("path", p) or ("pasted", None)
    reg.policy_spans = None
    reg.title_text = ""

    sections = {}
    order = []
    cur = None
    for ln, text in lines:
        if text.startswith("## "):
            written = text[3:].strip()
            name = C.section_key.get(written)
            if name and name not in sections:
                sections[name] = []
                order.append(name)
                cur = sections[name]
            elif name:
                errs.append("%s, line %d: section appears twice" % (written, ln))
                cur = []
            else:
                errs.append("line %d: unexpected section '## %s'" % (ln, clip(written, 40)))
                cur = []
            continue
        if cur is None:
            continue
        cur.append((ln, text))
    for name in SECTIONS:
        if name not in sections:
            errs.append("%s: section '## %s' is missing" % (C.w(name), C.w(name)))
    present = [n for n in SECTIONS if n in sections]
    if order != present:
        errs.append("sections out of order: found %s; the order is %s"
                    % (", ".join(C.w(n) for n in order), ", ".join(C.w(n) for n in SECTIONS)))

    tables = {}
    for name in SECTIONS:
        if name not in sections:
            tables[name] = None
            continue
        table, literal = read_section(name, sections[name], errs)
        tables[name] = table
        if name == "Referred elsewhere":
            ref = C.w(name)
            if table is not None and literal:
                errs.append("%s, line %d: holds a table and '%s'; one or the other"
                            % (ref, literal[0], C.no_refs))
            elif table is None and len(literal) != 1:
                errs.append("%s: needs a '| %s |' table or the single line '%s'"
                            % (ref, C.w("Reference"), C.no_refs))
            elif table is not None and not table.rows:
                errs.append("%s: the table has no rows; write '%s' instead" % (ref, C.no_refs))
        elif table is None:
            errs.append("%s: no table" % C.w(name))
    for name in ("Register", "Not rules"):
        t = tables[name]
        if t is None or any(cells is None for _, cells, _ in t.rows):
            reg.cov_ok = False

    # quotations for trace, from every cell that can hold them
    for name in ("Source", "Register", "Not rules", "Referred elsewhere"):
        t = tables[name]
        if t is None:
            continue
        cols = C.headers[name]
        for k, (ln, cells, raw) in enumerate(t.rows):
            for j, cell in enumerate(raw):
                col = cols[j] if cells is not None else "cell %d" % (j + 1)
                if name == "Source" or (name == "Referred elsewhere" and cells is not None):
                    col = ""
                for m in QRE.finditer(cell):
                    reg.all_quotes.append(("%s%s, line %d" % (row_label(name, k, raw),
                                                              col and " " + col, ln),
                                           Quote(m)))

    # Source
    t = tables["Source"]
    if t is not None:
        names = [cells[0] for _, cells, _ in t.rows if cells is not None]
        if names != C.source_rows:
            errs.append("%s: rows must be %s, in that order; found %s"
                        % (C.w("Source"), ", ".join(C.source_rows), ", ".join(names) or "none"))
        for ln, cells, _ in t.rows:
            if cells is None:
                continue
            written, entry = cells
            field = C.source_key.get(written, written)
            where = "%s %s, line %d" % (C.w("Source"), written, ln)
            if field == "Policy text" and entry == C.none:
                reg.policy_spans = []
            elif field == "Policy text":
                spans, bad = [], False
                for part in entry.split(" + "):
                    m = SPAN_RE.fullmatch(part.strip())
                    if not m:
                        bad = True
                        break
                    a = int(m.group(1))
                    spans.append((a, int(m.group(2)) if m.group(2) else a))
                if bad or not spans or any(a > b for a, b in spans) or any(
                        spans[i][1] >= spans[i + 1][0] for i in range(len(spans) - 1)):
                    errs.append("%s: must be one or more line spans in order, like 'L1-L57' or "
                                "'L1-L40 + L52-L60', or '%s'; found '%s'" % (where, C.none, clip(entry, 40)))
                else:
                    reg.policy_spans = spans
            elif field == "Input":
                m = re.match(r"^`([^`\s][^`]*)`$", entry)
                if entry in (C.pasted, "`%s`" % C.pasted):
                    reg.input_spec = ("pasted", None)
                elif m and not os.path.isabs(m.group(1)) and not m.group(1).startswith("~"):
                    reg.input_spec = ("path", m.group(1))
                else:
                    errs.append("%s: must be a backticked relative path or '%s', found '%s'"
                                % (where, C.pasted, clip(entry, 40)))
            else:
                c = parse_cell(entry, True, None, where, errs)
                if field == "Title" and c.ok and not c.nis:
                    reg.title_text = " ".join(q.norm for q in c.quotes)
        if not any(cells is not None and cells[0] == C.w("Input") for _, cells, _ in t.rows):
            errs.append("%s: the %s row is missing" % (C.w("Source"), C.w("Input")))

    # Register
    reg.rrows = []
    t = tables["Register"]
    prev = None
    if t is not None:
        for k, (ln, cells, raw) in enumerate(t.rows):
            r = RRow()
            r.ln = ln
            r.label = "%s, line %d" % (row_label("Register", k, raw), ln)
            r.ok = cells is not None
            reg.rrows.append(r)
            if not r.ok:
                continue
            rid, rule, force, addr, owner, ev, when, status = cells
            if rid != "R%d" % (k + 1):
                errs.append("%s: ID must be R%d, found '%s'" % (r.label, k + 1, clip(rid, 12)))
            r.rule = parse_cell(rule, False, None, r.label + " " + C.w("Rule"), errs)
            if not r.rule.ok:
                reg.cov_ok = False
            else:
                last = r.rule.quotes[-1].end
                if prev is not None and last < prev[1]:
                    errs.append("%s: its rule ends on L%d, before %s's L%d; rows run in input order"
                                % (r.label, last, prev[0], prev[1]))
                prev = (rid, last)
                for i, q in enumerate(r.rule.quotes):
                    reg.cov_quotes.append((lead_origin("register", r.rule.quotes, i), rid, q))
            m = C.force_re.fullmatch(force)
            if m and m.group(1).strip():
                r.force = (m.group(1), C.cls_key[m.group(2)])
            else:
                r.force = None
                errs.append("%s %s: must be %sterm%s CLASS, CLASS one of %s; found '%s'"
                            % (r.label, C.w("Force"), LQ, RQ,
                               ", ".join(C.cls[c] for c in REGISTER_CLASSES), clip(force, 40)))
            col = lambda n: " " + C.w(n)
            r.addr = parse_cell(addr, True, None, r.label + col("Addressee"), errs)
            r.owner = parse_cell(owner, True, C.collective, r.label + col("Owner"), errs)
            r.evidence = parse_cell(ev, True, None, r.label + col("Evidence"), errs)
            r.when = parse_cell(when, True, C.unspecified, r.label + col("When"), errs)
            r.status = parse_status(status)
            if r.status is None:
                errs.append("%s %s: must be '%s' or '%s: ' with %s in that order; found '%s'"
                            % (r.label, C.w("Status"), C.control, C.intention, ", ".join(C.attrs),
                               clip(status, 40)))

    # Not rules
    reg.nrows = []
    t = tables["Not rules"]
    if t is not None:
        for k, (ln, cells, raw) in enumerate(t.rows):
            r = RRow()
            r.label = "%s, line %d" % (row_label("Not rules", k, raw), ln)
            r.ok = cells is not None
            reg.nrows.append(r)
            if not r.ok:
                continue
            text, filed = cells
            r.text = parse_cell(text, False, None, r.label + " " + C.w("Text"), errs)
            if not r.text.ok:
                reg.cov_ok = False
            else:
                for i, q in enumerate(r.text.quotes):
                    reg.cov_quotes.append((lead_origin("notrules", r.text.quotes, i),
                                           "%s row %d" % (C.w("Not rules"), k + 1), q))
            m = C.filed_re.fullmatch(filed)
            f = C.filings
            if C.filing_key.get(filed) in ("statement", "heading", OUTSIDE):
                r.filed = (C.filing_key[filed], None)
            elif m and m.group(2).strip():
                r.filed = (C.filing_key[m.group(1)], m.group(2))
            else:
                r.filed = None
                errs.append("%s %s: must be '%s %st%s', '%s %st%s', "
                            "'%s', '%s' or '%s'; found '%s'"
                            % (r.label, C.w("Filed as"), f["recommendation"], LQ, RQ, f["optional"], LQ,
                               RQ, f["statement"], f["heading"], f[OUTSIDE], clip(filed, 40)))

    # Referred elsewhere
    t = tables["Referred elsewhere"]
    if t is not None:
        for k, (ln, cells, raw) in enumerate(t.rows):
            if cells is None:
                continue
            where = "%s, line %d" % (row_label("Referred elsewhere", k, raw), ln)
            c = parse_cell(cells[0], False, None, where, errs)
            if c.ok and len(c.quotes) != 1:
                errs.append("%s: one quotation per row" % where)

    # Tally
    reg.tally = {}
    t = tables["Tally"]
    if t is not None:
        names = [cells[0] for _, cells, _ in t.rows if cells is not None]
        if names != C.tally_rows:
            errs.append("%s: rows must be %s, in that order; found %s"
                        % (C.w("Tally"), "; ".join(C.tally_rows), "; ".join(names) or "none"))
        for ln, cells, _ in t.rows:
            if cells is None:
                continue
            key = C.tally_key.get(cells[0])
            if not re.match(r"^\d+$", cells[1]):
                errs.append("%s %s, line %d: value must be a whole number, found '%s'"
                            % (C.w("Tally"), cells[0], ln, clip(cells[1], 20)))
            elif key and key not in reg.tally:
                reg.tally[key] = (ln, int(cells[1]))
    reg.n_rules = len(t_rows(tables["Register"]))
    reg.n_not = len(t_rows(tables["Not rules"]))
    reg.has_register = tables["Register"] is not None
    reg.has_not = tables["Not rules"] is not None
    return reg


def lead_origin(origin, quotes, i):
    """A lead-in quoted before its item is told apart: a list may file some items as rules and
    others not, so its lead-in stands in both sections, and only its items must not."""
    if i < len(quotes) - 1 and quotes[i].norm.rstrip().endswith(":"):
        return origin + " lead-in"
    return origin


def t_rows(table):
    return table.rows if table is not None else []


def row_label(section, k, raw):
    if section == "Register":
        rid = raw[0] if raw else ""
        return rid if re.match(r"^R\d+$", rid) else "Register row %d" % (k + 1)
    if section == "Source" and raw and raw[0] in C.source_rows:
        return C.w("Source") + " " + raw[0]
    return "%s row %d" % (C.w(section), k + 1)


def src(field):
    """A Source row's label in the register's language: «Source Input»."""
    return C.w("Source") + " " + C.w(field)


# ---------------------------------------------------------------- input

def input_candidates(named):
    """Where a Source Input path may point: the working directory first, then the repository, then
    tests/noisy/, where the inputs of the adversarial runs keep the names their sessions knew."""
    return [os.path.join(os.getcwd(), named), os.path.join(ROOT, named),
            os.path.join(ROOT, "tests", "noisy", named)]


def resolve_input(named):
    cands = input_candidates(named)
    return next((p for p in cands if os.path.isfile(p)), cands[1])



def load_input(path):
    with open(path, encoding="utf-8-sig") as fh:
        lines = fh.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return [l.rstrip("\r") for l in lines]


def joined_range(lines, start, end):
    """Lines start..end joined and normalised, with each character's (line, col)."""
    out = []
    pos = []
    space = False
    for ln in range(start, end + 1):
        if ln > start and not space:
            out.append(" ")
            pos.append(None)
            space = True
        for col, ch in enumerate(lines[ln - 1]):
            if ch.isspace():
                if space:
                    continue
                out.append(" ")
                space = True
            else:
                out.append(QUOTE_MAP.get(ch, ch))
                space = False
            pos.append((ln, col))
    return "".join(out), pos


def find_all(hay, needle):
    found = []
    i = hay.find(needle)
    while i >= 0:
        found.append(i)
        i = hay.find(needle, i + 1)
    return found


def locate(lines, q):
    """Where q sits in its cited range: (positions per character, all occurrences,
    occurrences that start on the first cited line and end on the last)."""
    hay, pos = joined_range(lines, q.start, q.end)
    occ = find_all(hay, q.norm)
    tight = []
    for i in occ:
        span = [p for p in pos[i:i + len(q.norm)]
                if p is not None and not lines[p[0] - 1][p[1]].isspace()]
        if span and span[0][0] == q.start and span[-1][0] == q.end:
            tight.append(i)
    return pos, occ, tight


# ---------------------------------------------------------------- gates

class Result(object):
    def __init__(self, gates=GATES):
        self.gates = gates
        self.errors = dict((g, []) for g in gates)
        self.skip = {}
        self.input_shown = "?"

    def failing(self):
        return [g for g in self.gates if self.errors[g]]

    def passed(self):
        return not self.failing() and not self.skip


def check_register(lines, input_override=None):
    if any(refusal_language(text) for _, text in lines):
        return check_refusal(lines, input_override)
    select_language(lines)
    res = Result()
    err = res.errors
    reg = parse_register(lines, err["shape"])

    # which input
    input_path = None
    if reg.input_spec and reg.input_spec[0] == "path":
        res.input_shown = reg.input_spec[1]
    elif reg.input_spec:
        res.input_shown = "pasted"
    if input_override:
        input_path = input_override
        res.input_shown = shown_path(input_override)
        if reg.input_spec and reg.input_spec[0] == "path":
            want = os.path.realpath(input_override)
            if not any(os.path.realpath(p) == want for p in input_candidates(reg.input_spec[1])):
                err["shape"].append("%s: names %s, but --input is %s"
                                    % (src("Input"), reg.input_spec[1], res.input_shown))
    elif reg.input_spec and reg.input_spec[0] == "path":
        input_path = resolve_input(reg.input_spec[1])
    lines_in = None
    if input_path is not None:
        try:
            lines_in = load_input(input_path)
        except (OSError, UnicodeDecodeError) as e:
            err["trace"].append("%s: cannot read %s (%s)"
                                % (src("Input"), res.input_shown, e.__class__.__name__))
    elif reg.input_spec and reg.input_spec[0] == "pasted":
        err["trace"].append("%s: the input is '%s'; give its text with --input" % (src("Input"), C.pasted))
    else:
        res.skip["trace"] = "no Input row to check against"

    traced = {}
    if lines_in is not None:
        gate_language(lines_in, err["language"])
        gate_trace(reg, lines_in, err["trace"], traced)
    else:
        res.skip["language"] = "no input"
    gate_force(reg, err["force"])
    computed = gate_flags(reg, err["flags"])
    gate_status(reg, computed, err["status"])
    gate_tally(reg, computed, err["tally"])

    if lines_in is None:
        res.skip["coverage"] = "no input"
    elif not reg.cov_ok:
        res.skip["coverage"] = "shape errors leave the quotations incomplete"
    elif any(not traced.get(q.key(), False) for _, _, q in reg.cov_quotes):
        res.skip["coverage"] = "a quotation coverage needs failed trace"
    else:
        gate_coverage(reg, lines_in, err["coverage"])
    gate_scope(reg, traced if lines_in is not None else None, err["scope"], lines_in)
    return res


def language_share(lines, lex=None):
    """(marker words, words) in the input, by the markers of lex (default: the register's lexicon)."""
    lex = lex or LEX
    words = WORD.findall(norm(" ".join(lines)).lower())
    return sum(1 for w in words if w in lex.markers), len(words)


def show_share(markers, words, lex=None):
    lex = lex or LEX
    return "%d of its %d words (%d%%) are %s marker words from the lexicon" % (
        markers, words, round(100.0 * markers / words), lex.language)


def in_language(lines, lex):
    markers, words = language_share(lines, lex)
    return words >= lex.fewest_words and markers >= lex.marker_share * words


def gate_language(lines, errs):
    """The input is in the lexicon's language, unless it is too short to tell."""
    markers, words = language_share(lines)
    if words < LEX.fewest_words or markers >= LEX.marker_share * words:
        return
    other = [lex for lex, _ in LEXICONS if lex is not LEX and in_language(lines, lex)]
    if other:
        errs.append("the input is not in %s: %s, below the %g%% the lexicon sets. It is in %s: "
                    "its register is written with the %s contract words of reference/register-schema.md"
                    % (LEX.language, show_share(markers, words), 100 * LEX.marker_share,
                       other[0].language, other[0].language))
        return
    errs.append("the input is not in %s: %s, below the %g%% the lexicon sets. A register of it "
                "files every sentence as a statement and finds no rules, which says nothing "
                "about the policy; it gets no register, only the refusal in rules/posture.md"
                % (LEX.language, show_share(markers, words), 100 * LEX.marker_share))


def select_language(lines):
    """Set LEX and C to the language whose section names the register's '## ' headings use most;
    on a tie, the first lexicon (English)."""
    global LEX, C
    best, count = LEXICONS[0], -1
    for lex, contract in LEXICONS:
        n = sum(1 for _, t in lines if t.startswith("## ") and t[3:].strip() in contract.section_key)
        if n > count:
            best, count = (lex, contract), n
    LEX, C = best


def refusal_language(text):
    """The (lexicon, contract) whose refusal opens text, or None."""
    return next(((lex, c) for lex, c in LEXICONS if text.startswith(c.refusal)), None)


def check_refusal(lines, input_override):
    """A file holding the one-line refusal: shape and language only."""
    res = Result(["shape", "language"])
    err = res.errors
    found = None
    global LEX, C
    for ln, text in lines:
        s = text.strip()
        if not s or (s.startswith("<!--") and s.endswith("-->")) or (
                text.startswith("# ") and not refusal_language(s[2:])):
            continue
        if found is None and refusal_language(text):
            found = (ln, text.rstrip())
            LEX, C = refusal_language(text)
            continue
        err["shape"].append("line %d: a refusal is one line and nothing else; found '%s'"
                            % (ln, clip(s, 50)))
    if found is None:
        return res
    ln, text = found
    covered = [C.w(lex.language) for lex, _ in LEXICONS]
    m = C.refusal_re.match(text)
    if not m:
        err["shape"].append("line %d: the refusal must read '%s' (no path for pasted text); found '%s'"
                            % (ln, C.refusal_form.replace("<languages>", show_languages(covered)),
                               clip(text, 60)))
        res.skip["language"] = "the refusal's form is broken"
        return res
    named, langs = m.group(1), re.split(", |" + re.escape(C.joiner), m.group(2))
    missing = [l for l in covered if l not in langs]
    if missing:
        err["language"].append("line %d: the refusal names %s, not %s, the language%s of the lexicon%s"
                               % (ln, C.joiner.join(langs), show_languages(covered),
                                  "s" if len(covered) > 1 else "", "s" if len(covered) > 1 else ""))
    res.input_shown = named or "pasted"
    if input_override:
        res.input_shown = shown_path(input_override)
        if named and not any(os.path.realpath(p) == os.path.realpath(input_override)
                             for p in input_candidates(named)):
            err["shape"].append("line %d: names %s, but --input is %s" % (ln, named, res.input_shown))
        path = input_override
    elif named:
        path = resolve_input(named)
    else:
        err["language"].append("line %d: the input is pasted; give its text with --input" % ln)
        return res
    try:
        lines_in = load_input(path)
    except (OSError, UnicodeDecodeError) as e:
        err["language"].append("cannot read the input %s (%s)" % (res.input_shown, e.__class__.__name__))
        return res
    for lex, _ in LEXICONS:
        markers, words = language_share(lines_in, lex)
        if words >= lex.fewest_words and markers >= lex.marker_share * words:
            err["language"].append("the input is in %s: %s, at least the %g%% the lexicon sets. It "
                                   "gets a register, not a refusal"
                                   % (lex.language, show_share(markers, words, lex), 100 * lex.marker_share))
    return res


def show_languages(names):
    """English, French or German: the names joined the way the refusal joins them."""
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + C.joiner + names[-1]


def gate_scope(reg, traced, errs, lines=None):
    """Addressee, Evidence and When cite only lines the row's Rule cites; the Owner cites the
    Rule's lines, a lead-in above it, or a line holding a responsibility word; everything sits
    inside the policy text except entries filed outside it, which sit outside.
    A quotation that failed trace is left to trace."""
    ok = lambda q: traced is None or traced.get(q.key(), False)
    if lines is not None:
        gate_edges(reg, ok, errs, lines)
    for r in reg.rrows:
        if not r.ok or not r.rule.ok:
            continue
        allowed = set()
        for q in r.rule.quotes:
            allowed.update(range(q.start, q.end + 1))
        first = min(q.start for q in r.rule.quotes)
        if lines is not None and r.owner.ok and not r.owner.nis:
            for q in r.owner.quotes:
                if not ok(q) or q.end > len(lines):
                    continue
                span = set(range(q.start, q.end + 1))
                if span <= allowed:
                    continue
                if all((n <= first and lines[n - 1].rstrip().endswith(":"))
                       or LEX.responsibility_re.search(norm(lines[n - 1]))
                       for n in span):
                    continue
                errs.append("%s %s: %s cites a line that is neither the Rule's own (%s), a lead-in "
                            "above it, nor a line with a responsibility word"
                            % (r.label, C.w("Owner"), q.show(), show_lines(allowed)))
        for name, c in (("Addressee", r.addr), ("Evidence", r.evidence), ("When", r.when)):
            if not c.ok or c.nis:
                continue
            for q in c.quotes:
                if traced is not None and not traced.get(q.key(), False):
                    continue
                if not set(range(q.start, q.end + 1)) <= allowed:
                    errs.append("%s %s: %s cites lines outside the Rule's (%s); only Owner may "
                                "quote another sentence"
                                % (r.label, name, q.show(), show_lines(allowed)))


def gate_edges(reg, ok, errs, lines):
    """The Policy text row: spans inside the input; every entry on its side of the edge;
    an outside block in the middle of the input opens with a seam marker."""
    if reg.policy_spans is None:
        return
    n = len(lines)
    if reg.policy_spans and reg.policy_spans[-1][1] > n:
        errs.append("%s: L%d is past the input's last line (L%d)"
                    % (src("Policy text"), reg.policy_spans[-1][1], n))
        return
    inside = set()
    for a, b in reg.policy_spans:
        inside.update(range(a, b + 1))
    outside_keys = set()
    for r in reg.nrows:
        if r.ok and r.text.ok and r.filed and r.filed[0] == OUTSIDE:
            for q in r.text.quotes:
                outside_keys.add(q.key())
                if ok(q) and set(range(q.start, q.end + 1)) & inside:
                    errs.append("%s: %s is filed %s but cites the %s"
                                % (r.label, q.show(), C.filings[OUTSIDE], C.w("Policy text")))
    for label, q in reg.all_quotes:
        if q.key() in outside_keys or not ok(q):
            continue
        if not set(range(q.start, q.end + 1)) <= inside:
            errs.append("%s: %s cites a line outside the %s" % (label, q.show(), C.w("Policy text")))
    k = 1
    while k <= n:
        if k in inside or not lines[k - 1].strip():
            k += 1
            continue
        start = k
        while k <= n and k not in inside:
            k += 1
        end = k - 1
        touches = all(not lines[j - 1].strip() for j in range(1, start)) or \
            all(not lines[j - 1].strip() for j in range(end + 1, n + 1))
        opener = norm(lines[start - 1]).lower()
        if not touches and not any(s in opener for s in LEX.seams):
            errs.append("%s: L%d-L%d lies outside it in the middle of the input, "
                        "and L%d opens with no seam marker from the lexicon" % (src("Policy text"), start, end, start))


def show_lines(lines):
    return ", ".join("L%d" % n for n in sorted(lines))


def gate_trace(reg, lines, errs, traced):
    n = len(lines)
    for label, q in reg.all_quotes:
        if q.start < 1 or q.end > n or q.start > q.end:
            why = ("its range starts after it ends" if q.start > q.end
                   else "cites a line the input does not have (it has %d)" % n)
            errs.append("%s: %s %s" % (label, q.show(), why))
            traced[q.key()] = False
            continue
        pos, occ, tight = locate(lines, q)
        traced[q.key()] = bool(tight)
        span = "L%d" % q.start if q.start == q.end else "L%d-L%d" % (q.start, q.end)
        if not occ:
            errs.append("%s: %s is not on %s, which reads: '%s'"
                        % (label, q.show(), span, clip(lines[q.start - 1].strip(), 90)))
        elif not tight:
            got = [p[0] for p in pos[occ[0]:occ[0] + len(q.norm)] if p is not None]
            real = "L%d" % got[0] if got[0] == got[-1] else "L%d-L%d" % (got[0], got[-1])
            errs.append("%s: %s sits on %s; the citation must start on its first line and end "
                        "on its last" % (label, q.show(), real))


OPENING = "(a sentence start, a list item, or after a comma, semicolon or colon)"
PRESENT = ("MUST (present)", "MUST NOT (present)")
IMPERATIVE = ("MUST (imperative)", "MUST NOT (imperative)")


def outside_policy(reg, quotes):
    """True when every quotation lies outside the Policy text: scope's business, not force's."""
    if not reg.policy_spans:
        return False
    inside = set()
    for x, y in reg.policy_spans:
        inside.update(range(x, y + 1))
    return all(not set(range(q.start, q.end + 1)) & inside for q in quotes)


def is_directive(reg):
    return bool(LEX.directive_re and LEX.directive_re.search(reg.title_text))


def gate_force(reg, errs):
    for r in reg.rrows:
        if not r.ok or not r.rule.ok or r.force is None or outside_policy(reg, r.rule.quotes):
            continue
        text, starts = join_quotes(r.rule.quotes)
        hits = scan_terms(text)
        sent, clause = openings(text, starts)
        term_written, cls = r.force
        t = norm(term_written).lower().strip()
        shown = LQ + term_written + RQ
        own = [h for h in hits if h[2] == t]
        if t in LEX.terms or own:
            fit = [h for h in own if h[3][0] == cls] or own
            lcls, filed, _ = fit[0][3] if fit else LEX.terms[t]
            at = [h[0] for h in fit]
            if not at:
                errs.append("%s: Force %s is not in the Rule text as a term of its own" % (r.label, shown))
            elif lcls != cls:
                why = "" if t not in LEX.terms or lcls == LEX.terms[t][0] else \
                    " where a negation word stands in its clause"
                errs.append("%s: Force %s has class %s in the lexicon%s, not %s"
                            % (r.label, shown, C.cls[lcls], why, C.cls[cls]))
            elif filed != "Register":
                errs.append("%s: Force %s is filed in %s by the lexicon" % (r.label, shown, filed))
            elif "(imperative)" in cls and not any(p in sent or p in clause for p in at):
                errs.append("%s: Force %s does not stand at an opening %s" % (r.label, shown, OPENING))
        elif cls in PRESENT:
            check_present(reg, r, text, starts, hits, t, cls, shown, errs)
        elif cls not in IMPERATIVE and any(x[2] == t for x in present_verbs(text, starts)):
            errs.append("%s: Force %s is the verb after an actor that opens the sentence; a rule filed by "
                        "its present tense has class %s" % (r.label, shown, C.cls["MUST (present)"]))
        elif cls != "MUST (imperative)" and not (cls == "MUST NOT (imperative)" and LEX.negation_re):
            errs.append("%s: Force %s is not a lexicon term; only a %s verb phrase "
                        "may come from outside the lexicon" % (r.label, shown, C.cls["MUST (imperative)"]))
        elif LEX.term_re.match(t):
            errs.append("%s: Force %s opens with the lexicon term %s%s%s; the Force cell quotes that term"
                        % (r.label, shown, LQ, LEX.term_re.match(t).group(0), RQ))
        else:
            at = phrase_starts(text, t)
            if not at:
                errs.append("%s: Force %s does not occur in the Rule text" % (r.label, shown))
            elif not any(p in sent or p in clause for p in at):
                errs.append("%s: Force %s does not stand at an opening %s" % (r.label, shown, OPENING))
            elif all(completes_lead_in(r.rule.quotes, starts, p) for p in at):
                errs.append("%s: Force %s opens an item whose lead-in carries its own force term; the "
                            "item completes the lead-in and takes that force" % (r.label, shown))
            elif LEX.followers and (len(t.split()) < 2 or term_written.split()[-1] not in LEX.followers):
                errs.append("%s: Force %s is no imperative of this lexicon: a verb that opens the sentence "
                            "and is followed by %s" % (r.label, shown, " or ".join(
                                LQ + f + RQ for f in sorted(LEX.followers))))
            elif LEX.negation_re:
                p = next(p for p in at if p in sent or p in clause)
                want = "MUST NOT (imperative)" if negated(text, p, p + len(t)) else "MUST (imperative)"
                if want != cls:
                    errs.append("%s: Force %s has class %s here, not %s"
                                % (r.label, shown, C.cls[want], C.cls[cls]))
        best = None
        for p, _, term, entry in hits:
            lcls, _, forced = entry
            if forced == "opening" and p not in sent and p not in clause:
                continue
            if best is None or TIER[lcls] > TIER[best[1]]:
                best = (term, lcls)
        if best and TIER[best[1]] > TIER[cls]:
            errs.append("%s: the Rule text holds %s%s%s (%s), stronger than the Force class %s"
                        % (r.label, LQ, best[0], RQ, C.cls[best[1]], C.cls[cls]))

    for r in reg.nrows:
        if not r.ok or not r.text.ok:
            continue
        text, starts = join_quotes(r.text.quotes)
        hits = scan_terms(text)
        sent, _ = openings(text, starts)
        if r.filed and r.filed[1] is not None:
            kind, term_written = r.filed
            t = norm(term_written).lower().strip()
            shown = LQ + term_written + RQ
            want = FILINGS[kind]
            kind = C.filings[kind]
            own = [h for h in hits if h[2] == t]
            classes = [h[3][0] for h in own] or ([LEX.terms[t][0]] if t in LEX.terms else [])
            if not classes:
                errs.append("%s: %s %s is not a lexicon term" % (r.label, kind, shown))
            elif not any(c in want for c in classes):
                errs.append("%s: %s %s has class %s; %s needs %s"
                            % (r.label, kind, shown, C.cls[classes[0]], kind,
                               " or ".join(C.cls[c] for c in want)))
            elif not own:
                errs.append("%s: %s %s is not in the text as a term of its own" % (r.label, kind, shown))
        if r.filed and r.filed[0] == OUTSIDE:
            continue
        caught = False
        for p, e, term, entry in hits:
            forced = entry[2]
            if forced == "yes" or (forced == "opening" and p in sent):
                if ends_in_question(text, e):
                    continue
                errs.append("%s: holds the forced term %s%s%s; its sentence is a rule, not '%s'"
                            % (r.label, LQ, text[p:e], RQ, show_filed(r.filed)))
                caught = True
                break
        if not caught and is_directive(reg) and not binding_terms(hits):
            for p, e, verb, cls in present_verbs(text, starts):
                if not ends_in_question(text, e):
                    errs.append("%s: opens with an actor and the present-tense verb %s%s%s in a directive; "
                                "its sentence is a rule of class %s, not '%s'"
                                % (r.label, LQ, text[p:e], RQ, C.cls[cls], show_filed(r.filed)))
                    break


def check_present(reg, r, text, starts, hits, t, cls, shown, errs):
    """A rule filed by the present tense: the lexicon declares it, the policy is a directive, the
    verb follows an actor that opens the sentence, and no force term stands in the sentence."""
    if not LEX.present_entry:
        errs.append("%s: Force %s has class %s, but the lexicon declares no present-tense rule"
                    % (r.label, shown, C.cls[cls]))
        return
    if not is_directive(reg):
        errs.append("%s: Force %s has class %s, which only a directive carries; the Source Title "
                    "holds none of the lexicon's directive words" % (r.label, shown, C.cls[cls]))
        return
    binding = binding_terms(hits)
    if binding:
        errs.append("%s: the Rule text holds the force term %s%s%s; a sentence with a force term is "
                    "filed by it, not by its tense" % (r.label, LQ, binding[0][2], RQ))
        return
    match = [x for x in present_verbs(text, starts) if x[2] == t]
    if not match:
        errs.append("%s: Force %s is not the verb that follows an actor of the lexicon opening the "
                    "sentence" % (r.label, shown))
    elif cls not in [x[3] for x in match]:
        errs.append("%s: Force %s has class %s here, not %s"
                    % (r.label, shown, C.cls[match[0][3]], C.cls[cls]))


def completes_lead_in(quotes, starts, pos):
    """True when pos lies in a quotation that follows a lead-in holding a lexicon force term."""
    idx = max(i for i, s in enumerate(starts) if s <= pos)
    for q in quotes[:idx]:
        if q.norm.rstrip().endswith(":") and scan_terms(q.norm):
            return True
    return False


def show_filed(f):
    return C.show_filed(f)


def join_quotes(quotes):
    starts = []
    pos = 0
    for i, q in enumerate(quotes):
        if i:
            pos += 1
        starts.append(pos)
        pos += len(q.norm)
    return " ".join(q.norm for q in quotes), starts


def gate_flags(reg, errs):
    """Check the two flags; return the lexicon's flags per row for later gates."""
    computed = {}
    for r in reg.rrows:
        if not r.ok:
            continue
        coll = unspec = None
        if r.owner.ok and not r.owner.nis:
            coll = all(is_collective(q.norm) for q in r.owner.quotes)
            if coll and not r.owner.flag:
                errs.append("%s %s: every quotation is collective; add '%s'"
                            % (r.label, C.w("Owner"), C.collective))
            elif r.owner.flag and not coll:
                odd = [q for q in r.owner.quotes if not is_collective(q.norm)][0]
                errs.append("%s %s: '%s' set, but the head of %s ('%s') is not in "
                            "the Collective list" % (r.label, C.w("Owner"), C.collective, odd.show(),
                                                     owner_head(odd.norm)))
        if r.when.ok and not r.when.nis:
            unspec = not any(has_timing(q.norm) for q in r.when.quotes)
            if unspec and not r.when.flag:
                errs.append("%s %s: no digit or timing word; add '%s'"
                            % (r.label, C.w("When"), C.unspecified))
            elif r.when.flag and not unspec:
                errs.append("%s %s: '%s' set, but the text holds a digit or timing word"
                            % (r.label, C.w("When"), C.unspecified))
        computed[id(r)] = (coll, unspec)
    return computed


def statuses(r, computed):
    """(status from the flags as written, status from the lexicon's flags), or None."""
    if not r.ok or not (r.owner.ok and r.evidence.ok and r.when.ok):
        return None
    coll, unspec = computed[id(r)]
    written = status_of(r.owner, r.owner.flag, r.evidence, r.when, r.when.flag)
    derived = status_of(r.owner, bool(coll), r.evidence, r.when, bool(unspec))
    return written, derived


def gate_status(reg, computed, errs):
    for r in reg.rrows:
        both = statuses(r, computed)
        if both is None or r.status is None:
            continue
        if r.status not in both:
            errs.append("%s %s: written '%s', the cells give '%s'"
                        % (r.label, C.w("Status"), show_status(r.status), show_status(both[1])))


class _Unknown(Exception):
    pass


def gate_tally(reg, computed, errs):
    """Each count is accepted when it matches the cells as written or as recomputed;
    where those differ an earlier gate has already failed."""
    rows = reg.rrows
    options = {}
    options["Rules"] = [reg.n_rules] if reg.has_register else []
    options["Not rules"] = [reg.n_not] if reg.has_not else []
    if reg.has_not and all(r.ok for r in reg.nrows):
        options["Outside the policy"] = [sum(1 for r in reg.nrows if r.filed and r.filed[0] == OUTSIDE)]
    readable = all(r.ok for r in rows)

    def count(pred):
        try:
            return sum(1 for r in rows if pred(r))
        except _Unknown:
            return None

    def need(x):
        if x is None:
            raise _Unknown()
        return x

    def cell(r, name):
        c = getattr(r, name)
        if not c.ok:
            raise _Unknown()
        return c

    if readable and reg.has_register:
        written_st = count(lambda r: need(r.status) == ())
        st = [statuses(r, computed) for r in rows]
        variants = []
        for which in (0, 1):
            if any(s is None for s in st):
                variants.append(None)
            else:
                variants.append(sum(1 for s in st if s[which] == ()))
        c_opts = [v for v in [written_st] + variants if v is not None]
        options["Controls"] = c_opts
        options["Intentions"] = [len(rows) - v for v in c_opts]
        options["Evidence named"] = [v for v in [count(lambda r: not cell(r, "evidence").nis)]
                                     if v is not None]
        options["Owner named, not collective"] = [v for v in [
            count(lambda r: not cell(r, "owner").nis and not r.owner.flag),
            count(lambda r: not cell(r, "owner").nis and not computed[id(r)][0])] if v is not None]
        options["When named, not unspecified"] = [v for v in [
            count(lambda r: not cell(r, "when").nis and not r.when.flag),
            count(lambda r: not cell(r, "when").nis and not computed[id(r)][1])] if v is not None]
    for name in TALLY_ROWS:
        if name not in reg.tally or not options.get(name):
            continue
        ln, value = reg.tally[name]
        if value not in options[name]:
            errs.append("%s %s, line %d: written %d, the register gives %d"
                        % (C.w("Tally"), C.w(name), ln, value, options[name][-1]))


def gate_coverage(reg, lines, errs):
    cov = {"register": {}, "notrules": {}, "register lead-in": {}, "notrules lead-in": {}}
    for origin, label, q in reg.cov_quotes:
        pos, _, occ = locate(lines, q)
        if not occ:
            continue
        chosen = occ[0]
        for i in occ:
            alnum = [p for p in pos[i:i + len(q.norm)]
                     if p is not None and lines[p[0] - 1][p[1]].isalnum()]
            if not all(p in cov[origin] for p in alnum):
                chosen = i
                break
        for p in pos[chosen:chosen + len(q.norm)]:
            if p is not None and p not in cov[origin]:
                cov[origin][p] = label

    for ln, s in enumerate(lines, 1):
        if not s.strip():
            continue
        for a, b in runs(s, lambda col: s[col].isalnum() and not any(
                (ln, col) in cov[o] for o in cov), lambda col: s[col].isalnum()):
            errs.append("input L%d: not quoted anywhere: '%s'" % (ln, clip(s[a:b + 1])))
        for a, b in runs(s, lambda col: not s[col].isspace() and (ln, col) in cov["register"]
                         and (ln, col) in cov["notrules"], lambda col: not s[col].isspace()):
            errs.append("input L%d: quoted both by %s and by %s: '%s'"
                        % (ln, cov["register"][(ln, a)], cov["notrules"][(ln, a)], clip(s[a:b + 1])))


    gate_leadins(reg, lines, errs)


def gate_leadins(reg, lines, errs):
    """A lead-in (an entry ending in a colon) never stands alone, unless it heads subsections."""
    heads = set()
    for r in reg.nrows:
        if r.ok and r.text.ok and r.filed and r.filed[0] == "heading":
            heads.update(q.start for q in r.text.quotes)
    entries = [(r.label, r.rule, None) for r in reg.rrows if r.ok and r.rule.ok]
    entries += [(r.label, r.text, r.filed) for r in reg.nrows
                if r.ok and r.text.ok and not (r.filed and r.filed[0] == OUTSIDE)]
    for label, cell, filed in entries:
        if len(cell.quotes) != 1 or (filed and filed[0] == "heading"):
            continue
        q = cell.quotes[0]
        if not q.norm.rstrip().endswith(":"):
            continue
        nxt = q.end + 1
        while nxt <= len(lines) and not lines[nxt - 1].strip():
            nxt += 1
        if nxt in heads:
            continue
        errs.append("%s: %s is a lead-in quoted on its own; quote it with each of its items"
                    % (label, q.show()))


def runs(s, hit, counts):
    """Maximal stretches of s whose counting characters all satisfy hit."""
    out = []
    start = last = None
    for col in range(len(s)):
        if not counts(col):
            continue
        if hit(col):
            if start is None:
                start = col
            last = col
        elif start is not None:
            out.append((start, last))
            start = None
    if start is not None:
        out.append((start, last))
    return out


# ---------------------------------------------------------------- files and output

def read_lines(path):
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read()
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return [(i + 1, l.rstrip("\r")) for i, l in enumerate(lines)]


def split_examples(numbered):
    """Split a file into '# Example ' blocks: [(heading, lines)]."""
    heads = [i for i, (_, t) in enumerate(numbered) if t.startswith("# Example ")]
    out = []
    for k, i in enumerate(heads):
        j = heads[k + 1] if k + 1 < len(heads) else len(numbered)
        out.append((numbered[i][1][2:].strip(), numbered[i:j]))
    return out


def shown_path(path):
    full = os.path.abspath(path)
    if full.startswith(ROOT + os.sep):
        return os.path.relpath(full, ROOT)
    return path


def report(title, res, indent=""):
    print("%s== %s  (input: %s)" % (indent, title, res.input_shown))
    for g in res.gates:
        if g in res.skip:
            print("%s  %-9s SKIP (%s)" % (indent, g, res.skip[g]))
        elif res.errors[g]:
            errs = res.errors[g]
            print("%s  %-9s FAIL (%d)" % (indent, g, len(errs)))
            for e in errs[:SHOWN]:
                print("%s      %s" % (indent, e))
            if len(errs) > SHOWN:
                print("%s      ... and %d more" % (indent, len(errs) - SHOWN))
        else:
            print("%s  %-9s PASS" % (indent, g))


def check_file(path, input_override, tally, need_examples=False):
    """Check every register in one file; add (checked, passed) to tally."""
    try:
        numbered = read_lines(path)
    except (OSError, UnicodeDecodeError) as e:
        print("%s: cannot read (%s)" % (shown_path(path), e))
        tally["problems"] += 1
        return
    blocks = split_examples(numbered)
    if need_examples and not blocks:
        print("%s: no '# Example ' headings, so no registers to check" % shown_path(path))
        tally["problems"] += 1
        return
    if blocks:
        blocks = [("%s: %s" % (shown_path(path), h), lines) for h, lines in blocks]
    else:
        blocks = [(shown_path(path), numbered)]
    for title, lines in blocks:
        res = check_register(lines, input_override)
        report(title, res)
        tally["checked"] += 1
        tally["passed"] += res.passed()


def selftest(verbose):
    """Run every fixture; return (count, caught)."""
    files = sorted(glob.glob(os.path.join(FIXTURES, "*.md")))
    print("-- fixture self-test (%s)" % shown_path(FIXTURES))
    if not files:
        print("   no fixtures found")
        return 0, 0
    caught = 0
    for path in files:
        name = os.path.basename(path)
        try:
            numbered = read_lines(path)
        except (OSError, UnicodeDecodeError) as e:
            print("   %-44s cannot read (%s)" % (name, e.__class__.__name__))
            continue
        first = numbered[0][1] if numbered else ""
        m = re.match(r"^<!--\s*expect:\s*([a-z]+)\s*-->\s*$", first)
        if not m or m.group(1) not in GATES:
            print("   %-44s NO EXPECT LINE (first line must be '<!-- expect: GATE -->')" % name)
            continue
        want = m.group(1)
        res = check_register(numbered)
        failing = res.failing()
        if failing == [want]:
            verdict = "caught"
            caught += 1
        elif not failing:
            verdict = "NOT CAUGHT"
        else:
            verdict = "WRONG GATE"
        print("   %-44s expect %-9s failing %-24s %s"
              % (name, want, ",".join(failing) or "none", verdict))
        if verbose:
            report(name, res, indent="      ")
    return len(files), caught


def main(argv=None):
    try:
        sys.stdout.reconfigure(errors="backslashreplace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(
        prog="verify.py",
        description="Check registers against reference/register-schema.md and their inputs.")
    ap.add_argument("path", nargs="?", help="a register file (or a file of '# Example ' registers)")
    ap.add_argument("--input", help="the input text the register translates (required for 'pasted')")
    ap.add_argument("--selftest", action="store_true", help="run the fixtures in tests/fixtures/ only")
    ap.add_argument("--lexicon", help="the one lexicon to apply (default: reference/lexicon*.md, "
                                      "chosen by the register's language)")
    ap.add_argument("-v", "--verbose", action="store_true", help="print each fixture's full report")
    args = ap.parse_args(argv)
    if args.selftest and args.path:
        ap.error("--selftest takes no PATH")
    if args.input and not args.path:
        ap.error("--input needs a register PATH")
    if args.input and not os.path.isfile(args.input):
        ap.error("--input file not found: %s" % args.input)

    if args.lexicon and not os.path.isfile(args.lexicon):
        ap.error("--lexicon file not found: %s" % args.lexicon)
    lexicons = [args.lexicon] if args.lexicon else find_lexicons(args.path)
    schema = find_beside(SCHEMA, "register-schema.md", args.path)

    global LEX, C
    try:
        words = load_contract(schema)
    except LexiconError as e:
        print("%s: %s" % (shown_path(schema), e))
        return 2
    for lexicon in lexicons:
        try:
            lex = load_lexicon(lexicon)
        except LexiconError as e:
            print("%s: %s" % (shown_path(lexicon), e))
            return 2
        if lex.language not in words:
            print("%s: the language %s has no column under '## Contract words' in %s"
                  % (shown_path(lexicon), lex.language, shown_path(schema)))
            return 2
        LEXICONS.append((lex, Contract(lex.language, words[lex.language])))
    LEX, C = LEXICONS[0]

    tally = {"checked": 0, "passed": 0, "problems": 0}
    fixtures = None
    if args.path:
        if not os.path.isfile(args.path):
            print("%s: not found" % args.path)
            return 2
        check_file(args.path, os.path.abspath(args.input) if args.input else None, tally)
    elif not args.selftest:
        if not os.path.isfile(EXAMPLES):
            print("examples.md: not found at the repository root")
            tally["problems"] += 1
        else:
            check_file(EXAMPLES, None, tally, need_examples=True)
        evidence = sorted(glob.glob(os.path.join(ROOT, "evidence", "*register*.md")))
        if not evidence:
            print("-- evidence/: no *register*.md files to check")
        for path in evidence + sorted(glob.glob(os.path.join(ROOT, "tests", "language", "*.md"))):
            check_file(path, None, tally)
        fixtures = selftest(args.verbose)
    else:
        fixtures = selftest(args.verbose)
        if fixtures[0] == 0:
            tally["problems"] += 1

    parts = []
    if not args.selftest:
        parts.append("registers: %d checked, %d passed" % (tally["checked"], tally["passed"]))
    if fixtures is not None:
        parts.append("fixtures: %d of %d caught in their declared gate" % (fixtures[1], fixtures[0])
                     if fixtures[0] else "fixtures: none")
    print("Summary: " + "; ".join(parts))
    ok = (tally["checked"] == tally["passed"] and not tally["problems"]
          and (fixtures is None or fixtures[0] == fixtures[1]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
