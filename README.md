# Astronomie-Faktenkarten – 170 Karten

Karten zum Vorlesen für Besucherinnen und Besucher auf der Sternwarte.
Fortlaufend von 1 bis 170. Standardmäßig **einseitig**; wahlweise auch
als **Duplex-Fassung** mit Titel vorn und Text hinten.
Layout bewusst rein schwarz/weiß: Unter Rotlicht verschwinden Farben,
neutrale Graustufen bleiben lesbar.

## Dateien

| Datei | Karten/Bogen | Bögen | Schriftgrad Fakt |
|---|---|---|---|
| `astro-karten-A7.pdf` | 8 | 22 | 10,3–13,7 pt |
| `astro-karten-A7-nur-fakt.pdf` | 8 | 22 | **13,3–14,1 pt** |
| `astro-karten-A6.pdf` | 4 | 43 | 12,1–18,1 pt |
| `astro-karten-A6-nur-fakt.pdf` | 4 | 43 | **15,1–21,1 pt** |
| `astro-karten-A6Q.pdf` | 4 | 43 | 14,3–18,8 pt |
| `astro-karten-A6Q-nur-fakt.pdf` | 4 | 43 | **18,0–20,3 pt** |
| `astro-karten-A7-duplex.pdf` | 8 | 44 | 10,3–13,7 pt (Rückseite) |
| `astro-karten-A6-duplex.pdf` | 4 | 86 | 14,0–19,3 pt (Rückseite) |
| `astro-karten-A6Q-duplex.pdf` | 4 | 86 | 14,3–19,4 pt (Rückseite) |

Dazu `astro-karten-index.pdf` (Übersicht nach Themen), der Editor
`karten-editor.html` sowie die Quellen `facts.json`, `cards.css`,
`build_cards.py`, `build_editor.py`, `editor_template.html`, `fonts.py`.

## Welche Variante?

Die **„nur-fakt"-Varianten** enthalten nur den eigentlichen Fakt. Die
anderen drucken zusätzlich den Zusatzabsatz „Mehr dazu" unten auf die
Karte – nützlich für Rückfragen, kostet aber spürbar Schriftgröße.

**Auf A7 ist der Unterschied entscheidend:** mit Zusatz landet der
Fakt im Median bei 11,5 pt, ohne Zusatz bei 14,1 pt. Zum Vorlesen im
Halbdunkel sind 11 pt grenzwertig, 14 pt gehen gut. Wer den Zusatz
braucht, ist mit A6 besser bedient.

| Format | Kartengröße | Bogen |
|---|---|---|
| A7 | 105 × 74,25 mm (quer) | A4 hoch, 8 Karten |
| A6 hoch | 105 × 148,5 mm | A4 hoch, 4 Karten |
| A6 quer | 148,5 × 105 mm | A4 quer, 4 Karten |

**A6 quer lohnt sich.** Die Fläche ist dieselbe wie bei A6 hoch, aber die
Textspalte ist mit 128,5 statt 85 mm deutlich breiter. Das ergibt weniger
Zeilenumbrüche und damit größere Schrift – vor allem bei den langen Karten:
Der kleinste Schriftgrad steigt von 12,1 auf 14,3 pt, im Median von 15,1
auf 16,5 pt. Ohne „Mehr dazu“ liegt A6 quer bei durchweg 18 pt und mehr.

Zu beachten: Der Bogen läuft dann im **Querformat** durch den Drucker.

## Duplex: Titel vorn, Text hinten

Die Dateien mit `-duplex` im Namen sind anders aufgebaut: Vorn stehen nur
Thema, Nummer und Titel, groß in der Kartenmitte, dazu der Hinweis
„bitte wenden". Der Fakt und „Mehr dazu" stehen auf der Rückseite unter
der Überschrift „Antwort".

Das eignet sich zum Vorlesen mit Publikum: Titel zeigen oder vorlesen,
raten lassen, umdrehen. Nebenbei bringt es mehr Platz – der Text auf der
Rückseite wird deutlich größer als auf der einseitigen Karte:

| Format | einseitig | Duplex-Rückseite |
|---|---|---|
| A7 | 10,3–13,7 pt | 10,3–13,7 pt, Titel vorn bis 22 pt |
| A6 | 12,1–18,1 pt | 14,0–19,3 pt, Titel vorn bis 34 pt |

