import math
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
        return '<randomizer.Card: {}>'.format(self)

    def __gt__(self, other):
        return str(self) > str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __str__(self):
        if Event in self.types:
            formatStr = '({} Event): {}'
        elif Landmark in self.types:
            formatStr = '({} Landmark): {}'
        elif Project in self.types:
            formatStr = '({} Project): {}'
        else:
            formatStr = '{}: {}'
        return formatStr.format(self.set.name, self.name)


class Set(object):
    def __init__(self, name):
        global AllSets
        self.name = name
        self._cards = CardList()

        self._events = None
        self._landmarks = None
        self._projects = None
        self._potionCards = None

        AllSets[self.name] = self

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '<randomizer.Set: {}>'.format(self.name)

    def AddCards(self, cards):
        for cardData in cards:
            if isinstance(cardData, dict):
                card = Card(**cardData)
                card.set = self
                self.cards.add(card)
            else:
                # Assume card data is name for now
                self.cards.add(Card(cardData, cardSet=self))

    @property
    def cards(self):
        return self._cards

    @property
    def events(self):
        if self._events is None:
            self._events = CardList(
                card for card in self._cards if card.types & {Event})
        return self._events

    @property
    def landmarks(self):
        if self._landmarks is None:
            self._landmarks = CardList(
                card for card in self._cards if card.types & {Landmark})
        return self._landmarks

    @property
    def projects(self):
        if self._projects is None:
            self._projects = CardList(
                card for card in self._cards if card.types & {Project})
        return self._projects

    @property
    def potionCards(self):
        if self._potionCards is None:
            self._potionCards = CardList(
                card for card in self._cards if card.types & {Potion})
        return self._potionCards


Event = CardType('Event')
Landmark = CardType('Landmark')
Project = CardType('Project')
Potion = CardType('Potion')


Base = Set('Base')
Base.AddCards([
    'Cellar', 'Chapel', 'Moat', 'Harbinger', 'Merchant', 'Village', 'Workshop',
    'Vassal', 'Bureaucrat', 'Gardens', 'Militia', 'Moneylender', 'Poacher',
    'Remodel', 'Remodel', 'Smithy', 'Throne Room', 'Bandit', 'Council Room',
    'Festival', 'Laboratory', 'Library', 'Market', 'Mine', 'Sentry', 'Witch',
    'Artisan'
])

Intrigue = Set('Intrigue')
Intrigue.AddCards([
    'Courtyard', 'Lurker', 'Pawn', 'Masquerade', 'Shanty Town', 'Steward',
    'Swindler', 'Wishing Well', 'Baron', 'Bridge', 'Conspirator', 'Diplomat',
    'Ironworks', 'Mill', 'Mining Village', 'Secret Passage', 'Courtier',
    'Duke', 'Minion', 'Patrol', 'Replace', 'Torturer', 'Trading Post',
    'Upgrade', 'Harem', 'Nobles'
])

Seaside = Set('Seaside')
Seaside.AddCards([
    'Embargo', 'Haven', 'Lighthouse', 'Native Village', 'Pearl Diver',
    'Ambassador', 'Fishing Village', 'Lookout', 'Smugglers', 'Warehouse',
    'Caravan', 'Cutpurse', 'Island', 'Navigator', 'Pirate Ship', 'Salvager',
    'Sea Hag', 'Treasure Map', 'Bazaar', 'Explorer', 'Ghost Ship',
    'Merchant Ship', 'Outpost', 'Tactician', 'Treasury', 'Wharf'
])

Alchemy = Set('Alchemy')
Alchemy.AddCards([
    'Herbalist', 'Apprentice',
    {'name': 'Transmute', 'types': {Potion}},
    {'name': 'Vineyard', 'types': {Potion}},
    {'name': 'Apothecary', 'types': {Potion}},
    {'name': 'Scrying Pool', 'types': {Potion}},
    {'name': 'University', 'types': {Potion}},
    {'name': 'Alchemist', 'types': {Potion}},
    {'name': 'Familiar', 'types': {Potion}},
    {'name': 'Philosopher Stone', 'types': {Potion}},
    {'name': 'Golem', 'types': {Potion}},
    {'name': 'Possession', 'types': {Potion}}
])

