# Astronomie-Faktenkarten – 218 Karten

Karten zum Vorlesen für Besucherinnen und Besucher auf der Sternwarte.
Fortlaufend von 1 bis 218. Standardmäßig **einseitig**; wahlweise auch
als **Duplex-Fassung** mit Titel vorn und Text hinten.
Layout bewusst rein schwarz/weiß: Unter Rotlicht verschwinden Farben,
neutrale Graustufen bleiben lesbar.

## Dateien

Die Schriftgrade unten sind Anhaltswerte. Den genauen Bereich meldet
`build_cards.py` bei jedem Lauf – er hängt am Text der Karten.

| Datei | Karten/Bogen | Bögen | Schriftgrad Fakt ≈ |
|---|---|---|---|
| `astro-karten-A7.pdf` | 8 | 28 | 10,3–13,7 pt |
| `astro-karten-A7-nur-fakt.pdf` | 8 | 28 | **13,3–14,1 pt** |
| `astro-karten-A6.pdf` | 4 | 55 | 12,1–18,1 pt |
| `astro-karten-A6-nur-fakt.pdf` | 4 | 55 | **15,1–21,1 pt** |
| `astro-karten-A6Q.pdf` | 4 | 55 | 14,3–18,8 pt |
| `astro-karten-A6Q-nur-fakt.pdf` | 4 | 55 | **18,0–20,3 pt** |
| `astro-karten-A7-duplex.pdf` | 8 | 56 | 10,3–13,7 pt (Rückseite) |
| `astro-karten-A6-duplex.pdf` | 4 | 110 | 14,0–19,3 pt (Rückseite) |
| `astro-karten-A6Q-duplex.pdf` | 4 | 110 | 14,3–19,4 pt (Rückseite) |

Dazu `astro-karten-index.pdf` (Übersicht nach Themen), der Editor
`karten-editor.html` sowie die Quellen `facts.json`, `cards.css`,
`build_cards.py`, `build_editor.py`, `editor_template.html`, `fonts.py`.

