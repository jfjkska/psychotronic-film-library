"""Hand-curated deep cuts for the connections report (tools/make_connections.py).

Credits listed in the reviews (director, starring, music) are linked automatically.
Everything here is the stuff that isn't in the front matter: a film outside the
library that two or more library films both feed into, an uncredited writer, a
family tie, a club. Keys are review slugs (the filename without the date).

Each HUB is a film, show or company that is NOT in the library. `films` maps a
library slug to the person or reason that carries the link.
"""

HUBS = [
    {
        "id": "solange", "name": "Dallamano's schoolgirl trilogy", "year": "1972–78",
        "blurb": "What Have You Done to Solange? (1972) and What Have They Done to Your Daughters? (1974). "
                 "Dallamano co-wrote a third part, Enigma Rosso, then died in 1976; Alberto Negrin finished it "
                 "as Red Rings of Fear. The cast of the first two leaks all over the library.",
        "films": {
            "devil-in-the-flesh": "Massimo Dallamano directed both of the first two",
            "red-rings-of-fear": "the third part of the trilogy; Fabio Testi also led Solange",
            "tragic-ceremony": "Camille Keaton played Solange herself",
            "the-house-that-screamed": "Cristina Galbó played the doomed Elizabeth in Solange",
            "exorcist-ii-the-heretic": "Ennio Morricone scored Solange",
            "hands-of-steel": "Claudio Cassinelli led Daughters as Inspector Silvestri",
            "milano-calibro-9": "Mario Adorf co-stars in Daughters",
        },
    },
    {
        "id": "black-sabbath", "name": "Black Sabbath", "year": "1963",
        "blurb": "Mario Bava's three-part portmanteau. AIP had Les Baxter rescore it for America.",
        "films": {
            "hannah-queen-of-the-vampires": "Mark Damon is the young count in 'The Wurdalak', opposite Boris Karloff",
            "web-of-the-spider": "Michèle Mercier is the woman terrorised in 'The Telephone'",
            "frogs": "Les Baxter wrote the US score",
        },
    },
    {
        "id": "black-sunday", "name": "Black Sunday", "year": "1960",
        "blurb": "Bava's debut as director, the film that made Barbara Steele the face of Italian gothic.",
        "films": {
            "long-hair-of-death": "Barbara Steele, four years before",
            "eyeball": "John Richardson plays the young doctor who falls for Steele",
            "frogs": "Les Baxter again, on the AIP release",
        },
    },
    {
        "id": "castle-of-blood", "name": "Castle of Blood", "year": "1964",
        "blurb": "Margheriti's black-and-white ghost story with Barbara Steele.",
        "films": {
            "web-of-the-spider": "Margheriti remade it in colour as Web of the Spider",
            "long-hair-of-death": "same director, same star, same year, much the same crypts",
        },
    },
    {
        "id": "count-dracula", "name": "Count Dracula", "year": "1970",
        "blurb": "Jess Franco's El conde Drácula with Christopher Lee. The supporting cast is half of Franco's "
                 "stock company plus Klaus Kinski eating flies.",
        "films": {
            "she-killed-in-ecstasy": "Soledad Miranda (Lucy), Fred Williams (Harker) and Paul Muller (Seward)",
            "succubus": "Jack Taylor (Quincey) and Franco directing",
            "red-rings-of-fear": "Jack Taylor",
            "tragic-ceremony": "Paul Muller",
            "web-of-the-spider": "Klaus Kinski as Renfield",
            "devil-hunter": "Franco directing",
        },
    },
    {
        "id": "great-silence", "name": "The Great Silence", "year": "1968",
        "blurb": "Sergio Corbucci's snowbound western, the bleakest of them all.",
        "films": {
            "blacula": "Vonetta McGee is the widow who hires the mute gunman",
            "web-of-the-spider": "Klaus Kinski is the bounty killer Loco",
        },
    },
    {
        "id": "bunuel", "name": "Luis Buñuel's players", "year": "1962–67",
        "blurb": "Belle de Jour, The Exterminating Angel, Simon of the Desert. Three library actors did time with Buñuel.",
        "films": {
            "one-on-top-of-the-other": "Jean Sorel is Pierre, Catherine Deneuve's husband, in Belle de Jour",
            "the-fox-with-the-velvet-tail": "Jean Sorel again",
            "nightmare-city": "Francisco Rabal is the gangster Hyppolite in Belle de Jour (and the lead of Viridiana)",
            "alucarda": "Claudio Brook in The Exterminating Angel and as Simon of the Desert",
        },
    },
    {
        "id": "tenebrae", "name": "Tenebrae", "year": "1982",
        "blurb": "Argento's white-on-white giallo, and a video nasty in its own right.",
        "films": {
            "web-of-the-spider": "Anthony Franciosa plays the novelist Peter Neal",
            "i-dont-want-to-be-born": "John Steiner plays the TV critic Berti",
            "hands-of-steel": "John Saxon plays the agent Bullmer; Claudio Simonetti co-wrote the score",
            "the-bloodstained-shadow": "scored by the same Goblin line-up",
            "zombie-creeping-flesh": "Goblin, whose music Mattei recycled",
        },
    },
    {
        "id": "fulci", "name": "Fulci's gore cycle", "year": "1979–81",
        "blurb": "Zombie Flesh Eaters, City of the Living Dead, The Beyond, The Black Cat, The House by the Cemetery. "
                 "Ten years after One on Top of the Other, Fulci's casts were full of library faces.",
        "films": {
            "one-on-top-of-the-other": "Lucio Fulci directed it",
            "the-last-hunter": "Tisa Farrow (Zombie Flesh Eaters); David Warbeck (The Beyond, The Black Cat)",
            "devil-hunter": "Al Cliver (Zombie Flesh Eaters, The Beyond)",
            "the-perfume-of-the-lady-in-black": "Mimsy Farmer leads The Black Cat",
            "the-laughing-woman": "Dagmar Lassander (The Black Cat, The House by the Cemetery)",
            "hands-of-steel": "Janet Agren (City of the Living Dead)",
            "seven-deaths-in-the-cats-eye": "Venantino Venantini (City of the Living Dead)",
        },
    },
    {
        "id": "anthropophagous", "name": "Anthropophagous", "year": "1980",
        "blurb": "Joe D'Amato's video nasty: George Eastman as a starving cannibal on a Greek island.",
        "films": {
            "the-last-hunter": "Tisa Farrow leads it, the same year",
            "emanuelle-e-francoise": "Joe D'Amato directing George Eastman again",
            "2019-after-the-fall-of-new-york": "George Eastman",
            "hands-of-steel": "George Eastman",
        },
    },
    {
        "id": "martino-gialli", "name": "Sergio Martino's gialli", "year": "1971–73",
        "blurb": "The Strange Vice of Mrs Wardh, All the Colors of the Dark, Your Vice Is a Locked Room. Before the "
                 "cyborgs and the post-nuke wastelands, Martino made the slickest gialli of the early seventies.",
        "films": {
            "2019-after-the-fall-of-new-york": "Martino directed",
            "hands-of-steel": "Martino directed",
            "the-case-of-the-bloody-iris": "Edwige Fenech and George Hilton, both leads in Mrs Wardh",
            "strip-nude-for-your-killer": "Edwige Fenech, Martino's giallo star",
            "one-on-top-of-the-other": "Alberto de Mendoza, the husband in Mrs Wardh",
        },
    },
    {
        "id": "great-alligator", "name": "The Great Alligator", "year": "1979",
        "blurb": "Martino's Jaws in a jungle resort. Claudio Cassinelli was later killed in a helicopter crash "
                 "while shooting Hands of Steel in Arizona.",
        "films": {
            "hands-of-steel": "Claudio Cassinelli and Martino",
            "2019-after-the-fall-of-new-york": "Martino",
            "nightmare-city": "Mel Ferrer runs the resort",
        },
    },
    {
        "id": "manchester-morgue", "name": "The Living Dead at Manchester Morgue", "year": "1974",
        "blurb": "Jorge Grau's Lake District zombie film, prosecuted as a video nasty.",
        "films": {
            "the-house-that-screamed": "Cristina Galbó is the heroine",
            "queens-of-evil": "Ray Lovelock is the hero",
        },
    },
    {
        "id": "horror-express", "name": "Horror Express", "year": "1972",
        "blurb": "Lee and Cushing on the Trans-Siberian with a thawed ape-man. A Spanish production with a Spanish supporting cast.",
        "films": {
            "one-on-top-of-the-other": "Alberto de Mendoza as the mad monk Pujardov",
            "black-candles": "Helga Liné as the spy Natasha",
            "the-case-of-the-bloody-iris": "George Rigaud as Count Petrovski",
        },
    },
    {
        "id": "fistful", "name": "A Fistful of Dollars", "year": "1964",
        "blurb": "Leone's first Dollars film.",
        "films": {
            "devil-in-the-flesh": "Massimo Dallamano was Leone's cinematographer",
            "the-devils-nightmare": "Alessandro Alessandroni is the whistle on the theme",
            "exorcist-ii-the-heretic": "Ennio Morricone wrote it",
        },
    },
    {
        "id": "eyes-without-a-face", "name": "Eyes Without a Face", "year": "1960",
        "blurb": "Franju's surgeon peels faces off girls to fix his daughter's. Franco copied it two years later as "
                 "The Awful Dr Orlof with Howard Vernon.",
        "films": {
            "the-bloodstained-shadow": "Juliette Mayniel is the first girl on the slab",
            "succubus": "Howard Vernon, Franco's Dr Orlof",
            "she-killed-in-ecstasy": "Howard Vernon, plus a heroine whose husband was a surgeon",
        },
    },
    {
        "id": "hammer", "name": "Hammer Films", "year": "1958–74",
        "blurb": "The British gothic studio the library's British films grew up in the shadow of, and in some "
                 "cases tried to kill off.",
        "films": {
            "mumsy-nanny-sonny-and-girly": "Freddie Francis directed Dracula Has Risen from the Grave",
            "frightmare": "Rupert Davies is the Monsignor in Dracula Has Risen from the Grave",
            "i-dont-want-to-be-born": "Peter Sasdy directed Taste the Blood of Dracula, with Ralph Bates; "
                                      "Caroline Munro was in Dracula AD 1972 and Captain Kronos",
            "house-on-straw-hill": "Linda Hayden is Alice in Taste the Blood of Dracula",
            "schizo": "Lynne Frederick (Vampire Circus) and Stephanie Beacham (Dracula AD 1972)",
            "house-of-mortal-sin": "Stephanie Beacham (Dracula AD 1972)",
            "the-house-that-screamed": "John Moulder-Brown (Vampire Circus)",
            "groupie-girl": "the Collinson twins went straight on to Twins of Evil",
            "satans-slave": "Michael Gough (Dracula, 1958)",
            "intimate-confessions-of-a-chinese-courtesan": "Shaw Brothers co-produced The Legend of the 7 Golden Vampires with Hammer",
        },
    },
    {
        "id": "amicus", "name": "Tales from the Crypt", "year": "1972",
        "blurb": "Amicus portmanteau. In the Christmas segment a killer Santa comes for Joan Collins.",
        "films": {
            "i-dont-want-to-be-born": "Joan Collins",
            "mumsy-nanny-sonny-and-girly": "Freddie Francis directed it",
            "silent-night-bloody-night": "the other killer-at-Christmas film of 1972",
        },
    },
    {
        "id": "warhol", "name": "Andy Warhol's Factory", "year": "1966–74",
        "blurb": "Chelsea Girls, Flesh for Frankenstein, Blood for Dracula, L'Amour.",
        "films": {
            "silent-night-bloody-night": "Mary Woronov, plus Candy Darling, Ondine and Tally Brown in the flashbacks",
            "house-on-straw-hill": "Udo Kier, Morrissey's Frankenstein and Dracula",
            "the-bloodstained-shadow": "Stefania Casini, one of the daughters in Blood for Dracula",
            "the-perfume-of-the-lady-in-black": "Donna Jordan, star of Warhol and Morrissey's L'Amour",
        },
    },
    {
        "id": "corman", "name": "Roger Corman's New World", "year": "1972–79",
        "blurb": "Death Race 2000, The Big Bird Cage, Rock 'n' Roll High School.",
        "films": {
            "private-parts": "Paul Bartel directed Death Race 2000, and acts in Arkush's Rock 'n' Roll High School",
            "deathsport": "Corman's cash-in sequel to Death Race 2000, David Carradine again; Allan Arkush co-directed",
            "silent-night-bloody-night": "Mary Woronov is Calamity Jane in Death Race 2000",
            "spider-baby": "Jack Hill made The Big Bird Cage, with Sid Haig",
            "invasion-of-the-bee-girls": "Anitra Ford is in The Big Bird Cage",
        },
    },
    {
        "id": "satyricon", "name": "Fellini Satyricon", "year": "1969",
        "blurb": "Fellini's two leads went from Rome to the drive-in.",
        "films": {
            "seven-deaths-in-the-cats-eye": "Hiram Keller (Ascyltus)",
            "satans-slave": "Martin Potter (Encolpius)",
        },
    },
    {
        "id": "dont-look-now", "name": "Don't Look Now", "year": "1973",
        "blurb": "Nic Roeg's Venice: churches, a blind psychic, a small figure in a red coat.",
        "films": {
            "i-dont-want-to-be-born": "Hilary Mason, the blind psychic",
            "the-bloodstained-shadow": "Massimo Serato, the bishop",
            "alice-sweet-alice": "a small killer in a yellow raincoat, three years later",
        },
    },
    {
        "id": "apocalypse", "name": "Apocalypse Now / The Deer Hunter", "year": "1978–79",
        "blurb": "The two Vietnam epics every Italian war film of 1980 fed off.",
        "films": {
            "the-last-hunter": "the rip-off, title and all",
            "death-game": "Colleen Camp is one of the Playboy Playmates in Apocalypse Now",
            "spider-baby": "Quinn Redeker shared the Oscar nomination for The Deer Hunter's story",
        },
    },
    {
        "id": "caligula", "name": "Caligula", "year": "1979",
        "blurb": "Penthouse's notorious epic.",
        "films": {
            "caligula-and-messalina": "the cash-in",
            "i-dont-want-to-be-born": "John Steiner plays Longinus",
        },
    },
    {
        "id": "horror-hospital", "name": "Horror Hospital", "year": "1973",
        "blurb": "Antony Balch's lobotomy farce.",
        "films": {
            "satans-slave": "Michael Gough is the mad doctor",
            "cool-it-carol": "Robin Askwith is the pop singer",
            "the-flesh-and-blood-show": "Robin Askwith",
        },
    },
    {
        "id": "mulberry-bush", "name": "Here We Go Round the Mulberry Bush", "year": "1968",
        "blurb": "Swinging-sixties sex comedy set in Stevenage.",
        "films": {
            "die-screaming-marianne": "Barry Evans in the lead",
            "mumsy-nanny-sonny-and-girly": "Vanessa Howard (Girly) is one of his targets",
        },
    },
    {
        "id": "two-heads", "name": "The Thing with Two Heads", "year": "1972",
        "blurb": "A bigot's head grafted on to Rosey Grier's body. Made for AIP, Frogs' studio, the same year.",
        "films": {
            "love-camp-7": "Lee Frost directed both",
            "frogs": "Ray Milland is the head",
        },
    },
    {
        "id": "living-dead-girl", "name": "Jean Rollin's other films", "year": "1982",
        "blurb": "The Living Dead Girl.",
        "films": {
            "caligula-and-messalina": "Françoise Blanchard went straight on to play Rollin's Living Dead Girl",
            "lips-of-blood": "Rollin",
            "the-iron-rose": "Rollin",
            "the-grapes-of-death": "Rollin",
        },
    },
    {
        "id": "mind-your-language", "name": "Mind Your Language", "year": "ITV, 1977–79",
        "blurb": "The adult-education sitcom.",
        "films": {
            "die-screaming-marianne": "Barry Evans plays the teacher, Jeremy Brown",
            "the-iron-rose": "Françoise Pascal plays his French student, Danielle",
        },
    },
    {
        "id": "aybs", "name": "Are You Being Served?", "year": "BBC, 1972–85",
        "blurb": "Grace Brothers.",
        "films": {
            "keep-it-up-jack": "Frank Thornton, Captain Peacock",
            "house-of-whipcord": "Penny Irving, Young Mr Grace's secretary Miss Bakewell",
        },
    },
]

