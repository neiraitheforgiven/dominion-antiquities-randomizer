import math
import random
import sys


Events = ['(Empires Event): Triumph', '(Empires Event): Annex',
        '(Empires Event): Donate', '(Empires Event): Advance',
        '(Adventures Event): Alms', '(Adventures Event): Borrow',
        '(Adventures Event): Quest', '(Adventures Event): Save',
        '(Empires Event): Delve', '(Adventures Event): Scouting Party',
        '(Empires Event): Tax', '(Adventures Event): Travelling Fair',
        '(Empires Event): Banquet', '(Adventures Event): Bonfire',
        '(Adventures Event): Expedition', '(Adventures Event): Ferry',
        '(Adventures Event): Plan', '(Adventures Event): Mission',
        '(Adventures Event): Pilgrimage', '(Empires Event): Ritual',
        '(Empires Event): Salt the Earth', '(Empires Event): Wedding',
        '(Adventures Event): Ball', '(Adventures Event): Raid',
        '(Adventures Event): Seaway', '(Empires Event): Trade',
        '(Empires Event): Windfall', '(Empires Event): Conquest',
        '(Adventures Event): Lost Arts', '(Adventures Event): Training',
        '(Adventures Event): Inheritance', '(Adventures Event): Pathfinding',
        '(Empires Event): Dominate']

Landmarks = ['(Empires Landmark): Aqueduct', '(Empires Landmark): Arena',
        '(Empires Landmark): Bandit Fort', '(Empires Landmark): Basilica',
        '(Empires Landmark): Baths', '(Empires Landmark): Battlefield',
        '(Empires Landmark): Colonnade', '(Empires Landmark): Defiled Shrine',
        '(Empires Landmark): Fountain', '(Empires Landmark): Keep',
        '(Empires Landmark): Labyrinth', '(Empires Landmark): Mountain Pass',
        '(Empires Landmark): Museum', '(Empires Landmark): Obelisk',
        '(Empires Landmark): Orchard', '(Empires Landmark): Palace',
        '(Empires Landmark): Tomb', '(Empires Landmark): Tower',
        '(Empires Landmark): Triumphal Arch', '(Empires Landmark): Wall',
        '(Empires Landmark): Wolf Den']

Projects = ['(Renaissance Project): Cathedral',
        '(Renaissance Project): City Gate', '(Renaissance Project): Pageant',
        '(Renaissance Project): Sewers', '(Renaissance Project): Star Chart',
        '(Renaissance Project): Exploration', '(Renaissance Project): Fair',
        '(Renaissance Project): Silos', '(Renaissance Project): Sinister Plot',
        '(Renaissance Project): Academy', '(Renaissance Project): Capitalism',
        '(Renaissance Project): Fleet', '(Renaissance Project): Guildhall',
        '(Renaissance Project): Piazza', '(Renaissance Project): Road Network',
        '(Renaissance Project): Barracks', '(Renaissance Project): Crop Rotation',
        '(Renaissance Project): Innovation', '(Renaissance Project): Canal',
        '(Renaissance Project): Citadel']

Base = ['Base: Cellar', 'Base: Chapel', 'Base: Moat', 'Base: Harbinger',
        'Base: Merchant', 'Base: Village', 'Base: Workshop', 'Base: Vassal',
        'Base: Bureaucrat', 'Base: Gardens', 'Base: Militia',
        'Base: Moneylender', 'Base: Poacher', 'Base: Remodel', 'Base: Remodel',
        'Base: Smithy', 'Base: Throne Room', 'Base: Bandit',
        'Base: Council Room', 'Base: Festival', 'Base: Laboratory',
        'Base: Library', 'Base: Market', 'Base: Mine', 'Base: Sentry',
        'Base: Witch', 'Base: Artisan']

