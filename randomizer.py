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
    def __init__(self, name, types=None, cardSet=None, extras=None):
        self.name = name
        self.set = cardSet

        if isinstance(types, set):
            self.types = types
        elif types is None:
            self.types = set()
        else:
            self.types = set(types)

        if isinstance(extras, set):
            self.extras = extras
        elif extras is None:
            self.extras = set()
        else:
            self.extras = set(extras)

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
        elif Trait in self.types:
            formatStr = "({} Trait): {}"
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
        self._actions = None
        self._allyCards = None
        self._traits = None

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
    def actions(self):
        if self._actions is None:
            self._actions = CardList(
                card for card in self._cards if card.types & {Action}
            )
        return self._actions

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
    def traits(self):
        if self._traits is None:
            self._traits = CardList(
                card for card in self._cards if card.types & {Trait}
            )
        return self._traits

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
Trait = CardType("Trait")
Action = CardType("Action")

# Define sets
Base = Set("Base")
Base.AddCards(
    [
        "Gardens",
        {"name": "Artisan", "types": {Action}},
        {"name": "Cellar", "types": {Action}},
        {"name": "Chapel", "types": {Action}},
        {"name": "Moat", "types": {Action}},
        {"name": "Harbinger", "types": {Action}},
        {"name": "Merchant", "types": {Action}},
        {"name": "Village", "types": {Action}},
        {"name": "Workshop", "types": {Action}},
        {"name": "Vassal", "types": {Action}},
        {"name": "Bureaucrat", "types": {Action}},
        {"name": "Militia", "types": {Action}},
        {"name": "Moneylender", "types": {Action}},
        {"name": "Poacher", "types": {Action}},
        {"name": "Remodel", "types": {Action}},
        {"name": "Smithy", "types": {Action}},
        {"name": "Throne Room", "types": {Action}},
        {"name": "Bandit", "types": {Action}},
        {"name": "Council Room", "types": {Action}},
        {"name": "Festival", "types": {Action}},
        {"name": "Laboratory", "types": {Action}},
        {"name": "Library", "types": {Action}},
        {"name": "Market", "types": {Action}},
        {"name": "Mine", "types": {Action}},
        {"name": "Sentry", "types": {Action}},
        {"name": "Witch", "types": {Action}},
    ]
)
Base.firstEdition = [
    {"name": "Adventurer", "types": {Action}},
    {"name": "Chancellor", "types": {Action}},
    {"name": "Feast", "types": {Action}},
    {"name": "Spy", "types": {Action}},
    {"name": "Thief", "types": {Action}},
    {"name": "Woodcutter", "types": {Action}},
]
Base.secondEdition = Base.cards(
    "Artisan",
    "Bandit",
    "Harbinger",
    "Merchant",
    "Poacher",
    "Sentry",
    "Vassal",
)

Intrigue = Set("Intrigue")
Intrigue.AddCards(
    [
        "Harem",
        {"name": "Courtyard", "types": {Action}},
        {"name": "Lurker", "types": {Action}},
        {"name": "Pawn", "types": {Action}},
        {"name": "Masquerade", "types": {Action}},
        {"name": "Shanty Town", "types": {Action}},
        {"name": "Steward", "types": {Action}},
        {"name": "Swindler", "types": {Action}},
        {"name": "Wishing Well", "types": {Action}},
        {"name": "Baron", "types": {Action}},
        {"name": "Bridge", "types": {Action}},
        {"name": "Conspirator", "types": {Action}},
        {"name": "Diplomat", "types": {Action}},
        {"name": "Ironworks", "types": {Action}},
        {"name": "Mill", "types": {Action}},
        {"name": "Mining Village", "types": {Action}},
        {"name": "Secret Passage", "types": {Action}},
        {"name": "Courtier", "types": {Action}},
        {"name": "Duke", "types": {Action}},
        {"name": "Minion", "types": {Action}},
        {"name": "Patrol", "types": {Action}},
        {"name": "Replace", "types": {Action}},
        {"name": "Torturer", "types": {Action}},
        {"name": "Trading Post", "types": {Action}},
        {"name": "Upgrade", "types": {Action}},
        {"name": "Nobles", "types": {Action}},
    ]
)
Intrigue.firstEdition = [
    {"name": "Coppersmith", "types": {Action}},
    {"name": "Great Hall", "types": {Action}},
    {"name": "Saboteur", "types": {Action}},
    {"name": "Scout", "types": {Action}},
    {"name": "Secret Chamber", "types": {Action}},
    {"name": "Tribute", "types": {Action}},
]
Intrigue.secondEdition = Intrigue.cards(
    "Courtier", "Diplomat", "Lurker", "Mill", "Patrol", "Replace", "Secret Passage"
)

Seaside = Set("Seaside")
Seaside.AddCards(
    [
        "Astrolabe",
        {"name": "Bazaar", "types": {Action}},
        {"name": "Blockade", "types": {Action}},
        {"name": "Caravan", "types": {Action}},
        {"name": "Corsair", "types": {Action}},
        {"name": "Cutpurse", "types": {Action}},
        {"name": "Fishing Village", "types": {Action}},
        {"name": "Haven", "types": {Action}},
        {"name": "Island", "types": {Action}, "extras": {"Island Mat"}},
        {"name": "Lighthouse", "types": {Action}},
        {"name": "Lookout", "types": {Action}},
        {"name": "Merchant Ship", "types": {Action}},
        {"name": "Monkey", "types": {Action}},
        {"name": "Native Village", "types": {Action}, "extras": {"Native Village Mat"}},
        {"name": "Outpost", "types": {Action}},
        {"name": "Pirate", "types": {Action}},
        {"name": "Sailor", "types": {Action}},
        {"name": "Salvager", "types": {Action}},
        {"name": "Sea Chart", "types": {Action}},
        {"name": "Sea Witch", "types": {Action}},
        {"name": "Smugglers", "types": {Action}},
        {"name": "Tactician", "types": {Action}},
        {"name": "Tide Pools", "types": {Action}},
        {"name": "Treasure Map", "types": {Action}},
        {"name": "Treasury", "types": {Action}},
        {"name": "Warehouse", "types": {Action}},
        {"name": "Wharf", "types": {Action}},
    ]
)
Seaside.firstEdition = [
    {"name": "Embargo", "types": {Action}, "extras": {"Embargo Tokens"}},
    {"name": "Pearl Diver", "types": {Action}},
    {"name": "Ambassador", "types": {Action}},
    {"name": "Navigator", "types": {Action}},
    {
        "name": "Pirate Ship",
        "types": {Action},
        "extras": {"Coin Tokens", "Pirate Ship Mat"},
    },
    {"name": "Sea Hag", "types": {Action}},
    {"name": "Explorer", "types": {Action}},
    {"name": "Ghost Ship", "types": {Action}},
]
Seaside.secondEdition = Seaside.cards(
    "Astrolabe",
    "Blockade",
    "Corsair",
    "Monkey",
    "Pirate",
    "Sailor",
    "Sea Chart",
    "Sea Witch",
    "Tide Pools",
)

