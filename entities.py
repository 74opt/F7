import random
from colored import *

####################################################################################################################
####################################################################################################################
####################################################################################################################
class Weapon:
    def __init__(self, name, damage, rarity, level, hitrate, description, prefix, weptype, rof):
        self.name = name
        self.damage = int(damage * (level ** 2.3))
        self.rarity = rarity
        self.level = level
        self.hitrate = hitrate
        self.description = description
        self.prefix = prefix
        self.weptype = weptype
        self.rof = rof
        return

    prefix_dict = {
        # good prefixes
        'Accurate': 1,
        'Corrosive': 1,
        'Damaging': 1,
        'Fiery': 1,
        'Roguish': 1,
        # bad prefixes
        'Betraying': 1,
        'Lazy': 1,
        'Worn': 1
    }

    def addprefix(self, prefix):
        self.prefix = prefix
        return

    # displays stats of weapon
    def showstats(self):
        # keeps list of colors for different rarity
        # https://gitlab.com/dslackw/colored use for reference
        rarity_color = {
            'Common': 94,
            'Uncommon': 33,
            'Rare': 120,
            'Unbelievable': 14,
            'God-Crafted': 9
        }

        prefix_color = {
            'Accurate': 182,
            'Damaging': 129,
            'Fiery': 208,
            'Roguish': 28,
            'Betraying': 136,
            'Lazy': 252,
            '': 0
        }

        if self.prefix != '':
            print(stylize('Level ' + str(self.level) + ' ' + stylize(self.prefix, fg(prefix_color[self.prefix])) + ' ' + self.name, attr('bold')))
        else:
            print('Level', self.level, self.name)
        print(stylize(self.rarity, fg(rarity_color[self.rarity])), self.weptype)
        print(stylize('Damage:', attr('bold')), self.damage)
        print(stylize('Accuracy:', attr('bold')), str(self.hitrate) + '%')
        if self.weptype == 'Shotgun' or self.weptype == 'Full-Auto Gun':
            rof_dict = {
                'Shotgun': stylize('Pellets:', attr('bold')),
                'Full-Auto Gun': stylize('Rate of Fire:', attr('bold'))
            }

            print(rof_dict[self.weptype], self.rof)
        if self.description != '':
            print('\n' + self.description)
        return

# weapon attr: name, damage, rarity, hitrate, description, prefix, weapon type, rate of fire/pellets
# Note: Shotguns and Full-Autos have their damage for each bullet
# common
no_weapon = Weapon('Nothing', 0, 'Common', 0, 0, '', '', 'Melee', 0)

steel_sword = Weapon('Steel Sword', 10, 'Common', 1, 70, '', '', 'Melee', 1)

dagger = Weapon('Dagger', 12, 'Common', 1, 60, '', '', 'Melee', 1)

# uncommon
pistol = Weapon('Pistol', 22, 'Uncommon', 1, 60, '', '', 'Semi-Auto Gun', 1)

revolver = Weapon('Revolver', 30, 'Uncommon', 1, 50, '', '', 'Semi-Auto Gun', 1)

# rare
double_barrel = Weapon('Double-Barrel Shotgun', 4, 'Rare', 1, 50, '', '', 'Shotgun', 16)

fifty_cal =  Weapon('50. Caliber Rifle', 40, 'Rare', 1, 45, '', '', 'Semi-Auto Gun', 1)

# unbelievable
gauss_gun = Weapon('13R-Gauss Gun', 14, 'Unbelievable', 1, 95, 'It\'s still a prototype, not very strong, but beautifully accurate.', '', 'Semi-Auto Gun', 1)

disvita = Weapon('Disvita', 24, 'Unbelievable', 1, 80, 'And Weezrrer Corp. brought upon the people, a rocket-powered sledgehammer.', '', 'Melee', 1)

# god-crafted
intrensia = Weapon('Intrensia', 26, 'God-Crafted', 30, 85,
                   'Which God created the first Intrensia? No one knows.\nBut it\'s got a sick golden finish and the blade\'s\none of the sharpest things any living being has ever seen.\nPerfect.',
                   'Betraying', 'Melee', 1)

tachyon_minigun = Weapon('Tachyon Minigun', 2, 'God-Crafted', 1, 65, 'Sub-atomic penetration, rapid fire. Get a grip\non this instrument of death.', 'Fiery', 'Full-Auto Gun', 60)

# dict for weapons
weapon_dict = {
    'Common': [steel_sword, dagger],
    'Uncommon': [pistol, revolver],
    'Rare': [double_barrel, fifty_cal],
    'Unbelievable': [gauss_gun, disvita],
    'God-Crafted': [intrensia, tachyon_minigun]
}


