#!/usr/bin/env python3
"""
Embeds DejaVu Sans as WOFF2 directly into HTML.

Shared by build_cards.py, build_editor.py and build_web.py. That matters
for two reasons:

1. DejaVu Sans is normally not installed on Windows. Without embedding,
   the PDF build would fall back to Arial there, break lines differently
   and end up with different font sizes than here.
2. The editor preview and the print PDF then measure exactly the same
   font. A metric difference of 0.02 % is already enough to tip a line
   break and shift the reported print size by one step.

If the font file is missing (different system, no fonttools), the module
returns an empty string - the font stack from cards.css then applies.
"""

import base64
import functools
import io
import pathlib

SEARCH_PATHS = [
    pathlib.Path("/usr/share/fonts/truetype/dejavu"),
    pathlib.Path("/usr/share/fonts/dejavu"),
    pathlib.Path(__file__).parent / "fonts",
]

# Latin-1 plus the special characters that occur on the cards
CHARS = ("".join(chr(c) for c in range(0x20, 0x100))
         + "–—‘’‚“”„…"
         + "²³°·•×−→")


def _find(name: str):
    for folder in SEARCH_PATHS:
        p = folder / name
        if p.exists():
            return p
    return None


def _woff2(path: pathlib.Path) -> str:
    import logging
    logging.getLogger("fontTools").setLevel(logging.ERROR)
    from fontTools.ttLib import TTFont
    from fontTools.subset import Subsetter, Options
    f = TTFont(path)
    o = Options()
    o.layout_features = ["kern", "liga"]
    o.notdef_outline = True
    s = Subsetter(options=o)
    s.populate(text=CHARS)
    s.subset(f)
    f.flavor = "woff2"
    buf = io.BytesIO()
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


@functools.lru_cache(maxsize=1)
def fontface_css(quiet: bool = False) -> str:
    """Returns the @font-face block with the embedded font."""
    parts = []
    for name, weight in (("DejaVuSans.ttf", 400), ("DejaVuSans-Bold.ttf", 700)):
        p = _find(name)
        if not p:
            if not quiet:
                print(f"  Hinweis: {name} nicht gefunden, Schrift wird nicht eingebettet.")
            return ""
        try:
            b64 = _woff2(p)
        except Exception as e:                       # fonttools missing etc.
            if not quiet:
                print(f"  Hinweis: Einbettung fehlgeschlagen ({e}).")
            return ""
        parts.append(
            f'@font-face {{ font-family: "DejaVu Sans"; font-style: normal;\n'
            f'  font-weight: {weight};\n'
            f'  src: url("data:font/woff2;base64,{b64}") format("woff2"); }}')
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    css = fontface_css()
    print(f"{len(css) // 1024} kB CSS mit eingebetteter Schrift"
          if css else "keine Schrift eingebettet")