# Same person, both films, not visible in the listed credits.
DIRECT = [
    ("satans-slave", "the-flesh-and-blood-show", "Candace Glendenning"),
    ("house-of-whipcord", "frightmare", "David McGillivray (writer)"),
    ("frightmare", "house-of-mortal-sin", "David McGillivray (writer)"),
    ("house-of-mortal-sin", "schizo", "David McGillivray (writer)"),
    ("schizo", "satans-slave", "David McGillivray (writer)"),
    ("silent-night-bloody-night", "deathsport", "John Carradine and his son David"),
    ("hands-of-steel", "the-bloodstained-shadow", "Claudio Simonetti / Goblin"),
    ("hands-of-steel", "zombie-creeping-flesh", "Claudio Simonetti / Goblin"),
]

# Clubs: a shared distinction rather than a shared film.
CLUBS = [
    {"id": "playmates", "name": "Playboy Playmates", "films": {
        "invasion-of-the-bee-girls": "Victoria Vetri, Playmate of the Year 1968 (as Angela Dorian)",
        "deathsport": "Claudia Jennings, Playmate of the Year 1970",
        "groupie-girl": "Mary and Madeleine Collinson, the first twin Playmates, October 1970",
        "vampyres": "Anulka Dziubinska, Miss May 1973",
        "devil-hunter": "Ursula Buchfellner, Miss October 1979",
        "death-game": "Colleen Camp played one in Apocalypse Now",
    }},
    {"id": "bond", "name": "Bond", "films": {
        "tragic-ceremony": "Luciana Paluzzi, Fiona Volpe in Thunderball",
        "i-dont-want-to-be-born": "Caroline Munro, Naomi in The Spy Who Loved Me",
        "milano-calibro-9": "Barbara Bouchet, Moneypenny in Casino Royale (1967)",
        "home-before-midnight": "Richard Todd, Ian Fleming's own first choice for Dr. No",
    }},
    {"id": "sitcom", "name": "Britcom", "films": {
        "keep-it-up-jack": "Frank Thornton, Are You Being Served?",
        "house-of-whipcord": "Penny Irving, Are You Being Served?; Ray Brooks, the voice of Mr Benn",
        "groupie-girl": "James Beck, Private Walker in Dad's Army",
        "the-virgin-witch": "Vicki Michelle, Yvette in 'Allo 'Allo!",
        "the-flesh-and-blood-show": "Luan Peters, Raylene in Fawlty Towers",
        "die-screaming-marianne": "Barry Evans, Mind Your Language",
        "the-iron-rose": "Françoise Pascal, Mind Your Language",
        "satans-slave": "Michael Craze, Ben the Doctor Who companion",
    }},
    {"id": "oscars", "name": "Oscar winners", "films": {
        "frogs": "Ray Milland, Best Actor for The Lost Weekend",
        "exorcist-ii-the-heretic": "Louise Fletcher (Cuckoo's Nest) and Ennio Morricone",
        "mumsy-nanny-sonny-and-girly": "Freddie Francis, two Oscars for cinematography",
        "the-perfume-of-the-lady-in-black": "Nicola Piovani, Life Is Beautiful",
        "milano-calibro-9": "Luis Bacalov, Il Postino",
    }},
    {"id": "sisters", "name": "Real sisters", "films": {
        "the-virgin-witch": "Ann and Vicki Michelle play sisters and are sisters",
        "groupie-girl": "the Collinson twins",
        "lips-of-blood": "Catherine and Marie-Pierre Castel, Rollin's twins",
    }},
    {"id": "nasties", "name": "On the DPP 72", "films": {
        "love-camp-7": "", "devil-hunter": "", "the-last-hunter": "",
        "zombie-creeping-flesh": "", "house-on-straw-hill": "as Exposé",
    }},
    {"id": "christmas", "name": "Christmas killers", "films": {
        "silent-night-bloody-night": "the film itself",
        "creepozoids": "Linnea Quigley went on to Silent Night, Deadly Night (1984)",
        "the-black-room": "Linnea Quigley again",
        "witchcraft-70": "Edmund Purdom later directed and starred in Don't Open Till Christmas",
        "hands-of-steel": "John Saxon is the detective in Black Christmas",
    }},
]