Intrigue = ['Intrigue: Courtyard', 'Intrigue: Lurker', 'Intrigue: Pawn',
        'Intrigue: Masquerade', 'Intrigue: Shanty Town', 'Intrigue: Steward',
        'Intrigue: Swindler', 'Intrigue: Wishing Well', 'Intrigue: Baron',
        'Intrigue: Bridge', 'Intrigue: Conspirator', 'Intrigue: Diplomat',
        'Intrigue: Ironworks', 'Intrigue: Mill', 'Intrigue: Mining Village',
        'Intrigue: Secret Passage', 'Intrigue: Courtier', 'Intrigue: Duke',
        'Intrigue: Minion', 'Intrigue: Patrol', 'Intrigue: Replace',
        'Intrigue: Torturer', 'Intrigue: Trading Post', 'Intrigue: Upgrade',
        'Intrigue: Harem', 'Intrigue: Nobles']

Seaside = ['Seaside: Embargo', 'Seaside: Haven', 'Seaside: Lighthouse',
        'Seaside: Native Village', 'Seaside: Pearl Diver', 'Seaside: Ambassador',
        'Seaside: Fishing Village', 'Seaside: Lookout', 'Seaside: Smugglers',
        'Seaside: Warehouse', 'Seaside: Caravan', 'Seaside: Cutpurse',
        'Seaside: Island', 'Seaside: Navigator', 'Seaside: Pirate Ship',
        'Seaside: Salvager', 'Seaside: Sea Hag', 'Seaside: Treasure Map',
        'Seaside: Bazaar', 'Seaside: Explorer', 'Seaside: Ghost Ship',
        'Seaside: Merchant Ship', 'Seaside: Outpost', 'Seaside: Tactician',
        'Seaside: Treasury', 'Seaside: Wharf']

Alchemy = ['Alchemy: Herbalist', 'Alchemy: Apprentice', 'Alchemy: Transmute',
        'Alchemy: Vineyard', 'Alchemy: Apothecary', 'Alchemy: Scrying Pool',
        'Alchemy: University', 'Alchemy: Alchemist', 'Alchemy: Familiar',
        'Alchemy: Philosopher Stone', 'Alchemy: Golem', 'Alchemy: Possession']

PotionCards = ['Alchemy: Transmute', 'Alchemy: Vineyard', 'Alchemy: Apothecary',
        'Alchemy: Scrying Pool', 'Alchemy: University', 'Alchemy: Alchemist',
        'Alchemy: Familiar', 'Alchemy: Philosopher Stone', 'Alchemy: Golem',
        'Alchemy: Possession']

Prosperity = ['Prosperity: Loan', 'Prosperity: Trade Route',
        'Prosperity: Watchtower', 'Prosperity: Bishop', 'Prosperity: Monument',
        'Prosperity: Quarry', 'Prosperity: Talisman',
        'Prosperity: Worker Village', 'Prosperity: City',
        'Prosperity: Contraband', 'Prosperity: Counting House',
        'Prosperity: Mint', 'Prosperity: Mountebank', 'Prosperity: Rabble',
        'Prosperity: Royal Seal', 'Prosperity: Vault', 'Prosperity: Venture',
        'Prosperity: Goons', 'Prosperity: Grand Market', 'Prosperity: Hoard',
        'Prosperity: Bank', 'Prosperity: Expand', 'Prosperity: Forge',
        'Prosperity: King Court', 'Prosperity: Peddler']

