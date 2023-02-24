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
                card for card in self._cards if card.types & {_Potion}
            )
        return self._potionCards


# Define card types
# Landmarky Things
Event = CardType("Event")
Landmark = CardType("Landmark")
Project = CardType("Project")
Way = CardType("Way")
Ally = CardType("Ally")
Trait = CardType("Trait")
# Potion isn't written on the card
Action = CardType("Action")
Attack = CardType("Attack")
Command = CardType("Command")
Duration = CardType("Duration")
Knight = CardType("Knight")
Looter = CardType("Looter")
_Potion = CardType("_Potion")
Reaction = CardType("Reaction")
Reserve = CardType("Reserve")
Traveller = CardType("Traveller")
Treasure = CardType("Treasure")
Victory = CardType("Victory")
# for enhanced randomizer
_AttackResponse = CardType(
    "_AttackResponse"
)  # allows you to respond to attacks. Wants for Attacks
_BadSifter = CardType("_BadSifter")  # attacks by messing up your deck
_BadThinner = CardType("_BadThinner")  # attacks by trashing good things
_Buys = CardType("_Buys")  # allow you to buy more cards in a turn.
_Cantrip = CardType(
    "_Cantrip"
)  # card draws and chains, which essentially makes it a free bonus card
_Chainer = CardType("_Chainer")  # allows you to play another action after it is done
_Choice = CardType("_Choice")  # gives you a set of choices
_Command4 = CardType(
    "_Command4"
)  # allows you to play cards costing up to 4. Synnergizes with _Cost4.
_Cost0 = CardType("_Cost0")  # card costs 0
_Cost1 = CardType("_Cost1")  # card costs 1
_Cost2 = CardType("_Cost2")  # card costs 2
_Cost3 = CardType("_Cost3")  # card costs 3
_Cost4 = CardType("_Cost4")  # card costs 4
_Cost5 = CardType("_Cost5")  # card costs 5
_Cost6 = CardType("_Cost6")  # card costs 6
_Cost7 = CardType("_Cost7")  # card costs 7
_Cost8 = CardType("_Cost8")  # card costs 8
_CostReducer = CardType(
    "_CostReducer"
)  # reduces the cost of cards. synnergizes with _Buys and _Gainer
_CostVaries = CardType("_CostVaries")  # Gets cheaper or more expensive.
_Curser = CardType("_Curser")  # gives other players curses
_DeckGuesser = CardType(
    "_DeckGuesser"
)  # allows you to guess cards from the top of your deck. wants for _DeckSeeder
_DeckSeeder = CardType(
    "_DeckSeeder"
)  # allows you to manipulate your deck; synnergizes with _DeckGuesser
_Discard = CardType("_Discard")  # discards cards because sometimes you want to do that
_DiscardResponse = CardType(
    "_DiscardResponse"
)  # Reaction triggered by discards other than cleanup. Wants _Discard
_Downgrader = CardType("_Downgrader")  # attack card that does upgrades in reverse
_Draw2 = CardType("_Draw2")  # draws 2 cards
_Draw3 = CardType("_Draw3")  # draws 3 cards
_Draw4 = CardType("_Draw4")  # draws 4 cards
_Draw5 = CardType("_Draw5")  # draws 5 cards
_Drawload = CardType("_Drawload")  # draws potentially infinite numbers of cards
_Empty = CardType("_Empty")  # cares about empty supply piles
_ExtraCost = CardType(
    "_ExtraCost"
)  # has an extra cost, preventing gainers from gaining it. Bad synnergy with gainers
_Filler = CardType(
    "_Filler"
)  # fills hand up to a certain point; synnergizes with _Discard
_FreeAction = CardType(
    "_FreeAction"
)  # card that can play itself without expending actions
_FreeEvent = CardType(
    "_FreeEvent"
)  # event that gives you one buy, and therefore essentially costs no buy.
_FutureAction = CardType(
    "_FutureAction"
)  # gives a bonus action at the start of next turn
_FutureMoney1 = CardType(
    "_FutureMoney1"
)  # gives you future money, such as by giving 1 coffer or gaining a silver
_FutureMoney2 = CardType(
    "_FutureMoney2"
)  # gives you future money, such as by giving 2 coffers or gaining a gold
_FutureMoney4 = CardType(
    "_FutureMoney4"
)  # gives you future money, such as by giving gaining 2 spoils
_Gainer3 = CardType(
    "_Gainer3"
)  # allows you to gain cards from the supply costing up to 3; synnergizes with _CostReducer, _Cost3
_Gainer4 = CardType(
    "_Gainer4"
)  # allows you to gain cards from the supply costing up to 4; synnergizes with _CostReducer, _Cost4
_Gainer5 = CardType(
    "_Gainer5"
)  # allows you to gain cards from the supply costing up to 5; synnergizes with _CostReducer, _Cost5
_Gainer6 = CardType(
    "_Gainer6"
)  # allows you to gain cards from the supply costing up to 6; synnergizes with _CostReducer, _Cost6
_Kingdom = CardType("_Kingdom")  # Adds cards to the kingdom
_Interactive = CardType(
    "_Interactive"
)  # does something to other players that is not an attack
_Junker = CardType("_Junker")  # attacker gives opponents bad cards
_Money1 = CardType("_Money1")  # gives +1 Money
_Money2 = CardType("_Money2")  # gives +2 Money
_Money3 = CardType("_Money3")  # gives +3 Money
_Money4 = CardType("_Money4")  # gives +4 Money
_Money5 = CardType("_Money5")  # gives +5 Money
_MultiType = CardType("_MultiType")  # has more than two types
_MultiTypeLove = CardType("_MultiTypeLove")  # Wants cards with more than two types
_NamesMatter = CardType(
    "_NamesMatter"
)  # Wants a lot of different names in the game. Synnergizes with Looter, _SplitPile, etc
_Overpay = CardType(
    "_Overpay"
)  # Allows you to pay more for more functionality. Synnergizes with _Money3, _Money4, _Money5, _Payload.
_Payload = CardType(
    "_Payload"
)  # a card that adds variable, potentially infinite money.
_Peddler = CardType(
    "_Peddler"
)  # cantrip that give +1 Money; seperate class for randomizer reasons
_Random = CardType(
    "_Random"
)  # a card with seemly random effects (as opposed to _Choice)
_Saver = CardType(
    "_Saver"
)  # puts cards from this hand into future hands, without discards or draws
_Sifter = CardType("_Sifter")  # draws and discards cards to improve future hands
_SpeedUp = CardType("_SpeedUp")  # allows you to get gained cards into play faster
_SplitPile = CardType("_SplitPile")  # There's more than one named thing in here!
_Splitter = CardType(
    "_Splitter"
)  # allows you to play cards multiple times. Synnergizes with _Cantrip, _Chainer, and _Peddler
_Terminal = CardType(
    "_Terminal"
)  # doesn't allow more actions to be played. synnergizes with _Splitter and _Village
_Thinner = CardType(
    "_Thinner"
)  # Puts cards into the trash and leaves you with a smaller deck
_Trasher = CardType("_Trasher")  # Puts cards into the trash, but doesn't thin your deck
_TrashBenefit = CardType("_TrashBenefit")  # Wants to be trashed
_TrashGainer = CardType(
    "_TrashGainer"
)  # Gets cards out of the trash or gains cards in response to trashing. Wants for _Trasher
_Twin = CardType(
    "_Twin"
)  # Donald X's secret type that is a good idea to buy 2 of on turn 1
_Remodeler = CardType(
    "_Remodeler"
)  # allows you to trash cards and replace them with better cards
_Victory = CardType("_Victory")  # gains you victory cards or points
_Village = CardType(
    "_Village"
)  # replaces itself and allows multiple terminals to be played

