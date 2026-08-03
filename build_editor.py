#!/usr/bin/env python3
"""
Baut den Kartendaten-Editor als einzelne HTML-Datei.

  python3 build_editor.py   ->  out/karten-editor.html

Die Datei ist eigenstaendig: Doppelklick genuegt, kein Server, kein Internet.
Hineinkopiert werden
  - facts.json          als Startdatensatz
  - cards.css           damit die Vorschau exakt dem Druck entspricht
  - DejaVu Sans         (auf Latin-1 reduziert, als WOFF2 eingebettet)

Der eingebettete Zeichensatz ist der Punkt: Der Editor rechnet die
Druckgroesse live aus, und das stimmt nur, wenn er dieselbe Schrift
vermisst, die spaeter auch im PDF steht - DejaVu Sans ist auf Windows
normalerweise nicht installiert.
"""

import json
import pathlib

BASE = pathlib.Path(__file__).parent
OUT = BASE / "out"
OUT.mkdir(exist_ok=True)
FONTDIR = pathlib.Path("/usr/share/fonts/truetype/dejavu")

# Latin-1 plus Sonderzeichen, die in den Karten vorkommen
ZEICHEN = ("".join(chr(c) for c in range(0x20, 0x100))
           + "\u2013\u2014\u2018\u2019\u201a\u201c\u201d\u201e\u2026"
           + "\u00b2\u00b3\u00b0\u00b7\u2022\u00d7\u2212\u2192")


def main():
    print("Schriften einbetten ...")
    import fonts as F
    schrift = F.fontface_css()
    vorlage = (BASE / "editor_template.html").read_text(encoding="utf-8")
    daten = (BASE / "facts.json").read_text(encoding="utf-8")
    css = (BASE / "cards.css").read_text(encoding="utf-8")

    # cards.css unveraendert uebernehmen, nur zwei Regeln anpassen, damit sie
    # die Editor-Oberflaeche nicht mit ueberschreiben:
    #   html, body  ->  .buehne, .druckflaeche
    # So gelten Schrift, Farbe und Zeilenhoehe der Karten nur dort und
    # ueberschreiben nicht die Editor-Oberflaeche. @page bleibt erhalten,
    # es wird fuer den PDF-Druck aus dem Editor gebraucht.
    css = css.replace("html, body {", ".buehne, .druckflaeche {")

    # Formatdefinition und Auto-Fit direkt aus build_cards.py uebernehmen,
    # damit Vorschau und Druck garantiert dieselbe Rechnung benutzen.
    import build_cards as B

    html = (vorlage
            .replace("/*__FONTS__*/", schrift)
            .replace("/*__KARTEN_CSS__*/", css)
            .replace("/*__FORMATE__*/", json.dumps(B.FORMATE, ensure_ascii=False))
            .replace("/*__AUTOFIT__*/", B.AUTOFIT_JS)
            .replace("/*__DATEN__*/", daten.strip()))

    ziel = OUT / "karten-editor.html"
    ziel.write_text(html, encoding="utf-8")
    print(f"\n{ziel.name}  ({ziel.stat().st_size // 1024} kB)")


if __name__ == "__main__":
    main()
