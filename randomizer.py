import math
import random


AllSets = {}


class AdvTag(object):
    def __init__(self, card, bonusToTypes=[], wantsTypes=[], badTypes=[]):
        self.name = card.name
        self.bonusToTypes = bonusToTypes
        self.wantsTypes = wantsTypes
        self.badTypes = badTypes


class CardType(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


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
    def __init__(self, name, types=None, cardSet=None, advTags=None):
        self.name = name
        self.set = cardSet

        if isinstance(types, set):
            self.types = types
        elif types is None:
            self.types = set()
        else:
            self.types = set(types)

        if isinstance(advTags, set):
            self.advTags = advTags
        elif advTags is None:
            self.advTags = set()
        else:
            self.advTags = set(advTags)

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
# Donald X Landmarky Things
Event = CardType("Event")
Landmark = CardType("Landmark")
Project = CardType("Project")
Way = CardType("Way")
Ally = CardType("Ally")
Trait = CardType("Trait")
# Donald X types
# Potion isn't written on the card
Action = CardType("Action")
Attack = CardType("Attack")
Augur = CardType("Augur")
Castle = CardType("Castle")
Castle = CardType("Castle")
Clash = CardType("Clash")
Command = CardType("Command")
Doom = CardType("Doom")
Duration = CardType("Duration")
Fate = CardType("Fate")
Fort = CardType("Fort")
Gathering = CardType("Gathering")
Heirloom = CardType("Heirloom")
Knight = CardType("Knight")
Liaison = CardType("Liaison")
Looter = CardType("Looter")
Night = CardType("Night")
Potion = CardType("Potion")
Reaction = CardType("Reaction")
Reserve = CardType("Reserve")
Townsfolk = CardType("Townsfolk")
Traveller = CardType("Traveller")
Treasure = CardType("Treasure")
Victory = CardType("Victory")
Wizard = CardType("Wizard")


# for enhanced randomizer
# Define card types
# Donald X Landmarky Things
Event = CardType("Event")
Landmark = CardType("Landmark")
Project = CardType("Project")
Way = CardType("Way")
Ally = CardType("Ally")
Trait = CardType("Trait")
# Donald X types
# Potion isn't written on the card
Action = CardType("Action")
Attack = CardType("Attack")
Augur = CardType("Augur")
Castle = CardType("Castle")
Castle = CardType("Castle")
Clash = CardType("Clash")
Command = CardType("Command")
Doom = CardType("Doom")
Duration = CardType("Duration")
Fate = CardType("Fate")
Fort = CardType("Fort")
Gathering = CardType("Gathering")
Heirloom = CardType("Heirloom")
Knight = CardType("Knight")
Liaison = CardType("Liaison")
Looter = CardType("Looter")
Night = CardType("Night")
Potion = CardType("Potion")
Reaction = CardType("Reaction")
Reserve = CardType("Reserve")
Townsfolk = CardType("Townsfolk")
Traveller = CardType("Traveller")
Treasure = CardType("Treasure")
Victory = CardType("Victory")
Wizard = CardType("Wizard")

_AttackResponse = AdvTag(
    "_AttackResponse", wantsTypes=[Attack]
)  # allows you to respond to attacks. Wants for Attacks
_BadSifter = AdvTag("_BadSifter")  # attacks by messing up your deck
_BadThinner = AdvTag("_BadThinner")  # attacks by trashing good things
_BottomSeeder = AdvTag("_BottomSeeder")  # puts cards on the bottom of your deck.
_Buys = AdvTag("_Buys")  # allow you to buy more cards in a turn.
_Cantrip = AdvTag(
    "_Cantrip"
)  # card draws and chains, which essentially makes it a free bonus card
_Chainer = AdvTag("_Chainer")  # allows you to play another action after it is done
_Choice = AdvTag("_Choice")  # gives you a set of choices
_Cost0 = AdvTag("_Cost0")  # card costs 0
_Cost1 = AdvTag("_Cost1")  # card costs 1
_Cost2 = AdvTag("_Cost2")  # card costs 2
_Cost2Response = AdvTag(
    "_Cost2Response", wantsTypes=[_Cost2]
)  # Wants cards that cost 2
_Cost3 = AdvTag("_Cost3")  # card costs 3
_Cost4 = AdvTag("_Cost4")  # card costs 4
_Command4 = AdvTag(
    "_Command4", [_Cost4]
)  # allows you to play cards costing up to 4. Synnergizes with _Cost4.
_Cost5 = AdvTag("_Cost5")  # card costs 5
_Command5 = AdvTag(
    "_Command5", [_Cost5]
)  # allows you to play cards costing up to 5. Synnergizes with _Cost5.
_Cost6 = AdvTag("_Cost6")  # card costs 6
_Cost7 = AdvTag("_Cost7")  # card costs 7
_Cost8 = AdvTag("_Cost8")  # card costs 8
_Cost10 = AdvTag("_Cost10")  # card costs 10
_Cost14 = AdvTag("_Cost14")  # card costs 14
_Cost16 = AdvTag("_Cost16")  # card costs 16
_CostReducer = AdvTag(
    "_CostReducer", [_Buys]
)  # reduces the cost of cards. synnergizes with _Buys and _Gainer
_CostVaries = AdvTag("_CostVaries")  # Gets cheaper or more expensive.
_Curser = AdvTag("_Curser")  # gives other players curses
_Debt = AdvTag("_Debt")  # using this card gives you debt
_DeckSeeder = AdvTag(
    "_DeckSeeder",
)  # allows you to manipulate your deck; synnergizes with _DeckGuesser
_DeckGuesser = AdvTag(
    "_DeckGuesser", bonusToTypes=["_DeckSeeder"]
)  # allows you to guess cards from the top of your deck. wants for _DeckSeeder
_Discard = AdvTag("_Discard")  # discards cards because sometimes you want to do that
_DiscardResponse = AdvTag(
    "_DiscardResponse", wantsTypes=["_Discard"]
)  # Reaction triggered by discards other than cleanup. Wants _Discard
_Downgrader = AdvTag("_Downgrader")  # attack card that does upgrades in reverse
_Draw2 = AdvTag("_Draw2")  # draws 2 cards
_Draw3 = AdvTag("_Draw3")  # draws 3 cards
_Draw4 = AdvTag("_Draw4")  # draws 4 cards
_Draw5 = AdvTag("_Draw5")  # draws 5 cards
_Draw6 = AdvTag("_Draw6")  # draws 6 cards
_Draw7 = AdvTag("_Draw7")  # draws 7 cards
_Drawload = AdvTag("_Drawload")  # draws potentially infinite numbers of cards
_Empty = AdvTag("_Empty")  # cares about empty supply piles
_ExtraCost = AdvTag(
    "_ExtraCost"
)  # has an extra cost, preventing gainers from gaining it. Bad synnergy with gainers
_Filler = AdvTag(
    "_Filler", [_Discard]
)  # fills hand up to a certain point; synnergizes with _Discard
_FreeAction = AdvTag(
    "_FreeAction"
)  # card that can play itself without expending actions
_FreeEvent = AdvTag(
    "_FreeEvent"
)  # event that gives you one buy, and therefore essentially costs no buy.
_FutureAction = AdvTag(
    "_FutureAction"
)  # gives a bonus action at the start of next turn
_FutureMoney1 = AdvTag(
    "_FutureMoney1"
)  # gives you future money, such as by giving 1 coffer or gaining a silver
_FutureMoney2 = AdvTag(
    "_FutureMoney2"
)  # gives you future money, such as by giving 2 coffers or gaining a gold
_FutureMoney3 = AdvTag(
    "_FutureMoney3"
)  # gives you future money, such as by giving 3 coffers or gaining a gold and a silver
_FutureMoney4 = AdvTag(
    "_FutureMoney4"
)  # gives you future money, such as by gaining 2 spoils
_FutureMoney6 = AdvTag(
    "_FutureMoney6"
)  # gives you future money, such as by gaining 3 golds
_Gainer3 = AdvTag(
    "_Gainer3", bonusToTypes=[_Cost3, _CostReducer], badTypes=["_ExtraCost"]
)  # allows you to gain cards from the supply costing up to 3; synnergizes with _CostReducer, _Cost3
_Gainer4 = AdvTag(
    "_Gainer4", bonusToTypes=[_Cost4, _CostReducer], badTypes=["_ExtraCost"]
)  # allows you to gain cards from the supply costing up to 4; synnergizes with _CostReducer, _Cost4
_Gainer5 = AdvTag(
    "_Gainer5", bonusToTypes=[_Cost5, _CostReducer], badTypes=["_ExtraCost"]
)  # allows you to gain cards from the supply costing up to 5; synnergizes with _CostReducer, _Cost5
_Gainer6 = AdvTag(
    "_Gainer6", bonusToTypes=[_Cost6, _CostReducer], badTypes=["_ExtraCost"]
)  # allows you to gain cards from the supply costing up to 6; synnergizes with _CostReducer, _Cost6
_Kingdom = AdvTag("_Kingdom")  # Adds cards to the kingdom
_Interactive = AdvTag(
    "_Interactive"
)  # does something to other players that is not an attack
_Junker = AdvTag("_Junker")  # attacker gives opponents bad cards
_Money1 = AdvTag("_Money1")  # gives +1 Money
_Money2 = AdvTag("_Money2")  # gives +2 Money
_Money3 = AdvTag("_Money3")  # gives +3 Money
_Money4 = AdvTag("_Money4")  # gives +4 Money
_Money5 = AdvTag("_Money5")  # gives +5 Money
_Money6 = AdvTag("_Money6")  # gives +6 Money
_MultiType = AdvTag("_MultiType")  # has more than two types
_MultiTypeLove = AdvTag(
    "_MultiTypeLove", wantsTypes=[_MultiType]
)  # Wants cards with more than two types
_Payload = AdvTag("_Payload")  # a card that adds variable, potentially infinite money.
_Overpay = AdvTag(
    "_Overpay", [_FutureMoney2, _Money3, _Money4, _Money5, _Money6, _Payload]
)  # Allows you to pay more for more functionality. Synnergizes with _Money3, _Money4, _Money5, _Payload.
_Peddler = AdvTag(
    "_Peddler"
)  # cantrip that give +1 Money; seperate class for randomizer reasons
_Random = AdvTag("_Random")  # a card with seemly random effects (as opposed to _Choice)
_Reveal = AdvTag(
    "_Reveal"
)  # a card that makes you reveal other cards, explicitly using the word reveal
_RevealResponse = AdvTag(
    "_RevealResponse", [Doom, _Reveal]
)  # a card that reacts to being revealed, Wants _Reveal or Doom
_Saver = AdvTag(
    "_Saver"
)  # puts cards from this hand into future hands, without discards or draws
_ShuffleIn = AdvTag("_ShuffleIn")  # shuffles cards into other piles
_Sifter = AdvTag(
    "_Sifter", bonusToTypes=[_Discard]
)  # draws and discards cards to improve future hands
_SpeedUp = AdvTag("_SpeedUp")  # allows you to get gained cards into play faster
_SplitPile = AdvTag("_SplitPile")  # There's more than one named thing in here!
_NamesMatter = AdvTag(
    "_NamesMatter", [Looter, _FutureMoney2, _Kingdom, _SplitPile]
)  # Wants a lot of different names in the game. Synnergizes with Looter, _SplitPile, etc
_Terminal = AdvTag(
    "_Terminal"
)  # doesn't allow more actions to be played. synnergizes with _Splitter and _Village
_Splitter = AdvTag(
    "_Splitter", bonusToTypes=[_Terminal]
)  # allows you to play cards multiple times.
_Thinner = AdvTag(
    "_Thinner"
)  # Puts cards into the trash and leaves you with a smaller deck
_Trasher = AdvTag("_Trasher")  # Puts cards into the trash, but doesn't thin your deck
_TrashBenefit = AdvTag("_TrashBenefit")  # Wants to be trashed
_TrashGainer = AdvTag(
    "_TrashGainer", wantsTypes=[_Trasher]
)  # Gets cards out of the trash or gains cards in response to trashing. Wants for _Trasher
_Twin = AdvTag(
    "_Twin"
)  # Donald X's secret type that is a good idea to buy 2 of on turn 1
_Remodeler = AdvTag(
    "_Remodeler"
)  # allows you to trash cards and replace them with better cards
_Victory = AdvTag("_Victory")  # gains you victory cards or points
_Village = AdvTag(
    "_Village", bonusToTypes=[_Terminal]
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
                _Reveal,
                _Terminal,
            },
        },
        {
            "name": "Bureaucrat",
            "types": {
                Action,
                Attack,
                _Cost4,
                _DeckSeeder,
                _FutureMoney1,
                _Reveal,
                _Terminal,
            },
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
    {"name": "Adventurer", "types": {Action, _Cost6, _Reveal, _Sifter, _Terminal}},
    {
        "name": "Chancellor",
        "types": {Action, _Cost3, _Money2, _SpeedUp, _Terminal},
    },
    {"name": "Feast", "types": {Action, _Cost4, _Gainer5, _Terminal, _Trasher}},
    {"name": "Spy", "types": {Action, Attack, _BadSifter, _Cost4, _Reveal, _Sifter}},
    {
        "name": "Thief",
        "types": {
            Action,
            Attack,
            _BadThinner,
            _Cost4,
            _FutureMoney2,
            _Reveal,
            _Terminal,
        },
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
            "types": {
                Action,
                _Choice,
                _Cost5,
                _FutureMoney2,
                _Money3,
                _MultiTypeLove,
                _Reveal,
            },
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
        {
            "name": "Patrol",
            "types": {Action, _Cost5, _Draw3, _Reveal, _Sifter, _Terminal},
        },
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
        {"name": "Shanty Town", "types": {Action, _Cost3, _Reveal, _Twin, _Village}},
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
            "types": {Action, _Cantrip, _Cost3, _DeckGuesser, _Reveal, _Twin},
        },
    ]
)
Intrigue.firstEdition = [
    {"name": "Coppersmith", "types": {Action, _Cost4, _Payload, _Terminal}},
    {"name": "Great Hall", "types": {Action, Victory, _Cantrip, _Cost3}},
    {
        "name": "Saboteur",
        "types": {
            Action,
            Attack,
            _Downgrader,
            _Cost5,
            _Reveal,
            _Terminal,
            _Trasher,
        },
    },
    {"name": "Scout", "types": {Action, _Chainer, _Cost4, _Reveal, _Sifter}},
    {
        "name": "Secret Chamber",
        "types": {Action, Reaction, _AttackResponse, _Cost2, _DeckSeeder, _Discard},
    },
    {
        "name": "Tribute",
        "types": {Action, _Choice, _Cost5, _Discard, _MultiTypeLove, _Reveal},
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
        {
            "name": "Cutpurse",
            "types": {Action, Attack, _Cost4, _Discard, _Reveal, _Money2},
        },
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
        {
            "name": "Sea Chart",
            "types": {Action, _Cantrip, _Cost3, _DeckGuesser, _Reveal, _Twin},
        },
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
        "types": {Action, Attack, _Cost3, _Junker, _Reveal, _Terminal, _Thinner},
    },
    {"name": "Embargo", "types": {Action, _Cost2, _Curser, _Money2, _Trasher}},
    {
        "name": "Explorer",
        "types": {Action, _Cost5, _FutureMoney1, _FutureMoney2, _Reveal, _Terminal},
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
            "types": {Action, _Potion, _Cantrip, _ExtraCost, _Reveal, _Sifter},
        },
        {
            "name": "Apprentice",
            "types": {Action, _Chainer, _Cost5, _Drawload, _Thinner},
        },
        {
            "name": "Familiar",
            "types": {Action, Attack, _Potion, _Cantrip, _Curser, _ExtraCost},
        },
        {"name": "Golem", "types": {Action, _Potion, _ExtraCost, _Reveal, _Village}},
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
                _Reveal,
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
            "types": {Treasure, _Cost4, _Money1, _Reveal, _Thinner, _Victory},
        },
        {"name": "King's Court", "types": {Action, _Cost7, _Splitter}},
        {"name": "Magnate", "types": {Action, _Cost5, _Drawload, _Reveal, _Terminal}},
        {"name": "Mint", "types": {Action, _Cost5, _FutureMoney2, _Terminal, _Thinner}},
        {"name": "Monument", "types": {Action, _Cost4, _Money2, _Terminal, _Victory}},
        {"name": "Peddler", "types": {Action, _Cost8, _CostVaries, _Peddler}},
        {"name": "Quarry", "types": {Treasure, _Cost4, _CostReducer, _Money1}},
        {
            "name": "Rabble",
            "types": {Action, Attack, _BadSifter, _Cost5, _Draw3, _Reveal, _Terminal},
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
            "types": {
                Action,
                Reaction,
                _Cost3,
                _Filler,
                _Reveal,
                _SpeedUp,
                _Terminal,
                _Thinner,
            },
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
    {"name": "Loan", "types": {Treasure, _Cost3, _Discard, _Money1, _Reveal, _Thinner}},
    {
        "name": "Mountebank",
        "types": {Action, Attack, _Cost5, _Curser, _Junker, _Money2},
    },
    {"name": "Royal Seal", "types": {Treasure, _Cost5, _Money2, _SpeedUp}},
    {"name": "Talisman", "types": {Treasure, _Cost4, _Gainer4, _Money1}},
    {"name": "Trade Route", "types": {Action, _Buys, _Cost3, _Payload, _Thinner}},
    {"name": "Venture", "types": {Treasure, _Cost5, _Money1, _Reveal, _SpeedUp}},
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
            "types": {
                Action,
                Attack,
                _BadSifter,
                _Cost3,
                _Discard,
                _Money2,
                _Reveal,
                _Terminal,
            },
        },
        {"name": "Hamlet", "types": {Action, _Buys, _Cost2, _Discard, _Village}},
        {"name": "Horn of Plenty", "types": {Treasure, _Cost5, _NamesMatter, _Trasher}},
        {
            "name": "Menagerie",
            "types": {Action, _Cantrip, _Cost3, _Draw2, _NamesMatter, _Reveal},
        },
        {
            "name": "Farming Village",
            "types": {Action, _Cost4, _Sifter, _Reveal, _Village},
        },
        {
            "name": "Harvest",
            "types": {
                Action,
                _Cost5,
                _Discard,
                _Money1,
                _NamesMatter,
                _Reveal,
                _Terminal,
            },
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
        {"name": "Hunting Party", "types": {Action, _Cantrip, _Cost5, _Draw2, _Reveal}},
        {"name": "Jester", "types": {Action, Attack, _Cost5, _Curser, _Money2}},
        {"name": "Remake", "types": {Action, _Cost4, _Remodeler, _Terminal, _Trasher}},
        {"name": "Tournament", "types": {Action, _Cost4, _Interactive, _Peddler}},
        {
            "name": "Young Witch",
            "types": {
                Action,
                Attack,
                _Cost4,
                _Curser,
                _Kingdom,
                _Reveal,
                _Sifter,
                _Terminal,
            },
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
        {"name": "Crossroads", "types": {Action, _Cost2, _Drawload, _Reveal, _Village}},
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
        {
            "name": "Inn",
            "types": {Action, _Cost5, _DeckSeeder, _Reveal, _Sifter, _Village},
        },
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
            "types": {
                Action,
                Attack,
                _Cost5,
                _Curser,
                _Discard,
                _Reveal,
                _Sifter,
                _Terminal,
            },
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
        "types": {Action, Attack, _BadThinner, _Cost4, _FreeAction, _Money1, _Reveal},
    },
    {"name": "Nomad Camp", "types": {Action, _Buys, _Cost4, _DeckSeeder, _Money2}},
    {
        "name": "Oracle",
        "types": {
            Action,
            Attack,
            _BadSifter,
            _Cost3,
            _Draw2,
            _Reveal,
            _Sifter,
            _Terminal,
        },
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
                _Reveal,
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
                _Reveal,
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
        {
            "name": "Mystic",
            "types": {Action, _Chainer, _Cost5, _DeckGuesser, _Reveal, _Money2},
        },
        {
            "name": "Pillage",
            "types": {
                Action,
                Attack,
                _Cost5,
                _Discard,
                _FutureMoney4,
                _Reveal,
                _Terminal,
                _Trasher,
            },
        },
        {"name": "Poor House", "types": {Action, _Cost1, _Money4, _Reveal, _Terminal}},
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
                _Reveal,
                _Terminal,
                _TrashGainer,
            },
        },
        {"name": "Sage", "types": {Action, _Cantrip, _Cost3, _Reveal, _Sifter}},
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
        {"name": "Vagrant", "types": {Action, _Cantrip, _Cost2, _Reveal, _Sifter}},
        {
            "name": "Wandering Minstrel",
            "types": {Action, _Cost4, _Reveal, _Sifter, _Village},
        },
    ]
)