PlatinumLove = Prosperity + ['Hinterlands: Fools Gold', 'Guilds: Masterpiece',
        'Alchemy: Philosopher Stone', 'Hinterlands: Cache',
        'Dark Ages: Counterfeit', 'Adventures: Treasure Trove',
        'Empires: Encampment/Plunder', 'Empires: Capital', 'Empires: Crown',
        'Empires: Gladiator/Fortune', 'Cornucopia: Tournament',
        'Nocturne: Secret Cave + Magic Lamp (Heirloom)',
        'Nocturne: Pooka + Cursed Gold (Heirloom)', 'Base: Merchant',
        'Base: Mine', 'Antiquities: Discovery', 'Antiquities: Gamepiece',
        'Seaside: Treasure Map', 'Seaside: Explorer', 'Dark Ages: Poor House',
        'Adventures: Page', 'Empires: Legionary', 'Nocturne: Tragic Hero',
        'Antiquities: Pyramid', 'Antiquities: Collector', 'Base: Council Room',
        'Hinterlands: Duchess', 'Hinterlands: Embassy', 'Adventures: Hireling',
        'Adventures: Lost City', 'Nocturne: Sacred Grove', 'Guilds: Soothsayer',
        'Empires: Chariot Race', 'Empires: Farmers Market, Empires: Castles',
        'Empires: Sacrifice', 'Empires: Temple', 'Empires: Patrician/Emporium',
        'Empires: Groundskeeper', 'Empires: Wild Hunt', 'Antiquities: Dig',
        'Antiquities: Mission House', 'Antiquities: Stoneworks',
        'Nocturne: Raider', 'Intrigue: Nobles', 'Intrigue: Harem',
        'Dark Ages: Hunting Grounds', 'Dark Ages: Altar', 'Base: Artisan',
        'Hinterlands: Border Village', 'Antiquities: Stronghold',
        'Antiquities: Mausoleum', 'Antiquities: Pharaoh', 'Antiquities: Encroach',
        'Antiquities: Archaeologist', 'Renaissance: Ducat',
        'Renaissance: Scepter', 'Renaissance: Spices']

Cornucopia = ['Cornucopia: Hamlet', 'Cornucopia: Fortune Teller',
        'Cornucopia: Menagerie', 'Cornucopia: Farming Village',
        'Cornucopia: Horse Traders', 'Cornucopia: Remake',
        'Cornucopia: Tournament', 'Cornucopia: Young Witch',
        'Cornucopia: Harvest', 'Cornucopia: Horn of Plenty',
        'Cornucopia: Hunting Party', 'Cornucopia: Jester',
        'Cornucopia: Fairgrounds']

Hinterlands = ['Hinterlands: Crossroads', 'Hinterlands: Duchess',
        'Hinterlands: Fools Gold', 'Hinterlands: Develop', 'Hinterlands: Oasis',
        'Hinterlands: Oracle', 'Hinterlands: Scheme', 'Hinterlands: Tunnel',
        'Hinterlands: Jack of all Trades', 'Hinterlands: Noble Brigand',
        'Hinterlands: Nomad Camp', 'Hinterlands: Silk Road',
        'Hinterlands: Spice Merchant', 'Hinterlands: Trader',
        'Hinterlands: Cache', 'Hinterlands: Cartographer',
        'Hinterlands: Embassy', 'Hinterlands: Haggler', 'Hinterlands: Highway',
        'Hinterlands: Ill-gotten Gains', 'Hinterlands: Inn',
        'Hinterlands: Mandarin', 'Hinterlands: Margrave', 'Hinterlands: Stables',
        'Hinterlands: Border Village', 'Hinterlands: Farmland']

DarkAges = ['Dark Ages: Poor House', 'Dark Ages: Beggar', 'Dark Ages: Squire',
        'Dark Ages: Vagrant', 'Dark Ages: Forager', 'Dark Ages: Hermit',
        'Dark Ages: Market Square', 'Dark Ages: Sage', 'Dark Ages: Storeroom',
        'Dark Ages: Urchin', 'Dark Ages: Armory', 'Dark Ages: Death Cart',
        'Dark Ages: Feodum', 'Dark Ages: Fortress', 'Dark Ages: Ironmonger',
        'Dark Ages: Marauder', 'Dark Ages: Procession', 'Dark Ages: Rats',
        'Dark Ages: Scavenger', 'Dark Ages: Wandering Minstrel',
        'Dark Ages: Band of Misfits', 'Dark Ages: Bandit Camp',
        'Dark Ages: Catacombs', 'Dark Ages: Count', 'Dark Ages: Counterfeit',
        'Dark Ages: Cultist', 'Dark Ages: Graverobber', 'Dark Ages: Junk Dealer',
        'Dark Ages: Knights', 'Dark Ages: Mystic', 'Dark Ages: Pillage',
        'Dark Ages: Rebuild', 'Dark Ages: Rogue', 'Dark Ages: Altar',
        'Dark Ages: Hunting Grounds']

