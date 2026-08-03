# Astronomie-Faktenkarten

Druckbare Faktenkarten zum Vorlesen für Besucher einer Sternwarte.
Aus einer JSON-Datenquelle entstehen PDFs in drei Formaten sowie ein
eigenständiger HTML-Editor.

Sprache aller Inhalte, Kommentare und Ausgaben: **Deutsch.**

---

## Schnellstart

```bash
pip install playwright fonttools brotli
playwright install chromium

python3 build_cards.py          # alle PDFs nach ./out
python3 build_cards.py a7       # nur ein Format
python3 build_editor.py         # Editor nach ./out/karten-editor.html
```

`build_editor.py` importiert `build_cards.py`. Nach jeder Änderung an
`facts.json` oder `cards.css` **beide** Skripte laufen lassen, sonst
enthält der Editor einen veralteten Stand.

---

## Dateien

| Datei | Rolle |
|---|---|
| `facts.json` | **Einzige Datenquelle.** Themenliste + Karten |
| `cards.css` | **Einziges Layout.** Kartenmaße, Schriftgrade, Schnittlinien |
| `build_cards.py` | Baut die PDFs. Enthält `FORMATE` und den Auto-Fit |
| `editor_template.html` | Vorlage des Editors mit Platzhaltern |
| `build_editor.py` | Setzt Vorlage + `cards.css` + `facts.json` + Schrift zusammen |
| `fonts.py` | Bettet DejaVu Sans als WOFF2 ein (für PDF *und* Editor) |
| `add_*.py`, `patch_nachschlag.py` | Einmalskripte vergangener Änderungen, nur Historie |
| `out/` | Erzeugnisse, nicht von Hand bearbeiten |

### Datenformat

```json
{
  "meta":   { "titel": "...", "fusszeile": "Faktenkarte" },
  "themen": ["SONNENSYSTEM", "..."],
  "karten": [
    { "nr": 1, "thema": "SONNENSYSTEM", "titel": "...",
      "text": "...", "nachschlag": "..." }
  ]
}
```

- `thema` **muss** in `themen` vorkommen.
- Reihenfolge in `themen` bestimmt die Reihenfolge der Karten im Stapel.
- `nr` wird beim Sortieren neu vergeben, nie von Hand pflegen.
- Hochzahlen als `10<sup>67</sup>`. Nur `<sup>` ist erlaubt, alles
  andere wird escaped.

Stand: **170 Karten, 10 Themen**, jedes Thema ein zusammenhängender
Nummernblock (Sonnensystem 1–27 … Project Hail Mary 141–170).

---

## Der Auto-Fit ist der Kern

`AUTOFIT_JS` in `build_cards.py` ist ein JS-Schnipsel, der **im Browser**
jede gerenderte Karte vermisst und die Schriftgröße anpasst: kurze Texte
wachsen, lange schrumpfen. Ablauf je Karte:

1. wachsen, solange Platz ist (bis `maxText`)
2. schrumpfen, falls übergelaufen (bis `minText`)
3. Notbremse: Titel verkleinern (bis `minTitel`)
4. zu breite Wörter: betroffenes Element verkleinern

Rückgabe je Karte: `{nr, pt, eng, langwort}`.
`eng` = passt selbst beim Minimum nicht. `langwort` = ein Wort ist
breiter als die Spalte.

**Der Editor führt exakt dieselbe Funktion aus.** `build_editor.py`
kopiert `AUTOFIT_JS` und `FORMATE` aus `build_cards.py` in die HTML-Datei.
Nicht duplizieren, nicht nachbauen – sonst driften Vorschau und Druck
auseinander.

