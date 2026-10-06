#!/usr/bin/env python3
"""Check that a register honours reference/register-schema.md against its input.

A register is the set of markdown tables a translation produces from one policy
text. Eight gates run on each register:

  shape     the five sections in order, exact table headers, cell counts, IDs,
            row order, and the form of every cell
  trace     every quotation is in the input, character for character,
            starting on the first line it cites and ending on the last
  force     force terms and classes agree with reference/lexicon.md, an
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

The word lists are read from reference/lexicon.md on every run.

What it cannot check: it proves the quotations and every field derived from
them, not that a sentence was read correctly. It cannot tell whether a quoted
owner is really answerable for that rule, whether a quoted artefact would show
the rule was met, whether a "will" is binding or descriptive, whether a "may"
grants or only describes, whether an opening word is a verb, or whether every
document the policy names is listed under Referred elsewhere.

Usage:
  python3 scripts/verify.py                       examples.md, evidence/*register*.md
                                                  and the fixture self-test
  python3 scripts/verify.py PATH.md [--input F]   one file; each "# Example " block
                                                  in it if it has any
  python3 scripts/verify.py --selftest            fixtures in tests/fixtures/ only

A Source Input path is looked up from the working directory first, then from the
repository root; --input, when given, must name the same file.

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
EXAMPLES = os.path.join(ROOT, "examples.md")
FIXTURES = os.path.join(ROOT, "tests", "fixtures")

GATES = ["shape", "trace", "force", "flags", "status", "tally", "coverage", "scope"]
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
REGISTER_CLASSES = ["MUST NOT (imperative)", "MUST (imperative)", "MUST NOT", "MUST",
                    "WILL NOT", "WILL"]
TIER = {"MUST NOT (imperative)": 3, "MUST (imperative)": 3, "MUST NOT": 3, "MUST": 3,
        "WILL NOT": 2, "WILL": 2, "SHOULD NOT": 1, "SHOULD": 1, "MAY": 0}
FILINGS = {"recommendation": ("SHOULD", "SHOULD NOT"), "optional": ("MAY",)}
ATTRS = ["owner", "evidence", "when"]

QUOTE_MAP = {"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
             "\u201c": '"', "\u201d": '"', "\u201e": '"'}

QRE = re.compile(LQ + r"(.+?)" + RQ + r" L(\d+)(?:-L(\d+))?")
FORCE_RE = re.compile(LQ + r"(.+?)" + RQ + r" (" +
                      "|".join(re.escape(c) for c in REGISTER_CLASSES) + r")")
FILED_RE = re.compile(r"(recommendation|optional) " + LQ + r"(.+?)" + RQ)
OUTSIDE = "outside the policy"
SPAN_RE = re.compile(r"L(\d+)(?:-L(\d+))?")
SEPARATOR = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
RULE_LINE = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")
SENT_END = re.compile(r"[.:?!][\"')\]]*\s+")
MARKER = re.compile(r"(?:#+\s+|[-*\u2022]\s+|\(?[A-Za-z0-9]{1,4}[.)]\s+|[\"'(\[]+)")
CLAUSE_END = re.compile(r"[.!?](?=[\"')\]]*(?:\s|$))")
CLAUSE_START = re.compile(r"[,;:][\"')\]]*\s+")
JOINER = re.compile(r"(?:and|but|or|then)\s+", re.IGNORECASE)
DIGITS = re.compile(r"(?<![^\W_])[0-9]+(?![^\W_])")

LEX = None


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
    for name in ("Force", "Collective owners", "Timing words", "Policy edges"):
        if name not in secs:
            raise LexiconError("no '## %s' section" % name)
    lex = Lexicon()

    header, body = md_table(secs["Force"], "Force", "Term")
    it, ic, ifi, ifo = [column(header, n, "Force") for n in ("Term", "Class", "Filed in", "Forced")]
    lex.terms = {}
    for row in body:
        term = row[it].strip("`").strip()
        if not term or term[0] in "_*":
            continue
        cls = row[ic]
        if cls not in TIER:
            raise LexiconError("unknown class '%s' for term '%s'" % (cls, term))
        forced = row[ifo].lower()
        if forced not in ("yes", "no", "opening"):
            raise LexiconError("unknown Forced value '%s' for term '%s'" % (row[ifo], term))
        lex.terms[norm(term).lower()] = (cls, row[ifi], forced)
    if not lex.terms:
        raise LexiconError("the Force table holds no terms")
    lex.term_re = words_re(lex.terms)

    coll = secs["Collective owners"]
    header, body = md_table(coll, "Collective owners", "Collective")
    i = column(header, "Collective", "Collective owners")
    lex.collective = [norm(r[i]).lower().strip() for r in body if r[i].strip()]
    header, body = md_table(coll, "Collective owners", "Cut word")
    i = column(header, "Cut word", "Collective owners")
    lex.cut_words = set(norm(r[i]).lower().strip() for r in body if r[i].strip())
    if not lex.collective or not lex.cut_words:
        raise LexiconError("the Collective or Cut word table under '## Collective owners' is empty")

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


def ends_in_crowd(phrase):
    return any(phrase == c or phrase.endswith(" " + c) for c in LEX.collective)


def owner_head(text):
    """The Owner quotation cut before its first cut word, and before an -ing word
    that directly follows a crowd entry."""
    kept = []
    for tok in norm(text).lower().split():
        bare = re.sub(r"^\W+|\W+$", "", tok)
        if bare in LEX.cut_words:
            break
        if bare.endswith("ing") and kept and ends_in_crowd(" ".join(kept)):
            break
        if bare:
            kept.append(bare)
    return " ".join(kept)


def is_collective(text):
    return ends_in_crowd(owner_head(text))


def has_timing(text):
    t = norm(text)
    if LEX.digit and DIGITS.search(t):
        return True
    return bool(LEX.timing_re and LEX.timing_re.search(t))


def scan_terms(text):
    """Lexicon terms in text, longest first, each character used once."""
    return [(m.start(), m.end(), norm(m.group(0)).lower()) for m in LEX.term_re.finditer(text)]


def openings(text, starts):
    """Offsets where a first word begins: (sentence openings, clause openings).
    A sentence opens at a quotation's start or after . : ? ! and any list markers;
    a clause opens after , ; : with at most one joining and, but, or, then."""
    sent = set()
    for p in list(starts) + [m.end() for m in SENT_END.finditer(text)]:
        while p < len(text) and text[p].isspace():
            p += 1
        sent.add(p)
        for _ in range(3):
            m = MARKER.match(text, p)
            if not m or m.end() == p:
                break
            p = m.end()
            sent.add(p)
    clause = set()
    for m in CLAUSE_START.finditer(text):
        clause.add(m.end())
        j = JOINER.match(text, m.end())
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
    if text == NIS:
        if allow_nis:
            c.ok = c.nis = True
        else:
            errs.append("%s: needs quotation(s), not 'not in source'" % where)
        return c
    if text == "" or text.lower().rstrip(" .") == NIS or text.lower().startswith(NIS):
        errs.append("%s: an empty field is written exactly 'not in source', found '%s'"
                    % (where, clip(text, 40)))
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
        if name == "Referred elsewhere" and s == NO_REFS:
            literal.append(ln)
            continue
        errs.append("%s, line %d: text outside the table: '%s'" % (name, ln, clip(s, 50)))
    if not blocks:
        return None, literal
    if len(blocks) > 1:
        errs.append("%s, line %d: a second table; a section holds one" % (name, blocks[1][0][0]))
    block = blocks[0]
    want = HEADERS[name]
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
    if s == "control":
        return ()
    if s.startswith("intention: "):
        parts = s[len("intention: "):].split(", ")
        if all(p in ATTRS for p in parts):
            idx = [ATTRS.index(p) for p in parts]
            if idx == sorted(set(idx)):
                return tuple(parts)
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
    return "control" if not t else "intention: " + ", ".join(t)


def parse_register(lines, errs):
    reg = Register()
    reg.cov_ok = True
    reg.all_quotes = []     # (label, Quote) for trace
    reg.cov_quotes = []     # (origin, label, Quote) for coverage
    reg.input_spec = None   # ("path", p) or ("pasted", None)
    reg.policy_spans = None

    sections = {}
    order = []
    cur = None
    for ln, text in lines:
        if text.startswith("## "):
            name = text[3:].strip()
            if name in SECTIONS and name not in sections:
                sections[name] = []
                order.append(name)
                cur = sections[name]
            elif name in SECTIONS:
                errs.append("%s, line %d: section appears twice" % (name, ln))
                cur = []
            else:
                errs.append("line %d: unexpected section '## %s'" % (ln, clip(name, 40)))
                cur = []
            continue
        if cur is None:
            continue
        cur.append((ln, text))
    for name in SECTIONS:
        if name not in sections:
            errs.append("%s: section '## %s' is missing" % (name, name))
    present = [n for n in SECTIONS if n in sections]
    if order != present:
        errs.append("sections out of order: found %s; the order is %s"
                    % (", ".join(order), ", ".join(SECTIONS)))

    tables = {}
    for name in SECTIONS:
        if name not in sections:
            tables[name] = None
            continue
        table, literal = read_section(name, sections[name], errs)
        tables[name] = table
        if name == "Referred elsewhere":
            if table is not None and literal:
                errs.append("Referred elsewhere, line %d: holds a table and '%s'; one or the other"
                            % (literal[0], NO_REFS))
            elif table is None and len(literal) != 1:
                errs.append("Referred elsewhere: needs a '| Reference |' table or the single line '%s'"
                            % NO_REFS)
            elif table is not None and not table.rows:
                errs.append("Referred elsewhere: the table has no rows; write '%s' instead" % NO_REFS)
        elif table is None:
            errs.append("%s: no table" % name)
    for name in ("Register", "Not rules"):
        t = tables[name]
        if t is None or any(cells is None for _, cells, _ in t.rows):
            reg.cov_ok = False

    # quotations for trace, from every cell that can hold them
    for name in ("Source", "Register", "Not rules", "Referred elsewhere"):
        t = tables[name]
        if t is None:
            continue
        cols = HEADERS[name]
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
        if names != SOURCE_ROWS:
            errs.append("Source: rows must be %s, in that order; found %s"
                        % (", ".join(SOURCE_ROWS), ", ".join(names) or "none"))
        for ln, cells, _ in t.rows:
            if cells is None:
                continue
            field, entry = cells
            where = "Source %s, line %d" % (field, ln)
            if field == "Policy text" and entry == "none":
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
                                "'L1-L40 + L52-L60', or 'none'; found '%s'" % (where, clip(entry, 40)))
                else:
                    reg.policy_spans = spans
            elif field == "Input":
                m = re.match(r"^`([^`\s][^`]*)`$", entry)
                if entry in ("pasted", "`pasted`"):
                    reg.input_spec = ("pasted", None)
                elif m and not os.path.isabs(m.group(1)) and not m.group(1).startswith("~"):
                    reg.input_spec = ("path", m.group(1))
                else:
                    errs.append("%s: must be a backticked relative path or 'pasted', found '%s'"
                                % (where, clip(entry, 40)))
            else:
                parse_cell(entry, True, None, where, errs)
        if not any(cells is not None and cells[0] == "Input" for _, cells, _ in t.rows):
            errs.append("Source: the Input row is missing")

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
            r.rule = parse_cell(rule, False, None, r.label + " Rule", errs)
            if not r.rule.ok:
                reg.cov_ok = False
            else:
                last = r.rule.quotes[-1].end
                if prev is not None and last < prev[1]:
                    errs.append("%s: its rule ends on L%d, before %s's L%d; rows run in input order"
                                % (r.label, last, prev[0], prev[1]))
                prev = (rid, last)
                for q in r.rule.quotes:
                    reg.cov_quotes.append(("register", rid, q))
            m = FORCE_RE.fullmatch(force)
            if m and m.group(1).strip():
                r.force = (m.group(1), m.group(2))
            else:
                r.force = None
                errs.append("%s Force: must be %sterm%s CLASS, CLASS one of %s; found '%s'"
                            % (r.label, LQ, RQ, ", ".join(REGISTER_CLASSES), clip(force, 40)))
            r.addr = parse_cell(addr, True, None, r.label + " Addressee", errs)
            r.owner = parse_cell(owner, True, "(collective)", r.label + " Owner", errs)
            r.evidence = parse_cell(ev, True, None, r.label + " Evidence", errs)
            r.when = parse_cell(when, True, "(unspecified)", r.label + " When", errs)
            r.status = parse_status(status)
            if r.status is None:
                errs.append("%s Status: must be 'control' or 'intention: ' with owner, evidence, when "
                            "in that order; found '%s'" % (r.label, clip(status, 40)))

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
            r.text = parse_cell(text, False, None, r.label + " Text", errs)
            if not r.text.ok:
                reg.cov_ok = False
            else:
                for q in r.text.quotes:
                    reg.cov_quotes.append(("notrules", "Not rules row %d" % (k + 1), q))
            m = FILED_RE.fullmatch(filed)
            if filed in ("statement", "heading", OUTSIDE):
                r.filed = (filed, None)
            elif m and m.group(2).strip():
                r.filed = (m.group(1), m.group(2))
            else:
                r.filed = None
                errs.append("%s Filed as: must be 'recommendation %st%s', 'optional %st%s', "
                            "'statement', 'heading' or '%s'; found '%s'"
                            % (r.label, LQ, RQ, LQ, RQ, OUTSIDE, clip(filed, 40)))

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
        if names != TALLY_ROWS:
            errs.append("Tally: rows must be %s, in that order; found %s"
                        % ("; ".join(TALLY_ROWS), "; ".join(names) or "none"))
        for ln, cells, _ in t.rows:
            if cells is None:
                continue
            if not re.match(r"^\d+$", cells[1]):
                errs.append("Tally %s, line %d: value must be a whole number, found '%s'"
                            % (cells[0], ln, clip(cells[1], 20)))
            elif cells[0] in TALLY_ROWS and cells[0] not in reg.tally:
                reg.tally[cells[0]] = (ln, int(cells[1]))
    reg.n_rules = len(t_rows(tables["Register"]))
    reg.n_not = len(t_rows(tables["Not rules"]))
    reg.has_register = tables["Register"] is not None
    reg.has_not = tables["Not rules"] is not None
    return reg


def t_rows(table):
    return table.rows if table is not None else []


def row_label(section, k, raw):
    if section == "Register":
        rid = raw[0] if raw else ""
        return rid if re.match(r"^R\d+$", rid) else "Register row %d" % (k + 1)
    if section == "Source" and raw and raw[0] in SOURCE_ROWS:
        return "Source " + raw[0]
    return "%s row %d" % (section, k + 1)


# ---------------------------------------------------------------- input

def input_candidates(named):
    """Where a Source Input path may point: the working directory first, then the repository."""
    return [os.path.join(os.getcwd(), named), os.path.join(ROOT, named)]


def resolve_input(named):
    cands = input_candidates(named)
    return next((p for p in cands if os.path.isfile(p)), cands[-1])


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
    def __init__(self):
        self.errors = dict((g, []) for g in GATES)
        self.skip = {}
        self.input_shown = "?"

    def failing(self):
        return [g for g in GATES if self.errors[g]]

    def passed(self):
        return not self.failing() and not self.skip


def check_register(lines, input_override=None):
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
                err["shape"].append("Source Input: names %s, but --input is %s"
                                    % (reg.input_spec[1], res.input_shown))
    elif reg.input_spec and reg.input_spec[0] == "path":
        input_path = resolve_input(reg.input_spec[1])
    lines_in = None
    if input_path is not None:
        try:
            lines_in = load_input(input_path)
        except (OSError, UnicodeDecodeError) as e:
            err["trace"].append("Source Input: cannot read %s (%s)"
                                % (res.input_shown, e.__class__.__name__))
    elif reg.input_spec and reg.input_spec[0] == "pasted":
        err["trace"].append("Source Input: the input is 'pasted'; give its text with --input")
    else:
        res.skip["trace"] = "no Input row to check against"

    traced = {}
    if lines_in is not None:
        gate_trace(reg, lines_in, err["trace"], traced)
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
                errs.append("%s Owner: %s cites a line that is neither the Rule's own (%s), a lead-in "
                            "above it, nor a line with a responsibility word"
                            % (r.label, q.show(), show_lines(allowed)))
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
        errs.append("Source Policy text: L%d is past the input's last line (L%d)"
                    % (reg.policy_spans[-1][1], n))
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
                    errs.append("%s: %s is filed outside the policy but cites the Policy text"
                                % (r.label, q.show()))
    for label, q in reg.all_quotes:
        if q.key() in outside_keys or not ok(q):
            continue
        if not set(range(q.start, q.end + 1)) <= inside:
            errs.append("%s: %s cites a line outside the Policy text" % (label, q.show()))
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
            errs.append("Source Policy text: L%d-L%d lies outside it in the middle of the input, "
                        "and L%d opens with no seam marker from the lexicon" % (start, end, start))


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


def gate_force(reg, errs):
    for r in reg.rrows:
        if not r.ok or not r.rule.ok or r.force is None:
            continue
        text, starts = join_quotes(r.rule.quotes)
        hits = scan_terms(text)
        sent, clause = openings(text, starts)
        term_written, cls = r.force
        t = norm(term_written).lower().strip()
        shown = LQ + term_written + RQ
        if t in LEX.terms:
            lcls, filed, _ = LEX.terms[t]
            at = [h[0] for h in hits if h[2] == t]
            if not at:
                errs.append("%s: Force %s is not in the Rule text as a term of its own" % (r.label, shown))
            elif lcls != cls:
                errs.append("%s: Force %s has class %s in the lexicon, not %s" % (r.label, shown, lcls, cls))
            elif filed != "Register":
                errs.append("%s: Force %s is filed in %s by the lexicon" % (r.label, shown, filed))
            elif "(imperative)" in cls and not any(p in sent or p in clause for p in at):
                errs.append("%s: Force %s does not stand at an opening (a sentence start, a list item, "
                            "or after a comma, semicolon or colon)" % (r.label, shown))
        elif cls != "MUST (imperative)":
            errs.append("%s: Force %s is not a lexicon term; only a MUST (imperative) verb phrase "
                        "may come from outside the lexicon" % (r.label, shown))
        elif LEX.term_re.match(t):
            errs.append("%s: Force %s opens with the lexicon term %s%s%s; the Force cell quotes that term"
                        % (r.label, shown, LQ, LEX.term_re.match(t).group(0), RQ))
        else:
            at = phrase_starts(text, t)
            if not at:
                errs.append("%s: Force %s does not occur in the Rule text" % (r.label, shown))
            elif not any(p in sent or p in clause for p in at):
                errs.append("%s: Force %s does not stand at an opening (a sentence start, a list item, "
                            "or after a comma, semicolon or colon)" % (r.label, shown))
            elif all(completes_lead_in(r.rule.quotes, starts, p) for p in at):
                errs.append("%s: Force %s opens an item whose lead-in carries its own force term; the "
                            "item completes the lead-in and takes that force" % (r.label, shown))
        best = None
        for p, _, term in hits:
            lcls, _, forced = LEX.terms[term]
            if forced == "opening" and p not in sent and p not in clause:
                continue
            if best is None or TIER[lcls] > TIER[best[1]]:
                best = (term, lcls)
        if best and TIER[best[1]] > TIER[cls]:
            errs.append("%s: the Rule text holds %s%s%s (%s), stronger than the Force class %s"
                        % (r.label, LQ, best[0], RQ, best[1], cls))

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
            if t not in LEX.terms:
                errs.append("%s: %s %s is not a lexicon term" % (r.label, kind, shown))
            elif LEX.terms[t][0] not in want:
                errs.append("%s: %s %s has class %s; %s needs %s"
                            % (r.label, kind, shown, LEX.terms[t][0], kind, " or ".join(want)))
            elif not any(h[2] == t for h in hits):
                errs.append("%s: %s %s is not in the text as a term of its own" % (r.label, kind, shown))
        if r.filed and r.filed[0] == OUTSIDE:
            continue
        for p, e, term in hits:
            forced = LEX.terms[term][2]
            if forced == "yes" or (forced == "opening" and p in sent):
                if ends_in_question(text, e):
                    continue
                errs.append("%s: holds the forced term %s%s%s; its sentence is a rule, not '%s'"
                            % (r.label, LQ, text[p:e], RQ, show_filed(r.filed)))
                break


def completes_lead_in(quotes, starts, pos):
    """True when pos lies in a quotation that follows a lead-in holding a lexicon force term."""
    idx = max(i for i, s in enumerate(starts) if s <= pos)
    for q in quotes[:idx]:
        if q.norm.rstrip().endswith(":") and scan_terms(q.norm):
            return True
    return False


def show_filed(f):
    if f is None:
        return "?"
    return f[0] if f[1] is None else "%s %s%s%s" % (f[0], LQ, f[1], RQ)


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
                errs.append("%s Owner: every quotation is collective; add '(collective)'" % r.label)
            elif r.owner.flag and not coll:
                odd = [q for q in r.owner.quotes if not is_collective(q.norm)][0]
                errs.append("%s Owner: '(collective)' set, but the head of %s ('%s') is not in "
                            "the Collective list" % (r.label, odd.show(), owner_head(odd.norm)))
        if r.when.ok and not r.when.nis:
            unspec = not any(has_timing(q.norm) for q in r.when.quotes)
            if unspec and not r.when.flag:
                errs.append("%s When: no digit or timing word; add '(unspecified)'" % r.label)
            elif r.when.flag and not unspec:
                errs.append("%s When: '(unspecified)' set, but the text holds a digit or timing word"
                            % r.label)
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
            errs.append("%s Status: written '%s', the cells give '%s'"
                        % (r.label, show_status(r.status), show_status(both[1])))


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
            errs.append("Tally %s, line %d: written %d, the register gives %d"
                        % (name, ln, value, options[name][-1]))


def gate_coverage(reg, lines, errs):
    cov = {"register": {}, "notrules": {}}
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
    for g in GATES:
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
    ap.add_argument("-v", "--verbose", action="store_true", help="print each fixture's full report")
    args = ap.parse_args(argv)
    if args.selftest and args.path:
        ap.error("--selftest takes no PATH")
    if args.input and not args.path:
        ap.error("--input needs a register PATH")
    if args.input and not os.path.isfile(args.input):
        ap.error("--input file not found: %s" % args.input)

    global LEX
    try:
        LEX = load_lexicon(LEXICON)
    except LexiconError as e:
        print("reference/lexicon.md: %s" % e)
        return 2

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
        for path in evidence:
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
