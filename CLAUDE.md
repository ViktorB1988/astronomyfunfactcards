# Astronomie-Faktenkarten

Druckbare Faktenkarten zum Vorlesen für Besucher einer Sternwarte.
Aus einer JSON-Datenquelle entstehen PDFs in drei Formaten sowie ein
eigenständiger HTML-Editor.

## Sprache

Zwei Ebenen, klar getrennt:

- **Code ist englisch.** Bezeichner, Kommentare, CSS-Klassen, Feldnamen in
  `facts.json` und in der Datenbank, Namen der Workflow-Schritte.
- **Alles Sichtbare bleibt deutsch.** Kartentexte, Beschriftungen der
  Oberfläche, Status- und Fehlermeldungen, Konsolenausgaben der
  Bauskripte. Die Karten werden deutschsprachigem Publikum vorgelesen,
  und die Oberfläche bedienen Ehrenamtliche der Sternwarte.

Wer eine Zeichenkette anfasst, prüft also zuerst, ob sie jemand liest.

---

## Schnellstart

```bash
pip install playwright fonttools brotli
playwright install chromium

python3 build_cards.py          # alle PDFs nach ./out
python3 build_cards.py a7       # nur ein Format
python3 build_editor.py         # Editor nach ./out/karten-editor.html
python3 build_web.py            # Online-Fassung nach ./site
python3 fetch_facts.py          # Stand aus Firestore -> facts.json
```

`build_editor.py` und `build_web.py` importieren `build_cards.py`. Nach jeder
Änderung an `facts.json` oder `cards.css` die betroffenen Skripte laufen
lassen, sonst enthalten Editor und Seite einen veralteten Stand.

---

## Dateien

| Datei | Rolle |
|---|---|
| `facts.json` | **Einzige Datenquelle.** Themenliste + Karten |
| `cards.css` | **Einziges Layout.** Kartenmaße, Schriftgrade, Schnittlinien |
| `build_cards.py` | Baut die PDFs. Enthält `FORMATS` und den Auto-Fit |
| `editor_template.html` | Vorlage des Editors mit Platzhaltern |
| `build_editor.py` | Setzt Vorlage + `cards.css` + `facts.json` + Schrift zusammen |
| `fonts.py` | Bettet DejaVu Sans als WOFF2 ein (für PDF *und* Editor) |
| `build_web.py` | Baut die Online-Fassung nach `site/` |
| `web/firebase-app.js` | Datenbankanbindung der Online-Fassung |
| `web/firebase-config.js` | Projektkennung. Kein Geheimnis, siehe unten |
| `firestore.rules` | **Die eigentliche Zugriffssperre** |
| `fetch_facts.py` | Holt den Stand aus Firestore zurück in `facts.json` |
| `add_*.py`, `patch_nachschlag.py` | Einmalskripte vergangener Änderungen, nur Historie. **Laufen nicht mehr:** sie sprechen die alten deutschen Feldnamen an. Bewusst nicht mitgezogen – sie sind Geschichte, nicht Werkzeug |
| `out/`, `site/` | Erzeugnisse, nicht von Hand bearbeiten |

### Datenformat

```json
{
  "meta":   { "title": "...", "footer": "Faktenkarte" },
  "themes": ["SONNENSYSTEM", "..."],
  "cards": [
    { "no": 1, "theme": "SONNENSYSTEM", "title": "...",
      "text": "...", "more": "..." }
  ]
}
```

- `theme` **muss** in `themes` vorkommen.
- Reihenfolge in `themes` bestimmt die Reihenfolge der Karten im Stapel.
- `no` wird beim Sortieren neu vergeben, nie von Hand pflegen.
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
3. Notbremse: Titel verkleinern (bis `minTitle`)
4. zu breite Wörter: betroffenes Element verkleinern

Rückgabe je Karte: `{no, pt, tight, longWord}`.
`tight` = passt selbst beim Minimum nicht. `longWord` = ein Wort ist
breiter als die Spalte.

**Der Editor führt exakt dieselbe Funktion aus.** `build_editor.py`
kopiert `AUTOFIT_JS` und `FORMATS` aus `build_cards.py` in die HTML-Datei.
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