Prosperity = Set('Prosperity')
Prosperity.AddCards([
    'Loan', 'Trade Route', 'Watchtower', 'Bishop', 'Monument', 'Quarry',
    'Talisman', 'Worker Village', 'City', 'Contraband', 'Counting House',
    'Mint', 'Mountebank', 'Rabble', 'Royal Seal', 'Vault', 'Venture', 'Goons',
    'Grand Market', 'Hoard', 'Bank', 'Expand', 'Forge', "King's Court",
    'Peddler'
])

Cornucopia = Set('Cornucopia')
Cornucopia.AddCards([
    'Hamlet', 'Fortune Teller', 'Menagerie', 'Farming Village',
    'Horse Traders', 'Remake', 'Tournament', 'Young Witch', 'Harvest',
    'Horn of Plenty', 'Hunting Party', 'Jester', 'Fairgrounds'
])

Hinterlands = Set('Hinterlands')
Hinterlands.AddCards([
    'Crossroads', 'Duchess', 'Fools Gold', 'Develop', 'Oasis', 'Oracle',
    'Scheme', 'Tunnel', 'Jack of all Trades', 'Noble Brigand', 'Nomad Camp',
    'Silk Road', 'Spice Merchant', 'Trader', 'Cache', 'Cartographer',
    'Embassy', 'Haggler', 'Highway', 'Ill-gotten Gains', 'Inn', 'Mandarin',
    'Margrave', 'Stables', 'Border Village', 'Farmland'
])

DarkAges = Set('Dark Ages')
DarkAges.AddCards([
    'Poor House', 'Beggar', 'Squire', 'Vagrant', 'Forager', 'Hermit',
    'Market Square', 'Sage', 'Storeroom', 'Urchin', 'Armory', 'Death Cart',
    'Feodum', 'Fortress', 'Ironmonger', 'Marauder', 'Procession', 'Rats',
    'Scavenger', 'Wandering Minstrel', 'Band of Misfits', 'Bandit Camp',
    'Catacombs', 'Count', 'Counterfeit', 'Cultist', 'Graverobber',
    'Junk Dealer', 'Knights', 'Mystic', 'Pillage', 'Rebuild', 'Rogue', 'Altar',
    'Hunting Grounds'
])

Guilds = Set('Guilds')
Guilds.AddCards([
    'Candlestick Maker', 'Stonemason', 'Doctor', 'Masterpiece', 'Advisor',
    'Plaza', 'Taxman', 'Herald', 'Baker', 'Butcher', 'Journeyman',
    'Merchant Guild', 'Soothsayer'
])

Adventures = Set('Adventures')
Adventures.AddCards([
    'Coin of the Realm', 'Page', 'Peasant', 'Ratcatcher', 'Raze', 'Amulet',
    'Caravan Guard', 'Dungeon', 'Gear', 'Guide', 'Duplicate', 'Magpie',
    'Messenger', 'Miser', 'Port', 'Ranger', 'Transmogrify', 'Artificer',
    'Bridge Troll', 'Distant Lands', 'Giant', 'Haunted Woods', 'Lost City',
    'Relic', 'Royal Carriage', 'Storyteller', 'Swamp Hag', 'Treasure Trove',
    'Wine Merchant', 'Hireling',
    {'name': 'Alms', 'types': {Event}},
    {'name': 'Borrow', 'types': {Event}},
    {'name': 'Quest', 'types': {Event}},
    {'name': 'Save', 'types': {Event}},
    {'name': 'Scouting Party', 'types': {Event}},
    {'name': 'Travelling Fair', 'types': {Event}},
    {'name': 'Bonfire', 'types': {Event}},
    {'name': 'Expedition', 'types': {Event}},
    {'name': 'Ferry', 'types': {Event}},
    {'name': 'Plan', 'types': {Event}},
    {'name': 'Mission', 'types': {Event}},
    {'name': 'Pilgrimage', 'types': {Event}},
    {'name': 'Ball', 'types': {Event}},
    {'name': 'Raid', 'types': {Event}},
    {'name': 'Seaway', 'types': {Event}},
    {'name': 'Lost Arts', 'types': {Event}},
    {'name': 'Training', 'types': {Event}},
    {'name': 'Inheritance', 'types': {Event}},
    {'name': 'Pathfinding', 'types': {Event}}
])

