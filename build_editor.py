#!/usr/bin/env python3
"""
Builds the card editor as a single HTML file.

  python3 build_editor.py   ->  out/karten-editor.html

The file stands on its own: a double click is enough, no server, no
internet. Copied into it are
  - facts.json          as the initial data set
  - cards.css           so the preview matches the print exactly
  - DejaVu Sans         (reduced to Latin-1, embedded as WOFF2)

The embedded font is the point: the editor computes the print size live,
and that is only correct if it measures the same font that ends up in the
PDF - DejaVu Sans is normally not installed on Windows.

For the online version on GitHub Pages see build_web.py.
"""

import json
import pathlib

BASE = pathlib.Path(__file__).parent
OUT = BASE / "out"
OUT.mkdir(exist_ok=True)


def main():
    print("Schriften einbetten ...")
    import fonts as F
    font_css = F.fontface_css()
    template = (BASE / "editor_template.html").read_text(encoding="utf-8")
    data = (BASE / "facts.json").read_text(encoding="utf-8")
    css = (BASE / "cards.css").read_text(encoding="utf-8")

    # Take cards.css unchanged, adjusting only one rule so that it does not
    # paint over the editor interface:
    #   html, body  ->  .stage, .printarea
    # Font, colour and line height of the cards then apply only there.
    # @page stays, it is needed for printing a PDF from the editor.
    css = css.replace("html, body {", ".stage, .printarea {")

    # Take the format definition and the auto-fit straight from
    # build_cards.py so that preview and print are guaranteed to use the
    # same computation.
    import build_cards as B

    html = (template
            .replace("/*__FONTS__*/", font_css)
            .replace("/*__CARDS_CSS__*/", css)
            .replace("/*__FORMATS__*/", json.dumps(B.FORMATS, ensure_ascii=False))
            .replace("/*__LEVELS__*/", json.dumps(B.LEVELS, ensure_ascii=False))
            .replace("/*__AUTOFIT__*/", B.AUTOFIT_JS)
            .replace("/*__DATA__*/", data.strip()))

    target = OUT / "karten-editor.html"
    target.write_text(html, encoding="utf-8")
    print(f"\n{target.name}  ({target.stat().st_size // 1024} kB)")


if __name__ == "__main__":
    main()
