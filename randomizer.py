import math
import random


AllSets = {}


class AdvTag(object):
    def __init__(self, name, bonusToTags=[], wantsTags=[], badTags=[]):
        self.name = name
        self.bonusToTags = bonusToTags
        self.wantsTags = wantsTags
        self.badTags = badTags


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

        # create an entry in self.advTags for each type in self.types
        for type in self.types:
            self.advTags.add(AdvTag(f"_{type.name}"))

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
        self.PotionCards = None
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
        if self.PotionCards is None:
            self.PotionCards = CardList(
                card for card in self._cards if card.types & {Potion}
            )
        return self.PotionCards


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
Odyssey = CardType("Odyssey")
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
_Event = AdvTag("Event")
_Landmark = AdvTag("Landmark")
_Project = AdvTag("Project")
_Way = AdvTag("Way")
_Ally = AdvTag("Ally")
_Trait = AdvTag("Trait")
# Donald X types
# Potion isn't written on the card
_Action = AdvTag("Action")
_Attack = AdvTag("Attack")
_Augur = AdvTag("Augur")
_Castle = AdvTag("Castle")
_Clash = AdvTag("Clash")
_Command = AdvTag("Command")
_Doom = AdvTag("Doom")
_Duration = AdvTag("Duration")
_Fate = AdvTag("Fate")
_Fort = AdvTag("Fort")
_Gathering = AdvTag("Gathering")
_Heirloom = AdvTag("Heirloom")
_Knight = AdvTag("Knight")
_Liaison = AdvTag("Liaison")
_Looter = AdvTag("Looter")
_Night = AdvTag("Night")
_Odyssey = AdvTag("Odyssey")
_Potion = AdvTag("Potion")
_Reaction = AdvTag("Reaction")
_Reserve = AdvTag("Reserve")
_Townsfolk = AdvTag("Townsfolk")
_Traveller = AdvTag("Traveller")
_Treasure = AdvTag("Treasure")
_VictoryGainer = AdvTag("Victory")
_Wizard = AdvTag("Wizard")

_ActionLover = AdvTag("_ActionLover")  # wants a lot of actions in play
_AttackResponse = AdvTag(
    "_AttackResponse", wantsTags=[_Attack]
)  # allows you to respond to attacks. Wants for Attacks
_BadSifter = AdvTag("_BadSifter")  # attacks by messing up your deck
_BadThinner = AdvTag("_BadThinner")  # attacks by trashing good things
_BottomSeeder = AdvTag("_BottomSeeder")  # puts cards on the bottom of your deck.
_Buys = AdvTag("_Buys")  # allow you to buy more cards in a turn.
_Cantrip = AdvTag(
    "_Cantrip"
)  # card draws and chains, which essentially makes it a free bonus card
_CardLover = AdvTag("_CardLover")  # wants a lot of cards in play
_Chainer = AdvTag("_Chainer")  # allows you to play another action after it is done
_Choice = AdvTag("_Choice")  # gives you a set of choices
_Cost0 = AdvTag("_Cost0")  # card costs 0
_Cost1 = AdvTag("_Cost1")  # card costs 1
_Cost2 = AdvTag("_Cost2")  # card costs 2
_Cost2Response = AdvTag("_Cost2Response", wantsTags=[_Cost2])  # Wants cards that cost 2
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
    "_DeckGuesser", bonusToTags=["_DeckSeeder"]
)  # allows you to guess cards from the top of your deck. wants for _DeckSeeder
_Discard = AdvTag("_Discard")  # discards cards because sometimes you want to do that
_DiscardResponse = AdvTag(
    "_DiscardResponse", wantsTags=["_Discard"]
)  # Reaction triggered by discards other than cleanup. Wants _Discard
_DoubleDouble = AdvTag(
    "_DoubleDouble"
)  # gives 2 actions and 2 draw. OP with a downside.
_Downgrader = AdvTag("_Downgrader")  # attack card that does upgrades in reverse
_Draw1 = AdvTag("_Draw1")  # draws 1 card
_Draw2 = AdvTag("_Draw2")  # draws 2 cards
_Draw3 = AdvTag("_Draw3")  # draws 3 cards
_Draw4 = AdvTag("_Draw4")  # draws 4 cards
_Draw5 = AdvTag("_Draw5")  # draws 5 cards
_Draw6 = AdvTag("_Draw6")  # draws 6 cards
_Draw7 = AdvTag("_Draw7")  # draws 7 cards
_Drawload = AdvTag("_Drawload")  # draws potentially infinite numbers of cards
_Piler = AdvTag("_Piler")  # empties or refils piles
_Empty = AdvTag("_Empty")  # cares about empty supply piles
_Piler.bonusToTags = [_Empty]
_Empty.bonusToTags = [_Piler]
_Exchange = AdvTag(
    "_Exchange"
)  # allows you to exchange cards, triggering on-gain effects before the exchange
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
_FutureDraw1 = AdvTag("_FutureDraw1")  # gives a draw at the start of a future turn
_FutureDraw2 = AdvTag("_FutureDraw2")  # gives draw 2 at the start of a future turn
_FutureDraw5 = AdvTag("_FutureDraw5")  # gives draw 5 at the start of a future turn
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
_ExactGainer3 = AdvTag(
    "_ExactGainer3",
    bonusToTags=[_Cost3, _CostReducer],
    badTags=["_ExtraCost"],
    wantsTags=[_Cost3],
)  # allows you to gain cards from the supply costing exactly 3; synnergizes with _Cost3, _CostReducer
_ExactGainer4 = AdvTag(
    "_ExactGainer4",
    bonusToTags=[_Cost4, _CostReducer],
    badTags=["_ExtraCost"],
    wantsTags=[_Cost4],
)  # allows you to gain cards from the supply costing exactly 4; synnergizes with _Cost4, _CostReducer
_ExactGainer5 = AdvTag(
    "_ExactGainer5",
    bonusToTags=[_Cost5, _CostReducer],
    badTags=["_ExtraCost"],
    wantsTags=[_Cost5],
)  # allows you to gain cards from the supply costing exactly 5; synnergizes with _Cost5, _CostReducer
_ExactGainer6 = AdvTag(
    "_ExactGainer6",
    bonusToTags=[_Cost6, _CostReducer],
    badTags=["_ExtraCost"],
    wantsTags=[_Cost6],
)  # allows you to gain cards from the supply costing exactly 6; synnergizes with _Cost6, _CostReducer
_Gainer3 = AdvTag(
    "_Gainer3", bonusToTags=[_Cost3, _CostReducer], badTags=["_ExtraCost"]
)  # allows you to gain cards from the supply costing up to 3; synnergizes with _CostReducer, _Cost3
_Gainer4 = AdvTag(
    "_Gainer4", bonusToTags=[_Cost4, _CostReducer], badTags=["_ExtraCost"]
)  # allows you to gain cards from the supply costing up to 4; synnergizes with _CostReducer, _Cost4
_Gainer5 = AdvTag(
    "_Gainer5", bonusToTags=[_Cost5, _CostReducer], badTags=["_ExtraCost"]
)  # allows you to gain cards from the supply costing up to 5; synnergizes with _CostReducer, _Cost5
_Gainer6 = AdvTag(
    "_Gainer6", bonusToTags=[_Cost6, _CostReducer], badTags=["_ExtraCost"]
)  # allows you to gain cards from the supply costing up to 6; synnergizes with _CostReducer, _Cost6
_Gainer7 = AdvTag(
    "_Gainer7", bonusToTags=[_Cost7, _CostReducer], badTags=["_ExtraCost"]
)  # allows you to gain cards from the supply costing up to 7; synnergizes with _CostReducer, _Cost7

_GainResponse3 = AdvTag(
    "_GainResponse3",
    bonusToTags=[
        _ExactGainer3,
        _Exchange,
        _Gainer3,
        _Gainer4,
        _Gainer5,
        _Gainer6,
    ],
)  # Reaction triggered by gains.
_GainResponse4 = AdvTag(
    "_GainResponse4",
    bonusToTags=[_ExactGainer4, _Exchange, _Gainer4, _Gainer5, _Gainer6],
)  # Reaction triggered by gains.
_GainResponse5 = AdvTag(
    "_GainResponse5", bonusToTags=[_ExactGainer5, _Exchange, _Gainer5, _Gainer6]
)  # Reaction triggered by gains.
_GainResponse6 = AdvTag(
    "_GainResponse6", bonusToTags=[_ExactGainer6, _Gainer6, _Exchange]
)  # Reaction triggered by gains.
_Exchange.bonusToTags = [_GainResponse3, _GainResponse4, _GainResponse5, _GainResponse6]
_Kingdom = AdvTag("_Kingdom")  # Adds cards to the kingdom
_Interactive = AdvTag(
    "_Interactive"
)  # does something to other players that is not an attack
_Lab = AdvTag("_Lab")  # gives +2 Cards and +1 Action
_LimitsPlays = AdvTag("_LimitsPlays")  # limits the number of cards you can play
_Junker = AdvTag("_Junker")  # attacker gives opponents bad cards
_Money1 = AdvTag("_Money1")  # gives +1 Money
_Money2 = AdvTag("_Money2")  # gives +2 Money
_Money3 = AdvTag("_Money3")  # gives +3 Money
_Money4 = AdvTag("_Money4")  # gives +4 Money
_Money5 = AdvTag("_Money5")  # gives +5 Money
_Money6 = AdvTag("_Money6")  # gives +6 Money
_MultiType = AdvTag("_MultiType")  # has more than two types
_MultiTypeLove = AdvTag(
    "_MultiTypeLove", wantsTags=[_MultiType]
)  # Wants cards with more than two types
_Payload = AdvTag("_Payload")  # a card that adds variable, potentially infinite money.
_NoHandsPlay = AdvTag(
    "_NoHandsPlay"
)  # allows you to play cards without having them in your hand
_LimitsPlays.bonusToTags = [_NoHandsPlay]
_Overpay = AdvTag(
    "_Overpay", [_FutureMoney2, _Money3, _Money4, _Money5, _Money6, _Payload]
)  # Allows you to pay more for more functionality. Synnergizes with _Money3, _Money4, _Money5, _Payload.
_Peddler = AdvTag(
    "_Peddler"
)  # cantrip that give +1 Money; seperate class for randomizer reasons
_Terminal = AdvTag(
    "_Terminal"
)  # doesn't allow more actions to be played. synnergizes with _Splitter and _Village
_LimitsPlays.bonusToTags = [_NoHandsPlay, _Terminal]
_PhaseBreaker = AdvTag(
    "_PhaseBreaker", bonusToTags=[_Buys, _Terminal]
)  # messes with the phases. I want this separate because it's interesting
_PlayArea = AdvTag(
    "_PlayArea"
)  # Affects the play area. I want this seperate because it's interesting
_Prize = AdvTag("_Prize")  # the card gives access to powerful prizes
_Random = AdvTag("_Random")  # a card with seemly random effects (as opposed to _Choice)
_Reveal = AdvTag(
    "_Reveal"
)  # a card that makes you reveal other cards, explicitly using the word reveal
_RevealResponse = AdvTag(
    "_RevealResponse", [_Doom, _Reveal]
)  # a card that reacts to being revealed, Wants _Reveal or Doom
_Saver = AdvTag(
    "_Saver"
)  # puts cards from this hand into future hands, without discards or draws
_ShuffleIn = AdvTag("_ShuffleIn")  # shuffles cards into other piles
_Shuffler = AdvTag("_Shuffler")  # triggers the next shuffle right away
_Sifter = AdvTag(
    "_Sifter", bonusToTags=[_Discard]
)  # draws and discards cards to improve future hands
_SplitPile = AdvTag("_SplitPile")  # There's more than one named thing in here!
_NamesMatter = AdvTag(
    "_NamesMatter", [_Looter, _Kingdom, _Prize, _SplitPile]
)  # Wants a lot of different names in the game. Synnergizes with Looter, _SplitPile, etc
_Splitter = AdvTag(
    "_Splitter", bonusToTags=[_Terminal]
)  # allows you to play cards multiple times.
_Thinner = AdvTag(
    "_Thinner"
)  # Puts cards into the trash and leaves you with a smaller deck
_Trasher = AdvTag("_Trasher")  # Puts cards into the trash, but doesn't thin your deck
_TrashResponse = AdvTag(
    "_TrashResponse", wantsTags=[_Trasher]
)  # Responds to trashing or being trashed. Wants for _Trasher
_TrashGainer = AdvTag(
    "_TrashGainer", wantsTags=[_Trasher]
)  # Gets cards out of the trash or gains cards in response to trashing. Wants for _Trasher
_TreasuresMatter = AdvTag(
    "_TreasuresMatter", bonusToTags=[_Treasure, _Potion, _Prize]
)  # Increases in power if there are more differently named Treasures in tha game
_Twin = AdvTag(
    "_Twin"
)  # Donald X's secret type that is a good idea to buy 2 of on turn 1
_Remodeler = AdvTag(
    "_Remodeler",
    bonusToTags=[_Cost3, _Cost4, _Cost5, _Cost6, _Cost7],
)  # allows you to trash cards and replace them with better cards. Encourages an unbroken upgrade path to Province
_VictoryGainer = AdvTag("_VictoryGainer")  # gains you victory cards or points
_VictoryResponse = AdvTag(
    "_AttackResponse", bonusToTags=[_Gainer5], wantsTags=[_VictoryGainer]
)  # allows you to respond to other players gaining victory cards. Wants for victory cards, encourages gainers
_Village = AdvTag(
    "_Village", bonusToTags=[_Terminal]
)  # replaces itself and allows multiple terminals to be played
_ActionLover.bonusToTags = [_Village]
_CardLover.bonusToTags = [_Cantrip, _Village]

