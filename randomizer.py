import random


AllSets = {}


class CardType(object):
    def __init__(self, name):
        self.name = name


class CardList(set):
    def __contains__(self, item):
        if not isinstance(item, Card):
            for card in self:
                if card.name == item:
                    return True
        return super(CardList, self).__contains__(item)

    def __call__(self, *names):
        cards = set()
        for card in self:
            if card.name in names:
                cards.add(card)
        return cards


class Card(object):
    def __init__(self, name, types=None, cardSet=None):
        self.name = name
        self.set = cardSet

        if isinstance(types, set):
            self.types = types
        elif types is None:
            self.types = set()
        else:
            self.types = set(types)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return "<randomizer.Card: {}>".format(self)

    def __gt__(self, other):
        return str(self) > str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __str__(self):
        if Event in self.types:
            formatStr = "({} Event): {}"
        elif Landmark in self.types:
            formatStr = "({} Landmark): {}"
        elif Project in self.types:
            formatStr = "({} Project): {}"
        elif Way in self.types:
            formatStr = "({} Way): {}"
        elif Ally in self.types:
            formatStr = "({} Ally): {}"
        else:
            formatStr = "{}: {}"
        return formatStr.format(self.set.name, self.name)


class Set(object):
    def __init__(self, name):
        global AllSets
        self.name = name
        self._cards = CardList()
        self._firstEdition = None
        self._secondEdition = None

        self._events = None
        self._landmarks = None
        self._projects = None
        self._potionCards = None
        self._ways = None
        self._allyCards = None

        AllSets[self.name] = self

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "<randomizer.Set: {}>".format(self.name)

    def _AddCards(self, cardList, cards):
        for cardData in cards:
            if isinstance(cardData, Card):
                cardList.add(cardData)
            elif isinstance(cardData, dict):
                card = Card(**cardData)
                card.set = self
                cardList.add(card)
            else:
                # Assume card data is name for now
                cardList.add(Card(cardData, cardSet=self))

    def AddCards(self, cards):
        self._AddCards(self._cards, cards)

    def RemoveCards(self, cards):
        self._cards -= cards

    @property
    def cards(self):
        return self._cards

    @property
    def firstEdition(self):
        return self._firstEdition

    @firstEdition.setter
    def firstEdition(self, cards):
        if self._firstEdition is None:
            self._firstEdition = CardList()
        self._AddCards(self._firstEdition, cards)

    @property
    def secondEdition(self):
        return self._secondEdition

    @secondEdition.setter
    def secondEdition(self, cards):
        if self._secondEdition is None:
            self._secondEdition = CardList()
        self._AddCards(self._secondEdition, cards)

    @property
    def allyCards(self):
        if self._allyCards is None:
            self._allyCards = CardList(
                card for card in self._cards if card.types & {Ally}
            )
        return self._allyCards

    @property
    def events(self):
        if self._events is None:
            self._events = CardList(
                card for card in self._cards if card.types & {Event}
            )
        return self._events

    @property
    def landmarks(self):
        if self._landmarks is None:
            self._landmarks = CardList(
                card for card in self._cards if card.types & {Landmark}
            )
        return self._landmarks

    @property
    def projects(self):
        if self._projects is None:
            self._projects = CardList(
                card for card in self._cards if card.types & {Project}
            )
        return self._projects

    @property
    def ways(self):
        if self._ways is None:
            self._ways = CardList(card for card in self._cards if card.types & {Way})
        return self._ways

    @property
    def potionCards(self):
        if self._potionCards is None:
            self._potionCards = CardList(
                card for card in self._cards if card.types & {Potion}
            )
        return self._potionCards


# Define card types
Event = CardType("Event")
Landmark = CardType("Landmark")
Project = CardType("Project")
Way = CardType("Way")
Potion = CardType("Potion")
Ally = CardType("Ally")

# Define sets
Base = Set("Base")
Base.AddCards(
    [
        "Cellar",
        "Chapel",
        "Moat",
        "Harbinger",
        "Merchant",
        "Village",
        "Workshop",
        "Vassal",
        "Bureaucrat",
        "Gardens",
        "Militia",
        "Moneylender",
        "Poacher",
        "Remodel",
        "Smithy",
        "Throne Room",
        "Bandit",
        "Council Room",
        "Festival",
        "Laboratory",
        "Library",
        "Market",
        "Mine",
        "Sentry",
        "Witch",
        "Artisan",
    ]
)
Base.firstEdition = ["Adventurer", "Chancellor", "Feast", "Spy", "Thief", "Woodcutter"]
Base.secondEdition = Base.cards(
    "Artisan", "Bandit", "Harbinger", "Merchant", "Poacher", "Sentry", "Vassal"
)

Intrigue = Set("Intrigue")
Intrigue.AddCards(
    [
        "Courtyard",
        "Lurker",
        "Pawn",
        "Masquerade",
        "Shanty Town",
        "Steward",
        "Swindler",
        "Wishing Well",
        "Baron",
        "Bridge",
        "Conspirator",
        "Diplomat",
        "Ironworks",
        "Mill",
        "Mining Village",
        "Secret Passage",
        "Courtier",
        "Duke",
        "Minion",
        "Patrol",
        "Replace",
        "Torturer",
        "Trading Post",
        "Upgrade",
        "Harem",
        "Nobles",
    ]
)
Intrigue.firstEdition = [
    "Coppersmith",
    "Great Hall",
    "Saboteur",
    "Scout",
    "Secret Chamber",
    "Tribute",
]
Intrigue.secondEdition = Intrigue.cards(
    "Courtier", "Diplomat", "Lurker", "Mill", "Patrol", "Replace", "Secret Passage"
)