**Drucken:** beidseitig, **Wenden an der langen Kante** (Standard bei
Hochformat). Die Rückseiten sind dafür bereits gespiegelt angeordnet –
Bogen 1 trägt vorn die Karten 1–8, hinten dieselben in der Reihenfolge
2·1 / 4·3 / 6·5 / 8·7, damit sie nach dem Wenden passen.

Im Editor schaltet das Kästchen **„Duplex: Titel vorn, Text hinten"**
denselben Modus für Vorschau und PDF-Druck ein. Die Vorschau zeigt dann
beide Seiten untereinander.

Im Skript steht der Schalter als `DUPLEX` oben in `build_cards.py`.

## Drucken

1. **Papier:** 250–300 g/m² Karton, **matt** (glänzend spiegelt Stirnlampen).
2. **Skalierung: 100 % / „Tatsächliche Größe"** – *nicht* „An Seite anpassen".
   Sonst stimmen die Schnittmarken nicht mehr.
3. **Einseitig** – außer bei den `-duplex`-Dateien, siehe oben.
   Die Einstellung „Hintergrundgrafiken" ist egal – die Schnittlinien
   sind Rahmen und drucken immer mit.
4. Erst eine Testseite drucken, schneiden und unter der echten
   Rotlichtbeleuchtung gegenlesen, dann den Rest.

Die Karten stehen fortlaufend auf dem Bogen, zeilenweise von links oben:
A7-Bogen 1 trägt die Karten 1–8, Bogen 2 die Karten 9–16 und so weiter.
Der letzte A7-Bogen enthält die Karten 97–100 und vier Leerfelder.

## Schneiden

- Schnittlinien: die feinen grauen Linien auf dem Bogen.
  A7: eine senkrechte, drei waagerechte. A6: je eine.
  Abschaltbar über `SCHNITTLINIEN = False` in `build_cards.py`
  bzw. das Kästchen „Schnittlinien drucken" im Editor.
- Zusätzlich schwarze Marken an den Bogenrändern zum Anlegen.
- Außenkanten müssen nicht geschnitten werden – die Karten liegen
  exakt auf dem A4-Raster.
- Mit Stapelschneider mehrere Bögen gleichzeitig: erst alle waagerechten
  Schnitte, dann die senkrechten.

## Themen

Die Karten liegen nach Themen gruppiert im Stapel, jedes Thema hat einen
eigenen Nummernblock:

| Thema | Karten | Nummern |
|---|---|---|
| Sonnensystem | 27 | 1–27 |
| Sterne & Sternenreste | 8 | 28–35 |
| Schwarze Löcher | 22 | 36–57 |
| Zeitdilatation | 13 | 58–70 |
| Raumfahrt & Reisen | 7 | 71–77 |
| Galaxien & Kosmos | 11 | 78–88 |
| Ende des Universums | 12 | 89–100 |
| Star Trek | 20 | 101–120 |
| Star Wars | 20 | 121–140 |
| Project Hail Mary | 30 | 141–170 |

Die Karten zu Star Trek, Star Wars und Project Hail Mary nennen jeweils
einen Bezug aus den Filmen und daneben den astronomischen Sachverhalt
dahinter – vom Stern 40 Eridani über den echten Doppelsonnen-Planeten
Kepler-16b bis zu der Frage, wie viel Energie das Sprengen eines
Planeten kosten würde.

Die Project-Hail-Mary-Karten bleiben bewusst bei dem, was Trailer und
Klappentext ohnehin verraten: die schwächer werdende Sonne, das Ziel
Tau Ceti und der Stern 40 Eridani. Wendungen aus der zweiten Hälfte der
Handlung kommen nicht vor – die Karten lassen sich also auch vor
Publikum vorlesen, das den Film noch nicht kennt.

Das Thema steht oben links auf jeder Karte im Klartext. Eine zusätzliche
Randmarke gibt es nicht; da der Stapel nach Themen sortiert ist, findet
man ein Thema über seinen Nummernblock oder über `astro-karten-index.pdf`.

Die Reihenfolge der Themen steht in `facts.json` unter `themen`. Wer sie
dort umstellt, ändert damit die Reihenfolge der Karten im Stapel.