# Theme hubs: no shared person, a shared idea. Off by default in the map.
THEMES = [
    {"id": "t-catholic", "name": "Catholic guilt", "films": {
        "house-of-mortal-sin": "a killer priest", "alice-sweet-alice": "murder at First Communion",
        "alucarda": "a convent possessed", "exorcist-ii-the-heretic": "the Church's own sequel",
        "the-devils-nightmare": "a priest among the seven sins"}},
    {"id": "t-witches", "name": "Real witches on camera", "films": {
        "secret-rites": "Alex Sanders, 'King of the Witches'", "witchcraft-70": "Anton LaVey's Church of Satan",
        "the-virgin-witch": "a coven run out of a country house", "satans-slave": "a family coven"}},
    {"id": "t-schools", "name": "Girls' schools", "films": {
        "the-house-that-screamed": "boarding school", "red-rings-of-fear": "boarding school",
        "killers-moon": "a school choir trip", "house-of-whipcord": "a 'correction' house",
        "the-devils-plaything": "a castle of initiates"}},
    {"id": "t-vamps", "name": "Erotic vampires", "films": {
        "vampyres": "", "the-devils-plaything": "", "lips-of-blood": "", "the-black-room": "",
        "she-killed-in-ecstasy": "Soledad Miranda and Ewa Strömberg were Franco's Vampyros Lesbos the same year"}},
]