ShelterLove = DarkAges + ['Base: Remodel', 'Base: Mine', 'Intrigue: Replace',
        'Intrigue: Upgrade', 'Prosperity: Expand', 'Prosperity: Forge',
        'Cornucopia: Remake', 'Hinterlands: Develop', 'Hinterlands: Farmland',
        'Guilds: Stonemason', 'Guilds: Taxman', 'Guilds: Butcher',
        'Adventures: Transmogrify', 'Nocturne: Necromancer + Zombies',
        'Nocturne: Exorcist', 'Seaside: Salvager', 'Alchemy: Apprentice',
        'Prosperity: Bishop', 'Hinterlands: Trader', 'Adventures: Raze',
        'Empires: Catapult/Rocks', 'Empires: Sacrifice', 'Antiquities: Collector',
        'Antiquities: Pharaoh', 'Antiquities: Profiteer',
        'Antiquities: Snake Charmer', 'Antiquities: Stoneworks',
        'Nocturne: Cemetary + Haunted Mirror (Heirloom)', 'Antiquities: Shipwreck',
        'Antiquities: Graveyard', 'Alchemy: Scrying Pool', 'Guilds: Journeyman',
        'Antiquities: Stronghold', 'Renaissance: Priest']

LooterCards = ['Dark Ages: Death Cart', 'Dark Ages: Marauder',
        'Dark Ages: Cultist']

SpoilsCards = ['Dark Ages: Bandit Camp', 'Dark Ages: Marauder',
        'Dark Ages: Pillage']

Guilds = ['Guilds: Candlestick Maker', 'Guilds: Stonemason', 'Guilds: Doctor',
        'Guilds: Masterpiece', 'Guilds: Advisor', 'Guilds: Plaza',
        'Guilds: Taxman', 'Guilds: Herald', 'Guilds: Baker', 'Guilds: Butcher',
        'Guilds: Journeyman', 'Guilds: Merchant Guild', 'Guilds: Soothsayer']

Adventures = ['Adventures: Coin of the Realm', 'Adventures: Page',
        'Adventures: Peasant', 'Adventures: Ratcatcher', 'Adventures: Raze',
        'Adventures: Amulet', 'Adventures: Caravan Guard', 'Adventures: Dungeon',
        'Adventures: Gear', 'Adventures: Guide', 'Adventures: Duplicate',
        'Adventures: Magpie', 'Adventures: Messenger', 'Adventures: Miser',
        'Adventures: Port', 'Adventures: Ranger', 'Adventures: Transmogrify',
        'Adventures: Artificer', 'Adventures: Bridge Troll',
        'Adventures: Distant Lands', 'Adventures: Giant',
        'Adventures: Haunted Woods', 'Adventures: Lost City',
        'Adventures: Relic', 'Adventures: Royal Carriage',
        'Adventures: Storyteller', 'Adventures: Swamp Hag',
        'Adventures: Treasure Trove', 'Adventures: Wine Merchant',
        'Adventures: Hireling']

Empires = ['Empires: Engineer', 'Empires: City Quarter', 'Empires: Overlord',
        'Empires: Royal Blacksmith', 'Empires: Encampment/Plunder',
        'Empires: Patrician/Emporium', 'Empires: Settlers/Bustling Village',
        'Empires: Castles', 'Empires: Catapult/Rocks', 'Empires: Chariot Race',
        'Empires: Enchantress', 'Empires: Farmers Market',
        'Empires: Gladiator/Fortune', 'Empires: Sacrifice', 'Empires: Temple',
        'Empires: Villa', 'Empires: Archive', 'Empires: Capital',
        'Empires: Charm', 'Empires: Crown', 'Empires: Forum',
        'Empires: Groundskeeper', 'Empires: Legionary', 'Empires: Wild Hunt']