Seaside = Set("Seaside")
Seaside.AddCards(
    [
        "Embargo",
        "Haven",
        "Lighthouse",
        "Native Village",
        "Pearl Diver",
        "Ambassador",
        "Fishing Village",
        "Lookout",
        "Smugglers",
        "Warehouse",
        "Caravan",
        "Cutpurse",
        "Island",
        "Navigator",
        "Pirate Ship",
        "Salvager",
        "Sea Hag",
        "Treasure Map",
        "Bazaar",
        "Explorer",
        "Ghost Ship",
        "Merchant Ship",
        "Outpost",
        "Tactician",
        "Treasury",
        "Wharf",
    ]
)

Alchemy = Set("Alchemy")
Alchemy.AddCards(
    [
        "Herbalist",
        "Apprentice",
        {"name": "Transmute", "types": {Potion}},
        {"name": "Vineyard", "types": {Potion}},
        {"name": "Apothecary", "types": {Potion}},
        {"name": "Scrying Pool", "types": {Potion}},
        {"name": "University", "types": {Potion}},
        {"name": "Alchemist", "types": {Potion}},
        {"name": "Familiar", "types": {Potion}},
        {"name": "Philosopher's Stone", "types": {Potion}},
        {"name": "Golem", "types": {Potion}},
        {"name": "Possession", "types": {Potion}},
    ]
)

Prosperity = Set("Prosperity")
Prosperity.AddCards(
    [
        "Loan",
        "Trade Route",
        "Watchtower",
        "Bishop",
        "Monument",
        "Quarry",
        "Talisman",
        "Worker's Village",
        "City",
        "Contraband",
        "Counting House",
        "Mint",
        "Mountebank",
        "Rabble",
        "Royal Seal",
        "Vault",
        "Venture",
        "Goons",
        "Grand Market",
        "Hoard",
        "Bank",
        "Expand",
        "Forge",
        "King's Court",
        "Peddler",
    ]
)

Cornucopia = Set("Cornucopia")
Cornucopia.AddCards(
    [
        "Hamlet",
        "Fortune Teller",
        "Menagerie",
        "Farming Village",
        "Horse Traders",
        "Remake",
        "Tournament",
        "Young Witch",
        "Harvest",
        "Horn of Plenty",
        "Hunting Party",
        "Jester",
        "Fairgrounds",
    ]
)

Hinterlands = Set("Hinterlands")
Hinterlands.AddCards(
    [
        "Crossroads",
        "Duchess",
        "Fool's Gold",
        "Develop",
        "Oasis",
        "Oracle",
        "Scheme",
        "Tunnel",
        "Jack of All Trades",
        "Noble Brigand",
        "Nomad Camp",
        "Silk Road",
        "Spice Merchant",
        "Trader",
        "Cache",
        "Cartographer",
        "Embassy",
        "Haggler",
        "Highway",
        "Ill-gotten Gains",
        "Inn",
        "Mandarin",
        "Margrave",
        "Stables",
        "Border Village",
        "Farmland",
    ]
)

DarkAges = Set("Dark Ages")
DarkAges.AddCards(
    [
        "Poor House",
        "Beggar",
        "Squire",
        "Vagrant",
        "Forager",
        "Hermit",
        "Market Square",
        "Sage",
        "Storeroom",
        "Urchin",
        "Armory",
        "Death Cart",
        "Feodum",
        "Fortress",
        "Ironmonger",
        "Marauder",
        "Procession",
        "Rats",
        "Scavenger",
        "Wandering Minstrel",
        "Band of Misfits",
        "Bandit Camp",
        "Catacombs",
        "Count",
        "Counterfeit",
        "Cultist",
        "Graverobber",
        "Junk Dealer",
        "Knights",
        "Mystic",
        "Pillage",
        "Rebuild",
        "Rogue",
        "Altar",
        "Hunting Grounds",
    ]
)

Guilds = Set("Guilds")
Guilds.AddCards(
    [
        "Candlestick Maker",
        "Stonemason",
        "Doctor",
        "Masterpiece",
        "Advisor",
        "Plaza",
        "Taxman",
        "Herald",
        "Baker",
        "Butcher",
        "Journeyman",
        "Merchant Guild",
        "Soothsayer",
    ]
)

Adventures = Set("Adventures")
Adventures.AddCards(
    [
        "Coin of the Realm",
        "Page",
        "Peasant",
        "Ratcatcher",
        "Raze",
        "Amulet",
        "Caravan Guard",
        "Dungeon",
        "Gear",
        "Guide",
        "Duplicate",
        "Magpie",
        "Messenger",
        "Miser",
        "Port",
        "Ranger",
        "Transmogrify",
        "Artificer",
        "Bridge Troll",
        "Distant Lands",
        "Giant",
        "Haunted Woods",
        "Lost City",
        "Relic",
        "Royal Carriage",
        "Storyteller",
        "Swamp Hag",
        "Treasure Trove",
        "Wine Merchant",
        "Hireling",
        {"name": "Alms", "types": {Event}},
        {"name": "Borrow", "types": {Event}},
        {"name": "Quest", "types": {Event}},
        {"name": "Save", "types": {Event}},
        {"name": "Scouting Party", "types": {Event}},
        {"name": "Travelling Fair", "types": {Event}},
        {"name": "Bonfire", "types": {Event}},
        {"name": "Expedition", "types": {Event}},
        {"name": "Ferry", "types": {Event}},
        {"name": "Plan", "types": {Event}},
        {"name": "Mission", "types": {Event}},
        {"name": "Pilgrimage", "types": {Event}},
        {"name": "Ball", "types": {Event}},
        {"name": "Raid", "types": {Event}},
        {"name": "Seaway", "types": {Event}},
        {"name": "Lost Arts", "types": {Event}},
        {"name": "Training", "types": {Event}},
        {"name": "Inheritance", "types": {Event}},
        {"name": "Pathfinding", "types": {Event}},
    ]
)

