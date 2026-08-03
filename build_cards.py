#!/usr/bin/env python3
"""
Astronomy fact cards -> print-ready PDFs

  python3 build_cards.py            # every format
  python3 build_cards.py a7         # a single format
  python3 build_cards.py a6

Single-sided. The cards run consecutively across the sheets, row by row
from the top left. The back stays empty.

Writes into ./out:
  astro-karten-A7.pdf      22 sheets, 8 cards per sheet
  astro-karten-A6.pdf      43 sheets, 4 cards per sheet
  astro-karten-index.pdf   overview for looking things up quickly

Data lives in facts.json, layout in cards.css.
After rendering, the script measures every card and shrinks the text as
far as needed so that nothing gets cut off.

Note on language: identifiers and comments are English, but everything the
cards and the console say stays German - the cards are read aloud to German
visitors, and the printed text is the product.
"""

import json
import sys
import pathlib
import html as htmlmod
from playwright.sync_api import sync_playwright

import fonts

BASE = pathlib.Path(__file__).parent
OUT = BASE / "out"
OUT.mkdir(exist_ok=True)

# Print the extra paragraph ("Mehr dazu") at the bottom of the card.
# Set to False for the plain fact only - the text then gets noticeably
# larger.
WITH_MORE = True

# Print cutting lines and registration marks on the sheets.
# Set to False if the sheets are needed without any guide lines - but then
# nothing is left to align the cut against.
CUT_LINES = True

# Duplex mode: the front shows only theme and title, the fact is on the
# back. Sheets alternate (front, back, ...) and the back sheets are
# mirrored for flipping along the long edge.
DUPLEX = False

data = json.loads((BASE / "facts.json").read_text(encoding="utf-8"))
CSS = (BASE / "cards.css").read_text(encoding="utf-8")
THEMES = data["themes"]
CARDS = data["cards"]
FOOTER = data["meta"].get("footer", "Faktenkarte")

# Format definition: cards per sheet, columns, cutting lines in mm,
# minimum font sizes for the auto-fit
FORMATS = {
    "a6": {"per_sheet": 4, "columns": 2, "landscape": False,
           "vlines": [105.0], "hlines": [148.5],
           "title_long": 30, "minText": 11.0, "maxText": 21.0, "minTitle": 14.0,
           "minFront": 15.0, "maxFront": 34.0},
    "a6q": {"per_sheet": 4, "columns": 2, "landscape": True,
            "vlines": [148.5], "hlines": [105.0],
            "title_long": 34, "minText": 11.0, "maxText": 20.0, "minTitle": 14.0,
            "minFront": 15.0, "maxFront": 32.0},
    "a7": {"per_sheet": 8, "columns": 2, "landscape": False,
           "vlines": [105.0], "hlines": [74.25, 148.5, 222.75],
           "title_long": 26, "minText": 7.5, "maxText": 14.0, "minTitle": 9.0,
           "minFront": 10.0, "maxFront": 22.0},
}


def esc(s: str) -> str:
    """Escapes everything except the permitted <sup> tags."""
    s = htmlmod.escape(s, quote=False)
    return s.replace("&lt;sup&gt;", "<sup>").replace("&lt;/sup&gt;", "</sup>")


def plain_len(s: str) -> int:
    return len(s.replace("<sup>", "").replace("</sup>", ""))


def level(text: str) -> str:
    n = plain_len(text)
    return "s1" if n < 170 else "s2" if n < 215 else "s3" if n < 265 else "s4"


def theme_label(t: str) -> str:
    return t.replace("LOECHER", "LÖCHER")


def head(k: dict, label: str = None) -> str:
    return (f'<div class="card-head">'
            f'<div class="theme">{esc(label or theme_label(k["theme"]))}</div>'
            f'<div class="number">{k["no"]}</div></div>')


def card(k: dict, fmt: dict, key: str, side: str = None) -> str:
    """side: None = single-sided card, "front" = title only, "back" = text."""
    title_class = "title long" if len(k["title"]) > fmt["title_long"] else "title"

    if side == "front":
        return f"""
    <div class="card front" data-no="{k['no']}"
         data-max="{fmt['maxFront']}" data-min="{fmt['minFront']}">
      {head(k)}
      <div class="{title_class}">{esc(k['title'])}</div>
      <div class="card-foot">bitte wenden</div>
    </div>"""

    more = ""
    if WITH_MORE:
        more = (f'<div class="more"><div class="more-label">Mehr dazu</div>'
                f'<div class="more-text">{esc(k["more"])}</div></div>')
    css_class = "card back" if side == "back" else "card"
    foot = (f'<div class="card-foot">{esc(theme_label(k["theme"]))}</div>'
            if side == "back"
            else f'<div class="card-foot">{esc(FOOTER)} {k["no"]} / {len(CARDS)}</div>')
    return f"""
    <div class="{css_class}" data-no="{k['no']}">
      {head(k, "Antwort" if side == "back" else None)}
      <div class="{title_class}">{esc(k['title'])}</div>
      <div class="fact {level(k['text'])}">{esc(k['text'])}</div>
      {more}
      {foot}
    </div>"""