Empires = Set('Empires')
Empires.AddCards([
    'Engineer', 'City Quarter', 'Overlord', 'Royal Blacksmith',
    'Encampment/Plunder', 'Patrician/Emporium', 'Settlers/Bustling Village',
    'Castles', 'Catapult/Rocks', 'Chariot Race', 'Enchantress',
    'Farmers Market', 'Gladiator/Fortune', 'Sacrifice', 'Temple', 'Villa',
    'Archive', 'Capital', 'Charm', 'Crown', 'Forum', 'Groundskeeper',
    'Legionary', 'Wild Hunt',
    {'name': 'Advance', 'types': {Event}},
    {'name': 'Annex', 'types': {Event}},
    {'name': 'Banquet', 'types': {Event}},
    {'name': 'Conquest', 'types': {Event}},
    {'name': 'Delve', 'types': {Event}},
    {'name': 'Dominate', 'types': {Event}},
    {'name': 'Donate', 'types': {Event}},
    {'name': 'Salt the Earth', 'types': {Event}},
    {'name': 'Ritual', 'types': {Event}},
    {'name': 'Tax', 'types': {Event}},
    {'name': 'Trade', 'types': {Event}},
    {'name': 'Triumph', 'types': {Event}},
    {'name': 'Wedding', 'types': {Event}},
    {'name': 'Windfall', 'types': {Event}},
    {'name': 'Aqueduct', 'types': {Landmark}},
    {'name': 'Arena', 'types': {Landmark}},
    {'name': 'Bandit Fort', 'types': {Landmark}},
    {'name': 'Basilica', 'types': {Landmark}},
    {'name': 'Baths', 'types': {Landmark}},
    {'name': 'Battlefield', 'types': {Landmark}},
    {'name': 'Colonnade', 'types': {Landmark}},
    {'name': 'Defiled Shrine', 'types': {Landmark}},
    {'name': 'Fountain', 'types': {Landmark}},
    {'name': 'Keep', 'types': {Landmark}},
    {'name': 'Labyrinth', 'types': {Landmark}},
    {'name': 'Mountain Pass', 'types': {Landmark}},
    {'name': 'Museum', 'types': {Landmark}},
    {'name': 'Obelisk', 'types': {Landmark}},
    {'name': 'Orchard', 'types': {Landmark}},
    {'name': 'Palace', 'types': {Landmark}},
    {'name': 'Tomb', 'types': {Landmark}},
    {'name': 'Tower', 'types': {Landmark}},
    {'name': 'Triumphal Arch', 'types': {Landmark}},
    {'name': 'Wall', 'types': {Landmark}},
    {'name': 'Wolf Den', 'types': {Landmark}},
])

Nocturne = Set('Nocturne')
Nocturne.AddCards([
    'Bard', 'Blessed Village', 'Cemetary + Haunted Mirror (Heirloom)',
    'Changeling', 'Cobbler', 'Conclave', 'Crypt', 'Cursed Village',
    'Den of Sin', 'Devils Workshop', 'Druid', 'Exorcist', 'Faithful Hound',
    'Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)', 'Guardian',
    'Ghost Town', 'Idol', 'Leprechaun', 'Monastery', 'Necromancer + Zombies',
    'Night Watchman', 'Pixie + Goat (Heirloom)',
    'Pooka + Cursed Gold (Heirloom)', 'Sacred Grove',
    'Secret Cave + Magic Lamp (Heirloom)', 'Shepherd + Pasture (Heirloom)',
    'Raider', 'Skulk', 'Tormentor', 'Tracker + Pouch (Heirloom)',
    'Tragic Hero', 'Vampire', 'Werewolf'
])