Empires = Set("Empires")
Empires.AddCards(
    [
        "Engineer",
        "City Quarter",
        "Overlord",
        "Royal Blacksmith",
        "Encampment/Plunder",
        "Patrician/Emporium",
        "Settlers/Bustling Village",
        "Castles",
        "Catapult/Rocks",
        "Chariot Race",
        "Enchantress",
        "Farmers' Market",
        "Gladiator/Fortune",
        "Sacrifice",
        "Temple",
        "Villa",
        "Archive",
        "Capital",
        "Charm",
        "Crown",
        "Forum",
        "Groundskeeper",
        "Legionary",
        "Wild Hunt",
        {"name": "Advance", "types": {Event}},
        {"name": "Annex", "types": {Event}},
        {"name": "Banquet", "types": {Event}},
        {"name": "Conquest", "types": {Event}},
        {"name": "Delve", "types": {Event}},
        {"name": "Dominate", "types": {Event}},
        {"name": "Donate", "types": {Event}},
        {"name": "Salt the Earth", "types": {Event}},
        {"name": "Ritual", "types": {Event}},
        {"name": "Tax", "types": {Event}},
        {"name": "Trade", "types": {Event}},
        {"name": "Triumph", "types": {Event}},
        {"name": "Wedding", "types": {Event}},
        {"name": "Windfall", "types": {Event}},
        {"name": "Aqueduct", "types": {Landmark}},
        {"name": "Arena", "types": {Landmark}},
        {"name": "Bandit Fort", "types": {Landmark}},
        {"name": "Basilica", "types": {Landmark}},
        {"name": "Baths", "types": {Landmark}},
        {"name": "Battlefield", "types": {Landmark}},
        {"name": "Colonnade", "types": {Landmark}},
        {"name": "Defiled Shrine", "types": {Landmark}},
        {"name": "Fountain", "types": {Landmark}},
        {"name": "Keep", "types": {Landmark}},
        {"name": "Labyrinth", "types": {Landmark}},
        {"name": "Mountain Pass", "types": {Landmark}},
        {"name": "Museum", "types": {Landmark}},
        {"name": "Obelisk", "types": {Landmark}},
        {"name": "Orchard", "types": {Landmark}},
        {"name": "Palace", "types": {Landmark}},
        {"name": "Tomb", "types": {Landmark}},
        {"name": "Tower", "types": {Landmark}},
        {"name": "Triumphal Arch", "types": {Landmark}},
        {"name": "Wall", "types": {Landmark}},
        {"name": "Wolf Den", "types": {Landmark}},
    ]
)

Nocturne = Set("Nocturne")
Nocturne.AddCards(
    [
        "Bard",
        "Blessed Village",
        "Cemetary + Haunted Mirror (Heirloom)",
        "Changeling",
        "Cobbler",
        "Conclave",
        "Crypt",
        "Cursed Village",
        "Den of Sin",
        "Devil's Workshop",
        "Druid",
        "Exorcist",
        "Faithful Hound",
        "Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)",
        "Guardian",
        "Ghost Town",
        "Idol",
        "Leprechaun",
        "Monastery",
        "Necromancer + Zombies",
        "Night Watchman",
        "Pixie + Goat (Heirloom)",
        "Pooka + Cursed Gold (Heirloom)",
        "Sacred Grove",
        "Secret Cave + Magic Lamp (Heirloom)",
        "Shepherd + Pasture (Heirloom)",
        "Raider",
        "Skulk",
        "Tormentor",
        "Tracker + Pouch (Heirloom)",
        "Tragic Hero",
        "Vampire",
        "Werewolf",
    ]
)

Renaissance = Set("Renaissance")
Renaissance.AddCards(
    [
        "Border Guard",
        "Ducat",
        "Lackeys",
        "Acting Troupe",
        "Cargo Ship",
        "Experiment",
        "Improve",
        "Flag Bearer",
        "Hideout",
        "Inventor",
        "Mountain Village",
        "Patron",
        "Priest",
        "Research",
        "Silk Merchant",
        "Old Witch",
        "Recruiter",
        "Scepter",
        "Scholar",
        "Sculptor",
        "Seer",
        "Spices",
        "Swashbuckler",
        "Treasurer",
        "Villain",
        {"name": "Cathedral", "types": {Project}},
        {"name": "City Gate", "types": {Project}},
        {"name": "Pageant", "types": {Project}},
        {"name": "Sewers", "types": {Project}},
        {"name": "Star Chart", "types": {Project}},
        {"name": "Exploration", "types": {Project}},
        {"name": "Fair", "types": {Project}},
        {"name": "Silos", "types": {Project}},
        {"name": "Sinister Plot", "types": {Project}},
        {"name": "Academy", "types": {Project}},
        {"name": "Capitalism", "types": {Project}},
        {"name": "Fleet", "types": {Project}},
        {"name": "Guildhall", "types": {Project}},
        {"name": "Piazza", "types": {Project}},
        {"name": "Road Network", "types": {Project}},
        {"name": "Barracks", "types": {Project}},
        {"name": "Crop Rotation", "types": {Project}},
        {"name": "Innovation", "types": {Project}},
        {"name": "Canal", "types": {Project}},
        {"name": "Citadel", "types": {Project}},
    ]
)