# Define sets
Base = Set("Base")
Base.AddCards(
    [
        {
            "name": "Artisan",
            "types": {Action, _Cost6, _DeckSeeder, _Gainer5, _Terminal},
        },
        {
            "name": "Bandit",
            "types": {
                Action,
                Attack,
                _BadSifter,
                _BadThinner,
                _Cost5,
                _FutureMoney2,
                _Terminal,
            },
        },
        {
            "name": "Bureaucrat",
            "types": {Action, Attack, _Cost4, _DeckSeeder, _FutureMoney1, _Terminal},
        },
        {"name": "Cellar", "types": {Action, _Chainer, _Cost2, _Sifter}},
        {"name": "Chapel", "types": {Action, _Cost2, _Terminal, _Thinner}},
        {
            "name": "Council Room",
            "types": {Action, _Buys, _Cost5, _Draw4, _Interactive, _Terminal},
        },
        {"name": "Festival", "types": {Action, _Buys, _Buys, _Money2}},
        {"name": "Gardens", "types": {Victory, _Cost4}},
        {"name": "Harbinger", "types": {Action, _Cantrip, _Cost3, _DeckSeeder}},
        {"name": "Laboratory", "types": {Action, _Cantrip, _Cost5, _Draw2}},
        {"name": "Library", "types": {Action, _Cost5, _Filler, _Sifter, _Terminal}},
        {"name": "Market", "types": {Action, _Buys, _Cost5, _Peddler}},
        {"name": "Merchant", "types": {Action, _Peddler, _Cost3, _Money1}},
        {
            "name": "Militia",
            "types": {Action, Attack, _Discard, _Cost4, _Money2, _Terminal},
        },
        {"name": "Mine", "types": {Action, _Cost5, _Remodeler, _Terminal, _Trasher}},
        {
            "name": "Moat",
            "types": {Action, Reaction, _AttackResponse, _Cost2, _Draw2, _Terminal},
        },
        {
            "name": "Moneylender",
            "types": {Action, _Cost4, _Money3, _Terminal, _Thinner},
        },
        {
            "name": "Poacher",
            "types": {Action, _Cost4, _Discard, _Empty, _Peddler},
        },
        {
            "name": "Remodel",
            "types": {Action, _Cost4, _Remodeler, _Terminal, _Trasher},
        },
        {"name": "Sentry", "types": {Action, _Cantrip, _Cost5, _Sifter, _Thinner}},
        {"name": "Smithy", "types": {Action, _Cost4, _Draw3, _Terminal}},
        {"name": "Throne Room", "types": {Action, _Cost4, _Splitter}},
        {"name": "Workshop", "types": {Action, _Cost3, _Gainer4, _Terminal}},
        {
            "name": "Vassal",
            "types": {Action, _Cost3, _Money2, _Terminal, _Twin},
        },
        {"name": "Village", "types": {Action, _Cost3, _Village}},
        {"name": "Witch", "types": {Action, _Cost5, _Curser, _Terminal}},
    ]
)
Base.firstEdition = [
    {"name": "Adventurer", "types": {Action, _Cost6, _Sifter, _Terminal}},
    {
        "name": "Chancellor",
        "types": {Action, _Cost3, _Money2, _SpeedUp, _Terminal},
    },
    {"name": "Feast", "types": {Action, _Cost4, _Gainer5, _Terminal, _Trasher}},
    {"name": "Spy", "types": {Action, Attack, _BadSifter, _Cost4, _Sifter}},
    {
        "name": "Thief",
        "types": {Action, Attack, _BadThinner, _Cost4, _FutureMoney2, _Terminal},
    },
    {"name": "Woodcutter", "types": {Action, _Buys, _Cost3, _Money2, _Terminal}},
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
        {
            "name": "Baron",
            "types": {Action, _Buys, _Cost4, _Money4, _Terminal, _Victory},
        },
        {
            "name": "Bridge",
            "types": {Action, _Buys, _Cost4, _CostReducer, _Money1, _Terminal},
        },
        {"name": "Conspirator", "types": {Action, _Cost4, _Cantrip, _Money2}},
        {
            "name": "Courtier",
            "types": {Action, _Choice, _Cost5, _FutureMoney2, _Money3, _MultiTypeLove},
        },
        {
            "name": "Courtyard",
            "types": {Action, _Cost2, _DeckSeeder, _Draw2, _Terminal},
        },  # draws 2 and seeds 1
        {
            "name": "Diplomat",
            "types": {Action, Reaction, _AttackResponse, _Cost4, _Draw2},
        },
        {"name": "Duke", "types": {Victory, _Cost5}},
        {"name": "Harem", "types": {Treasure, Victory, _Cost6, _Money2}},
        {"name": "Ironworks", "types": {Action, _Choice, _Cost4, _Gainer4}},
        {
            "name": "Lurker",
            "types": {Action, _Cost2, _Chainer, _Trasher, _TrashGainer},
        },
        {
            "name": "Masquerade",
            "types": {Action, _Cost3, _Draw2, _Interactive, _Terminal, _Thinner},
        },
        {
            "name": "Mill",
            "types": {Action, Victory, _Cantrip, _Cost4, _Discard, _Money2},
        },
        {
            "name": "Mining Village",
            "types": {Action, _Cost4, _Money2, _Trasher, _Village},
        },
        {
            "name": "Minion",
            "types": {Action, Attack, _Chainer, _Choice, _Cost5, _Money2, _Sifter},
        },
        {"name": "Nobles", "types": {Action, Victory, _Choice, _Cost6}},
        {"name": "Patrol", "types": {Action, _Cost5, _Draw3, _Sifter, _Terminal}},
        {"name": "Pawn", "types": {Action, _Choice, _Cost2}},
        {
            "name": "Replace",
            "types": {
                Action,
                Attack,
                _Cost5,
                _Curser,
                _DeckSeeder,
                _Remodeler,
                _Terminal,
                _Trasher,
            },
        },
        {"name": "Secret Passage", "types": {Action, _Cantrip, _Cost4, _DeckSeeder}},
        {"name": "Shanty Town", "types": {Action, _Cost3, _Twin, _Village}},
        {"name": "Steward", "types": {Action, _Choice, _Cost3, _Terminal}},
        {
            "name": "Swindler",
            "types": {Action, Attack, _BadSifter, _Cost3, _Money2, _Terminal, _Trasher},
        },
        {
            "name": "Torturer",
            "types": {Action, Attack, _Cost5, _Curser, _Draw3, _Terminal},
        },
        {
            "name": "Trading Post",
            "types": {Action, _Cost5, _FutureMoney1, _Terminal, _Thinner},
        },
        {
            "name": "Upgrade",
            "types": {Action, _Cantrip, _Cost5, _Remodeler, _Trasher},
        },
        {
            "name": "Wishing Well",
            "types": {Action, _Cantrip, _Cost3, _DeckGuesser, _Twin},
        },
    ]
)
Intrigue.firstEdition = [
    {"name": "Coppersmith", "types": {Action, _Cost4, _Payload, _Terminal}},
    {"name": "Great Hall", "types": {Action, Victory, _Cantrip, _Cost3}},
    {
        "name": "Saboteur",
        "types": {Action, Attack, _Downgrader, _Cost5, _Remodeler, _Terminal, _Trasher},
    },
    {"name": "Scout", "types": {Action, _Chainer, _Cost4, _Sifter}},
    {
        "name": "Secret Chamber",
        "types": {Action, Reaction, _AttackResponse, _Cost2, _DeckSeeder, _Discard},
    },
    {
        "name": "Tribute",
        "types": {Action, _Choice, _Cost5, _Discard, _MultiTypeLove},
    },
]
Intrigue.secondEdition = Intrigue.cards(
    "Courtier", "Diplomat", "Lurker", "Mill", "Patrol", "Replace", "Secret Passage"
)