**Zeilenhöhen überall explizit setzen.** `.more-label` und `.card-foot`
erbten sonst `normal` im Druck und `1.5` im Editor – das reichte, um die
angezeigte Druckgröße um einen Schritt zu verfälschen.

**Fensterbreite beim Bauen ≥ 1400 px.** Querformat-Bögen sind 297 mm
≈ 1123 px breit. In einem schmaleren Fenster misst der Auto-Fit ein
gestauchtes Layout und liefert andere Schriftgrade.

**Jeder Textblock steht für sich.** Karten werden einzeln vorgelesen.
Weder `text` noch `more` dürfen mit einem Bezugswort ohne
Bezugswort beginnen („Sie", „Dabei", „Damit", „Dieser").

---

## Formate

In `FORMATS` (`build_cards.py`) definiert, vom Editor übernommen.

| Schlüssel | Karte | Bogen | pro Bogen |
|---|---|---|---|
| `a7` | 105 × 74,25 mm | A4 hoch | 8 |
| `a6` | 105 × 148,5 mm | A4 hoch | 4 |
| `a6q` | 148,5 × 105 mm | **A4 quer** | 4 |

Ein neues Format braucht: Eintrag in `FORMATS`, `.f-<key>`-Block in
`cards.css`, bei Querformat zusätzlich `landscape: True` (setzt `@page` auf
`landscape` und die Klasse `landscape` auf den Bogen).

### Schalter oben in `build_cards.py`

- `WITH_MORE` – Absatz „Mehr dazu" mitdrucken
- `CUT_LINES` – Schnittlinien und Anlegemarken
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
und Bereichen (zu klein / grenzwertig / gut lesbar). Grenzen in `READABLE`.

**PDF-Druck** nutzt die Druckfunktion des Browsers, keine PDF-Bibliothek:
Die Bögen werden in `#printarea` aufgebaut, `@media print` blendet
alles andere aus. Ergebnis ist wortgleich mit `build_cards.py`.

Bleibt die Startmeldung stehen, läuft das Skript nicht – meist, weil die
Datei in einer Vorschau statt im Browser geöffnet wurde.

Oberfläche dunkel, Karte immer schwarz auf weiß.
`localStorage` wird bewusst nicht verwendet; Sichern läuft über Download.

---

## Online-Fassung (GitHub Pages + Firestore)

Dieselbe Oberfläche, nur mit Datenbank statt Datei. `build_web.py` baut
sie nach `site/`, ein Workflow stellt sie auf GitHub Pages.

**Es gibt genau eine Vorlage.** `editor_template.html` trägt beide
Fassungen. `build_web.py` unterscheidet sich von `build_editor.py` nur
darin, dass es an der Stelle `<!--__FIREBASE__-->` das Modul einhängt.
Bleibt die Stelle leer, entsteht der unveränderte Offline-Editor. Nicht
in zwei Vorlagen aufteilen – dann driften Auto-Fit und Layout auseinander.

**Das Modul fasst den Zustand nie direkt an,** nur über `window.Editor`
(`holeStand`, `setzeStand`, `setzeSchreibrecht`, …). Es läuft als
`type="module"` und damit garantiert nach dem Hauptskript.

### Aufteilung in der Datenbank

| Ort | Inhalt |
|---|---|
| `cards/<id>` | je Karte ein Dokument: `pos`, `theme`, `title`, `text`, `more` |
| `config/meta` | `title`, `footer`, `themes` (Liste, Reihenfolge zählt) |
| `config/editors` | `emails`: wer schreiben darf. **Nur von Hand in der Konsole** |

`no` steht **nicht** in der Datenbank. Sie ist abgeleitet – würde man sie
speichern, fasste jedes Umsortieren alle 170 Dokumente an. Geordnet wird
über `pos`, `no` entsteht beim Laden neu.

Jede Karte trägt zusätzlich eine `id`, die nur im Browser lebt: sie ist der
Dokumentschlüssel. Ohne sie wäre nach einem Umsortieren nicht mehr
feststellbar, welche Karte welches Dokument ist, und Speichern vertauschte
Karten, statt sie zu ändern. In `facts.json` taucht sie nicht auf – das
Dateiformat bleibt wie dokumentiert.