Menagerie = Set("Menagerie")
Menagerie.AddCards(
    [
        "Animal Fair",
        "Barge",
        "Black Cat",
        "Bounty Hunter",
        "Camel Train",
        "Cardinal",
        "Cavalry",
        "Coven",
        "Destrier",
        "Displace",
        "Falconer",
        "Fisherman",
        "Gatekeeper",
        "Goatherd",
        "Groom",
        "Hostelry",
        "Hunting Lodge",
        "Kiln",
        "Livery",
        "Mastermind",
        "Paddock",
        "Sanctuary",
        "Scrap",
        "Sheepdog",
        "Sleigh",
        "Snowy Village",
        "Stockpile",
        "Supplies",
        "Village Green",
        "Wayfarer",
        {"name": "Alliance", "types": {Event}},
        {"name": "Banish", "types": {Event}},
        {"name": "Bargain", "types": {Event}},
        {"name": "Commerce", "types": {Event}},
        {"name": "Delay", "types": {Event}},
        {"name": "Demand", "types": {Event}},
        {"name": "Desperation", "types": {Event}},
        {"name": "Enclave", "types": {Event}},
        {"name": "Enhance", "types": {Event}},
        {"name": "Gamble", "types": {Event}},
        {"name": "Invest", "types": {Event}},
        {"name": "March", "types": {Event}},
        {"name": "Populate", "types": {Event}},
        {"name": "Pursue", "types": {Event}},
        {"name": "Reap", "types": {Event}},
        {"name": "Ride", "types": {Event}},
        {"name": "Seize the Day", "types": {Event}},
        {"name": "Stampede", "types": {Event}},
        {"name": "Toil", "types": {Event}},
        {"name": "Transport", "types": {Event}},
        {"name": "Way of the Butterfly", "types": {Way}},
        {"name": "Way of the Camel", "types": {Way}},
        {"name": "Way of the Chameleon", "types": {Way}},
        {"name": "Way of the Frog", "types": {Way}},
        {"name": "Way of the Goat", "types": {Way}},
        {"name": "Way of the Horse", "types": {Way}},
        {"name": "Way of the Mole", "types": {Way}},
        {"name": "Way of the Monkey", "types": {Way}},
        {"name": "Way of the Mouse", "types": {Way}},
        {"name": "Way of the Mule", "types": {Way}},
        {"name": "Way of the Otter", "types": {Way}},
        {"name": "Way of the Owl", "types": {Way}},
        {"name": "Way of the Ox", "types": {Way}},
        {"name": "Way of the Pig", "types": {Way}},
        {"name": "Way of the Rat", "types": {Way}},
        {"name": "Way of the Seal", "types": {Way}},
        {"name": "Way of the Sheep", "types": {Way}},
        {"name": "Way of the Squirrel", "types": {Way}},
        {"name": "Way of the Turtle", "types": {Way}},
        {"name": "Way of the Worm", "types": {Way}},
    ]
)

Allies = Set("Allies")
Allies.AddCards(
    [
        "Bauble",
        "Sycophant",
        "Townsfolk: Town Crier + Blacksmith + Miller + Elder",
        "Augers: Herb Gatherer + Acolyte + Sorceress + Sibyl",
        "Clashes: Battle Plan + Archer + Warlord + Territory",
        "Forts: Tent + Garrison + Hill Fort + Stronghold",
        "Merchant Camp",
        "Importer",
        "Odysseys: Old Map, Voyage, Sunken Treasure, Distant Shore",
        "Sentinel",
        "Underling",
        "Wizards: Student, Conjurer, Sorcerer, Lich",
        "Broker",
        "Carpenter",
        "Courier",
        "Innkeeper",
        "Royal Galley",
        "Town",
        "Barbarian",
        "Capital City",
        "Contract",
        "Emissary",
        "Galleria",
        "Guildmaster",
        "Highwayman",
        "Hunter",
        "Modify",
        "Skirmisher",
        "Specialist",
        "Swap",
        "Marquis",
        {"name": "Architects' Guild", "types": {Ally}},
        {"name": "Band of Nomads", "types": {Ally}},
        {"name": "Cave Dwellers", "types": {Ally}},
        {"name": "Circle of Witches", "types": {Ally}},
        {"name": "City-state", "types": {Ally}},
        {"name": "Coastal Haven", "types": {Ally}},
        {"name": "Crafters' Guild", "types": {Ally}},
        {"name": "Desert Guides", "types": {Ally}},
        {"name": "Family of Inventors", "types": {Ally}},
        {"name": "Fellowship of Scribes", "types": {Ally}},
        {"name": "Forest Dwellers", "types": {Ally}},
        {"name": "Gang of Pickpockets", "types": {Ally}},
        {"name": "Island Folk", "types": {Ally}},
        {"name": "League of Bankers", "types": {Ally}},
        {"name": "League of Shopkeepers", "types": {Ally}},
        {"name": "Market Towns", "types": {Ally}},
        {"name": "Mountain Folk", "types": {Ally}},
        {"name": "Order of Astrologers", "types": {Ally}},
        {"name": "Order of Masons", "types": {Ally}},
        {"name": "Peaceful Cult", "types": {Ally}},
        {"name": "Plateau Shepherds", "types": {Ally}},
        {"name": "Trappers' Lodge", "types": {Ally}},
        {"name": "Woodworkers' Guild", "types": {Ally}},
    ]
)