Seaside = Set("Seaside")
Seaside.AddCards(
    [
        {"name": "Astrolabe", "types": {Treasure, Duration, _Buys, _Cost3, _Money2}},
        {"name": "Bazaar", "types": {Action, _Cost5, _Peddler, _Village}},
        {
            "name": "Blockade",
            "types": {Action, Duration, Attack, _Cost4, _Curser, _Gainer4, _MultiType},
        },
        {"name": "Caravan", "types": {Action, Duration, _Cantrip, _Cost4, _Draw2}},
        {
            "name": "Corsair",
            "types": {
                Action,
                Duration,
                Attack,
                _BadThinner,
                _Cost5,
                _Draw2,
                _Money2,
                _MultiType,
                _Terminal,
            },
        },
        {"name": "Cutpurse", "types": {Action, Attack, _Cost4, _Discard, _Money2}},
        {
            "name": "Fishing Village",
            "types": {Action, Duration, _Cost3, _FutureAction, _Money2, _Village},
        },
        {"name": "Haven", "types": {Action, Duration, _Cantrip, _Cost2, _Saver}},
        {"name": "Island", "types": {Action, Victory, _Cost4, _Terminal, _Thinner}},
        {
            "name": "Lighthouse",
            "types": {Action, Duration, _AttackResponse, _Chainer, _Cost2, _Money2},
        },
        {"name": "Lookout", "types": {Action, _Chainer, _Cost3, _Sifter, _Thinner}},
        {
            "name": "Merchant Ship",
            "types": {Action, Duration, _Cost5, _Money4, _Terminal},
        },
        {"name": "Monkey", "types": {Action, Duration, _Cost3, _Draw2, _Terminal}},
        {"name": "Native Village", "types": {Action, _Cost2, _Saver, _Village}},
        {"name": "Outpost", "types": {Action, Duration, _Cost5, _Draw3, _Terminal}},
        {
            "name": "Pirate",
            "types": {
                Action,
                Duration,
                Reaction,
                _Cost5,
                _FutureMoney2,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Sailor",
            "types": {Action, Duration, _Cost4, _Money2, _SpeedUp, _Thinner, _Village},
        },
        {
            "name": "Salvager",
            "types": {Action, _Cost4, _Payload, _Terminal, _Thinner},
        },
        {"name": "Sea Chart", "types": {Action, _Cantrip, _Cost3, _DeckGuesser, _Twin}},
        {
            "name": "Sea Witch",
            "types": {
                Action,
                Duration,
                Attack,
                _Cost5,
                _Curser,
                _Draw2,
                _MultiType,
                _Sifter,
                _Terminal,
            },
        },
        {"name": "Smugglers", "types": {Action, _Cost3, _Gainer6, _Terminal}},
        {
            "name": "Tactician",
            "types": {
                Action,
                Duration,
                _Buys,
                _Cost5,
                _Discard,
                _Draw5,
                _FutureAction,
                _Terminal,
            },
        },
        {
            "name": "Tide Pools",
            "types": {Action, Duration, _Cantrip, _Cost4, _Sifter},
        },
        {
            "name": "Treasure Map",
            "types": {Action, _Cost4, _DeckSeeder, _FutureMoney2, _Trasher, _Terminal},
        },
        {"name": "Treasury", "types": {Action, _Cost5, _DeckSeeder, _Peddler}},
        {
            "name": "Warehouse",
            "types": {Action, _Cantrip, _Cost3, _Discard, _Sifter},
        },
        {
            "name": "Wharf",
            "types": {Action, Duration, _Buys, _Cost5, _Draw4, _Terminal},
        },
    ]
)
Seaside.firstEdition = [
    {
        "name": "Ambassador",
        "types": {Action, Attack, _Cost3, _Junker, _Terminal, _Thinner},
    },
    {"name": "Embargo", "types": {Action, _Cost2, _Curser, _Money2, _Trasher}},
    {
        "name": "Explorer",
        "types": {Action, _Cost5, _FutureMoney1, _FutureMoney2, _Terminal},
    },
    {
        "name": "Ghost Ship",
        "types": {Action, Attack, _Cost5, _Draw2, _BadSifter, _Terminal},
    },
    {"name": "Navigator", "types": {Action, _Cost4, _Money2, _Sifter, _Terminal}},
    {"name": "Pearl Diver", "types": {Action, _Cantrip, _Cost2, _DeckSeeder}},
    {
        "name": "Pirate Ship",
        "types": {Action, Attack, _BadSifter, _BadThinner, _Cost4, _Payload, _Terminal},
    },
    {
        "name": "Sea Hag",
        "types": {Action, Attack, _Cost4, _Curser, _Discard, _Terminal},
    },
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
        # the main point of _Cost# is synnergy with _Gainer#, so cards that can't be
        # gained don't have cost
        {
            "name": "Alchemist",
            "types": {Action, _Potion, _Cantrip, _DeckSeeder, _ExtraCost},
        },
        {
            "name": "Apothecary",
            "types": {Action, _Potion, _Cantrip, _ExtraCost, _Sifter},
        },
        {
            "name": "Apprentice",
            "types": {Action, _Chainer, _Cost5, _Drawload, _Thinner},
        },
        {
            "name": "Familiar",
            "types": {Action, Attack, _Potion, _Cantrip, _Curser, _ExtraCost},
        },
        {"name": "Golem", "types": {Action, _Potion, _ExtraCost, _Village}},
        {"name": "Herbalist", "types": {Action, _Buys, _Cost2, _DeckSeeder, _Money1}},
        {
            "name": "Philosopher's Stone",
            "types": {Treasure, _Potion, _ExtraCost, _Payload},
        },
        {
            "name": "Possession",
            "types": {Action, _Potion, _Buys, _Draw5, _ExtraCost, _Terminal},
        },
        {
            "name": "Scrying Pool",
            "types": {
                Action,
                Attack,
                _Potion,
                _BadSifter,
                _Chainer,
                _Drawload,
                _ExtraCost,
                _Sifter,
            },
        },
        {
            "name": "Transmute",
            "types": {
                Action,
                _Potion,
                _ExtraCost,
                _FutureMoney2,
                _MultiTypeLove,
                _Terminal,
                _Trasher,
                _Victory,
            },
        },
        {
            "name": "University",
            "types": {Action, _Potion, _ExtraCost, _Gainer5, _Village},
        },
        {"name": "Vineyard", "types": {Victory, _Potion, _ExtraCost}},
    ]
)