Nocturne = ['Nocturne: Bard', 'Nocturne: Blessed Village',
        'Nocturne: Cemetary + Haunted Mirror (Heirloom)',
        'Nocturne: Changeling', 'Nocturne: Cobbler', 'Nocturne: Conclave',
        'Nocturne: Crypt', 'Nocturne: Cursed Village', 'Nocturne: Den of Sin',
        'Nocturne: Devils Workshop', 'Nocturne: Druid', 'Nocturne: Exorcist',
        'Nocturne: Faithful Hound',
        'Nocturne: Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)',
        'Nocturne: Guardian', 'Nocturne: Ghost Town', 'Nocturne: Idol',
        'Nocturne: Leprechaun', 'Nocturne: Monastery',
        'Nocturne: Necromancer + Zombies', 'Nocturne: Night Watchman',
        'Nocturne: Pixie + Goat (Heirloom)',
        'Nocturne: Pooka + Cursed Gold (Heirloom)', 'Nocturne: Sacred Grove',
        'Nocturne: Secret Cave + Magic Lamp (Heirloom)',
        'Nocturne: Shepherd + Pasture (Heirloom)', 'Nocturne: Raider',
        'Nocturne: Skulk', 'Nocturne: Tormentor',
        'Nocturne: Tracker + Pouch (Heirloom)', 'Nocturne: Tragic Hero',
        'Nocturne: Vampire', 'Nocturne: Werewolf']

BoonCards = ['Nocturne: Bard', 'Nocturne: Blessed Village', 'Nocturne: Druid',
        'Nocturne: Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)',
        'Nocturne: Idol', 'Nocturne: Pixie + Goat (Heirloom)',
        'Nocturne: Sacred Grove', 'Nocturne: Tracker + Pouch (Heirloom)']

HexCards = ['Nocturne: Cursed Village', 'Nocturne: Leprechaun',
        'Nocturne: Skulk', 'Nocturne: Tormentor', 'Nocturne: Vampire',
        'Nocturne: Werewolf']

WishCards = ['Nocturne: Leprechaun',
        'Nocturne: Secret Cave + Magic Lamp (Heirloom)']

Renaissance = ['Renaissance: Border Guard', 'Renaissance: Ducat',
        'Renaissance: Lackeys', 'Renaissance: Acting Troupe',
        'Renaissance: Cargo Ship', 'Renaissance: Experiment',
        'Renaissance: Improve', 'Renaissance: Flag Bearer',
        'Renaissance: Hideout', 'Renaissance: Inventor',
        'Renaissance: Mountain Village', 'Renaissance: Patron',
        'Renaissance: Priest', 'Renaissance: Research',
        'Renaissance: Silk Merchant', 'Renaissance: Old Witch',
        'Renaissance: Recruiter', 'Renaissance: Scepter', 'Renaissance: Scholar',
        'Renaissance: Sculptor', 'Renaissance: Seer', 'Renaissance: Spices',
        'Renaissance: Swashbuckler', 'Renaissance: Treasurer',
        'Renaissance: Villain']

Antiquities = ['Antiquities: Inscription', 'Antiquities: Agora',
        'Antiquities: Discovery', 'Antiquities: Aquifer',
        'Antiquities: Tomb Raider', 'Antiquities: Curio',
        'Antiquities: Gamepiece', 'Antiquities: Dig',
        'Antiquities: Moundbuilder Village', 'Antiquities: Encroach',
        'Antiquities: Stoneworks', 'Antiquities: Graveyard',
        'Antiquities: Inspector', 'Antiquities: Archaeologist',
        'Antiquities: Mission House', 'Antiquities: Mendicant',
        'Antiquities: Profiteer', 'Antiquities: Miner',
        'Antiquities: Pyramid', 'Antiquities: Mastermind',
        'Antiquities: Mausoleum', 'Antiquities: Shipwreck',
        'Antiquities: Collector', 'Antiquities: Pharaoh',
        'Antiquities: Grave Watcher', 'Antiquities: Stronghold',
        'Antiquities: Snake Charmer']