Alchemy = Set("Alchemy")
Alchemy.AddCards(
    [
        {"name": "Herbalist", "types": {Action}},
        {"name": "Apprentice", "types": {Action}},
        {"name": "Transmute", "types": {Action, Potion}},
        {"name": "Vineyard", "types": {Potion}},
        {"name": "Apothecary", "types": {Action, Potion}},
        {"name": "Scrying Pool", "types": {Action, Potion}},
        {"name": "University", "types": {Action, Potion}},
        {"name": "Alchemist", "types": {Action, Potion}},
        {"name": "Familiar", "types": {Action, Potion}},
        {"name": "Philosopher's Stone", "types": {Potion}},
        {"name": "Golem", "types": {Action, Potion}},
        {"name": "Possession", "types": {Action, Potion}},
    ]
)

Prosperity = Set("Prosperity")
Prosperity.AddCards(
    [
        "Anvil",
        "Bank",
        {"name": "Collection", "extras": {"Victory Tokens"}},
        "Hoard",
        {"name": "Investment", "extras": {"Victory Tokens"}},
        "Quarry",
        "Tiara",
        "War Chest",
        {"name": "Bishop", "types": {Action}, "extras": {"Victory Tokens"}},
        {"name": "Charlatan", "types": {Action}},
        {"name": "City", "types": {Action}},
        {"name": "Clerk", "types": {Action}},
        {"name": "Expand", "types": {Action}},
        {"name": "Forge", "types": {Action}},
        {"name": "Grand Market", "types": {Action}},
        {"name": "King's Court", "types": {Action}},
        {"name": "Magnate", "types": {Action}},
        {"name": "Mint", "types": {Action}},
        {"name": "Monument", "types": {Action}, "extras": {"Victory Tokens"}},
        {"name": "Peddler", "types": {Action}},
        {"name": "Rabble", "types": {Action}},
        {"name": "Vault", "types": {Action}},
        {"name": "Watchtower", "types": {Action}},
        {"name": "Worker's Village", "types": {Action}},
    ]
)
Prosperity.firstEdition = [
    "Contraband",
    "Loan",
    "Royal Seal",
    "Talisman",
    "Venture",
    {"name": "Counting House", "types": {Action}},
    {"name": "Goons", "types": {Action}, "extras": {"Victory Tokens"}},
    {"name": "Mountebank", "types": {Action}},
    {
        "name": "Trade Route",
        "types": {Action},
        "extras": {"Coin Tokens", "Trade Route Mat"},
    },
]
Prosperity.secondEdition = Prosperity.cards(
    "Anvil",
    "Charlatan",
    "Clerk",
    "Collection",
    "Crystal Ball",
    "Investment",
    "Magnate",
    "Tiara",
    "War Chest",
)


Cornucopia = Set("Cornucopia")
Cornucopia.AddCards(
    [
        "Fairgrounds",
        "Horn of Plenty",
        {"name": "Hamlet", "types": {Action}},
        {"name": "Fortune Teller", "types": {Action}},
        {"name": "Menagerie", "types": {Action}},
        {"name": "Farming Village", "types": {Action}},
        {"name": "Horse Traders", "types": {Action}},
        {"name": "Remake", "types": {Action}},
        {"name": "Tournament", "types": {Action}},
        {"name": "Young Witch", "types": {Action}},
        {"name": "Harvest", "types": {Action}},
        {"name": "Hunting Party", "types": {Action}},
        {"name": "Jester", "types": {Action}},
    ]
)

Hinterlands = Set("Hinterlands")
Hinterlands.AddCards(
    [
        "Cauldron",
        "Farmland",
        "Fool's Gold",
        "Tunnel",
        {"name": "Berserker", "types": {Action}},
        {"name": "Border Village", "types": {Action}},
        {"name": "Cartographer", "types": {Action}},
        {"name": "Crossroads", "types": {Action}},
        {"name": "Develop", "types": {Action}},
        {"name": "Guard Dog", "types": {Action}},
        {"name": "Haggler", "types": {Action}},
        {"name": "Highway", "types": {Action}},
        {"name": "Inn", "types": {Action}},
        {"name": "Jack of All Trades", "types": {Action}},
        {"name": "Margrave", "types": {Action}},
        {"name": "Nomads", "types": {Action}},
        {"name": "Oasis", "types": {Action}},
        {"name": "Scheme", "types": {Action}},
        {"name": "Souk", "types": {Action}},
        {"name": "Spice Merchant", "types": {Action}},
        {"name": "Stables", "types": {Action}},
        {"name": "Trader", "types": {Action}},
        {"name": "Trail", "types": {Action}},
        {"name": "Weaver", "types": {Action}},
        {"name": "Wheelwright", "types": {Action}},
        {"name": "Witch's Hut", "types": {Action}},
    ]
)
Hinterlands.firstEdition = [
    "Cache",
    "Ill-gotten Gains",
    "Silk Road",
    {"name": "Duchess", "types": {Action}},
    {"name": "Embassy", "types": {Action}},
    {"name": "Mandarin", "types": {Action}},
    {"name": "Noble Brigand", "types": {Action}},
    {"name": "Nomad Camp", "types": {Action}},
    {"name": "Oracle", "types": {Action}},
]
Hinterlands.secondEdition = Hinterlands.cards(
    "Berserker",
    "Cauldron",
    "Guard Dog",
    "Nomads",
    "Souk",
    "Trail",
    "Weaver",
    "Wheelwright",
    "Witch's Hut",
)