Prosperity = Set("Prosperity")
Prosperity.AddCards(
    [
        {"name": "Anvil", "types": {Treasure, _Cost3, _Discard, _Gainer4, _Money1}},
        {"name": "Bank", "types": {Treasure, _Cost7, _Payload}},
        {
            "name": "Bishop",
            "types": {Action, _Cost4, _Interactive, _Money1, _Terminal, _Thinner},
        },
        {
            "name": "Charlatan",
            "types": {Action, Attack, _Cost5, _Curser, _Money3, _Terminal},
        },
        {
            "name": "City",
            "types": {Action, _Buys, _Cost5, _Draw2, _Empty, _Peddler, _Village},
        },
        {
            "name": "Clerk",
            "types": {
                Action,
                Reaction,
                Attack,
                _Cost4,
                _DeckSeeder,
                _FreeAction,
                _Money2,
                _Terminal,
            },
        },
        {"name": "Collection", "types": {Treasure, _Buys, _Cost5, _Money2, _Victory}},
        {
            "name": "Crystal Ball",
            "types": {Treasure, _Cost5, _Discard, _Money1, _Thinner},
        },
        {
            "name": "Expand",
            "types": {
                Action,
                _Cost7,
                _Remodeler,
                _Terminal,
                _Trasher,
            },
        },
        {"name": "Forge", "types": {Action, _Cost7, _Terminal, _Thinner}},
        {"name": "Grand Market", "types": {Action, _Buys, _Cost6, _Money2, _Peddler}},
        {"name": "Hoard", "types": {Treasure, _Cost6, _Money2, _Payload}},
        {
            "name": "Investment",
            "types": {Treasure, _Cost4, _Money1, _Thinner, _Victory},
        },
        {"name": "King's Court", "types": {Action, _Cost7, _Splitter}},
        {"name": "Magnate", "types": {Action, _Cost5, _Drawload, _Terminal}},
        {"name": "Mint", "types": {Action, _Cost5, _FutureMoney2, _Terminal, _Thinner}},
        {"name": "Monument", "types": {Action, _Cost4, _Money2, _Terminal, _Victory}},
        {"name": "Peddler", "types": {Action, _Cost8, _CostVaries, _Peddler}},
        {"name": "Quarry", "types": {Treasure, _Cost4, _CostReducer, _Money1}},
        {
            "name": "Rabble",
            "types": {Action, Attack, _BadSifter, _Cost5, _Draw3, _Terminal},
        },
        {
            "name": "Tiara",
            "types": {Treasure, _Buys, _Cost4, _CostReducer, _SpeedUp, _Splitter},
        },
        {"name": "War Chest", "types": {Treasure, _Cost5, _Gainer5}},
        {
            "name": "Vault",
            "types": {Action, _Cost5, _Draw2, _Discard, _Payload, _Terminal},
        },
        {
            "name": "Watchtower",
            "types": {Action, Reaction, _Cost3, _Filler, _SpeedUp, _Terminal, _Thinner},
        },
        {"name": "Worker's Village", "types": {Action, _Buys, _Cost4, _Village}},
    ]
)
Prosperity.firstEdition = [
    {"name": "Contraband", "types": {Treasure, _Buys, _Cost5, _Money3}},
    {"name": "Counting House", "types": {Action, _Cost5, _Payload, _Terminal}},
    {
        "name": "Goons",
        "types": {
            Action,
            Attack,
            _Buys,
            _Cost6,
            _Discard,
            _Money2,
            _Terminal,
            _Victory,
        },
    },
    {"name": "Loan", "types": {Treasure, _Cost3, _Discard, _Money1, _Thinner}},
    {
        "name": "Mountebank",
        "types": {Action, Attack, _Cost5, _Curser, _Junker, _Money2},
    },
    {"name": "Royal Seal", "types": {Treasure, _Cost5, _Money2, _SpeedUp}},
    {"name": "Talisman", "types": {Treasure, _Cost4, _Gainer4, _Money1}},
    {"name": "Trade Route", "types": {Action, _Buys, _Cost3, _Payload, _Thinner}},
    {"name": "Venture", "types": {Treasure, _Cost5, _Money1, _SpeedUp}},
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
        {"name": "Fairgrounds", "types": {Victory, _Cost6, _NamesMatter}},
        {
            "name": "Fortune Teller",
            "types": {Action, Attack, _BadSifter, _Cost3, _Discard, _Money2, _Terminal},
        },
        {"name": "Hamlet", "types": {Action, _Buys, _Cost2, _Discard, _Village}},
        {"name": "Horn of Plenty", "types": {Treasure, _Cost5, _NamesMatter, _Trasher}},
        {
            "name": "Menagerie",
            "types": {Action, _Cantrip, _Cost3, _Draw2, _NamesMatter},
        },
        {"name": "Farming Village", "types": {Action, _Cost4, _Sifter, _Village}},
        {
            "name": "Harvest",
            "types": {Action, _Cost5, _Discard, _Money1, _NamesMatter, _Terminal},
        },
        {
            "name": "Horse Traders",
            "types": {
                Action,
                Reaction,
                _AttackResponse,
                _Buys,
                _Cost4,
                _Discard,
                _Draw2,
                _Money3,
                _Terminal,
            },
        },
        {"name": "Hunting Party", "types": {Action, _Cantrip, _Cost5, _Draw2}},
        {"name": "Jester", "types": {Action, Attack, _Cost5, _Curser, _Money2}},
        {"name": "Remake", "types": {Action, _Cost4, _Remodeler, _Terminal, _Trasher}},
        {"name": "Tournament", "types": {Action, _Cost4, _Interactive, _Peddler}},
        {
            "name": "Young Witch",
            "types": {Action, Attack, _Cost4, _Curser, _Kingdom, _Sifter, _Terminal},
        },
    ]
)