TrapLove = Antiquities + ['Base: Cellar', 'Base: Harbinger', 'Base: Vassal',
        'Base: Remodel', 'Base: Mine', 'Intrigue: Lurker', 'Intrigue: Baron',
        'Intrigue: Mill', 'Intrigue: Replace', 'Intrigue: Upgrade',
        'Seaside: Treasure Map', 'Seaside: Tactician', 'Alchemy: Transmute',
        'Prosperity: Watchtower', 'Prosperity: Bishop',
        'Prosperity: Counting House', 'Prosperity: Vault', 'Prosperity: Goons',
        'Prosperity: Expand', 'Prosperity: Forge', 'Cornucopia: Hamlet',
        'Cornucopia: Horse Traders', 'Cornucopia: Remake', 'Cornucopia: Harvest',
        'Hinterlands: Fools Gold', 'Hinterlands: Develop', 'Hinterlands: Tunnel',
        'Hinterlands: Jack of all Trades', 'Hinterlands: Trader',
        'Hinterlands: Inn', 'Hinterlands: Stables', 'Hinterlands: Farmland',
        'Dark Ages: Beggar', 'Dark Ages: Squire', 'Dark Ages: Hermit',
        'Dark Ages: Market Square', 'Dark Ages: Storeroom', 'Dark Ages: Urchin',
        'Dark Ages: Feodum', 'Dark Ages: Procession', 'Dark Ages: Rats',
        'Dark Ages: Scavenger', 'Dark Ages: Catacombs', 'Dark Ages: Graverobber',
        'Dark Ages: Pillage', 'Dark Ages: Rebuild', 'Dark Ages: Altar',
        'Dark Ages: Hunting Grounds', 'Guilds: Stonemason', 'Guilds: Herald',
        'Guilds: Plaza', 'Guilds: Taxman', 'Guilds: Butcher', 'Adventures: Guide',
        'Adventures: Transmogrify', 'Adventures: Artificer', 'Empires: Engineer',
        'Empires: Settlers/Bustling Village', 'Empires: Chariot Race',
        'Empires: Farmers Market', 'Empires: Catapult/Rocks',
        'Empires: Sacrifice', 'Empires: Temple', 'Empires: Patrician/Emporium',
        'Empires: Groundskeeper', 'Empires: Encampment/Plunder',
        'Empires: Wild Hunt', 'Empires: Castles', 'Nocturne: Changeling',
        'Nocturne: Secret Cave + Magic Lamp (Heirloom)', 'Nocturne: Exorcist',
        'Nocturne: Shepherd + Pasture (Heirloom)', 'Nocturne: Tragic Hero',
        'Nocturne: Vampire', 'Nocturne: Necromancer + Zombies',
        'Nocturne: Cemetary + Haunted Mirror (Heirloom)', 'Renaissance: Improve',
        'Renaissance: Mountain Village', 'Renaissance: Swashbuckler',
        'Renaissance: Border Guard']