def marks(fmt: dict) -> str:
    if not CUT_LINES:
        return ""
    m = []
    for x in fmt["vlines"]:
        m.append(f'<div class="cut v" style="left:{x}mm"></div>')
        m.append(f'<div class="tick v-top" style="left:{x}mm"></div>')
        m.append(f'<div class="tick v-bottom" style="left:{x}mm"></div>')
    for y in fmt["hlines"]:
        m.append(f'<div class="cut h" style="top:{y}mm"></div>')
        m.append(f'<div class="tick h-left" style="top:{y}mm"></div>')
        m.append(f'<div class="tick h-right" style="top:{y}mm"></div>')
    return "".join(m)


EMPTY = '<div class="card"></div>'


def mirror(cells: list, columns: int) -> list:
    """Mirror the back sheets row by row for flipping along the long edge:
       1 2 / 3 4  ->  2 1 / 4 3"""
    out = []
    for i in range(0, len(cells), columns):
        out.extend(reversed(cells[i:i + columns]))
    return out


def sheet(key: str) -> str:
    """Consecutive layout: card 1 top left, then row by row.
    In duplex mode every front sheet is followed by its matching back sheet."""
    fmt = FORMATS[key]
    n = fmt["per_sheet"]
    land = " landscape" if fmt["landscape"] else ""
    out = []
    for i in range(0, len(CARDS), n):
        group = CARDS[i:i + n]
        missing = [EMPTY] * (n - len(group))
        if not DUPLEX:
            cells = [card(k, fmt, key) for k in group] + missing
            out.append(f'<div class="sheet f-{key}{land}">{marks(fmt)}{"".join(cells)}</div>')
            continue
        front = [card(k, fmt, key, "front") for k in group] + missing
        back = mirror([card(k, fmt, key, "back") for k in group] + missing, fmt["columns"])
        out.append(f'<div class="sheet f-{key}{land}">{marks(fmt)}{"".join(front)}</div>')
        out.append(f'<div class="sheet f-{key}{land}">{marks(fmt)}{"".join(back)}</div>')
    return "".join(out)


def index_html() -> str:
    parts = []
    for t in THEMES:
        rows = [k for k in CARDS if k["theme"] == t]
        if not rows:
            continue
        nos = [k["no"] for k in rows]
        span = (f"Karten {nos[0]}–{nos[-1]}"
                if nos == list(range(nos[0], nos[-1] + 1)) else f"{len(rows)} Karten")
        parts.append(f"<h2>{esc(theme_label(t))} "
                     f"<span class='range'>{span}</span></h2>")
        parts.append('<div class="index-cols">')
        for k in rows:
            parts.append(f'<div class="index-row"><span class="n">{k["no"]}</span>'
                         f'<span>{esc(k["title"])}</span></div>')
        parts.append("</div>")
    return (f'<div class="index-sheet"><h1>{esc(data["meta"]["title"])} '
            f'&ndash; Übersicht</h1><div class="sub">{len(CARDS)} Karten '
            f'&middot; nach Themen sortiert</div>{"".join(parts)}</div>')


def page(body: str, key: str = None) -> str:
    # Embed the font: DejaVu Sans is usually not installed on Windows, and
    # without embedding the text would break differently there.
    # Landscape formats additionally need their own page size.
    landscape = FORMATS.get(key, {}).get("landscape") if key else False
    page_rule = "@page { size: A4 landscape; margin: 0; }" if landscape else ""
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8">'
            f'<style>{fonts.fontface_css(quiet=True)}{CSS}{page_rule}</style>'
            f'</head><body>{body}</body></html>')