Renaissance = Set('Renaissance')
Renaissance.AddCards([
    'Border Guard', 'Ducat', 'Lackeys', 'Acting Troupe', 'Cargo Ship',
    'Experiment', 'Improve', 'Flag Bearer', 'Hideout', 'Inventor',
    'Mountain Village', 'Patron', 'Priest', 'Research', 'Silk Merchant',
    'Old Witch', 'Recruiter', 'Scepter', 'Scholar', 'Sculptor', 'Seer',
    'Spices', 'Swashbuckler', 'Treasurer', 'Villain',
    {'name': 'Cathedral', 'types': {Project}},
    {'name': 'City Gate', 'types': {Project}},
    {'name': 'Pageant', 'types': {Project}},
    {'name': 'Sewers', 'types': {Project}},
    {'name': 'Star Chart', 'types': {Project}},
    {'name': 'Exploration', 'types': {Project}},
    {'name': 'Fair', 'types': {Project}},
    {'name': 'Silos', 'types': {Project}},
    {'name': 'Sinister Plot', 'types': {Project}},
    {'name': 'Academy', 'types': {Project}},
    {'name': 'Capitalism', 'types': {Project}},
    {'name': 'Fleet', 'types': {Project}},
    {'name': 'Guildhall', 'types': {Project}},
    {'name': 'Piazza', 'types': {Project}},
    {'name': 'Road Network', 'types': {Project}},
    {'name': 'Barracks', 'types': {Project}},
    {'name': 'Crop Rotation', 'types': {Project}},
    {'name': 'Innovation', 'types': {Project}},
    {'name': 'Canal', 'types': {Project}},
    {'name': 'Citadel', 'types': {Project}},
])

Antiquities = Set('Antiquities')
Antiquities.AddCards([
    'Inscription', 'Agora', 'Discovery', 'Aquifer', 'Tomb Raider', 'Curio',
    'Gamepiece', 'Dig', 'Moundbuilder Village', 'Encroach', 'Stoneworks',
    'Graveyard', 'Inspector', 'Archaeologist', 'Mission House', 'Mendicant',
    'Profiteer', 'Miner', 'Pyramid', 'Mastermind', 'Mausoleum', 'Shipwreck',
    'Collector', 'Pharaoh', 'Grave Watcher', 'Stronghold', 'Snake Charmer'
])

Events = Adventures.events | Empires.events

Landmarks = Empires.landmarks

Projects = Renaissance.projects

PotionCards = Alchemy.potionCards

PlatinumLove = Prosperity.cards.union(
    Base.cards('Artisan', 'Council Room', 'Merchant', 'Mine'),
    Intrigue.cards('Harem', 'Nobles'),
    Seaside.cards('Explorer', 'Treasure Map'),
    Alchemy.cards('Philosopher Stone'),
    Cornucopia.cards('Tournament'),
    Hinterlands.cards(
        'Border Village', 'Cache', 'Duchess', 'Embassy', 'Fools Gold'
    ),
    DarkAges.cards('Altar', 'Counterfeit', 'Hunting Grounds', 'Poor House'),
    Guilds.cards('Masterpiece', 'Soothsayer'),
    Adventures.cards('Hireling', 'Lost City', 'Page', 'Treasure Trove'),
    Empires.cards(
        'Capital', 'Castles', 'Chariot Race', 'Crown', 'Encampment/Plunder',
        'Farmers Market', 'Gladiator/Fortune', 'Groundskeeper', 'Legionary',
        'Patrician/Emporium', 'Sacrifice', 'Temple', 'Wild Hunt'
    ),
    Nocturne.cards(
        'Pooka + Cursed Gold (Heirloom)', 'Raider', 'Sacred Grove',
        'Secret Cave + Magic Lamp (Heirloom)', 'Tragic Hero'
    ),
    Renaissance.cards('Ducat', 'Scepter', 'Spices'),
    Antiquities.cards(
        'Archaeologist', 'Collector', 'Dig', 'Discovery', 'Encroach',
        'Gamepiece', 'Mausoleum', 'Mission House', 'Pharaoh', 'Pyramid',
        'Stoneworks', 'Stronghold'
    )
)