Antiquities = Set("Antiquities")
Antiquities.AddCards(
    [
        "Inscription",
        "Agora",
        "Discovery",
        "Aquifer",
        "Tomb Raider",
        "Curio",
        "Gamepiece",
        "Dig",
        "Moundbuilder Village",
        "Encroach",
        "Stoneworks",
        "Graveyard",
        "Inspector",
        "Archaeologist",
        "Mission House",
        "Mendicant",
        "Profiteer",
        "Miner",
        "Pyramid",
        "Mastermind",
        "Mausoleum",
        "Shipwreck",
        "Collector",
        "Pharaoh",
        "Grave Watcher",
        "Stronghold",
        "Snake Charmer",
    ]
)

# Define Landscape cards
Events = Adventures.events | Empires.events | Menagerie.events
Landmarks = Empires.landmarks
Projects = Renaissance.projects
Ways = Menagerie.ways
LandscapeCards = Events | Landmarks | Projects | Ways

# Define cards requiring potions
PotionCards = Alchemy.potionCards

# Define Ally cards
AllyCards = Allies.allyCards

# Define randomizer rules
PlatinumLove = Prosperity.cards.union(
    Base.cards("Artisan", "Council Room", "Merchant", "Mine"),
    Intrigue.cards("Harem", "Nobles"),
    Seaside.cards("Explorer", "Treasure Map"),
    Alchemy.cards("Philosopher's Stone"),
    Cornucopia.cards("Tournament"),
    Hinterlands.cards("Border Village", "Cache", "Duchess", "Embassy", "Fool's Gold"),
    DarkAges.cards("Altar", "Counterfeit", "Hunting Grounds", "Poor House"),
    Guilds.cards("Masterpiece", "Soothsayer"),
    Adventures.cards(
        "Hireling", "Lost City", "Page", "Treasure Trove", "Seaway", "Training"
    ),
    Empires.cards(
        "Capital",
        "Castles",
        "Chariot Race",
        "Crown",
        "Encampment/Plunder",
        "Farmers' Market",
        "Gladiator/Fortune",
        "Groundskeeper",
        "Legionary",
        "Patrician/Emporium",
        "Sacrifice",
        "Temple",
        "Wild Hunt",
        "Triumph",
        "Delve",
        "Wedding",
        "Conquest",
        "Dominate",
        "Basilica",
        "Keep",
    ),
    Nocturne.cards(
        "Pooka + Cursed Gold (Heirloom)",
        "Raider",
        "Sacred Grove",
        "Secret Cave + Magic Lamp (Heirloom)",
        "Tragic Hero",
    ),
    Renaissance.cards("Ducat", "Scepter", "Spices", "Capitalism", "Guildhall"),
    Menagerie.cards(
        "Supplies",
        "Camel Train",
        "Stockpile",
        "Livery",
        "Animal Fair",
        "Commerce",
        "Enclave",
        "Way of the Chameleon",
    ),
    Antiquities.cards(
        "Agora",
        "Archaeologist",
        "Curio",
        "Discovery",
        "Encroach",
        "Gamepiece",
        "Moundbuilder Village",
        "Pharaoh",
        "Pyramid",
        "Snake Charmer",
        "Stoneworks",
    ),
    Allies.cards("Town", "Galleria", "Marquis"),
)

ShelterLove = DarkAges.cards.union(
    Base.cards("Remodel", "Mine"),
    Intrigue.cards("Replace", "Upgrade"),
    Seaside.cards("Salvager"),
    Alchemy.cards("Apprentice", "Scrying Pool"),
    Prosperity.cards("Bishop", "Expand", "Forge"),
    Cornucopia.cards("Remake"),
    Hinterlands.cards("Develop", "Farmland", "Trader"),
    Adventures.cards("Raze", "Transmogrify", "Trade"),
    Empires.cards(
        "Catapult/Rocks", "Sacrifice", "Fountain", "Labyrinth", "Museum", "Tomb"
    ),
    Guilds.cards("Butcher", "Journeyman", "Stonemason", "Taxman"),
    Nocturne.cards(
        "Cemetary + Haunted Mirror (Heirloom)", "Exorcist", "Necromancer + Zombies"
    ),
    Renaissance.cards("Priest", "Pageant"),
    Menagerie.cards(
        "Camel Train", "Scrap", "Displace", "Enhance", "Way of the Butterfly"
    ),
    Antiquities.cards(
        "Collector",
        "Graveyard",
        "Mendicant",
        "Pharaoh",
        "Profiteer",
        "Shipwreck",
        "Snake Charmer",
        "Stoneworks",
    ),
    Allies.cards("Broker", "Carpenter", "Modify"),
)

LooterCards = DarkAges.cards("Death Cart", "Marauder", "Cultist")

SpoilsCards = DarkAges.cards("Bandit Camp", "Marauder", "Pillage")

BoonCards = Nocturne.cards(
    "Bard",
    "Blessed Village",
    "Druid",
    "Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)",
    "Idol",
    "Pixie + Goat (Heirloom)",
    "Sacred Grove",
    "Tracker + Pouch (Heirloom)",
)

HexCards = Nocturne.cards(
    "Cursed Village", "Leprechaun", "Skulk", "Tormentor", "Vampire", "Werewolf"
)

WishCards = Nocturne.cards("Leprechaun", "Secret Cave + Magic Lamp (Heirloom)")

