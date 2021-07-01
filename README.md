![DBNL banner](banners/AlgemeenLetterkundigLexicon_BannerWikimedia_NL.jpg)
# DBNL-Algemeen-letterkundig-lexicon
https://www.wikidata.org/wiki/Wikidata:WikiProject_Algemeen_letterkundig_lexicon

*Turning https://www.dbnl.org/tekst/dela012alge01_01/ into Linked Open Data using Wikidata*

* Lijst van alle begrippen: https://kbnlwikimedia.github.io/DBNL-Algemeen-letterkundig-lexicon/scrapemaps/all-begrippen.html (webrender of [this file](scrapemaps/all-begrippen.html))
* Let op verschil tussen 'begrip' en 'lemma' (nog uitwerken)
* Reconcile sources (https://github.com/KBNLwikimedia/DBNL-Algemeen-letterkundig-lexicon/blob/master/20200708%20Sources%20ALL.csv) and authors of these sources with Wikidata so they can be used as references or 'P973/Described at' with the (future) Q-ids.

1e zin uit een stuk tekst halen met regexp: https://stackoverflow.com/questions/46167065/extracting-first-sentence-from-a-paragraph
*Regular Expressions can definitely be used. The following uses a simple but typical definition of "end of sentence": a ., ! or ? followed by either 1) at least one space then a capital letter, or 2) the end of the text.*

## Wikidata
* <a href="https://www.wikidata.org/wiki/Q96870923"> Algemeen Letterkundig Lexicon (Q96870923)</a>
* <a href="https://www.wikidata.org/wiki/Q97097245"> Digital Algemeen Letterkundig Lexicon (Q97097245) </a>

## Wikipedia NL
* https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/ALL (i.v.m. stageopdracht Calvin Keutgen april-augustus 2021)
* https://nl.wikipedia.org/wiki/Sjabloon:Bronvermelding_ALL
* https://nl.wikipedia.org/wiki/Gebruiker:CalvinKeutgen/Lijst_van_letterkundige_begrippen <sub>(voor script die deze pagina genereert, zie [scripts/image-downloader/export-Lijst-van-letterkundige-begrippen](scripts/image-downloader/export-Lijst-van-letterkundige-begrippen))</sub>