DarkAges = Set("Dark Ages")
DarkAges.AddCards(
    [
        "Counterfeit",
        "Feodum",
        {"name": "Poor House", "types": {Action}},
        {"name": "Beggar", "types": {Action}},
        {"name": "Squire", "types": {Action}},
        {"name": "Vagrant", "types": {Action}},
        {"name": "Forager", "types": {Action}},
        {"name": "Hermit", "types": {Action}},
        {"name": "Market Square", "types": {Action}},
        {"name": "Sage", "types": {Action}},
        {"name": "Storeroom", "types": {Action}},
        {"name": "Urchin", "types": {Action}},
        {"name": "Armory", "types": {Action}},
        {"name": "Death Cart", "types": {Action}},
        {"name": "Fortress", "types": {Action}},
        {"name": "Ironmonger", "types": {Action}},
        {"name": "Marauder", "types": {Action}},
        {"name": "Procession", "types": {Action}},
        {"name": "Rats", "types": {Action}},
        {"name": "Scavenger", "types": {Action}},
        {"name": "Wandering Minstrel", "types": {Action}},
        {"name": "Band of Misfits", "types": {Action}},
        {"name": "Bandit Camp", "types": {Action}},
        {"name": "Catacombs", "types": {Action}},
        {"name": "Count", "types": {Action}},
        {"name": "Cultist", "types": {Action}},
        {"name": "Graverobber", "types": {Action}},
        {"name": "Junk Dealer", "types": {Action}},
        {"name": "Knights", "types": {Action}},
        {"name": "Mystic", "types": {Action}},
        {"name": "Pillage", "types": {Action}},
        {"name": "Rebuild", "types": {Action}},
        {"name": "Rogue", "types": {Action}},
        {"name": "Altar", "types": {Action}},
        {"name": "Hunting Grounds", "types": {Action}},
    ]
)

Guilds = Set("Guilds")
Guilds.AddCards(
    [
        "Masterpiece",
        {
            "name": "Candlestick Maker",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers Mat"},
        },
        {"name": "Stonemason", "types": {Action}},
        {"name": "Doctor", "types": {Action}},
        {"name": "Advisor", "types": {Action}},
        {"name": "Plaza", "types": {Action}, "extras": {"Coin Tokens", "Coffers Mat"}},
        {"name": "Taxman", "types": {Action}},
        {"name": "Herald", "types": {Action}},
        {"name": "Baker", "types": {Action}, "extras": {"Coin Tokens", "Coffers Mat"}},
        {
            "name": "Butcher",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers Mat"},
        },
        {"name": "Journeyman", "types": {Action}},
        {
            "name": "Merchant Guild",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers Mat"},
        },
        {"name": "Soothsayer", "types": {Action}},
    ]
)

Adventures = Set("Adventures")
Adventures.AddCards(
    [
        {"name": "Coin of the Realm", "extras": {"Tavern Mat"}},
        {"name": "Distant Lands", "extras": {"Tavern Mat"}},
        {"name": "Relic", "extras": {"Adventure Tokens"}},
        "Treasure Trove",
        {"name": "Page", "types": {Action}},
        {
            "name": "Peasant",
            "types": {Action},
            "extras": {"Tavern Mat", "Adventure Tokens"},
        },
        {"name": "Ratcatcher", "types": {Action}, "extras": {"Tavern Mat"}},
        {"name": "Raze", "types": {Action}},
        {"name": "Amulet", "types": {Action}},
        {"name": "Caravan Guard", "types": {Action}},
        {"name": "Dungeon", "types": {Action}},
        {"name": "Gear", "types": {Action}},
        {"name": "Guide", "types": {Action}, "extras": {"Tavern Mat"}},
        {"name": "Duplicate", "types": {Action}, "extras": {"Tavern Mat"}},
        {"name": "Magpie", "types": {Action}},
        {"name": "Messenger", "types": {Action}},
        {"name": "Miser", "types": {Action}, "extras": {"Tavern Mat"}},
        {"name": "Port", "types": {Action}},
        {"name": "Ranger", "types": {Action}, "extras": {"Adventure Tokens"}},
        {"name": "Transmogrify", "types": {Action}, "extras": {"Tavern Mat"}},
        {"name": "Artificer", "types": {Action}},
        {"name": "Bridge Troll", "types": {Action}, "extras": {"Adventure Tokens"}},
        {"name": "Giant", "types": {Action}, "extras": {"Adventure Tokens"}},
        {"name": "Haunted Woods", "types": {Action}},
        {"name": "Lost City", "types": {Action}},
        {"name": "Royal Carriage", "types": {Action}, "extras": {"Tavern Mat"}},
        {"name": "Storyteller", "types": {Action}},
        {"name": "Swamp Hag", "types": {Action}},
        {"name": "Wine Merchant", "types": {Action}, "extras": {"Tavern Mat"}},
        {"name": "Hireling", "types": {Action}},
        {"name": "Alms", "types": {Event}},
        {"name": "Borrow", "types": {Event}, "extras": {"Adventure Tokens"}},
        {"name": "Quest", "types": {Event}},
        {"name": "Save", "types": {Event}},
        {"name": "Scouting Party", "types": {Event}},
        {"name": "Travelling Fair", "types": {Event}},
        {"name": "Bonfire", "types": {Event}},
        {"name": "Expedition", "types": {Event}},
        {"name": "Ferry", "types": {Event}, "extras": {"Adventure Tokens"}},
        {"name": "Plan", "types": {Event}, "extras": {"Adventure Tokens"}},
        {"name": "Mission", "types": {Event}},
        {"name": "Pilgrimage", "types": {Event}, "extras": {"Adventure Tokens"}},
        {"name": "Ball", "types": {Event}, "extras": {"Adventure Tokens"}},
        {"name": "Raid", "types": {Event}, "extras": {"Adventure Tokens"}},
        {"name": "Seaway", "types": {Event}, "extras": {"Adventure Tokens"}},
        {"name": "Lost Arts", "types": {Event}, "extras": {"Adventure Tokens"}},
        {"name": "Training", "types": {Event}, "extras": {"Adventure Tokens"}},
        {"name": "Inheritance", "types": {Event}, "extras": {"Adventure Tokens"}},
        {"name": "Pathfinding", "types": {Event}, "extras": {"Adventure Tokens"}},
    ]
)