ShelterLove = DarkAges.cards.union(
    Base.cards('Remodel', 'Mine'),
    Intrigue.cards('Replace', 'Upgrade'),
    Seaside.cards('Salvager'),
    Alchemy.cards('Apprentice', 'Scrying Pool'),
    Prosperity.cards('Bishop', 'Expand', 'Forge'),
    Cornucopia.cards('Remake'),
    Hinterlands.cards('Develop', 'Farmland', 'Trader'),
    Adventures.cards('Raze', 'Transmogrify'),
    Empires.cards('Catapult/Rocks', 'Sacrifice'),
    Guilds.cards('Butcher', 'Journeyman', 'Stonemason', 'Taxman'),
    Nocturne.cards(
        'Cemetary + Haunted Mirror (Heirloom)', 'Exorcist',
        'Necromancer + Zombies'
    ),
    Renaissance.cards('Priest'),
    Antiquities.cards(
        'Collector', 'Graveyard', 'Pharaoh', 'Profiteer', 'Shipwreck',
        'Snake Charmer', 'Stoneworks', 'Stronghold'
    )
)

LooterCards = DarkAges.cards('Death Cart', 'Marauder', 'Cultist')

SpoilsCards = DarkAges.cards('Bandit Camp', 'Marauder', 'Pillage')

BoonCards = Nocturne.cards(
    'Bard', 'Blessed Village', 'Druid',
    'Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)', 'Idol',
    'Pixie + Goat (Heirloom)', 'Sacred Grove', 'Tracker + Pouch (Heirloom)'
)

HexCards = Nocturne.cards(
    'Cursed Village', 'Leprechaun', 'Skulk', 'Tormentor', 'Vampire', 'Werewolf'
)

WishCards = Nocturne.cards('Leprechaun', 'Secret Cave + Magic Lamp (Heirloom)')

TrapLove = Antiquities.cards.union(
    Base.cards('Cellar', 'Harbinger', 'Vassal', 'Remodel', 'Mine'),
    Intrigue.cards('Lurker', 'Baron', 'Mill', 'Replace', 'Upgrade'),
    Seaside.cards('Treasure Map', 'Tactician'),
    Alchemy.cards('Transmute'),
    Prosperity.cards(
        'Watchtower', 'Bishop', 'Counting House', 'Vault', 'Goons', 'Expand',
        'Forge'
    ),
    Cornucopia.cards('Hamlet', 'Horse Traders', 'Remake', 'Harvest'),
    Hinterlands.cards(
        'Fools Gold', 'Develop', 'Tunnel', 'Jack of all Trades', 'Trader',
        'Inn', 'Stables', 'Farmland'
    ),
    DarkAges.cards(
        'Beggar', 'Squire', 'Hermit', 'Market Square', 'Storeroom', 'Urchin',
        'Feodum', 'Procession', 'Rats', 'Scavenger', 'Catacombs',
        'Graverobber', 'Pillage', 'Rebuild', 'Altar', 'Hunting Grounds'
    ),
    Guilds.cards('Stonemason', 'Herald', 'Plaza', 'Taxman', 'Butcher'),
    Adventures.cards('Guide', 'Transmogrify', 'Artificer'),
    Empires.cards(
        'Engineer', 'Settlers/Bustling Village', 'Chariot Race',
        'Farmers Market', 'Catapult/Rocks', 'Sacrifice', 'Temple',
        'Patrician/Emporium', 'Groundskeeper', 'Encampment/Plunder',
        'Wild Hunt', 'Castles'
    ),
    Nocturne.cards(
        'Changeling', 'Secret Cave + Magic Lamp (Heirloom)', 'Exorcist',
        'Shepherd + Pasture (Heirloom)', 'Tragic Hero', 'Vampire',
        'Necromancer + Zombies', 'Cemetary + Haunted Mirror (Heirloom)'
    ),
    Renaissance.cards(
        'Improve', 'Mountain Village', 'Swashbuckler', 'Border Guard'
    )
)