# Auto-fit: measures every card in the browser and adapts the font sizes to
# the height actually available - short texts grow, long ones shrink.
# Character count alone is not a good enough estimate: German compounds
# ("Hintergrundstrahlung") break early and produce extra lines.
AUTOFIT_JS = r"""(g) => {
  const PT = 96 / 72;
  const tooTall = c => c.scrollHeight - c.clientHeight > 0.5;

  // Does a word fail to fit the column width even with hyphenation? Then
  // the emergency break from cards.css kicks in and splits mid-word.
  // Tested by switching the emergency break off briefly and measuring
  // whether a line runs past the edge. That accounts for German
  // hyphenation correctly - "Donaudampfschifffahrt..." breaks cleanly,
  // a string without break points does not.
  const hardBreak = c => {
    let hit = null;
    c.querySelectorAll(".title,.fact,.more-text").forEach(e => {
      if (hit || !e.textContent.trim()) return;
      const prev = e.style.overflowWrap;
      e.style.overflowWrap = "normal";
      const r = document.createRange(); r.selectNodeContents(e);
      let b = 0; for (const q of r.getClientRects()) b = Math.max(b, q.width);
      const over = b - e.clientWidth > 0.5;
      e.style.overflowWrap = prev;
      if (over) hit = {el: e, word: e.textContent.trim().split(/\s+/)
                            .reduce((a, w) => w.length > a.length ? w : a, "")};
    });
    return hit;
  };
  const px = el => parseFloat(getComputedStyle(el).fontSize);
  const bump = (el, d) => { if (el) el.style.fontSize = (px(el) + d) + 'px'; };
  const report = [];
  document.querySelectorAll('.card[data-no]').forEach(c => {
    // The duplex title side has no body text - there the title itself is
    // scaled, with its own limits from data-min/data-max.
    const more  = c.querySelector('.more-text');
    const title = c.querySelector('.title');
    const fact  = c.querySelector('.fact') || title;
    if (!fact) return;
    const low  = +c.dataset.min || g.minText;
    const high = +c.dataset.max || g.maxText;

    // 1. grow while there is room
    let guard = 400;
    while (!tooTall(c) && px(fact) < high * PT && guard-- > 0) {
      bump(fact, 0.5); bump(more, 0.5);
    }
    // 2. one step back if that overflowed
    guard = 400;
    while (tooTall(c) && px(fact) > low * PT && guard-- > 0) {
      bump(fact, -0.5); bump(more, -0.5);
    }
    // 3. last resort: shrink the title if it still does not fit
    guard = 200;
    while (tooTall(c) && title && title !== fact && px(title) > g.minTitle * PT && guard-- > 0) {
      bump(title, -0.5);
    }
    // 4. Words that are too wide: shrink the affected element until the
    //    longest word fits the column. Shrinking also lowers the height,
    //    so the fit from steps 1-3 stays valid.
    guard = 200;
    let n;
    while ((n = hardBreak(c)) && guard-- > 0) {
      const limit = n.el === fact ? low
                  : n.el.classList.contains("title") ? g.minTitle : g.minText;
      if (px(n.el) - 0.5 < limit * PT) break;
      bump(n.el, -0.5);
    }
    const rest = hardBreak(c);
    report.push({no: c.dataset.no,
                 pt: Math.round(px(fact) / PT * 10) / 10,
                 tight: tooTall(c),
                 longWord: rest ? rest.word : null});
  });
  return report;
}"""


def render(html_str: str, pdf: pathlib.Path, pg, limits: dict = None):
    tmp = OUT / (pdf.stem + ".html")
    tmp.write_text(html_str, encoding="utf-8")
    pg.goto(tmp.as_uri())
    pg.emulate_media(media="print")
    if limits:
        b = pg.evaluate(AUTOFIT_JS, limits)
        if b:
            g = sorted(x["pt"] for x in b)
            print(f"    Auto-Fit: Textgrad {g[0]}–{g[-1]} pt "
                  f"(Median {g[len(g) // 2]} pt)")
        for x in b:
            if x.get("longWord"):
                w = x["longWord"]
                print(f"    ACHTUNG Karte {x['no']}: „{w[:30]}{'...' if len(w) > 30 else ''}“ "
                      f"({len(w)} Zeichen) ist breiter als die Karte und wird "
                      f"mitten im Wort umbrochen.")
            if x["tight"]:
                print(f"    ACHTUNG Karte {x['no']} passt auch bei {x['pt']} pt "
                      f"nicht - Text kuerzen!")
    pg.pdf(path=str(pdf), print_background=True,
           margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
           prefer_css_page_size=True)   # size comes from @page
    print(f"    {pdf.name}")


def main():
    wanted = [a.lower() for a in sys.argv[1:]] or list(FORMATS)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1400, "height": 1200})
        for key in wanted:
            if key not in FORMATS:
                print(f"Unbekanntes Format: {key}")
                continue
            up, f = key.upper(), FORMATS[key]
            sheets = -(-len(CARDS) // f["per_sheet"])
            kind = "Duplex, " if DUPLEX else ""
            print(f"Format {up}: {kind}{f['per_sheet']} Karten je Bogen, "
                  f"{sheets * (2 if DUPLEX else 1)} Bögen")
            g = {"minText": f["minText"], "maxText": f["maxText"],
                 "minTitle": f["minTitle"]}
            render(page(sheet(key), key),
                   OUT / f"astro-karten-{up}{'-duplex' if DUPLEX else ''}.pdf", pg, g)
        print("Index:")
        render(page(index_html()), OUT / "astro-karten-index.pdf", pg)
        br.close()
    print(f"Fertig: {len(CARDS)} Karten, einseitig.")


if __name__ == "__main__":
    main()
