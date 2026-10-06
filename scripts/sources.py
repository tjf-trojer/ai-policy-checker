#!/usr/bin/env python3
"""Prove every shipped input and reference text against the original it was taken from.

  python3 scripts/sources.py           offline, standard library: the SHA-256 of every original,
                                       then each input in inputs/ rebuilt from its original and
                                       compared byte for byte, then each reference excerpt matched
                                       word for word, in order, against its original
  python3 scripts/sources.py --pdf     also re-extract every PDF text layer and compare it with
                                       the shipped one (needs PyMuPDF)
  python3 scripts/sources.py --fetch   also download every original again and compare hashes
                                       (needs a network; a living page may have changed since;
                                       the AI Act text has no download a script can make)

The inputs are rebuilt, so any change to a character fails. The reference excerpts are matched,
not rebuilt: their line breaks and paragraph numbers were set by hand, and the match proves that
every word of each line stands in the original in the same order. Exit status 0 only when
everything holds.
"""
import argparse
import hashlib
import html
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORIGINALS = [
    # path, sha256, url
    ("inputs/originals/uk-civil-service-guidance.govuk.json",
     "636450fa1047d6617cb308301cd86a7cbe1f6b18c1263bacb5deca1f4893fea3",
     "https://www.gov.uk/api/content/government/publications/guidance-to-civil-servants-on-use-of-generative-ai/guidance-to-civil-servants-on-use-of-generative-ai"),
    ("inputs/originals/uk-generative-ai-framework.govuk.json",
     "d57b96f4617b0810db731f54a2509c3a5fad838628b9c137499f50632081db4e",
     "https://www.gov.uk/api/content/government/publications/generative-ai-framework-for-hmg/generative-ai-framework-for-hmg-html"),
    ("inputs/originals/wikipedia-bot-policy-1371001773.parse.json",
     "ce1f3d845cd5a3c2a3ac54f6b1c745571898d880ecd1870024494190eb107c7b",
     "https://en.wikipedia.org/w/api.php?action=parse&oldid=1371001773&prop=text|revid|displaytitle&format=json&formatversion=2&disablelimitreport=1&disableeditsection=1"),
    ("inputs/originals/omb-m-25-21.pdf",
     "0aab0aa4eaeac969ed93894d3940c5dc9d0b7377048171b164a439e8b9e49813",
     "https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf"),
    ("inputs/originals/omb-m-25-21.textlayer.txt",
     "dfefba3cf6fb338910f38028e397f520d82b5e4df9d768a557bd9123bf268f7d", None),
    ("inputs/originals/zuerich-strb-2025-2281-beilage-1.pdf",
     "baea5c7cb0e36eac01ecc872d602c4e92a0d5590b92fe158016aaade736e2a11",
     "https://www.stadt-zuerich.ch/content/dam/web/de/politik-verwaltung/politik-recht/stadtratsbeschluesse/2025/08/stzh-strb-2025-2281-beilage-1.pdf"),
    ("inputs/originals/zuerich-strb-2025-2281-beilage-1.blocks.txt",
     "6328166dcdec5e9ccbccdec6b0a0fd583dc48b052d653fe80cced290fa9154be", None),
    ("inputs/originals/appenzell-ki-werkzeuge-richtlinie-v2.pdf",
     "9ab504b5b173c848319eeb28e9f072bc4c8531e13a2ad015b13515af3478a66c",
     "https://www.ai.ch/themen/staat-und-recht/digitale-verwaltung/ki-werkzeuge/dokument/verzeichnis-algorithmischer-systeme-appenzell-i-rh/download"),
    ("inputs/originals/appenzell-ki-werkzeuge-richtlinie-v2.blocks.txt",
     "ad2b189e8c0ec2163a1d9897c7485ab114ffde8019edfd43ce19edf25a316ac5", None),
    ("inputs/originals/darmstadt-regelung-generative-ki-r4.pdf",
     "78005081e141609b810c1e71410e3bd1f36d8923153e0cdef8abed26c6618f4d",
     "https://rp-darmstadt.hessen.de/sites/rp-darmstadt.hessen.de/files/2026-03/regelung_zum_umgang_mit_generativer_ki_r_4.pdf"),
    ("inputs/originals/darmstadt-regelung-generative-ki-r4.blocks.txt",
     "bb56e122f5f2ce95976256449e6f46fb1c32c533a7af94a656b1d3cbd40480c8", None),
    ("inputs/originals/darmstadt-hausverfuegung-8.pdf",
     "933febd338880bc2fb21751cae3afa4fd2e9533f0a18916081a7e1b9f10f7ad7",
     "https://rp-darmstadt.hessen.de/sites/rp-darmstadt.hessen.de/files/2026-03/hv_regelungzum_umgang_mit_generativer_ki_8.pdf"),
    ("inputs/originals/darmstadt-hausverfuegung-8.blocks.txt",
     "43e9593aeeafdfc8df4b1000e1cb5e034efe9cde3764478df41a894736220c9e", None),
    ("inputs/originals/st-gallen-leitlinien-chatgpt.pdf",
     "1ee9abb5837cf03946a68e854f7e23e449fd52187d61a8ca2c29401f3f9b9ac3",
     "https://www.sg.ch/content/dam/sgch/sicherheit/datenschutz/SK_Leitlinien_ueber_die_Verwendung_von_ChatGPT_und_aehnlichen_Systemen_in_der_Verwaltung.pdf"),
    ("inputs/originals/st-gallen-leitlinien-chatgpt.blocks.txt",
     "d512e7b29af4397c46b890c645cccdb7b33b4348e469f7dc0cd62c2ee54d42fc", None),
    ("reference/sources/originals/nist-ai-100-1.pdf",
     "7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1",
     "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf"),
    ("reference/sources/originals/nist-ai-100-1.textlayer.txt",
     "f722156af6e4d6df263002752c5f117bf5b121936852b5ef95494812f91e0a21", None),
    ("reference/sources/originals/ai-act-2024-1689-en.md",
     "c91edf73cde8635db4861327555be9cd71ff228bc43190bdbc8f5dcb96f7ffbe", None),  # EUR-Lex refuses scripted downloads
    ("reference/sources/rfc2119.txt",
     "3c2ceb7bfc84cd34720f4a5271338ab9d8280d34bdd1eb250c64306202f2ed8b",
     "https://www.rfc-editor.org/rfc/rfc2119.txt"),
]

