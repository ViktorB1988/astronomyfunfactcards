#!/usr/bin/env python3
"""
Bettet DejaVu Sans als WOFF2 direkt in HTML ein.

Wird von build_cards.py und build_editor.py gemeinsam benutzt. Das ist wichtig
aus zwei Gruenden:

1. Auf Windows ist DejaVu Sans normalerweise nicht installiert. Ohne
   Einbettung wuerde der PDF-Bau dort auf Arial ausweichen, anders umbrechen
   und andere Schriftgroessen ergeben als hier.
2. Vorschau im Editor und Druck-PDF vermessen so garantiert dieselbe Schrift.
   Schon 0,02 % Metrikunterschied reichen, um einen Zeilenumbruch zu kippen
   und damit die angezeigte Druckgroesse um einen Schritt zu verschieben.

Faellt die Schriftdatei aus (anderes System, fehlendes fonttools), liefert
das Modul einen leeren String - dann greift die Schriftliste aus cards.css.
"""

import base64
import functools
import io
import pathlib

SUCHPFADE = [
    pathlib.Path("/usr/share/fonts/truetype/dejavu"),
    pathlib.Path("/usr/share/fonts/dejavu"),
    pathlib.Path(__file__).parent / "fonts",
]

# Latin-1 plus die Sonderzeichen, die in den Karten vorkommen
ZEICHEN = ("".join(chr(c) for c in range(0x20, 0x100))
           + "\u2013\u2014\u2018\u2019\u201a\u201c\u201d\u201e\u2026"
           + "\u00b2\u00b3\u00b0\u00b7\u2022\u00d7\u2212\u2192")


def _finde(name: str):
    for ordner in SUCHPFADE:
        p = ordner / name
        if p.exists():
            return p
    return None


def _woff2(pfad: pathlib.Path) -> str:
    import logging
    logging.getLogger("fontTools").setLevel(logging.ERROR)
    from fontTools.ttLib import TTFont
    from fontTools.subset import Subsetter, Options
    f = TTFont(pfad)
    o = Options()
    o.layout_features = ["kern", "liga"]
    o.notdef_outline = True
    s = Subsetter(options=o)
    s.populate(text=ZEICHEN)
    s.subset(f)
    f.flavor = "woff2"
    buf = io.BytesIO()
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


@functools.lru_cache(maxsize=1)
def fontface_css(still: bool = False) -> str:
    """Liefert den @font-face-Block mit eingebetteter Schrift."""
    teile = []
    for datei, gewicht in (("DejaVuSans.ttf", 400), ("DejaVuSans-Bold.ttf", 700)):
        p = _finde(datei)
        if not p:
            if not still:
                print(f"  Hinweis: {datei} nicht gefunden, Schrift wird nicht eingebettet.")
            return ""
        try:
            b64 = _woff2(p)
        except Exception as e:                       # fonttools fehlt o. ae.
            if not still:
                print(f"  Hinweis: Einbettung fehlgeschlagen ({e}).")
            return ""
        teile.append(
            f'@font-face {{ font-family: "DejaVu Sans"; font-style: normal;\n'
            f'  font-weight: {gewicht};\n'
            f'  src: url("data:font/woff2;base64,{b64}") format("woff2"); }}')
    return "\n".join(teile) + "\n"


if __name__ == "__main__":
    css = fontface_css()
    print(f"{len(css) // 1024} kB CSS mit eingebetteter Schrift"
          if css else "keine Schrift eingebettet")