Empires = Set("Empires")
Empires.AddCards(
    [
        {"name": "Castles", "extras": {"Victory Tokens"}},
        {"name": "Capital", "extras": {"Debt Tokens"}},
        "Charm",
        {"name": "Engineer", "types": {Action}, "extras": {"Debt Tokens"}},
        {"name": "City Quarter", "types": {Action}, "extras": {"Debt Tokens"}},
        {"name": "Overlord", "types": {Action}, "extras": {"Debt Tokens"}},
        {"name": "Royal Blacksmith", "types": {Action}, "extras": {"Debt Tokens"}},
        {"name": "Encampment/Plunder", "types": {Action}, "extras": {"Victory Tokens"}},
        {"name": "Patrician/Emporium", "types": {Action}, "extras": {"Victory Tokens"}},
        {"name": "Settlers/Bustling Village", "types": {Action}},
        {"name": "Catapult/Rocks", "types": {Action}},
        {"name": "Chariot Race", "types": {Action}, "extras": {"Victory Tokens"}},
        {"name": "Enchantress", "types": {Action}},
        {"name": "Farmers' Market", "types": {Action}, "extras": {"Victory Tokens"}},
        {"name": "Gladiator/Fortune", "types": {Action}, "extras": {"Debt Tokens"}},
        {"name": "Sacrifice", "types": {Action}, "extras": {"Victory Tokens"}},
        {"name": "Temple", "types": {Action}, "extras": {"Victory Tokens"}},
        {"name": "Villa", "types": {Action}},
        {"name": "Archive", "types": {Action}},
        {"name": "Crown", "types": {Action}},
        {"name": "Forum", "types": {Action}},
        {"name": "Groundskeeper", "types": {Action}, "extras": {"Victory Tokens"}},
        {"name": "Legionary", "types": {Action}},
        {"name": "Wild Hunt", "types": {Action}, "extras": {"Victory Tokens"}},
        {"name": "Advance", "types": {Event}},
        {"name": "Annex", "types": {Event}, "extras": {"Debt Tokens"}},
        {"name": "Banquet", "types": {Event}},
        {"name": "Conquest", "types": {Event}, "extras": {"Victory Tokens"}},
        {"name": "Delve", "types": {Event}},
        {"name": "Dominate", "types": {Event}, "extras": {"Victory Tokens"}},
        {"name": "Donate", "types": {Event}, "extras": {"Debt Tokens"}},
        {"name": "Salt the Earth", "types": {Event}, "extras": {"Victory Tokens"}},
        {"name": "Ritual", "types": {Event}, "extras": {"Victory Tokens"}},
        {"name": "Tax", "types": {Event}, "extras": {"Debt Tokens"}},
        {"name": "Trade", "types": {Event}},
        {
            "name": "Triumph",
            "types": {Event},
            "extras": {"Debt Tokens", "Victory Tokens"},
        },
        {
            "name": "Wedding",
            "types": {Event},
            "extras": {"Debt Tokens", "Victory Tokens"},
        },
        {"name": "Windfall", "types": {Event}},
        {"name": "Aqueduct", "types": {Landmark}, "extras": {"Victory Tokens"}},
        {"name": "Arena", "types": {Landmark}, "extras": {"Victory Tokens"}},
        {"name": "Bandit Fort", "types": {Landmark}},
        {"name": "Basilica", "types": {Landmark}, "extras": {"Victory Tokens"}},
        {"name": "Baths", "types": {Landmark}, "extras": {"Victory Tokens"}},
        {"name": "Battlefield", "types": {Landmark}, "extras": {"Victory Tokens"}},
        {"name": "Colonnade", "types": {Landmark}, "extras": {"Victory Tokens"}},
        {"name": "Defiled Shrine", "types": {Landmark}, "extras": {"Victory Tokens"}},
        {"name": "Fountain", "types": {Landmark}},
        {"name": "Keep", "types": {Landmark}},
        {"name": "Labyrinth", "types": {Landmark}, "extras": {"Victory Tokens"}},
        {
            "name": "Mountain Pass",
            "types": {Landmark},
            "extras": {"Debt Tokens", "Victory Tokens"},
        },
        {"name": "Museum", "types": {Landmark}},
        {"name": "Obelisk", "types": {Landmark}},
        {"name": "Orchard", "types": {Landmark}},
        {"name": "Palace", "types": {Landmark}},
        {"name": "Tomb", "types": {Landmark}, "extras": {"Victory Tokens"}},
        {"name": "Tower", "types": {Landmark}},
        {"name": "Triumphal Arch", "types": {Landmark}},
        {"name": "Wall", "types": {Landmark}},
        {"name": "Wolf Den", "types": {Landmark}},
    ]
)

Nocturne = Set("Nocturne")
Nocturne.AddCards(
    [
        "Cemetary + Haunted Mirror (Heirloom)",
        "Changeling",
        "Cobbler",
        "Crypt",
        "Den of Sin",
        "Devil's Workshop",
        "Exorcist",
        "Guardian",
        "Ghost Town",
        "Idol",
        "Monastery",
        "Night Watchman",
        "Raider",
        "Vampire",
        {"name": "Bard", "types": {Action}},
        {"name": "Blessed Village", "types": {Action}},
        {"name": "Conclave", "types": {Action}},
        {"name": "Cursed Village", "types": {Action}},
        {"name": "Druid", "types": {Action}},
        {"name": "Faithful Hound", "types": {Action}},
        {
            "name": "Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)",
            "types": {Action},
        },
        {"name": "Leprechaun", "types": {Action}},
        {"name": "Necromancer + Zombies", "types": {Action}},
        {"name": "Pixie + Goat (Heirloom)", "types": {Action}},
        {"name": "Pooka + Cursed Gold (Heirloom)", "types": {Action}},
        {"name": "Sacred Grove", "types": {Action}},
        {"name": "Secret Cave + Magic Lamp (Heirloom)", "types": {Action}},
        {"name": "Shepherd + Pasture (Heirloom)", "types": {Action}},
        {"name": "Skulk", "types": {Action}},
        {"name": "Tormentor", "types": {Action}},
        {"name": "Tracker + Pouch (Heirloom)", "types": {Action}},
        {"name": "Tragic Hero", "types": {Action}},
        {"name": "Werewolf", "types": {Action}},
    ]
)