####################################################################################################################
####################################################################################################################
####################################################################################################################
class Enemy:
    def __init__(self, name, health, damage, rarity, hitrate, entype, description):
        self.level = None
        self.name = name
        self.health = health
        self.damage = damage
        self.rarity = rarity
        self.hitrate = hitrate
        self.entype = entype
        self.description = description
        return

    def showstats(self):
        rarity_color = {
            'Common': 94,
            'Uncommon': 33,
            'Rare': 120,
            'Special': 14,
            'God-Like': 9
        }

        if self.description == '':
            print(stylize('Level', attr('bold')), stylize(self.level, attr('bold')), stylize(self.name, attr('bold')),
                  '\n' + stylize(self.rarity, fg(rarity_color.get(self.rarity))),
                  self.entype, stylize('\nHealth:', attr('bold')), stylize(self.health, fg(9)),
                  stylize('\nAverage Damage:', attr('bold')), stylize(self.damage, fg(9)))
        else:
            print(stylize('Level', attr('bold')), stylize(self.level, attr('bold')), stylize(self.name, attr('bold')),
                  '\n' + stylize(self.rarity, fg(rarity_color.get(self.rarity))),
                  self.entype, stylize('\nHealth:', attr('bold')), stylize(self.health, fg(9)),
                  stylize('\nAverage Damage:', attr('bold')), stylize(self.damage, fg(9)), '\n\n' + self.description)
        return


# enemy attr: name, health, damage, rarity, hitrate, enemy type, description
# common
bear = Enemy('Bear', 7, 4, 'Common', 68, 'Slasher', '')

# uncommon
nomad = Enemy('Nomad', 9, 4, 'Uncommon', 75, 'Fistfighter', '')

# rare
F3 = Enemy('F3', 6, 6, 'Rare', 84, 'Gunslinger', 'A younger generation of the F series android. \nProgrammed only to obey. Watch out.')

chainsaw_guy = Enemy('Logger', 9, 11, 'Rare', 35, 'Slasher', 'Their bulky chainsaw isn\'t very accurate, but will destroy you.')

mutated_hawk = Enemy('Mutated Hawk', 7, 8, 'Rare', 70, 'Mutant', 'They\'ve been hanging around the radiation for way too long.')

# special
fishman = Enemy('Fishman', 12, 6, 'Special', 80, 'Mutant', 'Not a fisherman... A literal fishman.')

# demigod
angel = Enemy('Angel', 8, 10, 'God-Like', 93, 'Magical Being', 'They really don\'t want you messing around with nature...')

# dictionaries of enemies
plains_enemies = {
    'Common': [bear],
    'Uncommon': [nomad],
    'Rare': [chainsaw_guy, mutated_hawk],
    'Special': [fishman],
    'God-Like': [angel]
}

# flavor text for enemies:
flavor_text = {
    'Slasher': [
            'slices into you!', 'slashes the metal off you!', 'scrapes the metal off your arm!',
            'scrapes the metal off your leg!', 'slashes into your chest!', 'leaves a mark on your face!'
        ],
    'Gunslinger': [
        'shoots into your arm!', 'hits the mark!', 'shoots your leg!', 'grazes you!',
        'uses their accurate eye and hits you!', 'gets a hit on you!', 'hits a bullet right through you!'
    ],
    'Mutant': [
        'spits acid at you!', 'hits you with their diseased body!', 'bites you!',
        'swipes at you and hits!', 'penetrates through your arm!', 'penetrates through your leg!'
    ],
    'Fistfighter': [
        'knocks you right in the chest!', 'uppercuts you!', 'smacks you right in the head!',
        'makes a dent in your chest!', 'makes a dent in your arm!', 'jabs you!'
    ],
    'Magical Being': [
        'blasts you!', 'hits you with some strange force!', 'casts rays of damage upon you!',
        'summons flames and hits you!', 'summons a hailstorm of stones!', 'zaps you!'
    ]
}

flavor_text_miss = ['just barely gets you, but misses!', 'tries to attack, but you dodge it!', 'embarrassingly misses!',
                    'accidentally hits the ground!', 'attacks the air instead of you!', 'almost hits you by an inch!',
                    'hesitates and doesn\'t get the chance to attack!', 'zones out and doesn\'t attack!',
                    'gets distracted and doesn\'t attack!', 'was so close to hitting you!', 'can\'t seem to get you!',
                    'doesn\'t hit!', 'misses!', 'attacks, and you successfully dodge!', 'gets frustrated and misses!',
                    'gets frustrated from your dodge!', 'was about to hit you, but you dodge!']


