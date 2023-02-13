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
Victory = CardType("Victory")
Reaction = CardType("Reaction")
Attack = CardType("Attack")
# for enhanced randomizer
cbBadSifter = CardType("cbBadSifter")  # attacks by messing up your deck
cbBadThinner = CardType("cbBadThinner")  # attacks by messing up your deck
cbBlocker = CardType(
    "cbBlocker"
)  # allows you to be immune to attacks. Wants for Attacks
cbBuys = CardType("cbBuys")  # allow you to buy more cards in a turn.
cbCantrip = CardType(
    "cbCantrip"
)  # card draws and chains, which essentially makes it a free bonus card
cbChainer = CardType("cbChainer")  # allows you to play another action after it is done
cbCost2 = CardType("cbCost2")  # card costs 2
cbCost3 = CardType("cbCost3")  # card costs 3
cbCost4 = CardType("cbCost4")  # card costs 4
cbCost5 = CardType("cbCost5")  # card costs 5
cbCost6 = CardType("cbCost6")  # card costs 6
cbCostReducer = CardType(
    "cbCostReducer"
)  # reduces the cost of cards. synnergizes with cbBuys and cbGainer
cbCurser = CardType("cbCurser")  # gives other players curses
cbDeckGuesser = CardType(
    "cbDeckGuesser"
)  # allows you to guess cards from the top of your deck. wants for cbDeckSeeder
cbDeckSeeder = CardType(
    "cbDeckSeeder"
)  # allows you to manipulate your deck; synnergizes with cbDeckGuesser
cbDiscard = CardType(
    "cbDiscard"
)  # discards cards because sometimes you want to do that
cbDraw2 = CardType("cbDraw2")  # draws 2 cards
cbDraw3 = CardType("cbDraw3")  # draws 3 cards
cbDraw4 = CardType("cbDraw4")  # draws 4 cards
cbEmpty = CardType("cbEmpty")  # cares about empty supply piles
cbFiller = CardType(
    "cbFiller"
)  # fills hand up to a certain point; synnergizes with cbDiscard
cbGainer4 = CardType(
    "cbGainer4"
)  # allows you to gain cards from the supply costing up to 4; synnergizes with cbCostReducer, cbCost4
cbGainer5 = CardType(
    "cbGainer5"
)  # allows you to gain cards from the supply costing up to 5; synnergizes with cbCostReducer, cbCost5
cbInteractive = CardType(
    "cbInteractive"
)  # does something to other players that is not an attack

cbMoney1 = CardType("cbMoney1")  # gives +1 Money
cbMoney2 = CardType("cbMoney2")  # gives +2 Money
cbMoney3 = CardType("cbMoney3")  # gives +3 Money
cbPeddler = CardType(
    "cbPeddler"
)  # cantrip that give +1 Money; seperate class for randomizer reasons
cbShuffler = CardType("cbShuffler")  # allows you to shuffle your deck immediately
cbSifter = CardType("cbSifter")  # draws and discards cards to improve hands
cbSplitter = CardType(
    "cbSplitter"
)  # allows you to play cards multiple times. Synnergizes with cbCantrip, cbChainer, and cbPeddler
cbTerminal = CardType(
    "cbTerminal"
)  # doesn't allow more actions to be played. synnergizes with cbSplitter and cbVillage
cbThinner = CardType(
    "cbThinner"
)  # Puts cards into the trash and leaves you with a smaller deck
cbTrasher = CardType(
    "cbTrasher"
)  # Puts cards into the trash, but doesn't thin your deck
cbTwin = CardType(
    "cbTwin"
)  # Donald X's secret type that is a good idea to buy 2 of on turn 1
cbUpgrader = CardType(
    "cbUpgrader"
)  # allows you to trash cards and replace them with better cards
cbVillage = CardType(
    "cbVillage"
)  # replaces itself and allows multiple terminals to be played