Hinterlands = Set("Hinterlands")
Hinterlands.AddCards(
    [
        {
            "name": "Berserker",
            "types": {Action, Attack, _Discard, _FreeAction, _Gainer4, _Terminal},
        },
        {"name": "Border Village", "types": {Action, _Cost6, _Gainer5, _Village}},
        {"name": "Cartographer", "types": {Action, _Cantrip, _Discard, _Sifter}},
        {
            "name": "Cauldron",
            "types": {Treasure, Attack, _Buys, _Cost5, _Curser, _Money2},
        },
        {"name": "Crossroads", "types": {Action, _Cost2, _Drawload, _Village}},
        {"name": "Develop", "types": {Action, _Cost3, _Remodeler, _Terminal, _Twin}},
        {"name": "Farmland", "types": {Victory, _Cost6, _Remodeler, _Trasher}},
        {
            "name": "Fool's Gold",
            "types": {
                Treasure,
                Reaction,
                _Cost2,
                _DeckSeeder,
                _FutureMoney2,
                _Money1,
                _Money4,
                _Trasher,
                _TrashGainer,
            },
        },
        {
            "name": "Guard Dog",
            "types": {
                Action,
                Reaction,
                _AttackResponse,
                _Cost3,
                _Draw2,
                _Draw4,
                _Terminal,
            },
        },
        {"name": "Haggler", "types": {Action, _Cost5, _Money2, _Terminal}},
        {
            "name": "Tunnel",
            "types": {
                Victory,
                Reaction,
                _Cost3,
                _DiscardResponse,
                _Remodeler,
                _Trasher,
            },
        },
        {"name": "Highway", "types": {Action, _Cantrip, _Cost5, _CostReducer}},
        {"name": "Inn", "types": {Action, _Cost5, _DeckSeeder, _Sifter, _Village}},
        {
            "name": "Jack of All Trades",
            "types": {
                Action,
                _Cost4,
                _Discard,
                _Filler,
                _FutureMoney1,
                _Sifter,
                _Terminal,
                _Thinner,
            },
        },
        {
            "name": "Margrave",
            "types": {
                Action,
                Attack,
                _Buys,
                _Cost5,
                _Discard,
                _Draw3,
                _Interactive,
                _Terminal,
            },
        },
        {
            "name": "Nomads",
            "types": {Action, _Buys, _Cost4, _Money2, _Money4, _Terminal},
        },
        {"name": "Oasis", "types": {Action, _Cost3, _Discard, _Peddler}},
        {"name": "Scheme", "types": {Action, _Cantrip, _Cost3, _DeckSeeder, _Twin}},
        # since this is terminal, I'm calling it a Money3
        {
            "name": "Souk",
            "types": {Action, _Buys, _Cost5, _Money3, _Terminal, _Thinner},
        },
        {
            "name": "Spice Merchant",
            "types": {Action, _Buys, _Choice, _Cost4, _Draw2, _Money2},
        },
        {"name": "Stables", "types": {Action, _Cantrip, _Cost5, _Discard, _Draw3}},
        {
            "name": "Trader",
            "types": {
                Action,
                Reaction,
                _Cost4,
                _FutureMoney1,
                _Terminal,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Trail",
            "types": {Action, Reaction, _Cost4, _FreeAction},
        },
        {
            "name": "Tunnel",
            "types": {Victory, Reaction, _Cost3, _Discard, _FutureMoney2},
        },
        {
            "name": "Weaver",
            "types": {
                Action,
                Reaction,
                _DiscardResponse,
                _Cost4,
                _FreeAction,
                _FutureMoney2,
                _Gainer4,
                _Terminal,
            },
        },
        {
            "name": "Wheelwright",
            "types": {Action, _Cantrip, _Cost5, _Discard, _Gainer5},
        },
        {
            "name": "Witch's Hut",
            "types": {Action, Attack, _Cost5, _Curser, _Discard, _Sifter, _Terminal},
        },
    ]
)
Hinterlands.firstEdition = [
    {"name": "Cache", "types": {Treasure, _Cost5, _Money3}},
    {"name": "Duchess", "types": {Action, _Cost2, _Interactive, _Money2, _Sifter}},
    {
        "name": "Embassy",
        "types": {Action, _Cost5, _Draw2, _Interactive, _Sifter, _Terminal},
    },
    {"name": "Ill-gotten Gains", "types": {Treasure, _Cost5, _Curser, _Money2}},
    {"name": "Mandarin", "types": {Action, _Cost5, _DeckSeeder, _Money3, _Terminal}},
    {
        "name": "Noble Brigand",
        "types": {Action, Attack, _BadThinner, _Cost4, _FreeAction, _Money1},
    },
    {"name": "Nomad Camp", "types": {Action, _Buys, _Cost4, _DeckSeeder, _Money2}},
    {
        "name": "Oracle",
        "types": {Action, Attack, _BadSifter, _Cost3, _Draw2, _Sifter, _Terminal},
    },
    {"name": "Silk Road", "types": {Victory, _Cost4}},
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
        {"name": "Altar", "types": {Action, _Cost6, _Gainer5, _Trasher, _Terminal}},
        {"name": "Armory", "types": {Action, _Cost4, _DeckSeeder, _Gainer4, _Terminal}},
        {
            "name": "Beggar",
            "types": {
                Action,
                Reaction,
                _AttackResponse,
                _Cost2,
                _DeckSeeder,
                _FutureMoney2,
                _Money3,
                _Terminal,
            },
        },
        {"name": "Band of Misfits", "types": {Action, Command, _Command4, _Cost5}},
        {"name": "Bandit Camp", "types": {Action, _Cost5, _FutureMoney2, _Village}},
        {
            "name": "Catacombs",
            "types": {Action, _Cost5, _Draw3, _Sifter, _TrashGainer, _Terminal},
        },
        {
            "name": "Count",
            "types": {
                Action,
                _Cost5,
                _Choice,
                _DeckSeeder,
                _Discard,
                _Junker,
                _Money3,
                _Terminal,
                _Thinner,
                _Victory,
            },
        },
        {
            "name": "Counterfeit",
            "types": {Treasure, _Buys, _Cost5, _Money1, _Splitter, _Thinner},
        },
        {
            "name": "Cultist",
            "types": {Action, Attack, _Cost5, _Draw2, _Terminal, _TrashGainer},
        },
        {
            "name": "Death Cart",
            "types": {Action, Looter, _Cost4, _Junker, _Money5, _Terminal, _Thinner},
        },
        {"name": "Feodum", "types": {Victory, _Cost4, _TrashGainer}},
        {
            "name": "Forager",
            "types": {Action, _Buys, _Chainer, _Cost3, _Payload, _Thinner},
        },
        {"name": "Fortress", "types": {Action, _Cost4, _TrashGainer, _Village}},
        {
            "name": "Hermit",
            "types": {
                Action,
                _Cost3,
                _Drawload,
                _Gainer3,
                _Terminal,
                _Trasher,
                _Twin,
                _Village,
            },
        },
        {
            "name": "Graverobber",
            "types": {Action, _Cost5, _Remodeler, _Terminal, _Trasher, _TrashGainer},
        },
        {
            "name": "Hunting Grounds",
            "types": {Action, _Cost6, _Draw4, _Terminal, _TrashGainer, _Victory},
        },
        {
            "name": "Ironmonger",
            "types": {
                Action,
                _Cost4,
                _DeckGuesser,
                _Discard,
                _Draw2,
                _Money1,
                _Village,
            },
        },
        {"name": "Junk Dealer", "types": {Action, _Cost5, _Peddler, _Thinner}},
        {
            "name": "Knights",
            "types": {
                Action,
                Attack,
                Knight,
                _BadThinner,
                _Buys,
                _Cantrip,
                _Cost4,
                _Cost5,
                _Discard,
                _Draw2,
                _FutureMoney2,
                _Gainer3,
                _Money2,
                _MultiType,
                _SplitPile,
                _Terminal,
                _Thinner,
                _TrashGainer,
                _Village,
            },
        },
        {
            "name": "Marauder",
            "types": {
                Action,
                Attack,
                Looter,
                _Cost4,
                _FutureMoney2,
                _Junker,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Market Square",
            "types": {
                Action,
                Reaction,
                _Buys,
                _Cantrip,
                _Cost3,
                _FutureMoney2,
                _TrashGainer,
            },
        },
        {"name": "Mystic", "types": {Action, _Chainer, _Cost5, _DeckGuesser, _Money2}},
        {
            "name": "Pillage",
            "types": {
                Action,
                Attack,
                _Cost5,
                _Discard,
                _FutureMoney4,
                _Terminal,
                _Trasher,
            },
        },
        {"name": "Poor House", "types": {Action, _Cost1, _Money4, _Terminal}},
        {
            "name": "Procession",
            "types": {Action, _Cost4, _Splitter, _Remodeler, _Terminal, _Trasher},
        },
        {
            "name": "Rats",
            "types": {Action, _Cantrip, _Cost4, _Trasher, _TrashGainer},
        },
        {
            "name": "Rebuild",
            "types": {Action, _Cantrip, _Cost5, _Remodeler, _Trasher, _Victory},
        },
        {
            "name": "Rogue",
            "types": {
                Action,
                Attack,
                _BadThinner,
                _Cost5,
                _Money2,
                _Terminal,
                _TrashGainer,
            },
        },
        {"name": "Sage", "types": {Action, _Cantrip, _Cost3, _Sifter}},
        {
            "name": "Scavenger",
            "types": {Action, _Cost4, _Money2, _DeckSeeder, _SpeedUp, _Terminal},
        },
        {
            "name": "Squire",
            "types": {
                Action,
                _AttackResponse,
                _Buys,
                _Choice,
                _Cost2,
                _FutureMoney1,
                _Money1,
                _TrashGainer,
                _Village,
            },
        },
        {
            "name": "Storeroom",
            "types": {
                Action,
                _Buys,
                _Cost3,
                _Discard,
                _Drawload,
                _Payload,
                _Sifter,
                _Terminal,
                _Twin,
            },
        },
        {
            "name": "Urchin",
            "types": {
                Action,
                Attack,
                _Cantrip,
                _Cost3,
                _Discard,
                _Draw2,
                _Money2,
                _Thinner,
                _Terminal,
                _Twin,
            },
        },
        {"name": "Vagrant", "types": {Action, _Cantrip, _Cost2, _Sifter}},
        {"name": "Wandering Minstrel", "types": {Action, _Cost4, _Sifter, _Village}},
    ]
)

Guilds = Set("Guilds")
Guilds.AddCards(
    [
        {
            "name": "Advisor",
            "types": {Action, _BadSifter, _Cantrip, _Cost4, _Discard, _Draw2},
        },
        {"name": "Baker", "types": {Action, _Cantrip, _FutureMoney2, _Cost5}},
        {
            "name": "Candlestick Maker",
            "types": {Action, _Buys, _Chainer, _FutureMoney2, _Cost2},
        },
        {
            "name": "Butcher",
            "types": {Action, _Cost5, _FutureMoney2, _Remodeler, _Terminal, _Trasher},
        },
        {"name": "Doctor", "types": {Action, _Cost3, _Overpay, _Terminal, _Thinner}},
        {
            "name": "Herald",
            "types": {Action, _Cantrip, _Cost4, _DeckGuesser, _DeckSeeder, _Overpay},
        },
        {
            "name": "Journeyman",
            "types": {Action, _Cost5, _DeckGuesser, _Draw3, _Sifter, _Terminal},
        },
        {"name": "Masterpiece", "types": {Treasure, _Cost3, _Money1, _Overpay}},
        {
            "name": "Merchant Guild",
            "types": {Action, _Buys, _Cost5, _Money1, _Payload, _Terminal},
        },
        {"name": "Plaza", "types": {Action, _FutureMoney2, _Cost4, _Discard, _Village}},
        {
            "name": "Stonemason",
            "types": {Action, _Cost2, _Overpay, _Remodeler, _Trasher},
        },
        {
            "name": "Soothsayer",
            "types": {Action, Attack, _Cost5, _Curser, _Interactive, _Terminal},
        },
        {
            "name": "Taxman",
            "types": {
                Action,
                Attack,
                _BadSifter,
                _Cost4,
                _Discard,
                _Remodeler,
                _Terminal,
                _Trasher,
            },
        },
    ]
)

Adventures = Set("Adventures")
Adventures.AddCards(
    [
        # Kingdom
        {
            "name": "Amulet",
            "types": {
                Action,
                Duration,
                _Choice,
                _Cost3,
                _FutureMoney1,
                _FutureMoney2,
                _Money1,
                _Money2,
                _Thinner,
            },
        },
        {
            "name": "Artificer",
            "types": {Action, _Cost5, _Discard, _Peddler, _Remodeler},
        },
        {
            "name": "Bridge Troll",
            "types": {Action, Duration, Attack, _Buys, _Cost5, _CostReducer, _Terminal},
        },
        {
            "name": "Caravan Guard",
            "types": {
                Action,
                Duration,
                Reaction,
                _AttackResponse,
                _Cantrip,
                _Cost3,
                _FutureMoney1,
                _MultiType,
            },
        },
        {
            "name": "Coin of the Realm",
            "types": {Treasure, Reserve, _Cost2, _Money1, _Village},
        },
        {
            "name": "Distant Lands",
            "types": {Action, Victory, Reserve, _Cost5, _MultiType},
        },
        {"name": "Dungeon", "types": {Action, Duration, _Chainer, _Cost3, _Sifter}},
        {
            "name": "Gear",
            "types": {Action, Duration, _Cost3, _DeckSeeder, _Draw2, _Terminal, _Twin},
        },
        {"name": "Duplicate", "types": {Action, Reserve, _Cost4, _Gainer6, _Terminal}},
        {
            "name": "Giant",
            "types": {
                Action,
                Attack,
                _BadThinner,
                _Cost5,
                _Curser,
                _Discard,
                _Money1,
                _Money5,
                _Terminal,
            },
        },
        {
            "name": "Guide",
            "types": {Action, Reserve, _Cantrip, _Cost3, _Discard, _Draw5},
        },
        {
            "name": "Haunted Woods",
            "types": {
                Action,
                Duration,
                Attack,
                _BadSifter,
                _Cost5,
                _Draw3,
                _MultiType,
                _Terminal,
            },
        },
        {"name": "Hireling", "types": {Action, Duration, _Cost6, _Terminal}},
        {
            "name": "Lost City",
            "types": {Action, _Cost5, _Draw2, _Interactive, _Village},
        },
        {"name": "Magpie", "types": {Action, _Cantrip, _Cost4, _DeckGuesser}},
        {
            "name": "Messenger",
            "types": {Action, _Buys, _Cost4, _Gainer4, _Money2, _SpeedUp, _Terminal},
        },
        {"name": "Miser", "types": {Action, _Cost4, _Payload, _Terminal, _Thinner}},
        {
            "name": "Page",
            "types": {
                Action,
                Traveller,
                _BadSifter,
                _BadThinner,
                _Cantrip,
                _Cost2,
                _Draw2,
                _FutureMoney1,
                _FutureMoney2,
                _Money1,
                _Money2,
                _SplitPile,
                _Village,
            },
        },
        {
            "name": "Peasant",
            "types": {
                Action,
                Traveller,
                _Buys,
                _Cost2,
                _Discard,
                _Draw2,
                _Money1,
                _Money2,
                _Payload,
                _Splitter,
                _Terminal,
            },
        },
        {"name": "Port", "types": {Action, _Cost4, _Village}},
        {"name": "Ranger", "types": {Action, _Buys, _Cost4, _Draw5, _Terminal}},
        {"name": "Ratcatcher", "types": {Action, Reserve, _Cantrip, _Cost2, _Thinner}},
        {"name": "Raze", "types": {Action, _Cantrip, _Cost2, _Sifter, _Thinner}},
        {"name": "Relic", "types": {Treasure, Attack, _Cost5, _Money2}},
        {
            "name": "Royal Carriage",
            "types": {Action, Reserve, _Chainer, _Cost5, _Splitter},
        },
        {"name": "Storyteller", "types": {Action, _Cantrip, _Cost5, _Drawload}},
        {
            "name": "Swamp Hag",
            "types": {Action, Duration, Attack, _Cost5, _Curser, _Money3, _Terminal},
        },
        {
            "name": "Transmogrify",
            "types": {Action, Reserve, _Chainer, _Cost4, _Remodeler, _Trasher},
        },
        {"name": "Treasure Trove", "types": {Treasure, _Cost5, _FutureMoney2, _Junker}},
        {"name": "Wine Merchant", "types": {Action, _Buys, _Cost5, _Money4, _Terminal}},
        # Landscapes
        {"name": "Alms", "types": {Event, _Cost0, _Gainer4}},
        {"name": "Ball", "types": {Event, _Cost5, _Gainer4}},
        {"name": "Bonfire", "types": {Event, _Cost3, _Thinner}},
        {"name": "Borrow", "types": {Event, _Cost0, _FreeEvent, _Money1}},
        {"name": "Expedition", "types": {Event, _Cost3, _Draw2}},
        {"name": "Ferry", "types": {Event, _Cost3, _CostReducer}},
        {"name": "Inheritance", "types": {Event, _Command4, _Cost7}},
        {"name": "Lost Arts", "types": {Event, _Chainer, _Cost6}},
        {"name": "Mission", "types": {Event, _Cost4, _Draw5}},
        {"name": "Quest", "types": {Event, _Cost0, _Discard, _FutureMoney2}},
        {"name": "Pathfinding", "types": {Event, _Cost8, _Drawload}},
        {"name": "Pilgrimage", "types": {Event, _Cost4, _Gainer6}},
        {"name": "Plan", "types": {Event, _Cost3, _Thinner}},
        {"name": "Raid", "types": {Event, _Cost5, _Payload}},
        {"name": "Save", "types": {Event, _Cost1, _DeckSeeder, _FreeEvent}},
        {"name": "Scouting Party", "types": {Event, _Cost2, _FreeEvent, _Sifter}},
        {"name": "Seaway", "types": {Event, _Buys, _Cost5, _Gainer4}},
        {"name": "Training", "types": {Event, _Cost6, _FutureMoney1}},
        {"name": "Travelling Fair", "types": {Event, _Buys, _Cost2, _DeckSeeder}},
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
_PotionCards = Alchemy.potionCards

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

    # Check for _Potions
    include_Potions = Alchemy.potionCards & resultSet

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

    if include_Potions:
        additionalCards.add("Alchemy: _Potions")
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