Renaissance = Set("Renaissance")
Renaissance.AddCards(
    [
        {"name": "Ducat", "extras": {"Coin Tokens", "Coffers/Villagers Mat"}},
        "Scepter",
        {"name": "Spices", "extras": {"Coin Tokens", "Coffers/Villagers Mat"}},
        {"name": "Border Guard", "types": {Action}},
        {
            "name": "Lackeys",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat"},
        },
        {
            "name": "Acting Troupe",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat"},
        },
        {"name": "Cargo Ship", "types": {Action}},
        {"name": "Experiment", "types": {Action}},
        {"name": "Improve", "types": {Action}},
        {"name": "Flag Bearer", "types": {Action}},
        {"name": "Hideout", "types": {Action}},
        {"name": "Inventor", "types": {Action}},
        {"name": "Mountain Village", "types": {Action}},
        {
            "name": "Patron",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat"},
        },
        {"name": "Priest", "types": {Action}},
        {"name": "Research", "types": {Action}},
        {
            "name": "Silk Merchant",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat"},
        },
        {"name": "Old Witch", "types": {Action}},
        {
            "name": "Recruiter",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat"},
        },
        {"name": "Scholar", "types": {Action}},
        {
            "name": "Sculptor",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat"},
        },
        {"name": "Seer", "types": {Action}},
        {
            "name": "Swashbuckler",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat"},
        },
        {"name": "Treasurer", "types": {Action}},
        {
            "name": "Villain",
            "types": {Action},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat"},
        },
        {"name": "Cathedral", "types": {Project}, "extras": {"Wooden Cubes"}},
        {"name": "City Gate", "types": {Project}, "extras": {"Wooden Cubes"}},
        {
            "name": "Pageant",
            "types": {Project},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat", "Wooden Cubes"},
        },
        {"name": "Sewers", "types": {Project}, "extras": {"Wooden Cubes"}},
        {"name": "Star Chart", "types": {Project}, "extras": {"Wooden Cubes"}},
        {
            "name": "Exploration",
            "types": {Project},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat", "Wooden Cubes"},
        },
        {"name": "Fair", "types": {Project}, "extras": {"Wooden Cubes"}},
        {"name": "Silos", "types": {Project}, "extras": {"Wooden Cubes"}},
        {
            "name": "Sinister Plot",
            "types": {Project},
            "extras": {"Coin Tokens", "Wooden Cubes"},
        },
        {
            "name": "Academy",
            "types": {Project},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat", "Wooden Cubes"},
        },
        {"name": "Capitalism", "types": {Project}, "extras": {"Wooden Cubes"}},
        {"name": "Fleet", "types": {Project}, "extras": {"Wooden Cubes"}},
        {
            "name": "Guildhall",
            "types": {Project},
            "extras": {"Coin Tokens", "Coffers/Villagers Mat", "Wooden Cubes"},
        },
        {"name": "Piazza", "types": {Project}, "extras": {"Wooden Cubes"}},
        {"name": "Road Network", "types": {Project}, "extras": {"Wooden Cubes"}},
        {"name": "Barracks", "types": {Project}, "extras": {"Wooden Cubes"}},
        {"name": "Crop Rotation", "types": {Project}, "extras": {"Wooden Cubes"}},
        {"name": "Innovation", "types": {Project}, "extras": {"Wooden Cubes"}},
        {"name": "Canal", "types": {Project}, "extras": {"Wooden Cubes"}},
        {"name": "Citadel", "types": {Project}, "extras": {"Wooden Cubes"}},
    ]
)

Menagerie = Set("Menagerie")
Menagerie.AddCards(
    [
        {"name": "Stockpile", "extras": {"Exile Mat"}},
        "Supplies",
        {"name": "Animal Fair", "types": {Action}},
        {"name": "Barge", "types": {Action}},
        {"name": "Black Cat", "types": {Action}},
        {"name": "Bounty Hunter", "types": {Action}, "extras": {"Exile Mat"}},
        {"name": "Camel Train", "types": {Action}, "extras": {"Exile Mat"}},
        {"name": "Cardinal", "types": {Action}, "extras": {"Exile Mat"}},
        {"name": "Cavalry", "types": {Action}},
        {"name": "Coven", "types": {Action}, "extras": {"Exile Mat"}},
        {"name": "Destrier", "types": {Action}},
        {"name": "Displace", "types": {Action}, "extras": {"Exile Mat"}},
        {"name": "Falconer", "types": {Action}},
        {"name": "Fisherman", "types": {Action}},
        {"name": "Gatekeeper", "types": {Action}, "extras": {"Exile Mat"}},
        {"name": "Goatherd", "types": {Action}},
        {"name": "Groom", "types": {Action}},
        {"name": "Hostelry", "types": {Action}},
        {"name": "Hunting Lodge", "types": {Action}},
        {"name": "Kiln", "types": {Action}},
        {"name": "Livery", "types": {Action}},
        {"name": "Mastermind", "types": {Action}},
        {"name": "Paddock", "types": {Action}},
        {"name": "Sanctuary", "types": {Action}, "extras": {"Exile Mat"}},
        {"name": "Scrap", "types": {Action}},
        {"name": "Sheepdog", "types": {Action}},
        {"name": "Sleigh", "types": {Action}},
        {"name": "Snowy Village", "types": {Action}},
        {"name": "Village Green", "types": {Action}},
        {"name": "Wayfarer", "types": {Action}},
        {"name": "Alliance", "types": {Event}},
        {"name": "Banish", "types": {Event}, "extras": {"Exile Mat"}},
        {"name": "Bargain", "types": {Event}},
        {"name": "Commerce", "types": {Event}},
        {"name": "Delay", "types": {Event}},
        {"name": "Demand", "types": {Event}},
        {"name": "Desperation", "types": {Event}},
        {"name": "Enclave", "types": {Event}, "extras": {"Exile Mat"}},
        {"name": "Enhance", "types": {Event}},
        {"name": "Gamble", "types": {Event}},
        {"name": "Invest", "types": {Event}, "extras": {"Exile Mat"}},
        {"name": "March", "types": {Event}},
        {"name": "Populate", "types": {Event}},
        {"name": "Pursue", "types": {Event}},
        {"name": "Reap", "types": {Event}},
        {"name": "Ride", "types": {Event}},
        {"name": "Seize the Day", "types": {Event}},
        {"name": "Stampede", "types": {Event}},
        {"name": "Toil", "types": {Event}},
        {"name": "Transport", "types": {Event}, "extras": {"Exile Mat"}},
        {"name": "Way of the Butterfly", "types": {Way}},
        {"name": "Way of the Camel", "types": {Way}, "extras": {"Exile Mat"}},
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
        {"name": "Way of the Worm", "types": {Way}, "extras": {"Exile Mat"}},
    ]
)