# Define sets
Base = Set("Base")
Base.AddCards(
    [
        {
            "name": "Artisan",
            "types": {Action, cbCost6, cbDeckSeeder, cbGainer5, cbTerminal},
        },
        {
            "name": "Bandit",
            "types": {Action, Attack, cbBadSifter, cbBadThinner, cbCost5, cbTerminal},
        },
        {
            "name": "Bureaucrat",
            "types": {Action, Attack, cbCost4, cbDeckSeeder, cbTerminal},
        },
        {"name": "Cellar", "types": {Action, cbChainer, cbCost2, cbSifter}},
        {"name": "Chapel", "types": {Action, cbCost2, cbTerminal, cbThinner}},
        {
            "name": "Council Room",
            "types": {Action, cbBuys, cbCost5, cbDraw4, cbInteractive, cbTerminal},
        },
        {"name": "Festival", "types": {Action, cbBuys, cbBuys, cbMoney2}},
        {"name": "Gardens", "types": {Victory, cbCost4}},
        {"name": "Harbinger", "types": {Action, cbCantrip, cbCost3, cbDeckSeeder}},
        {"name": "Laboratory", "types": {Action, cbCantrip, cbCost5, cbDraw2}},
        {"name": "Library", "types": {Action, cbCost5, cbFiller, cbSifter, cbTerminal}},
        {"name": "Market", "types": {Action, cbBuys, cbCost5, cbPeddler}},
        {"name": "Merchant", "types": {Action, cbPeddler, cbCost3, cbMoney1}},
        {
            "name": "Militia",
            "types": {Action, Attack, cbDiscard, cbCost4, cbMoney2, cbTerminal},
        },
        {"name": "Mine", "types": {Action, cbCost5, cbTerminal, cbTrasher, cbUpgrader}},
        {
            "name": "Moat",
            "types": {Action, Reaction, cbBlocker, cbCost2, cbDraw2, cbTerminal},
        },
        {
            "name": "Moneylender",
            "types": {Action, cbCost4, cbMoney3, cbTerminal, cbThinner},
        },
        {
            "name": "Poacher",
            "types": {Action, cbCost4, cbDiscard, cbEmpty, cbPeddler},
        },
        {
            "name": "Remodel",
            "types": {Action, cbCost4, cbTerminal, cbTrasher, cbUpgrader},
        },
        {"name": "Sentry", "types": {Action, cbCantrip, cbCost5, cbSifter, cbThinner}},
        {"name": "Smithy", "types": {Action, cbCost4, cbDraw3, cbTerminal}},
        {"name": "Throne Room", "types": {Action, cbCost4, cbSplitter}},
        {"name": "Workshop", "types": {Action, cbCost3, cbGainer4, cbTerminal}},
        {
            "name": "Vassal",
            "types": {Action, cbCost3, cbMoney2, cbTerminal, cbTwin},
        },
        {"name": "Village", "types": {Action, cbCost3, cbVillage}},
        {"name": "Witch", "types": {Action, cbCost5, cbCurser, cbTerminal}},
    ]
)
Base.firstEdition = [
    {"name": "Adventurer", "types": {Action, cbCost6, cbSifter, cbTerminal}},
    {
        "name": "Chancellor",
        "types": {Action, cbCost3, cbMoney2, cbShuffler, cbTerminal},
    },
    {"name": "Feast", "types": {Action, cbCost4, cbTerminal, cbTrasher, cbUpgrader}},
    {"name": "Spy", "types": {Action, Attack, cbBadSifter, cbCost4, cbSifter}},
    {"name": "Thief", "types": {Action, Attack, cbBadThinner, cbCost4, cbTerminal}},
    {"name": "Woodcutter", "types": {Action, cbBuys, cbCost3, cbMoney2, cbTerminal}},
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
        {"name": "Island", "types": {Action}},
        {"name": "Lighthouse", "types": {Action}},
        {"name": "Lookout", "types": {Action}},
        {"name": "Merchant Ship", "types": {Action}},
        {"name": "Monkey", "types": {Action}},
        {"name": "Native Village", "types": {Action}},
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
    {"name": "Embargo", "types": {Action}},
    {"name": "Pearl Diver", "types": {Action}},
    {"name": "Ambassador", "types": {Action}},
    {"name": "Navigator", "types": {Action}},
    {"name": "Pirate Ship", "types": {Action}},
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
        "Collection",
        "Hoard",
        "Investment",
        "Quarry",
        "Tiara",
        "War Chest",
        {"name": "Bishop", "types": {Action}},
        {"name": "Charlatan", "types": {Action}},
        {"name": "City", "types": {Action}},
        {"name": "Clerk", "types": {Action}},
        {"name": "Expand", "types": {Action}},
        {"name": "Forge", "types": {Action}},
        {"name": "Grand Market", "types": {Action}},
        {"name": "King's Court", "types": {Action}},
        {"name": "Magnate", "types": {Action}},
        {"name": "Mint", "types": {Action}},
        {"name": "Monument", "types": {Action}},
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
    {"name": "Goons", "types": {Action}},
    {"name": "Mountebank", "types": {Action}},
    {"name": "Trade Route", "types": {Action}},
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
        {"name": "Candlestick Maker", "types": {Action}},
        {"name": "Stonemason", "types": {Action}},
        {"name": "Doctor", "types": {Action}},
        {"name": "Advisor", "types": {Action}},
        {"name": "Plaza", "types": {Action}},
        {"name": "Taxman", "types": {Action}},
        {"name": "Herald", "types": {Action}},
        {"name": "Baker", "types": {Action}},
        {"name": "Butcher", "types": {Action}},
        {"name": "Journeyman", "types": {Action}},
        {"name": "Merchant Guild", "types": {Action}},
        {"name": "Soothsayer", "types": {Action}},
    ]
)