# a .textlayer.txt is PyMuPDF's text of each page; a .blocks.txt is its text blocks with their
# positions, which the German inputs need to put margin titles and boxes where the page shows them
TEXT_LAYERS = [
    ("inputs/originals/omb-m-25-21.pdf", "inputs/originals/omb-m-25-21.textlayer.txt"),
    ("reference/sources/originals/nist-ai-100-1.pdf",
     "reference/sources/originals/nist-ai-100-1.textlayer.txt"),
] + [("inputs/originals/%s.pdf" % n, "inputs/originals/%s.blocks.txt" % n) for n in (
    "zuerich-strb-2025-2281-beilage-1", "appenzell-ki-werkzeuge-richtlinie-v2",
    "darmstadt-regelung-generative-ki-r4", "darmstadt-hausverfuegung-8", "st-gallen-leitlinien-chatgpt")]


def path(rel):
    return os.path.join(ROOT, rel)


def read(rel):
    with open(path(rel), encoding="utf-8") as f:
        return f.read()


def sha256(rel):
    h = hashlib.sha256()
    with open(path(rel), "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


# ------------------------------------------------------------------ HTML to text, as extracted

def govuk_text(body, strip_trailing):
    t = re.sub(r'<(br|/p|/li|/h[1-6])\s*/?>', '\n', body)
    t = re.sub(r'<li[^>]*>', '- ', t)
    t = re.sub(r'<h([1-6])[^>]*>', lambda m: '#' * int(m.group(1)) + ' ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    if strip_trailing:
        t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n\s*\n+', '\n\n', t)
    return t.strip() + "\n"


def wikipedia_text(h):
    h = re.sub(r'<style.*?</style>', '', h, flags=re.S)
    h = re.sub(r'<table.*?</table>', '', h, flags=re.S)
    h = re.sub(r'<div role="note".*?</div>', '', h, flags=re.S)
    h = re.sub(r'<sup[^>]*class="reference".*?</sup>', '', h, flags=re.S)
    h = re.sub(r'<span class="mw-editsection">.*?</span></span>', '', h, flags=re.S)
    t = re.sub(r'<h([1-6])[^>]*>', lambda m: '\n' + '#' * int(m.group(1)) + ' ', h)
    t = re.sub(r'</h[1-6]>', '\n', t)
    t = re.sub(r'<(br|/p|/li|/dd|/dt)\s*/?>', '\n', t)
    t = re.sub(r'<li[^>]*>', '- ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n\s*\n+', '\n\n', t)
    return t.strip() + "\n"


def one_item_per_line(lines):
    """Join a bare list marker with the text on the line after it."""
    out, pending = [], False
    for line in lines:
        if line.strip() == '-':
            pending = True
            continue
        if pending and line.strip():
            out.append('- ' + line.strip())
            pending = False
            continue
        m = re.match(r'\s+- (.*)', line)
        out.append('- ' + m.group(1).strip() if m else line.rstrip())
    return out


def tidy(lines):
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip() + '\n'


# ------------------------------------------------------------------ the inputs, rebuilt

def build_uk_guidance():
    d = json.loads(read("inputs/originals/uk-civil-service-guidance.govuk.json"))
    lines = govuk_text(d["details"]["body"], False).split('\n')
    s = next(i for i, l in enumerate(lines) if l.startswith('This guidance outlines'))
    e = next(i for i, l in enumerate(lines) if l.startswith('### Government approach'))
    head = "%s\n\n%s\n\n[...]\n\n" % (d["title"], lines[0])
    return head + tidy(one_item_per_line(lines[s:e]))


def build_uk_framework():
    d = json.loads(read("inputs/originals/uk-generative-ai-framework.govuk.json"))
    lines = govuk_text(d["details"]["body"], True).split('\n')
    s = next(i for i, l in enumerate(lines) if l.startswith('### Governance'))
    e = next((i for i in range(s + 1, len(lines)) if re.match(r'^##? ', lines[i])), len(lines))
    title = re.sub(r' \(HTML\)$', '', d["title"])
    return "%s\n\n[...]\n\n" % title + tidy(one_item_per_line(lines[s:e]))


def build_wikipedia():
    p = json.loads(read("inputs/originals/wikipedia-bot-policy-1371001773.parse.json"))["parse"]
    lines = wikipedia_text(p["text"]).split('\n')
    s = next(i for i, l in enumerate(lines) if l.startswith('## Bot usage'))
    e = next(i for i, l in enumerate(lines) if l.startswith('#### Performance'))
    kept = [l.rstrip() for l in lines[s:e] if not re.match(r'^- Shortcut', l) and l.strip() != '-']
    return "%s\n\n[...]\n\n" % p["title"] + tidy(kept)


def build_omb():
    layer = read("inputs/originals/omb-m-25-21.textlayer.txt").split('\n')
    page1 = [l.rstrip() for l in layer[:30]]
    pick = lambda start: next(l for l in page1 if l.startswith(start))
    subject = page1[page1.index('SUBJECT:') + 1]
    head = "\n".join([pick('EXECUTIVE OFFICE'), pick('OFFlCE'), pick('WASHINGTON'), pick('T HE'),
                      "", pick('April'), "", pick('M-25-21'), "", pick('MEMORANDUM FOR'), "",
                      "SUBJECT: " + subject, "", "[...]", "", ""])

    start = next(i for i, l in enumerate(layer) if l.strip() == 'IMPROVING AI GOVERNANCE') - 1
    end = next(i for i, l in enumerate(layer) if l.strip().startswith('c. Federal Governance Roles'))
    body, foot, in_foot = [], [], False
    for raw in layer[start:end]:
        s = raw.rstrip()
        if s.startswith('=====PAGE'):
            in_foot = False
            continue
        if re.match(r'^\d{1,2} $', raw) or re.match(r'^\d{1,2}$', s):
            in_foot = False
            continue
        if re.match(r'^(20|21|22|23) [A-Z]', s):
            in_foot = True
            foot.append(s)
            continue
        if in_foot:
            foot[-1] += ' ' + s.strip()
            continue
        body.append(s)

    paras, cur, marker = [], None, None
    alone = re.compile(r'^(\d{1,2}|[ivxlm1]{1,3}|v|I)\.$')
    starts = re.compile(r'^([A-J]\. |[1-5]\. |[ab]\. |For CFO Act agencies|IMPROVING AI GOVERNANCE|3\.$)')
    for line in body:
        s = line.strip()
        if not s:
            continue
        if alone.match(s) and s != '3.':
            if cur:
                paras.append(cur)
            cur, marker = None, s
            continue
        if marker:
            cur, marker = marker + ' ' + s, None
            continue
        if starts.match(s):
            if cur:
                paras.append(cur)
            cur = s
            continue
        if cur is None:
            cur = s
            continue
        cur = cur[:-1] + '-' + s if cur.endswith('\xad') else cur + ' ' + s
    if cur:
        paras.append(cur)
    if paras[0] == '3.':
        paras = [paras[0] + ' ' + paras[1]] + paras[2:]
    foot = [f.replace('\xad ', '-').replace('\xad', '-') for f in foot]
    text = '\n\n'.join(paras) + '\n\n' + '\n\n'.join(foot) + '\n'
    for a in ('3. IMPROVING AI GOVERNANCE', 'a. Agency Governance Roles and Bodies',
              'b. Agency Governance Responsibilities'):
        text = text.replace(a + ' ', a + '\n\n', 1)
    return head + text


# ------------------------------------------------------------------ the German inputs, from block layers

def blocks(rel):
    """Pages of blocks from a block layer: [[(x0, y0, x1, y1, [lines])]]."""
    pages = []
    for line in read(rel).rstrip("\n").split("\n"):
        if line.startswith("=====PAGE "):
            pages.append([])
        elif re.match(r"^@[\d.]+ [\d.]+ [\d.]+ [\d.]+$", line):
            pages[-1].append(tuple(float(v) for v in line[1:].split()) + ([],))
        else:
            pages[-1][-1][4].append(line)
    return pages


def reading_order(page, margin=None):
    """A page's blocks top to bottom; a margin title before the body block beside it."""
    return sorted(page, key=lambda b: (round(b[1]), 0 if margin and margin(b) else 1))


def unwrap(lines):
    """Join wrapped lines with a space. A line-end hyphen before a lower-case letter divides a word
    and goes with the break («ge-» + «nerativen»); before anything else it belongs to the word and
    stays, and the lines join without a space («KI-» + «Werkzeuge»)."""
    out = ""
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if out and re.search(r"[^\W\d_]-$", out):
            out = out[:-1] + s if s[0].islower() else out + s
        else:
            out = out + " " + s if out else s
    return out


def paragraphs(lines, starts, alone=None, heading=None, own=None):
    """Paragraphs from lines. A blank line ends one; a line that starts matches begins one; a line
    that own matches is one by itself; a line that alone matches (a bare number) is joined to the
    line after it, and if heading matches it, that heading takes one more line opening in lower
    case (a wrapped heading) and ends."""
    out, cur, pending, closed = [], [], None, False

    def flush():
        if cur:
            out.append(cur[0] + " " + unwrap(cur[1:]) if len(cur) > 1 and alone and alone.match(cur[0])
                       else unwrap(cur))

    for line in lines:
        s = line.strip()
        if not s:
            flush()
            cur, closed = [], False
        elif alone and alone.match(s):
            flush()
            cur, pending, closed = [], s, False
        elif pending is not None:
            cur, closed, pending = [pending, s], bool(heading and heading.match(pending)), None
        elif cur and closed and s[0].islower():
            cur.append(s)
            flush()
            cur, closed = [], False
        elif own and own.match(s):
            flush()
            cur = [s]
            flush()
            cur, closed = [], False
        elif not cur or closed or starts.match(s):
            flush()
            cur, closed = [s], False
        else:
            cur.append(s)
    flush()
    return out


SEPARATOR = re.compile(r"^ {20,}$")   # the rule above a page's footnotes
PAGE = re.compile(r"^\d[/-]\d\s*$")    # a page number: «1/3», «1-3»


def build_zuerich():
    body, notes = [], []
    for page in blocks("inputs/originals/zuerich-strb-2025-2281-beilage-1.blocks.txt"):
        art = [b for b in page if b[4] and b[4][0].startswith("Art.")]
        left, right = min(b[0] for b in art), max(b[2] for b in art)
        margin = lambda b: b[0] > right or b[2] < left
        foot = False
        for b in reading_order(page, margin):
            if b[4] and SEPARATOR.match(b[4][0]):
                foot = True
            elif margin(b):
                body += [""] + b[4] + [""]
            else:
                (notes if foot else body).extend(l for l in b[4] if not PAGE.match(l))
    paras = paragraphs(body, re.compile(r"^(Art\. \d+|\d (?=[A-ZÄÖÜ])|[a-h]\. |[A-D]\. |STRB)"),
                       re.compile(r"^[a-h]\.$"))
    return "\n\n".join(paras + paragraphs(notes, re.compile(r"^\d "))) + "\n"


def build_st_gallen():
    body, notes = [], []
    for page in blocks("inputs/originals/st-gallen-leitlinien-chatgpt.blocks.txt"):
        foot = False
        for b in reading_order(page):
            for l in b[4]:
                if SEPARATOR.match(l):
                    foot = True
                elif not PAGE.match(l):
                    (notes if foot else body).append(l)
    paras = paragraphs(body, re.compile(r"^– "), re.compile(r"^\d(\.\d)*\.?\s*$"),
                       re.compile(r"^\d(\.\d)*\s*$"), re.compile(r"^(Beispiel einer Texteingabe:|Antwort:)\s*$"))
    return "\n\n".join(paras + paragraphs(notes, re.compile(r"^$"), re.compile(r"^\d\s*$"))) + "\n"


def build_appenzell():
    number, body = None, []
    for page in blocks("inputs/originals/appenzell-ki-werkzeuge-richtlinie-v2.blocks.txt"):
        for b in reading_order(page):
            if b[1] > 780:      # the footer: the document number and the page
                number = number or b[4][0].strip()
            elif b[1] > 40:     # below the running head of pages 2 and 3
                body += b[4] + [""]
    return "\n\n".join([number] + paragraphs(body, re.compile(r"^▪"), re.compile(r"^▪\s*$"))) + "\n"


def build_darmstadt():
    body, notes = [], []
    for page in blocks("inputs/originals/darmstadt-regelung-generative-ki-r4.blocks.txt"):
        for b in reading_order(page):
            text = [l for l in b[4] if l.strip()]
            if b[1] > 720 and text and re.match(r"^\d ", text[0]):    # a footnote at the foot of the page
                notes.append(unwrap(text))
            else:
                body += b[4]
    starts = re.compile(r"^(\(\d\) |\d\. [A-ZÄÖÜ]|Präambel|gez\.|Regierungsvizepräsident|im Hause|"
                        r"Regierungspräsidium Darmstadt \.|\d+\. Oktober)")
    return "\n\n".join(paragraphs(body, starts) + notes) + "\n"


def build_darmstadt_order():
    out = []
    for b in reading_order(blocks("inputs/originals/darmstadt-hausverfuegung-8.blocks.txt")[0]):
        lines = [l.strip() for l in b[4] if l.strip()]
        if lines and lines[0].startswith("Az:"):
            out += lines[:2] + [" ".join(lines[2:])]
        elif lines:
            out.append(unwrap(lines))
    i = out.index("An alle")
    return "\n\n".join(out[:i] + [" ".join(out[i:i + 3])] + out[i + 3:]) + "\n"


INPUTS = [
    ("inputs/uk-civil-service-generative-ai-guidance.txt", build_uk_guidance),
    ("inputs/uk-generative-ai-framework-governance.txt", build_uk_framework),
    ("inputs/wikipedia-bot-policy.txt", build_wikipedia),
    ("inputs/omb-m-25-21-section-3.txt", build_omb),
    ("inputs/zuerich-ki-richtlinie.txt", build_zuerich),
    ("inputs/appenzell-ki-richtlinie.txt", build_appenzell),
    ("inputs/darmstadt-regelung-generative-ki.txt", build_darmstadt),
    ("inputs/darmstadt-hausverfuegung.txt", build_darmstadt_order),
    ("inputs/st-gallen-leitlinien-chatgpt.txt", build_st_gallen),
]


# ------------------------------------------------------------------ the reference excerpts, matched

def words(text):
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    return re.findall(r'\w+', text.lower())


def in_order(needle, hay, index):
    """True when every word of needle appears in hay, in order, near its first word."""
    if not needle:
        return True
    window = 2 * len(needle) + 60
    for start in index.get(needle[0], []):
        k, pos = 1, start + 1
        while k < len(needle) and pos < min(len(hay), start + window):
            if hay[pos] == needle[k]:
                k += 1
            pos += 1
        if k == len(needle):
            return True
    return False


EXCERPTS = [
    ("reference/sources/nist-ai-rmf-govern.txt", "reference/sources/originals/nist-ai-100-1.textlayer.txt"),
    ("reference/sources/eu-ai-act-excerpts.txt", "reference/sources/originals/ai-act-2024-1689-en.md"),
]


def match_excerpt(rel, original):
    hay = words(read(original))
    index = {}
    for i, w in enumerate(hay):
        index.setdefault(w, []).append(i)
    lines = read(rel).split('\n')
    body = lines[lines.index('----') + 1:]
    # a leading paragraph or point number was moved back to its paragraph by hand; it is not matched
    unnumbered = [re.sub(r'^(\d{1,2}\.|\([a-z]\)) ', '', line) for line in body]
    missing = [n for n, line in enumerate(unnumbered, lines.index('----') + 2)
               if line.strip() and not in_order(words(line), hay, index)]
    return len([l for l in body if l.strip()]), missing


# ------------------------------------------------------------------ run

def main(argv=None):
    ap = argparse.ArgumentParser(prog="sources.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", action="store_true", help="also re-extract the PDF text layers (needs PyMuPDF)")
    ap.add_argument("--fetch", action="store_true", help="also download every original again (needs a network)")
    args = ap.parse_args(argv)
    ok = True
    print("originals")
    for rel, want, _ in ORIGINALS:
        got = sha256(rel)
        good = got == want
        ok &= good
        print("  %s  %s" % ("ok  " if good else "FAIL", rel) + ("" if good else "  sha256 %s" % got))

    print("inputs, rebuilt from their originals")
    for rel, build in INPUTS:
        good = build() == read(rel)
        ok &= good
        print("  %s  %s" % ("ok  " if good else "FAIL", rel))

    print("reference excerpts, matched word for word")
    for rel, original in EXCERPTS:
        n, missing = match_excerpt(rel, original)
        ok &= not missing
        print("  %s  %s: %d lines%s" % ("ok  " if not missing else "FAIL", rel, n,
              "" if not missing else ", not found in order: " + ", ".join("L%d" % m for m in missing)))

    if args.pdf:
        import fitz
        print("text layers, re-extracted with PyMuPDF %s" % fitz.VersionBind)
        for pdf, layer in TEXT_LAYERS:
            doc = fitz.open(path(pdf))
            if layer.endswith(".blocks.txt"):
                text = "".join("=====PAGE %d\n" % (i + 1) + "".join(
                    "@%.1f %.1f %.1f %.1f\n%s\n" % (b[:4] + (b[4].rstrip("\n"),)) for b in p.get_text("blocks"))
                    for i, p in enumerate(doc))
            else:
                text = "\n".join("=====PAGE %d\n" % (i + 1) + p.get_text() for i, p in enumerate(doc))
            good = text == read(layer)
            ok &= good
            print("  %s  %s" % ("ok  " if good else "FAIL", layer))

    if args.fetch:
        print("originals, downloaded again")
        for rel, want, url in ORIGINALS:
            if not url:
                continue
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "ai-policy-checker sources.py"})
                data = urllib.request.urlopen(req, timeout=60).read()
                got = hashlib.sha256(data).hexdigest()
                print("  %s  %s" % ("same" if got == want else "DIFF", url))
            except Exception as e:
                print("  n/a   %s (%s)" % (url, e.__class__.__name__))

    print("RESULT: %s" % ("every original, input and excerpt holds" if ok else "something failed"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