HorseCards = Menagerie.cards(
    "Cavalry",
    "Groom",
    "Hostelry",
    "Livery",
    "Paddock",
    "Scrap",
    "Sleigh",
    "Supplies",
    # Events
    "Bargain",
    "Demand",
    "Ride",
    "Stampede",
)

LiaisonCards = Allies.cards(
    "Bauble",
    "Sycophant",
    "Importer",
    "Wizards: Student, Conjurer, Sorcerer, Lich",
    "Underling",
    "Broker",
    "Contract",
    "Emissary",
    "Guildmaster",
)

# TrapLove: cards that care about discarding, sifting, extra kingdom pile gains, and value for multiple gains
TrapLove = Antiquities.cards.union(
    Base.cards("Vassal", "Remodel", "Workshop", "Mine", "Library", "Artisan"),
    Intrigue.cards(
        "Courtyard",
        "Lurker",
        "Masquerade",
        "Swindler",
        "Ironworks",
        "Minion",
        "Replace",
        "Upgrade",
    ),
    Seaside.cards("Lookout", "Warehouse", "Navigator", "Salvager"),
    Alchemy.cards("University"),
    Prosperity.cards(
        "Loan", "Watchtower", "Bishop", "Vault", "Venture", "Goons", "Expand", "Forge"
    ),
    Cornucopia.cards(
        "Fortune Teller",
        "Menagerie",
        "Farming Village",
        "Remake",
        "Young Witch",
        "Harvest",
        "Hunting Party",
    ),
    Hinterlands.cards(
        "Develop",
        "Oracle",
        "Trader",
        "Cartographer",
        "Embassy",
        "Haggler",
        "Margrave",
        "Border Village",
        "Farmland",
    ),
    DarkAges.cards(
        "Hermit",
        "Storeroom",
        "Urchin",
        "Feodum",
        "Rats",
        "Wandering Minstrel",
        "Catacombs",
        "Rebuild",
        "Rogue",
    ),
    Guilds.cards("Stonemason", "Butcher"),
    Adventures.cards(
        "Raze",
        "Guide",
        "Duplicate",
        "Magpie",
        "Messenger",
        "Transmogrify",
        "Scouting Party",
    ),
    Empires.cards(
        "Engineer",
        "Farmers' Market",
        "Catapult/Rocks",
        "Gladiator/Fortune",
        "Temple",
        "Forum",
        "Legionary",
        "Triumph",
        "Ritual",
        "Conquest",
        "Labyrinth",
        "Museum",
    ),
    Nocturne.cards(
        "Monastery",
        "Changeling",
        "Secret Cave + Magic Lamp (Heirloom)",
        "Devil's Workshop",
        "Exorcist",
        "Cobbler",
        "Vampire",
        "Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)",
    ),
    Renaissance.cards(
        "Experiment",
        "Inventor",
        "Research",
        "Recruiter",
        "Scholar",
        "Sculptor",
        "Villain",
    ),
    Menagerie.cards(
        "Camel Train",
        "Scrap",
        "Bounty Hunter",
        "Groom",
        "Hunting Lodge",
        "Displace",
        "Kiln",
        "Livery",
        "Destrier",
        "Enhance",
        "Commerce",
        "Populate",
        "Way of the Mole",
    ),
    Allies.cards(
        "Sycophant",
        "Townsfolk: Town Crier + Blacksmith + Miller + Elder",
        "Augers: Herb Gatherer + Acolyte + Sorceress + Sibyl",
        "Forts: Tent + Garrison + Hill Fort + Stronghold",
        "Importer",
        "Odysseys: Old Map, Voyage, Sunken Treasure, Distant Shore",
        "Sentinel",
        "Broker",
        "Carpenter",
        "Courier",
        "Innkeeper",
        "Capital City",
        "Galleria",
        "Guildmaster",
        "Hunter",
        "Specialist",
        "Swap",
        "Marquis",
        "Architect's Guild",
        "Coastal Haven",
        "Desert Guides",
    ),
)

