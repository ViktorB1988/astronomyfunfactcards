#!/usr/bin/env python3
"""Ergaenzt das Thema PROJECT HAIL MARY um 30 Karten und sortiert alles neu."""
import json, pathlib

THEMA = "PROJECT HAIL MARY"

NEU = [
("Das Ziel liegt 11,9 Lichtjahre entfernt",
 "Der Stern Tau Ceti, Ziel der Reise in „Project Hail Mary\u201c, steht 11,9 Lichtjahre von uns entfernt. Sein Licht, das heute bei uns ankommt, ist zur Zeit der Jahrtausendwende gestartet.",
 "Damit gehört Tau Ceti zu den zwei Dutzend Sternsystemen in unserer unmittelbaren Nachbarschaft. Auf galaktischen Maßstäben liegt er praktisch nebenan."),

("Warum ausgerechnet Tau Ceti",
 "Unter den nahen Sternen ist Tau Ceti einer der wenigen, die der Sonne wirklich ähneln: etwas kleiner, etwas kühler, rund 55 Prozent ihrer Leuchtkraft – und vor allem ein Einzelstern ohne störenden Begleiter.",
 "Die meisten nahen Sterne sind entweder Rote Zwerge oder Teil eines Doppelsystems. Sonnenähnliche Einzelsterne sind in Reichweite selten."),

("Zwei Dutzend Nachbarn",
 "Innerhalb von zwölf Lichtjahren um die Sonne liegen ungefähr zwei Dutzend Sternsysteme. Die allermeisten davon sind Rote Zwerge, die man ohne Teleskop nie zu sehen bekommt.",
 "Mit bloßem Auge sichtbar sind aus dieser Nachbarschaft nur eine Handvoll, darunter Sirius, Prokyon und Tau Ceti."),

("Die Sonnenkonstante",
 "Am Ort der Erde treffen pro Quadratmeter rund 1.361 Watt Sonnenstrahlung ein. Dieser Wert heißt Sonnenkonstante und ist die Grundlage jeder Klimarechnung.",
 "Gemessen wird er seit 1978 von Satelliten. Vom Boden aus ginge es nicht: Die Atmosphäre schluckt einen erheblichen Teil der Strahlung."),

("So konstant ist die Sonne gar nicht",
 "Im Rhythmus des elfjährigen Sonnenfleckenzyklus schwankt die Strahlungsleistung der Sonne um etwa ein Promille. Für das Klima ist das wenig, messbar ist es trotzdem.",
 "Erstaunlich dabei: Bei vielen Sonnenflecken strahlt die Sonne insgesamt etwas stärker, obwohl die Flecken selbst dunkel sind."),

("Als die Sonnenflecken verschwanden",
 "Zwischen 1645 und 1715 wurden über Jahrzehnte kaum Sonnenflecken beobachtet. Diese Phase heißt Maunder-Minimum und fiel mit einem besonders kalten Abschnitt in Europa zusammen.",
 "Ob und wie stark die Sonne daran schuld war, ist bis heute umstritten. Gleichzeitig gab es zahlreiche große Vulkanausbrüche."),

("Ein Prozent weniger würde reichen",
 "Sänke die Sonneneinstrahlung dauerhaft um nur ein Prozent, kühlte die Erde spürbar ab. Der Effekt bliebe nicht bei einem Prozent stehen, denn das Klima verstärkt solche Anstöße selbst.",
 "Genau davon lebt die Ausgangslage in „Project Hail Mary\u201c: Nicht die Sonne muss erlöschen, sie muss nur ein wenig schwächer werden."),

("Eis macht mehr Eis",
 "Schnee und Eis werfen Sonnenlicht zurück, dunkles Wasser und dunkler Boden schlucken es. Wird es kälter, wächst die Eisfläche – und die größere Eisfläche kühlt weiter ab.",
 "Diese Rückkopplung wirkt in beide Richtungen und macht das Klima empfindlich gegenüber kleinen Änderungen der Einstrahlung."),

("Die Sonne wird von selbst heller",
 "Seit ihrer Entstehung ist die Sonne rund 30 Prozent heller geworden, und sie legt weiter zu – etwa zehn Prozent pro Milliarde Jahre.",
 "In rund einer Milliarde Jahren dürfte das reichen, um die Ozeane verdampfen zu lassen. Die Erde wird also unbewohnbar, lange bevor die Sonne stirbt."),

("Ein Leuchten in der Ekliptik",
 "Zwischen den Planeten schwebt feiner Staub, der Sonnenlicht streut. Bei sehr dunklem Himmel sieht man ihn als schwachen Lichtkegel entlang der Tierkreisbahn: das Zodiakallicht.",
 "Am besten sichtbar ist es im Frühjahr nach der Dämmerung und im Herbst vor Sonnenaufgang – ganz ohne Teleskop."),

("Jeder Stoff hat einen Fingerabdruck",
 "Zerlegt man Licht in seine Farben, fehlen an ganz bestimmten Stellen Linien. Dieses Muster ist für jedes Element und jedes Molekül einmalig.",
 "Deshalb wissen wir, woraus Sterne bestehen, ohne je einen berührt zu haben. Entdeckt wurde das Prinzip in den 1860er Jahren."),

("Wärmestrahlung sieht man nur von oben",
 "Das mittlere Infrarot, in dem warme Objekte strahlen, wird von der Erdatmosphäre fast vollständig geschluckt. Vom Boden aus ist dieser Bereich praktisch blind.",
 "Deshalb steht das James-Webb-Teleskop im All und wird auf unter minus 230 Grad gekühlt – sonst würde es sich selbst überstrahlen."),

("40 Eridani ist doppelt vergeben",
 "Die Heimat des Außerirdischen in „Project Hail Mary\u201c liegt bei 40 Eridani. Denselben Stern hatte Star Trek Jahrzehnte zuvor bereits als Sonne von Spocks Heimatwelt Vulkan festgelegt.",
 "Den Stern gibt es wirklich: ein Dreifachsystem in 16,3 Lichtjahren Entfernung, gut sichtbar im Sternbild Eridanus."),

("Ein Weißer Zwerg zum Selbersehen",
 "40 Eridani B ist einer der am leichtesten zu beobachtenden Weißen Zwerge überhaupt. Mit rund 9,5 Größenklassen zeigt ihn schon ein kleines Teleskop.",
 "Ein Weißer Zwerg ist der ausgeglühte Rest eines Sterns: etwa so groß wie die Erde, aber mit ungefähr der halben Masse der Sonne."),

("Der dritte Stern flackert",
 "Zum System 40 Eridani gehört noch ein Roter Zwerg. Er ist ein Flarestern: Innerhalb von Minuten kann er sich deutlich aufhellen und wieder abklingen.",
 "Solche Ausbrüche schleudern Strahlung und Teilchen ins All. Für Planeten in der Nähe wären sie ein ernsthaftes Problem."),

("Druck wie in 290 Metern Tiefe",
 "Die Heimatwelt des Außerirdischen hat im Roman einen Luftdruck von etwa 29 bar. Auf der Erde herrscht dieser Druck erst in rund 290 Metern Wassertiefe.",
 "Extrem ist das im Sonnensystem nicht: Auf der Venus liegt der Bodendruck bei 92 bar, dem Dreifachen davon."),

("Dichte Luft macht laut, nicht schnell",
 "Wie schnell Schall ist, hängt vor allem von Temperatur und Gasart ab, kaum vom Druck. Sehr wohl vom Druck abhängt jedoch, wie viel Energie eine Schallwelle trägt.",
 "In einer dichten Atmosphäre wäre dasselbe Geräusch also deutlich lauter und trüge weiter – Verständigung über Töne läge dort nahe."),

("Ammoniak statt Wasser",
 "Wasser gilt als ideales Lösungsmittel für Leben, ist aber nicht das einzig denkbare. Ammoniak bleibt bei tieferen Temperaturen flüssig und löst ebenfalls viele Stoffe.",
 "Unter höherem Druck erweitert sich sein flüssiger Bereich zusätzlich. In der Astrobiologie wird Ammoniak deshalb ernsthaft diskutiert."),

("Der kälteste bekannte Nachbar",
 "In 7,2 Lichtjahren Entfernung steht das Objekt WISE 0855: ein Brauner Zwerg, zu leicht zum Zünden der Kernfusion, mit einer Temperatur von etwa minus 20 bis minus 40 Grad.",
 "Es ist damit kälter als jeder bekannte Stern und wurde erst 2014 entdeckt – trotz der geringen Entfernung, weil es fast nur im Infraroten strahlt."),

("Der schnellste Stern am Himmel",
 "Barnards Pfeilstern in knapp sechs Lichtjahren Entfernung wandert schneller über den Himmel als jeder andere Stern: Er legt in rund 180 Jahren die Breite des Vollmonds zurück.",
 "Alle Sterne bewegen sich, nur sind sie meist zu weit weg, um das zu bemerken. Die Sternbilder verändern sich über Jahrtausende hinweg."),

("Sirius ist ein Doppelstern",
 "Der hellste Stern des Nachthimmels hat einen Begleiter: einen Weißen Zwerg, der 1862 entdeckt wurde. Vorhergesagt hatte man ihn schon 1844, weil Sirius merkwürdig taumelte.",
 "Der Begleiter ist zehntausendmal lichtschwächer und geht im Glanz des Hauptsterns fast unter – ein schwieriges, aber lohnendes Teleskopziel."),

("Fünf Jahre an Bord, dreizehn auf der Erde",
 "Ein Schiff mit 92 Prozent der Lichtgeschwindigkeit bräuchte für die 11,9 Lichtjahre nach Tau Ceti knapp 13 Jahre. An Bord vergingen dabei nur etwa fünf.",
 "Der Unterschied ist keine technische Frage, sondern folgt direkt aus der Relativitätstheorie. Wer zurückkäme, fände eine um Jahrzehnte gealterte Heimat vor."),

("Das eigentliche Problem ist die Energie",
 "Nicht die Entfernung macht interstellare Reisen schwierig, sondern der Antrieb. Um überhaupt in die Nähe der Lichtgeschwindigkeit zu kommen, braucht es unvorstellbare Energiemengen.",
 "Chemische Raketen scheiden aus: Ihr Treibstoff setzt pro Kilogramm nur einige Millionen Joule frei, benötigt würde das Milliardenfache."),

("Antimaterie wäre der dichteste Treibstoff",
 "Treffen ein Gramm Materie und ein Gramm Antimaterie aufeinander, wird die gesamte Masse in Energie umgewandelt: rund 1,8 mal 10<sup>14</sup> Joule.",
 "Das entspricht etwa der Sprengkraft von 40.000 Tonnen TNT. Herstellen lassen sich bisher nur winzigste Mengen, mit gewaltigem Aufwand."),

("Sonnensegel fliegen wirklich",
 "Licht übt Druck aus. Zwar ist er winzig, wirkt aber ununterbrochen – ein großes, dünnes Segel kann ein Raumfahrzeug damit beschleunigen, ganz ohne Treibstoff.",
 "Japan zeigte das 2010 mit der Sonde IKAROS, 2019 folgte die private Mission LightSail 2 in der Erdumlaufbahn."),

("Ein Staubkorn wird zur Bombe",
 "Bei 92 Prozent der Lichtgeschwindigkeit trägt schon ein Staubkorn von einem Milligramm die Energie von etwa 30 Tonnen TNT.",
 "Ein Schutzschild gegen solche Treffer ist eines der ungelösten Probleme jeder ernsthaften Planung interstellarer Reisen."),

("Zwischen den Sternen ist fast nichts",
 "Im interstellaren Raum schwebt im Schnitt etwa ein Atom pro Kubikzentimeter. Das ist ein besseres Vakuum, als sich auf der Erde herstellen lässt.",
 "Auf Strecken von Lichtjahren summiert sich selbst das: Ein Schiff durchpflügt dabei erhebliche Mengen Material."),

("Eine Antwort bräuchte 24 Jahre",
 "Ein Funkspruch zum Stern Tau Ceti ist 11,9 Jahre unterwegs. Auf eine Antwort müsste man noch einmal genauso lange warten.",
 "Ein Gespräch ist damit ausgeschlossen. Jede Nachricht müsste für sich allein verständlich sein – wie eine Flaschenpost."),

("Schwerkraft durch Drehung",
 "Ein rotierendes Raumschiff erzeugt eine nach außen gerichtete Kraft, die sich wie Schwerkraft anfühlt. Für volle Erdschwere bei vier Umdrehungen pro Minute bräuchte es einen Radius von rund 56 Metern.",
 "Dreht sich der Ring schneller, genügt weniger Radius – dann aber unterscheidet sich die Kraft an Kopf und Füßen so stark, dass vielen übel wird."),

("Strahlung ist der stille Begleiter",
 "Der Rover Curiosity maß auf dem Flug zum Mars die Strahlenbelastung im freien Raum. Für Hin- und Rückflug ergaben sich etwa 0,66 Sievert.",
 "Das liegt nahe an dem, was Raumfahrtbehörden als Lebenszeitgrenze ansetzen. Für Jahre im interstellaren Raum bräuchte es massive Abschirmung."),
]

p = pathlib.Path(__file__).parent / "facts.json"
d = json.loads(p.read_text(encoding="utf-8"))
if THEMA not in d["themen"]:
    d["themen"].append(THEMA)
vorhanden = {k["titel"] for k in d["karten"]}
for titel, text, nach in NEU:
    if titel in vorhanden:
        continue
    d["karten"].append({"nr": 0, "thema": THEMA, "titel": titel,
                        "text": text, "nachschlag": nach})

rang = {t: i for i, t in enumerate(d["themen"])}
d["karten"].sort(key=lambda k: rang.get(k["thema"], 999))
for i, k in enumerate(d["karten"], 1):
    k["nr"] = i
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"{'Thema':26} {'Karten':>6}  Nummern")
for t in d["themen"]:
    n = [k["nr"] for k in d["karten"] if k["thema"] == t]
    print(f"{t.replace('LOECHER','LÖCHER'):26} {len(n):>6}  {n[0]}\u2013{n[-1]}")
print(f"\nGesamt {len(d['karten'])}")
