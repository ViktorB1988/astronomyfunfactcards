#!/usr/bin/env python3
"""Ergaenzt das Thema STAR TREK um 20 Karten und sortiert alles neu."""
import json, pathlib

THEMA = "STAR TREK"

NEU = [
("Vulkan gibt es wirklich",
 "Gene Roddenberry legte 1991 gemeinsam mit Astronomen in einer Fachzeitschrift fest, dass Spocks Heimatwelt den Stern 40 Eridani A umkreist. Den gibt es tatsächlich: ein Dreifachsystem in 16,3 Lichtjahren Entfernung.",
 "2018 meldeten Forscher dort einen Planeten. Spätere Messungen zeigten, dass das Signal von der Aktivität des Sterns stammte."),

("Der andere Planet Vulkan",
 "Lange vor Star Trek gab es schon einen Planeten Vulkan: 1859 postulierte Urbain Le Verrier einen Planeten innerhalb der Merkurbahn, um dessen seltsame Bahndrehung zu erklären. Gefunden wurde er nie.",
 "Einsteins Allgemeine Relativitätstheorie erklärte die Bahndrehung 1915 ohne zusätzlichen Planeten. Vulkan war damit überflüssig."),

("Ein Pluto-Mond hätte fast Vulcan geheißen",
 "2013 durfte das Publikum über die Namen zweier neuer Pluto-Monde abstimmen. Auf Vorschlag von William Shatner gewann „Vulcan\u201c mit deutlichem Abstand.",
 "Die Internationale Astronomische Union lehnte ab, weil der Name in der Astronomie längst vergeben war. Die Monde heißen heute Kerberos und Styx."),

("Wolf 359 ist ein Winzling",
 "Der Schauplatz der berühmten Raumschlacht ist ein realer Stern: Wolf 359 steht nur 7,9 Lichtjahre entfernt und gehört zu den nächsten Nachbarn der Sonne.",
 "Er ist ein Roter Zwerg mit weniger als einem Zehntel der Sonnenmasse und so lichtschwach, dass man ihn nur im Teleskop sieht."),

("Tau Ceti wäre kein guter Wohnort",
 "Der sonnenähnliche Stern Tau Ceti in 11,9 Lichtjahren Entfernung galt lange als Hoffnungsträger für bewohnbare Planeten. Er ist von einer Trümmerscheibe umgeben, die zehnmal mehr Material enthält als unser Kuipergürtel.",
 "Planeten dort stünden unter Dauerbeschuss durch Kometen und Asteroiden – ein ähnlich lebensfeindliches Los wie das von Khans Exilwelt."),

("Omicron Ceti ist ein pulsierender Stern",
 "Omicron Ceti heißt in Wirklichkeit Mira und ist ein Veränderlicher: Seine Helligkeit schwankt im Rhythmus von 332 Tagen um etwa das Tausendfache.",
 "2007 entdeckte der Satellit GALEX, dass Mira einen kometenartigen Schweif von rund 13 Lichtjahren Länge hinter sich herzieht."),

("Rigel ist zu jung für Leben",
 "Rigel im Orion, in Star Trek gleich mehrfach als Planetensystem im Einsatz, ist ein blauer Überriese in rund 860 Lichtjahren Entfernung mit etwa der hunderttausendfachen Leuchtkraft der Sonne.",
 "Der Stern ist erst wenige Millionen Jahre alt. Für die Entstehung von Leben blieb dort schlicht keine Zeit."),

("Denebs Licht ist älter als jede Geschichte",
 "Deneb im Schwan, in Star Trek der Zielort der ersten Mission der Enterprise-D, ist je nach Messung rund 2.600 Lichtjahre entfernt – einer der leuchtkräftigsten Sterne am Nachthimmel.",
 "Sein Licht, das heute bei uns ankommt, startete zur Zeit der frühen griechischen Antike."),

("Antares würde das halbe Sonnensystem füllen",
 "Antares im Skorpion, häufiger Namensgeber in Star Trek, ist ein Roter Überriese in rund 550 Lichtjahren Entfernung.",
 "Stünde er anstelle der Sonne, reichte seine Oberfläche über die Marsbahn hinaus. Erde und Mars lägen im Inneren des Sterns."),

("Epsilon Eridani war der erste Kandidat",
 "Frühe Star-Trek-Quellen ordneten Vulkan dem Stern Epsilon Eridani zu, bevor sich 40 Eridani A durchsetzte. Epsilon Eridani ist real und mit 10,5 Lichtjahren einer der nächsten sonnenähnlichen Sterne.",
 "Dort wurde tatsächlich ein Riesenplanet nachgewiesen. Der Stern ist allerdings sehr jung und von einer dichten Trümmerscheibe umgeben."),

("Der Warpantrieb hat eine Fachveröffentlichung",
 "1994 veröffentlichte der Physiker Miguel Alcubierre eine Arbeit, die einen Warpantrieb im Rahmen der Allgemeinen Relativitätstheorie beschreibt: Der Raum wird vorn gestaucht und hinten gedehnt.",
 "Alcubierre nannte Star Trek ausdrücklich als Anregung. Sein Antrieb bräuchte Materie mit negativer Energiedichte, von der niemand weiß, ob es sie gibt."),

("Dilithium gibt es tatsächlich",
 "Der Treibstoffkristall aus Star Trek trägt einen echten chemischen Namen: Dilithium ist ein Molekül aus zwei Lithiumatomen, das in der Gasphase nachgewiesen wurde.",
 "Mit Antimaterie hat es nichts zu tun. Es ist ein schwach gebundenes Molekül, das sich nur unter besonderen Bedingungen hält."),

("Wurmlöcher sind seit 1935 im Gespräch",
 "Albert Einstein und Nathan Rosen beschrieben 1935 eine Verbindung zwischen zwei Orten der Raumzeit. Solche Brücken kollabieren allerdings, bevor irgendetwas hindurchfliegen könnte.",
 "1988 zeigten Michael Morris und Kip Thorne, wie ein durchquerbares Wurmloch aussehen müsste – es bräuchte exotische Materie, um offen zu bleiben."),

("Die Dyson-Sphäre ist eine ernsthafte Idee",
 "Die Kugelschale um einen ganzen Stern, in Star Trek einmal als Schauplatz genutzt, geht auf einen Vorschlag des Physikers Freeman Dyson von 1960 zurück.",
 "Astronomen suchen tatsächlich nach solchen Bauwerken – sie müssten Wärmestrahlung abgeben. Ein 2015 verdächtigter Stern entpuppte sich als von Staub umgeben."),

("V'Ger hat ein reales Vorbild",
 "Die Sonde, die im ersten Star-Trek-Kinofilm zur Bedrohung wird, ist als Voyager 6 ausgegeben. Die echten Sonden Voyager 1 und 2 starteten 1977 und funken bis heute.",
 "Voyager 1 ist über 25 Milliarden Kilometer entfernt. Ein Funkspruch von dort braucht fast einen Tag bis zur Erde."),

("Es gab eine echte Enterprise",
 "Die erste Raumfähre der NASA hieß Enterprise. Nach einer Zuschriftenkampagne von Fans wurde sie 1976 auf diesen Namen getauft.",
 "Ins All flog sie nie: Sie diente Gleit- und Landeversuchen in der Erdatmosphäre. Ihr Rumpf hatte kein Hitzeschild."),

("Asteroiden tragen Star-Trek-Namen",
 "Im Asteroidengürtel zwischen Mars und Jupiter kreisen Kleinplaneten, die nach Darstellern der Serie benannt sind – etwa der Asteroid 4864 Nimoy.",
 "Namen für Kleinplaneten vergibt die Internationale Astronomische Union. Sie sind endgültig und lassen sich nicht zurücknehmen."),

("Der Transporter existiert im Kleinen",
 "1997 gelang Physikern erstmals die Quantenteleportation: Der Zustand eines Teilchens wurde auf ein anderes übertragen, ohne dass etwas den Weg dazwischen zurücklegte.",
 "Materie wird dabei nicht bewegt. Der ursprüngliche Zustand wird zerstört – teleportiert wird die Information, nicht das Objekt."),

("Im All ist es still",
 "Raumschiffe rauschen in Star Trek an der Kamera vorbei und Explosionen krachen. Im Vakuum gibt es dafür kein Medium: Schall braucht Materie, die schwingt.",
 "Hörbar wird es erst wieder in dichten Gaswolken. Dort haben Astronomen Druckwellen nachgewiesen, allerdings viele Oktaven unterhalb des Hörbaren."),

("Klasse M hat ein echtes Vorbild",
 "Star Treks „Klasse-M-Planeten\u201c entsprechen dem, was die Astronomie habitable Zone nennt: der Abstandsbereich um einen Stern, in dem flüssiges Wasser auf einer Oberfläche bestehen kann.",
 "Den Begriff prägte der Astronom Su-Shu Huang 1959, sieben Jahre vor der ersten Star-Trek-Folge."),
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