BaneCards = set().union(
    Adventures.cards(
        "Amulet",
        "Caravan Guard",
        "Coin of the Realm",
        "Dungeon",
        "Gear",
        "Guide",
        "Page",
        "Peasant",
        "Ratcatcher",
        "Raze",
    ),
    Alchemy.cards("Herbalist"),
    Allies.cards(
        "Bauble",
        "Sycophant",
        "Townsfolk: Town Crier + Blacksmith + Miller + Elder",
        "Augers: Herb Gatherer + Acolyte + Sorceress + Sibyl",
        "Clashes: Battle Plan + Archer + Warlord + Territory",
        "Forts: Tent + Garrison + Hill Fort + Stronghold",
        "Merchant Camp",
        "Importer",
        "Odysseys: Old Map, Voyage, Sunken Treasure, Distant Shore",
        "Sentinel",
        "Underling",
        "Wizards: Student, Conjurer, Sorcerer, Lich",
    ),
    Antiquities.cards(
        "Discovery",
        "Gamepiece",
        "Grave Watcher",
        "Inscription",
        "Inspector",
        "Profiteer",
        "Shipwreck",
        "Tomb Raider",
        "Miner",
    ),
    Base.cards(
        "Cellar",
        "Chapel",
        "Harbinger",
        "Merchant",
        "Moat",
        "Vassal",
        "Village",
        "Workshop",
    ),
    Cornucopia.cards("Fortune Teller", "Hamlet", "Menagerie"),
    DarkAges.cards(
        "Beggar",
        "Forager",
        "Hermit",
        "Market Square",
        "Sage",
        "Squire",
        "Storeroom",
        "Urchin",
        "Vagrant",
    ),
    Empires.cards(
        "Castles",
        "Catapult/Rocks",
        "Chariot Race",
        "Encampment/Plunder",
        "Enchantress",
        "Farmers' Market",
        "Gladiator/Fortune",
        "Patrician/Emporium",
        "Settlers/Bustling Village",
    ),
    Guilds.cards("Candlestick Maker", "Doctor", "Masterpiece", "Stonemason"),
    Hinterlands.cards(
        "Crossroads", "Develop", "Duchess", "Fool's Gold", "Oasis", "Scheme", "Tunnel"
    ),
    Intrigue.cards(
        "Courtyard",
        "Great Hall",
        "Lurker",
        "Masquerade",
        "Pawn",
        "Secret Chamber",
        "Shanty Town",
        "Steward",
        "Swindler",
        "Wishing Well",
    ),
    Menagerie.cards(
        "Black Cat",
        "Camel Train",
        "Goatherd",
        "Scrap",
        "Sheepdog",
        "Sleigh",
        "Snowy Village",
        "Stockpile",
        "Supplies",
    ),
    Nocturne.cards(
        "Changeling",
        "Druid",
        "Faithful Hound",
        "Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)",
        "Ghost Town",
        "Guardian",
        "Leprechaun",
        "Monastery",
        "Night Watchman",
        "Pixie + Goat (Heirloom)",
        "Secret Cave + Magic Lamp (Heirloom)",
        "Tracker + Pouch (Heirloom)",
    ),
    Prosperity.cards("Loan", "Trade Route", "Watchtower"),
    Renaissance.cards(
        "Acting Troupe",
        "Border Guard",
        "Cargo Ship",
        "Ducat",
        "Experiment",
        "Improve",
        "Lackeys",
    ),
    Seaside.cards(
        "Ambassador",
        "Embargo",
        "Fishing Village",
        "Haven",
        "Lighthouse",
        "Lookout",
        "Native Village",
        "Pearl Diver",
        "Smugglers",
        "Warehouse",
    ),
)