Jeder Textblock nennt sein Thema selbst und ist ohne die anderen Karten
verständlich – auch der Zusatzabsatz, wenn man ihn allein vorliest.

## Karten ändern: der Editor

`karten-editor.html` **herunterladen, lokal speichern und doppelklicken.**
Eine einzelne Datei, kein Server, kein Internet, keine Installation. Sie
enthält den aktuellen Kartenstand bereits.

Wichtig ist das Herunterladen: In Vorschaufenstern – etwa in einem Chat,
einem Dateimanager oder auf einer Weboberfläche – werden Skripte oft
blockiert. Der Editor bleibt dann leer und keine Schaltfläche reagiert.
Passiert das, erscheint jetzt ein Hinweiskasten, der genau das erklärt.
Steht dort stattdessen ein roter Fehlertext, liegt ein echter Fehler im
Editor vor.

- **Links** die Kartenliste mit Suche und Themenfilter. Unter jedem Titel
  steht das zugehörige Thema. Rechts in jeder Zeile erscheint beim
  Überfahren ein **×** zum direkten Löschen – nachgefragt wird trotzdem.
- **Mitte** Thema, Titel, Fakt und „Mehr dazu“ bearbeiten. Darunter
  Karte verschieben, duplizieren oder löschen.
  Unten links sortiert **„Nach Thema sortieren"** den ganzen Stapel wieder
  in die Themenreihenfolge und nummeriert ihn neu durch – praktisch,
  nachdem Karten hinzugekommen sind.
  Einzelne Karten lassen sich außerdem **mit der Maus umsortieren**:
  Zeile greifen, an die neue Stelle ziehen, loslassen. Eine Linie zeigt,
  wo die Karte landet. Das funktioniert auch bei gefilterter Liste, weil
  immer relativ zur Karte eingefügt wird, auf der man loslässt.
  Nach jedem Verschieben wird neu durchnummeriert.
- **Rechts** die Karte in echter Größe, umschaltbar zwischen A7 und A6.

Die Oberfläche ist dunkel gehalten, damit die Karte als einzige helle
Fläche heraussticht – so sieht man sie ungefähr so, wie sie später als
weißes Kärtchen in der Hand liegt. Die Karte selbst bleibt immer
schwarz auf weiß, unabhängig vom Aussehen der Oberfläche.

**Die Anzeige „pt Druckgröße“ ist der eigentliche Zweck.** Sie rechnet
mit demselben Auto-Fit wie der PDF-Bau und mit derselben eingebetteten
Schrift, zeigt also beim Tippen die Größe, in der der Text tatsächlich
gedruckt wird – grün ab 12,5 pt (A7) bzw. 15 pt (A6), gelb darunter,
rot wenn es zum Vorlesen zu klein wird. So sieht man sofort, ob ein
zusätzlicher Satz die Karte unlesbar macht.

Daneben wird gewarnt bei leeren Feldern, doppelten Titeln und bei
Texten, die mit einem Bezugswort wie „Sie“ oder „Dabei“ beginnen –
jede Karte wird einzeln vorgelesen und muss für sich stehen.

**Zu lange Wörter** meldet der Editor ebenfalls. Ist ein einzelnes Wort
breiter als die Kartenspalte, verkleinert der Auto-Fit zunächst die
Schrift. Reicht das nicht bis zum kleinsten erlaubten Grad, wird das Wort
mitten im Wort umbrochen – dann erscheint eine rote Meldung mit dem
betroffenen Wort. Abhilfe: kürzeres Wort, anderes Format, oder ein
**bedingter Trennstrich** an der gewünschten Trennstelle
(Windows: Alt + 0173). Das bringt oft viel Größe zurück – bei
„Rindfleisch­etikettierungs­überwachungs­gesetz“ auf A6 von 11,0 auf 17,4 pt.

Zum Schluss **„facts.json sichern“** (oder Strg+S) und die
heruntergeladene Datei über die alte `facts.json` legen. Danach
`python3 build_cards.py` für die neuen PDFs.

Umgekehrt holt **„facts.json laden“** einen vorhandenen Stand in den
Editor – wahlweise über den Knopf oder indem man die Datei einfach aufs
Fenster zieht. Nach dem Laden erscheint unten eine Meldung mit Dateiname
und Kartenzahl; passt etwas nicht, steht dort rot, woran es liegt.

