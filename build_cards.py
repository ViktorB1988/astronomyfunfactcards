#!/usr/bin/env python3
"""
Astronomie-Faktenkarten -> druckfertige PDFs

  python3 build_cards.py            # beide Formate
  python3 build_cards.py a7         # nur A7
  python3 build_cards.py a6

Einseitig. Die Karten stehen fortlaufend von 1 bis 100 auf den Boegen,
zeilenweise von links oben nach rechts unten. Die Rueckseite bleibt leer.

Erzeugt im Ordner ./out:
  astro-karten-A7.pdf      13 Boegen, 8 Karten je Bogen
  astro-karten-A6.pdf      25 Boegen, 4 Karten je Bogen
  astro-karten-index.pdf   Uebersichtsliste zum schnellen Finden

Daten liegen in facts.json, Layout in cards.css.
Nach dem Rendern misst das Skript jede Karte und verkleinert den Text
so weit noetig, damit nichts abgeschnitten wird.
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

# Zusatzinfo ("Nachschlag") unten auf die Karte drucken.
# Auf False setzen, wenn nur der reine Fakt erscheinen soll -
# dann wird der Text deutlich groesser.
MIT_NACHSCHLAG = True

# Schnittlinien und Anlegemarken auf die Boegen drucken.
# Auf False setzen, wenn die Boegen ohne jede Hilfslinie gebraucht werden -
# dann bleibt aber nichts, woran sich der Schnitt ausrichten laesst.
SCHNITTLINIEN = True

# Duplexmodus: Vorderseite zeigt nur Thema und Titel, der Fakt steht auf der
# Rueckseite. Die Boegen wechseln sich ab (Vorderseite, Rueckseite, ...) und
# die Rueckseiten sind fuer das Wenden an der langen Kante gespiegelt.
DUPLEX = False

data = json.loads((BASE / "facts.json").read_text(encoding="utf-8"))
CSS = (BASE / "cards.css").read_text(encoding="utf-8")
THEMEN = data["themen"]
KARTEN = data["karten"]
FUSS = data["meta"].get("fusszeile", "Faktenkarte")

# Formatdefinition: Karten pro Bogen, Spalten, Schnittlinien in mm,
# Mindestschriftgrade fuer den Auto-Fit
FORMATE = {
    "a6": {"pro_bogen": 4, "spalten": 2, "quer": False,
           "vlinien": [105.0], "hlinien": [148.5],
           "titel_lang": 30, "minText": 11.0, "maxText": 21.0, "minTitel": 14.0,
           "minVorne": 15.0, "maxVorne": 34.0},
    "a6q": {"pro_bogen": 4, "spalten": 2, "quer": True,
            "vlinien": [148.5], "hlinien": [105.0],
            "titel_lang": 34, "minText": 11.0, "maxText": 20.0, "minTitel": 14.0,
            "minVorne": 15.0, "maxVorne": 32.0},
    "a7": {"pro_bogen": 8, "spalten": 2, "quer": False,
           "vlinien": [105.0], "hlinien": [74.25, 148.5, 222.75],
           "titel_lang": 26, "minText": 7.5, "maxText": 14.0, "minTitel": 9.0,
           "minVorne": 10.0, "maxVorne": 22.0},
}

def esc(s: str) -> str:
    """Escaped alles ausser den erlaubten <sup>-Tags."""
    s = htmlmod.escape(s, quote=False)
    return s.replace("&lt;sup&gt;", "<sup>").replace("&lt;/sup&gt;", "</sup>")


def plain_len(s: str) -> int:
    return len(s.replace("<sup>", "").replace("</sup>", ""))


def stufe(text: str) -> str:
    n = plain_len(text)
    return "s1" if n < 170 else "s2" if n < 215 else "s3" if n < 265 else "s4"


def thema_anzeige(t: str) -> str:
    return t.replace("LOECHER", "LÖCHER")


def kopf(k: dict, beschriftung: str = None) -> str:
    return (f'<div class="card-head">'
            f'<div class="thema">{esc(beschriftung or thema_anzeige(k["thema"]))}</div>'
            f'<div class="nummer">{k["nr"]}</div></div>')


def karte(k: dict, fmt: dict, key: str, seite: str = None) -> str:
    """seite: None = einseitige Karte, "vorne" = nur Titel, "hinten" = Text."""
    tk = "titel long" if len(k["titel"]) > fmt["titel_lang"] else "titel"

    if seite == "vorne":
        return f"""
    <div class="card vorne" data-nr="{k['nr']}"
         data-max="{fmt['maxVorne']}" data-min="{fmt['minVorne']}">
      {kopf(k)}
      <div class="{tk}">{esc(k['titel'])}</div>
      <div class="card-foot">bitte wenden</div>
    </div>"""

    mehr = ""
    if MIT_NACHSCHLAG:
        mehr = (f'<div class="mehr"><div class="mehr-label">Mehr dazu</div>'
                f'<div class="nachschlag">{esc(k["nachschlag"])}</div></div>')
    klasse = "card hinten" if seite == "hinten" else "card"
    fuss = (f'<div class="card-foot">{esc(thema_anzeige(k["thema"]))}</div>'
            if seite == "hinten"
            else f'<div class="card-foot">{esc(FUSS)} {k["nr"]} / {len(KARTEN)}</div>')
    return f"""
    <div class="{klasse}" data-nr="{k['nr']}">
      {kopf(k, "Antwort" if seite == "hinten" else None)}
      <div class="{tk}">{esc(k['titel'])}</div>
      <div class="fakt {stufe(k['text'])}">{esc(k['text'])}</div>
      {mehr}
      {fuss}
    </div>"""


def marken(fmt: dict) -> str:
    if not SCHNITTLINIEN:
        return ""
    m = []
    for x in fmt["vlinien"]:
        m.append(f'<div class="cut v" style="left:{x}mm"></div>')
        m.append(f'<div class="tick v-top" style="left:{x}mm"></div>')
        m.append(f'<div class="tick v-bottom" style="left:{x}mm"></div>')
    for y in fmt["hlinien"]:
        m.append(f'<div class="cut h" style="top:{y}mm"></div>')
        m.append(f'<div class="tick h-left" style="top:{y}mm"></div>')
        m.append(f'<div class="tick h-right" style="top:{y}mm"></div>')
    return "".join(m)


LEER = '<div class="card"></div>'


def spiegeln(zellen: list, spalten: int) -> list:
    """Rueckseiten fuers Wenden an der langen Kante zeilenweise spiegeln:
       1 2 / 3 4  ->  2 1 / 4 3"""
    out = []
    for i in range(0, len(zellen), spalten):
        out.extend(reversed(zellen[i:i + spalten]))
    return out


def bogen(key: str) -> str:
    """Fortlaufende Belegung: Karte 1 links oben, dann zeilenweise weiter.
    Im Duplexmodus folgt auf jeden Vorderseitenbogen der passende Rueckseitenbogen."""
    fmt = FORMATE[key]
    n = fmt["pro_bogen"]
    q = " quer" if fmt["quer"] else ""
    out = []
    for i in range(0, len(KARTEN), n):
        gruppe = KARTEN[i:i + n]
        fehlt = [LEER] * (n - len(gruppe))
        if not DUPLEX:
            zellen = [karte(k, fmt, key) for k in gruppe] + fehlt
            out.append(f'<div class="sheet f-{key}{q}">{marken(fmt)}{"".join(zellen)}</div>')
            continue
        v = [karte(k, fmt, key, "vorne") for k in gruppe] + fehlt
        h = spiegeln([karte(k, fmt, key, "hinten") for k in gruppe] + fehlt, fmt["spalten"])
        out.append(f'<div class="sheet f-{key}{q}">{marken(fmt)}{"".join(v)}</div>')
        out.append(f'<div class="sheet f-{key}{q}">{marken(fmt)}{"".join(h)}</div>')
    return "".join(out)


def index_html() -> str:
    parts = []
    for t in THEMEN:
        rows = [k for k in KARTEN if k["thema"] == t]
        if not rows:
            continue
        nrn = [k["nr"] for k in rows]
        spanne = (f"Karten {nrn[0]}\u2013{nrn[-1]}"
                  if nrn == list(range(nrn[0], nrn[-1] + 1)) else f"{len(rows)} Karten")
        parts.append(f"<h2>{esc(thema_anzeige(t))} "
                     f"<span class='spanne'>{spanne}</span></h2>")
        parts.append('<div class="index-cols">')
        for k in rows:
            parts.append(f'<div class="index-row"><span class="n">{k["nr"]}</span>'
                         f'<span>{esc(k["titel"])}</span></div>')
        parts.append("</div>")
    return (f'<div class="index-sheet"><h1>{esc(data["meta"]["titel"])} '
            f'&ndash; \u00dcbersicht</h1><div class="sub">{len(KARTEN)} Karten '
            f'&middot; nach Themen sortiert</div>{"".join(parts)}</div>')


def seite(body: str, key: str = None) -> str:
    # Schrift mit einbetten: DejaVu Sans ist auf Windows meist nicht
    # installiert, ohne Einbettung braeche der Satz dort anders um.
    # Querformate brauchen zusaetzlich eine eigene Seitengroesse.
    quer = FORMATE.get(key, {}).get("quer") if key else False
    seitenregel = "@page { size: A4 landscape; margin: 0; }" if quer else ""
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8">'
            f'<style>{fonts.fontface_css(still=True)}{CSS}{seitenregel}</style>'
            f'</head><body>{body}</body></html>')


# Auto-Fit: misst jede Karte im Browser und passt die Schriftgrade an die
# tatsaechlich vorhandene Hoehe an - kleine Texte wachsen, lange schrumpfen.
# Reine Zeichenzahl reicht als Schaetzung nicht: deutsche Komposita
# ("Hintergrundstrahlung") brechen frueh um und erzeugen Extrazeilen.
AUTOFIT_JS = r"""(g) => {
  const PT = 96 / 72;
  const zuGross = c => c.scrollHeight - c.clientHeight > 0.5;

  // Passt ein Wort selbst mit Silbentrennung nicht in die Spaltenbreite?
  // Dann greift der Notumbruch aus cards.css und trennt mitten im Wort.
  // Geprueft wird, indem der Notumbruch kurz abgeschaltet und gemessen wird,
  // ob eine Zeile ueber den Rand laeuft. Das beruecksichtigt die deutsche
  // Silbentrennung korrekt - "Donaudampfschifffahrt..." bricht sauber um,
  // eine Zeichenkette ohne Trennstellen nicht.
  const notumbruch = c => {
    let treffer = null;
    c.querySelectorAll(".titel,.fakt,.nachschlag").forEach(e => {
      if (treffer || !e.textContent.trim()) return;
      const alt = e.style.overflowWrap;
      e.style.overflowWrap = "normal";
      const r = document.createRange(); r.selectNodeContents(e);
      let b = 0; for (const q of r.getClientRects()) b = Math.max(b, q.width);
      const ueber = b - e.clientWidth > 0.5;
      e.style.overflowWrap = alt;
      if (ueber) treffer = {el: e, wort: e.textContent.trim().split(/\s+/)
                              .reduce((a, w) => w.length > a.length ? w : a, "")};
    });
    return treffer;
  };
  const px = el => parseFloat(getComputedStyle(el).fontSize);
  const setz = (el, d) => { if (el) el.style.fontSize = (px(el) + d) + 'px'; };
  const bericht = [];
  document.querySelectorAll('.card[data-nr]').forEach(c => {
    // Auf der Duplex-Titelseite gibt es keinen Fliesstext - dort wird der
    // Titel selbst skaliert, mit eigenen Grenzen aus data-min/data-max.
    const zusatz = c.querySelector('.nachschlag');
    const titel  = c.querySelector('.titel');
    const fakt   = c.querySelector('.fakt') || titel;
    if (!fakt) return;
    const unten = +c.dataset.min || g.minText;
    const oben  = +c.dataset.max || g.maxText;

    // 1. wachsen, solange Platz ist
    let guard = 400;
    while (!zuGross(c) && px(fakt) < oben * PT && guard-- > 0) {
      setz(fakt, 0.5); setz(zusatz, 0.5);
    }
    // 2. einen Schritt zurueck, falls dabei uebergelaufen
    guard = 400;
    while (zuGross(c) && px(fakt) > unten * PT && guard-- > 0) {
      setz(fakt, -0.5); setz(zusatz, -0.5);
    }
    // 3. Notbremse: Titel verkleinern, wenn es immer noch nicht passt
    guard = 200;
    while (zuGross(c) && titel && titel !== fakt && px(titel) > g.minTitel * PT && guard-- > 0) {
      setz(titel, -0.5);
    }
    // 4. Zu breite Woerter: das betroffene Element verkleinern, bis das
    //    laengste Wort in die Spalte passt. Verkleinern senkt auch die
    //    Hoehe, der Fit aus Schritt 1-3 bleibt also gueltig.
    guard = 200;
    let n;
    while ((n = notumbruch(c)) && guard-- > 0) {
      const grenze = n.el === fakt ? unten
                   : n.el.classList.contains("titel") ? g.minTitel : g.minText;
      if (px(n.el) - 0.5 < grenze * PT) break;
      setz(n.el, -0.5);
    }
    const rest = notumbruch(c);
    bericht.push({nr: c.dataset.nr,
                  pt: Math.round(px(fakt) / PT * 10) / 10,
                  eng: zuGross(c),
                  langwort: rest ? rest.wort : null});
  });
  return bericht;
}"""


def render(html_str: str, pdf: pathlib.Path, pg, grenzen: dict = None):
    tmp = OUT / (pdf.stem + ".html")
    tmp.write_text(html_str, encoding="utf-8")
    pg.goto(tmp.as_uri())
    pg.emulate_media(media="print")
    if grenzen:
        b = pg.evaluate(AUTOFIT_JS, grenzen)
        if b:
            g = sorted(x["pt"] for x in b)
            print(f"    Auto-Fit: Textgrad {g[0]}–{g[-1]} pt "
                  f"(Median {g[len(g) // 2]} pt)")
        for x in b:
            if x.get("langwort"):
                w = x["langwort"]
                print(f"    ACHTUNG Karte {x['nr']}: „{w[:30]}{'...' if len(w) > 30 else ''}“ "
                      f"({len(w)} Zeichen) ist breiter als die Karte und wird "
                      f"mitten im Wort umbrochen.")
            if x["eng"]:
                print(f"    ACHTUNG Karte {x['nr']} passt auch bei {x['pt']} pt "
                      f"nicht - Text kuerzen!")
    pg.pdf(path=str(pdf), print_background=True,
           margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
           prefer_css_page_size=True)   # Groesse kommt aus @page
    print(f"    {pdf.name}")


def main():
    wunsch = [a.lower() for a in sys.argv[1:]] or list(FORMATE)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1400, "height": 1200})
        for key in wunsch:
            if key not in FORMATE:
                print(f"Unbekanntes Format: {key}")
                continue
            up, f = key.upper(), FORMATE[key]
            boegen = -(-len(KARTEN) // f["pro_bogen"])
            art = "Duplex, " if DUPLEX else ""
            print(f"Format {up}: {art}{f['pro_bogen']} Karten je Bogen, "
                  f"{boegen * (2 if DUPLEX else 1)} Bögen")
            g = {"minText": f["minText"], "maxText": f["maxText"],
                 "minTitel": f["minTitel"]}
            render(seite(bogen(key), key),
                   OUT / f"astro-karten-{up}{'-duplex' if DUPLEX else ''}.pdf", pg, g)
        print("Index:")
        render(seite(index_html()), OUT / "astro-karten-index.pdf", pg)
        br.close()
    print(f"Fertig: {len(KARTEN)} Karten, einseitig.")


if __name__ == "__main__":
    main()