Allies = Set("Allies")
Allies.AddCards(
    [
        {"name": "Bauble", "extras": {"Coin Tokens", "Favors Mat"}},
        {"name": "Contract", "extras": {"Coin Tokens", "Favors Mat"}},
        {
            "name": "Sycophant",
            "types": {Action},
            "extras": {"Coin Tokens", "Favors Mat"},
        },
        {
            "name": "Townsfolk: Town Crier + Blacksmith + Miller + Elder",
            "types": {Action},
        },
        {
            "name": "Augers: Herb Gatherer + Acolyte + Sorceress + Sibyl",
            "types": {Action},
        },
        {
            "name": "Clashes: Battle Plan + Archer + Warlord + Territory",
            "types": {Action},
        },
        {"name": "Forts: Tent + Garrison + Hill Fort + Stronghold", "types": {Action}},
        {"name": "Merchant Camp", "types": {Action}},
        {
            "name": "Importer",
            "types": {Action},
            "extras": {"Coin Tokens", "Favors Mat"},
        },
        {
            "name": "Odysseys: Old Map, Voyage, Sunken Treasure, Distant Shore",
            "types": {Action},
        },
        {"name": "Sentinel", "types": {Action}},
        {
            "name": "Underling",
            "types": {Action},
            "extras": {"Coin Tokens", "Favors Mat"},
        },
        {
            "name": "Wizards: Student, Conjurer, Sorcerer, Lich",
            "types": {Action},
            "extras": {"Coin Tokens", "Favors Mat"},
        },
        {"name": "Broker", "types": {Action}, "extras": {"Coin Tokens", "Favors Mat"}},
        {"name": "Carpenter", "types": {Action}},
        {"name": "Courier", "types": {Action}},
        {"name": "Innkeeper", "types": {Action}},
        {"name": "Royal Galley", "types": {Action}},
        {"name": "Town", "types": {Action}},
        {"name": "Barbarian", "types": {Action}},
        {"name": "Capital City", "types": {Action}},
        {
            "name": "Emissary",
            "types": {Action},
            "extras": {"Coin Tokens", "Favors Mat"},
        },
        {"name": "Galleria", "types": {Action}},
        {
            "name": "Guildmaster",
            "types": {Action},
            "extras": {"Coin Tokens", "Favors Mat"},
        },
        {"name": "Highwayman", "types": {Action}},
        {"name": "Hunter", "types": {Action}},
        {"name": "Modify", "types": {Action}},
        {"name": "Skirmisher", "types": {Action}},
        {"name": "Specialist", "types": {Action}},
        {"name": "Swap", "types": {Action}},
        {"name": "Marquis", "types": {Action}},
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
        {"name": "Plateau Shepherds", "types": {Ally}, "extras": {"Victory Tokens"}},
        {"name": "Trappers' Lodge", "types": {Ally}},
        {"name": "Woodworkers' Guild", "types": {Ally}},
    ]
)

Plunder = Set("Plunder")
Plunder.AddCards(
    [
        "Abundance",
        "Buried Treasure",
        "Cage",
        "Crucible",
        "Figurine",
        "Gondola",
        "Grotto",
        "Jewelled Egg",
        "King's Cache",
        "Pendant",
        "Pickaxe",
        "Rope",
        "Sack of Loot",
        "Silver Mine",
        "Tools",
        {"name": "Search", "types": {Action}},
        {"name": "Shaman", "types": {Action}},
        {"name": "Secluded Shrine", "types": {Action}},
        {"name": "Siren", "types": {Action}},
        {"name": "Stowaway", "types": {Action}},
        {"name": "Taskmaster", "types": {Action}},
        {"name": "Cabin Boy", "types": {Action}},
        {"name": "Flagship", "types": {Action}},
        {"name": "Fortune Hunter", "types": {Action}},
        {"name": "Harbor Village", "types": {Action}},
        {"name": "Landing Party", "types": {Action}},
        {"name": "Mapmaker", "types": {Action}},
        {"name": "Maroon", "types": {Action}},
        {"name": "Swamp Shacks", "types": {Action}},
        {"name": "Crew", "types": {Action}},
        {"name": "Cutthroat", "types": {Action}},
        {"name": "Enlarge", "types": {Action}},
        {"name": "First Mate", "types": {Action}},
        {"name": "Frigate", "types": {Action}},
        {"name": "Longship", "types": {Action}},
        {"name": "Mining Road", "types": {Action}},
        {"name": "Pilgrim", "types": {Action}},
        {"name": "Quartermaster", "types": {Action}},
        {"name": "Trickster", "types": {Action}},
        {"name": "Wealthy Village", "types": {Action}},
        {"name": "Bury", "types": {Event}},
        {"name": "Avoid", "types": {Event}},
        {"name": "Deliver", "types": {Event}},
        {"name": "Peril", "types": {Event}},
        {"name": "Rush", "types": {Event}},
        {"name": "Foray", "types": {Event}},
        {"name": "Launch", "types": {Event}},
        {"name": "Mirror", "types": {Event}},
        {"name": "Prepare", "types": {Event}},
        {"name": "Scrounge", "types": {Event}},
        {"name": "Journey", "types": {Event}},
        {"name": "Maelstrom", "types": {Event}},
        {"name": "Looting", "types": {Event}},
        {"name": "Invasion", "types": {Event}},
        {"name": "Prosper", "types": {Event}},
        {"name": "Cheap", "types": {Trait}},
        {"name": "Cursed", "types": {Trait}},
        {"name": "Fated", "types": {Trait}},
        {"name": "Fawning", "types": {Trait}},
        {"name": "Friendly", "types": {Trait}},
        {"name": "Hasty", "types": {Trait}},
        {"name": "Inherited", "types": {Trait}},
        {"name": "Inspiring", "types": {Trait}},
        {"name": "Nearby", "types": {Trait}},
        {"name": "Patient", "types": {Trait}},
        {"name": "Pious", "types": {Trait}},
        {"name": "Reckless", "types": {Trait}},
        {"name": "Rich", "types": {Trait}},
        {"name": "Shy", "types": {Trait}},
        {"name": "Tireless", "types": {Trait}},
    ]
)