def RandomizeDominion(setNames=None, options=None):
    # Make full list + Events + Landmarks to determine landmarks
    sets = set()
    if setNames is None:
        sets.update(AllSets.values())
    else:
        for setName in setNames:
            if setName in AllSets:
                sets.add(AllSets[setName])

    if options:
        if Base in sets:
            if options.get("base-first-edition"):
                Base.AddCards(Base.firstEdition)

            if not options.get("base-second-edition", True):
                Base.RemoveCards(Base.secondEdition)

        if Intrigue in sets:
            if options.get("intrigue-first-edition"):
                Intrigue.AddCards(Intrigue.firstEdition)

            if not options.get("intrigue-second-edition", True):
                Intrigue.RemoveCards(Intrigue.secondEdition)

    completeSet = set().union(*(cardSet.cards for cardSet in sets))
    # Allies are not randomized
    completeSet = completeSet - AllyCards
    landscapeSet = set()

    if completeSet & LandscapeCards:
        # Handle sets that include landscape cards
        kingdomSet = completeSet - LandscapeCards

        resultSet = set()
        waySet = set()
        counter = 0
        while not landscapeSet and counter < 3:
            # Shuffle all cards
            cards = iter(random.sample(completeSet, len(completeSet)))

            # Categorize cards from the shuffled pile
            while len(resultSet) < 10:
                card = next(cards)
                if card.types & {Way}:
                    waySet.add(card)
                elif card.types & {Event, Landmark, Project}:
                    landscapeSet.add(card)
                else:
                    resultSet.add(card)

            counter += 1

        # Get final list of landscape cards
        if options and options.get("limit-landscapes"):
            landscapeList = random.sample(waySet, len(waySet))[:1]
            landscapeList.extend(
                random.sample(landscapeSet, len(landscapeSet))[: 2 - len(landscapeList)]
            )
        else:
            landscapeList = random.sample(landscapeSet, len(landscapeSet))[:3]
            landscapeList.extend(random.sample(waySet, len(waySet))[:1])
    else:
        kingdomSet = completeSet
        landscapeList = []

        resultSet = set(random.sample(kingdomSet, 10))

    # Enforce Alchemy rule
    if (options or {}).get("enforce-alchemy-rule", True):
        alchemyCards = Alchemy.cards & resultSet
        if len(alchemyCards) == 1:
            # If there's only 1 Alchemy card, remove Alchemy from the options
            # and draw an addtional Kingdom card
            resultSet -= alchemyCards
            resultSet.update(random.sample(kingdomSet - resultSet, 1))
        elif len(alchemyCards) == 2:
            # If there are only 2 Alchemy cards, pull an additional Alchemy
            # card and randomly remove one non-Alchemy card
            alchemyCards.update(random.sample(Alchemy.cards - alchemyCards, 1))
            resultSet = alchemyCards.union(random.sample(resultSet, 7))
        # If there are 3 or more Alchemy cards, let it lie.

    # Young Witch support
    includeBane = resultSet & Cornucopia.cards("Young Witch")
    if includeBane:
        eligibleBanes = (kingdomSet & BaneCards) - resultSet
        if not eligibleBanes:
            # All eligible Bane cards are already part of the randomized set!
            # Add a new card to the set and pull a Bane from the randomized
            # cards.
            resultSet.update(random.sample(kingdomSet - resultSet, 1))
            baneCard = random.sample(resultSet & BaneCards, 1)[0]
        else:
            baneCard = random.sample(eligibleBanes, 1)[0]
            resultSet.add(baneCard)

    # Get card for Way of the Mouse. This uses similar rules to Young Witch, so
    # select a card from the Bane Cards. The card chosen for Way of the Mouse
    # should not be used when determining most additional card rules.
    includeMouse = Menagerie.cards("Way of the Mouse").intersection(landscapeList)
    mouseSet = set()
    if includeMouse:
        eligibleMice = (kingdomSet & BaneCards) - resultSet
        if not eligibleMice:
            # All eligible Mouse cards are already part of the randomized set!
            # (This is nearly impossible.) Get a Mouse from the randomized
            # cards, add a new card to the set, and remove the mouse from the
            # set.
            eligibleMice = resultSet & BaneCards
            if includeBane:
                eligibleMice.remove(baneCard)

            mouseCard = random.sample(eligibleMice, 1)[0]
            resultSet.update(random.sample(kingdomSet - resultSet, 1))
            resultSet.remove(mouseCard)
        else:
            mouseCard = random.sample(eligibleMice, 1)[0]
        mouseSet.add(mouseCard)

    fullResults = resultSet.union(landscapeList)

    # Check for Colonies and Platinums
    includeColoniesAndPlatinum = Prosperity in sets and PlatinumLove.intersection(
        random.sample(fullResults, 2)
    )

    # Check for Potions
    includePotions = Alchemy.potionCards & resultSet

    # Check for Prizes
    includePrizes = Cornucopia.cards("Tournament") & resultSet

    # Check for Shelters
    includeShelters = DarkAges in sets and ShelterLove.intersection(
        random.sample(fullResults, 2)
    )
    # Check for Ruins
    includeRuins = LooterCards & resultSet
    # Check for Madman
    includeMadman = DarkAges.cards("Hermit") & resultSet
    # Check for Mercenary
    includeMercenary = DarkAges.cards("Urchin") & resultSet
    # Check for Spoils
    includeSpoils = SpoilsCards & resultSet

    # Check for special Nocturne cards
    includeGhost = resultSet & Nocturne.cards(
        "Cemetary + Haunted Mirror (Heirloom)", "Exorcist"
    )

    includeBoons = BoonCards & (resultSet | mouseSet)

    includeHexes = HexCards & (resultSet | mouseSet)

    includeWisp = includeBoons or (Nocturne.cards("Exorcist") & resultSet)

    includeBat = Nocturne.cards("Vampire") & resultSet

    includeImp = resultSet & Nocturne.cards("Devil's Workshop", "Exorcist", "Tormentor")

    includeWish = resultSet & Nocturne.cards(
        "Leprechaun", "Secret Cave + Magic Lamp (Heirloom)"
    )

    # Check for Horses
    includeHorse = HorseCards & (fullResults | mouseSet)

    # Check for Liaisons (for a random Ally Card)
    includeAlly = LiaisonCards & (fullResults | mouseSet)

    # Check for Boulder traps
    includeBoulderTraps = Antiquities in sets and TrapLove.intersection(
        random.sample(fullResults, 1)
    )

    # Create final list
    additionalCards = set()

    if includePotions:
        additionalCards.add("Alchemy: Potions")
    if includeShelters:
        additionalCards.add("Dark Ages: Shelters")
    if includeRuins:
        additionalCards.add("Dark Ages: Ruins")
    if includeColoniesAndPlatinum:
        additionalCards.update(("Prosperity: Colony", "Prosperity: Platinum"))
    if includeBoulderTraps:
        # Technically this is not a landscape card, but it is set up
        # differently than other Kingdom cards
        landscapeList.append("(Antiquities Trap): Boulder Traps")
    if includeMadman:
        additionalCards.add("Dark Ages: Madman")
    if includeMercenary:
        additionalCards.add("Dark Ages: Mercenary")
    if includeSpoils:
        additionalCards.add("Dark Ages: Spoils")
    if includePrizes:
        additionalCards.update(
            (
                "Cornucopia: Bag of Gold",
                "Cornucopia: Diadem",
                "Cornucopia: Followers",
                "Cornucopia: Princess",
                "Cornucopia: Trusty Steed",
            )
        )
    if includeGhost:
        additionalCards.add("Nocturne: Ghost")
    if includeBoons:
        landscapeList.append("(Nocturne: Boons Deck)")
    if includeHexes:
        landscapeList.append("(Nocturne: Hexes Deck)")
    if includeWisp:
        additionalCards.add("Nocturne: Will-o'-wisp")
    if includeBat:
        additionalCards.add("Nocturne: Bat")
    if includeImp:
        additionalCards.add("Nocturne: Imp")
    if includeWish:
        additionalCards.add("Nocturne: Wish")
    if includeHorse:
        additionalCards.add("Menagerie: Horse")

    # Create final card list
    if includeBane:
        # Append Bane Card to end of list
        resultSet.remove(baneCard)
        finalResult = sorted(resultSet | additionalCards)
        finalResult.append("Bane is {}".format(baneCard))
    else:
        finalResult = sorted(resultSet | additionalCards)

    # Add non-kingdom cards
    if includeAlly:
        ally = random.sample(AllyCards, 1)[0]
        finalResult.append(ally)
    finalResult.extend(sorted(landscapeList))
    if includeMouse:
        finalResult.append("Mouse is {}".format(mouseCard))

    return [str(card) for card in finalResult]


if __name__ == "__main__":
    print("\n".join(RandomizeDominion()))
