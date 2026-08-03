#!/usr/bin/env python3
"""
Fetches the card state from Firestore and writes it to facts.json.

  python3 fetch_facts.py            # to facts.json, asks first
  python3 fetch_facts.py --yes      # overwrite without asking
  python3 fetch_facts.py -o new.json

This keeps the PDF build tied to the database: edit online, fetch here,
then run build_cards.py. Without this route the state would have to be
downloaded by hand in the browser and the file copied over.

It only reads, and reading is public according to firestore.rules - so the
script needs no sign-in, no service key and no extra packages. The project
id comes from web/firebase-config.js so that it is not maintained twice.
"""

import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

BASE = pathlib.Path(__file__).parent
CONFIG = BASE / "web" / "firebase-config.js"
ROOT = "https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents"


def project_id() -> str:
    text = CONFIG.read_text(encoding="utf-8")
    hit = re.search(r'projectId\s*:\s*"([^"]+)"', text)
    if not hit or "HIER_EINTRAGEN" in hit.group(1):
        sys.exit("In web/firebase-config.js steht noch keine projectId.")
    return hit.group(1)


def fetch(url: str) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=30) as answer:
            return json.loads(answer.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 403:
            sys.exit("Firestore verweigert das Lesen (403). Sind die Regeln aus "
                     "firestore.rules veroeffentlicht?")
        if e.code == 404:
            sys.exit("Datenbank oder Sammlung nicht gefunden (404). Ist Firestore "
                     "im Projekt schon angelegt?")
        sys.exit(f"Firestore antwortet mit {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        sys.exit(f"Keine Verbindung zu Firestore: {e.reason}")


def value(field: dict):
    """One Firestore field to a Python value. Firestore puts the type in the
    key, and numbers come back as strings."""
    for key, raw in field.items():
        if key == "integerValue":
            return int(raw)
        if key == "doubleValue":
            return float(raw)
        if key == "booleanValue":
            return bool(raw)
        if key == "nullValue":
            return None
        if key == "arrayValue":
            return [value(x) for x in raw.get("values", [])]
        if key == "mapValue":
            return {k: value(v) for k, v in raw.get("fields", {}).items()}
        return raw
    return None


def fields(document: dict) -> dict:
    return {k: value(v) for k, v in document.get("fields", {}).items()}


def all_cards(pid: str) -> list:
    result, token = [], None
    while True:
        url = f"{ROOT.format(pid=pid)}/cards?pageSize=300"
        if token:
            url += "&pageToken=" + token
        answer = fetch(url)
        result.extend(answer.get("documents", []))
        token = answer.get("nextPageToken")
        if not token:
            break
    return result


def main():
    p = argparse.ArgumentParser(description="Fetch the card state from Firestore")
    p.add_argument("-o", "--out", default="facts.json", help="target file")
    p.add_argument("--yes", action="store_true", help="overwrite without asking")
    args = p.parse_args()

    pid = project_id()
    print(f"Lese aus Projekt {pid} ...")

    raw = all_cards(pid)
    if not raw:
        sys.exit("Die Sammlung 'cards' ist leer. In der Datenbank steht noch nichts.")

    # The order comes from pos, not from the response: the REST interface
    # sorts by document id, which is arbitrary here.
    # The document name carries the id, and it is written out: it is what a
    # card is, independent of its wording, and it is what lets the file go
    # back in without every card arriving as a new one.
    cards = []
    for d in raw:
        k = fields(d)
        k["id"] = d["name"].rsplit("/", 1)[-1]
        cards.append(k)
    cards.sort(key=lambda k: k.get("pos", 0))

    meta = fields(fetch(f"{ROOT.format(pid=pid)}/config/meta"))
    themes = meta.pop("themes", [])
    if not themes:
        sys.exit("In config/meta fehlt die Themenliste.")

    data = {
        "meta": meta,
        "themes": themes,
        # `no` is assigned here - it is not stored in the database, it is
        # purely derived from the order.
        "cards": [{"id": k["id"],
                   "no": i + 1,
                   "theme": k.get("theme", ""),
                   "title": k.get("title", ""),
                   "text": k.get("text", ""),
                   "more": k.get("more", "")}
                  for i, k in enumerate(cards)],
    }

    unknown = sorted({k["theme"] for k in data["cards"]} - set(themes))
    if unknown:
        print("  ACHTUNG: Themen ohne Eintrag in der Themenliste: "
              + ", ".join(unknown))

    target = BASE / args.out
    if target.exists() and not args.yes:
        old = json.loads(target.read_text(encoding="utf-8"))
        print(f"  {target.name} hat {len(old.get('cards', []))} Karten, "
              f"neu waeren es {len(data['cards'])}.")
        if input("  Ueberschreiben? [j/N] ").strip().lower() not in ("j", "ja", "y"):
            sys.exit("Abgebrochen, nichts geaendert.")

    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(f"\n{target.name}: {len(data['cards'])} Karten, {len(themes)} Themen.")
    print("Weiter mit: python3 build_cards.py")


if __name__ == "__main__":
    main()