BaneCards = set().union(
    Adventures.cards(
        'Amulet', 'Caravan Guard', 'Coin of the Realm', 'Dungeon', 'Gear',
        'Guide', 'Page', 'Peasant', 'Ratcatcher', 'Raze'
    ),
    Alchemy.cards('Herbalist'),
    Antiquities.cards(
        'Discovery', 'Gamepiece', 'Grave Watcher', 'Inscription', 'Inspector',
        'Profiteer', 'Shipwreck', 'Tomb Raider', 'Miner'
    ),
    Base.cards(
        'Cellar', 'Chapel', 'Harbinger', 'Merchant', 'Moat', 'Vassal',
        'Village', 'Workshop'
    ),
    Cornucopia.cards('Fortune Teller', 'Hamlet', 'Menagerie'),
    DarkAges.cards(
        'Beggar', 'Forager', 'Hermit', 'Market Square', 'Sage', 'Squire',
        'Storeroom', 'Urchin', 'Vagrant'
    ),
    Empires.cards(
        'Castles', 'Catapult/Rocks', 'Chariot Race', 'Encampment/Plunder',
        'Enchantress', 'Farmers Market', 'Gladiator', 'Gladiator/Forture',
        'Patrician/Emporium', 'Settlers/Bustling Village'
    ),
    Guilds.cards('Candlestick Maker', 'Doctor', 'Masterpiece', 'Stonemason'),
    Hinterlands.cards(
        'Crossroads', 'Develop', 'Duchess', 'Fools Gold', 'Oasis', 'Scheme',
        'Tunnel'
    ),
    Intrigue.cards(
        'Courtyard', 'Lurker', 'Masquerade', 'Pawn', 'Shanty Town', 'Steward',
        'Swindler', 'Wishing Well'
    ),
    Nocturne.cards(
        'Changeling', 'Druid', 'Faithful Hound',
        'Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)',
        'Ghost Town', 'Guardian', 'Leprechaun', 'Monastery', 'Night Watchman',
        'Pixie + Goat (Heirloom)', 'Secret Cave + Magic Lamp (Heirloom)',
        'Tracker + Pouch (Heirloom)'
    ),
    Prosperity.cards('Loan', 'Trade Route', 'Watchtower'),
    Renaissance.cards(
        'Acting Troupe', 'Border Guard', 'Cargo Ship', 'Ducat', 'Experiment',
        'Improve', 'Lackeys'
    ),
    Seaside.cards(
        'Ambassador', 'Embargo', 'Fishing Village', 'Haven', 'Lighthouse',
        'Lookout', 'Native Village', 'Pearl Diver', 'Smugglers', 'Warehouse'
    )
)


