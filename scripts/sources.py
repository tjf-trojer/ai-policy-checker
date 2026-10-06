#!/usr/bin/env python3
"""Prove every shipped input and reference text against the original it was taken from.

  python3 scripts/sources.py           offline, standard library: the SHA-256 of every original,
                                       then each input in inputs/ rebuilt from its original and
                                       compared byte for byte, then each reference excerpt matched
                                       word for word, in order, against its original
  python3 scripts/sources.py --pdf     also re-extract the two PDF text layers and compare them
                                       with the shipped ones (needs PyMuPDF)
  python3 scripts/sources.py --fetch   also download every original again and compare hashes
                                       (needs a network; a living page may have changed since;
                                       the AI Act text has no download a script can make)

The inputs are rebuilt, so any change to a character fails. The reference excerpts are matched,
not rebuilt: their line breaks and paragraph numbers were set by hand, and the match proves that
every word of each line stands in the original in the same order. Exit status 0 only when
everything holds.
"""
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

TEXT_LAYERS = [
    ("inputs/originals/omb-m-25-21.pdf", "inputs/originals/omb-m-25-21.textlayer.txt"),
    ("reference/sources/originals/nist-ai-100-1.pdf",
     "reference/sources/originals/nist-ai-100-1.textlayer.txt"),
]


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


INPUTS = [
    ("inputs/uk-civil-service-generative-ai-guidance.txt", build_uk_guidance),
    ("inputs/uk-generative-ai-framework-governance.txt", build_uk_framework),
    ("inputs/wikipedia-bot-policy.txt", build_wikipedia),
    ("inputs/omb-m-25-21-section-3.txt", build_omb),
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

def main(argv):
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

    if "--pdf" in argv:
        import fitz
        print("text layers, re-extracted with PyMuPDF %s" % fitz.VersionBind)
        for pdf, layer in TEXT_LAYERS:
            doc = fitz.open(path(pdf))
            text = "\n".join("=====PAGE %d\n" % (i + 1) + p.get_text() for i, p in enumerate(doc))
            good = text == read(layer)
            ok &= good
            print("  %s  %s" % ("ok  " if good else "FAIL", layer))

    if "--fetch" in argv:
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
    sys.exit(main(sys.argv[1:]))