BaneCards = ['Dark Ages: Vagrant', 'Dark Ages: Squire', 'Dark Ages: Beggar',
        'Hinterlands: Crossroads', 'Hinterlands: Duchess',
        'Hinterlands: Fools Gold', 'Cornucopia: Hamlet', 'Base: Moat',
        'Base: Chapel', 'Base: Cellar', 'Intrigue: Courtyard', 'Intrigue: Lurker',
        'Intrigue: Pawn', 'Seaside: Embargo', 'Alchemy: Herbalist',
        'Seaside: Pearl Diver', 'Seaside: Native Village', 'Seaside: Lighthouse',
        'Seaside: Haven', 'Adventures: Coin of the Realm', 'Adventures: Page',
        'Adventures: Peasant', 'Adventures: Ratcatcher', 'Adventures: Raze',
        'Guilds: Candlestick Maker', 'Guilds: Stonemason',
        'Empires: Settlers/Bustling Village', 'Empires: Patrician/Emporium',
        'Empires: Encampment/Plunder', 'Dark Ages: Urchin',
        'Dark Ages: Storeroom', 'Dark Ages: Sage', 'Dark Ages: Market Square',
        'Dark Ages: Hermit', 'Dark Ages: Forager', 'Hinterlands: Develop',
        'Hinterlands: Oasis', 'Hinterlands: Scheme', 'Hinterlands: Tunnel',
        'Prosperity: Trade Route', 'Prosperity: Watchtower', 'Prosperity: Loan',
        'Cornucopia: Fortune Teller', 'Cornucopia: Menagerie',
        'Intrigue: Masquerade', 'Intrigue: Shanty Town', 'Intrigue: Steward',
        'Intrigue: Swindler', 'Intrigue: Wishing Well', 'Base: Harbinger',
        'Base: Merchant', 'Base: Village', 'Base: Workshop', 'Base: Vassal',
        'Seaside: Fishing Village', 'Seaside: Lookout', 'Seaside: Ambassador',
        'Seaside: Warehouse', 'Seaside: Smugglers', 'Adventures: Amulet',
        'Adventures: Caravan Guard', 'Adventures: Dungeon', 'Adventures: Gear',
        'Adventures: Guide', 'Guilds: Doctor', 'Guilds: Masterpiece',
        'Empires: Castles', 'Empires: Gladiator', 'Empires: Farmers Market',
        'Empires: Encantress', 'Empires: Chariot Race', 'Empires: Catapult/Rocks',
        'Empires: Gladiator/Forture', 'Antiquities: Discovery',
        'Antiquities: Tomb Raider', 'Antiquities: Inscription',
        'Antiquities: Inspector', 'Antiquities: Gamepiece', 'Antiquties: Miner',
        'Antiquities: Shipwreck', 'Antiquities: Profiteer',
        'Antiquities: Grave Watcher', 'Nocturne: Druid',
        'Nocturne: Faithful Hound', 'Nocturne: Pixie + Goat (Heirloom)',
        'Nocturne: Tracker + Pouch (Heirloom)',
        'Nocturne: Fool + Lucky Coin (Heirloom) + Lost In the Woods (State)',
        'Nocturne: Secret Cave + Magic Lamp (Heirloom)', 'Nocturne: Guardian',
        'Nocturne: Monastery', 'Nocturne: Changeling', 'Nocturne: Ghost Town',
        'Nocturne: Leprechaun', 'Nocturne: Night Watchman',
        'Renaissance: Border Guard', 'Renaissance: Ducat', 'Renaissance: Lackeys',
        'Renaissance: Acting Troupe', 'Renaissance: Cargo Ship',
        'Renaissance: Experiment', 'Renaissance: Improve']

#Make full list + Events + Landmarks to determine landmarks
completeList = Events + Landmarks + Projects + Base + Intrigue + Seaside + Alchemy + \
        Prosperity + Cornucopia + Hinterlands + DarkAges + Guilds + Adventures + \
        Empires + Antiquities + Nocturne + Renaissance