Adventures = Set("Adventures")
Adventures.AddCards(
    [
        "Coin of the Realm",
        "Distant Lands",
        "Relic",
        "Treasure Trove",
        {"name": "Page", "types": {Action}},
        {"name": "Peasant", "types": {Action}},
        {"name": "Ratcatcher", "types": {Action}},
        {"name": "Raze", "types": {Action}},
        {"name": "Amulet", "types": {Action}},
        {"name": "Caravan Guard", "types": {Action}},
        {"name": "Dungeon", "types": {Action}},
        {"name": "Gear", "types": {Action}},
        {"name": "Guide", "types": {Action}},
        {"name": "Duplicate", "types": {Action}},
        {"name": "Magpie", "types": {Action}},
        {"name": "Messenger", "types": {Action}},
        {"name": "Miser", "types": {Action}},
        {"name": "Port", "types": {Action}},
        {"name": "Ranger", "types": {Action}},
        {"name": "Transmogrify", "types": {Action}},
        {"name": "Artificer", "types": {Action}},
        {"name": "Bridge Troll", "types": {Action}},
        {"name": "Giant", "types": {Action}},
        {"name": "Haunted Woods", "types": {Action}},
        {"name": "Lost City", "types": {Action}},
        {"name": "Royal Carriage", "types": {Action}},
        {"name": "Storyteller", "types": {Action}},
        {"name": "Swamp Hag", "types": {Action}},
        {"name": "Wine Merchant", "types": {Action}},
        {"name": "Hireling", "types": {Action}},
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
        "Castles",
        "Capital",
        "Charm",
        {"name": "Engineer", "types": {Action}},
        {"name": "City Quarter", "types": {Action}},
        {"name": "Overlord", "types": {Action}},
        {"name": "Royal Blacksmith", "types": {Action}},
        {"name": "Encampment/Plunder", "types": {Action}},
        {"name": "Patrician/Emporium", "types": {Action}},
        {"name": "Settlers/Bustling Village", "types": {Action}},
        {"name": "Catapult/Rocks", "types": {Action}},
        {"name": "Chariot Race", "types": {Action}},
        {"name": "Enchantress", "types": {Action}},
        {"name": "Farmers' Market", "types": {Action}},
        {"name": "Gladiator/Fortune", "types": {Action}},
        {"name": "Sacrifice", "types": {Action}},
        {"name": "Temple", "types": {Action}},
        {"name": "Villa", "types": {Action}},
        {"name": "Archive", "types": {Action}},
        {"name": "Crown", "types": {Action}},
        {"name": "Forum", "types": {Action}},
        {"name": "Groundskeeper", "types": {Action}},
        {"name": "Legionary", "types": {Action}},
        {"name": "Wild Hunt", "types": {Action}},
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
        "Ducat",
        "Scepter",
        "Spices",
        {"name": "Border Guard", "types": {Action}},
        {"name": "Lackeys", "types": {Action}},
        {"name": "Acting Troupe", "types": {Action}},
        {"name": "Cargo Ship", "types": {Action}},
        {"name": "Experiment", "types": {Action}},
        {"name": "Improve", "types": {Action}},
        {"name": "Flag Bearer", "types": {Action}},
        {"name": "Hideout", "types": {Action}},
        {"name": "Inventor", "types": {Action}},
        {"name": "Mountain Village", "types": {Action}},
        {"name": "Patron", "types": {Action}},
        {"name": "Priest", "types": {Action}},
        {"name": "Research", "types": {Action}},
        {"name": "Silk Merchant", "types": {Action}},
        {"name": "Old Witch", "types": {Action}},
        {"name": "Recruiter", "types": {Action}},
        {"name": "Scholar", "types": {Action}},
        {"name": "Sculptor", "types": {Action}},
        {"name": "Seer", "types": {Action}},
        {"name": "Swashbuckler", "types": {Action}},
        {"name": "Treasurer", "types": {Action}},
        {"name": "Villain", "types": {Action}},
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
        "Stockpile",
        "Supplies",
        {"name": "Animal Fair", "types": {Action}},
        {"name": "Barge", "types": {Action}},
        {"name": "Black Cat", "types": {Action}},
        {"name": "Bounty Hunter", "types": {Action}},
        {"name": "Camel Train", "types": {Action}},
        {"name": "Cardinal", "types": {Action}},
        {"name": "Cavalry", "types": {Action}},
        {"name": "Coven", "types": {Action}},
        {"name": "Destrier", "types": {Action}},
        {"name": "Displace", "types": {Action}},
        {"name": "Falconer", "types": {Action}},
        {"name": "Fisherman", "types": {Action}},
        {"name": "Gatekeeper", "types": {Action}},
        {"name": "Goatherd", "types": {Action}},
        {"name": "Groom", "types": {Action}},
        {"name": "Hostelry", "types": {Action}},
        {"name": "Hunting Lodge", "types": {Action}},
        {"name": "Kiln", "types": {Action}},
        {"name": "Livery", "types": {Action}},
        {"name": "Mastermind", "types": {Action}},
        {"name": "Paddock", "types": {Action}},
        {"name": "Sanctuary", "types": {Action}},
        {"name": "Scrap", "types": {Action}},
        {"name": "Sheepdog", "types": {Action}},
        {"name": "Sleigh", "types": {Action}},
        {"name": "Snowy Village", "types": {Action}},
        {"name": "Village Green", "types": {Action}},
        {"name": "Wayfarer", "types": {Action}},
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
        "Contract",
        {"name": "Sycophant", "types": {Action}},
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
        {"name": "Importer", "types": {Action}},
        {
            "name": "Odysseys: Old Map, Voyage, Sunken Treasure, Distant Shore",
            "types": {Action},
        },
        {"name": "Sentinel", "types": {Action}},
        {"name": "Underling", "types": {Action}},
        {"name": "Wizards: Student, Conjurer, Sorcerer, Lich", "types": {Action}},
        {"name": "Broker", "types": {Action}},
        {"name": "Carpenter", "types": {Action}},
        {"name": "Courier", "types": {Action}},
        {"name": "Innkeeper", "types": {Action}},
        {"name": "Royal Galley", "types": {Action}},
        {"name": "Town", "types": {Action}},
        {"name": "Barbarian", "types": {Action}},
        {"name": "Capital City", "types": {Action}},
        {"name": "Emissary", "types": {Action}},
        {"name": "Galleria", "types": {Action}},
        {"name": "Guildmaster", "types": {Action}},
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
        {"name": "Plateau Shepherds", "types": {Ally}},
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
        if len(alchemyCards) == 1:
            # If there's only 1 Alchemy card, remove Alchemy from the options
            # and draw an addtional Kingdom card
            resultSet -= alchemyCards
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
