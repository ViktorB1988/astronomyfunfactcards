#!/usr/bin/env python3
"""
Builds the online version for GitHub Pages.

  python3 build_web.py   ->  site/

Difference to build_editor.py: the editor additionally gets the database
layer from web/ and then takes its data from Firestore instead of from the
bundled facts.json.

facts.json is embedded anyway, for two reasons:

1. The page is there immediately and stays usable even when Firestore is
   unreachable or the project is not set up yet.
2. It is the template for the initial fill of the empty database - without
   it, all 170 cards would have to be entered by hand.

After the first snapshot from the database it is replaced.

FORMATS and the auto-fit come straight from build_cards.py, same as for
the offline editor. Do not reimplement: preview, print and PDF have to use
the same computation.
"""

import hashlib
import json
import pathlib

BASE = pathlib.Path(__file__).parent
TARGET = BASE / "site"
WEB = BASE / "web"

# Inserted into editor_template.html at the <!--__FIREBASE__--> marker.
# A module always runs after the classic script, so the window.Editor
# interface is guaranteed to be in place.
#
# The ?v= is a content stamp and it matters: GitHub Pages hands out assets
# with a ten-minute cache lifetime, and the page and its module expire
# separately. Without the stamp a returning visitor can end up running a
# stale module against fresh HTML - which looks exactly like a bug that
# will not reproduce. A changed module gets a new address and is fetched.
INCLUDE = '<script type="module" src="firebase-app.js?v={stamp}"></script>'


def main():
    TARGET.mkdir(exist_ok=True)

    print("Schriften einbetten ...")
    import fonts as F
    font_css = F.fontface_css()
    if not font_css:
        print("  ACHTUNG: keine Schrift eingebettet. Die angezeigte Druckgroesse")
        print("  weicht dann je nach Rechner vom PDF ab. Auf Debian/Ubuntu:")
        print("  apt-get install fonts-dejavu-core")

    import build_cards as B

    template = (BASE / "editor_template.html").read_text(encoding="utf-8")
    data = (BASE / "facts.json").read_text(encoding="utf-8")
    css = (BASE / "cards.css").read_text(encoding="utf-8")

    # As in build_editor.py: cards.css applies only to the preview stage and
    # the print area, so that it does not paint over the editor interface.
    css = css.replace("html, body {", ".stage, .printarea {")

    # One stamp for both files: the module and its configuration are only
    # ever correct as a pair, so a change to either has to invalidate both.
    app_js = (WEB / "firebase-app.js").read_text(encoding="utf-8")
    config_js = (WEB / "firebase-config.js").read_text(encoding="utf-8")
    stamp = hashlib.sha256((app_js + config_js).encode("utf-8")).hexdigest()[:10]
    include = INCLUDE.format(stamp=stamp)

    html = (template
            .replace("/*__FONTS__*/", font_css)
            .replace("/*__CARDS_CSS__*/", css)
            .replace("/*__FORMATS__*/", json.dumps(B.FORMATS, ensure_ascii=False))
            .replace("/*__LEVELS__*/", json.dumps(B.LEVELS, ensure_ascii=False))
            .replace("/*__AUTOFIT__*/", B.AUTOFIT_JS)
            .replace("/*__DATA__*/", data.strip())
            .replace("<!--__FIREBASE__-->", include))

    if include not in html:
        raise SystemExit("editor_template.html no longer contains <!--__FIREBASE__--> - "
                         "without that marker the page gets no database.")

    (TARGET / "index.html").write_text(html, encoding="utf-8")

    # The module imports its configuration itself, so that address needs the
    # same stamp - otherwise a fresh module could pick up a stale config.
    (TARGET / "firebase-app.js").write_text(
        app_js.replace('"./firebase-config.js"', f'"./firebase-config.js?v={stamp}"'),
        encoding="utf-8")
    (TARGET / "firebase-config.js").write_text(config_js, encoding="utf-8")

    # GitHub Pages runs everything through Jekyll, which swallows files
    # starting with an underscore. Does not affect us today, costs nothing.
    (TARGET / ".nojekyll").write_text("", encoding="utf-8")

    config = (WEB / "firebase-config.js").read_text(encoding="utf-8")
    if "HIER_EINTRAGEN" in config:
        print("\n  Hinweis: web/firebase-config.js ist noch nicht ausgefuellt.")
        print("  Die Seite laeuft, zeigt aber nur den Stand aus facts.json")
        print("  und speichert nirgendwohin.")

    size = (TARGET / "index.html").stat().st_size // 1024
    print(f"\nsite/index.html  ({size} kB)")
    print("site/firebase-app.js, site/firebase-config.js")


if __name__ == "__main__":
    main()