Die Kartennummern vergibt der Editor fortlaufend neu, sobald Karten
hinzukommen, wegfallen oder die Reihenfolge sich ändert – die
Nummerierung bleibt damit immer lückenlos 1 bis n.

Nach Änderungen an `facts.json` oder `cards.css` den Editor mit
`python3 build_editor.py` neu bauen, damit er den aktuellen Stand
und das aktuelle Layout enthält.

## Karten ändern: direkt in der Datei

Alles steht in `facts.json`:

```json
{
  "nr": 101,
  "thema": "SONNENSYSTEM",
  "titel": "Kurzer Titel",
  "text": "Der Fakt, zwei bis drei Sätze, in sich verständlich.",
  "nachschlag": "Ein Satz Zusatzinfo für den Absatz „Mehr dazu\"."
}
```

Danach neu bauen:

```bash
pip install playwright
playwright install chromium
python3 build_cards.py          # beide Formate
python3 build_cards.py a7       # nur A7
python3 build_editor.py         # Editor neu bauen
```

Für den Editor wird zusätzlich `fonttools` und `brotli` gebraucht
(`pip install fonttools brotli`).

Für die Varianten ohne Zusatzabsatz `MIT_NACHSCHLAG = False` oben in
`build_cards.py` setzen.

**Auto-Fit:** Das Skript misst nach dem Rendern jede einzelne Karte im
Browser und passt die Schriftgröße an die tatsächlich vorhandene Höhe an –
kurze Texte wachsen, lange schrumpfen. Reine Zeichenzahl reicht als
Schätzung nicht: deutsche Komposita wie „Hintergrundstrahlung" brechen
früh um und erzeugen Extrazeilen. Beim Bauen wird der erreichte
Schriftgradbereich gemeldet.

Passt eine Karte selbst beim kleinsten erlaubten Grad nicht
(A7: 7,5 pt, A6: 11 pt), erscheint eine Warnung – dann ist der Text
zu lang und sollte gekürzt werden.

Weitere Hinweise:

- Für Hochzahlen `10<sup>67</sup>` schreiben.
- `thema` muss einem Eintrag aus der Liste `themen` entsprechen. Neue Themen
  dort ergänzen; die Position in dieser Liste bestimmt, wo der Themenblock
  im Stapel liegt.
- Die Fußzeile lässt sich unter `meta.fusszeile` ändern, z. B. auf den
  Vereinsnamen. Auf A7 ist sie ausgeblendet, dort fehlt der Platz.
- Ober- und Untergrenze der Schriftgröße stehen als `minText` / `maxText`
  im Dictionary `FORMATE` in `build_cards.py`.
- Ein neues Format ergänzt man dort plus einem `.f-xx`-Block in `cards.css`.
  Der Editor übernimmt beides automatisch beim nächsten Bauen.
- Die Schrift DejaVu Sans wird über `fonts.py` in PDF *und* Editor
  eingebettet. Das ist nötig, weil sie auf Windows normalerweise fehlt:
  ohne Einbettung würde der Satz dort anders umbrechen als hier.
- Aus demselben Grund steht die Silbentrennung auf `hyphens: manual`.
  Die automatische Trennung hängt davon ab, ob das Betriebssystem ein
  deutsches Trennwörterbuch mitbringt – unter Windows ja, auf dem
  Baurechner nein. Die Ausgabe wäre also je nach Maschine anders
  umbrochen. Selbst gesetzte bedingte Trennstriche wirken weiterhin.
- Läuft ein Wort trotzdem über die Spalte, greift `overflow-wrap:
  break-word`: lieber ein hässlicher Umbruch als Text, der von
  `overflow: hidden` lautlos abgeschnitten wird. Der Bau meldet solche
  Stellen mit Kartennummer und Wort.

## Praxistipps

- In der Kuppel wird es feucht und kalt. Wer Karten dauerhaft nutzt,
  sollte eine Auswahl laminieren – dann aber **matt**, nicht glänzend.
- Ein Gummiband und eine Blankokarte als Deckel oben und unten
  schützen den Stapel im Rucksack.
