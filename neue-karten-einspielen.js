/* Fuegt die 32 neuen Karten zum Stand hinzu, der gerade im Browser liegt.
   Vorhandene Karten werden nicht angefasst: Ihre Kennungen bleiben, und
   das Speichern schreibt nur, was sich unterscheidet - also genau die
   neuen Dokumente. Mehrfaches Ausfuehren schadet nicht, schon vorhandene
   Titel werden uebersprungen. */
(() => {
  const E = window.Editor;
  if (!E) return "Kein Editor auf dieser Seite gefunden.";
  const knopf = document.getElementById("formsave");
  if (!knopf || knopf.disabled) return "Erst anmelden - der Speichern-Knopf ist gesperrt.";

  const THEMEN = ["TERRAFORMING MARS", "ARTEMIS 2", "WARPANTRIEB", "FIKTION WIRD WIRKLICH"];
  const NEU = [
  {
    "theme": "TERRAFORMING MARS",
    "title": "Der Luftdruck reicht nicht",
    "text": "Die Marsatmosphäre besteht zu 95 Prozent aus Kohlendioxid, drückt aber nur mit 6 Millibar auf den Boden. Ein Mensch ohne Anzug würde dort nicht ersticken – seine Körperflüssigkeiten begännen bei Körpertemperatur zu sieden.",
    "more": "Die Grenze heißt Armstrong-Linie und liegt bei rund 63 Millibar, dem Druck in 19 Kilometern Höhe über der Erde."
  },
  {
    "theme": "TERRAFORMING MARS",
    "title": "Das Kohlendioxid reicht auch nicht",
    "text": "Der Plan, das gefrorene Kohlendioxid der Marspole zu verdampfen, wurde 2018 durchgerechnet. Alles zugängliche Kohlendioxid zusammen ergäbe 15 Millibar Druck. Für eine atembare Atmosphäre bräuchte es das Sechzigfache.",
    "more": "Die Rechnung stammt von Bruce Jakosky und Christopher Edwards und erschien in Nature Astronomy."
  },
  {
    "theme": "TERRAFORMING MARS",
    "title": "Der Sonnenwind trägt die Luft davon",
    "text": "Mars hat kein globales Magnetfeld. Der Sonnenwind trifft die Atmosphäre deshalb ungebremst und reißt beständig Gas ins All. Eine neu aufgebaute Lufthülle würde ohne Schutz auf lange Sicht dasselbe Schicksal erleiden.",
    "more": "Die Raumsonde MAVEN vermaß den Verlust auf rund 100 Gramm pro Sekunde, bei Sonnenstürmen deutlich mehr."
  },
  {
    "theme": "TERRAFORMING MARS",
    "title": "Ein Magnetschild vor dem Planeten",
    "text": "2017 schlug der NASA-Wissenschaftler Jim Green vor, zwischen Sonne und Mars ein künstliches Magnetfeld aufzuspannen. Der Schild stünde weit vor dem Planeten und lenkte den Sonnenwind um ihn herum. Die Atmosphäre könnte sich dann von selbst wieder verdichten.",
    "more": "Der Vorschlag ist eine Studie geblieben. Ein Magnetfeld dieser Größe hat noch niemand gebaut."
  },
  {
    "theme": "TERRAFORMING MARS",
    "title": "Der Boden ist giftig",
    "text": "Im Marsstaub stecken Perchlorate, Salze der Überchlorsäure. Der Lander Phoenix wies sie 2008 nach, spätere Messungen fanden sie überall. Schon unter einem Prozent stört die Schilddrüse und macht den Boden ohne Behandlung für Pflanzen unbrauchbar.",
    "more": "Manche irdischen Bakterien atmen Perchlorat und könnten den Boden womöglich entgiften."
  },
  {
    "theme": "TERRAFORMING MARS",
    "title": "Wärmer wird es nicht von allein",
    "text": "Auf dem Mars liegt die mittlere Temperatur bei etwa minus 63 Grad. Selbst am Äquator fällt sie nachts unter minus 70 Grad. Damit flüssiges Wasser dauerhaft bestehen könnte, müsste das Mittel um mehr als 60 Grad steigen.",
    "more": "Zum Vergleich: Auf der Erde liegt die mittlere Temperatur bei rund 15 Grad."
  },
  {
    "theme": "TERRAFORMING MARS",
    "title": "Wasser ist genug da, nur gefroren",
    "text": "An Wasser mangelt es dem Mars nicht. In den Polkappen und unter der Oberfläche steckt so viel Eis, dass es den ganzen Planeten mehrere Meter hoch bedecken würde. Beim heutigen Luftdruck bliebe es nur nicht flüssig.",
    "more": "Radarmessungen der Sonde Mars Express fanden 2018 Hinweise auf Wasser unter dem Südpol; die Deutung ist umstritten."
  },
  {
    "theme": "TERRAFORMING MARS",
    "title": "Weniger Schwerkraft, unbekannte Folgen",
    "text": "Auf dem Mars wiegt ein Mensch nur 38 Prozent dessen, was er auf der Erde wiegt. Wie sich das über Jahre auswirkt, weiß niemand: Alle Daten stammen aus der Schwerelosigkeit oder von wenigen Tagen auf dem Mond.",
    "more": "Auf der Raumstation verlieren Menschen ohne tägliches Training rund ein Prozent Knochenmasse im Monat."
  },
  {
    "theme": "ARTEMIS 2",
    "title": "Vier Menschen um den Mond",
    "text": "Artemis 2 ist der erste bemannte Flug des Raumschiffs Orion. An Bord sind vier Menschen: Reid Wiseman, Victor Glover, Christina Koch und der Kanadier Jeremy Hansen. Der Weg führt einmal um den Mond herum und zurück, ohne in eine Umlaufbahn einzuschwenken.",
    "more": "Christina Koch hält mit 328 Tagen am Stück den Rekord für den längsten Raumflug einer Frau."
  },
  {
    "theme": "ARTEMIS 2",
    "title": "Der weiteste Ausflug seit 1972",
    "text": "Seit Apollo 17 im Dezember 1972 kam kein Mensch mehr weiter hinaus als in eine Erdumlaufbahn. Artemis 2 führt wieder darüber hinaus, hinter den Mond und zurück. Zwischen den beiden Flügen liegen mehr als fünfzig Jahre.",
    "more": "Die zwölf Menschen, die auf dem Mond gestanden haben, waren alle zwischen 1969 und 1972 dort."
  },
  {
    "theme": "ARTEMIS 2",
    "title": "Die Bahn bringt sie von selbst zurück",
    "text": "Artemis 2 fliegt auf einer freien Rückkehrbahn. Die Schwerkraft des Mondes lenkt das Raumschiff dabei so um, dass es ohne weiteres Zünden von allein zur Erde zurückfällt. Fällt unterwegs der Antrieb aus, kommt die Besatzung trotzdem heim.",
    "more": "Eine solche Bahn rettete 1970 die Besatzung von Apollo 13, nachdem ein Sauerstofftank explodiert war."
  },
  {
    "theme": "ARTEMIS 2",
    "title": "Zehn Tage, kein Landeanflug",
    "text": "Der Flug ist auf rund zehn Tage angelegt, gelandet wird nicht. Artemis 2 soll zeigen, dass Orion Menschen sicher hinaus und zurückbringt und dass Lebenserhaltung, Navigation und Funk über diese Entfernung arbeiten. Das Landen bleibt späteren Flügen vorbehalten.",
    "more": "Der Vorgänger Artemis 1 flog dieselbe Strecke 2022 unbemannt, mit Messpuppen auf den Sitzen."
  },
  {
    "theme": "ARTEMIS 2",
    "title": "Die Rückkehr ist der heißeste Teil",
    "text": "Orion kommt mit fast 40.000 Kilometern pro Stunde in die Erdatmosphäre zurück. Der Hitzeschild muss dabei rund 2.800 Grad aushalten. Beim unbemannten Vorgängerflug löste sich mehr Material vom Schild als erwartet.",
    "more": "Der Schild besteht aus Avcoat, einem Material, das gezielt verglüht und die Wärme mit sich fortträgt."
  },
  {
    "theme": "ARTEMIS 2",
    "title": "Jedes Gespräch hat eine Pause",
    "text": "Vom Mond zur Erde braucht ein Funksignal etwa 1,3 Sekunden. Zwischen einer Frage und ihrer Antwort liegen also mindestens zweieinhalb Sekunden. Gespräche zwischen Besatzung und Bodenkontrolle bekommen dadurch ihren stockenden Rhythmus.",
    "more": "Zum Mars dauert dasselbe je nach Stellung der Planeten zwischen drei und 22 Minuten je Richtung."
  },
  {
    "theme": "ARTEMIS 2",
    "title": "Eine Rakete, die nur einmal fliegt",
    "text": "Getragen wird Artemis 2 von der Rakete Space Launch System. Sie ist gut 98 Meter hoch und liefert beim Start rund 39 Meganewton Schub. Jede dieser Raketen fliegt genau einmal, wiederverwendet wird nichts.",
    "more": "Die Saturn V der Apollo-Flüge war mit 110 Metern höher, hatte aber weniger Schub beim Start."
  },
  {
    "theme": "ARTEMIS 2",
    "title": "Warum überhaupt zurück zum Mond",
    "text": "Artemis zielt nicht auf einen Besuch, sondern auf ein Bleiben. Am Südpol des Mondes liegt in nie besonnten Kratern Wassereis. Wasser lässt sich trinken, atmen und zu Treibstoff verarbeiten.",
    "more": "Ein Kilogramm zum Mond zu bringen kostet ein Vielfaches dessen, was ein Kilogramm in die Erdumlaufbahn kostet."
  },
  {
    "theme": "WARPANTRIEB",
    "title": "Nicht das Schiff bewegt sich",
    "text": "Ein Warpantrieb umgeht das Tempolimit der Lichtgeschwindigkeit, indem er nicht das Schiff beschleunigt, sondern den Raum darum. Vor dem Schiff wird der Raum gestaucht, dahinter gedehnt. Das Schiff selbst ruht in seiner Blase.",
    "more": "Für den Raum gilt kein Tempolimit. Kurz nach dem Urknall dehnte er sich weit schneller aus, als Licht fliegt."
  },
  {
    "theme": "WARPANTRIEB",
    "title": "1994 wurde es vorgerechnet",
    "text": "Der Physiker Miguel Alcubierre veröffentlichte 1994 eine Lösung der einsteinschen Feldgleichungen, die genau so eine Blase beschreibt. Die Rechnung ist mathematisch sauber. Über die Frage, ob sich das Nötige beschaffen lässt, sagt sie nichts.",
    "more": "Alcubierre gab später an, die Idee beim Ansehen von Star Trek gehabt zu haben."
  },
  {
    "theme": "WARPANTRIEB",
    "title": "Es braucht Materie, die es nicht gibt",
    "text": "Die Blase hält nur zusammen, wenn man Materie mit negativer Energiedichte hineinsteckt, also etwas, das weniger als nichts wiegt. Beobachtet wurde so etwas nie. Bekannt ist lediglich ein schwacher verwandter Effekt zwischen zwei Metallplatten im Vakuum.",
    "more": "Der Casimir-Effekt erzeugt zwischen zwei Platten einen winzigen Bereich negativer Energiedichte."
  },
  {
    "theme": "WARPANTRIEB",
    "title": "Erst ein Universum, dann ein paar Zentner",
    "text": "Alcubierres erste Abschätzung verlangte negative Energie in der Größenordnung des ganzen sichtbaren Universums. Spätere Arbeiten drückten den Bedarf auf die Masse des Jupiter, dann auf einige Hundert Kilogramm.",
    "more": "Die Verkleinerung gelang durch dünnere Blasenwände und eine schwingende Blase, nicht durch neue Physik."
  },
  {
    "theme": "WARPANTRIEB",
    "title": "Die Blase sammelt unterwegs ein",
    "text": "2012 rechneten Physiker durch, was eine Warpblase auf ihrem Weg aufliest. Teilchen, die ihr in die Quere kommen, stauen sich an der Blasenwand. Beim Anhalten würden sie nach vorn losgelassen und alles vor dem Schiff verglühen lassen.",
    "more": "Die Arbeit stammt von Brendan McMonigal, Geraint Lewis und Philip O'Byrne."
  },
  {
    "theme": "WARPANTRIEB",
    "title": "Und die Zeit gerät durcheinander",
    "text": "Wer schneller als das Licht reist, reist von manchen Standpunkten aus gesehen rückwärts in der Zeit. Zwei Warpflüge nacheinander könnten ein Schiff zurückschicken, bevor es losgeflogen ist.",
    "more": "Stephen Hawking vermutete, die Physik verhindere Zeitreisen von selbst, und nannte das Chronologieschutz."
  },
  {
    "theme": "WARPANTRIEB",
    "title": "Eine Warpblase ohne Überlichtgeschwindigkeit",
    "text": "2021 zeigten Alexey Bobrick und Gianni Martire, dass sich Warpblasen auch ohne negative Energie beschreiben lassen. Der Preis ist hoch: Solche Blasen bleiben langsamer als das Licht. Als Antrieb taugen sie damit nicht, als Rechenbeispiel schon.",
    "more": "Nötig wären trotzdem Massen in der Größenordnung ganzer Planeten."
  },
  {
    "theme": "WARPANTRIEB",
    "title": "Gemessen wurde bisher nichts",
    "text": "Kein Experiment hat je eine Warpblase erzeugt oder eine Spur davon gefunden. Ein NASA-Labor suchte jahrelang mit Laserinterferometern nach winzigen Verzerrungen des Raums, ohne Ergebnis.",
    "more": "Der Warpantrieb ist Rechnung geblieben, anders als der Ionenantrieb, der ebenfalls aus der Literatur kam und heute fliegt."
  },
  {
    "theme": "FIKTION WIRD WIRKLICH",
    "title": "Der Kommunikator wurde zum Handy",
    "text": "Martin Cooper baute 1973 bei Motorola das erste Mobiltelefon. Als Vorbild nannte er den Kommunikator aus Star Trek, den er wenige Jahre zuvor im Fernsehen gesehen hatte. Das Gerät wog rund ein Kilogramm und hielt eine halbe Stunde durch.",
    "more": "Cooper führte den ersten Anruf auf offener Straße in New York, und zwar bei einem Konkurrenten."
  },
  {
    "theme": "FIKTION WIRD WIRKLICH",
    "title": "Jules Verne traf beinahe alles",
    "text": "In Jules Vernes Roman von 1865 startet eine Kapsel mit drei Mann von Florida aus zum Mond und fällt am Ende in den Pazifik. Apollo 11 startete gut hundert Jahre später aus Florida, mit drei Mann, und wasserte im Pazifik.",
    "more": "Verne rechnete auch die nötige Startgeschwindigkeit aus und lag nur wenige Prozent daneben."
  },
  {
    "theme": "FIKTION WIRD WIRKLICH",
    "title": "Der geostationäre Satellit stand im Aufsatz",
    "text": "1945 beschrieb der Schriftsteller Arthur C. Clarke in einer Fachzeitschrift, wie drei Satelliten in 36.000 Kilometern Höhe die ganze Erde mit Funk versorgen könnten. In dieser Höhe braucht ein Satellit genau einen Tag pro Umlauf und steht deshalb still über einem Punkt.",
    "more": "Die Bahn heißt heute Clarke-Gürtel. Clarke selbst hat die Idee nie patentieren lassen."
  },
  {
    "theme": "FIKTION WIRD WIRKLICH",
    "title": "Das Tablet lief 1968 im Kino",
    "text": "In Stanley Kubricks Film 2001 essen zwei Astronauten und schauen dabei auf flache Bildschirme, die lose auf dem Tisch liegen. Als Samsung 2011 von Apple wegen des Aussehens des iPad verklagt wurde, führte der Konzern diese Szene an, um zu zeigen, dass die Form älter sei.",
    "more": "Das Gericht ließ den Einwand nicht zu."
  },
  {
    "theme": "FIKTION WIRD WIRKLICH",
    "title": "Der Taser heißt nach einem Romanhelden",
    "text": "Der Erfinder Jack Cover benannte seine Elektrowaffe nach einem Jugendbuch: Tom Swift and His Electric Rifle. Aus dem Titel wurde die Abkürzung TSER, die sich schlecht sprechen ließ. Cover schob ein A dazwischen, und daraus wurde Taser.",
    "more": "Die Bücher um den jungen Erfinder Tom Swift erscheinen seit 1910."
  },
  {
    "theme": "FIKTION WIRD WIRKLICH",
    "title": "Das Bildtelefon aus dem Stummfilm",
    "text": "In Fritz Langs Film Metropolis von 1927 telefoniert der Herrscher der Stadt mit Bild. Die Wirklichkeit war schneller als gedacht: Ab 1936 betrieb die Deutsche Reichspost Bildtelefonstuben zwischen Berlin und Leipzig.",
    "more": "Die Verbindung lief über eigens verlegte Breitbandkabel. Der Betrieb endete im Krieg."
  },
  {
    "theme": "FIKTION WIRD WIRKLICH",
    "title": "Raketen, die auf dem Heck landen",
    "text": "Rückwärts landende Raketen waren jahrzehntelang ein Bild aus Comics und Filmen, während die Raumfahrt ihre Stufen im Meer versenkte. Seit 2015 landet die erste Stufe der Falcon 9 regelmäßig senkrecht, auf einer Betonplatte oder auf einem Schiff.",
    "more": "Einzelne Exemplare sind mehr als zwanzigmal geflogen."
  },
  {
    "theme": "FIKTION WIRD WIRKLICH",
    "title": "Der Roboterarm hieß erst Waldo",
    "text": "Robert Heinlein beschrieb 1942 in einer Erzählung ferngesteuerte Greifarme, mit denen ein kranker Erfinder schwere Arbeit verrichtet. Die Technik steht heute in jedem Labor mit radioaktivem Material. In der Fachsprache heißen solche Manipulatoren bis heute Waldos.",
    "more": "Heinlein veröffentlichte die Geschichte unter dem Namen Anson MacDonald."
  }
];

  const stand = E.getState();
  const da = new Set(stand.cards.map(c => c.title.trim().toLowerCase()));
  const fehlend = NEU.filter(c => !da.has(c.title.trim().toLowerCase()));
  if (!fehlend.length) return "Alle 32 Karten sind schon da - nichts zu tun.";

  E.setState({
    meta: stand.meta,
    themes: [...stand.themes, ...THEMEN.filter(t => !stand.themes.includes(t))],
    cards: [...stand.cards, ...fehlend.map(c => ({...c, id: E.newId()}))]
  });
  E.setDirty(true);
  return `${fehlend.length} Karten eingefuegt, jetzt ${E.S.cards.length} insgesamt. `
       + `Zum Schreiben unten auf "Speichern" druecken.`;
})()