Für die Fassung im Netz zusätzlich `build_web.py`, `web/`, `firestore.rules`
und `fetch_facts.py` – siehe [Die Seite im Netz](#die-seite-im-netz).

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
| A7 | 97 × 70,25 mm (quer) | A4 hoch, 8 Karten |
| A6 hoch | 97 × 140,5 mm | A4 hoch, 4 Karten |
| A6 quer | 140,5 × 97 mm | A4 quer, 4 Karten |

Die Maße sind **bewusst etwas kleiner als DIN A7 bzw. A6**. Rundherum
bleiben 8 mm Rand – siehe [Schneiden](#schneiden).

**A6 quer lohnt sich.** Die Fläche ist dieselbe wie bei A6 hoch, aber die
Textspalte ist mit 124,5 statt 81 mm deutlich breiter. Das ergibt weniger
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
   Sonst stimmen die Maße nicht mehr. Seit die Bögen einen Rand haben,
   ist ein versehentliches Verkleinern allerdings kein Beinbruch mehr:
   die Karten werden dann gleichmäßig etwas kleiner, statt ungleich.
3. **Einseitig** – außer bei den `-duplex`-Dateien, siehe oben.
   Die Einstellung „Hintergrundgrafiken" ist egal – die Schnittlinien
   sind Rahmen und drucken immer mit.
4. Erst eine Testseite drucken, schneiden und unter der echten
   Rotlichtbeleuchtung gegenlesen, dann den Rest.

Die Karten stehen fortlaufend auf dem Bogen, zeilenweise von links oben:
A7-Bogen 1 trägt die Karten 1–8, Bogen 2 die Karten 9–16 und so weiter.
Der letzte A7-Bogen trägt die Karten 217–218 und sechs Leerfelder.

## Schneiden

- **Alle vier Seiten werden geschnitten**, die außen liegenden
  eingeschlossen. Rundherum stehen 8 mm Rand, der wegfällt.
- Schnittlinien: die feinen grauen **gepunkteten** Linien auf dem Bogen.
  A7: drei senkrechte, fünf waagerechte. A6: je drei. Gepunktet, damit
  ein nicht ganz genauer Schnitt Pünktchen an der Kartenkante hinterlässt
  statt eines durchgezogenen Strichs.
  Abschaltbar über `CUT_LINES = False` in `build_cards.py`
  bzw. das Kästchen „Schnittlinien drucken" im Editor.
- Zusätzlich schwarze Marken im Rand zum Anlegen. Sie laufen von der
  Papierkante bis zur Ecke des Kartenblocks; das äußere Stück schluckt
  der Drucker, das innere bleibt stehen.
- Mit Stapelschneider mehrere Bögen gleichzeitig: erst alle waagerechten
  Schnitte, dann die senkrechten.

**Warum überhaupt ein Rand?** Kein Bürodrucker druckt bis an die
Papierkante; 3 bis 5 mm bleiben immer frei. Ein Layout, das den Bogen
exakt ausfüllt, lässt dem Treiber nur zwei Möglichkeiten: alles
verkleinern oder abschneiden. Verkleinern ist der Normalfall – und genau
das führte dazu, dass die außen liegenden Karten nach dem Schneiden
anders aussahen als die inneren: innen wurde auf der gedruckten Linie
geschnitten, außen gar nicht, dort blieb der weiße Rand des Treibers
stehen. Mit dem Rand liegt jede Schnittlinie im druckbaren Bereich, jede
Karte wird auf allen vier Seiten geschnitten, und das Ergebnis hängt
nicht mehr davon ab, was der Treiber entschieden hat.

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
| Terraforming Mars | 8 | 171–178 |
| Artemis 2 | 8 | 179–186 |
| Warpantrieb | 8 | 187–194 |
| Fiktion wird wirklich | 8 | 195–202 |
| Neutrinos | 8 | 203–210 |
| Gravitationswellen | 8 | 211–218 |

Die vier jüngsten Themen hängen zusammen: **Terraforming Mars** sammelt,
woran ein Umbau des Nachbarplaneten scheitert, **Artemis 2** beschreibt den
ersten bemannten Mondflug seit 1972, **Warpantrieb** geht der Frage nach,
warum überlichtschnelles Reisen zwar rechenbar, aber nicht baubar ist, und
**Fiktion wird wirklich** sammelt Technik, die zuerst in Romanen und Filmen
auftauchte – vom Mobiltelefon bis zur senkrecht landenden Rakete.

**Neutrinos** und **Gravitationswellen** handeln von den beiden Wegen,
auf denen die Astronomie seit wenigen Jahrzehnten etwas anderes empfängt
als Licht: Teilchen, die durch die ganze Erde fliegen, und ein Zittern des
Raums, das kleiner ist als ein Proton. Bei diesen sechzehn Karten steht
auch die Quelle im Editor.

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

Die Reihenfolge der Themen steht in `facts.json` unter `themes`. Wer sie
dort umstellt, ändert damit die Reihenfolge der Karten im Stapel.

Jeder Textblock nennt sein Thema selbst und ist ohne die anderen Karten
verständlich – auch der Zusatzabsatz, wenn man ihn allein vorliest.

## Die Seite im Netz

Es gibt den Editor zweimal, mit demselben Aussehen und derselben Rechnung:

| | Offline | Online |
|---|---|---|
| Datei | `karten-editor.html` herunterladen | Adresse aufrufen |
| Daten | in der Datei, Sichern per Download | Firestore, für alle gleich |
| Ändern | immer | nur angemeldete Redaktion |
| Braucht | nichts | Internet |

Die Online-Fassung liegt auf GitHub Pages und holt die Karten aus einer
Firestore-Datenbank. **Lesen, Blättern und Drucken kann jeder**, auch ohne
Konto – der Link lässt sich also einfach weitergeben, wenn jemand einen
Satz Karten ausdrucken soll. **Ändern kann nur, wer angemeldet und als
Redaktion eingetragen ist.**

Wer online etwas ändert, drückt **„Speichern"** (oder Strg+S) – der Knopf
steht unter der Karte, bei den übrigen Kartenbefehlen. Danach sehen alle
anderen den neuen Stand sofort.

Die Knöpfe **„facts.json laden"** und **„facts.json sichern"** gibt es
online nicht: dort ist die Datenbank die Quelle, und eine zweite Fassung
als Datei danebenzulegen würde nur auseinanderlaufen. Für den PDF-Bau
holt `fetch_facts.py` den Stand, ganz ohne Browser.

### Größere Änderungen einspielen

Für den umgekehrten Weg – viele Karten auf einmal in die Datenbank – gibt
es **„JSON einspielen"**. Der Knopf erscheint nur für Konten, die in
`config/editors` zusätzlich unter `import` eingetragen sind.

Eingespielt wird **zusammengeführt, nicht ersetzt**: Karten werden an
ihrer `id` wiedererkannt und behalten sie, sodass das anschließende
Speichern nur die tatsächlichen Unterschiede schreibt. Eine umbenannte
Karte bleibt dadurch dieselbe Karte. Nur bei Dateien ohne Kennung – etwa
einer von Hand geschriebenen – dient ersatzweise der Titel als Merkmal.
Karten, die in der Datei fehlen, bleiben erhalten – ein Import fügt hinzu
und ändert, er räumt nicht auf. Vor dem Übernehmen zeigt eine Rückfrage,
wie viele Karten neu, geändert und unverändert sind.

> Ohne das Zusammenführen wäre es ein Totalaustausch: `facts.json` enthält
> keine Kennungen, jede Karte käme als neues Dokument an, und alle
> bisherigen würden gelöscht.

Den Eintrag legt man in der Firebase-Konsole an: *Firestore* → `config` →
`editors` → Feld `import` (Array) mit den Adressen, klein geschrieben.

**Umsortieren und Löschen speichern sich selbst.** Beides ist eine
Entscheidung, kein Zwischenstand – es geht sofort in die Datenbank. Nur
getippter Text wartet auf „Speichern".

### Einmalige Einrichtung

Einmal von oben nach unten durcharbeiten, dann läuft es. Die Reihenfolge
ist nicht beliebig – Schritt 4 muss vor Schritt 5 stehen, sonst sperren
sich die Regeln selbst aus (siehe Kasten dort).

Alles bleibt im kostenlosen **Spark-Tarif**. Eine Kreditkarte wird nicht
gebraucht.

#### A · In der Firebase-Konsole

**1. Firestore anlegen.**
*Build* → *Firestore Database* → *Datenbank erstellen*.
Region **europe-west3** (Frankfurt), Start im **Produktionsmodus**.

> Die Region lässt sich später **nicht** ändern. Produktionsmodus heißt:
> erst einmal ist alles gesperrt – genau richtig, die Freigaben kommen in
> Schritt 5.

**2. Google-Anmeldung einschalten.**
*Build* → *Authentication* → *Get started* → Reiter *Sign-in method* →
*Google* → aktivieren → Support-Mail wählen → *Speichern*.

**3. Adresse freigeben.**
*Authentication* → *Settings* → *Authorized domains* → *Add domain* →

```
viktorb1988.github.io
```

Nur der Rechnername: ohne `https://`, ohne Pfad, ohne Repo-Namen. Die
Adresse darf ruhig schon jetzt eingetragen werden, auch wenn die Seite
noch gar nicht steht – Firebase prüft nicht, ob es sie gibt.

**4. Redaktion eintragen.**
Das ist die Liste derer, die ändern dürfen. Sie existiert noch nicht, sie
wird hier angelegt:

*Firestore Database* → Reiter *Daten* → *Sammlung starten*

| Feld | Wert |
|---|---|
| Sammlungs-ID | `config` |
| Dokument-ID | `editors` — **selbst eintippen, nicht „Auto-ID"** |
| Feldname | `emails` |
| Typ | `array` |
| Werte | je ein `string` pro Person, **klein geschrieben** |

Ergebnis: ein Dokument `config/editors` mit einem einzigen Array-Feld.

> **Kleinschreibung ist Pflicht.** Die Regel vergleicht
> `request.auth.token.email.lower()` mit dieser Liste – `Max@Gmail.com`
> passt dann nie.
>
> **Es muss die Google-Adresse sein,** mit der man sich anmeldet, nicht
> die GitHub-Adresse.
>
> **Dieses Dokument über die Seite zu ändern ist absichtlich unmöglich.**
> Sonst könnte ein Redaktionskonto stillschweigend weitere Konten
> eintragen. Neue Leute kommen nur hier in der Konsole dazu.

**5. Regeln veröffentlichen.**
Inhalt von [`firestore.rules`](firestore.rules) kopieren, *Firestore
Database* → Reiter *Regeln* → alles ersetzen → *Veröffentlichen*.

Alternativ ohne Konsole, einmalig eingerichtet:

```bash
npm install -g firebase-tools
firebase login
firebase use --add
firebase deploy --only firestore:rules
```

`firebase login` öffnet den Browser; die Anmeldung passiert dort, nicht im
Terminal. Danach genügt nach jeder Regeländerung die letzte Zeile.
`firebase.json` im Projektordner sagt dem Befehl, welche Datei gemeint ist.

> **Erst Schritt 4, dann Schritt 5.** Die Regeln schlagen für die
> Schreibprüfung in `config/editors` nach. Fehlt das Dokument, schlägt
> die Prüfung fehl und **niemand** darf schreiben – auch Sie nicht. Das
> sieht dann aus wie ein kaputtes Login, ist aber nur die fehlende Liste.

**6. Zugangsdaten abschreiben.**
*Projekteinstellungen* (Zahnrad) → *Allgemein* → *Meine Apps*. Gibt es
noch keine Web-App, eine anlegen (`</>`-Symbol, Hosting nicht ankreuzen).
Den Block *SDK-Einrichtung und Konfiguration* → *Konfiguration* in
[`web/firebase-config.js`](web/firebase-config.js) übertragen.

> Diese Werte sind **kein Geheimnis** und gehören ins Repository. Ein
> Firebase-Web-Schlüssel benennt nur das Projekt, er berechtigt zu
> nichts. Wer was darf, steht ausschließlich in den Regeln aus Schritt 5.
> Sie in ein Secret zu verstecken bringt nichts und bricht den Bau.

#### B · Im GitHub-Repository

**7. Pages einschalten.**
*Settings* → *Pages* → *Source*: **GitHub Actions** – nicht
„Deploy from a branch". Die Seite wird gebaut, nicht aus einem Ordner
ausgeliefert.

Vor dem ersten Push einschalten, sonst scheitert der Arbeitsablauf beim
Veröffentlichen.

**8. Committen und pushen.**

```bash
git add -A && git commit -m "Firebase-Zugangsdaten eintragen" && git push
```

Erst der Push baut die Seite. Solange die ausgefüllte
`web/firebase-config.js` nur lokal liegt, meldet die veröffentlichte
Seite weiterhin „keine Firebase-Konfiguration".

Der Fortschritt steht unter *Actions*. Beim ersten Lauf dauert es ein
bis zwei Minuten. Danach steht die Seite unter

<https://viktorb1988.github.io/astronomyfunfactcards/>

> **Groß- und Kleinschreibung zählt.** Der Rechnername davor ist
> gleichgültig, der Pfad dahinter nicht: `.../astronomyfunfactcards/`
> führt zur Seite, `.../AstronomyFunFactCards/` nicht. So arbeiten
> Web-Adressen, daran lässt sich nichts einstellen. Der Name des
> Repositorys ist deshalb durchgehend klein geschrieben – dann stimmt,
> was man ohnehin tippt. Am sichersten bleibt es, die Adresse als Link
> weiterzugeben statt sie zu diktieren.

#### C · Datenbank befüllen

**9.** Seite aufrufen → **Anmelden** → **„Speichern"**.

Die Seite startet mit dem Stand aus `facts.json` und meldet
„Datenbank leer". Der Klick legt die 170 Karten einmalig an. **Ab jetzt
ist die Datenbank die Quelle**, nicht mehr die Datei.

### Wenn es nicht geht

Alle Meldungen erscheinen unten in der Mitte der Seite.

| Meldung oder Symptom | Ursache |
|---|---|
| „keine Firebase-Konfiguration" | Schritt 6 fehlt – oder Schritt 8: die Werte liegen nur lokal |
| `auth/unauthorized-domain` | Schritt 3 fehlt, oder mit `https://`/Pfad eingetragen |
| „… ist nicht als Redaktion eingetragen" | Adresse fehlt in `config/editors`, ist groß geschrieben, oder es ist eine andere Google-Adresse als gedacht |
| „Die Sicherheitsregeln lassen das Lesen nicht zu" | Schritt 5 fehlt – die Regeln stehen noch auf Produktionsmodus |
| „Dieses Konto darf laut Sicherheitsregeln nicht schreiben" | Regeln veröffentlicht, aber `config/editors` fehlt oder heißt anders |
| Anmeldefenster geht auf und sofort wieder zu | Pop-up-Blocker |
| Startmeldung bleibt stehen | JavaScript blockiert – Seite direkt im Browser öffnen, nicht in einer Vorschau |

## Alltag

Nach der Einrichtung gibt es im Wesentlichen vier Handgriffe.

### Karten online ändern

Seite aufrufen, **Anmelden**, tippen, **„Speichern"** (oder Strg+S).
Alle anderen sehen den neuen Stand beim nächsten Laden.

**Reihenfolge ändern und Karten löschen wird sofort geschrieben** – auch
ohne „Speichern". Wer eine Karte an eine andere Stelle zieht und den
Browser schließt, findet sie beim nächsten Mal dort wieder.

Gespeichert wird nur, was sich geändert hat. Ändern zwei Leute
gleichzeitig, bleibt die Arbeit des anderen also erhalten – solange nicht
beide dieselbe Karte anfassen. Kommt während des Tippens eine fremde
Änderung herein, wartet sie: es erscheint ein Hinweis, und übernommen
wird sie erst nach dem eigenen Speichern.

### PDFs neu bauen

Der PDF-Bau liest `facts.json`, nicht die Datenbank. Den aktuellen Stand
also erst holen:

```bash
python3 fetch_facts.py
python3 build_cards.py
```

`fetch_facts.py` braucht keine Anmeldung – Lesen ist öffentlich. Es fragt
nach, bevor es `facts.json` überschreibt.

### `facts.json` im Repo aktuell halten

Die Datenbank kennt keine Versionsgeschichte: Wer eine Karte löscht und
speichert, hat sie endgültig gelöscht. Git kennt sie sehr wohl. Deshalb
lohnt es sich, den geholten Stand hin und wieder mitzucommitten:

```bash
python3 fetch_facts.py
git add facts.json && git commit -m "Kartenstand aus der Datenbank" && git push
```

Das kostet nichts und bringt dreierlei:

- **Sicherung.** Jeder Commit ist ein Wiederherstellungspunkt.
- **Startbestand.** Aus dieser Datei wird eine leere Datenbank befüllt.
- **Rückfallebene.** Ist Firestore einmal nicht erreichbar, zeigt die
  Seite diesen Stand an, statt leer zu bleiben.

Der Push baut die Seite neu – `facts.json` steht in der Auslöserliste des
Arbeitsablaufs.

### Jemanden zur Redaktion hinzufügen

Nur in der Firebase-Konsole, nicht über die Seite: *Firestore Database* →
*Daten* → `config` → `editors` → Feld `emails` → *Element hinzufügen* →
Google-Adresse **klein geschrieben**.

Wirkt sofort; die betreffende Person muss die Seite nur neu laden. Zum
Entfernen den Eintrag aus dem Array löschen.

> Dass das nicht über die Seite geht, ist Absicht: sonst könnte ein
> Redaktionskonto stillschweigend weitere Konten eintragen.

### Und offline?

`out/karten-editor.html` gibt es weiterhin – eine einzelne Datei ohne
Server, Internet und Konto. Sie kennt die Datenbank nicht: Sie enthält
den Stand aus `facts.json` zum Zeitpunkt des Bauens und sichert per
Download. Praktisch im Bus, in der Kuppel ohne Empfang, oder wenn jemand
ohne Google-Konto etwas vorbereiten soll.

Neu bauen mit `python3 build_editor.py` – am besten direkt nach einem
`fetch_facts.py`, sonst ist der Stand darin veraltet.

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

Dieser Abschnitt gilt für die **Offline-Fassung**. Online gibt es die
beiden Dateiknöpfe nicht, und Strg+S schreibt in die Datenbank.

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
  "id": "kmsdl1jave79g39",
  "no": 101,
  "theme": "SONNENSYSTEM",
  "title": "Kurzer Titel",
  "text": "Der Fakt, zwei bis drei Sätze, in sich verständlich.",
  "more": "Ein Satz Zusatzinfo für den Absatz „Mehr dazu\".",
  "source": "",
  "level": ""
}
```

`source` ist ein Notizfeld für die Redaktion und erscheint nur im Editor.
`level` ist die Schwierigkeit – `easy`, `medium`, `expert` oder leer – und
**steht oben auf der Karte**, mittig zwischen Thema und Nummer:

```
SONNENSYSTEM        EINFACH        1
```

Auf der Karte steht deutsch (Einfach, Mittel, Experte), in den Daten
englisch. Karten ohne Stufe zeigen an der Stelle nichts.

Die `id` bleibt, wie sie ist. Daran wird die Karte beim Einspielen
wiedererkannt – auch dann, wenn Titel und Text sich geändert haben. Neue
Karten legt man ohne `id` an; der Editor vergibt sie.

Die Feldnamen sind englisch, die Inhalte deutsch – im ganzen Projekt so
gehalten: Code englisch, alles Sichtbare deutsch.

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

Für die Varianten ohne Zusatzabsatz `WITH_MORE = False` oben in
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
- `theme` muss einem Eintrag aus der Liste `themes` entsprechen. Neue Themen
  dort ergänzen; die Position in dieser Liste bestimmt, wo der Themenblock
  im Stapel liegt.
- Einseitige Karten haben keine Fußzeile mehr. Die Kartennummer steht
  klein oben rechts, `meta.footer` wird nicht mehr gedruckt.
- Ober- und Untergrenze der Schriftgröße stehen als `minText` / `maxText`
  im Dictionary `FORMATS` in `build_cards.py`.
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