Guilds = Set("Guilds")
Guilds.AddCards(
    [
        {
            "name": "Advisor",
            "types": {Action, _BadSifter, _Cantrip, _Cost4, _Discard, _Draw2, _Reveal},
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
        {
            "name": "Doctor",
            "types": {Action, _Cost3, _Overpay, _Reveal, _Terminal, _Thinner},
        },
        {
            "name": "Herald",
            "types": {
                Action,
                _Cantrip,
                _Cost4,
                _DeckGuesser,
                _DeckSeeder,
                _Overpay,
                _Reveal,
            },
        },
        {
            "name": "Journeyman",
            "types": {
                Action,
                _Cost5,
                _DeckGuesser,
                _Draw3,
                _Reveal,
                _Sifter,
                _Terminal,
            },
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
                _Reveal,
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
                _Reveal,
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
        {"name": "Magpie", "types": {Action, _Cantrip, _Cost4, _DeckGuesser, _Reveal}},
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
        {"name": "Archive", "types": {Action, Duration, _Cantrip, _Cost5, _Draw3}},
        {"name": "Capital", "types": {Treasure, _Cost5, _Buys, _Debt, _Money6}},
        {
            "name": "Castles",
            "types": {
                Action,
                Treasure,
                Victory,
                Castle,
                _CostVaries,
                _FutureMoney1,
                _Money1,
                _Payload,
                _Reveal,
                _SplitPile,
                _Trasher,
                _Victory,
            },
        },
        {
            "name": "Catapult/Rocks",
            "types": {
                Action,
                Attack,
                Treasure,
                _Cost3,
                _Cost4,
                _Curser,
                _Discard,
                _FutureMoney1,
                _Money1,
                _SplitPile,
                _Terminal,
                _Thinner,
                _TrashGainer,
                _Twin,
            },
        },
        {
            "name": "Chariot Race",
            "types": {Action, _Cantrip, _Cost3, _Money1, _Reveal, _Victory},
        },
        {
            "name": "Charm",
            "types": {Treasure, _Buys, _Choice, _Cost5, _Gainer6, _Money2},
        },
        {
            "name": "City Quarter",
            "types": {Action, _Cost8, _Debt, _Drawload, _ExtraCost, _Reveal, _Village},
        },
        {
            "name": "Encampment/Plunder",
            "types": {
                Action,
                Treasure,
                _Cost2,
                _Cost5,
                _Draw2,
                _Money2,
                _Reveal,
                _SplitPile,
                _Victory,
                _Village,
            },
        },
        {"name": "Crown", "types": {Action, Treasure, _Cost5, _Splitter, _Terminal}},
        {
            "name": "Enchantress",
            "types": {Action, Attack, Duration, _Cost3, _Draw2, _Terminal},
        },
        {
            "name": "Engineer",
            "types": {Action, _Cost4, _Debt, _ExtraCost, _Gainer4, _Trasher},
        },
        {
            "name": "Farmers' Market",
            "types": {
                Action,
                Gathering,
                _Buys,
                _Cost3,
                _Money2,
                _Terminal,
                _Twin,
                _Victory,
            },
        },
        {"name": "Forum", "types": {Action, _Buys, _Cantrip, _Cost5, _Sifter}},
        {
            "name": "Gladiator/Fortune",
            "types": {
                Action,
                Treasure,
                _Buys,
                _Cost3,
                _Cost16,
                _Debt,
                _ExtraCost,
                _Money3,
                _Payload,
                _Reveal,
                _SplitPile,
                _Terminal,
                _Twin,
                _Trasher,
            },
        },
        {"name": "Groundskeeper", "types": {Action, _Cantrip, _Cost5, _Victory}},
        {
            "name": "Legionary",
            "types": {Action, Attack, _Cost5, _Discard, _Money3, _Terminal},
        },
        {
            "name": "Overlord",
            "types": {Action, Command, _Command5, _Cost8, _Debt, _ExtraCost, _Terminal},
        },
        {
            "name": "Patrician/Emporium",
            "types": {
                Action,
                _Cantrip,
                _Cost2,
                _Cost5,
                _Draw2,
                _Peddler,
                _Reveal,
                _Victory,
            },
        },
        {
            "name": "Royal Blacksmith",
            "types": {Action, _Cost8, _Debt, _Discard, _Draw5, _Reveal, _Terminal},
        },
        {
            "name": "Sacrifice",
            "types": {
                Action,
                _Choice,
                _Cost4,
                _Draw2,
                _Money2,
                _Trasher,
                _TrashGainer,
                _Victory,
            },
        },
        {
            "name": "Settlers/Bustling Village",
            "types": {Action, _Cantrip, _Cost2, _Cost5, _Money1, _SplitPile, _Village},
        },
        {
            "name": "Temple",
            "types": {Action, Gathering, _Cost4, _Terminal, _Thinner, _Victory},
        },
        {"name": "Villa", "types": {Action, _Buys, _Cost4, _Money1, _Village}},
        {"name": "Wild Hunt", "types": {Action, _Cost5, _Draw3, _Terminal, _Victory}},
        # Event cards
        {"name": "Advance", "types": {Event, _Cost0, _Gainer6, _Trasher}},
        {
            "name": "Annex",
            "types": {Event, _Cost8, _Debt, _ExtraCost, _Sifter, _Victory},
        },
        {"name": "Banquet", "types": {Event, _Cost3, _Gainer5, _Junker}},
        {"name": "Conquest", "types": {Event, _Cost6, _FutureMoney2, _Victory}},
        {"name": "Delve", "types": {Event, _Cost2, _FreeEvent, _FutureMoney1}},
        {"name": "Dominate", "types": {Event, _Cost14, _Victory}},
        {
            "name": "Donate",
            "types": {Event, _Cost8, _Debt, _ExtraCost, _SpeedUp, _Thinner},
        },
        {"name": "Salt the Earth", "types": {Event, _Cost4, _Trasher, _Victory}},
        {"name": "Ritual", "types": {Event, _Cost4, _Curser, _Trasher, _Victory}},
        {"name": "Tax", "types": {Event, _Cost2, _Debt}},
        {"name": "Trade", "types": {Event, _Cost5, _FutureMoney2, _Trasher}},
        {"name": "Triumph", "types": {Event, _Cost5, _Debt, _ExtraCost, _Victory}},
        {
            "name": "Wedding",
            "types": {Event, _Cost7, _Debt, _ExtraCost, _FutureMoney2, _Victory},
        },
        {"name": "Windfall", "types": {Event, _Cost5, _FutureMoney6}},
        # Landmark Cards
        {"name": "Aqueduct", "types": {Landmark, _Victory}},
        {"name": "Arena", "types": {Landmark, _Discard, _Victory}},
        {"name": "Bandit Fort", "types": {Landmark, _Curser}},
        {"name": "Basilica", "types": {Landmark, _Victory}},
        {"name": "Baths", "types": {Landmark, _Victory}},
        {"name": "Battlefield", "types": {Landmark, _Victory}},
        {"name": "Colonnade", "types": {Landmark, _Victory}},
        {"name": "Defiled Shrine", "types": {Landmark, _Curser, _Victory}},
        {"name": "Fountain", "types": {Landmark, _Junker, _Victory}},
        {"name": "Keep", "types": {Landmark, _Victory}},
        {"name": "Labyrinth", "types": {Landmark, _Victory}},
        {"name": "Mountain Pass", "types": {Landmark, _Debt, _Victory}},
        {"name": "Museum", "types": {Landmark, _NamesMatter, _Victory}},
        {"name": "Obelisk", "types": {Landmark, _Victory}},
        {"name": "Orchard", "types": {Landmark, _NamesMatter, _Victory}},
        {"name": "Palace", "types": {Landmark, _Victory}},
        {"name": "Tomb", "types": {Landmark, _TrashGainer, _Victory}},
        {"name": "Tower", "types": {Landmark, _Empty, _Victory}},
        {"name": "Triumphal Arch", "types": {Landmark, _Victory}},
        {"name": "Wall", "types": {Landmark, _Curser}},
        {"name": "Wolf Den", "types": {Landmark, _Curser}},
    ]
),

Nocturne = Set("Nocturne")
Nocturne.AddCards(
    [
        {"name": "Bard", "types": {Action, Fate, _Cost4, _Money2, _Terminal}},
        {"name": "Blessed Village", "types": {Action, Fate, _Cost4, _Village}},
        {
            "name": "Cemetery + Haunted Mirror (Heirloom)",
            "types": {
                Victory,
                Treasure,
                Heirloom,
                _Cost4,
                _Money1,
                _Thinner,
                _TrashGainer,
            },
        },
        {
            "name": "Changeling",
            "types": {Night, _Cost3, _Trasher, _TrashGainer},
        },
        {
            "name": "Cobbler",
            "types": {Night, Duration, _Cost4, _Gainer4, _SpeedUp},
        },
        {"name": "Conclave", "types": {Action, _Cost4, _Money2, _Village}},
        {"name": "Crypt", "types": {Night, Duration, _Cost5, _DeckSeeder, _Payload}},
        {"name": "Cursed Village", "types": {Action, Doom, _Cost5, _Filler, _Village}},
        {"name": "Den of Sin", "types": {Night, Duration, _Cost5, _Draw2}},
        {"name": "Devil's Workshop", "types": {Night, _Cost4, _FutureMoney2, _Gainer4}},
        {"name": "Druid", "types": {Action, Fate, _Buys, _Cost2, _Terminal}},
        {"name": "Exorcist", "types": {Night, _Cost4, _Trasher, _TrashGainer}},
        {
            "name": "Faithful Hound",
            "types": {
                Action,
                Reaction,
                _Cost2,
                _DeckSeeder,
                _DiscardResponse,
                _Draw2,
                _Terminal,
            },
        },
        {
            "name": "Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)",
            "types": {
                Action,
                Fate,
                Treasure,
                Heirloom,
                _Cost3,
                _Discard,
                _FutureMoney1,
                _Money1,
                _Terminal,
            },
        },
        {
            "name": "Guardian",
            "types": {Night, Duration, _AttackResponse, _Cost2, _Money1},
        },
        {"name": "Ghost Town", "types": {Night, _Cantrip, _Cost3}},
        {
            "name": "Idol",
            "types": {Treasure, Attack, Fate, _Cost5, _Curser, _Money2, _MultiType},
        },
        {
            "name": "Leprechaun",
            "types": {Action, Doom, _Cost3, _FutureMoney2, _Terminal},
        },
        {"name": "Monastery", "types": {Night, _Cost2, _Thinner}},
        {
            "name": "Necromancer + Zombies",
            "types": {Action, _Choice, _Cost4, _Discard, _Draw3, _Remodeler, _Trasher},
        },
        {"name": "Night Watchman", "types": {Night, _Cost3, _Sifter}},
        {
            "name": "Pixie + Goat (Heirloom)",
            "types": {
                Action,
                Fate,
                Treasure,
                Heirloom,
                _Cantrip,
                _Cost2,
                _Money1,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Pooka + Cursed Gold (Heirloom)",
            "types": {
                Action,
                Treasure,
                Heirloom,
                _Cost5,
                _Curser,
                _Draw4,
                _Money3,
                _Thinner,
            },
        },
        {
            "name": "Raider",
            "types": {
                Night,
                Duration,
                Attack,
                _Cost6,
                _Discard,
                _Money3,
                _MultiType,
                _Reveal,
            },
        },
        {
            "name": "Sacred Grove",
            "types": {Action, Fate, _Buys, _Cost5, _Interactive, _Money3, _Terminal},
        },
        {
            "name": "Secret Cave + Magic Lamp (Heirloom)",
            "types": {
                Action,
                Duration,
                Treasure,
                Heirloom,
                _Cantrip,
                _Cost3,
                _Discard,
                _Money1,
                _Money3,
                _TrashGainer,
                _Twin,
            },
        },
        {
            "name": "Shepherd + Pasture (Heirloom)",
            "types": {
                Action,
                Treasure,
                Victory,
                Heirloom,
                _Chainer,
                _Cost4,
                _Discard,
                _Drawload,
                _Money1,
                _MultiType,
            },
        },
        {
            "name": "Skulk",
            "types": {
                Action,
                Attack,
                Doom,
                _Buys,
                _Cost4,
                _FutureMoney2,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Tormentor",
            "types": {Action, Attack, Doom, _Cost5, _Money2, _MultiType, _Terminal},
        },
        {
            "name": "Tracker + Pouch (Heirloom)",
            "types": {
                Action,
                Fate,
                Treasure,
                Heirloom,
                _Buys,
                _Cost2,
                _DeckSeeder,
                _Money1,
                _Terminal,
            },
        },
        {
            "name": "Tragic Hero",
            "types": {Action, _Buys, _Cost5, _Draw3, _Terminal, _Trasher, _TrashGainer},
        },
        {
            "name": "Vampire",
            "types": {Night, Attack, Doom, _Cost5, _Gainer5, _MultiType, _Thinner},
        },
        {
            "name": "Werewolf",
            "types": {
                Action,
                Night,
                Attack,
                Doom,
                _Cost5,
                _Draw3,
                _MultiType,
                _Terminal,
            },
        },
    ]
)

Renaissance = Set("Renaissance")
Renaissance.AddCards(
    [
        {
            "name": "Acting Troupe",
            "types": {Action, _Cost3, _Trasher, _TrashGainer, _Terminal, _Village},
        },
        {
            "name": "Border Guard",
            "types": {
                Action,
                _Cantrip,
                _Cost2,
                _Cantrip,
                _DeckSeeder,
                _Reveal,
                _Sifter,
            },
        },
        {
            "name": "Cargo Ship",
            "types": {Action, Duration, _Cost3, _DeckSeeder, _Money2, _Terminal},
        },
        {"name": "Ducat", "types": {Treasure, _Buys, _Cost2, _FutureMoney1, _Trasher}},
        {"name": "Experiment", "types": {Action, _Cantrip, _Cost3, _Draw2}},
        {
            "name": "Flag Bearer",
            "types": {Action, _Cost4, _Money2, _Terminal, _TrashGainer},
        },
        {"name": "Hideout", "types": {Action, _Cost4, _Curser, _Thinner, _Village}},
        {
            "name": "Improve",
            "types": {Action, _Cost3, _Money2, _Remodeler, _Terminal, _Trasher},
        },
        {
            "name": "Inventor",
            "types": {Action, _Cost4, _CostReducer, _Gainer4, _Terminal},
        },
        {"name": "Lackeys", "types": {Action, _Cost2, _Draw2, _Terminal, _Village}},
        {"name": "Mountain Village", "types": {Action, _Cost4, _Village}},
        {
            "name": "Patron",
            "types": {
                Action,
                Reaction,
                _Chainer,
                _FutureMoney1,
                _Money2,
                _RevealResponse,
            },
        },
        {
            "name": "Priest",
            "types": {Action, _Cost4, _Payload, _Money2, _Terminal, _Thinner},
        },
        {
            "name": "Old Witch",
            "types": {Action, Attack, _Cost5, _Curser, _Draw3, _Interactive, _Trasher},
        },
        {
            "name": "Recruiter",
            "types": {Action, _Cost5, _Draw2, _Terminal, _Thinner, _Village},
        },
        {
            "name": "Research",
            "types": {Action, Duration, _Chainer, _Cost4, _Filler, _Thinner},
        },
        {"name": "Scepter", "types": {Treasure, _Choice, _Cost5, _Money2, _Splitter}},
        {"name": "Scholar", "types": {Action, _Cost5, _Discard, _Draw7, _Terminal}},
        {"name": "Sculptor", "types": {Action, _Cantrip, _Cost5, _Gainer4, _Terminal}},
        {"name": "Seer", "types": {Action, _Cantrip, _Cost5, _Draw4, _Reveal}},
        {
            "name": "Silk Merchant",
            "types": {
                Action,
                _Buys,
                _Cantrip,
                _Draw2,
                _FutureMoney1,
                _Terminal,
                _TrashGainer,
            },
        },
        {"name": "Spices", "types": {Treasure, _Buys, _Cost5, _FutureMoney2, _Money2}},
        {
            "name": "Swashbuckler",
            "types": {
                Action,
                _Cost5,
                _Discard,
                _Draw3,
                _FutureMoney1,
                _Payload,
                _Terminal,
            },
        },
        {
            "name": "Treasurer",
            "types": {
                Action,
                _Cost5,
                _Money3,
                _Payload,
                _Terminal,
                _Thinner,
                _TrashGainer,
            },
        },
        {
            "name": "Villain",
            "types": {
                Action,
                Attack,
                _Cost5,
                _Discard,
                _FutureMoney2,
                _Reveal,
                _Terminal,
            },
        },
        # Project
        {"name": "Academy", "types": {Project, _Chainer, _Cost4}},
        {"name": "Barracks", "types": {Project, _Cost6, _Village}},
        {"name": "Capitalism", "types": {Project, _Cost5}},
        {"name": "Cathedral", "types": {Project, _Cost3, _Thinner}},
        {"name": "Canal", "types": {Project, _Cost7, _CostReducer}},
        {"name": "Citadel", "types": {Project, _Cost8, _Splitter}},
        {"name": "City Gate", "types": {Project, _Cost3, _DeckSeeder}},
        {"name": "Crop Rotation", "types": {Project, _Cost6, _Draw2}},
        {"name": "Exploration", "types": {Project, _Chainer, _Cost4, _FutureMoney1}},
        {"name": "Fair", "types": {Project, _Buys, _Cost4}},
        {"name": "Fleet", "types": {Project, _Cost5, _Draw5}},
        {"name": "Guildhall", "types": {Project, _Cost5, _FutureMoney1}},
        {"name": "Innovation", "types": {Project, _Chainer, _Cost6}},
        {"name": "Pageant", "types": {Project, _Cost3, _FutureMoney1}},
        {"name": "Piazza", "types": {Project, _Chainer, _Cost5}},
        {"name": "Road Network", "types": {Project, _Cost5, _Drawload}},
        {"name": "Sewers", "types": {Project, _Cost3, _Thinner}},
        {"name": "Silos", "types": {Project, _Cost4, _Sifter}},
        {"name": "Sinister Plot", "types": {Project, _Cost4, _Drawload}},
        {"name": "Star Chart", "types": {Project, _Cost3, _DeckSeeder}},
    ]
)

Menagerie = Set("Menagerie")
Menagerie.AddCards(
    [
        {
            "name": "Animal Fair",
            "types": {
                Action,
                _Buys,
                _Cost7,
                _CostVaries,
                _Empty,
                _Money4,
                _Terminal,
                _Thinner,
            },
        },
        {
            "name": "Barge",
            "types": {Action, Duration, _Buys, _Cost5, _Draw3, _Terminal},
        },
        {
            "name": "Black Cat",
            "types": {
                Action,
                Attack,
                Reaction,
                _Cost2,
                _Curser,
                _Draw2,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Bounty Hunter",
            "types": {Action, _Chainer, _Cost4, _Money3, _Thinner},
        },
        {"name": "Camel Train", "types": {Action, _Cost3, _FutureMoney2, _Terminal}},
        {
            "name": "Cardinal",
            "types": {
                Action,
                Attack,
                _BadSifter,
                _BadThinner,
                _Cost4,
                _Discard,
                _Money2,
                _Terminal,
            },
        },
        {"name": "Cavalry", "types": {Action, _Buys, _Cost4, _Draw2, _Terminal}},
        {
            "name": "Coven",
            "types": {Action, Attack, _Chainer, _Cost5, _Curser, _Money2},
        },
        {"name": "Destrier", "types": {Action, _Cantrip, _Cost6, _CostVaries, _Draw2}},
        {"name": "Displace", "types": {Action, _Cost5, _Remodeler, _Terminal}},
        {
            "name": "Falconer",
            "types": {Action, Reaction, _Cost5, _Gainer4, _MultiTypeLove, _Terminal},
        },
        {"name": "Fisherman", "types": {Action, _Cost3, _Cost5, _Peddler}},
        {
            "name": "Gatekeeper",
            "types": {
                Action,
                Duration,
                Attack,
                _BadThinner,
                _Cost5,
                _Money3,
                _MultiType,
                _Terminal,
            },
        },
        {"name": "Goatherd", "types": {Action, _Chainer, _Cost3, _Drawload, _Thinner}},
        {
            "name": "Groom",
            "types": {
                Action,
                _Cantrip,
                _Choice,
                _Cost4,
                _FutureMoney1,
                _Gainer4,
                _Terminal,
            },
        },
        {"name": "Hostelry", "types": {Action, _Cost4, _Discard, _Drawload, _Village}},
        {
            "name": "Hunting Lodge",
            "types": {Action, _Cost5, _Discard, _Filler, _Village},
        },
        {"name": "Kiln", "types": {Action, _Cost5, _Money2, _Gainer6, _Terminal}},
        {"name": "Livery", "types": {Action, _Cost5, _Drawload, _Money3, _Terminal}},
        {
            "name": "Mastermind",
            "types": {Action, Duration, _Cost5, _Splitter, _Terminal},
        },
        {
            "name": "Paddock",
            "types": {Action, _Chainer, _Cost5, _Draw2, _Empty, _Money2},
        },
        {"name": "Sanctuary", "types": {Action, _Buys, _Cantrip, _Cost5, _Thinner}},
        {
            "name": "Scrap",
            "types": {Action, _Buys, _Cantrip, _Choice, _Drawload, _Payload, _Thinner},
        },
        {
            "name": "Sheepdog",
            "types": {Action, Reaction, _Cost3, _Draw2, _FreeAction, _Terminal},
        },
        {
            "name": "Sleigh",
            "types": {Action, Reaction, _Cost2, _DeckSeeder, _Draw2, _Terminal},
        },
        {"name": "Snowy Village", "types": {Action, _Buys, _Cost3, _Village}},
        {"name": "Stockpile", "types": {Treasure, _Buys, _Cost3, _Money3, _Thinner}},
        {"name": "Supplies", "types": {Treasure, _Cost2, _Money1, _DeckSeeder}},
        {
            "name": "Village Green",
            "types": {
                Action,
                Duration,
                Reaction,
                _Cost4,
                _DiscardResponse,
                _MultiType,
                _Village,
            },
        },
        {
            "name": "Wayfarer",
            "types": {Action, _Cost6, _CostVaries, _Draw3, _FutureMoney1, _Terminal},
        },
        # Events
        {
            "name": "Alliance",
            "types": {Event, _Cost10, _FutureMoney3, _Junker, _Victory},
        },
        {"name": "Banish", "types": {Event, _Cost4, _Thinner}},
        {"name": "Bargain", "types": {Event, _Cost4, _Gainer5, _Interactive}},
        {"name": "Commerce", "types": {Event, _Cost5, _Payload}},
        {"name": "Delay", "types": {Event, _Cost0, _FreeAction, _Saver}},
        {"name": "Demand", "types": {Event, _Cost5, _DeckSeeder, _Gainer4}},
        {"name": "Desperation", "types": {Event, _Cost0, _Curser, _FreeEvent, _Money2}},
        {"name": "Enclave", "types": {Event, _Cost8, _FutureMoney2, _Victory}},
        {"name": "Enhance", "types": {Event, _Cost3, _Remodeler, _Trasher}},
        {
            "name": "Gamble",
            "types": {Event, _Chainer, _Cost2, _Discard, _FreeEvent, _Reveal},
        },
        {"name": "Invest", "types": {Event, _Cost4, _Drawload}},
        {"name": "March", "types": {Event, _Chainer, _Cost3}},
        {"name": "Populate", "types": {Event, _Cost10, _Gainer6}},
        {
            "name": "Pursue",
            "types": {Event, _Cost2, _Discard, _FreeEvent, _Reveal, _Sifter},
        },
        {"name": "Reap", "types": {Event, _Cost7, _FutureMoney2, _Money3}},
        {"name": "Ride", "types": {Event, _Cost2, _Draw2}},
        {"name": "Seize the Day", "types": {Event, _Cost4, _Draw5}},
        {"name": "Stampede", "types": {Event, _Cost5, _DeckSeeder, _Draw5}},
        {"name": "Toil", "types": {Event, _Chainer, _Cantrip, _FreeEvent}},
        {"name": "Transport", "types": {Event, _Cost3, _DeckSeeder}},
        # Way
        {"name": "Way of the Butterfly", "types": {Way, _Remodeler}},
        {"name": "Way of the Camel", "types": {Way, _FutureMoney2}},
        {"name": "Way of the Chameleon", "types": {Way}},
        {"name": "Way of the Frog", "types": {Way, _Chainer, _DeckSeeder}},
        {"name": "Way of the Goat", "types": {Way, _Thinner}},
        {"name": "Way of the Horse", "types": {Way, _Draw2, _Thinner}},
        {"name": "Way of the Mole", "types": {Way, _Chainer, _Sifter}},
        {"name": "Way of the Monkey", "types": {Way, _Buys, _Money1}},
        {"name": "Way of the Mouse", "types": {Way, _Kingdom}},
        {"name": "Way of the Mule", "types": {Way, _Chainer, _Money1}},
        {"name": "Way of the Otter", "types": {Way, _Draw2}},
        {"name": "Way of the Owl", "types": {Way, _Filler}},
        {"name": "Way of the Ox", "types": {Way, _Village}},
        {"name": "Way of the Pig", "types": {Way, _Cantrip}},
        {"name": "Way of the Rat", "types": {Way, _Discard, _Gainer6}},
        {"name": "Way of the Seal", "types": {Way, _DeckSeeder, _Money1}},
        {"name": "Way of the Sheep", "types": {Way, _Money2}},
        {"name": "Way of the Squirrel", "types": {Way, _Draw2}},
        {"name": "Way of the Turtle", "types": {Way, _FreeAction}},
        {"name": "Way of the Worm", "types": {Way, _Victory}},
    ]
)

Allies = Set("Allies")
Allies.AddCards(
    [
        {
            "name": "Augers: Herb Gatherer + Acolyte + Sorceress + Sibyl",
            "types": {
                Action,
                Attack,
                Augur,
                _BottomSeeder,
                _Buys,
                _CostVaries,
                _Curser,
                _DeckGuesser,
                _DeckSeeder,
                _Draw2,
                _Money3,
                _MultiTypeLove,
                _SpeedUp,
                _Thinner,
                _TrashGainer,
            },
        },
        {
            "name": "Barbarian",
            "types": {Action, Attack, _Cost5, _Curser, _Downgrader, _Money2, _Trasher},
        },
        {
            "name": "Bauble",
            "types": {Treasure, Liaison, _Buys, _Choice, _Cost2, _DeckSeeder, _Money1},
        },
        {
            "name": "Broker",
            "types": {
                Action,
                Liaison,
                _Cost4,
                _Drawload,
                _Payload,
                _Terminal,
                _Thinner,
                _Trasher,
                _TrashGainer,
                _Village,
            },
        },
        {
            "name": "Capital City",
            "types": {Action, _Cost5, _Discard, _Draw2, _Money2, _Village},
        },
        {
            "name": "Carpenter",
            "types": {
                Action,
                _Chainer,
                _Cost4,
                _Gainer4,
                _Remodeler,
                _Terminal,
                _Trasher,
            },
        },
        {
            "name": "Clashes: Battle Plan + Archer + Warlord + Territory",
            "types": {
                Action,
                Attack,
                Duration,
                Victory,
                Clash,
                _BadSifter,
                _Cantrip,
                _CostVaries,
                _Draw2,
                _Empty,
                _Money2,
                _MultiType,
                _Payload,
            },
        },
        {
            "name": "Contract",
            "types": {
                Treasure,
                Duration,
                Liaison,
                _Chainer,
                _Cost5,
                _Money2,
                _MultiType,
                _Saver,
            },
        },
        {"name": "Courier", "types": {Action, _Chainer, _Cost4, _Discard, _Money1}},
        {
            "name": "Forts: Tent + Garrison + Hill Fort + Stronghold",
            "types": {
                Action,
                Victory,
                Duration,
                Fort,
                _Cantrip,
                _CostVaries,
                _DeckSeeder,
                _Draw3,
                _Drawload,
                _Gainer4,
                _Money2,
                _Money3,
                _MultiType,
                _Terminal,
            },
        },
        {"name": "Emissary", "types": {Action, Liaison, _Cantrip, _Draw3, _Terminal}},
        {
            "name": "Importer",
            "types": {
                Action,
                Duration,
                Liaison,
                _Cost3,
                _Gainer5,
                _MultiType,
                _Terminal,
            },
        },
        {"name": "Galleria", "types": {Action, _Buys, _Cost5, _Money3}},
        {
            "name": "Guildmaster",
            "types": {Action, Liaison, _Cost5, _Discard, _Money3, _Terminal},
        },
        {
            "name": "Highwayman",
            "types": {Action, Duration, Attack, _Cost5, _Draw3, _MultiType, _Terminal},
        },
        {"name": "Hunter", "types": {Action, _Cantrip, _Cost5, _Reveal, _Sifter}},
        {"name": "Innkeeper", "types": {Action, _Cantrip, _Choice, _Cost4, _Sifter}},
        {
            "name": "Marquis",
            "types": {Action, _Buys, _Cost6, _Discard, _Drawload, _Terminal},
        },
        {
            "name": "Merchant Camp",
            "types": {Action, _Cost3, _DeckSeeder, _Money1, _Village},
        },
        {
            "name": "Modify",
            "types": {Action, _Choice, _Cost5, _Remodeler, _Thinner, _Trasher},
        },
        {
            "name": "Odysseys: Old Map, Voyage, Sunken Treasure, Distant Shore",
            "types": {Action},
        },
        {
            "name": "Royal Galley",
            "types": {Action, Duration, _Chainer, _Cost4, _Splitter},
        },
        {"name": "Sentinel", "types": {Action, _Cost3, _Sifter, _Terminal, _Thinner}},
        {
            "name": "Sycophant",
            "types": {
                Action,
                Liaison,
                _Chainer,
                _Cost2,
                _Discard,
                _Money3,
                _TrashGainer,
            },
        },
        {
            "name": "Skirmisher",
            "types": {Action, Attack, _AttackResponse, _Cost5, _Discard, _Peddler},
        },
        {
            "name": "Specialist",
            "types": {Action, _Cost5, _Gainer6, _Splitter, _Terminal},
        },
        {"name": "Swap", "types": {Action, _Cantrip, _Cost5, _Gainer5, _Remodeler}},
        {"name": "Town", "types": {Action, _Buys, _Choice, _Cost4, _Money2, _Village}},
        {
            "name": "Townsfolk: Town Crier + Blacksmith + Miller + Elder",
            "types": {
                Action,
                Townsfolk,
                _Choice,
                _CostVaries,
                _Discard,
                _Draw2,
                _Filler,
                _FutureMoney1,
                _Money2,
                _Sifter,
            },
        },
        {"name": "Underling", "types": {Action, Liaison, _Cantrip, _Cost3}},
        {
            "name": "Wizards: Student, Conjurer, Sorcerer, Lich",
            "types": {
                Action,
                Duration,
                Liaison,
                Attack,
                Wizard,
                _Cantrip,
                _Chainer,
                _CostVaries,
                _Curser,
                _DeckGuesser,
                _DeckSeeder,
                _Draw6,
                _Gainer4,
                _Gainer5,
                _Saver,
                _Thinner,
                _TrashGainer,
                _Village,
            },
        },
        # Allies
        {"name": "Architects' Guild", "types": {Ally, _Gainer5}},
        {"name": "Band of Nomads", "types": {Ally, _Buys, _Choice}},
        {"name": "Cave Dwellers", "types": {Ally, _Sifter}},
        {"name": "Circle of Witches", "types": {Ally, _Curser}},
        {"name": "City-state", "types": {Ally, _Chainer}},
        {"name": "Coastal Haven", "types": {Ally, _Saver}},
        {"name": "Crafters' Guild", "types": {Ally, _DeckSeeder, _Gainer4}},
        {"name": "Desert Guides", "types": {Ally, _Sifter}},
        {"name": "Family of Inventors", "types": {Ally, _CostReducer}},
        {"name": "Fellowship of Scribes", "types": {Ally, _Filler}},
        {"name": "Forest Dwellers", "types": {Ally, _DeckSeeder, _Discard, _Sifter}},
        {"name": "Gang of Pickpockets", "types": {Ally, _Discard}},
        {"name": "Island Folk", "types": {Ally, _Draw5}},
        {"name": "League of Bankers", "types": {Ally, _Payload}},
        {"name": "League of Shopkeepers", "types": {Ally, _Buys, _Chainer, _Payload}},
        {"name": "Market Towns", "types": {Ally, _Chainer}},
        {"name": "Mountain Folk", "types": {Ally, _Draw3}},
        {"name": "Order of Astrologers", "types": {Ally, _DeckSeeder}},
        {"name": "Order of Masons", "types": {Ally, _Discard}},
        {"name": "Peaceful Cult", "types": {Ally, _Thinner}},
        {"name": "Plateau Shepherds", "types": {Ally, _Cost2Response, _Victory}},
        {"name": "Trappers' Lodge", "types": {Ally, _DeckSeeder}},
        {"name": "Woodworkers' Guild", "types": {Ally, _Trasher, _TrashGainer}},
    ]
)

Plunder = Set("Plunder")
Plunder.AddCards(
    [
        {
            "name": "Abundance",
            "types": {Treasure, Duration, _Buys, _Cost4, _Money3, _Terminal},
        },
        {
            "name": "Buried Treasure",
            "types": {
                Treasure,
                Duration,
                _Buys,
                _Cost5,
                _FreeAction,
                _Money3,
                _Terminal,
            },
        },
        {
            "name": "Cabin Boy",
            "types": {Action, Duration, _Gainer6, _Money2, _Peddler, _Trasher},
        },
        {
            "name": "Cage",
            "types": {Treasure, Duration, _Cost2, _Saver, _Trasher},
        },
        {
            "name": "Crew",
            "types": {Action, Duration, _Cost5, _Draw3, _DeckSeeder, _Terminal},
        },
        {
            "name": "Crucible",
            "types": {Treasure, _Cost4, _Payload, _Thinner, _Trasher, _TrashGainer},
        },
        {
            "name": "Cutthroat",
            "types": {
                Action,
                Duration,
                Attack,
                _Cost5,
                _Discard,
                _FutureMoney2,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Enlarge",
            "types": {Action, Duration, _Cost5, _Remodeler, _Terminal, _Trasher},
        },
        {
            "name": "Figurine",
            "types": {Treasure, _Buys, _Cost5, _Discard, _Draw2, _Money1},
        },
        {"name": "First Mate", "types": {Action, _Cost5, _Filler, _Village}},
        {
            "name": "Flagship",
            "types": {
                Action,
                Duration,
                Command,
                _Cost4,
                _Money2,
                _MultiType,
                _Splitter,
                _Terminal,
            },
        },
        {
            "name": "Fortune Hunter",
            "types": {Action, _Cost4, _Payload, _Sifter, _Terminal},
        },
        {
            "name": "Frigate",
            "types": {
                Action,
                Duration,
                Attack,
                _Cost5,
                _Discard,
                _Money3,
                _MultiType,
                _Terminal,
            },
        },
        {"name": "Gondola", "types": {Treasure, Duration, _Chainer, _Cost4, _Money2}},
        {
            "name": "Grotto",
            "types": {Action, Duration, _Chainer, _Cost2, _Discard, _Draw4},
        },
        {"name": "Harbor Village", "types": {Action, _Cost4, _Peddler, _Village}},
        {
            "name": "Jewelled Egg",
            "types": {Treasure, _Buys, _Cost2, _FutureMoney2, _Money1, _TrashGainer},
        },
        {"name": "King's Cache", "types": {Treasure, _Cost7, _Splitter}},
        {
            "name": "Landing Party",
            "types": {Action, Duration, _Cost4, _DeckSeeder, _Draw2, _Village},
        },
        {"name": "Longship", "types": {Action, Duration, _Cost5, _Draw2, _Village}},
        {
            "name": "Mapmaker",
            "types": {
                Action,
                Reaction,
                _Cost4,
                _Discard,
                _Draw2,
                _FreeAction,
                _Sifter,
                _Terminal,
            },
        },
        {
            "name": "Maroon",
            "types": {Action, _Cost4, _Drawload, _Terminal, _Thinner, _Trasher},
        },
        {"name": "Mining Road", "types": {Action, _Buys, _Chainer, _Money2, _SpeedUp}},
        {"name": "Pendant", "types": {Treasure, _Cost5, _Payload}},
        {
            "name": "Pickaxe",
            "types": {Treasure, _Cost5, _Money1, _Money4, _Thinner, _Trasher},
        },
        {"name": "Pilgrim", "types": {Action, _Cost5, _DeckSeeder, _Draw4, _Terminal}},
        {
            "name": "Quartermaster",
            "types": {Action, Duration, _Cost5, _Gainer4, _Saver, _Terminal},
        },
        {
            "name": "Rope",
            "types": {Treasure, Duration, _Buys, _Money1, _Sifter, _Thinner},
        },
        {
            "name": "Sack of Loot",
            "types": {Treasure, _Buys, _Cost6, _FutureMoney2, _Money1},
        },
        {"name": "Silver Mine", "types": {Treasure, _Cost5, _Gainer4, _Money2}},
        {"name": "Tools", "types": {Treasure, _Cost4, _Gainer6}},
        {
            "name": "Search",
            "types": {
                Action,
                Duration,
                _Cost2,
                _Empty,
                _FutureMoney2,
                _Money2,
                _Terminal,
            },
        },
        {
            "name": "Shaman",
            "types": {
                Action,
                _Chainer,
                _Cost2,
                _Money1,
                _Thinner,
                _Trasher,
                _TrashGainer,
            },
        },
        {
            "name": "Secluded Shrine",
            "types": {Action, Duration, _Cost3, _Money1, _Terminal, _Thinner, _Trasher},
        },
        {
            "name": "Siren",
            "types": {
                Action,
                Duration,
                Attack,
                _Cost3,
                _Curser,
                _Filler,
                _MultiType,
                _Terminal,
                _Trasher,
            },
        },
        {
            "name": "Stowaway",
            "types": {
                Action,
                Duration,
                Reaction,
                _Cost3,
                _Draw2,
                _FreeAction,
                _MultiType,
                _Terminal,
            },
        },
        {"name": "Swamp Shacks", "types": {Action, _Cost4, _Drawload, _Village}},
        {"name": "Taskmaster", "types": {Action, Duration, _Money2, _Village}},
        {
            "name": "Trickster",
            "types": {Action, Attack, _Cost5, _Curser, _Saver, _Terminal},
        },
        {"name": "Wealthy Village", "types": {Action, _Cost5, _FutureMoney2, _Village}},
        # Events
        {"name": "Avoid", "types": {Event, _Cost2, _Discard, _FreeEvent}},
        {"name": "Bury", "types": {Event, _BottomSeeder, _Cost1, _FreeEvent}},
        {"name": "Deliver", "types": {Event, _Cost2, _FreeEvent, _Saver}},
        {"name": "Foray", "types": {Event, _Cost3, _Discard, _FutureMoney2}},
        {
            "name": "Invasion",
            "types": {Event, _AttackResponse, _Chainer, _Cost10, _Money3, _Victory},
        },
        {"name": "Journey", "types": {Event, _Cost4, _Draw5}},
        {"name": "Launch", "types": {Event, _Cantrip, _Cost3, _FreeEvent}},
        {"name": "Looting", "types": {Event, _Cost6, _FutureMoney2}},
        {"name": "Maelstrom", "types": {Event, _Cost4, _Interactive, _Thinner}},
        {"name": "Mirror", "types": {Event, _Cost3, _FreeEvent, _Gainer6}},
        {"name": "Peril", "types": {Event, _Cost2, _FutureMoney2, _Thinner}},
        {"name": "Prepare", "types": {Event, _Cost3, _Discard, _Saver, _Village}},
        {
            "name": "Prosper",
            "types": {Event, _Cost10, _FutureMoney2, _Gainer3, _Gainer6},
        },
        {"name": "Rush", "types": {Event, _Chainer, _Cost2, _FreeEvent}},
        {
            "name": "Scrounge",
            "types": {
                Event,
                _Choice,
                _Cost3,
                _Gainer5,
                _Thinner,
                _TrashGainer,
                _Victory,
            },
        },
        # Traits
        {"name": "Cheap", "types": {Trait, _CostReducer}},
        {"name": "Cursed", "types": {Trait, _Curser, _FutureMoney2}},
        {"name": "Fated", "types": {Trait, _BottomSeeder, _DeckSeeder}},
        {"name": "Fawning", "types": {Trait, _Gainer6}},
        {"name": "Friendly", "types": {Trait, _Discard, _Gainer6}},
        {"name": "Hasty", "types": {Trait, _SpeedUp}},
        {"name": "Inherited", "types": {Trait, _Kingdom}},
        {"name": "Inspiring", "types": {Trait, _Chainer}},
        {"name": "Nearby", "types": {Trait, _Buys}},
        {"name": "Patient", "types": {Trait, _Saver}},
        {"name": "Pious", "types": {Trait, _Thinner, _Trasher}},
        {"name": "Reckless", "types": {Trait, _Splitter, _Thinner}},
        {"name": "Rich", "types": {Trait, _FutureMoney1}},
        {"name": "Shy", "types": {Trait, _Discard, _Draw2}},
        {"name": "Tireless", "types": {Trait, _DeckSeeder}},
    ]
)

Antiquities = Set("Antiquities")
Antiquities.AddCards(
    [
        {
            "name": "Agora",
            "types": {
                Action,
                Reaction,
                _Cost5,
                _Discard,
                _FutureMoney1,
                _Money2,
                _Village,
            },
        },
        {
            "name": "Aquifer",
            "types": {Action, _Choice, _Cantrip, _Cost4, _Gainer4, _Money1, _Terminal},
        },
        {
            "name": "Archaeologist",
            "types": {
                Action,
                _Cost7,
                _DeckSeeder,
                _Discard,
                _Draw3,
                _Sifter,
                _Terminal,
            },
        },
        {
            "name": "Collector",
            "types": {
                Action,
                _Cost4,
                _DeckSeeder,
                _Interactive,
                _Remodeler,
                _Sifter,
                _Terminal,
                _Trasher,
            },
        },
        {"name": "Curio", "types": {Treasure, _Cost4, _Money1, _Payload}},
        {"name": "Dig", "types": {Action, _Cost8, _Discard, _Reveal, _Victory}},
        {
            "name": "Discovery",
            "types": {Treasure, _Cost2, _FutureMoney2, _ShuffleIn, _Thinner},
        },
        {
            "name": "Encroach",
            "types": {
                Action,
                _Cost6,
                _Discard,
                _Filler,
                _Remodeler,
                _Terminal,
                _Victory,
            },
        },
        {
            "name": "Gamepiece",
            "types": {Treasure, Reaction, _Cost3, _Discard, _DiscardResponse, _Money1},
        },
        {
            "name": "Graveyard",
            "types": {Action, _Cost1, _Gainer6, _TrashGainer, _Village},
        },
        {
            "name": "Grave Watcher",
            "types": {
                Action,
                Attack,
                _BadSifter,
                _Chainer,
                _Choice,
                _Cost3,
                _Curser,
                _Discard,
                _Junker,
                _Money2,
                _Money3,
                _Terminal,
            },
        },
        {
            "name": "Inscription",
            "types": {
                Action,
                Reaction,
                _Cost3,
                _Discard,
                _DiscardResponse,
                _Filler,
                _Sifter,
            },
        },
        {
            "name": "Inspector",
            "types": {Action, Attack, _BadSifter, _Cost3, _Discard, _Reveal, _Sifter},
        },
        {
            "name": "Mastermind",
            "types": {Action, _BottomSeeder, _Cantrip, _Cost5, _Discard, _FreeAction},
        },
        {
            "name": "Mausoleum",
            "types": {Action, _Choice, _Cost6, _Draw2, _Saver, _Village},
        },
        {
            "name": "Mendicant",
            "types": {Action, _Cantrip, _Cost4, _Discard, _Junker, _Victory},
        },
        {"name": "Miner", "types": {Action, _Cantrip, _Cost3, _Discard, _Remodeler}},
        {
            "name": "Mission House",
            "types": {Action, _Cost5, _Discard, _Draw2, _Victory, _Village},
        },
        {
            "name": "Moundbuilder Village",
            "types": {Action, _Cost5, _Money3, _Peddler, _Thinner, _Village},
        },
        {
            "name": "Pharaoh",
            "types": {Action, Attack, _Cost8, _Curser, _Payload, _Terminal, _Trasher},
        },
        {"name": "Profiteer", "types": {Action, _Buys, _Chainer, _Cost3, _CostReducer}},
        {
            "name": "Pyramid",
            "types": {Action, _Buys, _Cost5, _Terminal, _Thinner, _Trasher, _Victory},
        },
        {
            "name": "Shipwreck",
            "types": {
                Action,
                _BottomSeeder,
                _Buys,
                _Cost3,
                _Draw2,
                _FutureMoney1,
                _FutureMoney2,
                _Terminal,
                _TrashGainer,
            },
        },
        {
            "name": "Stoneworks",
            "types": {
                Action,
                _Buys,
                _DeckSeeder,
                _FutureMoney1,
                _Trasher,
                _TrashGainer,
                _Victory,
            },
        },
        {
            "name": "Stronghold",
            "types": {
                Action,
                Reaction,
                _AttackResponse,
                _Cost5,
                _SpeedUp,
                _Trasher,
                _Terminal,
                _Thinner,
            },
        },
        {
            "name": "Tomb Raider",
            "types": {
                Action,
                Attack,
                _AttackResponse,
                _Chainer,
                _Cost3,
                _Discard,
                _Gainer6,
            },
        },
        {
            "name": "Snake Charmer",
            "types": {
                Action,
                Attack,
                _BottomSeeder,
                _Chainer,
                _Cost4,
                _Curser,
                _Money1,
                _Money4,
                _Thinner,
                _Trasher,
            },
        },
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


def AdvancedRandomize(options, typeDict, completeSet, landscapeSet=[]):
    """Sketch some thoughts here:
    1. Get all the Card Types (visible and _internal) and put them in a dict.
    2. Weight each of the card types based on two things:
        a.  1 if 5 or more examples in pool
        b.  0.2 * # if 4 or less in pool
    3. Randomly pull a Card Type.
    4. Randomly select a card with that Card Type.
    5. Remove that Card Type from the list of Card Types so we cannot get it again.
    6. Rebalance the weight of each Card Type:
        a.  If it's already in the Results, -0.1 for each card with that type in the Results.
        b.  For each Card Type in the Results that synnergizes with this card, increase
            the weight by +0.2, unless there is another example of this Card Type in the
            Results.
        c.  For each Card Type in the Results that wants this card, increase the weight by +1
        d.  "BadTypes" stop any synnergies from being applied to this type if they are present
    7. Repeat steps 3-6 until results are done. Do the same for landscapes.
    """
    resultSet = set()
    waySet = set()
    typeSet = set()
    for card in completeSet:
        typeSet = typeSet | card.types
    typeDict = {}
    selectedTypes = set()
    includedTypes = set()
    # set the initial card type weights
    for cardType in typeSet:
        typeDict[cardType] = (
            min(5, len([card for card in completeSet if cardType in card.types])) * 1
        )
    counter = 0
    while len(resultSet) < 10:
        # choose a card type:
        cardType = random.choices(list(typeDict.keys()), list(typeDict.values()))[0]
        cardsOfType = [card for card in completeSet if cardType in card.types]
        if cardsOfType:
            cardDict = {}
            for cardOfType in reversed(cardsOfType):
                typesForCardOfType = [
                    typeDict[cardsType]
                    for cardsType in cardOfType.types
                    if cardsType in typeDict and cardsType != cardType
                ]
                if typesForCardOfType:
                    cardDict[cardOfType] = int(
                        round(sum(typesForCardOfType) / len(typesForCardOfType), 0)
                    )
                else:
                    cardDict[cardOfType] = 5
            selectedTypes.add(cardType)
            typeDict.pop(cardType)
        else:
            typeDict.pop(cardType)
            continue
        card = random.choices(list(cardDict.keys()), list(cardDict.values()))[0]
        # Categorize the card from the shuffled pile
        if card.types & {Way}:
            waySet.add(card)
        elif card.types & {Event, Landmark, Project, Trait}:
            landscapeSet.add(card)
        else:
            resultSet.add(card)
        counter += 1
        # Rebalance the card type weights
        badTypes = set()
        bonusedTypes = []
        wantedTypes = []
        for cardType in card.types:
            includedTypes.add(cardType)
        for cardType in card.types:
            if cardType in typeDict:
                typeDict[cardType] = max(0, typeDict[cardType] - 1)
                for selectedType in selectedTypes:
                    badTypes.add(badType for badType in selectedType.badTypes)
                for bonusType in cardType.bonusToTypes:
                    if (
                        bonusType in typeDict
                        and bonusType not in bonusedTypes
                        and bonusType not in badTypes
                    ):
                        typeDict[bonusType] = typeDict[bonusType] + 6
                        bonusedTypes.append(bonusType)
                for wantedType in cardType.wantsTypes:
                    if (
                        wantedType in typeDict
                        and wantedType not in includedTypes
                        and wantedType not in wantedTypes
                        and wantedType not in badTypes
                    ):
                        typeDict[wantedType] = typeDict[wantedType] + 50
                        wantedTypes.append(wantedType)
    if landscapeSet:
        # Get final list of landscape cards
        if options and options.get("limit-landscapes"):
            landscapeList = random.sample([way for way in waySet], len(waySet))[:1]
            landscapeList.extend(
                random.sample(landscapeSet, len(landscapeSet))[: 2 - len(landscapeList)]
            )
        else:
            landscapeList = random.sample(landscapeSet, len(landscapeSet))[:3]
            landscapeList.extend(random.sample(waySet, len(waySet))[:1])
        return typeDict, landscapeList, resultSet, waySet
    else:
        return typeDict, [], resultSet, set()


def AdvancedSample(typeDict, cardSet, num):
    resultSet = set()
    typeSet = set()
    for card in cardSet:
        typeSet = typeSet | card.types
    selectedTypes = set()
    includedTypes = set()
    # set the initial card type weights
    for cardType in typeSet:
        typeDict[cardType] = (
            min(5, len([card for card in cardSet if cardType in card.types])) * 1
        )
    counter = 0
    while len(resultSet) < num:
        # choose a card type:
        cardType = random.choices(list(typeDict.keys()), list(typeDict.values()))[0]
        cardsOfType = [card for card in cardSet if cardType in card.types]
        if cardsOfType:
            cardDict = {}
            for cardOfType in reversed(cardsOfType):
                typesForCardOfType = [
                    typeDict[cardsType]
                    for cardsType in cardOfType.types
                    if cardsType in typeDict and cardsType != cardType
                ]
                if typesForCardOfType:
                    cardDict[cardOfType] = math.ceil(
                        sum(typesForCardOfType) / len(typesForCardOfType)
                    )
                else:
                    cardDict[cardOfType] = 5
            selectedTypes.add(cardType)
            typeDict.pop(cardType)
        else:
            typeDict.pop(cardType)
            continue
        card = random.choices(list(cardDict.keys()), list(cardDict.values()))[0]
        resultSet.add(card)
        counter += 1
        # Rebalance the card type weights
        badTypes = set()
        bonusedTypes = []
        wantedTypes = []
        for cardType in card.types:
            includedTypes.add(cardType)
        for cardType in card.types:
            if cardType in typeDict:
                typeDict[cardType] = max(0, typeDict[cardType] - 1)
                for selectedType in selectedTypes:
                    badTypes.add(badType for badType in selectedType.badTypes)
                for bonusType in cardType.bonusToTypes:
                    if (
                        bonusType in typeDict
                        and bonusType not in bonusedTypes
                        and bonusType not in badTypes
                    ):
                        typeDict[bonusType] = typeDict[bonusType] + 6
                        bonusedTypes.append(bonusType)
                for wantedType in cardType.wantsTypes:
                    if (
                        wantedType in typeDict
                        and wantedType not in includedTypes
                        and wantedType not in wantedTypes
                        and wantedType not in badTypes
                    ):
                        typeDict[wantedType] = typeDict[wantedType] + 50
                        wantedTypes.append(wantedType)

    return list(resultSet)


def BasicRandomize(options, typeDict, completeSet, landscapes=False):
    if landscapes:
        resultSet = set()
        waySet = set()
        landscapeSet = set()
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
        return landscapeList, resultSet, waySet
    else:
        resultSet = set(random.sample(completeSet, 10))
        return typeDict, [], resultSet, set()


def BasicSample(cardSet, num):
    return random.sample(list(cardSet), num)


def RandomizeDominion(setNames=None, options=None):
    # Make full list + landscape cards to determine landscape cards
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
    typeDict = {}

    if completeSet & LandscapeCards:
        # Handle sets that include landscape cards
        kingdomSet = completeSet - LandscapeCards
        landscapeSet = completeSet & LandscapeCards

        resultSet = set()
        waySet = set()

        # for testing only
        typeDict, landscapeList, resultSet, waySet = AdvancedRandomize(
            options, typeDict, completeSet, landscapeSet
        )

        # if options and options.get("advanced-randomization"):
        #    typeDict, landscapeList, resultSet, waySet = AdvancedRandomize(
        #        options, typeDict, completeSet, landscapeSet
        #    )
        # else:
        #    typeDict, landscapeList, resultSet, waySet = BasicRandomize(
        #        options, typeDict, completeSet, landscapeSet
        #    )
    else:
        kingdomSet = completeSet
        landscapeList = []

        if options and options.get("advanced-randomization"):
            typeDict, landscapeList, resultSet, waySet = AdvancedRandomize(
                options, typeDict, completeSet
            )
        else:
            typeDict, landscapeList, resultSet, waySet = BasicRandomize(
                options, typeDict, completeSet
            )

    # Enforce Alchemy rule
    if (options or {}).get("enforce-alchemy-rule", True):
        alchemyCards = Alchemy.cards & resultSet
        if len(alchemyCards) == 1:
            # If there's only 1 Alchemy card, remove Alchemy from the options
            # and draw an addtional Kingdom card
            resultSet -= alchemyCards
            resultSet.update(
                SampleDominion(options, typeDict, kingdomSet - resultSet, 1)
            )
        elif len(alchemyCards) == 2:
            # If there are only 2 Alchemy cards, pull an additional Alchemy
            # card and randomly remove one non-Alchemy card
            resultSet -= alchemyCards
            alchemyCards.update(
                SampleDominion(options, typeDict, Alchemy.cards - alchemyCards, 1)
            )
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
            resultSet.update(
                SampleDominion(options, typeDict, kingdomSet - resultSet, 1)
            )
            baneCard = SampleDominion(options, typeDict, resultSet & BaneCards, 1)[0]
        else:
            baneCard = SampleDominion(options, typeDict, eligibleBanes, 1)[0]
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

            mouseCard = SampleDominion(options, typeDict, eligibleMice, 1)[0]
            resultSet.update(
                SampleDominion(options, typeDict, kingdomSet - resultSet, 1)
            )
            resultSet.remove(mouseCard)
        else:
            mouseCard = SampleDominion(options, typeDict, eligibleMice, 1)[0]
        mouseSet.add(mouseCard)

    fullResults = resultSet.union(landscapeList)

    # Check for Colonies and Platinums
    includeColoniesAndPlatinum = Prosperity in sets and PlatinumLove.intersection(
        random.sample(fullResults, 1)
    )

    # Check for _Potions
    include_Potions = Alchemy.potionCards & resultSet

    # Check for Prizes
    includePrizes = Cornucopia.cards("Tournament") & resultSet

    # Check for Shelters
    includeShelters = DarkAges in sets and ShelterLove.intersection(
        random.sample(fullResults, 1)
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


def SampleDominion(options, typeDict, cardSet, num):
    # Temporary for testing
    return AdvancedSample(typeDict, cardSet, num)
    # if options and options.get("advanced-randomization"):
    #     return AdvancedSample(typeDict, cardSet, num)
    # else:
    #     return BasicSample(cardSet, num)


if __name__ == "__main__":
    print("\n".join(RandomizeDominion()))