def RandomizeDominion(setNames=None):
    # Make full list + Events + Landmarks to determine landmarks
    sets = set()
    if setNames is None:
        sets.update(AllSets.values())
    else:
        for setName in setNames:
            if setName in AllSets:
                sets.add(AllSets[setName])

    completeSet = set().union(*(cardSet.cards for cardSet in sets))
    completeList = list(completeSet)

    # Check 10% of all cards for Events
    random.shuffle(completeList)
    tempList = completeList[:int(math.ceil(len(completeList) / 10))]
    eventList = []
    for t in tempList:
        if t in Events:
            eventList = eventList + [t]
    eventList = eventList[:len(eventList) % 2]

    # Check 10% of all cards for Landmarks
    random.shuffle(completeList)
    tempList = completeList[:int(math.ceil(len(completeList) / 10))]
    landmarkList = []
    for t in tempList:
        if t in Landmarks:
            landmarkList = landmarkList + [t]
    landmarkList = landmarkList[:len(landmarkList) % 2]

    # Check 10% of all cards for Projects
    random.shuffle(completeList)
    tempList = completeList[:int(math.ceil(len(completeList) / 10))]
    projectList = []
    for t in tempList:
        if t in Projects:
            projectList = projectList + [t]
    projectList = projectList[:len(projectList) % 2]

    # Pull cards
    pullSet = completeSet - (Events | Landmarks | Projects)
    pullList = list(pullSet)
    random.shuffle(pullList)
    resultList = pullList[:10]

    # enforce Alchemy rule
    alcCount = 0
    for r in resultList:
        if r in Alchemy.cards:
            alcCount = alcCount + 1
    # if there's only 1 alchemy card, remove alchemy from the options and
    # redraw Kingdom cards
    if alcCount == 1:
        pullSet -= Alchemy.cards
        pullList = list(pullSet)
        random.shuffle(pullList)
        resultList = pullList[:10]
    # if there's only alchemy cards, pull 3 alchemy cards, and then randomize
    # the rest from not alchemy
    if alcCount == 2:
        alcList = list(Alchemy.cards)
        random.shuffle(alcList)
        alcList = alcList[:3]
        pullSet -= set(alcList)
        pullList = list(pullSet)
        random.shuffle(pullList)
        resultList = alcList + pullList[:7]
    # if there are 3 or more alchemy cards, let it lie.

    # Check for Potions
    includePotions = set(resultList) & Alchemy.potionCards

    # Check for Shelters
    random.shuffle(resultList)
    includeShelters = DarkAges in sets and set(resultList[:2]) & ShelterLove

    # Check for Colonies and Platinums
    random.shuffle(resultList)
    includeColPlat = Prosperity in sets and set(resultList[:2]) & PlatinumLove

    # Check for Boulder traps
    random.shuffle(resultList)
    includeBTraps = Antiquities in sets and set(resultList[:1]) & TrapLove

    resultSet = set(resultList)

    # Check for Looters
    includeLooters = LooterCards & resultSet
    # Check for Madman
    includeMadman = DarkAges.cards('Hermit') & resultSet
    # Check for Mercenary
    includeMercenary = DarkAges.cards('Urchin') & resultSet
    # Check for Spoils
    includeSpoils = SpoilsCards & resultSet

    # add Prizes
    includePrizes = Cornucopia.cards('Tournament') & resultSet

    includeGhost = resultSet & Nocturne.cards(
        'Cemetary + Haunted Mirror (Heirloom)', 'Exorcist')

    includeBoons = resultSet & BoonCards
    includeHex = resultSet & HexCards

    includeWisp = includeBoons or (Nocturne.cards('Exorcist') & resultSet)

    includeBat = Nocturne.cards('Vampire') & resultSet

    includeImp = resultSet & Nocturne.cards(
        'Devils Workshop', 'Exorcist', 'Tormentor')

    includeWish = resultSet & Nocturne.cards(
        'Leprechaun', 'Secret Cave + Magic Lamp (Heirloom)')

    # create final list
    additionalCards = []

    if includePotions:
        additionalCards = additionalCards + ['Alchemy: Potions']
    if includeShelters:
        additionalCards = additionalCards + ['Dark Ages: Shelters']
    if includeLooters:
        additionalCards = additionalCards + ['Dark Ages: Ruins']
    if includeColPlat:
        additionalCards = additionalCards + [
            'Prosperity: Colony', 'Prosperity: Platinum']
    if includeBTraps:
        additionalCards = additionalCards + ['Antiquities: Boulder Traps']
    if includeMadman:
        additionalCards = additionalCards + ['Dark Ages: Madman']
    if includeMercenary:
        additionalCards = additionalCards + ['Dark Ages: Mercenary']
    if includeSpoils:
        additionalCards = additionalCards + ['Dark Ages: Spoils']
    if includePrizes:
        additionalCards = additionalCards + [
            'Cornucopia: Bag of Gold',
            'Cornucopia: Diadem',
            'Cornucopia: Followers',
            'Cornucopia: Princess',
            'Cornucopia: Trusty Steed'
        ]
    if includeGhost:
        additionalCards = additionalCards + ['Nocturne: Ghost']
    if includeBoons:
        additionalCards = additionalCards + ['Nocturne: Boons Deck']
    if includeHex:
        additionalCards = additionalCards + ['Nocturne: Hexes Deck']
    if includeWisp:
        additionalCards = additionalCards + ['Nocturne: Will-o-wisp']
    if includeBat:
        additionalCards = additionalCards + ['Nocturne: Bat']
    if includeImp:
        additionalCards = additionalCards + ['Nocturne: Imp']
    if includeWish:
        additionalCards = additionalCards + ['Nocturne: Wish']

    finalResult = sorted(resultList + additionalCards)

    # Young Witch Support
    includeBane = resultSet & Cornucopia.cards('Young Witch')
    if includeBane:
        eligibleBanes = list((pullSet & BaneCards) - resultSet)
        random.shuffle(eligibleBanes)
        baneCard = ['Bane is {}'.format(eligibleBanes[0])]
        finalResult = finalResult + baneCard

    finalResult = finalResult + sorted(eventList + landmarkList + projectList)

    return [str(card) for card in finalResult]


if __name__ == '__main__':
    print('\n'.join(RandomizeDominion()))