# Define sets
Base = Set("Base")
Base.AddCards(
    [
        {
            "name": "Artisan",
            "types": {Action},
            "advTags": {_Cost6, _DeckSeeder, _Gainer5, _Terminal},
        },
        {
            "name": "Bandit",
            "types": {Action, Attack},
            "advTags": {
                _BadThinner,
                _Cost5,
                _Discard,
                _FutureMoney2,
                _Reveal,
                _Terminal,
            },
        },
        {
            "name": "Bureaucrat",
            "types": {Action, Attack},
            "advTags": {
                _BadSifter,
                _Cost4,
                _DeckSeeder,
                _FutureMoney1,
                _Reveal,
                _Terminal,
            },
        },
        {
            "name": "Cellar",
            "types": {Action},
            "advTags": {_Chainer, _Cost2, _Discard, _Drawload},
        },
        {
            "name": "Chapel",
            "types": {Action},
            "advTags": {_Cost2, _Terminal, _Thinner, _Trasher},
        },
        {
            "name": "Council Room",
            "types": {Action},
            "advTags": {_Buys, _Cost5, _Draw4, _Interactive, _Terminal},
        },
        {
            "name": "Festival",
            "types": {Action},
            "advTags": {_Buys, _Cost5, _Money2, _Village},
        },
        {"name": "Gardens", "types": {Victory}, "advTags": {_Cost4}},
        {
            "name": "Harbinger",
            "types": {Action},
            "advTags": {_Cantrip, _Cost3, _DeckSeeder},
        },
        {
            "name": "Laboratory",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _Draw2},
        },
        {
            "name": "Library",
            "types": {Action},
            "advTags": {_Cost5, _Filler, _Sifter, _Terminal},
        },
        {"name": "Market", "types": {Action}, "advTags": {_Buys, _Cost5, _Peddler}},
        {"name": "Merchant", "types": {Action}, "advTags": {_Peddler, _Cost3}},
        {
            "name": "Militia",
            "types": {Action, Attack},
            "advTags": {_Cost4, _Discard, _Money2, _Terminal},
        },
        {
            "name": "Mine",
            "types": {Action},
            "advTags": {_Cost5, _Remodeler, _Terminal, _Trasher},
        },
        {
            "name": "Moat",
            "types": {Action, Reaction},
            "advTags": {_AttackResponse, _Cost2, _Draw2, _Terminal},
        },
        {
            "name": "Moneylender",
            "types": {Action},
            "advTags": {_Cost4, _Money3, _Terminal, _Thinner, _Trasher},
        },
        {
            "name": "Poacher",
            "types": {Action},
            "advTags": {_Cost4, _Discard, _Empty, _Peddler},
        },
        {
            "name": "Remodel",
            "types": {Action},
            "advTags": {_Cost4, _Remodeler, _Terminal, _Trasher},
        },
        {
            "name": "Sentry",
            "types": {Action},
            "advTags": {
                _Cantrip,
                _Cost5,
                _DeckSeeder,
                _Discard,
                _Sifter,
                _Trasher,
                _Thinner,
            },
        },
        {"name": "Smithy", "types": {Action}, "advTags": {_Cost4, _Draw3, _Terminal}},
        {"name": "Throne Room", "types": {Action}, "advTags": {_Cost4, _Splitter}},
        {
            "name": "Workshop",
            "types": {Action},
            "advTags": {_Cost3, _Gainer4, _Terminal},
        },
        {
            "name": "Vassal",
            "types": {Action},
            "advTags": {
                _Chainer,
                _Cost3,
                _DeckGuesser,
                _Discard,
                _Money2,
                _NoHandsPlay,
                _Twin,
            },
        },
        {"name": "Village", "types": {Action}, "advTags": {_Cost3, _Village}},
        {"name": "Witch", "types": {Action}, "advTags": {_Cost5, _Curser, _Terminal}},
    ]
)
Base.firstEdition = [
    {
        "name": "Adventurer",
        "types": {Action},
        "advTags": {_Cost6, _Reveal, _Sifter, _Terminal},
    },
    {
        "name": "Chancellor",
        "types": {Action},
        "advTags": {_Cost3, _Money2, _Shuffler, _Terminal},
    },
    {
        "name": "Feast",
        "types": {Action},
        "advTags": {_Cost4, _Gainer5, _Terminal, _Trasher},
    },
    {
        "name": "Spy",
        "types": {Action, Attack},
        "advTags": {
            _BadSifter,
            _Cantrip,
            _Cost4,
            _DeckSeeder,
            _Discard,
            _Reveal,
            _Sifter,
        },
    },
    {
        "name": "Thief",
        "types": {Action, Attack},
        "advTags": {
            _BadThinner,
            _Cost4,
            _Discard,
            _FutureMoney2,
            _Gainer6,
            _Reveal,
            _Terminal,
            _Trasher,
        },
    },
    {
        "name": "Woodcutter",
        "types": {Action},
        "advTags": {_Buys, _Cost3, _Money2, _Terminal},
    },
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
            "types": {Action},
            "advTags": {_Buys, _Cost4, _Discard, _Money4, _Terminal, _VictoryGainer},
        },
        {
            "name": "Bridge",
            "types": {Action},
            "advTags": {_Buys, _Cost4, _CostReducer, _Money1, _Terminal},
        },
        {
            "name": "Conspirator",
            "types": {Action},
            "advTags": {_ActionLover, _Cost4, _Cantrip, _Money2},
        },
        {
            "name": "Courtier",
            "types": {Action},
            "advTags": {
                _Buys,
                _Chainer,
                _Choice,
                _Cost5,
                _FutureMoney2,
                _Money3,
                _MultiTypeLove,
                _Reveal,
                _Terminal,
            },
        },
        {
            "name": "Courtyard",
            "types": {Action},
            "advTags": {_Cost2, _DeckSeeder, _Draw2, _Terminal},
        },  # draws 2 and seeds 1
        {
            "name": "Diplomat",
            "types": {Action, Reaction},
            "advTags": {
                _ActionLover,
                _AttackResponse,
                _Cost4,
                _Discard,
                _DoubleDouble,
                _Reveal,
                _Sifter,
                _Terminal,
            },
        },
        {"name": "Duke", "types": {Victory}, "advTags": {_Cost5}},
        {"name": "Harem", "types": {Treasure, Victory}, "advTags": {_Cost6, _Money2}},
        {
            "name": "Ironworks",
            "types": {Action},
            "advTags": {_Cantrip, _Cost4, _Gainer4, _Money1, _MultiTypeLove},
        },
        {
            "name": "Lurker",
            "types": {Action},
            "advTags": {_Cost2, _Chainer, _Piler, _Trasher, _TrashGainer},
        },
        {
            "name": "Masquerade",
            "types": {Action},
            "advTags": {
                _Cost3,
                _Draw2,
                _Interactive,
                _Junker,
                _Terminal,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Mill",
            "types": {Action, Victory},
            "advTags": {_Cantrip, _Cost4, _Discard, _Money2},
        },
        {
            "name": "Mining Village",
            "types": {Action},
            "advTags": {_Cost4, _Money2, _Thinner, _Trasher, _Village},
        },
        {
            "name": "Minion",
            "types": {Action, Attack},
            "advTags": {
                _BadSifter,
                _Chainer,
                _Choice,
                _Cost5,
                _Discard,
                _Money2,
                _Sifter,
            },
        },
        {
            "name": "Nobles",
            "types": {Action, Victory},
            "advTags": {_Choice, _Cost6, _Draw3, _Village},
        },
        {
            "name": "Patrol",
            "types": {Action},
            "advTags": {_Cost5, _Draw3, _Reveal, _Sifter, _Terminal},
        },
        {
            "name": "Pawn",
            "types": {Action},
            "advTags": {_Buys, _Cantrip, _Choice, _Cost2, _Draw1, _Money1},
        },
        {
            "name": "Replace",
            "types": {Action, Attack},
            "advTags": {
                _Cost5,
                _Curser,
                _DeckSeeder,
                _Remodeler,
                _Terminal,
                _Trasher,
            },
        },
        {
            "name": "Secret Passage",
            "types": {Action},
            "advTags": {_Lab, _Cost4, _DeckSeeder},
        },
        {
            "name": "Shanty Town",
            "types": {Action},
            "advTags": {_Cost3, _Draw2, _Reveal, _Twin, _Village},
        },
        {
            "name": "Steward",
            "types": {Action},
            "advTags": {
                _Choice,
                _Cost3,
                _Draw2,
                _Money2,
                _Terminal,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Swindler",
            "types": {Action, Attack},
            "advTags": {_Cost3, _Downgrader, _Money2, _Terminal, _Trasher},
        },
        {
            "name": "Torturer",
            "types": {Action, Attack},
            "advTags": {_Choice, _Cost5, _Curser, _Discard, _Draw3, _Terminal},
        },
        {
            "name": "Trading Post",
            "types": {Action},
            "advTags": {_Cost5, _FutureMoney1, _Terminal, _Thinner},
        },
        {
            "name": "Upgrade",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _Remodeler, _Trasher},
        },
        {
            "name": "Wishing Well",
            "types": {Action},
            "advTags": {_Cantrip, _Cost3, _DeckGuesser, _Draw2, _Reveal},
        },
    ]
)
Intrigue.firstEdition = [
    {
        "name": "Coppersmith",
        "types": {Action},
        "advTags": {_Cost4, _Payload, _Terminal},
    },
    {"name": "Great Hall", "types": {Action, Victory}, "advTags": {_Cantrip, _Cost3}},
    {
        "name": "Saboteur",
        "types": {Action, Attack},
        "advTags": {
            _Downgrader,
            _Cost5,
            _Discard,
            _Reveal,
            _Terminal,
            _Trasher,
        },
    },
    {
        "name": "Scout",
        "types": {Action},
        "advTags": {_Cantrip, _Cost4, _DeckSeeder, _Drawload, _Reveal, _Sifter},
    },
    {
        "name": "Secret Chamber",
        "types": {Action, Reaction},
        "advTags": {
            _AttackResponse,
            _Cost2,
            _DeckSeeder,
            _Discard,
            _Payload,
            _Sifter,
            _Terminal,
        },
    },
    {
        "name": "Tribute",
        "types": {Action},
        "advTags": {_Choice, _Cost5, _Discard, _MultiTypeLove, _Reveal},
    },
]
Intrigue.secondEdition = Intrigue.cards(
    "Courtier", "Diplomat", "Lurker", "Mill", "Patrol", "Replace", "Secret Passage"
)