def RandomizeDominion():
    #Check 10% of all cards for Events
    random.shuffle(completeList)
    tempList = completeList[:int(math.ceil(len(completeList)/10))]
    eventList = []
    for t in tempList:
        if t in Events:
            eventList = eventList + [t]
    eventList = eventList[:len(eventList)%2]

    #Check 10% of all cards for Landmarks
    random.shuffle(completeList)
    tempList = completeList[:int(math.ceil(len(completeList)/10))]
    landmarkList = []
    for t in tempList:
        if t in Landmarks:
            landmarkList = landmarkList + [t]
    landmarkList = landmarkList[:len(landmarkList)%2]

    #Check 10% of all cards for Projects
    random.shuffle(completeList)
    tempList = completeList[:int(math.ceil(len(completeList)/10))]
    projectList = []
    for t in tempList:
        if t in Projects:
            projectList = projectList + [t]
    projectList = projectList[:len(projectList)%2]

    #Pull cards
    pullList = Base + Intrigue + Seaside + Alchemy + Prosperity + Cornucopia + \
            Hinterlands + DarkAges + Guilds + Adventures + Empires + Antiquities + \
            Nocturne + Renaissance
    random.shuffle(pullList)
    resultList = pullList[:10]

    #enforce Alchemy rule
    alcCount = 0
    for r in resultList:
        if r in Alchemy:
            alcCount = alcCount + 1
    #if there's only 1 alchemy card, remove alchemy from the options and redraw Kingdom cards
    if alcCount == 1:
        pullList = list(set(pullList) - set(Alchemy))
        random.shuffle(pullList)
        resultList = pullList[:10]
    #if there's only alchemy cards, pull 3 alchemy cards, and then randomize the rest from not alchemy
    if alcCount == 2:
        random.shuffle(Alchemy)
        alcList = Alchemy[:3]
        pullList = list(set(pullList) - set(alcList))
        resultList = alcList + pullList[:7]
    #if there are 3 or more alchemy cards, let it lie.

    #Check for Potions
    includePotions = set(resultList) & set(PotionCards)

    #Check for Shelters
    random.shuffle(resultList)
    includeShelters = set(resultList[:2]) & set(ShelterLove)

    #Check for Looters
    includeLooters = set(resultList) & set(LooterCards)

    #Check for Colonies and Platinums
    random.shuffle(resultList)
    includeColPlat = set(resultList[:2]) & set(PlatinumLove)

    #Check for Boulder traps
    random.shuffle(resultList)
    includeBTraps = set(resultList[:1]) & set(TrapLove)

    #Check for Madman
    includeMadman = 'Dark Ages: Hermit' in resultList
    #Check for Mercenary
    includeMercenary = 'Dark Ages: Urchin' in resultList
    #Check for Spoils
    includeSpoils = set(SpoilsCards) & set(resultList)

    # add Prizes
    includePrizes = 'Cornucopia: Tournament' in resultList

    includeGhost = set(['Nocturne: Cemetary + Haunted Mirror (Heirloom)',
            'Nocturne: Exorcist']) & set(resultList)

    includeBoons = set(resultList) & set(BoonCards)
    includeHex = set(resultList) & set(HexCards)

    includeWisp = includeBoons or ('Nocturne: Exorcist' in resultList)

    includeBat = 'Nocturne: Vampire' in resultList

    includeImp = set(['Nocturne: Devils Workshop', 'Nocturne: Exorcist',
            'Nocturne: Tormentor']) & set(resultList)

    includeWish = set(['Nocturne: Leprechaun',
            'Nocturne: Secret Cave + Magic Lamp (Heirloom)']) & set(resultList)

    # create final list
    additionalCards = []

    if includePotions:
        additionalCards = additionalCards + ['Alchemy: Potions']
    if includeShelters:
        additionalCards = additionalCards + ['Dark Ages: Shelters']
    if includeLooters:
        additionalCards = additionalCards + ['Dark Ages: Ruins']
    if includeColPlat:
        additionalCards = additionalCards + ['Prosperity: Colony',
                'Prosperity: Platinum']
    if includeBTraps:
        additionalCards = additionalCards + ['Antiquities: Boulder Traps']
    if includeMadman:
        additionalCards = additionalCards + ['Dark Ages: Madman']
    if includeMercenary:
        additionalCards = additionalCards + ['Dark Ages: Mercenary']
    if includeSpoils:
        additionalCards = additionalCards + ['Dark Ages: Spoils']
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

    finalResult = list(sorted(resultList + additionalCards))

    #Young Witch Support
    includeBane = 'Cornucopia: Young Witch' in resultList
    if includeBane:
        eligibleBanes = list(set(BaneCards) - set(resultList))
        random.shuffle(eligibleBanes)
        baneCard = ['Bane is ' + eligibleBanes[0]]
        finalResult = finalResult + baneCard

    finalResult = finalResult + list(sorted(eventList + landmarkList + projectList))

    return '\n'.join(finalResult)


if __name__ == '__main__':
    print(RandomizeDominion())