####################################################################################################################
####################################################################################################################
####################################################################################################################
class Shield:
    def __init__(self, name, resist, turns, rarity):
        self.name = name
        self.resist = resist
        self.turns = turns
        self.rarity = rarity
        return

    def showstats(self):

        rarity_color = {
            'Common': 94,
            'Uncommon': 33,
            'Rare': 120,
            'Astronomical': 14,
            'Holy': 9
        }

        print(stylize(self.name, attr('bold')))
        print(stylize(self.rarity, fg(rarity_color[self.rarity])), 'Shield')
        print(stylize('Resistance:', attr('bold')), stylize(str(self.resist) + '%', fg(128)))
        print(stylize('Effective Time:', attr('bold')), stylize(str(self.turns) + ' turns', fg(122)))


# shield attr: name, resistance, turns, rarity
# common
makeshift = Shield('Makeshift Shield', 50, 2, 'Common')
no_shield = Shield('Nothing', 0, 0, 'Common')

# uncommon
civilian = Shield('Civilian Shield', 70, 1, 'Uncommon')

# rare
military = Shield('Military-Grade Shield', 65, 4, 'Rare')

# astronomical
nasa = Shield('NASA Prototype Shield', 90, 3, 'Astronomical')

# holy
aegis = Shield('Aegis-11', 100, 1, 'Holy')

shield_dict = {
    'Common': [makeshift],
    'Uncommon': [civilian],
    'Rare': [military],
    'Astronomical': [nasa],
    'Holy': [aegis]
}

####################################################################################################################
####################################################################################################################
####################################################################################################################
# lists for scrap

common_scrap = ['Wood', 'Sheet Metal', 'Rope', 'Duct Tape', 'Stone']

uncommon_scrap = ['Gunpowder', 'Reinforced Metal', 'Basic Battery', 'Barbed Wire']

rare_scrap = ['Future Corp. H72 Battery', 'Q-TYPE Adhesive XXIV', 'Harnessed Plasma']

####################################################################################################################
####################################################################################################################
####################################################################################################################
# crafting recipes


scrap_craft = {
    'Future Corp. H72 Battery': ['Basic Battery', 'Basic Battery', 'Sheet Metal', 'Gunpowder'],
    'Q-TYPE Adhesive XXIV': ['Duct Tape', 'Reinforced Metal'],
    'Harnessed Plasma': ['Future Corp. H72 Battery', 'Future Corp. H72 Battery'],
}

consume_craft = {
    'Toolbox': ['Duct Tape', 'Sheet Metal'],
    'Flashbang': ['Gunpowder', 'Gunpowder', 'Sheet Metal'],
    'Targeting Chip': ['Basic Battery', 'Reinforced Metal'],
    'Corrosion Grenade': ['Reinforced Metal', 'Gunpowder'],
    'Metallic Aura': ['Reinforced Metal', 'Harnessed Plasma'],
    'Smokescreen': ['Sheet Metal', 'Gunpowder'],
}

shield_craft = {
    makeshift.name: [[makeshift], ['Basic Battery', 'Sheet Metal', 'Duct Tape']],
    civilian.name: [[civilian], ['Basic Battery', 'Reinforced Metal', 'Duct Tape', 'Duct Tape']],
    military.name: [[military], ['Basic Battery', 'Basic Battery', 'Reinforced Metal', 'Reinforced Metal']],
    nasa.name: [[nasa], ['Harnessed Plasma', 'Basic Battery', 'Reinforced Metal']],
    aegis.name: [[aegis], ['Harnessed Plasma', 'Harnessed Plasma', 'Future Corp. H72 Battery']],
}

weapon_craft = {
    double_barrel.name: [[double_barrel], ['Stone', 'Sheet Metal', 'Gunpowder', 'Wood', 'Wood']],
    fifty_cal.name: [[fifty_cal], ['Reinforced Metal', 'Reinforced Metal', 'Gunpowder', 'Gunpowder']],
    gauss_gun.name: [[gauss_gun], ['Harnessed Plasma', 'Basic Battery', 'Reinforced Metal']],
    disvita.name: [[disvita], ['Reinforced Metal', 'Reinforced Metal', 'Sheet Metal', 'Gunpowder']],
    intrensia.name: [[intrensia], ['Reinforced Metal', 'Reinforced Metal', 'Reinforced Metal', 'Reinforced Metal', 'Q-TYPE Adhesive XXIV']],
    tachyon_minigun.name: [[tachyon_minigun], ['Harnessed Plasma', 'Future Corp. H72 Battery', 'Reinforced Metal', 'Gunpowder']]
}