Seaside = Set("Seaside")
Seaside.AddCards(
    [
        {
            "name": "Astrolabe",
            "types": {Treasure, Duration},
            "advTags": {_Buys, _Cost3, _FutureMoney1, _Money1},
        },
        {"name": "Bazaar", "types": {Action}, "advTags": {_Cost5, _Peddler, _Village}},
        {
            "name": "Blockade",
            "types": {Action, Duration, Attack},
            "advTags": {
                _Cost4,
                _Curser,
                _Gainer4,
                _GainResponse4,
                _MultiType,
                _Saver,
                _Terminal,
            },
        },
        {
            "name": "Caravan",
            "types": {Action, Duration},
            "advTags": {_Cantrip, _Cost4, _FutureDraw1},
        },
        {
            "name": "Corsair",
            "types": {Action, Duration, Attack},
            "advTags": {
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
            "types": {Action, Attack},
            "advTags": {_Cost4, _Discard, _Reveal, _Money2, _Terminal},
        },
        {
            "name": "Fishing Village",
            "types": {Action, Duration},
            "advTags": {_Cost3, _FutureAction, _FutureMoney1, _Money1, _Village},
        },
        {
            "name": "Haven",
            "types": {Action, Duration},
            "advTags": {_Cantrip, _Cost2, _Saver},
        },
        {
            "name": "Island",
            "types": {Action, Victory},
            "advTags": {_Cost4, _Terminal, _Thinner},
        },
        {
            "name": "Lighthouse",
            "types": {Action, Duration},
            "advTags": {_AttackResponse, _Chainer, _Cost2, _FutureMoney1, _Money1},
        },
        {
            "name": "Lookout",
            "types": {Action},
            "advTags": {
                _Chainer,
                _Cost3,
                _DeckSeeder,
                _Discard,
                _Sifter,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Merchant Ship",
            "types": {Action, Duration},
            "advTags": {_Cost5, _Money4, _Terminal},
        },
        {
            "name": "Monkey",
            "types": {Action, Duration},
            "advTags": {_Cost3, _GainResponse6, _FutureDraw1, _Terminal},
        },
        {
            "name": "Native Village",
            "types": {Action},
            "advTags": {_Choice, _Cost2, _Drawload, _Saver, _Thinner, _Village},
        },
        {
            "name": "Outpost",
            "types": {Action, Duration},
            "advTags": {_Cost5, _Draw3, _Terminal},
        },
        {
            "name": "Pirate",
            "types": {Action, Duration, Reaction},
            "advTags": {
                _Cost5,
                _FreeAction,
                _FutureMoney2,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Sailor",
            "types": {Action, Duration},
            "advTags": {
                _Cost4,
                _GainResponse6,
                _FutureMoney2,
                _Shuffler,
                _Thinner,
                _Trasher,
                _Village,
            },
        },
        {
            "name": "Salvager",
            "types": {Action},
            "advTags": {_Buys, _Cost4, _Payload, _Terminal, _Thinner, _Trasher},
        },
        {
            "name": "Sea Chart",
            "types": {Action},
            "advTags": {_Cantrip, _Cost3, _DeckGuesser, _Draw2, _Reveal, _Twin},
        },
        {
            "name": "Sea Witch",
            "types": {Action, Duration, Attack},
            "advTags": {
                _Cost5,
                _Curser,
                _Discard,
                _Draw2,
                _MultiType,
                _Sifter,
                _Terminal,
            },
        },
        {
            "name": "Smugglers",
            "types": {Action},
            "advTags": {_Cost3, _Gainer6, _GainResponse6, _Terminal},
        },
        {
            "name": "Tactician",
            "types": {Action, Duration},
            "advTags": {
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
            "types": {Action, Duration},
            "advTags": {_Cantrip, _Cost4, _Discard, _Sifter},
        },
        {
            "name": "Treasure Map",
            "types": {Action},
            "advTags": {_Cost4, _DeckSeeder, _FutureMoney6, _Trasher, _Terminal},
        },
        {
            "name": "Treasury",
            "types": {Action},
            "advTags": {_Cost5, _DeckSeeder, _Peddler},
        },
        {
            "name": "Warehouse",
            "types": {Action},
            "advTags": {_Chainer, _Cost3, _Discard, _Sifter},
        },
        {
            "name": "Wharf",
            "types": {Action, Duration},
            "advTags": {_Buys, _Cost5, _Draw4, _Terminal},
        },
    ]
)
Seaside.firstEdition = [
    {
        "name": "Ambassador",
        "types": {Action, Attack},
        "advTags": {_Cost3, _Junker, _Reveal, _Terminal, _Thinner},
    },
    {
        "name": "Embargo",
        "types": {Action},
        "advTags": {_Cost2, _Curser, _Money2, _Thinner, _Trasher},
    },
    {
        "name": "Explorer",
        "types": {Action},
        "advTags": {_Cost5, _FutureMoney1, _FutureMoney2, _Reveal, _Terminal},
    },
    {
        "name": "Ghost Ship",
        "types": {Action, Attack},
        "advTags": {_Cost5, _Draw2, _BadSifter, _Terminal},
    },
    {
        "name": "Navigator",
        "types": {Action},
        "advTags": {_Cost4, _DeckSeeder, _Discard, _Money2, _Sifter, _Terminal},
    },
    {
        "name": "Pearl Diver",
        "types": {Action},
        "advTags": {_Cantrip, _Cost2, _DeckSeeder},
    },
    {
        "name": "Pirate Ship",
        "types": {Action, Attack},
        "advTags": {_BadThinner, _Cost4, _Discard, _Payload, _Reveal, _Terminal},
    },
    {
        "name": "Sea Hag",
        "types": {Action, Attack},
        "advTags": {_Cost4, _Curser, _DeckSeeder, _Discard, _Terminal},
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
            "types": {Action, Potion},
            "advTags": {_Cantrip, _Cost3, _DeckSeeder, _Draw2, _ExtraCost},
        },
        {
            "name": "Apothecary",
            "types": {Action, Potion},
            "advTags": {_DeckSeeder, _ExtraCost, _Money4, _Reveal, _Sifter, _Peddler},
        },
        {
            "name": "Apprentice",
            "types": {Action},
            "advTags": {_Chainer, _Cost5, _Drawload, _Thinner, _Trasher},
        },
        {
            "name": "Familiar",
            "types": {Action, Attack, Potion},
            "advTags": {_Cantrip, _Cost3, _Curser, _ExtraCost},
        },
        {
            "name": "Golem",
            "types": {Action, Potion},
            "advTags": {_ExtraCost, _NoHandsPlay, _Reveal, _Village},
        },
        {
            "name": "Herbalist",
            "types": {Action},
            "advTags": {_Buys, _Cost2, _DeckSeeder, _Money1, _PlayArea, _Terminal},
        },
        {
            "name": "Philosopher's Stone",
            "types": {Treasure, Potion},
            "advTags": {_ExtraCost, _Payload},
        },
        {
            "name": "Possession",
            "types": {Action, Potion},
            "advTags": {_Buys, _Draw5, _ExtraCost, _Terminal},
        },
        {
            "name": "Scrying Pool",
            "types": {Action, Attack, Potion},
            "advTags": {
                _BadSifter,
                _Cantrip,
                _Cost2,
                _Discard,
                _Drawload,
                _ExtraCost,
                _Reveal,
                _Sifter,
            },
        },
        {
            "name": "Transmute",
            "types": {Action, Potion},
            "advTags": {
                _ExtraCost,
                _FutureMoney2,
                _MultiTypeLove,
                _Terminal,
                _Trasher,
                _VictoryGainer,
            },
        },
        {
            "name": "University",
            "types": {Action, Potion},
            "advTags": {_Cost2, _ExtraCost, _Gainer5, _Village},
        },
        {"name": "Vineyard", "types": {Victory, Potion}, "advTags": {_ExtraCost}},
    ]
)

Prosperity = Set("Prosperity")
Prosperity.AddCards(
    [
        {
            "name": "Anvil",
            "types": {Treasure},
            "advTags": {_Cost3, _Discard, _Gainer4, _Money1},
        },
        {"name": "Bank", "types": {Treasure}, "advTags": {_Cost7, _Payload}},
        {
            "name": "Bishop",
            "types": {Action},
            "advTags": {
                _Cost4,
                _Interactive,
                _Money1,
                _Terminal,
                _Thinner,
                _Trasher,
                _TrashResponse,
                _VictoryGainer,
            },
        },
        {
            "name": "Charlatan",
            "types": {Action, Attack},
            "advTags": {_Cost5, _Curser, _Money3, _Terminal},
        },
        {
            "name": "City",
            "types": {Action},
            "advTags": {_Buys, _Cost5, _Draw2, _Empty, _Money1, _Village},
        },
        {
            "name": "Clerk",
            "types": {Action, Reaction, Attack},
            "advTags": {
                _BadSifter,
                _Cost4,
                _DeckSeeder,
                _FreeAction,
                _Money2,
                _Terminal,
            },
        },
        {
            "name": "Collection",
            "types": {Treasure},
            "advTags": {_Buys, _Cost5, _Money2, _GainResponse5, _VictoryGainer},
        },
        {
            "name": "Crystal Ball",
            "types": {Treasure},
            "advTags": {_Cost5, _Discard, _FreeAction, _Money1, _Thinner, _Trasher},
        },
        {
            "name": "Expand",
            "types": {Action},
            "advTags": {
                _Cost7,
                _Remodeler,
                _Terminal,
                _Trasher,
            },
        },
        {"name": "Forge", "types": {Action}, "advTags": {_Cost7, _Terminal, _Thinner}},
        {
            "name": "Grand Market",
            "types": {Action},
            "advTags": {_Buys, _Cost6, _Money2, _Peddler},
        },
        {"name": "Hoard", "types": {Treasure}, "advTags": {_Cost6, _Money2, _Payload}},
        {
            "name": "Investment",
            "types": {Treasure},
            "advTags": {
                _Cost4,
                _Money1,
                _Reveal,
                _Thinner,
                _Trasher,
                _TreasuresMatter,
                _VictoryGainer,
            },
        },
        {"name": "King's Court", "types": {Action}, "advTags": {_Cost7, _Splitter}},
        {
            "name": "Magnate",
            "types": {Action},
            "advTags": {_Cost5, _Drawload, _Reveal, _Terminal},
        },
        {
            "name": "Mint",
            "types": {Action},
            "advTags": {_Cost5, _FutureMoney2, _Terminal, _Thinner},
        },
        {
            "name": "Monument",
            "types": {Action},
            "advTags": {_Cost4, _Money2, _Terminal, _VictoryGainer},
        },
        {
            "name": "Peddler",
            "types": {Action},
            "advTags": {
                _ActionLover,
                _Cost8,
                _CostVaries,
                _Peddler,
            },
        },
        {
            "name": "Quarry",
            "types": {Treasure},
            "advTags": {_Cost4, _CostReducer, _Money1},
        },
        {
            "name": "Rabble",
            "types": {Action, Attack},
            "advTags": {_BadSifter, _Cost5, _Draw3, _Reveal, _Terminal},
        },
        {
            "name": "Tiara",
            "types": {Treasure},
            "advTags": {_Buys, _Cost4, _DeckSeeder, _GainResponse6, _Splitter},
        },
        {"name": "War Chest", "types": {Treasure}, "advTags": {_Cost5, _Gainer5}},
        {
            "name": "Vault",
            "types": {Action},
            "advTags": {_Cost5, _Draw2, _Discard, _Payload, _Terminal},
        },
        {
            "name": "Watchtower",
            "types": {Action, Reaction},
            "advTags": {
                _Cost3,
                _DeckSeeder,
                _Filler,
                _GainResponse6,
                _Reveal,
                _Terminal,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Worker's Village",
            "types": {Action},
            "advTags": {_Buys, _Cost4, _Village},
        },
    ]
)
Prosperity.firstEdition = [
    {"name": "Contraband", "types": {Treasure}, "advTags": {_Buys, _Cost5, _Money3}},
    {
        "name": "Counting House",
        "types": {Action},
        "advTags": {_Cost5, _Payload, _Terminal},
    },
    {
        "name": "Goons",
        "types": {Action, Attack},
        "advTags": {
            _Buys,
            _Cost6,
            _Discard,
            _Money2,
            _Terminal,
            _VictoryGainer,
        },
    },
    {
        "name": "Loan",
        "types": {Treasure},
        "advTags": {_Cost3, _Discard, _Money1, _Reveal, _Thinner, _Trasher},
    },
    {
        "name": "Mountebank",
        "types": {Action, Attack},
        "advTags": {_Cost5, _Curser, _Junker, _Money2},
    },
    {
        "name": "Royal Seal",
        "types": {Treasure},
        "advTags": {_Cost5, _Money2, _Shuffler},
    },
    {
        "name": "Talisman",
        "types": {Treasure},
        "advTags": {_Cost4, _Gainer4, _GainResponse4, _Money1},
    },
    {
        "name": "Trade Route",
        "types": {Action},
        "advTags": {_Buys, _Cost3, _Payload, _Thinner, _Trasher, _VictoryResponse},
    },
    {
        "name": "Venture",
        "types": {Treasure},
        "advTags": {_Cost5, _Money1, _Reveal, _Shuffler},
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
        {"name": "Fairgrounds", "types": {Victory}, "advTags": {_Cost6, _NamesMatter}},
        {
            "name": "Fortune Teller",
            "types": {Action, Attack},
            "advTags": {
                _BadSifter,
                _Cost3,
                _DeckSeeder,
                _Discard,
                _Money2,
                _Reveal,
                _Terminal,
            },
        },
        {
            "name": "Hamlet",
            "types": {Action},
            "advTags": {_Buys, _Cantrip, _Choice, _Cost2, _Discard, _Village},
        },
        {
            "name": "Horn of Plenty",
            "types": {Treasure},
            "advTags": {_Cost5, _NamesMatter, _Trasher},
        },
        {
            "name": "Menagerie",
            "types": {Action},
            "advTags": {_Cantrip, _Cost3, _Draw3, _NamesMatter, _Reveal},
        },
        {
            "name": "Farming Village",
            "types": {Action},
            "advTags": {_Cost4, _Discard, _Sifter, _Reveal, _Village},
        },
        {
            "name": "Harvest",
            "types": {Action},
            "advTags": {
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
            "types": {Action, Reaction},
            "advTags": {
                _AttackResponse,
                _Buys,
                _Cost4,
                _Discard,
                _FutureDraw1,
                _Money3,
                _Saver,
                _Terminal,
            },
        },
        {
            "name": "Hunting Party",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _Discard, _Draw2, _Reveal},
        },
        {
            "name": "Jester",
            "types": {Action, Attack},
            "advTags": {_Cost5, _Curser, _Money2},
        },
        {
            "name": "Remake",
            "types": {Action},
            "advTags": {_Cost4, _Remodeler, _Terminal, _Trasher},
        },
        {
            "name": "Tournament",
            "types": {Action},
            "advTags": {
                _Cost4,
                _DeckSeeder,
                _Discard,
                _Interactive,
                _Peddler,
                _Prize,
                _Reveal,
                _VictoryGainer,
            },
        },
        {
            "name": "Young Witch",
            "types": {Action, Attack},
            "advTags": {
                _Cost4,
                _Curser,
                _Discard,
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
            "types": {Action, Attack},
            "advTags": {_Discard, _FreeAction, _Gainer4, _Terminal},
        },
        {
            "name": "Border Village",
            "types": {Action},
            "advTags": {_Cost6, _Gainer5, _GainResponse6, _Village},
        },
        {
            "name": "Cartographer",
            "types": {Action},
            "advTags": {_Cantrip, _DeckSeeder, _Discard, _Sifter},
        },
        {
            "name": "Cauldron",
            "types": {Treasure, Attack},
            "advTags": {_Buys, _Cost5, _Curser, _GainResponse5, _Money2},
        },
        {
            "name": "Crossroads",
            "types": {Action},
            "advTags": {_Cost2, _Drawload, _Reveal, _Village},
        },
        {
            "name": "Develop",
            "types": {Action},
            "advTags": {_Cost3, _DeckSeeder, _Remodeler, _Terminal, _Trasher, _Twin},
        },
        {
            "name": "Farmland",
            "types": {Victory},
            "advTags": {_Cost6, _Remodeler, _Trasher},
        },
        {
            "name": "Fool's Gold",
            "types": {Treasure, Reaction},
            "advTags": {
                _Cost2,
                _DeckSeeder,
                _FutureMoney2,
                _Money1,
                _Money4,
                _Trasher,
                _VictoryResponse,
            },
        },
        {
            "name": "Guard Dog",
            "types": {Action, Reaction},
            "advTags": {
                _AttackResponse,
                _Cost3,
                _Draw4,
                _FreeAction,
                _Terminal,
            },
        },
        {"name": "Haggler", "types": {Action}, "advTags": {_Cost5, _Money2, _Terminal}},
        {
            "name": "Tunnel",
            "types": {Victory, Reaction},
            "advTags": {
                _Cost3,
                _DiscardResponse,
                _FutureMoney2,
            },
        },
        {
            "name": "Highway",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _CostReducer},
        },
        {
            "name": "Inn",
            "types": {Action},
            "advTags": {_Cost5, _Discard, _Reveal, _Sifter, _Shuffler, _Village},
        },
        {
            "name": "Jack of All Trades",
            "types": {Action},
            "advTags": {
                _Cost4,
                _Discard,
                _Filler,
                _FutureMoney1,
                _Sifter,
                _Terminal,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Margrave",
            "types": {Action, Attack},
            "advTags": {
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
            "types": {Action},
            "advTags": {
                _Buys,
                _Cost4,
                _GainResponse4,
                _Money2,
                _Terminal,
                _TrashResponse,
            },
        },
        {
            "name": "Oasis",
            "types": {Action},
            "advTags": {_Chainer, _Cost3, _Discard, _Money1, _Sifter},
            # Not actually a cantrip because you don't increase your hand size
        },
        {
            "name": "Scheme",
            "types": {Action},
            "advTags": {_Cantrip, _Cost3, _DeckSeeder, _Saver},
        },
        {
            "name": "Souk",
            "types": {Action},
            "advTags": {
                _Buys,
                _Cost5,
                _GainResponse5,
                _Payload,
                _Terminal,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Spice Merchant",
            "types": {Action},
            "advTags": {
                _Buys,
                _Choice,
                _Cost4,
                _Lab,
                _Money2,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Stables",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _Discard, _Draw3},
        },
        {
            "name": "Trader",
            "types": {Action, Reaction},
            "advTags": {
                _Cost4,
                _Exchange,
                _GainResponse4,
                _Payload,
                _Terminal,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Trail",
            "types": {Action, Reaction},
            "advTags": {
                _Cantrip,
                _Cost4,
                _DiscardResponse,
                _FreeAction,
                _GainResponse4,
                _TrashResponse,
            },
        },
        {
            "name": "Tunnel",
            "types": {Victory, Reaction},
            "advTags": {_Cost3, _DiscardResponse, _FutureMoney2},
        },
        {
            "name": "Weaver",
            "types": {Action, Reaction},
            "advTags": {
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
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _Discard, _Gainer6, _Remodeler},
        },
        {
            "name": "Witch's Hut",
            "types": {Action, Attack},
            "advTags": {
                _Cost5,
                _Curser,
                _Discard,
                _Draw2,
                _Reveal,
                _Sifter,
                _Terminal,
            },
        },
    ]
)
Hinterlands.firstEdition = [
    {"name": "Cache", "types": {Treasure}, "advTags": {_Cost5, _Money3}},
    {
        "name": "Duchess",
        "types": {Action},
        "advTags": {
            _Cost2,
            _Discard,
            _GainResponse5,
            _Interactive,
            _Money2,
            _Sifter,
            _Terminal,
        },
    },
    {
        "name": "Embassy",
        "types": {Action},
        "advTags": {
            _Cost5,
            _Discard,
            _Draw2,
            _GainResponse5,
            _Interactive,
            _Sifter,
            _Terminal,
        },
    },
    {
        "name": "Ill-gotten Gains",
        "types": {Treasure},
        "advTags": {_Cost5, _Curser, _Money2},
    },
    {
        "name": "Mandarin",
        "types": {Action},
        "advTags": {_Cost5, _DeckSeeder, _Money3, _Terminal},
    },
    {
        "name": "Noble Brigand",
        "types": {Action, Attack},
        "advTags": {
            _BadThinner,
            _Cost4,
            _Discard,
            _FreeAction,
            _FutureMoney6,
            _GainResponse4,
            _Junker,
            _Money1,
            _Reveal,
            _Terminal,
            _Trasher,
        },
    },
    {
        "name": "Nomad Camp",
        "types": {Action},
        "advTags": {_Buys, _Cost4, _DeckSeeder, _GainResponse4, _Money2, _Terminal},
    },
    {
        "name": "Oracle",
        "types": {Action, Attack},
        "advTags": {
            _BadSifter,
            _Cost3,
            _DeckSeeder,
            _Discard,
            _Draw2,
            _Reveal,
            _Sifter,
            _Terminal,
        },
    },
    {"name": "Silk Road", "types": {Victory}, "advTags": {_Cost4}},
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
        {
            "name": "Altar",
            "types": {Action},
            "advTags": {_Cost6, _Gainer5, _Trasher, _Terminal},
        },
        {
            "name": "Armory",
            "types": {Action},
            "advTags": {_Cost4, _DeckSeeder, _Gainer4, _Terminal},
        },
        {
            "name": "Beggar",
            "types": {Action, Reaction},
            "advTags": {
                _AttackResponse,
                _Cost2,
                _DeckSeeder,
                _FutureMoney2,
                _Junker,
                _Money3,
                _Terminal,
            },
        },
        {
            "name": "Band of Misfits",
            "types": {Action, Command},
            "advTags": {_Command4, _Cost5},
        },
        {
            "name": "Bandit Camp",
            "types": {Action},
            "advTags": {_Cost5, _FutureMoney2, _Village},
        },
        {
            "name": "Catacombs",
            "types": {Action},
            "advTags": {
                _Choice,
                _Cost5,
                _Discard,
                _Draw3,
                _Gainer4,
                _Sifter,
                _TrashResponse,
                _Terminal,
            },
        },
        {
            "name": "Count",
            "types": {Action},
            "advTags": {
                _Cost5,
                _Choice,
                _DeckSeeder,
                _Discard,
                _Junker,
                _Money3,
                _Terminal,
                _Thinner,
                _Trasher,
                _VictoryGainer,
            },
        },
        {
            "name": "Counterfeit",
            "types": {Treasure},
            "advTags": {_Buys, _Cost5, _Money1, _Splitter, _Thinner, _Trasher},
        },
        {
            "name": "Cultist",
            "types": {Action, Attack},
            "advTags": {_Cost5, _Draw2, _Terminal, _TrashGainer},
        },
        {
            "name": "Death Cart",
            "types": {Action, Looter},
            "advTags": {
                _Cost4,
                _Junker,
                _Money5,
                _GainResponse4,
                _Terminal,
                _Thinner,
                _Trasher,
                _TrashResponse,
            },
        },
        {
            "name": "Feodum",
            "types": {Victory},
            "advTags": {_Cost4, _FutureMoney3, _TrashResponse},
        },
        {
            "name": "Forager",
            "types": {Action},
            "advTags": {
                _Buys,
                _Chainer,
                _Cost3,
                _Payload,
                _Thinner,
                _Trasher,
                _TreasuresMatter,
            },
        },
        {
            "name": "Fortress",
            "types": {Action},
            "advTags": {_Cost4, _TrashResponse, _Village},
        },
        {
            "name": "Hermit",  # and Madman
            "types": {Action},
            "advTags": {
                _Cost3,  # Hermit
                _Drawload,  # Madman
                _Exchange,  # Hermit
                _Gainer3,  # Hermit
                _Terminal,  # Hermit
                _Thinner,  # Madman
                _Trasher,  # Hermit
                _Village,  # Madman
            },
        },
        {
            "name": "Graverobber",
            "types": {Action},
            "advTags": {_Cost5, _Remodeler, _Terminal, _Trasher, _TrashGainer},
        },
        {
            "name": "Hunting Grounds",
            "types": {Action},
            "advTags": {_Cost6, _Draw4, _Terminal, _TrashGainer, _VictoryGainer},
        },
        {
            "name": "Ironmonger",
            "types": {Action},
            "advTags": {
                _Cost4,
                _DeckGuesser,
                _Discard,
                _DoubleDouble,
                _Money1,
                _MultiTypeLove,
                _Reveal,
            },
        },
        {
            "name": "Junk Dealer",
            "types": {Action},
            "advTags": {_Cost5, _Peddler, _Thinner, _Trasher},
        },
        {
            "name": "Knights",
            "types": {Action, Attack, Knight},
            "advTags": {
                _BadThinner,  # all
                _Buys,  # Sir Martin
                _Cantrip,
                _Cost4,  # all
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
                _Thinner,  # all
                _Trasher,  # all
                _TrashResponse,  # all
                _Village,
            },
        },
        {
            "name": "Marauder",
            "types": {Action, Attack, Looter},
            "advTags": {
                _Cost4,
                _FutureMoney2,
                _Junker,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Market Square",
            "types": {Action, Reaction},
            "advTags": {
                _Buys,
                _Cantrip,
                _Cost3,
                _FutureMoney2,
                _TrashResponse,
            },
        },
        {
            "name": "Mystic",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _DeckGuesser, _Reveal, _Money2},
        },
        {
            "name": "Pillage",
            "types": {Action, Attack},
            "advTags": {
                _Cost5,
                _Discard,
                _FutureMoney4,
                _Reveal,
                _Terminal,
                _Trasher,
            },
        },
        {
            "name": "Poor House",
            "types": {Action},
            "advTags": {_Cost1, _Money4, _Reveal, _Terminal},
        },
        {
            "name": "Procession",
            "types": {Action},
            "advTags": {_Cost4, _Splitter, _Remodeler, _Trasher},
        },
        {
            "name": "Rats",
            "types": {Action},
            "advTags": {_Cantrip, _Cost4, _Draw1, _Trasher, _TrashResponse},
        },
        {
            "name": "Rebuild",
            "types": {Action},
            "advTags": {
                _Chainer,
                _Cost5,
                _Discard,
                _Remodeler,
                _Reveal,
                _Trasher,
                _VictoryGainer,
            },
        },
        {
            "name": "Rogue",
            "types": {Action, Attack},
            "advTags": {
                _BadThinner,
                _Cost5,
                _Discard,
                _Money2,
                _Reveal,
                _Terminal,
                _TrashGainer,
            },
        },
        {
            "name": "Sage",
            "types": {Action},
            "advTags": {_Cantrip, _Cost3, _Discard, _Reveal, _Sifter},
        },
        {
            "name": "Scavenger",
            "types": {Action},
            "advTags": {_Cost4, _Money2, _DeckSeeder, _Shuffler, _Terminal},
        },
        {
            "name": "Squire",
            "types": {Action},
            "advTags": {
                _AttackResponse,
                _Buys,
                _Choice,
                _Cost2,
                _FutureMoney1,
                _Money1,
                _TrashResponse,
                _Village,
            },
        },
        {
            "name": "Storeroom",
            "types": {Action},
            "advTags": {
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
            "types": {Action, Attack},
            "advTags": {
                _AttackResponse,  # Urchin
                _Cantrip,  # Urchin
                _Cost3,  # Urchin
                _Discard,  # Urchin
                _Draw2,
                _Money2,
                _Thinner,
                _Terminal,
                _Trasher,  # Urchin
                _Twin,  # Urchin
            },
        },
        {
            "name": "Vagrant",
            "types": {Action},
            "advTags": {_Cantrip, _Cost2, _DeckGuesser, _Draw2, _Reveal},
        },
        {
            "name": "Wandering Minstrel",
            "types": {Action},
            "advTags": {_Cost4, _DeckSeeder, _Discard, _Reveal, _Sifter, _Village},
        },
    ]
)

Guilds = Set("Guilds")
Guilds.AddCards(
    [
        {
            "name": "Advisor",
            "types": {Action},
            "advTags": {_Cost4, _Discard, _Lab, _Interactive, _Reveal},
        },
        {
            "name": "Baker",
            "types": {Action},
            "advTags": {_Cantrip, _FutureMoney2, _Cost5},
        },
        {
            "name": "Candlestick Maker",
            "types": {Action},
            "advTags": {_Buys, _Chainer, _Cost2, _FutureMoney1},
        },
        {
            "name": "Butcher",
            "types": {Action},
            "advTags": {_Cost5, _FutureMoney2, _Remodeler, _Terminal, _Trasher},
        },
        {
            "name": "Doctor",
            "types": {Action},
            "advTags": {_Cost3, _Overpay, _Reveal, _Terminal, _Thinner},
        },
        {
            "name": "Herald",
            "types": {Action},
            "advTags": {
                _Cost4,
                _DeckGuesser,
                _DeckSeeder,
                _NoHandsPlay,
                _Overpay,
                _Reveal,
                _Village,
            },
        },
        {
            "name": "Journeyman",
            "types": {Action},
            "advTags": {
                _Cost5,
                _DeckGuesser,
                _Discard,
                _Draw3,
                _Reveal,
                _Sifter,
                _Terminal,
            },
        },
        {
            "name": "Masterpiece",
            "types": {Treasure},
            "advTags": {_Cost3, _Money1, _Overpay, _Payload},
        },
        {
            "name": "Merchant Guild",
            "types": {Action},
            "advTags": {_Buys, _Cost5, _Money1, _Payload, _Terminal},
        },
        {
            "name": "Plaza",
            "types": {Action},
            "advTags": {_FutureMoney1, _Cost4, _Discard, _Village},
        },
        {
            "name": "Stonemason",
            "types": {Action},
            "advTags": {_Cost2, _Gainer6, _Overpay, _Remodeler, _Trasher},
        },
        {
            "name": "Soothsayer",
            "types": {Action, Attack},
            "advTags": {_Cost5, _Curser, _Interactive, _Terminal},
        },
        {
            "name": "Taxman",
            "types": {Action, Attack},
            "advTags": {
                _BadSifter,
                _Cost4,
                _DeckSeeder,
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
            "types": {Action, Duration},
            "advTags": {
                _Choice,
                _Cost3,
                _FutureMoney1,
                _FutureMoney2,
                _Money1,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Artificer",
            "types": {Action},
            "advTags": {_Cost5, _Discard, _Peddler, _Remodeler},
        },
        {
            "name": "Bridge Troll",
            "types": {Action, Duration, Attack},
            "advTags": {_Buys, _Cost5, _CostReducer, _Terminal},
        },
        {
            "name": "Caravan Guard",
            "types": {Action, Duration, Reaction},
            "advTags": {
                _AttackResponse,
                _Cantrip,
                _Cost3,
                _FreeAction,
                _FutureMoney1,
                _MultiType,
            },
        },
        {
            "name": "Coin of the Realm",
            "types": {Treasure, Reserve},
            "advTags": {_Cost2, _PhaseBreaker, _Money1, _Village},
        },
        {
            "name": "Distant Lands",
            "types": {Action, Victory, Reserve},
            "advTags": {_Cost5, _MultiType},
        },
        {
            "name": "Dungeon",
            "types": {Action, Duration},
            "advTags": {_Chainer, _Cost3, _Discard, _Sifter},
        },
        {
            "name": "Gear",
            "types": {Action, Duration},
            "advTags": {_Cost3, _Saver, _Sifter, _Terminal, _Twin},
        },
        {
            "name": "Duplicate",
            "types": {Action, Reserve},
            "advTags": {_Cost4, _FreeAction, _Gainer6, _GainResponse6, _Terminal},
        },
        {
            "name": "Giant",
            "types": {Action, Attack},
            "advTags": {
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
            "types": {Action, Reserve},
            "advTags": {_Cantrip, _Cost3, _Discard, _Draw5, _FreeAction},
        },
        {
            "name": "Haunted Woods",
            "types": {Action, Duration, Attack},
            "advTags": {
                _BadSifter,
                _Cost5,
                _Draw3,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Hireling",
            "types": {Action, Duration},
            "advTags": {_Cost6, _Terminal},
        },
        {
            "name": "Lost City",
            "types": {Action},
            "advTags": {_Cost5, _Draw2, _Interactive, _Village},
        },
        {
            "name": "Magpie",
            "types": {Action},
            "advTags": {
                _Cantrip,
                _Cost4,
                _DeckGuesser,
                _Piler,
                _Reveal,
                _RevealResponse,
            },
        },
        {
            "name": "Messenger",
            "types": {Action},
            "advTags": {
                _Buys,
                _Cost4,
                _Gainer4,
                _Interactive,
                _Money2,
                _Shuffler,
                _Terminal,
            },
        },
        {
            "name": "Miser",
            "types": {Action},
            "advTags": {_Cost4, _Payload, _Terminal, _Thinner},
        },
        {
            "name": "Page",
            "types": {Action, Traveller},
            "advTags": {
                _BadSifter,
                _BadThinner,  # Warrior
                _Cantrip,  # Page
                _Chainer,  # Treasure Hunter
                _Cost2,  # Page
                _Discard,  # Warrior
                _Draw2,  # Warrior
                _Exchange,
                _FutureMoney1,
                _FutureMoney2,
                _Money1,  # Treasure Hunter
                _Money2,
                _Payload,  # Treasure Hunter
                _SplitPile,
                _Village,
            },
        },
        {
            "name": "Peasant",
            "types": {Action, Traveller},
            "advTags": {
                _Buys,  # Peasant
                _Cantrip,  # Fugitive
                _Cost2,  # Peasant
                _Discard,  # Soldier
                _Draw2,
                _Money1,  # Peasant
                _Money2,  # Soldier
                _Payload,  # Soldier
                _Sifter,  # Fugitive
                _SplitPile,
                _Splitter,
                _Terminal,  # Peasant
            },
        },
        {
            "name": "Port",
            "types": {Action},
            "advTags": {_Cost4, _GainResponse4, _Piler, _Village},
        },
        {
            "name": "Ranger",
            "types": {Action},
            "advTags": {_Buys, _Cost4, _Draw5, _Terminal},
        },
        {
            "name": "Ratcatcher",
            "types": {Action, Reserve},
            "advTags": {_Cantrip, _Cost2, _FreeAction, _Thinner, _Trasher},
        },
        {
            "name": "Raze",
            "types": {Action},
            "advTags": {
                _Chainer,
                _Cost2,
                _Discard,
                _Draw1,
                _Sifter,
                _Thinner,
                _Trasher,
            },
        },
        {"name": "Relic", "types": {Treasure, Attack}, "advTags": {_Cost5, _Money2}},
        {
            "name": "Royal Carriage",
            "types": {Action, Reserve},
            "advTags": {_Chainer, _Cost5, _FreeAction, _Splitter},
        },
        {
            "name": "Storyteller",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _Drawload},
        },
        {
            "name": "Swamp Hag",
            "types": {Action, Duration, Attack},
            "advTags": {_Cost5, _Curser, _Money3, _Terminal},
        },
        {
            "name": "Transmogrify",
            "types": {Action, Reserve},
            "advTags": {_Chainer, _Cost4, _FreeAction, _Remodeler, _Trasher},
        },
        {
            "name": "Treasure Trove",
            "types": {Treasure},
            "advTags": {_Cost5, _FutureMoney2, _Junker},
        },
        {
            "name": "Wine Merchant",
            "types": {Action},
            "advTags": {_Buys, _Cost5, _Money4, _Terminal},
        },
        # Landscapes
        {"name": "Alms", "types": {Event}, "advTags": {_Cost0, _Gainer4}},
        {"name": "Ball", "types": {Event}, "advTags": {_Cost5, _Gainer4}},
        {"name": "Bonfire", "types": {Event}, "advTags": {_Cost3, _PlayArea, _Thinner}},
        {"name": "Borrow", "types": {Event}, "advTags": {_Cost0, _FreeEvent, _Money1}},
        {"name": "Expedition", "types": {Event}, "advTags": {_Cost3, _FutureDraw2}},
        {"name": "Ferry", "types": {Event}, "advTags": {_Cost3, _CostReducer}},
        {"name": "Inheritance", "types": {Event}, "advTags": {_Command4, _Cost7}},
        {"name": "Lost Arts", "types": {Event}, "advTags": {_Chainer, _Cost6}},
        {"name": "Mission", "types": {Event}, "advTags": {_Cost4, _Draw5}},
        {
            "name": "Quest",
            "types": {Event},
            "advTags": {_Cost0, _Discard, _FutureMoney2},
        },
        {"name": "Pathfinding", "types": {Event}, "advTags": {_Cost8, _Drawload}},
        {
            "name": "Pilgrimage",
            "types": {Event},
            "advTags": {_Cost4, _Gainer6, _NamesMatter, _PlayArea},
        },
        {"name": "Plan", "types": {Event}, "advTags": {_Cost3, _Thinner}},
        {"name": "Raid", "types": {Event}, "advTags": {_Cost5, _Payload}},
        {
            "name": "Save",
            "types": {Event},
            "advTags": {_Cost1, _DeckSeeder, _FreeEvent},
        },
        {
            "name": "Scouting Party",
            "types": {Event},
            "advTags": {_Cost2, _DeckSeeder, _Discard, _FreeEvent, _Sifter},
        },
        {"name": "Seaway", "types": {Event}, "advTags": {_Buys, _Cost5, _Gainer4}},
        {"name": "Training", "types": {Event}, "advTags": {_Cost6, _FutureMoney1}},
        {
            "name": "Travelling Fair",
            "types": {Event},
            "advTags": {_Buys, _Cost2, _DeckSeeder, _FreeEvent},
        },
    ]
)

Empires = Set("Empires")
Empires.AddCards(
    [
        {
            "name": "Archive",
            "types": {Action, Duration},
            "advTags": {_Cantrip, _Cost5, _Draw3, _Saver},
        },
        {
            "name": "Capital",
            "types": {Treasure},
            "advTags": {_Cost5, _Buys, _Debt, _Money6},
        },
        {
            "name": "Castles",
            "types": {Action, Treasure, Victory, Castle},
            "advTags": {
                _Cost3,  # Humble Castle
                _Cost4,  # Crumbling Castle
                _GainResponse4,  # Crumbling Castle
                _FutureMoney1,  # Crumbling Castle
                _Money1,  # Humble Castle
                _Payload,
                _Reveal,
                _SplitPile,
                _Trasher,
                _TrashResponse,  # Crumbling Castle
                _VictoryGainer,  # Crumbling Castle
            },
        },
        {
            "name": "Catapult/Rocks",
            "types": {Action, Attack, Treasure},
            "advTags": {
                _Cost3,  # Catapult
                _Cost4,  # Rocks
                _Curser,  # Catapult
                _DeckSeeder,  # Rocks
                _Discard,  # Catapult
                _FutureMoney1,  # Rocks
                _GainResponse4,  # Rocks
                _Money1,  # Catapult, Rocks
                _Money2,  # Rocks
                _SplitPile,
                _Terminal,  # Catapult
                _Thinner,  # Catapult
                _Trasher,  # Catapult
                _TrashResponse,  # Rocks
                _Twin,  # Catapult
            },
        },
        {
            "name": "Chariot Race",
            "types": {Action},
            "advTags": {_Cost3, _Peddler, _Reveal, _VictoryGainer},
        },
        {
            "name": "Charm",
            "types": {Treasure},
            "advTags": {_Buys, _Choice, _Cost5, _Gainer6, _Money2},
        },
        {
            "name": "City Quarter",
            "types": {Action},
            "advTags": {_Cost8, _Debt, _Drawload, _ExtraCost, _Reveal, _Village},
        },
        {
            "name": "Encampment/Plunder",
            "types": {Action, Treasure},
            "advTags": {
                _Cost2,  # Encampment
                _Cost5,
                _Draw2,  # Encampment
                _Money2,
                _Reveal,  # Encampment
                _SplitPile,
                _VictoryGainer,
                _Village,  # Encampment
            },
        },
        {
            "name": "Crown",
            "types": {Action, Treasure},
            "advTags": {_Cost5, _Splitter},
        },
        {
            "name": "Enchantress",
            "types": {Action, Attack, Duration},
            "advTags": {_Cost3, _FutureDraw2, _Terminal},
        },
        {
            "name": "Engineer",
            "types": {Action},
            "advTags": {_Cost4, _Debt, _ExtraCost, _Gainer4, _Trasher},
        },
        {
            "name": "Farmers' Market",
            "types": {Action, Gathering},
            "advTags": {
                _Buys,
                _Cost3,
                _Money1,
                _Money2,
                _Money3,
                _Money4,
                _Terminal,
                _Thinner,
                _Trasher,
                _Twin,
                _VictoryGainer,
            },
        },
        {
            "name": "Forum",
            "types": {Action},
            "advTags": {_Buys, _Cantrip, _Cost5, _Discard, _GainResponse5, _Sifter},
        },
        {
            "name": "Gladiator/Fortune",
            "types": {Action, Treasure},
            "advTags": {
                _Buys,
                _Cost3,  # Gladiator
                _Cost16,
                _Debt,
                _ExtraCost,
                _Money3,  # Gladiator
                _Payload,
                _Reveal,  # Gladiator
                _SplitPile,
                _Terminal,
                _Twin,
                _Trasher,
            },
        },
        {
            "name": "Groundskeeper",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _VictoryGainer, _VictoryResponse},
        },
        {
            "name": "Legionary",
            "types": {Action, Attack},
            "advTags": {_Cost5, _Discard, _Money3, _Terminal},
        },
        {
            "name": "Overlord",
            "types": {Action, Command},
            "advTags": {_Command5, _Cost8, _Debt, _ExtraCost, _Terminal},
        },
        {
            "name": "Patrician/Emporium",
            "types": {Action},
            "advTags": {
                _Cantrip,  # Patrician
                _Cost2,  # Patrician
                _Cost5,
                _Draw2,  # Patrician
                _Peddler,
                _Reveal,  # Patrician
                _VictoryGainer,
            },
        },
        {
            "name": "Royal Blacksmith",
            "types": {Action},
            "advTags": {_Cost8, _Debt, _Discard, _Draw5, _Reveal, _Terminal},
        },
        {
            "name": "Sacrifice",
            "types": {Action},
            "advTags": {
                _Cost4,
                _DoubleDouble,
                _Money2,
                _MultiTypeLove,
                _Thinner,
                _Trasher,
                _VictoryGainer,
            },
        },
        {
            "name": "Settlers/Bustling Village",
            "types": {Action},
            "advTags": {
                _Cost2,  # Settlers
                _Cost5,
                _Peddler,  # Settlers
                _SplitPile,
                _Village,
            },
        },
        {
            "name": "Temple",
            "types": {Action, Gathering},
            "advTags": {
                _Cost4,
                _GainResponse4,
                _NamesMatter,
                _Terminal,
                _Thinner,
                _VictoryGainer,
            },
        },
        {
            "name": "Villa",
            "types": {Action},
            "advTags": {
                _Buys,
                _Cost4,
                _GainResponse4,
                _Money1,
                _PhaseBreaker,
                _Village,
            },
        },
        {
            "name": "Wild Hunt",
            "types": {Action},
            "advTags": {_Cost5, _Draw3, _Terminal, _VictoryGainer},
        },
        # Event cards
        {"name": "Advance", "types": {Event}, "advTags": {_Cost0, _Gainer6, _Trasher}},
        {
            "name": "Annex",
            "types": {Event},
            "advTags": {_Cost8, _Debt, _ExtraCost, _Sifter, _VictoryGainer},
        },
        {"name": "Banquet", "types": {Event}, "advTags": {_Cost3, _Gainer5, _Junker}},
        {
            "name": "Conquest",
            "types": {Event},
            "advTags": {_Cost6, _FutureMoney2, _VictoryGainer},
        },
        {
            "name": "Delve",
            "types": {Event},
            "advTags": {_Cost2, _FreeEvent, _FutureMoney1},
        },
        {"name": "Dominate", "types": {Event}, "advTags": {_Cost14, _VictoryGainer}},
        {
            "name": "Donate",
            "types": {Event},
            "advTags": {_Cost8, _Debt, _ExtraCost, _Shuffler, _Thinner},
        },
        {
            "name": "Salt the Earth",
            "types": {Event},
            "advTags": {_Cost4, _Piler, _Trasher, _VictoryGainer},
        },
        {
            "name": "Ritual",
            "types": {Event},
            "advTags": {_Cost4, _Curser, _Trasher, _VictoryGainer},
        },
        {"name": "Tax", "types": {Event}, "advTags": {_Cost2, _Debt}},
        {
            "name": "Trade",
            "types": {Event},
            "advTags": {_Cost5, _FutureMoney2, _Trasher},
        },
        {
            "name": "Triumph",
            "types": {Event},
            "advTags": {_Cost5, _Debt, _ExtraCost, _VictoryGainer},
        },
        {
            "name": "Wedding",
            "types": {Event},
            "advTags": {_Cost7, _Debt, _ExtraCost, _FutureMoney2, _VictoryGainer},
        },
        {"name": "Windfall", "types": {Event}, "advTags": {_Cost5, _FutureMoney6}},
        # Landmark Cards
        {"name": "Aqueduct", "types": {Landmark}, "advTags": {_VictoryGainer}},
        {"name": "Arena", "types": {Landmark}, "advTags": {_Discard, _VictoryGainer}},
        {"name": "Bandit Fort", "types": {Landmark}, "advTags": {_Curser}},
        {"name": "Basilica", "types": {Landmark}, "advTags": {_VictoryGainer}},
        {"name": "Baths", "types": {Landmark}, "advTags": {_VictoryGainer}},
        {"name": "Battlefield", "types": {Landmark}, "advTags": {_VictoryGainer}},
        {"name": "Colonnade", "types": {Landmark}, "advTags": {_VictoryGainer}},
        {
            "name": "Defiled Shrine",
            "types": {Landmark},
            "advTags": {_Curser, _VictoryGainer},
        },
        {"name": "Fountain", "types": {Landmark}, "advTags": {_Junker, _VictoryGainer}},
        {"name": "Keep", "types": {Landmark}, "advTags": {_VictoryGainer}},
        {"name": "Labyrinth", "types": {Landmark}, "advTags": {_VictoryGainer}},
        {
            "name": "Mountain Pass",
            "types": {Landmark},
            "advTags": {_Debt, _VictoryGainer},
        },
        {
            "name": "Museum",
            "types": {Landmark},
            "advTags": {_NamesMatter, _VictoryGainer},
        },
        {"name": "Obelisk", "types": {Landmark}, "advTags": {_VictoryGainer}},
        {
            "name": "Orchard",
            "types": {Landmark},
            "advTags": {_NamesMatter, _VictoryGainer},
        },
        {"name": "Palace", "types": {Landmark}, "advTags": {_VictoryGainer}},
        {
            "name": "Tomb",
            "types": {Landmark},
            "advTags": {_TrashGainer, _VictoryGainer},
        },
        {"name": "Tower", "types": {Landmark}, "advTags": {_Empty, _VictoryGainer}},
        {"name": "Triumphal Arch", "types": {Landmark}, "advTags": {_VictoryGainer}},
        {"name": "Wall", "types": {Landmark}, "advTags": {_Curser}},
        {"name": "Wolf Den", "types": {Landmark}, "advTags": {_Curser}},
    ]
),

Nocturne = Set("Nocturne")
Nocturne.AddCards(
    [
        {
            "name": "Bard",
            "types": {Action, Fate},
            "advTags": {
                _Buys,
                _Cantrip,
                _Chainer,
                _Cost4,
                _DeckSeeder,
                _Discard,
                _Draw1,
                _FutureDraw1,
                _FutureDraw2,
                _FutureMoney1,
                _FutureMoney2,
                _Gainer4,
                _Money2,
                _Money3,
                _Random,
                _Reveal,
                _Sifter,
                _Terminal,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Blessed Village",
            "types": {
                Action,
                Fate,
            },  # Fate means _Buys, _Cantrip, _Chainer, _DeckSeeder, _Discard, _Draw1, _FutureDraw1, _FutureDraw2, _FutureMoney1, _FutureMoney2, _Gainer4, _Money1, _Random, _Reveal, _Sifter, _Thinner, _Trasher,
            "advTags": {
                _Cantrip,
                _Chainer,
                _Cost4,
                _DeckSeeder,
                _Discard,
                _DoubleDouble,
                _FutureDraw1,
                _FutureDraw2,
                _FutureMoney1,
                _FutureMoney2,
                _Gainer4,
                _Money1,
                _Random,
                _Reveal,
                _Sifter,
                _Thinner,
                _Trasher,
                _Village,
            },
        },
        {
            "name": "Cemetery + Haunted Mirror (Heirloom)",
            "types": {Victory, Treasure, Heirloom},
            "advTags": {
                _Cost4,  # Cemetary
                _Discard,  # Ghost
                _GainResponse4,  # Cemetary
                _Money1,  # Haunted Mirror
                _NoHandsPlay,  # Ghost
                _Splitter,  # Ghost
                _Trasher,  # Cemetary
                _Thinner,  # Cemetary
                _TrashResponse,  # Haunted Mirror
            },
        },
        {
            "name": "Changeling",
            "types": {Night},
            "advTags": {_Cost3, _Trasher, _TrashGainer},
        },
        {
            "name": "Cobbler",
            "types": {Night, Duration},
            "advTags": {_Cost4, _Gainer4, _Shuffler},
        },
        {
            "name": "Conclave",
            "types": {Action},
            "advTags": {_Cost4, _Money2, _NamesMatter, _Village},
        },
        {
            "name": "Crypt",
            "types": {Night, Duration},
            "advTags": {_Cost5, _DeckSeeder, _Payload},
        },
        {
            "name": "Cursed Village",
            "types": {Action, Doom},
            "advTags": {_Cost5, _Filler, _Village},
        },
        {"name": "Den of Sin", "types": {Night, Duration}, "advTags": {_Cost5, _Draw2}},
        {
            "name": "Devil's Workshop",
            "types": {Night},
            "advTags": {
                _Cost4,  # Devil's Workshop,
                _FutureDraw2,  # Imp,
                _FutureMoney2,  # Devil's Workshop,
                _Gainer4,  # Devil's Workshop
                _Lab,  # Imp
                _NamesMatter,  # Imp
            },
        },
        {
            "name": "Druid",
            "types": {Action, Fate},
            "advTags": {_Buys, _Choice, _Cost2, _Terminal},
        },
        {
            "name": "Exorcist",
            "types": {Night},
            "advTags": {
                _Cantrip,  # Will-o'-Wisp
                _Cost4,  # Exorcist
                _Discard,  # Ghost
                _FutureDraw2,  # Imp, Will-o'-Wisp
                _Lab,  # Imp
                _NamesMatter,  # Imp
                _Reveal,  # Will-o'-Wisp
                _Splitter,  # Ghost
                _Terminal,  # Exorcist
                _Trasher,  # Exorcist
            },
        },
        {
            "name": "Faithful Hound",
            "types": {Action, Reaction},
            "advTags": {
                _Cost2,
                _DiscardResponse,
                _Draw2,
                _Saver,
                _Terminal,
            },
        },
        {
            "name": "Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)",
            "types": {Action, Fate, Treasure, Heirloom},
            "advTags": {
                _Cost3,
                _Discard,
                _FutureMoney1,  # Lucky Coin
                _Money1,  # Lucky Coin
                _Terminal,
            },
        },
        {
            "name": "Guardian",
            "types": {Night, Duration},
            "advTags": {_AttackResponse, _Cost2, _FutureMoney1, _Shuffler},
        },
        {"name": "Ghost Town", "types": {Night}, "advTags": {_Cantrip, _Cost3}},
        {
            "name": "Idol",
            "types": {Treasure, Attack, Fate},
            "advTags": {_Cost5, _Curser, _Money2, _MultiType},
        },
        {
            "name": "Leprechaun",
            "types": {Action, Doom},
            "advTags": {_Cost3, _FutureMoney2, _Terminal},
        },
        {
            "name": "Monastery",
            "types": {Night},
            "advTags": {_Cost2, _GainResponse6, _PlayArea, _Thinner, _Trasher},
        },
        {
            "name": "Necromancer + Zombies",
            "types": {Action},
            "advTags": {
                _Cantrip,  # Zombie Apprentice, Zombie Spy
                _Chainer,  # Necromancer,  # Zombie Apprentice
                _Cost4,  # Necromancer
                _DeckGuesser,  # Zombie Mason
                _DeckSeeder,  # Zombie Spy
                _Discard,  # Zombie Spy
                _Draw3,  # Zombie Apprentice
                _Kingdom,  # Necromancer
                _Remodeler,  # Zombie Mason
                _Sifter,  # Zombie Spy
                _Thinner,  # Zombie Apprentice
                _Trasher,  # Zombie Apprentice
                _TrashResponse,  # Necromancer
            },
        },
        {
            "name": "Night Watchman",
            "types": {Night},
            "advTags": {_Cost3, _DeckSeeder, _Discard, _Sifter},
        },
        {
            "name": "Pixie + Goat (Heirloom)",
            "types": {Action, Fate, Treasure, Heirloom},
            "advTags": {
                _Cantrip,  # Pixie
                _Cost2,  # Pixie,
                _Money1,  # Goat
                _Random,  # Pixie
                _Thinner,  # Pixie + Goat
                _Trasher,  # Pixie + Goat
            },
        },
        {
            "name": "Pooka + Cursed Gold (Heirloom)",
            "types": {Action, Treasure, Heirloom},
            "advTags": {
                _Cost5,
                _Curser,  # Cursed Gold
                _Draw4,
                _Money3,  # Cursed Gold
                _Thinner,
            },
        },
        {
            "name": "Raider",
            "types": {Night, Duration, Attack},
            "advTags": {
                _Cost6,
                _Discard,
                _Money3,
                _MultiType,
                _Reveal,
            },
        },
        {
            "name": "Sacred Grove",
            "types": {Action, Fate},
            "advTags": {_Buys, _Cost5, _Interactive, _Money3, _Terminal},
        },
        {
            "name": "Secret Cave + Magic Lamp (Heirloom)",
            "types": {Action, Duration, Treasure, Heirloom},
            "advTags": {
                _Cantrip,  # Secret Cave
                _Cost3,  # Secret Cave
                _Discard,  # Secret Cave
                _Gainer6,  # Magic Lamp
                _Money1,  # Magic Lamp
                _Money3,
                _NamesMatter,  # Magic Lamp
                _TrashResponse,  # Magic Lamp
                _Thinner,  # Magic Lamp
                _Trasher,  # Magic Lamp
                _Twin,
            },
        },
        {
            "name": "Shepherd + Pasture (Heirloom)",
            "types": {Action, Treasure, Victory, Heirloom},
            "advTags": {
                _Chainer,  # Shepherd
                _Cost4,  # Shepherd
                _Discard,  # Shepherd
                _Drawload,  # Shepherd
                _Money1,  # Pasture
                _Reveal,  # Shepherd
            },
        },
        {
            "name": "Skulk",
            "types": {
                Action,
                Attack,
                Doom,
            },  # Doom gives _BadSifter, _BadThinner, _Curser, _Discard, _Junker, _Random, _Trasher
            "advTags": {
                _BadSifter,
                _BadThinner,
                _Buys,
                _Cost4,
                _Curser,
                _Discard,
                _FutureMoney2,
                _GainResponse4,
                _Junker,
                _MultiType,
                _Random,
                _Terminal,
                _Trasher,
            },
        },
        {
            "name": "Tormentor",
            "types": {Action, Attack, Doom},
            "advTags": {_Cost5, _Money2, _MultiType, _Terminal},
        },
        {
            "name": "Tracker + Pouch (Heirloom)",
            "types": {Action, Fate, Treasure, Heirloom},
            "advTags": {
                _Buys,
                _Cost2,
                _DeckSeeder,
                # _GainResponse2, There's no _Gainer2, so doing GainResponse3
                _GainResponse3,
                _Money1,
                _Terminal,
            },
        },
        {
            "name": "Tragic Hero",
            "types": {Action},
            "advTags": {_Buys, _Cost5, _Draw3, _Terminal, _Trasher, _TrashGainer},
        },
        {
            "name": "Vampire",
            "types": {Night, Attack, Doom},
            "advTags": {_Cost5, _Exchange, _Gainer5, _MultiType, _Thinner, _Trasher},
        },
        {
            "name": "Werewolf",
            "types": {Action, Night, Attack, Doom},
            "advTags": {
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
            "types": {Action},
            "advTags": {_Cost3, _FutureAction, _Trasher, _TrashResponse, _Terminal},
        },
        {
            "name": "Border Guard",
            "types": {Action},
            "advTags": {
                _Cantrip,
                _Cost2,
                _DeckSeeder,
                _Discard,
                _Reveal,
                _Sifter,
            },
        },
        {
            "name": "Cargo Ship",
            "types": {Action, Duration},
            "advTags": {_Cost3, _Money2, _Saver, _Terminal},
        },
        {
            "name": "Ducat",
            "types": {Treasure},
            "advTags": {
                _Buys,
                _Cost2,
                _FutureMoney1,  # _GainResponse2, There is no Gainer2
                _GainResponse3,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Experiment",
            "types": {Action},
            "advTags": {_Cantrip, _Cost3, _Draw2, _GainResponse3, _Piler},
        },
        {
            "name": "Flag Bearer",
            "types": {Action},
            "advTags": {
                _Cost4,
                _Drawload,
                _Money2,
                _Terminal,
                _GainResponse4,
                _TrashResponse,
            },
        },
        {
            "name": "Hideout",
            "types": {Action},
            "advTags": {_Cost4, _Curser, _Thinner, _Trasher, _Village},
        },
        {
            "name": "Improve",
            "types": {Action},
            "advTags": {_Cost3, _Money2, _Remodeler, _Terminal, _Trasher},
        },
        {
            "name": "Inventor",
            "types": {Action},
            "advTags": {_Cost4, _CostReducer, _Gainer4, _Terminal},
        },
        {
            "name": "Lackeys",
            "types": {Action},
            "advTags": {
                _Cost2,
                _Draw2,
                _FutureAction,
                # _GainResponse2, There is no Gainer2 at this point.
                _GainResponse3,
                _Terminal,
            },
        },
        {"name": "Mountain Village", "types": {Action}, "advTags": {_Cost4, _Village}},
        {
            "name": "Old Witch",
            "types": {Action, Attack},
            "advTags": {_Cost5, _Curser, _Draw3, _Interactive, _Trasher},
        },
        {
            "name": "Patron",
            "types": {Action, Reaction},
            "advTags": {
                _FutureAction,
                _FutureMoney1,
                _Money2,
                _RevealResponse,
                _Terminal,
            },
        },
        {
            "name": "Priest",
            "types": {Action},
            "advTags": {_Cost4, _Payload, _Money2, _Terminal, _Thinner, _Trasher},
        },
        {
            "name": "Recruiter",
            "types": {Action},
            "advTags": {_Cost5, _Draw2, _Terminal, _Thinner, _Village},
        },
        {
            "name": "Research",
            "types": {Action, Duration},
            "advTags": {_Chainer, _Cost4, _Saver, _Thinner, _Trasher},
        },
        {
            "name": "Scepter",
            "types": {Treasure},
            "advTags": {_ActionLover, _Choice, _Cost5, _Money2, _Splitter},
        },
        {
            "name": "Scholar",
            "types": {Action},
            "advTags": {_Cost5, _Discard, _Draw7, _Terminal},
        },
        {
            "name": "Sculptor",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _Gainer4, _Terminal},
        },
        {
            "name": "Seer",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _DeckSeeder, _Draw4, _Reveal},
        },
        {
            "name": "Silk Merchant",
            "types": {Action},
            "advTags": {
                _Buys,
                _Draw2,
                _FutureAction,
                _FutureMoney1,
                _GainResponse4,
                _Terminal,
                _TrashResponse,
            },
        },
        {
            "name": "Spices",
            "types": {Treasure},
            "advTags": {_Buys, _Cost5, _GainResponse5, _FutureMoney2, _Money2},
        },
        {
            "name": "Swashbuckler",
            "types": {Action},
            "advTags": {
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
            "types": {Action},
            "advTags": {
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
            "types": {Action, Attack},
            "advTags": {
                _Cost5,
                _Discard,
                _FutureMoney2,
                _Reveal,
                _Terminal,
            },
        },
        # Project
        {"name": "Academy", "types": {Project}, "advTags": {_Chainer, _Cost4}},
        {"name": "Barracks", "types": {Project}, "advTags": {_Cost6, _Village}},
        {"name": "Capitalism", "types": {Project}, "advTags": {_Cost5}},
        {
            "name": "Cathedral",
            "types": {Project},
            "advTags": {_Cost3, _Thinner, _Trasher},
        },
        {"name": "Canal", "types": {Project}, "advTags": {_Cost7, _CostReducer}},
        {"name": "Citadel", "types": {Project}, "advTags": {_Cost8, _Splitter}},
        {
            "name": "City Gate",
            "types": {Project},
            "advTags": {_Cost3, _DeckSeeder, _Sifter},
        },
        {
            "name": "Crop Rotation",
            "types": {Project},
            "advTags": {_Cost6, _Discard, _Draw2},
        },
        {
            "name": "Exploration",
            "types": {Project},
            "advTags": {_Cost4, _FutureAction, _FutureMoney1},
        },
        {"name": "Fair", "types": {Project}, "advTags": {_Buys, _Cost4}},
        {"name": "Fleet", "types": {Project}, "advTags": {_Cost5, _Draw5}},
        {"name": "Guildhall", "types": {Project}, "advTags": {_Cost5, _FutureMoney1}},
        {"name": "Innovation", "types": {Project}, "advTags": {_Chainer, _Cost6}},
        {"name": "Pageant", "types": {Project}, "advTags": {_Cost3, _FutureMoney1}},
        {"name": "Piazza", "types": {Project}, "advTags": {_Chainer, _Cost5}},
        {"name": "Road Network", "types": {Project}, "advTags": {_Cost5, _Drawload}},
        {"name": "Sewers", "types": {Project}, "advTags": {_Cost3, _Thinner, _Trasher}},
        {"name": "Silos", "types": {Project}, "advTags": {_Cost4, _Discard, _Sifter}},
        {"name": "Sinister Plot", "types": {Project}, "advTags": {_Cost4, _Drawload}},
        {"name": "Star Chart", "types": {Project}, "advTags": {_Cost3, _DeckSeeder}},
    ]
)

Menagerie = Set("Menagerie")
Menagerie.AddCards(
    [
        {
            "name": "Animal Fair",
            "types": {Action},
            "advTags": {
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
            "types": {Action, Duration},
            "advTags": {_Buys, _Cost5, _Draw3, _Terminal},
        },
        {
            "name": "Black Cat",
            "types": {Action, Attack, Reaction},
            "advTags": {
                _Cost2,
                _Curser,
                _Draw2,
                _FreeAction,
                _MultiType,
                _Terminal,
                _VictoryResponse,
            },
        },
        {
            "name": "Bounty Hunter",
            "types": {Action},
            "advTags": {_Chainer, _Cost4, _Money3, _NamesMatter, _Saver, _Thinner},
        },
        {
            "name": "Camel Train",
            "types": {Action},
            "advTags": {_Cost3, _FutureMoney2, _GainResponse3, _Gainer6, _Terminal},
        },
        {
            "name": "Cardinal",
            "types": {Action, Attack},
            "advTags": {
                _BadThinner,
                _Cost4,
                _Discard,
                _Money2,
                _Reveal,
                _Terminal,
            },
        },
        {
            "name": "Cavalry",
            "types": {Action},
            "advTags": {
                _Buys,
                _Cost4,
                _Draw2,
                _FutureDraw2,
                _GainResponse4,
                _PhaseBreaker,
                _Terminal,
            },
        },
        {
            "name": "Coven",
            "types": {Action, Attack},
            "advTags": {_Chainer, _Cost5, _Curser, _Money2},
        },
        {
            "name": "Destrier",
            "types": {Action},
            "advTags": {_Cantrip, _Cost6, _CostVaries, _Draw2},
        },
        {
            "name": "Displace",
            "types": {Action},
            "advTags": {_Cost5, _Remodeler, _Terminal},
        },
        {
            "name": "Falconer",
            "types": {Action, Reaction},
            "advTags": {_Cost5, _FreeAction, _Gainer4, _MultiTypeLove, _Terminal},
        },
        {
            "name": "Fisherman",
            "types": {Action},
            "advTags": {_Cost3, _Cost5, _CostVaries, _Peddler},
        },
        {
            "name": "Gatekeeper",
            "types": {Action, Duration, Attack},
            "advTags": {
                _BadThinner,
                _Cost5,
                _GainResponse5,
                _Money3,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Goatherd",
            "types": {Action},
            "advTags": {
                _Chainer,
                _Cost3,
                _Drawload,
                _Thinner,
                _Trasher,
                _TrashResponse,
            },
        },
        {
            "name": "Groom",
            "types": {Action},
            "advTags": {
                _Cantrip,
                _Choice,
                _Cost4,
                _FutureDraw1,
                _FutureMoney1,
                _Gainer4,
            },
        },
        {
            "name": "Hostelry",
            "types": {Action},
            "advTags": {_Cost4, _Discard, _Drawload, _GainResponse4, _Village},
        },
        {
            "name": "Hunting Lodge",
            "types": {Action},
            "advTags": {_Cost5, _Discard, _Draw5, _Village},
        },
        {
            "name": "Kiln",
            "types": {Action},
            "advTags": {_Cost5, _Money2, _Gainer6, _Terminal},
        },
        {
            "name": "Livery",
            "types": {Action},
            "advTags": {_Cost5, _Drawload, _Money3, _Terminal},
        },
        {
            "name": "Mastermind",
            "types": {Action, Duration},
            "advTags": {_Cost5, _Splitter, _Terminal},
        },
        {
            "name": "Paddock",
            "types": {Action},
            "advTags": {_Chainer, _Cost5, _Draw2, _Empty, _Money2},
        },
        {
            "name": "Sanctuary",
            "types": {Action},
            "advTags": {_Buys, _Cantrip, _Cost5, _Thinner},
        },
        {
            "name": "Scrap",
            "types": {Action},
            "advTags": {
                _Buys,
                _Cantrip,
                _Choice,
                _FutureDraw1,
                _FutureMoney1,
                _Money1,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Sheepdog",
            "types": {Action, Reaction},
            "advTags": {_Cost3, _Draw2, _FreeAction, _GainResponse6, _Terminal},
        },
        {
            "name": "Sleigh",
            "types": {Action, Reaction},
            "advTags": {
                _Cost2,
                _DeckSeeder,
                _Discard,
                _Draw2,
                # _GainResponse2, There's no support for _GainResponse2 (i.e., no _Gainer2)
                _GainResponse3,
                _Shuffler,
                _Terminal,
            },
        },
        {
            "name": "Snowy Village",
            "types": {Action},
            "advTags": {_Buys, _Cost3, _Village},
        },
        {
            "name": "Stockpile",
            "types": {Treasure},
            "advTags": {_Buys, _Cost3, _GainResponse3, _Money3, _Thinner},
        },
        {
            "name": "Supplies",
            "types": {Treasure},
            "advTags": {_Cost2, _DeckSeeder, _Draw1, _Money1},
        },
        {
            "name": "Village Green",
            "types": {Action, Duration, Reaction},
            "advTags": {
                _Cost4,
                _DiscardResponse,
                _FreeAction,
                _MultiType,
                _Village,
            },
        },
        {
            "name": "Wayfarer",
            "types": {Action},
            "advTags": {_Cost6, _CostVaries, _Draw3, _FutureMoney1, _Terminal},
        },
        # Events
        {
            "name": "Alliance",
            "types": {Event},
            "advTags": {_Cost10, _FutureMoney3, _Junker, _VictoryGainer},
        },
        {"name": "Banish", "types": {Event}, "advTags": {_Cost4, _Saver, _Thinner}},
        {
            "name": "Bargain",
            "types": {Event},
            "advTags": {_Cost4, _Gainer5, _Interactive},
        },
        {"name": "Commerce", "types": {Event}, "advTags": {_Cost5, _Payload}},
        {"name": "Delay", "types": {Event}, "advTags": {_Cost0, _FutureAction, _Saver}},
        {
            "name": "Demand",
            "types": {Event},
            "advTags": {_Cost5, _DeckSeeder, _Gainer4},
        },
        {
            "name": "Desperation",
            "types": {Event},
            "advTags": {_Cost0, _Curser, _FreeEvent, _Money2},
        },
        {
            "name": "Enclave",
            "types": {Event},
            "advTags": {_Cost8, _FutureMoney2, _VictoryGainer},
        },
        {
            "name": "Enhance",
            "types": {Event},
            "advTags": {_Cost3, _Remodeler, _Trasher},
        },
        {
            "name": "Gamble",
            "types": {Event},
            "advTags": {_Chainer, _Cost2, _Discard, _FreeEvent, _PhaseBreaker, _Reveal},
        },
        {
            "name": "Invest",
            "types": {Event},
            "advTags": {_Cost4, _Drawload, _GainResponse6, _Piler, _Saver},
        },
        {"name": "March", "types": {Event}, "advTags": {_Chainer, _Cost3}},
        {"name": "Populate", "types": {Event}, "advTags": {_Cost10, _Gainer6}},
        {
            "name": "Pursue",
            "types": {Event},
            "advTags": {
                _Cost2,
                _DeckGuesser,
                _DeckSeeder,
                _Discard,
                _FreeEvent,
                _Reveal,
                _Sifter,
            },
        },
        {"name": "Reap", "types": {Event}, "advTags": {_Cost7, _FutureMoney2, _Money3}},
        {"name": "Ride", "types": {Event}, "advTags": {_Cost2, _Draw1}},
        {
            "name": "Seize the Day",
            "types": {Event},
            "advTags": {_Cost4, _Draw5, _PhaseBreaker},
        },
        {
            "name": "Stampede",
            "types": {Event},
            "advTags": {_Cost5, _DeckSeeder, _Draw5},
        },
        {
            "name": "Toil",
            "types": {Event},
            "advTags": {_Chainer, _Cost2, _FreeEvent},
        },
        {
            "name": "Transport",
            "types": {Event},
            "advTags": {_Cost3, _DeckSeeder, _Gainer6},
        },
        # Way
        {"name": "Way of the Butterfly", "types": {Way}, "advTags": {_Remodeler}},
        {"name": "Way of the Camel", "types": {Way}, "advTags": {_FutureMoney2}},
        {"name": "Way of the Chameleon", "types": {Way}},
        {"name": "Way of the Frog", "types": {Way}, "advTags": {_Chainer, _DeckSeeder}},
        {"name": "Way of the Goat", "types": {Way}, "advTags": {_Thinner}},
        {"name": "Way of the Horse", "types": {Way}, "advTags": {_Draw2, _Thinner}},
        {
            "name": "Way of the Mole",
            "types": {Way},
            "advTags": {_Chainer, _Discard, _Sifter},
        },
        {"name": "Way of the Monkey", "types": {Way}, "advTags": {_Buys, _Money1}},
        {"name": "Way of the Mouse", "types": {Way}, "advTags": {_Kingdom}},
        {"name": "Way of the Mule", "types": {Way}, "advTags": {_Chainer, _Money1}},
        {"name": "Way of the Otter", "types": {Way}, "advTags": {_Draw2}},
        {"name": "Way of the Owl", "types": {Way}, "advTags": {_Filler}},
        {"name": "Way of the Ox", "types": {Way}, "advTags": {_Village}},
        {"name": "Way of the Pig", "types": {Way}, "advTags": {_Cantrip}},
        {"name": "Way of the Rat", "types": {Way}, "advTags": {_Discard, _Gainer6}},
        {"name": "Way of the Seal", "types": {Way}, "advTags": {_DeckSeeder, _Money1}},
        {"name": "Way of the Sheep", "types": {Way}, "advTags": {_Money2}},
        {"name": "Way of the Squirrel", "types": {Way}, "advTags": {_Draw2}},
        {"name": "Way of the Turtle", "types": {Way}, "advTags": {_FreeAction}},
        {"name": "Way of the Worm", "types": {Way}, "advTags": {_VictoryGainer}},
    ]
)

Allies = Set("Allies")
Allies.AddCards(
    [
        {
            "name": "Augers: Herb Gatherer + Acolyte + Sorceress + Sibyl",
            "types": {Action, Attack, Augur},
            "advTags": {
                _BottomSeeder,  # Sibyl
                _Buys,  # Herb Gatherer
                _Cantrip,  # Sorceress
                _Cost3,  # Herb Gatherer
                _Cost4,  # Acolyte
                _Cost5,  # Sorceress
                _Cost6,  # Sibyl
                _Curser,  # Sorceress
                _DeckGuesser,  # Sorceress
                _DeckSeeder,  # Sibyl
                _FutureMoney2,  # Acolyte
                _Gainer6,  # Acolyte
                _Lab,  # Sibyl
                _NoHandsPlay,  # Herb Gatherer
                _PhaseBreaker,  # Herb Gatherer
                _Reveal,  # Sorceress
                _Sifter,  # Sibyl
                _Shuffler,  # Herb Gatherer
                _SplitPile,  # all
                _Terminal,  # Acolyte, # Herb Gatherer
                _Trasher,  # Acolyte
                _TrashResponse,  # Acolyte
            },
        },
        {
            "name": "Barbarian",
            "types": {Action, Attack},
            "advTags": {_Cost5, _Curser, _Downgrader, _Money2, _Terminal, _Trasher},
        },
        {
            "name": "Bauble",
            "types": {Treasure, Liaison},
            "advTags": {_Buys, _Choice, _Cost2, _DeckSeeder, _Money1},
        },
        {
            "name": "Broker",
            "types": {Action, Liaison},
            "advTags": {
                _Choice,
                _Cost4,
                _Drawload,
                _Payload,
                _Thinner,
                _Trasher,
                _Village,
            },
        },
        {
            "name": "Capital City",
            "types": {Action},
            "advTags": {_Cost5, _Discard, _Draw2, _Money2, _Village},
        },
        {
            "name": "Carpenter",
            "types": {Action},
            "advTags": {
                _Chainer,
                _Cost4,
                _Empty,
                _Gainer4,
                _Remodeler,
                _Trasher,
            },
        },
        {
            "name": "Clashes: Battle Plan + Archer + Warlord + Territory",
            "types": {Action, Attack, Duration, Victory, Clash},
            "advTags": {
                _AttackResponse,
                _BadSifter,
                _Cantrip,  # Warlord
                _Cost3,
                _Cost4,  # Archer
                _Cost5,  # Warlord
                _Cost6,
                _Discard,  # Archer
                _Draw2,  # Warlord
                _Empty,
                _GainResponse6,
                _Money2,  # Archer
                _MultiType,  # Archer
                _Payload,
                _Reveal,  # Archer
                _Terminal,  # Archer
            },
        },
        {
            "name": "Contract",
            "types": {Treasure, Duration, Liaison},
            "advTags": {
                _Chainer,
                _Cost5,
                _Money2,
                _MultiType,
                _Saver,
            },
        },
        {
            "name": "Courier",
            "types": {Action},
            "advTags": {_Chainer, _Cost4, _Discard, _NoHandsPlay, _Money1},
        },
        {
            "name": "Forts: Tent + Garrison + Hill Fort + Stronghold",
            "types": {Action, Victory, Duration, Fort},
            "advTags": {
                _Cantrip,  # Hill Fort
                _Choice,  # Hill Fort, Stronghold
                _Cost3,
                _Cost4,  # Garrison
                _Cost5,
                _Cost6,  # Stronghold
                _DeckSeeder,
                _Draw3,  # Stronghold
                _Drawload,  # Garrison
                _Gainer4,  # Hill Fort
                _GainResponse6,  # Stronghold
                _Money2,  # Garrison
                _Money3,  # Stronghold
                _MultiType,  # Garrison
                _Shuffler,  # Hill Fort
                _Terminal,  # Hill Fort, Stronghold, # Garrison
            },
        },
        {
            "name": "Emissary",
            "types": {Action, Liaison},
            "advTags": {_Cantrip, _Draw3, _Terminal},
        },
        {"name": "Galleria", "types": {Action}, "advTags": {_Buys, _Cost5, _Money3}},
        {
            "name": "Guildmaster",
            "types": {Action, Liaison},
            "advTags": {_Cost5, _Discard, _Money3, _Terminal},
        },
        {
            "name": "Highwayman",
            "types": {Action, Duration, Attack},
            "advTags": {_Cost5, _Draw3, _MultiType, _Terminal},
        },
        {
            "name": "Hunter",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _Discard, _Draw3, _Reveal, _Sifter},
        },
        {
            "name": "Importer",
            "types": {Action, Duration, Liaison},
            "advTags": {
                _Cost3,
                _Gainer5,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Innkeeper",
            "types": {Action},
            "advTags": {_Cantrip, _Choice, _Cost4, _Discard, _Sifter},
        },
        {
            "name": "Marquis",
            "types": {Action},
            "advTags": {_Buys, _Cost6, _Discard, _Filler, _Terminal},
        },
        {
            "name": "Merchant Camp",
            "types": {Action},
            "advTags": {_Cost3, _DeckSeeder, _Money1, _Village},
        },
        {
            "name": "Modify",
            "types": {Action},
            "advTags": {_Choice, _Cost5, _Remodeler, _Thinner, _Trasher},
        },
        {
            "name": "Odysseys: Old Map, Voyage, Sunken Treasure, Distant Shore",
            "types": {Action, Duration, Odyssey, Treasure, Victory},
            "advTags": {
                _Cantrip,  # Old Map
                _Chainer,  # Voyage
                _Cost3,  # Old Map
                _Cost4,  # Voyage
                _Cost5,  # Sunken Treasure
                _Cost6,  # Distant Shore
                _Discard,  # Old Map
                _Gainer7,  # Sunken Treasure
                _Lab,  # Distant Shore
                _LimitsPlays,  # Voyage
                _MultiType,  # Voyage, Distant Shore
                _NamesMatter,  # Sunken Treasure
                _PhaseBreaker,  # Voyage
                _Sifter,  # Old Map
                _SplitPile,  # all
                _VictoryGainer,  # Distant Shore
            },
        },
        {
            "name": "Royal Galley",
            "types": {Action, Duration},
            "advTags": {_Cantrip, _Cost4, _NoHandsPlay, _Saver, _Splitter},
        },
        {
            "name": "Sentinel",
            "types": {Action},
            "advTags": {_Cost3, _Sifter, _Terminal, _Thinner},
        },
        {
            "name": "Sycophant",
            "types": {Action, Liaison},
            "advTags": {
                _Chainer,
                _Cost2,
                _Discard,
                # _GainResponse2, At this point there's no support for _GainResponse2 (i.e., no Gainer2)
                _GainResponse3,
                _Money3,
                _TrashResponse,
            },
        },
        {
            "name": "Skirmisher",
            "types": {Action, Attack},
            "advTags": {_AttackResponse, _Cost5, _Discard, _GainResponse5, _Peddler},
        },
        {
            "name": "Specialist",
            "types": {Action},
            "advTags": {_Chainer, _Choice, _Cost5, _Gainer6, _Splitter, _Terminal},
        },
        {
            "name": "Swap",
            "types": {Action},
            "advTags": {_Cantrip, _Cost5, _Gainer5, _Remodeler},
        },
        {
            "name": "Town",
            "types": {Action},
            "advTags": {_Buys, _Choice, _Cost4, _Money2, _Village},
        },
        {
            "name": "Townsfolk: Town Crier + Blacksmith + Miller + Elder",
            "types": {Action, Townsfolk},
            "advTags": {
                _Cantrip,  # Miller, Blacksmith, Town Crier
                _Choice,  # Blacksmith, Town Crier
                _Cost2,  # Town Crier
                _Cost3,  # Blacksmith
                _Cost4,  # Miller
                _Cost5,  # Elder
                _Discard,  # Miller
                _Draw2,  # Blacksmith
                _Filler,  # Blacksmith
                _FutureMoney1,  # Town Crier
                _Money2,  # Town Crier
                _Sifter,  # Miller
                _Terminal,  # Miller
            },
        },
        {
            "name": "Underling",
            "types": {Action, Liaison},
            "advTags": {_Cantrip, _Cost3},
        },
        {
            "name": "Wizards: Student, Conjurer, Sorcerer, Lich",
            "types": {Action, Duration, Liaison, Attack, Wizard},
            "advTags": {
                _Cantrip,  # Sorcerer
                _Chainer,  # Student
                _Cost3,  # Student
                _Cost4,  # Conjurer
                _Cost5,  # Sorcerer
                _Cost6,  # Lich
                _Curser,  # Sorcerer
                _DeckGuesser,  # Sorcerer
                _DeckSeeder,  # Student
                _Draw6,  # Lich
                _Gainer4,  # Conjurer
                _Gainer5,  # Lich
                _Reveal,  # Sorcerer
                _Saver,  # Conjurer
                _Thinner,  # Student
                _Trasher,  # Student
                _TrashGainer,  # Lich
                _TrashResponse,  # Lich
                _Village,  # Lich
            },
        },
        # Allies
        {"name": "Architects' Guild", "types": {Ally}, "advTags": {_Gainer5}},
        {"name": "Band of Nomads", "types": {Ally}, "advTags": {_Buys, _Choice}},
        {"name": "Cave Dwellers", "types": {Ally}, "advTags": {_Sifter}},
        {"name": "Circle of Witches", "types": {Ally}, "advTags": {_Curser}},
        {"name": "City-state", "types": {Ally}, "advTags": {_Chainer}},
        {"name": "Coastal Haven", "types": {Ally}, "advTags": {_Saver}},
        {
            "name": "Crafters' Guild",
            "types": {Ally},
            "advTags": {_DeckSeeder, _Gainer4},
        },
        {
            "name": "Desert Guides",
            "types": {Ally},
            "advTags": {_Discard, _Draw5, _Sifter},
        },
        {"name": "Family of Inventors", "types": {Ally}, "advTags": {_CostReducer}},
        {"name": "Fellowship of Scribes", "types": {Ally}, "advTags": {_Filler}},
        {
            "name": "Forest Dwellers",
            "types": {Ally},
            "advTags": {_DeckSeeder, _Discard, _Sifter},
        },
        {"name": "Gang of Pickpockets", "types": {Ally}, "advTags": {_Discard}},
        {"name": "Island Folk", "types": {Ally}, "advTags": {_Draw5}},
        {"name": "League of Bankers", "types": {Ally}, "advTags": {_Payload}},
        {
            "name": "League of Shopkeepers",
            "types": {Ally},
            "advTags": {_Buys, _Chainer, _Payload},
        },
        {"name": "Market Towns", "types": {Ally}, "advTags": {_Chainer}},
        {"name": "Mountain Folk", "types": {Ally}, "advTags": {_Draw3}},
        {"name": "Order of Astrologers", "types": {Ally}, "advTags": {_DeckSeeder}},
        {"name": "Order of Masons", "types": {Ally}, "advTags": {_Discard}},
        {"name": "Peaceful Cult", "types": {Ally}, "advTags": {_Thinner}},
        {
            "name": "Plateau Shepherds",
            "types": {Ally},
            "advTags": {_Cost2Response, _VictoryGainer},
        },
        {"name": "Trappers' Lodge", "types": {Ally}, "advTags": {_DeckSeeder}},
        {
            "name": "Woodworkers' Guild",
            "types": {Ally},
            "advTags": {_Trasher, _TrashGainer},
        },
    ]
)

Plunder = Set("Plunder")
Plunder.AddCards(
    [
        {
            "name": "Abundance",
            "types": {Treasure, Duration},
            "advTags": {_Buys, _Cost4, _FutureMoney3},
        },
        {
            "name": "Buried Treasure",
            "types": {Treasure, Duration},
            "advTags": {
                _Buys,
                _Cost5,
                _FreeAction,
                _Money3,
                _Terminal,
            },
        },
        {
            "name": "Cabin Boy",
            "types": {Action, Duration},
            "advTags": {_Cantrip, _FutureMoney2, _Gainer6, _Trasher},
        },
        {
            "name": "Cage",
            "types": {Treasure, Duration},
            "advTags": {_Cost2, _Saver, _Thinner, _Trasher, _VictoryResponse},
        },
        {
            "name": "Crew",
            "types": {Action, Duration},
            "advTags": {_Cost5, _Draw3, _DeckSeeder, _Terminal},
        },
        {
            "name": "Crucible",
            "types": {Treasure},
            "advTags": {_Cost4, _Payload, _Thinner, _Trasher},
        },
        {
            "name": "Cutthroat",
            "types": {Action, Duration, Attack},
            "advTags": {
                _Cost5,
                _Discard,
                _FutureMoney2,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Enlarge",
            "types": {Action, Duration},
            "advTags": {_Cost5, _Remodeler, _Terminal, _Trasher},
        },
        {
            "name": "Figurine",
            "types": {Treasure},
            "advTags": {_Buys, _Cost5, _Discard, _Draw2, _Money1},
        },
        {
            "name": "First Mate",
            "types": {Action},
            "advTags": {_Cost5, _Filler, _Village},
        },
        {
            "name": "Flagship",
            "types": {Action, Duration, Command},
            "advTags": {
                _Cost4,
                _Money2,
                _MultiType,
                _Splitter,
                _Terminal,
            },
        },
        {
            "name": "Fortune Hunter",
            "types": {Action},
            "advTags": {
                _Chainer,
                _Cost4,
                _DeckSeeder,
                _Money2,
                _NoHandsPlay,
                _PhaseBreaker,
                _Sifter,
            },
        },
        {
            "name": "Frigate",
            "types": {Action, Duration, Attack},
            "advTags": {
                _Cost5,
                _Discard,
                _Money3,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Gondola",
            "types": {Treasure, Duration},
            "advTags": {
                _Chainer,
                _Choice,
                _Cost4,
                _FutureMoney2,
                _GainResponse4,
                _Money2,
            },
        },
        {
            "name": "Grotto",
            "types": {Action, Duration},
            "advTags": {_Chainer, _Cost2, _Discard, _Draw4},
        },
        {
            "name": "Harbor Village",
            "types": {Action},
            "advTags": {_Cost4, _Peddler, _Village},
        },
        {
            "name": "Jewelled Egg",
            "types": {Treasure},
            "advTags": {_Buys, _Cost2, _FutureMoney2, _Money1, _Prize, _TrashResponse},
        },
        {"name": "King's Cache", "types": {Treasure}, "advTags": {_Cost7, _Splitter}},
        {
            "name": "Landing Party",
            "types": {Action, Duration},
            "advTags": {_Cost4, _DeckSeeder, _DoubleDouble},
        },
        {
            "name": "Longship",
            "types": {Action, Duration},
            "advTags": {_Cost5, _Draw2, _Village},
        },
        {
            "name": "Mapmaker",
            "types": {Action, Reaction},
            "advTags": {
                _Cost4,
                _Discard,
                _Draw2,
                _FreeAction,
                _Sifter,
                _Terminal,
                _VictoryResponse,
            },
        },
        {
            "name": "Maroon",
            "types": {Action},
            "advTags": {
                _Cost4,
                _Drawload,
                _MultiTypeLove,
                _Terminal,
                _Thinner,
                _Trasher,
            },
        },
        {
            "name": "Mining Road",
            "types": {Action},
            "advTags": {_Buys, _Chainer, _Money2, _Shuffler},
        },
        {"name": "Pendant", "types": {Treasure}, "advTags": {_Cost5, _Payload}},
        {
            "name": "Pickaxe",
            "types": {Treasure},
            "advTags": {_Cost5, _Money1, _Money4, _Thinner, _Trasher},
        },
        {
            "name": "Pilgrim",
            "types": {Action},
            "advTags": {_Cost5, _DeckSeeder, _Draw4, _Terminal},
        },
        {
            "name": "Quartermaster",
            "types": {Action, Duration},
            "advTags": {_Cost5, _FreeAction, _Gainer4, _Saver, _Terminal},
        },
        {
            "name": "Rope",
            "types": {Treasure, Duration},
            "advTags": {_Buys, _FutureDraw1, _Money1, _Thinner, _Trasher},
        },
        {
            "name": "Sack of Loot",
            "types": {Treasure},
            "advTags": {_Buys, _Cost6, _FutureMoney2, _Money1, _Prize},
        },
        {
            "name": "Silver Mine",
            "types": {Treasure},
            "advTags": {_Cost5, _Gainer4, _Money2},
        },
        {
            "name": "Search",
            "types": {Action, Duration},
            "advTags": {
                _Cost2,
                _Empty,
                _FutureMoney2,
                _PlayArea,
                _Prize,
                _Money2,
                _Terminal,
            },
        },
        {
            "name": "Shaman",
            "types": {Action},
            "advTags": {
                _Chainer,
                _Cost2,
                _Gainer6,
                _Money1,
                _Thinner,
                _Trasher,
                _TrashGainer,
            },
        },
        {
            "name": "Secluded Shrine",
            "types": {Action, Duration},
            "advTags": {_Cost3, _Money1, _Terminal, _Thinner, _Trasher},
        },
        {
            "name": "Siren",
            "types": {Action, Duration, Attack},
            "advTags": {
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
            "types": {Action, Duration, Reaction},
            "advTags": {
                _Cost3,
                _Draw2,
                _FreeAction,
                _MultiType,
                _Terminal,
            },
        },
        {
            "name": "Swamp Shacks",
            "types": {Action},
            "advTags": {_Cost4, _CardLover, _Drawload, _Village},
        },
        {
            "name": "Taskmaster",
            "types": {Action, Duration},
            "advTags": {_Chainer, _Cost3, _FutureAction, _GainResponse5, _Payload},
        },
        {
            "name": "Trickster",
            "types": {Action, Attack},
            "advTags": {_Cost5, _Curser, _Saver, _Terminal},
        },
        {"name": "Tools", "types": {Treasure}, "advTags": {_Cost4, _Gainer7}},
        {
            "name": "Wealthy Village",
            "types": {Action},
            "advTags": {_Cost5, _FutureMoney2, _GainResponse5, _Village},
        },
        # Events
        {
            "name": "Avoid",
            "types": {Event},
            "advTags": {_Cost2, _Discard, _FreeEvent, _Sifter},
        },
        {
            "name": "Bury",
            "types": {Event},
            "advTags": {_BottomSeeder, _Cost1, _FreeEvent},
        },
        {
            "name": "Deliver",
            "types": {Event},
            "advTags": {_Cost2, _FreeEvent, _Saver, _Shuffler},
        },
        {
            "name": "Foray",
            "types": {Event},
            "advTags": {_Cost3, _Discard, _FutureMoney2},
        },
        {
            "name": "Invasion",
            "types": {Event},
            "advTags": {_AttackResponse, _Chainer, _Cost10, _Money3, _VictoryGainer},
        },
        {
            "name": "Journey",
            "types": {Event},
            "advTags": {_Cost4, _Draw5, _PhaseBreaker},
        },
        {"name": "Launch", "types": {Event}, "advTags": {_Cantrip, _Cost3, _FreeEvent}},
        {"name": "Looting", "types": {Event}, "advTags": {_Cost6, _FutureMoney2}},
        {
            "name": "Maelstrom",
            "types": {Event},
            "advTags": {_Cost4, _Interactive, _Thinner, _Trasher},
        },
        {
            "name": "Mirror",
            "types": {Event},
            "advTags": {_Cost3, _FreeEvent, _Gainer6, _GainResponse6},
        },
        {
            "name": "Peril",
            "types": {Event},
            "advTags": {_Cost2, _FutureMoney2, _Prize, _Trasher},
        },
        {
            "name": "Prepare",
            "types": {Event},
            "advTags": {_Cost3, _Discard, _Saver, _Village},
        },
        {
            "name": "Prosper",
            "types": {Event},
            "advTags": {_Cost10, _FutureMoney2, _Gainer3, _Gainer6},
        },
        {
            "name": "Rush",
            "types": {Event},
            "advTags": {_Chainer, _Cost2, _FreeEvent, _PhaseBreaker},
        },
        {
            "name": "Scrounge",
            "types": {Event},
            "advTags": {
                _Choice,
                _Cost3,
                _Gainer5,
                _Thinner,
                _TrashGainer,
                _VictoryGainer,
            },
        },
        # Traits
        {"name": "Cheap", "types": {Trait}, "advTags": {_CostReducer}},
        {"name": "Cursed", "types": {Trait}, "advTags": {_Curser, _FutureMoney2}},
        {"name": "Fated", "types": {Trait}, "advTags": {_BottomSeeder, _DeckSeeder}},
        {"name": "Fawning", "types": {Trait}, "advTags": {_Gainer6}},
        {"name": "Friendly", "types": {Trait}, "advTags": {_Discard, _Gainer6}},
        {"name": "Hasty", "types": {Trait}, "advTags": {_Shuffler}},
        {"name": "Inherited", "types": {Trait}, "advTags": {_Kingdom}},
        {"name": "Inspiring", "types": {Trait}, "advTags": {_Chainer}},
        {"name": "Nearby", "types": {Trait}, "advTags": {_Buys}},
        {"name": "Patient", "types": {Trait}, "advTags": {_Saver}},
        {"name": "Pious", "types": {Trait}, "advTags": {_Thinner, _Trasher}},
        {"name": "Reckless", "types": {Trait}, "advTags": {_Splitter, _Thinner}},
        {"name": "Rich", "types": {Trait}, "advTags": {_FutureMoney1}},
        {"name": "Shy", "types": {Trait}, "advTags": {_Discard, _Draw2}},
        {"name": "Tireless", "types": {Trait}, "advTags": {_DeckSeeder}},
    ]
)

Antiquities = Set("Antiquities")
Antiquities.AddCards(
    [
        {
            "name": "Agora",
            "types": {Action, Reaction},
            "advTags": {
                _Cost5,
                _Discard,
                _FutureMoney1,
                _Money2,
                _Village,
            },
        },
        {
            "name": "Aquifer",
            "types": {Action},
            "advTags": {_Choice, _Cantrip, _Cost4, _Gainer4, _Money1, _Terminal},
        },
        {
            "name": "Archaeologist",
            "types": {Action},
            "advTags": {
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
            "types": {Action},
            "advTags": {
                _Cost4,
                _DeckSeeder,
                _Interactive,
                _Remodeler,
                _Sifter,
                _Terminal,
                _Trasher,
            },
        },
        {"name": "Curio", "types": {Treasure}, "advTags": {_Cost4, _Money1, _Payload}},
        {
            "name": "Dig",
            "types": {Action},
            "advTags": {_Cost8, _Discard, _Reveal, _VictoryGainer},
        },
        {
            "name": "Discovery",
            "types": {Treasure},
            "advTags": {_Cost2, _FutureMoney2, _ShuffleIn, _Thinner},
        },
        {
            "name": "Encroach",
            "types": {Action},
            "advTags": {
                _Cost6,
                _Discard,
                _Filler,
                _Remodeler,
                _Terminal,
                _VictoryGainer,
            },
        },
        {
            "name": "Gamepiece",
            "types": {Treasure, Reaction},
            "advTags": {_Cost3, _Discard, _DiscardResponse, _Money1},
        },
        {
            "name": "Graveyard",
            "types": {Action},
            "advTags": {_Cost1, _Gainer6, _TrashGainer, _Village},
        },
        {
            "name": "Grave Watcher",
            "types": {Action, Attack},
            "advTags": {
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
            "types": {Action, Reaction},
            "advTags": {
                _Cost3,
                _Discard,
                _DiscardResponse,
                _Filler,
                _Sifter,
            },
        },
        {
            "name": "Inspector",
            "types": {Action, Attack},
            "advTags": {_BadSifter, _Cost3, _Discard, _Reveal, _Sifter},
        },
        {
            "name": "Mastermind",
            "types": {Action},
            "advTags": {_BottomSeeder, _Cantrip, _Cost5, _Discard, _FreeAction},
        },
        {
            "name": "Mausoleum",
            "types": {Action},
            "advTags": {_Choice, _Cost6, _Draw2, _Saver, _Village},
        },
        {
            "name": "Mendicant",
            "types": {Action},
            "advTags": {_Cantrip, _Cost4, _Discard, _Junker, _VictoryGainer},
        },
        {
            "name": "Miner",
            "types": {Action},
            "advTags": {_Cantrip, _Cost3, _Discard, _Remodeler},
        },
        {
            "name": "Mission House",
            "types": {Action},
            "advTags": {_Cost5, _Discard, _Draw2, _VictoryGainer, _Village},
        },
        {
            "name": "Moundbuilder Village",
            "types": {Action},
            "advTags": {_Cost5, _Money3, _Peddler, _Thinner, _Village},
        },
        {
            "name": "Pharaoh",
            "types": {Action, Attack},
            "advTags": {_Cost8, _Curser, _Payload, _Terminal, _Trasher},
        },
        {
            "name": "Profiteer",
            "types": {Action},
            "advTags": {_Buys, _Chainer, _Cost3, _CostReducer},
        },
        {
            "name": "Pyramid",
            "types": {Action},
            "advTags": {_Buys, _Cost5, _Terminal, _Thinner, _Trasher, _VictoryGainer},
        },
        {
            "name": "Shipwreck",
            "types": {Action},
            "advTags": {
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
            "types": {Action},
            "advTags": {
                _Buys,
                _DeckSeeder,
                _FutureMoney1,
                _Trasher,
                _TrashGainer,
                _VictoryGainer,
            },
        },
        {
            "name": "Stronghold",
            "types": {Action, Reaction},
            "advTags": {
                _AttackResponse,
                _Cost5,
                _Shuffler,
                _Trasher,
                _Terminal,
                _Thinner,
            },
        },
        {
            "name": "Tomb Raider",
            "types": {Action, Attack},
            "advTags": {
                _AttackResponse,
                _Chainer,
                _Cost3,
                _Discard,
                _Gainer6,
            },
        },
        {
            "name": "Snake Charmer",
            "types": {Action, Attack},
            "advTags": {
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


def AdvancedRandomize(options, advTagDict, completeSet, landscapeSet=[]):
    """Sketch some thoughts here:
    1. Get all the Card tags and put them in a dict.
    2. Weight each of the card tags based on two things:
        a.  1 if 5 or more examples in pool
        b.  0.2 * # if 4 or less in pool
    3. Randomly pull a Card Tag.
    4. Randomly select a card with that Card Tag.
    5. Remove that Card Tag from the list of Card tags so we cannot get it again.
    6. Rebalance the weight of each Card Tag:
        a.  If it's already in the Results, -0.1 for each card with that type in the Results.
        b.  For each Card Tag in the Results that synnergizes with this card, increase
            the weight by +0.2, unless there is another example of this Card Tag in the
            Results.
        c.  For each Card Tag in the Results that wants this card, increase the weight by +1
        d.  "badTags" stop any synnergies from being applied to this type if they are present
    7. Repeat steps 3-6 until results are done. Do the same for landscapes.
    """
    resultSet = set()
    waySet = set()
    tagSet = set()
    for card in completeSet:
        tagSet = tagSet | card.advTags
    advTagDict = {}
    selectedTags = set()
    includedTags = set()
    # set the initial card type weights
    for cardTag in tagSet:
        advTagDict[cardTag] = (
            min(5, len([card for card in completeSet if cardTag in card.advTags])) * 1
        )
    counter = 0
    while len(resultSet) < 10:
        # choose a card type:
        if sum(advTagDict.values()) == 0:
            print("no matching tags...")
            # reset the weights
            for card in completeSet:
                tagSet = tagSet | card.advTags
            for cardTag in tagSet:
                advTagDict[cardTag] = (
                    min(
                        5,
                        len([card for card in completeSet if cardTag in card.advTags]),
                    )
                    * 1
                )
            print(sum(advTagDict.values()))
        cardTag = random.choices(list(advTagDict.keys()), list(advTagDict.values()))[0]
        cardsWithTag = [card for card in completeSet if cardTag in card.advTags]
        if cardsWithTag:
            cardDict = {}
            for cardWithTag in reversed(cardsWithTag):
                tagsForCardWithTag = [
                    advTagDict[cardsTag]
                    for cardsTag in cardWithTag.advTags
                    if cardsTag in advTagDict and cardsTag != cardTag
                ]
                if tagsForCardWithTag:
                    cardDict[cardWithTag] = int(
                        round(sum(tagsForCardWithTag) / len(tagsForCardWithTag), 0)
                    )
                else:
                    cardDict[cardWithTag] = 5
            selectedTags.add(cardTag)
            advTagDict.pop(cardTag)
        else:
            advTagDict.pop(cardTag)
            continue
        if sum(cardDict.values()) == 0:
            print("no matching cards...")
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
        badTags = set()
        bonusedTags = []
        wantedTags = []
        for cardTag in card.advTags:
            includedTags.add(cardTag)
        for cardTag in card.advTags:
            if cardTag in advTagDict:
                advTagDict[cardTag] = max(0, advTagDict[cardTag] - 1)
                for selectedTag in selectedTags:
                    badTags.add(badTag for badTag in selectedTag.badTags)
                for bonusTag in cardTag.bonusToTags:
                    if (
                        bonusTag in advTagDict
                        and bonusTag not in bonusedTags
                        and bonusTag not in badTags
                    ):
                        advTagDict[bonusTag] = advTagDict[bonusTag] + 6
                        bonusedTags.append(bonusTag)
                for wantedTag in cardTag.wantsTags:
                    if (
                        wantedTag in advTagDict
                        and wantedTag not in includedTags
                        and wantedTag not in wantedTags
                        and wantedTag not in badTags
                    ):
                        advTagDict[wantedTag] = advTagDict[wantedTag] + 50
                        wantedTags.append(wantedTag)
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
        return advTagDict, landscapeList, resultSet, waySet
    else:
        return advTagDict, [], resultSet, set()


def AdvancedSample(advTagDict, cardSet, completeSet, num):
    resultSet = set()
    tagSet = set()
    for card in cardSet:
        tagSet = tagSet | card.advTags
    selectedTags = set()
    includedTags = set()
    # set the initial card type weights
    for cardTag in tagSet:
        advTagDict[cardTag] = (
            min(5, len([card for card in cardSet if cardTag in card.advTags])) * 1
        )
    counter = 0
    while len(resultSet) < num:
        # choose a card type:
        if sum(advTagDict.values()) == 0:
            # reset card type weights
            for card in cardSet:
                tagSet = tagSet | card.advTags
            for cardTag in tagSet:
                advTagDict[cardTag] = (
                    min(
                        5,
                        len([card for card in completeSet if cardTag in card.advTags]),
                    )
                    * 1
                )
            print(sum(advTagDict.values()))
        cardTag = random.choices(list(advTagDict.keys()), list(advTagDict.values()))[0]
        cardsWithTag = [card for card in cardSet if cardTag in card.advTags]
        if cardsWithTag:
            cardDict = {}
            for cardWithTag in reversed(cardsWithTag):
                tagsForCardWithTag = [
                    advTagDict[cardsType]
                    for cardsType in cardWithTag.advTags
                    if cardsType in advTagDict and cardsType != cardTag
                ]
                if tagsForCardWithTag:
                    cardDict[cardWithTag] = math.ceil(
                        sum(tagsForCardWithTag) / len(tagsForCardWithTag)
                    )
                else:
                    cardDict[cardWithTag] = 5
            selectedTags.add(cardTag)
            advTagDict.pop(cardTag)
        else:
            advTagDict.pop(cardTag)
            continue
        card = random.choices(list(cardDict.keys()), list(cardDict.values()))[0]
        resultSet.add(card)
        counter += 1
        # Rebalance the card type weights
        badTags = set()
        bonusedTags = []
        wantedTags = []
        for cardTag in card.advTags:
            includedTags.add(cardTag)
        for cardTag in card.advTags:
            if cardTag in advTagDict:
                advTagDict[cardTag] = max(0, advTagDict[cardTag] - 1)
                for selectedTag in selectedTags:
                    badTags.add(badTag for badTag in selectedTag.badTags)
                for bonusTag in cardTag.bonusToTags:
                    if (
                        bonusTag in advTagDict
                        and bonusTag not in bonusedTags
                        and bonusTag not in badTags
                    ):
                        advTagDict[bonusTag] = advTagDict[bonusTag] + 6
                        bonusedTags.append(bonusTag)
                for wantedTag in cardTag.wantsTags:
                    if (
                        wantedTag in advTagDict
                        and wantedTag not in includedTags
                        and wantedTag not in wantedTags
                        and wantedTag not in badTags
                    ):
                        advTagDict[wantedTag] = advTagDict[wantedTag] + 50
                        wantedTags.append(wantedTag)

    return list(resultSet)


def BasicRandomize(options, advTagDict, completeSet, landscapes=False):
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
        return advTagDict, [], resultSet, set()


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
    advTagDict = {}

    if completeSet & LandscapeCards:
        # Handle sets that include landscape cards
        kingdomSet = completeSet - LandscapeCards
        landscapeSet = completeSet & LandscapeCards

        resultSet = set()
        waySet = set()

        # for testing only
        advTagDict, landscapeList, resultSet, waySet = AdvancedRandomize(
            options, advTagDict, completeSet, landscapeSet
        )

        # if options and options.get("advanced-randomization"):
        #    advTagDict, landscapeList, resultSet, waySet = AdvancedRandomize(
        #        options, advTagDict, completeSet, landscapeSet
        #    )
        # else:
        #    advTagDict, landscapeList, resultSet, waySet = BasicRandomize(
        #        options, advTagDict, completeSet, landscapeSet
        #    )
    else:
        kingdomSet = completeSet
        landscapeList = []

        if options and options.get("advanced-randomization"):
            advTagDict, landscapeList, resultSet, waySet = AdvancedRandomize(
                options, advTagDict, completeSet
            )
        else:
            advTagDict, landscapeList, resultSet, waySet = BasicRandomize(
                options, advTagDict, completeSet
            )

    # Enforce Alchemy rule
    if (options or {}).get("enforce-alchemy-rule", True):
        alchemyCards = Alchemy.cards & resultSet
        if len(alchemyCards) == 1:
            # If there's only 1 Alchemy card, remove Alchemy from the options
            # and draw an addtional Kingdom card
            resultSet -= alchemyCards
            resultSet.update(
                SampleDominion(
                    options, advTagDict, kingdomSet - resultSet, completeSet, 1
                )
            )
        elif len(alchemyCards) == 2:
            # If there are only 2 Alchemy cards, pull an additional Alchemy
            # card and randomly remove one non-Alchemy card
            resultSet -= alchemyCards
            alchemyCards.update(
                SampleDominion(
                    options, advTagDict, Alchemy.cards - alchemyCards, completeSet, 1
                )
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
                SampleDominion(
                    options, advTagDict, kingdomSet - resultSet, completeSet, 1
                )
            )
            baneCard = SampleDominion(
                options, advTagDict, resultSet & BaneCards, completeSet, 1
            )[0]
        else:
            baneCard = SampleDominion(
                options, advTagDict, eligibleBanes, completeSet, 1
            )[0]
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

            mouseCard = SampleDominion(
                options, advTagDict, eligibleMice, completeSet, 1
            )[0]
            resultSet.update(
                SampleDominion(
                    options, advTagDict, kingdomSet - resultSet, completeSet, 1
                )
            )
            resultSet.remove(mouseCard)
        else:
            mouseCard = SampleDominion(
                options, advTagDict, eligibleMice, completeSet, 1
            )[0]
        mouseSet.add(mouseCard)

    fullResults = resultSet.union(landscapeList)

    # Check for Colonies and Platinums
    includeColoniesAndPlatinum = Prosperity in sets and PlatinumLove.intersection(
        random.sample(fullResults, 1)
    )

    # Check for Potions
    includePotions = Alchemy.potionCards & resultSet

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


def SampleDominion(options, advTagDict, cardSet, completeSet, num):
    # Temporary for testing
    return AdvancedSample(advTagDict, cardSet, completeSet, num)
    # if options and options.get("advanced-randomization"):
    #     return AdvancedSample(advTagDict, cardSet, num)
    # else:
    #     return BasicSample(cardSet, num)


if __name__ == "__main__":
    print("\n".join(RandomizeDominion()))