Antiquities = Set("Antiquities")
Antiquities.AddCards(
    [
        "Curio",
        "Discovery",
        "Gamepiece",
        {"name": "Inscription", "types": {Action}},
        {"name": "Agora", "types": {Action}},
        {"name": "Aquifer", "types": {Action}},
        {"name": "Tomb Raider", "types": {Action}},
        {"name": "Dig", "types": {Action}},
        {"name": "Moundbuilder Village", "types": {Action}},
        {"name": "Encroach", "types": {Action}},
        {"name": "Stoneworks", "types": {Action}},
        {"name": "Graveyard", "types": {Action}},
        {"name": "Inspector", "types": {Action}},
        {"name": "Archaeologist", "types": {Action}},
        {"name": "Mission House", "types": {Action}},
        {"name": "Mendicant", "types": {Action}},
        {"name": "Profiteer", "types": {Action}},
        {"name": "Miner", "types": {Action}},
        {"name": "Pyramid", "types": {Action}},
        {"name": "Mastermind", "types": {Action}},
        {"name": "Mausoleum", "types": {Action}},
        {"name": "Shipwreck", "types": {Action}},
        {"name": "Collector", "types": {Action}},
        {"name": "Pharaoh", "types": {Action}},
        {"name": "Grave Watcher", "types": {Action}},
        {"name": "Stronghold", "types": {Action}},
        {"name": "Snake Charmer", "types": {Action}},
    ]
)

# Define Landscape cards
Events = Adventures.events | Empires.events | Menagerie.events | Plunder.events
Landmarks = Empires.landmarks
Projects = Renaissance.projects
Ways = Menagerie.ways
Traits = Plunder.traits
LandscapeCards = Events | Landmarks | Projects | Ways | Traits

# Define action cards
Actions = set().union(*(cardSet.actions for cardSet in AllSets.values()))

# Define cards requiring potions
PotionCards = Alchemy.potionCards

# Define Ally cards
AllyCards = Allies.allyCards

# Define randomizer rules
# PlatinumLove cards grant additional value to other cards or care about extra buys
PlatinumLove = Prosperity.cards.union(
    Base.cards("Artisan", "Council Room", "Merchant", "Mine"),
    Intrigue.cards("Harem", "Nobles"),
    Seaside.cards("Explorer", "Treasure Map", "Pirate"),
    Alchemy.cards("Philosopher's Stone"),
    Cornucopia.cards("Tournament"),
    Hinterlands.cards(
        "Border Village",
        "Cache",
        "Duchess",
        "Embassy",
        "Fool's Gold",
        "Nomads",
        "Cauldron",
        "Souk",
    ),
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
    Plunder.cards(
        "Search",
        "Fortune Hunter",
        "Harbor Village",
        "Mining Road",
        "Pendant",
        "King's Cache",
        "Deliver",
        "Prosper",
    ),
)