Warum kein Vorausberechnen aus der Zeichenzahl: Deutsche Komposita
(„Hintergrundstrahlung") brechen früh um und erzeugen Extrazeilen. Ein
früherer Versuch über Zeichenzahl hat Karten abgeschnitten.

---

## Fallen, die schon zugeschlagen haben

Diese Punkte sind teuer erkauft. Bitte nicht „aufräumen".

**Schrift wird eingebettet.** DejaVu Sans ist auf Windows nicht
installiert. Ohne `fonts.py` bricht der Satz dort anders um als in den
mitgelieferten PDFs. Betrifft PDF *und* Editor.

**`hyphens: manual`, nicht `auto`.** Automatische Silbentrennung hängt
davon ab, ob das System ein deutsches Trennwörterbuch mitbringt – Windows
ja, Linux-Container nein. Sonst wäre die Ausgabe maschinenabhängig.
Selbst gesetzte bedingte Trennstriche (U+00AD) wirken weiterhin.

**Alle Linien und Marken sind Rahmen, keine Hintergrundflächen.**
Browser drucken Hintergründe nur, wenn im Dialog „Hintergrundgrafiken"
angehakt ist – standardmäßig aus. Mit `background` verschwinden
Schnittlinien im PDF spurlos.

**`overflow-wrap: break-word` muss bleiben.** `.card` hat
`overflow: hidden`; ohne Notumbruch verschwindet zu breiter Text
lautlos aus dem PDF.

**Zeilenhöhen überall explizit setzen.** `.mehr-label` und `.card-foot`
erbten sonst `normal` im Druck und `1.5` im Editor – das reichte, um die
angezeigte Druckgröße um einen Schritt zu verfälschen.

**Fensterbreite beim Bauen ≥ 1400 px.** Querformat-Bögen sind 297 mm
≈ 1123 px breit. In einem schmaleren Fenster misst der Auto-Fit ein
gestauchtes Layout und liefert andere Schriftgrade.

**Jeder Textblock steht für sich.** Karten werden einzeln vorgelesen.
Weder `text` noch `nachschlag` dürfen mit einem Bezugswort ohne
Bezugswort beginnen („Sie", „Dabei", „Damit", „Dieser").

---

## Formate

In `FORMATE` (`build_cards.py`) definiert, vom Editor übernommen.

| Schlüssel | Karte | Bogen | pro Bogen |
|---|---|---|---|
| `a7` | 105 × 74,25 mm | A4 hoch | 8 |
| `a6` | 105 × 148,5 mm | A4 hoch | 4 |
| `a6q` | 148,5 × 105 mm | **A4 quer** | 4 |

Ein neues Format braucht: Eintrag in `FORMATE`, `.f-<key>`-Block in
`cards.css`, bei Querformat zusätzlich `quer: True` (setzt `@page` auf
`landscape` und die Klasse `quer` auf den Bogen).

### Schalter oben in `build_cards.py`

- `MIT_NACHSCHLAG` – Absatz „Mehr dazu" mitdrucken
- `SCHNITTLINIEN` – Schnittlinien und Anlegemarken
- `DUPLEX` – Vorderseite nur Thema + Titel, Text auf der Rückseite;
  Rückseitenbögen werden zeilenweise gespiegelt (Wenden an langer Kante)

Im Editor entsprechen diesen Schaltern Kästchen über der Vorschau.

---

## Editor

Eine einzelne HTML-Datei, offline lauffähig, ohne Installation.
Enthält Daten, Layout, Schrift und den Auto-Fit.

Funktionen: Suche, Themenfilter, Bearbeiten, Hinzufügen, Duplizieren,
Löschen (Detailansicht **und** × in der Liste), Umsortieren per Ziehen,
„Nach Thema sortieren", `facts.json` laden/sichern, PDF drucken.

**Die Druckgrößen-Anzeige ist der Zweck der Oberfläche.** Sie zeigt beim
Tippen, in welcher Größe der Text tatsächlich gedruckt wird, mit Skala
und Bereichen (zu klein / grenzwertig / gut lesbar). Grenzen in `LESBAR`.

**PDF-Druck** nutzt die Druckfunktion des Browsers, keine PDF-Bibliothek:
Die Bögen werden in `#druckflaeche` aufgebaut, `@media print` blendet
alles andere aus. Ergebnis ist wortgleich mit `build_cards.py`.

Bleibt die Startmeldung stehen, läuft das Skript nicht – meist, weil die
Datei in einer Vorschau statt im Browser geöffnet wurde.

Oberfläche dunkel, Karte immer schwarz auf weiß.
`localStorage` wird bewusst nicht verwendet; Sichern läuft über Download.

---

## Prüfen vor dem Ausliefern

Nach Änderungen an Daten, `cards.css` oder dem Auto-Fit:

1. **Kein Überlauf.** `build_cards.py` meldet `ACHTUNG` bei `eng` oder
   `langwort`. Muss leer bleiben, in allen Formaten und beiden Modi.
2. **Vorschau = Druck.** Aus dem Editor ein PDF erzeugen und die
   Wortpositionen aller Seiten mit dem Skript-PDF vergleichen. Muss
   identisch sein. Beim Vergleich für **beide** `page.pdf()`-Aufrufe
   dieselben Parameter verwenden, sonst entstehen Scheinabweichungen.
3. **Nummern lückenlos** 1..n, jedes Thema zusammenhängend.
4. **Keine hängenden Satzanfänge** (Regex-Prüfung, siehe oben).
5. **Seitengeometrie:** 210 × 297 mm, bei `a6q` 297 × 210 mm.

---

## Stil

- Deutsche Bezeichner und Kommentare im Projektcode.
- Kommentare erklären *warum*, nicht *was* – vor allem bei den Fallen.
- Karten: zwei bis drei Sätze, ohne Vorwissen verständlich, keine
  Ausrufezeichen, Zahlen mit deutschem Dezimalkomma.
- Fakten müssen stimmen und überprüfbar sein. Im Zweifel weglassen.