# What a film was cashing in on, or what it set going. (source, year, slug, note, direction)
LINEAGE = [
    ("The Birds", 1963, "frogs", "nature run amok", "from"),
    ("Castle of Blood", 1964, "web-of-the-spider", "self-remake", "from"),
    ("Dracula", 1958, "blacula", "the Count, reborn in 1972 LA", "from"),
    ("The Exorcist", 1973, "i-dont-want-to-be-born", "possessed infant", "from"),
    ("The Exorcist", 1973, "exorcist-ii-the-heretic", "official sequel", "from"),
    ("The Crazies", 1973, "the-grapes-of-death", "poisoned villagers", "from"),
    ("Death Race 2000", 1975, "deathsport", "Corman's follow-up", "from"),
    ("Dawn of the Dead", 1978, "zombie-creeping-flesh", "zombies, plus Goblin", "from"),
    ("Apocalypse Now", 1979, "the-last-hunter", "Vietnam, Italian style", "from"),
    ("Caligula", 1979, "caligula-and-messalina", "the cash-in", "from"),
    ("Escape from New York", 1981, "2019-after-the-fall-of-new-york", "Snake Plissken, Roman style", "from"),
    ("The Terminator", 1984, "hands-of-steel", "cyborg on a mission", "from"),
    ("Ilsa, She Wolf of the SS", 1975, "love-camp-7", "Love Camp 7 got there six years first", "to"),
    ("Suspiria", 1977, "the-house-that-screamed", "the girls' school as a trap", "to"),
    ("Black Christmas", 1974, "silent-night-bloody-night", "Christmas slasher template", "to"),
    ("Knock Knock", 2015, "death-game", "remade by Eli Roth, Locke and Camp producing", "to"),
    ("Lust for Love of a Chinese Courtesan", 1984, "intimate-confessions-of-a-chinese-courtesan", "Shaw Brothers sequel", "to"),
]