# ShelterLove cards are cards that trash for benefit, or gain victory cards.
# Hypothetically, ShelterLove could also include terminal cards, which would
# mean adding a ShelterHate for villages and reducing the chances for each
# ShelterHate.
ShelterLove = DarkAges.cards.union(
    Base.cards("Remodel", "Mine"),
    Intrigue.cards("Replace", "Upgrade"),
    Seaside.cards("Salvager", "Sailor"),
    Alchemy.cards("Apprentice", "Scrying Pool"),
    Prosperity.cards(
        "Bishop",
        "Expand",
        "Forge",
        "Investment",
        "Crystal Ball",
    ),
    Cornucopia.cards("Remake"),
    Hinterlands.cards("Develop", "Farmland", "Trader", "Souk"),
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
    Plunder.cards(
        "Cage",
        "Jewelled Egg",
        "Search",
        "Shaman",
        "Enlarge",
        "Peril",
        "Scrounge",
        "Invasion",
        "Inherited",
    ),
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

LootCards = Plunder.cards(
    "Cutthroat",
    "Jewelled Egg",
    "Pickaxe",
    "Sack of Loot",
    "Search",
    "Wealthy Village",
    # Events
    "Foray",
    "Invasion",
    "Looting",
    "Peril",
    "Prosper",
    # Traits
    "Cursed",
)

# TrapLove: cards that care about discarding, sifting, extra kingdom pile
# gains, and value for multiple gains
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
    Seaside.cards(
        "Lookout",
        "Warehouse",
        "Navigator",
        "Salvager",
        "Monkey",
        "Sailor",
        "Sea Witch",
    ),
    Alchemy.cards("University"),
    Prosperity.cards(
        "Loan",
        "Watchtower",
        "Bishop",
        "Vault",
        "Venture",
        "Goons",
        "Expand",
        "Forge",
        "Tiara",
        "Crystal Ball",
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
        "Wheelwright",
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
        {
            "name": "Forts: Tent + Garrison + Hill Fort + Stronghold",
            "extras": {"Coin Tokens"},
        },
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
    Plunder.cards(
        "Cage",
        "Grotto",
        "Mapmaker",
        "Pickaxe",
        "Quartermaster",
        "Avoid",
        "Foray",
        "Prepare",
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
        "Chancellor",
        "Chapel",
        "Harbinger",
        "Merchant",
        "Moat",
        "Vassal",
        "Village",
        "Woodcutter",
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
        "Crossroads",
        "Develop",
        "Duchess",
        "Fool's Gold",
        "Oasis",
        "Scheme",
        "Tunnel",
        "Guard Dog",
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
    Prosperity.cards(
        "Anvil",
        "Loan",
        "Trade Route",
        "Watchtower",
    ),
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
        "Astrolabe",
        "Embargo",
        "Fishing Village",
        "Haven",
        "Lighthouse",
        "Lookout",
        "Monkey",
        "Native Village",
        "Pearl Diver",
        "Sea Chart",
        "Smugglers",
        "Warehouse",
    ),
    Plunder.cards(
        "Cage",
        "Grotto",
        "Jewelled Egg",
        "Search",
        "Shaman",
        "Secluded Shrine",
        "Siren",
        "Stowaway",
        "Taskmaster",
    ),
)

CannotHaveTraits = set().union(
    Base.cards("Gardens"),
    Seaside.cards("Astrolabe"),
    Alchemy.cards("Vineyard"),
    Cornucopia.cards("Fairgrounds"),
    Hinterlands.cards(
        "Tunnel",
        "Silk Road",
    ),
    DarkAges.cards("Feodum"),
    Empires.cards("Castles"),
    Nocturne.cards(
        "Guardian",
        "Monastery",
        "Changeling",
        "Ghost Town",
        "Night Watchman",
        "Cemetary",
        "Devil's Workshop",
        "Exorcist",
        "Cobbler",
        "Crypt",
        "Den of Sin",
        "Vampire",
        "Raider",
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
            else:
                Base.RemoveCards(Base.firstEdition)

            if not options.get("base-second-edition", True):
                Base.RemoveCards(Base.secondEdition)
            else:
                Base.AddCards(Base.secondEdition)

        if Intrigue in sets:
            if options.get("intrigue-first-edition"):
                Intrigue.AddCards(Intrigue.firstEdition)
            else:
                Intrigue.RemoveCards(Intrigue.firstEdition)

            if not options.get("intrigue-second-edition", True):
                Intrigue.RemoveCards(Intrigue.secondEdition)
            else:
                Intrigue.AddCards(Intrigue.secondEdition)

        if Prosperity in sets:
            if options.get("prosperity-first-edition"):
                Prosperity.AddCards(Prosperity.firstEdition)
            else:
                Prosperity.RemoveCards(Prosperity.firstEdition)

            if not options.get("prosperity-second-edition", True):
                Prosperity.RemoveCards(Prosperity.secondEdition)
            else:
                Prosperity.AddCards(Prosperity.secondEdition)

        if Seaside in sets:
            if options.get("seaside-first-edition"):
                Seaside.AddCards(Seaside.firstEdition)
            else:
                Seaside.RemoveCards(Seaside.firstEdition)

            if not options.get("seaside-second-edition", True):
                Seaside.RemoveCards(Seaside.secondEdition)
            else:
                Seaside.AddCards(Seaside.secondEdition)

        if Hinterlands in sets:
            if options.get("hinterlands-first-edition"):
                Hinterlands.AddCards(Hinterlands.firstEdition)
            else:
                Hinterlands.RemoveCards(Hinterlands.firstEdition)

            if not options.get("hinterlands-second-edition", True):
                Hinterlands.RemoveCards(Hinterlands.secondEdition)
            else:
                Hinterlands.AddCards(Hinterlands.secondEdition)

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
                elif card.types & {Event, Landmark, Project, Trait}:
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
        if not alchemyCards:
            kingdomSet -= Alchemy.cards
        elif len(alchemyCards) == 1:
            # If there's only 1 Alchemy card, remove Alchemy from the options
            # and draw an addtional Kingdom card
            resultSet -= alchemyCards
            kingdomSet -= Alchemy.cards
            resultSet.update(random.sample(kingdomSet - resultSet, 1))
        elif len(alchemyCards) == 2:
            # If there are only 2 Alchemy cards, pull an additional Alchemy
            # card and randomly remove one non-Alchemy card
            resultSet -= alchemyCards
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

    # Check for Loot cards
    includeLoot = LootCards & (fullResults | mouseSet)

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
    if includeLoot:
        landscapeList.append("(Plunder: Loot Deck)")

    # Assign Traits to selected cards
    selectedTraits = Traits.intersection(landscapeList)
    if selectedTraits:
        eligibleCards = resultSet - CannotHaveTraits
        for trait in selectedTraits:
            landscapeList.remove(trait)
            if not eligibleCards:
                break
            traitCard = random.sample(eligibleCards, 1)[0]
            eligibleCards.remove(traitCard)
            landscapeList.append("{} (on {})".format(trait, traitCard))

    # Obelisk support
    obeliskPicked = Empires.cards("Obelisk").intersection(landscapeList)
    if obeliskPicked:
        eligibleCards = resultSet & Actions
        (obelisk,) = Empires.cards("Obelisk")
        landscapeList.remove(list(obeliskPicked)[0])
        if eligibleCards:
            obeliskCard = random.sample(eligibleCards, 1)[0]
            landscapeList.append(
                "(Empires Landmark): Obelisk (on {})".format(obeliskCard)
            )

    # Handle extras
    extras = set().union(*(card.extras for card in resultSet))

    # Create final card list
    if includeBane:
        # Append Bane Card to end of list
        resultSet.remove(baneCard)
        extras.update(baneCard.extras)
        finalResult = sorted(resultSet | additionalCards)
        finalResult.append("Bane is {}".format(baneCard))
    else:
        finalResult = sorted(resultSet | additionalCards)

    # Add non-kingdom cards
    if includeAlly:
        ally = random.sample(AllyCards, 1)[0]
        extras.update(ally.extras)
        finalResult.append(ally)
    finalResult.extend(sorted(landscapeList))
    if includeMouse:
        extras.update(mouseCard.extras)
        finalResult.append("Mouse is {}".format(mouseCard))

    # append extras at the end
    if "Coffers Mat" in extras and Allies in sets:
        extras.remove("Coffers Mat")
        extras.add("Coffers/Villagers Mat")
    if extras:
        finalResult.append("Extras:")
        finalResult.extend(sorted(extras))

    return [str(card) for card in finalResult]


if __name__ == "__main__":
    print("\n".join(RandomizeDominion()))