### Fallen der Online-Fassung

**`firestore.rules` ist die Sperre, nicht die Oberfläche.** Die Seite ist
öffentlich, ihr Quelltext samt Firebase-Schlüssel für jeden lesbar. Das
Nur-Lesen im Editor ist Höflichkeit; wer schreiben darf, entscheidet allein
die Regeldatei. Änderungen dort müssen veröffentlicht werden, sonst gilt
weiter der alte Stand.

**Der Firebase-Web-Schlüssel ist kein Geheimnis.** Er benennt nur das
Projekt. Ihn in ein Secret zu verstecken bringt nichts und macht den Bau
kaputt – er steht im Klartext in `web/firebase-config.js`.

**Die Redaktionsliste (`config/editors`) ist über die Regeln nicht
beschreibbar.** Sonst könnte sich ein Redaktionskonto weitere Konten
eintragen, und die Liste wäre keine Grenze mehr. Anlegen und ändern nur in
der Konsole.

**Ein Schnappschuss fährt niemandem ins Tippen.** Kommt eine fremde
Änderung herein, während `S.dirty` gesetzt ist, wird sie zurückgestellt und
erst nach dem Speichern übernommen. Ohne das verschwänden halbe Sätze unter
den Fingern.

**Gespeichert wird im Abgleich, nicht im Rundumschlag.** Geschrieben wird
nur, was sich geändert hat. Ein voller Durchlauf kostete sonst 170
Schreibvorgänge je Klick und überschriebe parallele Änderungen anderer.

**Eigene Schreibvorgänge nicht auf sich selbst zurückspielen.**
`schnapp.metadata.hasPendingWrites` filtert das lokale Echo – sonst setzt
sich beim Tippen der Cursor um.

**Leere Datenbank heißt: nichts übernehmen.** Der Editor zeigt dann weiter
den eingebauten Stand aus `facts.json`, und genau der lässt sich mit einem
Klick hochspielen. Ein leerer Schnappschuss darf die Anzeige nicht leeren.

**Gebaut wird auf Ubuntu.** `fonts.py` sucht DejaVu Sans unter
`/usr/share/fonts`; unter Windows liegt sie dort nicht. Der Workflow prüft
nach dem Bauen, ob wirklich eine Schrift eingebettet wurde – ohne sie sähe
die Seite richtig aus und zeigte trotzdem falsche Druckgrößen an.

### PDFs bleiben am Dateiweg

`build_cards.py` liest weiter `facts.json`. Nach Änderungen online also
`python3 fetch_facts.py` (liest über die öffentliche REST-Schnittstelle,
ohne Anmeldung), dann `build_cards.py`.

---

## Prüfen vor dem Ausliefern

Nach Änderungen an Daten, `cards.css` oder dem Auto-Fit:

1. **Kein Überlauf.** `build_cards.py` meldet `ACHTUNG` bei `tight` oder
   `longWord`. Muss leer bleiben, in allen Formaten und beiden Modi.
2. **Vorschau = Druck.** Aus dem Editor ein PDF erzeugen und die
   Wortpositionen aller Seiten mit dem Skript-PDF vergleichen. Muss
   identisch sein. Beim Vergleich für **beide** `page.pdf()`-Aufrufe
   dieselben Parameter verwenden, sonst entstehen Scheinabweichungen.
3. **Nummern lückenlos** 1..n, jedes Thema zusammenhängend.
4. **Keine hängenden Satzanfänge** (Regex-Prüfung, siehe oben).
5. **Seitengeometrie:** 210 × 297 mm, bei `a6q` 297 × 210 mm.

---

## Stil

- Englische Bezeichner und Kommentare, deutsche Ausgaben – siehe oben.
- Kommentare erklären *warum*, nicht *was* – vor allem bei den Fallen.
- Karten: zwei bis drei Sätze, ohne Vorwissen verständlich, keine
  Ausrufezeichen, Zahlen mit deutschem Dezimalkomma.
- Fakten müssen stimmen und überprüfbar sein. Im Zweifel weglassen.
