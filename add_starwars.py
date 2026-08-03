#!/usr/bin/env python3
"""Ergaenzt das Thema STAR WARS um 20 Karten und sortiert alles neu."""
import json, pathlib

THEMA = "STAR WARS"

NEU = [
("Tatooine gibt es wirklich",
 "2011 entdeckte das Kepler-Teleskop den Planeten Kepler-16b, der zwei Sterne gleichzeitig umkreist. Von seiner Bahn aus gehen tatsächlich zwei Sonnen unter.",
 "Die NASA taufte ihn inoffiziell Tatooine. Wüste gibt es dort allerdings keine: Kepler-16b ist ein kalter Gasplanet von Saturnmasse."),

("Der echte Doppelsonnenuntergang",
 "Die beiden Sonnen von Kepler-16b sind ein orangefarbener Zwergstern und ein deutlich kleinerer roter. Zusammen liefern sie nur wenige Prozent der Strahlung unserer Sonne.",
 "Auf dem Planeten herrschen rund minus 70 Grad. Der berühmte Sonnenuntergang wäre rötlich und ziemlich dunkel."),

("Doppelsonnen sind der Normalfall",
 "Etwa die Hälfte aller sonnenähnlichen Sterne gehört zu einem Doppel- oder Mehrfachsystem. Ein Himmel mit zwei Sonnen ist im Universum nichts Besonderes.",
 "Unsere Sonne ist der Sonderfall: Sie zieht ihre Bahn allein durch die Milchstraße."),

("Ein Tatooine in der habitablen Zone",
 "Kepler-1647b, 2016 entdeckt, ist der größte bekannte Planet, der zwei Sterne umkreist. Er braucht dafür gut drei Jahre und liegt im Abstandsbereich, in dem flüssiges Wasser möglich wäre.",
 "Der Planet selbst ist ein Gasriese von Jupitergröße. Ein Mond in seiner Umlaufbahn wäre der bessere Kandidat für Leben."),

("Ein Praktikant fand einen Doppelsonnen-Planeten",
 "Der Planet TOI-1338 b umkreist ebenfalls zwei Sterne. Entdeckt hat ihn 2020 ein 17-jähriger Praktikant der NASA, der in seinen ersten Arbeitstagen Messkurven durchsah.",
 "Solche Planeten sind schwer zu finden, weil ihre Verdunkelungen unregelmäßig ausfallen – die beiden Sterne bewegen sich ja mit."),

("Hoth steht im Katalog",
 "Ein 2006 entdeckter Planet mit der Katalognummer OGLE-2005-BLG-390Lb ist rund fünfeinhalbmal so schwer wie die Erde und etwa minus 220 Grad kalt.",
 "Die NASA führt ihn unter dem Spitznamen Hoth. Er ist rund 21.000 Lichtjahre entfernt und wurde nur über eine kurzzeitige Lichtverstärkung entdeckt."),

("Durch ein Asteroidenfeld zu fliegen ist langweilig",
 "Im echten Asteroidengürtel zwischen Mars und Jupiter liegen im Schnitt Hunderttausende Kilometer zwischen zwei Brocken. Sonden fliegen ohne Ausweichmanöver hindurch.",
 "Die Wahrscheinlichkeit, dabei auf einen Asteroiden zu treffen, ist verschwindend gering. Alle Ausweichmanöver müssten geplant angeflogen werden."),

("Der Todesstern wäre kleiner als ein Mond",
 "Die Kampfstation hat je nach Quelle rund 120 bis 160 Kilometer Durchmesser. Der Saturnmond Mimas misst 396 Kilometer – er wäre mehr als doppelt so groß.",
 "Kurios: Mimas trägt einen 130 Kilometer weiten Einschlagkrater und sieht dadurch selbst aus wie der Todesstern. Fotografiert wurde er erst 1980, drei Jahre nach dem ersten Film."),

("Einen Planeten zu sprengen kostet viel",
 "Um eine erdgroße Welt vollständig auseinanderzureißen, müsste man ihre Gravitationsbindung überwinden – rund 2 mal 10<sup>32</sup> Joule.",
 "Die Sonne strahlt diese Energie in etwa einer Woche ab. Eine Waffe müsste sie in Sekunden aufbringen und gebündelt abgeben."),

("Ein Parsec ist keine Zeit",
 "Der Parsec ist eine Längeneinheit: 3,26 Lichtjahre. Er ist definiert über die Parallaxe, also die scheinbare Verschiebung eines Sterns, während die Erde die Sonne umrundet.",
 "Eine Strecke in Parsec anzugeben ist deshalb sinnvoll – als Angabe für einen Rekord in Bestzeit dagegen nicht."),

("Der Asteroidengürtel ist kein zerstörter Planet",
 "Zwischen Mars und Jupiter kreisen Millionen Brocken, aber sie stammen nicht von einer gesprengten Welt. Jupiters Schwerkraft verhinderte von Anfang an, dass sich dort ein Planet zusammenballte.",
 "Alle Asteroiden zusammen wiegen weniger als fünf Prozent des Erdmonds – für einen Planeten viel zu wenig Material."),

("Mustafar liegt im Sonnensystem",
 "Der Jupitermond Io ist der vulkanisch aktivste Körper des Sonnensystems. Hunderte Vulkane schleudern Schwefel kilometerweit ins All.",
 "Angetrieben wird das durch Gezeitenkräfte: Jupiter und die Nachbarmonde walken Io durch, die Reibungswärme hält das Innere flüssig."),

("Eine Wolkenstadt würde absinken",
 "Gasriesen haben keine feste Oberfläche, ihre Atmosphäre besteht überwiegend aus Wasserstoff und Helium. Atemluft ist deutlich schwerer als dieses Gemisch.",
 "Eine mit Luft gefüllte Stadt würde dort also nicht schweben, sondern sinken. Auf der Venus mit ihrer schweren CO₂-Atmosphäre funktionierte es dagegen."),

("Waldmonde sind noch unbestätigt",
 "Um einen Gasriesen kreisende Monde sind in unserem Sonnensystem der Normalfall. Außerhalb wurde bislang kein einziger sicher nachgewiesen.",
 "Der bekannteste Kandidat wurde 2018 beim Planeten Kepler-1625b gemeldet, wäre so groß wie Neptun – und ist bis heute umstritten."),

("Eine Stadtwelt würde man von weitem sehen",
 "Jede Energie, die eine Zivilisation verbraucht, wird am Ende zu Wärme und muss abgestrahlt werden. Ein vollständig bebauter Planet müsste im Infraroten auffällig hell leuchten.",
 "Genau danach suchen Astronomen bei der Fahndung nach außerirdischen Zivilisationen – nach Wärme, die nicht zum Stern passt."),

("Der Sprung in den Hyperraum sähe anders aus",
 "Bei nahezu Lichtgeschwindigkeit würden die Sterne nicht als Streifen nach hinten ziehen. Die Aberration schiebt alles Licht nach vorn zusammen, und die Farben verschieben sich ins Blaue.",
 "Vor dem Schiff bliebe ein heller Fleck: die kosmische Hintergrundstrahlung, hochverschoben ins Sichtbare. Der Rest des Himmels wäre dunkel."),

("Lichtschwerter bestehen aus dem häufigsten Zustand",
 "Plasma ist Gas, dem die Elektronen entrissen wurden. Über 99 Prozent der sichtbaren Materie im Universum liegen in diesem Zustand vor, denn alle Sterne bestehen daraus.",
 "Frei geformtes Plasma leuchtet zwar, hält aber ohne Magnetfeld keine Form – und schon gar nicht auf einer festen Länge."),

("Planeten ohne Sonne gibt es zuhauf",
 "Nicht jeder Planet gehört zu einem Stern. Frei durch die Galaxis treibende Welten wurden vielfach nachgewiesen und könnten sogar zahlreicher sein als die Sterne selbst.",
 "2023 fand das James-Webb-Teleskop im Orionnebel Dutzende solcher Objekte, viele davon paarweise unterwegs – bis heute unerklärt."),

("Sandstürme kann der Mars besser",
 "Auf dem Mars wachsen Staubstürme gelegentlich so weit an, dass sie den ganzen Planeten einhüllen. Wochenlang dringt dann kaum Sonnenlicht bis zum Boden.",
 "Ein solcher Sturm beendete 2018 die Mission des Rovers Opportunity: Seine Solarzellen bekamen zu wenig Licht."),

("Ewiger Tag auf der einen Seite",
 "Planeten, die einen Roten Zwerg eng umkreisen, geraten meist in gebundene Rotation: Sie wenden dem Stern immer dieselbe Seite zu.",
 "Auf der einen Hälfte steht die Sonne dann für immer am selben Punkt, auf der anderen ist ewige Nacht. Leben wäre am ehesten im Dämmerungsgürtel dazwischen denkbar."),
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