TITLE_CLASHES = [
    ("Succubus", ["succubus", "the-devils-nightmare"], "Franco's film and The Devil's Nightmare both went out as Succubus."),
    ("Trauma", ["red-rings-of-fear", "house-on-straw-hill"], "Two different films, both sold as Trauma."),
    ("Venus in Furs", ["devil-in-the-flesh"], "Dallamano's 1969 film shares its English title with Jess Franco's 1969 Venus in Furs, which stars Klaus Kinski."),
    ("…Hunter", ["the-last-hunter", "devil-hunter"], "Both 1980, both Hunters, both on the video nasty list."),
    ("…Ecstasy", ["she-killed-in-ecstasy", "the-devils-plaything"], "The Devil's Plaything was also sold as Vampire Ecstasy."),
    ("Silent Night, ___ Night", ["silent-night-bloody-night"], "Twelve years later came Silent Night, Deadly Night, with Linnea Quigley from Creepozoids and The Black Room."),
]

PSEUDONYMS = [
    ("Antonio Margheriti", "Anthony M. Dawson", ["the-last-hunter"]),
    ("Bruno Mattei", "Vincent Dawn", ["zombie-creeping-flesh"]),
    ("Sergio Martino", "Martin Dolman", ["2019-after-the-fall-of-new-york", "hands-of-steel"]),
    ("Aristide Massaccesi", "Joe D'Amato", ["emanuelle-e-francoise"]),
    ("Luigi Montefiori", "George Eastman", ["emanuelle-e-francoise", "2019-after-the-fall-of-new-york", "hands-of-steel"]),
    ("Pierluigi Conti", "Al Cliver", ["devil-hunter"]),
    ("Luciano Stella", "Tony Kendall", ["the-fox-with-the-velvet-tail"]),
    ("Annie Brilland", "Annie Belle", ["lips-of-blood"]),
]
