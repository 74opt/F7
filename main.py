# MATTHIEU DE ROBLES EVEN 4
# The greatest project of all time kiddo

import random  # for some reason, random and import dont appear as used? pycharm what?
from colored import *
import time as t
import os
from playsound import playsound
from levels import *
from entities import *
import cutscene  # cut out the cutscene features
import copy
import threading
import platform
import json


# clearing screen differs between systems so i need to do this
def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    return


def main_music():
    while True:
        playsound('music/F7_music.wav')
    return


menu = threading.Thread(target=main_music)  # music gets to play while the rest of code runs god bless threading
menu.start()


# F7 code
class Player:
    def __init__(self, name, health, temphealth, level, exp, weapon1, weapon2, weapon3, weapon4, weapon_equipped, x, y, shield):
        self.name = name
        self.health = health
        self.temphealth = temphealth
        self.level = level
        self.exp = exp
        self.weapon1 = weapon1
        self.weapon2 = weapon2
        self.weapon3 = weapon3
        self.weapon4 = weapon4
        self.weapon_equipped = weapon_equipped
        self.x = x
        self.y = y
        self.shield = shield
        return

    # F7's consumables
    consumable_list = []

    def add_consumable(self, consumable):
        self.consumable_list.append(consumable)
        self.consumable_list.sort()
        return

    # F7's scrap
    scrap_list = []

    def add_scrap(self, scrap):
        self.scrap_list.append(scrap)
        self.scrap_list.sort()
        return

    def addexp(self, add):
        self.exp += add
        self.levelup()
        return

    def levelup(self):  # increases level and the stats
        exp_needed = int(200 + 300 * self.level ** 1.6)
        if self.exp >= exp_needed:
            self.level += 1
            self.exp -= exp_needed
            self.health += int((self.health * .95) * (self.level ** .0001))
            self.temphealth = self.health
            self.levelup()
        return

    # inventory
    # will contain:
    # 4 slots for weapons
    # consumable section
    # shows amount of money (if i add merchants)
    # 1/11: dear past me: MONEY??? MERCHANTS????

    def equip_weapon(self):  # switches out the weapon being used
        clear()
        print('Select a weapon to equip.')
        print('a)', self.weapon1.name)
        print('b)', self.weapon2.name)
        print('c)', self.weapon3.name)
        print('d)', self.weapon4.name)
        weapon_wanted = input()

        weapon_equipping_dict = {
            'a': self.weapon1,
            'b': self.weapon2,
            'c': self.weapon3,
            'd': self.weapon4
        }

        if weapon_wanted in weapon_equipping_dict:
            self.weapon_equipped = weapon_equipping_dict[weapon_wanted]
            print(weapon_equipping_dict[weapon_wanted].name, 'equipped.')
            t.sleep(2)
            self.showstats()
        else:
            print('That\'s not an option.')
            t.sleep(2)
            self.showstats()
        return

    def throwaway(self):  #  throws out a weapon in the inventory
        clear()
        print('Select a weapon to remove. (You will not get this weapon back!)')
        print('a)', self.weapon1.name)
        print('b)', self.weapon2.name)
        print('c)', self.weapon3.name)
        print('d)', self.weapon4.name)
        print('e) Nevermind')
        weapon_removed = input()

        weapon_removal_dict = {
            'a': self.weapon1,
            'b': self.weapon2,
            'c': self.weapon3,
            'd': self.weapon4,
            'e': ''
        }
        # i had to use a lot of if elses because it wasn't working with just this dict. That sucks.
        # 1/11: you could also use multiple functions and dicts and something?
        if weapon_removed in weapon_removal_dict and weapon_removed != 'e':
            print('Are you sure you want to do this? (y/n)')
            confirm = input()
            if confirm.lower() == 'y':
                print(weapon_removal_dict[weapon_removed].name, 'removed.')
                if weapon_removed == 'a':
                    if self.weapon1 == self.weapon_equipped:
                        self.weapon_equipped = no_weapon
                    self.weapon1 = no_weapon
                elif weapon_removed == 'b':
                    if self.weapon2 == self.weapon_equipped:
                        self.weapon_equipped = no_weapon
                    self.weapon2 = no_weapon
                elif weapon_removed == 'c':
                    if self.weapon3 == self.weapon_equipped:
                        self.weapon_equipped = no_weapon
                    self.weapon3 = no_weapon
                elif weapon_removed == 'd':
                    if self.weapon4 == self.weapon_equipped:
                        self.weapon_equipped = no_weapon
                    self.weapon4 = no_weapon
                t.sleep(2)
                self.showstats()
            elif confirm.lower() == 'n':
                print('Ok.')
                t.sleep(2)
                self.showstats()
            else:
                print('Not an option, canceling action.')
                t.sleep(2)
                self.showstats()
        elif weapon_removed == 'e':
            print('Canceling action.')
            t.sleep(2)
            self.showstats()
        else:
            print('Not an option, canceling action.')
            t.sleep(2)
            self.showstats()
        return

    def inspect(self):  # shows stats of a weapon
        clear()
        print('What weapon would you like to inspect?')
        print('a)', self.weapon1.name)
        print('b)', self.weapon2.name)
        print('c)', self.weapon3.name)
        print('d)', self.weapon4.name)
        inspection = input()
        clear()

        weapon_inspection = {
            'a': self.weapon1,
            'b': self.weapon2,
            'c': self.weapon3,
            'd': self.weapon4
        }

        if inspection in weapon_inspection and weapon_inspection[inspection] != no_weapon:
            weapon_inspection[inspection].showstats()
            print('\n\nInput any key to exit')
            exiting = input()
            print('Exiting...')
        elif weapon_inspection[inspection] == no_weapon:
            print('You can\'t inspect nothing!')
        else:
            print('That is not an option.')
        t.sleep(2)
        self.showstats()
        return

    def use_toolbox(self):  # toolboxes are the only useful consumable outside of combat
        before_health = self.temphealth
        if 'Toolbox' in self.consumable_list:
            toolbox()
            amount_restored = self.temphealth - before_health
            print('Toolbox used.', stylize(amount_restored, fg(9)), 'health restored.')
        else:
            print('You do not have any toolboxes.')
        t.sleep(2)
        self.showstats()
        return

    def setpos(self, x, y):
        self.x = x
        self.y = y
        return

    # shows your stats + inventory
    def showstats(self):  # main inventory menu
        clear()
        # note: maybe make an exp bar with ascii? (no.)
        print(
            stylize('F7-Model 891M', fg(50), attr('bold')), '\n\nCopyright 2112, Future Corp.\nVersion:',
            stylize('null error, version non-existant or from a third party.', fg(9)),
            stylize('\n\nLevel:', attr('bold')), self.level,
            stylize('\nExperience Points:', attr('bold')), stylize(str(int(self.exp)), fg(46)), 'out of',
            stylize(str(int(200 + 300 * self.level ** 1.6)), fg(46)), '(' +
            str(round((self.exp/int(200 + 300 * self.level ** 1.6)) * 100, 2)) + '%)', stylize('\nHealth:', attr('bold')),
            stylize(str(self.temphealth), fg(9)), 'out of',
            stylize(str(self.health), fg(9)), '(' + str(round((self.temphealth/self.health) * 100, 2)) + '%)', '\n\nPlease contact', stylize('[number terminated]', fg(246)),
            'for more info.', stylize('\n\nInventory:', attr('bold')), stylize('\nEquipped Weapon:', attr('bold')),
            self.weapon_equipped.name, stylize('\nWeapons:', attr('bold')), '\n1:',
            self.weapon1.name, '\n2:', self.weapon2.name, '\n3:', self.weapon3.name, '\n4:', self.weapon4.name, stylize('\n\nShield:', attr('bold')))

        self.shield.showstats()

        print(stylize('\nConsumables:', attr('bold')))

        for i in self.consumable_list:
            print(i)

        print(stylize('\nScrap:', attr('bold')))

        for i in self.scrap_list:
            print(i)

        print(stylize('\n\nWhat would you like to do?', attr('bold')))
        print('a) Exit Inventory')
        print('b) Use Toolbox')
        print('c) Equip New Weapon')
        print('d) Throw Item Away')
        print('e) Inspect Weapon')

        inventory_input = input()

        inventory_options = {
            'a': travel.travel_menu,
            'b': self.use_toolbox,
            'c': self.equip_weapon,
            'd': self.throwaway,
            'e': self.inspect
        }

        if inventory_input in inventory_options:
            inventory_options[inventory_input]()
        else:
            print('That\'s not an option.')
            t.sleep(2)
            self.showstats()
        return


# consumables
def toolbox():  # the rest of the consumables are in the combat class
    restoration = random.randint(15, 20) / 100
    F7.temphealth += F7.health * restoration
    F7.temphealth = int(F7.temphealth)
    if F7.temphealth > F7.health:
        excess = F7.temphealth - F7.health
        F7.temphealth -= excess
        print('Too much power detected. Releasing excess health.', stylize(excess, fg(9)), 'health removed.')
        t.sleep(2)
    F7.consumable_list.remove('Toolbox')
    return


# for when you get consumables in hacking storage
common_consume = ['Toolbox', 'Smokescreen']

uncommon_consume = ['Corrosive Grenade', 'Targeting Chip']

rare_consume = ['Metallic Aura', 'Flashbang']

# creating F7
F7 = Player('F7', 50, 50, 1, 0, dagger, no_weapon, no_weapon, no_weapon, dagger, 0, 0, makeshift)

'''
This was for dev testing
F7 = Player('F7', 18, 18000, 1, 0, dagger, steel_sword, double_barrel, tachyon_minigun, dagger, 0, 0, makeshift)

for i in range(2):
    F7.add_consumable('Toolbox')
    F7.add_consumable('Flashbang')
    F7.add_consumable('Targeting Chip')
    F7.add_consumable('Corrosion Grenade')
    F7.add_consumable('Metallic Aura')
    F7.add_consumable('Smokescreen')

F7.addexp(61075)

for i in range(3):
    F7.add_scrap('Wood')

for i in range(4):
    F7.add_scrap('Basic Battery')

#F7.showstats()
'''

# combat
# gonna be turn based
# different choices: (kinda like pokemon)
# attack
# use consumable
# run
# switch weapon
# defend


# combat menu
class Combat:
    def __init__(self, area):
        # lots of booleans because of all the possible things that could
        # be in effect during combat
        self.area = area
        self.turn = None
        self.enemy = None
        self.enemy_shield_up = False
        self.player_shield_up = False
        self.corrosive = False
        self.start = True
        self.shield_allowed = True
        self.countdown = 0
        self.flash_countdown = 0
        self.chip = False
        self.metal = False
        self.smoke = False

    def spawn_enemy(self):
        x = random.randint(1, 100)

        area_dict = {
            'plains': plains_enemies
        }

        chance_dict = {
            'x <= 60': 'Common',
            '60 < x <= 81': 'Uncommon',
            '81 < x <= 93': 'Rare',
            '93 < x <= 99': 'Special',
            'x >= 100': 'God-Like'
        }

        minimum_level = {
            'plains': 1,
            'forest': 5,
            'city': 10
        }

        maximum_level = {
            'plains': 10,
            'forest': 20,
            'city': 30
        }

        for key in chance_dict:
            check = eval(key)  # x gets used here
            if check:
                self.enemy = copy.deepcopy(area_dict[self.area][chance_dict[key]][random.randint(0, len(area_dict[self.area][chance_dict[key]]) - 1)])
                # above line basically does:
                # enemy spawned = the randomly chosen enemy of the specified area of the randomly chosen rarity
                self.enemy.level = F7.level + random.randint(-1, 1)
                if self.enemy.level < minimum_level[self.area]:
                    self.enemy.level = minimum_level[self.area]
                if self.enemy.level > maximum_level[self.area]:
                    self.enemy.level = maximum_level[self.area]
                damage_randomness = int(random.randint(-3, 4) * (self.enemy.level / random.randint(1, 3)))
                health_randomness = int(random.randint(-2, 2) * (self.enemy.level / random.randint(1, 2))) + damage_randomness / random.randint(2, 4)
                self.enemy.health *= int(self.enemy.health * (self.enemy.level ** 1) + health_randomness)
                self.enemy.damage *= int(self.enemy.damage * (self.enemy.level ** 1) + damage_randomness)
        return

    def die(self):  # this is for the player dying
        self.turn = None
        self.enemy.health = 0
        self.enemy.damage = 0
        print('You died!')
        t.sleep(2)
        clear()
        print(stylize(str(random.randint(3, 8)) + ' hours pass...', attr('bold')))
        t.sleep(2)
        print(stylize('Future Corp\'s prototype Revival-67TLA is installed in your system.', fg(14)))
        t.sleep(2)
        print('Using your possessions and materials to revive you.')
        t.sleep(2)
        for i in F7.consumable_list:
            consume_removal_chance = random.randint(1, 2)
            if consume_removal_chance == 1:
                F7.consumable_list.remove(i)
                print(i, 'removed.')
        t.sleep(2)
        print('')
        for i in F7.scrap_list:
            scrap_removal_chance = random.randint(1, 5)
            if scrap_removal_chance < 4:
                F7.scrap_list.remove(i)
                print(i, 'removed.')
        t.sleep(2)
        print('You will be brought back now. Thank you, F7.')
        F7.temphealth = F7.health
        t.sleep(2)
        travel.travel_menu()
        return

    def end_combat(self):  # this is for the enemy dying
        self.turn = None
        self.enemy.health = 0
        self.enemy.damage = 0
        xp_dict = {
            'Common': 1,
            'Uncommon': 1.3,
            'Rare': 2,
            'Special': 2.5,
            'God-Like': 3
        }

        xp_added = int(((200 + 300 * self.enemy.level ** 1.6) * (random.randint(73, 96)/100)) * xp_dict[self.enemy.rarity])

        print(xp_added, 'XP gained.')
        F7.addexp(xp_added)

        weapon_spawned = random.randint(1, 5)
        if weapon_spawned <= 4:
            t.sleep(2)
            x = random.randint(1, 100)

            # the rarer an enemy, the better the chance to drop a better item
            enemy_drop = {
                'Common': 0,
                'Uncommon': 7,
                'Rare': 15,
                'Special': 30,
                'God-Like': 65
            }

            x += enemy_drop[self.enemy.rarity]

            chance_dict = {
                'x <= 60': 'Common',
                '60 < x <= 81': 'Uncommon',
                '81 < x <= 93': 'Rare',
                '93 < x <= 99': 'Special',
                'x >= 100': 'God-like'
            }

            for key in chance_dict:
                check = eval(key)  # x gets used here
                if check:
                    weapon_dropped = copy.deepcopy(weapon_dict[chance_dict[key]][random.randint(0, len(weapon_dict[chance_dict[key]]) - 1)])
                    weapon_dropped.level = self.enemy.level + random.randint(-1, 1)
                    weapon_dropped.damage = int(weapon_dropped.damage * (weapon_dropped.level ** 2.3))
                    prefix_list = ['Accurate', 'Damaging', 'Fiery', 'Roguish', 'Betraying', 'Lazy']
                    prefix_added = random.randint(1, 25)
                    if prefix_added <= 2:
                        weapon_dropped.prefix = prefix_list[random.randint(0, 5)]
                    print('\nA weapon dropped!')
                    t.sleep(1)
                    print('')
                    weapon_dropped.showstats()
                    t.sleep(1)
                    print('\nWill you take the weapon? (y/n)')
                    take = input()
                    if take.lower() == 'y':
                        print('\nPick a weapon slot to put this in.')
                        print('a) Slot 1:', F7.weapon1.name)
                        print('b) Slot 2:', F7.weapon2.name)
                        print('c) Slot 3:', F7.weapon3.name)
                        print('d) Slot 4:', F7.weapon4.name)
                        print('e) Nevermind, Discard Weapon')

                        slot_input = input()

                        # dumb fix for equipping weapons bc dicts dont work properly
                        def swap1(weapon):
                            F7.weapon1 = weapon
                            return

                        def swap2(weapon):
                            F7.weapon2 = weapon
                            return

                        def swap3(weapon):
                            F7.weapon3 = weapon
                            return

                        def swap4(weapon):
                            F7.weapon4 = weapon
                            return

                        slot_dict = {
                            'a': swap1,
                            'b': swap2,
                            'c': swap3,
                            'd': swap4
                        }

                        if slot_input.lower() in slot_dict:
                            slot_dict[slot_input.lower()](weapon_dropped)
                            print(weapon_dropped.name, 'equipped. Exiting out of combat now.')
                            t.sleep(2)
                            travel.travel_menu()
                        elif slot_input.lower() == 'e':
                            print('Ok, weapon will be discarded. Exiting out of combat now.')
                            t.sleep(2)
                            travel.travel_menu()
                        else:
                            print('Not an option. Exiting out of combat now.')
                            t.sleep(2)
                            travel.travel_menu()
        t.sleep(2)
        travel.travel_menu()
        return

    def setturn(self):
        # turn either goes to enemy or F7, 50/50 chance
        turn_chooser = random.randint(1, 2)
        if turn_chooser == 1:
            self.turn = 'F7'
        else:
            self.turn = 'Enemy'
        return

    def check_dead(self):
        t.sleep(2)
        if self.turn == 'F7':
            if F7.temphealth <= 0:
                self.die()
            else:
                self.combatmenu()
        else:
            if self.enemy.health <= 0:
                self.end_combat()
            else:
                self.combatmenu()
        return

    def player_attack(self):
        print('You attack with', F7.weapon_equipped.name + '!')
        t.sleep(2)
        amount_hit = 0
        for i in range(F7.weapon_equipped.rof):
            if self.chip:
                hit = 100
                print('Your targeting chip aids you in your aim!')
                t.sleep(2)
            else:
                hit = random.randint(1, 100)
            if hit <= F7.weapon_equipped.hitrate:
                amount_hit += 1
        damage = int(amount_hit*(F7.weapon_equipped.damage*(random.randint(85, 125)/100)))
        if self.metal:
            multiplier = random.randint(16, 27)
            print('The metallic aura increases your damage by', str(multiplier) + '%')
            damage += damage * (multiplier/100)
            t.sleep(2)
        self.enemy.health -= damage
        if amount_hit == 0:
            print('You miss!')
            self.turn = 'Enemy'
            self.check_dead()
        if F7.weapon_equipped.weptype == 'Shotgun' or F7.weapon_equipped.weptype == 'Full-Auto Gun':
            # shotguns/full autos are treated differently
            rof_words = {
                'Shotgun': 'Pellets',
                'Full-Auto Gun': 'Bullets'
            }
            print(amount_hit, rof_words[F7.weapon_equipped.weptype], 'hit!')
            t.sleep(2)
            print(stylize(damage, fg(9)), 'damage dealt.')
            self.turn = 'Enemy'
            self.check_dead()
        else:
            print('You hit!')
            t.sleep(2)
            print(stylize(damage, fg(9)), 'damage dealt.')
            self.turn = 'Enemy'
            self.check_dead()
        return

    def enemy_attack(self):
        t.sleep(2)
        print(self.enemy.name, 'is going to attack!')
        t.sleep(2)
        hit = random.randint(1, 100)
        if self.smoke:
            smoked = random.randint(1, 10)
            print('The smokescreen is up!')
            if smoked <= 9:
                t.sleep(2)
                print('The smoke covers you, and the enemy can\'t attack!')
                hit = 101
                self.smoke = False
            else:
                print('The enemy can still get a hit on you!')
                hit = random.randint(50, 100)
                self.smoke = False
        if hit <= self.enemy.hitrate:
            damage = int(self.enemy.damage * (random.randint(85, 110) / 100))
            if self.player_shield_up:
                print('Your shield is up, blocking', str(F7.shield.resist) + '%', 'damage.')
                t.sleep(2)
                damage -= int(damage * (F7.shield.resist/100))
            F7.temphealth -= damage
            print(self.enemy.name, flavor_text[self.enemy.entype][random.randint(0, len(flavor_text[self.enemy.entype]) - 1)])
            t.sleep(1)
            print(stylize(str(damage), fg(9)), 'damage dealt!')
        else:
            print(self.enemy.name, flavor_text_miss[random.randint(0, len(flavor_text_miss) - 1)])
        t.sleep(2)
        self.turn = 'F7'
        self.check_dead()
        return

    def run(self):
        print('Are you sure you want to run? The enemy could get a shot at you! (y/n)')
        confirm = input()
        if confirm.lower() == 'y':
            self.turn = None
            self.enemy.health = 0
            self.enemy.damage = 0
            print('Running away...')
            t.sleep(2)
            shot = random.randint(1, 5)
            if shot <= 4:
                health_lost = F7.health * (random.randint(15, 22)/100)  # this way the player will be
                                                                        # penalized, but wont die from
                                                                        # running
                F7.temphealth -= int(health_lost)
                print(self.enemy.name, 'was able to attack you while you were running! You lost', int(health_lost), 'health.')
                t.sleep(2)
                travel.travel_menu()
            else:
                t.sleep(2)
                travel.travel_menu()
        elif confirm.lower() == 'n':
            print('Ok.')
            t.sleep(2)
            self.combatmenu()
        else:
            print('That\'s not an option, staying in position.')
            t.sleep(2)
            self.combatmenu()
        return

    # the functions for using the rest of the consumables
    def corrosive_grenade(self):
        F7.consumable_list.remove('Corrosion Grenade')
        print('You toss a corrosion grenade!')
        self.corrosive = True
        return

    def metallic_aura(self):
        F7.consumable_list.remove('Metallic Aura')
        print('You imbue your weapon with a metallic aura!')
        self.metal = True
        return

    def smokescreen(self):
        F7.consumable_list.remove('Smokescreen')
        print('You toss a smokescreen to cover you!')
        self.smoke = True
        return

    def targeting_chips(self):
        F7.consumable_list.remove('Targeting Chip')
        print('You install a short-term usage targeting chip!')
        self.chip = True
        return

    def flashbang(self):
        F7.consumable_list.remove('Flashbang')
        print('You toss a flashbang!')
        self.flash_countdown = 1
        return

    def consumable(self):  # selecting a consumable to use
        clear()
        print('Which consumable do you want to use?')
        for i in F7.consumable_list:
            print(i)
        print('')

        consumable_dict = {
            'Toolbox': toolbox,
            'Corrosive Grenade': self.corrosive_grenade,
            'Metallic Aura': self.metallic_aura,
            'Smokescreen': self.smokescreen,
            'Targeting Chip': self.targeting_chips,
            'Flashbang': self.flashbang
        }

        consume = input()
        if consume.title() in F7.consumable_list and consume.title() in consumable_dict and consume.title() != 'Toolbox':
            self.turn = 'Enemy'
            consumable_dict[consume.title()]()
            t.sleep(2)
            self.combatmenu()
        elif consume.title() in F7.consumable_list and consume.title() in consumable_dict and consume.title() == 'Toolbox':
            self.turn = 'Enemy'
            before_health = F7.temphealth
            toolbox()
            amount_restored = F7.temphealth - before_health
            print('Toolbox used.', stylize(amount_restored, fg(9)), 'health restored.')
            t.sleep(2)
            self.combatmenu()
        else:
            print('That\'s not an option.')
            t.sleep(2)
            self.combatmenu()
        return

    def wepswitch(self):
        clear()
        print('Select a weapon to equip.')
        print('a)', stylize(F7.weapon1.name, attr('bold')))
        if F7.weapon1 != no_weapon:
            print('')
            F7.weapon1.showstats()
            print('')
        print('b)', stylize(F7.weapon2.name, attr('bold')))
        if F7.weapon2 != no_weapon:
            print('')
            F7.weapon2.showstats()
            print('')
        print('c)', stylize(F7.weapon3.name, attr('bold')))
        if F7.weapon3 != no_weapon:
            print('')
            F7.weapon3.showstats()
            print('')
        print('d)', stylize(F7.weapon4.name, attr('bold')))
        if F7.weapon4 != no_weapon:
            print('')
            F7.weapon4.showstats()
            print('')
        print('e)', stylize('Nevermind', attr('bold')))
        weapon_wanted = input()

        weapon_equipping_dict = {
            'a': F7.weapon1,
            'b': F7.weapon2,
            'c': F7.weapon3,
            'd': F7.weapon4
        }

        if weapon_wanted.lower() in weapon_equipping_dict:
            F7.weapon_equipped = weapon_equipping_dict[weapon_wanted]
            print(weapon_equipping_dict[weapon_wanted].name, 'equipped.')
            self.turn = 'Enemy'
            self.countdown += 1
            t.sleep(2)
            self.combatmenu()
        elif weapon_wanted.lower() == 'e':
            print('Ok.')
            t.sleep(2)
            self.combatmenu()
        else:
            print('That\'s not an option.')
            t.sleep(2)
            self.combatmenu()
        return

    def shield(self):
        if self.shield_allowed and not self.player_shield_up:
            if F7.shield != no_shield:
                self.player_shield_up = True
                self.countdown = 0
                print(F7.shield.name, 'activated.')
                self.turn = 'Enemy'
                t.sleep(2)
                self.combatmenu()
            else:
                print('You have no shield!')
                t.sleep(2)
                combat.combatmenu()
        elif not self.shield_allowed:
            print('Your shield has no energy!')
            t.sleep(2)
            combat.combatmenu()
        elif self.player_shield_up:
            print('Your shield is already up!')
            t.sleep(2)
            combat.combatmenu()
        return

    def combatmenu(self):
        clear()
        print(stylize('Müller\'s Targeting Computer BETA 0.991', fg(10)))
        print(stylize('A 3rd party software created for F bots. Screw the Futurget.', fg(10)))
        print(stylize('\nNote for Dr. Müller: UPDATE THIS UI PLEASE!!!', fg(226)))
        print('-F7 and Charlie')
        if self.start:
            t.sleep(2)
        print(stylize('\nF7 Health:', attr('bold')),
              stylize(str(F7.temphealth), fg(9)), 'out of',
              stylize(str(F7.health), fg(9)), '(' + str(round((F7.temphealth/F7.health) * 100, 2)) + '%)')
        print(stylize('\nWeapon Equipped:', attr('bold')))
        # i cant use showstats because i dont want the description to be visible
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

        if F7.weapon_equipped.prefix != '':
            print(stylize('Level ' + str(F7.weapon_equipped.level) + ' ' +
                          stylize(F7.weapon_equipped.prefix, fg(prefix_color[F7.weapon_equipped.prefix])) + ' ' +
                          F7.weapon_equipped.name, attr('bold')))
        else:
            print('Level', F7.weapon_equipped.level, F7.weapon_equipped.name)
        print(stylize(F7.weapon_equipped.rarity, fg(rarity_color[F7.weapon_equipped.rarity])), F7.weapon_equipped.weptype)
        print(stylize('Damage:', attr('bold')), F7.weapon_equipped.damage)
        print(stylize('Accuracy:', attr('bold')), str(F7.weapon_equipped.hitrate) + '%')
        if F7.weapon_equipped.weptype == 'Shotgun' or F7.weapon_equipped.weptype == 'Full-Auto Gun':
            rof_dict = {
                'Shotgun': stylize('Pellets:', attr('bold')),
                'Full-Auto Gun': stylize('Rate of Fire:', attr('bold'))
            }

            print(rof_dict[F7.weapon_equipped.weptype], F7.weapon_equipped.rof)
        print(stylize('\nShield:', attr('bold')))
        F7.shield.showstats()
        print(stylize('\nEnemy:', attr('bold')))
        self.enemy.showstats()
        if self.start:
            t.sleep(2)
            self.start = False
        if self.turn == 'F7':
            print('\nF7\'s turn.')
            print(stylize('\nWhat would you like to do?', attr('bold')))
            print('a) Attack With', stylize(F7.weapon_equipped.name, attr('bold')))
            print('b) Use Consumable')
            print('c) Put Up Shield')
            print('d) Switch Weapon')
            print('e) Run Away')

            chosen = input()

            combat_options = {
                'a': self.player_attack,
                'b': self.consumable,
                'c': self.shield,
                'd': self.wepswitch,
                'e': self.run
            }
            if chosen in combat_options:
                if self.player_shield_up and self.countdown >= F7.shield.turns:
                    print('Shield ran out of power. Deactivating now.')
                    self.shield_allowed = False
                    self.player_shield_up = False
                    t.sleep(2)
                combat_options[chosen]()
            else:
                print('That\'s not an option.')
                t.sleep(2)
                self.combatmenu()
        elif self.turn == 'Enemy':
            print('\n' + self.enemy.name + '\'s turn.')
            if not 0 < self.flash_countdown < 3:
                if self.corrosive:
                    corrosion = self.enemy.health*(random.randint(2, 6)/100)
                    self.enemy.health -= corrosion
                    t.sleep(2)
                    print('The corrosion from your grenade damages the enemy!')
                    t.sleep(2)
                    print(corrosion, 'damage dealt.')
                    t.sleep(2)
                self.enemy_attack()
            else:
                self.flash_countdown += 1
                t.sleep(2)
                print('The enemy is blinded from your flashbang!')
                t.sleep(2)
                self.turn = 'F7'
                self.combatmenu()
        else:
            pass
        return

    def start_combat(self):
        chance = random.randint(1, 5)
        if chance <= 4:
            self.enemy_shield_up = False
            self.player_shield_up = False
            self.shield_allowed = True
            self.start = True
            self.corrosive = False
            self.flash_countdown = 0
            self.countdown = 0
            self.chip = False
            self.metal = False
            self.smoke = False
            self.spawn_enemy()
            self.setturn()
            self.combatmenu()
        else:
            print(stylize('Müller\'s Targeting Computer BETA 0.991', fg(10)))
            print(stylize('A 3rd party software created for F bots. Screw the Futurget.', fg(10)))
            print(stylize('\nNote for Dr. Müller: UPDATE THIS UI PLEASE!!!', fg(226)))
            print('-F7 and Charlie')
            t.sleep(2)
            print('\nNo enemies to fight here.')
            t.sleep(2)
            travel.travel_menu()

combat = Combat(current_level_name)
#combat.start_combat()

# the minigames
all_words = [
    'national', 'fountain', 'relation', 'original', 'treasurer',
    'sodium', 'defender', 'record', 'ignore', 'demonstrate',
    'comfort', 'understand', 'admire', 'manufacture', 'inhabitant',
    'horoscope', 'format', 'outfit', 'revolution', 'selection',
    'experiment', 'evaluate', 'active', 'ignite', 'delivery',
    'maximum', 'minimum', 'generate', 'manner', 'intermediate',
    'dismissal', 'experience', 'restrain', 'establish', 'retreat',
    'father', 'mother', 'family', 'detect', 'second',
    'temple', 'quantity', 'kinship', 'clique', 'depend',
    'welfare', 'discriminate', 'vision', 'rehearsal', 'factory',
    'reason', 'wonder', 'deviation', 'graphic', 'inside',
    'holiday', 'devote', 'thesis', 'conscious', 'sympathy',
    'moving', 'accident', 'misery', 'company', 'paralyze',
    'complicated', 'soldier', 'confront', 'certain', 'ambition',
    'discriminate', 'spirit', 'guarantee', 'silver', 'weapon',
    'harvest', 'imposter', 'thread', 'sunshine', 'trivial',
    'conglomerate', 'civilization', 'temperature', 'disagreement', 'considerations'
]

# this is used for the salvage game
small_words = [
    'key', 'pat', 'crime', 'zero', 'duck',
    'creep', 'rice', 'shape', 'attic', 'glory',
    'nerve', 'virus', 'lock', 'game', 'half',
    'rumor', 'price', 'angel', 'mist', 'debt',
    'lung', 'class', 'echo', 'sell', 'sense',
    'wheel', 'go', 'ridge', 'guilt', 'club'
]

# next 2 lists are just for style and stuff
random_characters = [
    '@', '#', '*', '&', ';',
    '{', '}', '/', '|', '<',
    '>', '?', '!', '=', '+'
]

alphabet = [
    'a', 'b', 'c', 'd', 'e',
    'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y',
    'z'
]


def scan():
    # type as many words as possible for shield
    displayed_words1 = []
    displayed_words2 = []
    scanned_words = 0
    print(stylize('DISBARON DRONE MARK XII', fg(14), attr('bold')))
    t.sleep(.5)
    print(stylize('Mode: Scanning & Research', fg(243)))
    print(stylize('Scanning Module: Gra-l23 v. 4.03 by Außerhalb', fg(240)))
    print(stylize('Language: English', fg(240)))
    t.sleep(.5)
    print(stylize('DRONE LICENSE EXPIRED (11/3/2109): RENEW AT NEAREST ACTICAP FACILITY', fg(1)))
    print('\n')
    located = random.randint(1, 10)
    t.sleep(1)
    if located >= 7:
        t.sleep(1)
        print(stylize('Items found. Requiring junk clearing.', attr('bold')))
        print('\n')
        t.sleep(1)

        for i in range(8):
            displayed_words1.append(all_words[random.randint(0, 84)])
            displayed_words2.append(all_words[random.randint(0, 84)])

        for i in range(8):
            random1 = random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)]
            random2 = random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)]
            random3 = random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)]
            random4 = random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)]

            alpha1 = alphabet[random.randint(0, 25)].upper() + alphabet[random.randint(0, 25)].upper() + alphabet[random.randint(0, 25)].upper()
            alpha2 = alphabet[random.randint(0, 25)].upper() + alphabet[random.randint(0, 25)].upper() + alphabet[random.randint(0, 25)].upper()
            alpha3 = alphabet[random.randint(0, 25)].upper() + alphabet[random.randint(0, 25)].upper() + alphabet[random.randint(0, 25)].upper()
            alpha4 = alphabet[random.randint(0, 25)].upper() + alphabet[random.randint(0, 25)].upper() + alphabet[random.randint(0, 25)].upper()

            print(random1 + alpha4 + displayed_words1[i].upper() + alpha1 + random2 + random3 + alpha2 + displayed_words2[i].upper() + alpha3 + random4)

        t.sleep(1)
        print('\nPrepare to clear junk and scan.')
        t.sleep(2)
        print('\nBegin with scanning process now. Ten seconds.')

        timer = t.time()
        while t.time() - timer < 10:
            print('gral.POSSIBLE_SCAN: ')
            scanned = input()
            if scanned.lower() in displayed_words1 or scanned.lower() in displayed_words2:
                print(stylize('Good scan.', fg(10)))
                scanned_words += 1
            else:
                print(stylize('Unsuccessful scan.', fg(1)))
        print('Scanning process stopping now.')
        t.sleep(2)
        print('gral.SCAN_SCORE:', scanned_words)
        xp_added = int(((int(200 + 300 * F7.level ** 1.6)) * (random.randint(27, 32) / 100)) * (scanned_words / 2))
        F7.addexp(xp_added)
        print(xp_added, 'XP gained.')
        if scanned_words <= 1:
            print('Insufficient amount of scanning. Nothing recieved.')
        else:
            print('Analyzing contents...')
            t.sleep(2)

            chance_dict = {
                2: 'Common',
                3: 'Uncommon',
                4: 'Rare',
                5: 'Astronomical',
                6: 'Holy'
            }

            if scanned_words in chance_dict:
                drop = copy.deepcopy(shield_dict[chance_dict[scanned_words]][random.randint(0, len(shield_dict[chance_dict[scanned_words]]) - 1)])
            else:
                drop = copy.deepcopy(shield_dict['Holy'])
            print(drop.name, 'dropped!')
            drop.showstats()
            print('Do you want to take it? (y/n)')
            confirm = input()
            if confirm.lower() == 'y':
                F7.shield = drop
                print(drop.name, 'equipped.')
                t.sleep(2)
                travel.travel_menu()
            elif confirm.lower() == 'n':
                print('Ok, leaving now.')
            else:
                print('That is not an option. Exiting now.')
                t.sleep(2)
                travel.travel_menu()
        t.sleep(3)
        travel.travel_menu()
    else:
        print(stylize('Nothing worth scanning here. Exiting now.', attr('bold')))
        t.sleep(2)
        travel.travel_menu()
        return


def hack():
    # unscramble a word for consumables
    print(stylize('DISBARON DRONE MARK XII', fg(14), attr('bold')))
    t.sleep(.5)
    print(stylize('Mode: Hacking', fg(243)))
    print(stylize('Hacking Module: Randamuwādo v. 7.00 by Kaisha', fg(240)))
    print(stylize('Language: English', fg(240)))
    t.sleep(.5)
    print(stylize('DRONE LICENSE EXPIRED (11/3/2109): RENEW AT NEAREST ACTICAP FACILITY', fg(1)))
    print('\n')
    located = random.randint(1, 10)
    t.sleep(1)
    if located >= 7:
        print(stylize('Container secure. Requiring password decryption.', attr('bold')))
        print('\n')
        t.sleep(1)

        word = all_words[random.randint(0, 84)]
        letters = []

        for i in word:
            letters.append(i)

        random.shuffle(letters)

        for i in letters:
            print(i.upper() + str(random.randint(0, 9)))

        tries = 3

        t.sleep(2)
        print('\nUnscramble the given letters. Begin now.')
        while tries > 0:
            print('ATTEMPT', str(tries) + ':', 'possible_password: ')
            guess = input()
            if guess.lower() == word:
                print(stylize('Correct password', fg(10)))
                t.sleep(1)
                print(stylize('Analyzing contents of the container...', fg(10)))
                t.sleep(1)
                loot = random.randint(0, 100) + len(guess.lower())*2
                if loot <= 66:
                    loot_common = common_consume[random.randint(0, 1)]
                    amount = random.randint(1, 4)
                    print(amount, loot_common, 'found.')
                    for i in range(amount):
                        F7.add_consumable(loot_common)
                elif 66 < loot <= 92:
                    loot_common = common_consume[random.randint(0, 1)]
                    loot_uncommon = uncommon_consume[random.randint(0, 1)]
                    amount_common = random.randint(1, 3)
                    amount_uncommon = random.randint(1, 3)
                    print(amount_common, loot_common, 'found.')
                    print(amount_uncommon, loot_uncommon, 'found.')
                    for i in range(amount_common):
                        F7.add_consumable(loot_common)
                    for i in range(amount_uncommon):
                        F7.add_consumable(loot_uncommon)
                else:
                    loot_common = common_consume[random.randint(0, 1)]
                    loot_uncommon = uncommon_consume[random.randint(0, 1)]
                    loot_rare = rare_consume[random.randint(0, 1)]
                    amount_uncommon = random.randint(1, 3)
                    amount_rare = random.randint(1, 2)
                    print(1, loot_common, 'found')
                    print(amount_uncommon, loot_uncommon, 'found.')
                    print(amount_rare, loot_rare, 'found.')
                    F7.add_consumable(loot_common)
                    for i in range(amount_uncommon):
                        F7.add_consumable(loot_uncommon)
                    for i in range(amount_rare):
                        F7.add_consumable(loot_rare)
                t.sleep(1)
                xp_added = int(((int(200 + 300 * F7.level ** 1.6)) * (random.randint(27, 32)/100)) * (len(guess)/3))
                F7.addexp(xp_added)
                print(xp_added, 'XP gained.')
                t.sleep(3)
                travel.travel_menu()
                break
            else:
                print(stylize('Invalid password', fg(1)))
                tries -= 1
        print('All password tries used. Unsuccessful hack. Exiting program.')
        t.sleep(3)
        travel.travel_menu()
    else:
        print(stylize('Container does not appear to have valuables. Exiting now.', attr('bold')))
        t.sleep(2)
        travel.travel_menu()
    return


def salvage():
    # try to remember a word for scrap
    print(stylize('DISBARON DRONE MARK XII', fg(14), attr('bold')))
    t.sleep(.5)
    print(stylize('Mode: Salvaging', fg(243)))
    print(stylize('Salvaging Module: Pengeboran v. 0.88 by Sangat Bagus', fg(240)))
    print(stylize('Language: English', fg(240)))
    t.sleep(.5)
    print(stylize('DRONE LICENSE EXPIRED (11/3/2109): RENEW AT NEAREST ACTICAP FACILITY', fg(1)))
    print('\n')
    located = random.randint(1, 10)
    t.sleep(1)
    if located <= 7:
        print(stylize('Scrap located. Requiring value evaluation.', attr('bold')))
        print(stylize('\nScrap will be displayed for one second. Please remember the list.', attr('bold')))
        print('\n')
        t.sleep(1)

        salvage_words = []
        displayed_words1 = []
        displayed_words2 = []

        for i in all_words:
            salvage_words.append(i)

        for i in small_words:
            salvage_words.append(i)

        for i in range(8):
            displayed_words1.append(salvage_words[random.randint(0, 114)])
            displayed_words2.append(salvage_words[random.randint(0, 114)])

        for i in range(8):
            random1 = random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)]
            random2 = random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)]
            random3 = random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)]
            random4 = random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)] + random_characters[random.randint(0, 14)]

            print(random1 + displayed_words1[i].upper() + random2 + random3 + displayed_words2[i].upper() + random4)

        t.sleep(2)
        clear()
        print('\nInput the longest scrap word recalled.')
        guess = input()
        t.sleep(1)

        if guess.lower() in displayed_words1 or guess.lower() in displayed_words2:
            if len(guess) > 5:
                print(stylize('Scrap value: peng.VALIDATED', fg(10)))
                t.sleep(1)
                print(stylize('Analyzing Scrap Yield...', fg(10)))
                t.sleep(1)
                loot = random.randint(0, 100)
                if loot <= 60:
                    loot_common = common_scrap[random.randint(0, len(common_scrap) - 1)]
                    amount = random.randint(1, 5)
                    print(amount, loot_common, 'found.')
                    for i in range(amount):
                        F7.add_scrap(loot_common)
                elif 60 < loot <= 90:
                    loot_common = common_scrap[random.randint(0, len(common_scrap) - 1)]
                    loot_uncommon = uncommon_scrap[random.randint(0, len(uncommon_scrap) - 1)]
                    amount_common = random.randint(1, 3)
                    amount_uncommon = random.randint(1, 3)
                    print(amount_common, loot_common, 'found.')
                    print(amount_uncommon, loot_uncommon, 'found.')
                    for i in range(amount_common):
                        F7.add_scrap(loot_common)
                    for i in range(amount_uncommon):
                        F7.add_scrap(loot_uncommon)
                else:
                    loot_common = common_scrap[random.randint(0, len(common_scrap) - 1)]
                    loot_uncommon = uncommon_scrap[random.randint(0, len(uncommon_scrap) - 1)]
                    loot_rare = rare_scrap[random.randint(0, len(rare_scrap) - 1)]
                    amount_common = random.randint(1, 2)
                    amount_uncommon = random.randint(1, 4)
                    print(amount_common, loot_common, 'found')
                    print(amount_uncommon, loot_uncommon, 'found.')
                    print(1, loot_rare, 'found.')
                    for i in range(amount_common):
                        F7.add_scrap(loot_common)
                    for i in range(amount_uncommon):
                        F7.add_scrap(loot_uncommon)
                    F7.add_scrap(loot_rare)
                t.sleep(1)
                xp_added = int(((int(200 + 300 * F7.level ** 1.6)) * (random.randint(27, 32) / 100)) * (len(guess) / 3))
                F7.addexp(xp_added)
                print(xp_added, 'XP gained.')
                t.sleep(3)
                travel.travel_menu()
            else:
                print(stylize('Scrap value: peng.INVALIDATED\nScrap too invaluable.', fg(1)))
                t.sleep(3)
                travel.travel_menu()
        else:
            print(stylize('Scrap value: peng.INVALIDATED\nScrap not found.', fg(1)))
            t.sleep(3)
            travel.travel_menu()
    else:
        print(stylize('No scrap located. Exiting now.', attr('bold')))
        t.sleep(2)
        travel.travel_menu()
    return


# travelling menu
class Travel:
    def __init__(self, level):
        self.level = level
        self.stop = False
        return

    def spawn(self, x, y):
        global current_level
        F7.x = x
        F7.y = y
        del current_level[y][x]
        current_level[y].insert(x, f)
        return

    def move(self, direction):
        global current_level  # excessive commenting bc this was hard for me to do
        global current_level_name
        oldy = F7.y  # saves current position
        oldx = F7.x

        move_dict = {
            'up': [0, -1],
            'down': [0, 1],
            'left': [-1, 0],
            'right': [1, 0]
        }

        # the big comments were my attempt at multi-region travel, which i had to scrap.
        '''
        switch_dict = {
            fp: ['plains', 29, 0, 1],
            pf: ['forest', 29, 19, 2],
            cf: ['forest', 29, 0, 3],
            fc: ['city', 29, 0, 4],
        }
        '''

        if current_level[F7.y + move_dict[direction][1]][F7.x + move_dict[direction][0]] not in collision:
            '''
            if current_level[F7.y + move_dict[direction][1]][F7.x + move_dict[direction][0]] in switch_dict:
                save_pos = current_level[F7.y + move_dict[direction][1]][F7.x + move_dict[direction][0]]
            '''
            F7.setpos(F7.x + move_dict[direction][0], F7.y + move_dict[direction][1])  # sets up F7's new position
            del current_level[oldy][oldx]  # gets rid of F7 in the current pos
            current_level[oldy].insert(oldx, level_dict[self.level][oldy][oldx])  # adds the old texture F7 was on
            del current_level[F7.y][F7.x]  # deletes the texture F7 will be on
            current_level[F7.y].insert(F7.x, f)  # adds F7 to new position
            '''
            try:
                if save_pos in switch_dict:
                    save_pos = pf
                    print(save_pos)
                    current_level = copy.deepcopy(level_dict[switch_dict[save_pos][0]])
                    current_level_name = switch_dict[save_pos][0]
                    self.spawn(switch_dict[save_pos][1], switch_dict[save_pos][2])
                    print(switch_dict[save_pos][3])
                    print('Moving to', level_names[switch_dict[save_pos][0]])
                    t.sleep(1)
            except UnboundLocalError:
                pass
            '''
        else:
            self.stop = True
        return

    def activate_movement(self):  # this is the actual UI for moving around
        clear()
        print(stylize('Future Corp. Satellite | Model XKU-9990', fg(14)))
        print(stylize('Location:', attr('bold')), stylize('#%&V;}!%@( ERROR ;}=@&!(/?{', fg(1)))
        print(stylize('Region:', attr('bold')), stylize(level_names[current_level_name], fg(10)))
        draw_level(current_level)
        print('▓ = 10x10 meters')

        print('Input up, down, left, or right. Input \"exit\" to exit.')
        move = input()

        move_list = ['up', 'down', 'left', 'right']

        if move.lower() in move_list:
            print('How many tiles do you want to move?')
            tiles = input()
            try:
                tiles = int(tiles)
                print('Moving.')
                for i in range(tiles):
                    if not self.stop:
                        self.move(move.lower())
                        clear()
                        print(stylize('Future Corp. Satellite | Model XKU-9990', fg(14)))
                        print(stylize('Location:', attr('bold')), stylize('#%&V;}!%@( ERROR ;}=@&!(/?{', fg(1)))
                        print(stylize('Region:', attr('bold')), stylize(level_names[current_level_name], fg(10)))
                        draw_level(current_level)
                        print('▓ = 10x10 meters')
                        t.sleep(.016)
                    else:
                        print('You can\'t go here!')
                        self.stop = False
                        break
                print('Movement finished.')
                t.sleep(1)
                self.activate_movement()
            except ValueError:
                print('That\'s not an option.')
                t.sleep(2)
                self.activate_movement()
        elif move.lower() == 'exit':
            print('Exiting now.')
            t.sleep(2)
            self.travel_menu()
        else:
            print('That\'s not an option.')
            t.sleep(2)
            self.activate_movement()
        return

    def save(self):  # love this feature, idk why. saves into a txt
        print('Saving...')
        t.sleep(2)
        '''
        Notes: I need to save:
        F7's position
        All of F7's stats
            Level
            Amount of xp
            Health
            Temporary Health
        Everything in F7's inventory
        Stats of the weapons
        '''
        info = [F7.x, F7.y, F7.level, F7.exp, F7.health, F7.temphealth, json.dumps(F7.weapon_equipped.__dict__),
                json.dumps(F7.weapon1.__dict__), json.dumps(F7.weapon2.__dict__), json.dumps(F7.weapon3.__dict__),
                json.dumps(F7.weapon4.__dict__), json.dumps(F7.shield.__dict__), json.dumps(F7.consumable_list),
                json.dumps(F7.scrap_list)]

        save_file = open('saves.txt', 'r+')
        save_file.seek(0, 0)

        save_file.write('saved')
        save_file.write('\n')
        for i in info:
            save_file.write(str(i))
            save_file.write('\n')

        save_file.close()

        print('Game saved.')
        t.sleep(2)
        self.travel_menu()
        return

    def exit_game(self):
        print('Are you sure you want to exit? Be sure to save first! (y/n)')
        exiting = input()
        if exiting.lower() == 'y':
            print('Closing...')
            t.sleep(2)
            sys.exit()
        elif exiting.lower() == 'n':
            print('Ok.')
            t.sleep(2)
            self.travel_menu()
        else:
            print('Not an option. Game will not close.')
            t.sleep(2)
            self.travel_menu()
        return

    def codex(self):  # these are tutorials
        print('Which category would you like?')
        print('a) Fighting')
        print('b) Consumables')
        print('c) Getting Items')
        print('d) Items')
        print('e) Traveling')
        chosen = input()

        def fighting():
            print('a) Attacking')
            print('b) Other Actions')
            print('c) Running From Battle')
            print('d) Turn-Based Combat')

            inside_dict = {
                'a': 'Attacking is the main part of combat. You do it, your enemies do it. Attack and defeat\nyour enemies before they can get you.',
                'b': 'You can do other things than attacking:\nUse a consumable\nPut up your shield\nSwitch your weapon\nRun from combat',
                'c': 'If you think you\'re in a bad situation, you can run from the battle. However, the\nenemy can still get some extra damage against you',
                'd': 'Combat goes in turns, you, then the enemy. Whoever goes first is randomly decided.\nThe combat ends when you run away, or when someone loses.'
            }

            choose = input()
            if choose in inside_dict:
                print(inside_dict[choose])
            return

        def consumables():
            print('a) Toolboxes')
            print('b) Flashbangs')
            print('c) Targeting Chips')
            print('d) Corrosion Grenades')
            print('e) Metallic Auras')
            print('f) Smokescreens')

            inside_dict = {
                'a': 'Toolboxes will heal you in and out of combat.',
                'b': 'Flashbangs will make the enemy stunned for two turns.',
                'c': 'Targeting Chips highly increase your range throughout the battle.',
                'd': 'Corrosion Grenades will slowly chip away enemy health.',
                'e': 'The Metallic Aura will increase the damage of you weapon during the battle',
                'f': 'Smokescreens will make you harder to hit, but will dissipate after a short time.'
            }

            choose = input()
            if choose in inside_dict:
                print(inside_dict[choose])
            return

        def getting_items():
            print('a) Salvaging')
            print('b) Scanning')
            print('c) Hacking')
            print('d) Weapon Drops From Combat')
            print('e) Crafting')

            inside_dict = {
                'a': 'Salvaging leads to obtaining scrap. To salvage, you will be required to try and\nremember the longest word in a list of words.',
                'b': 'Scanning leads to obtaining shields. To scan, you will be required to try and\nidentify as many words as possible in 10 seconds.',
                'c': 'Hacking leads to obtaining consumables. To hack, you will be required to try and\n unscramble a group of letters into a word.',
                'd': 'After combat, there\'s a chance for a weapon to drop. Rarer enemies drop rarer weapons.',
                'e': 'Crafting is another way to obtain most items, which utilizes scrap.'
            }

            choose = input()
            if choose in inside_dict:
                print(inside_dict[choose])
            return

        def items():
            print('a) Weapons')
            print('b) Shields')
            print('c) Consumables')
            print('d) Scrap')

            inside_dict = {
                'a': 'The world is home to many weapons, each with their own levels affecting damage\noutput. Some are also stylized with prefixes, but they don\'t seem to do anything...',
                'b': 'Shields will block a certain percent of damage when activated. They stay on for\na certain amount of turns, and once they end, they cannot be switched on again.',
                'c': 'Consumables will aid you during combat. See \"Consumables\" in the codex for more\n details.',
                'd': 'Scrap is used for crafting items and can be obtained from salvaging.'
            }

            choose = input()
            if choose in inside_dict:
                print(inside_dict[choose])
            return

        def traveling():
            print('a) Regions')
            print('b) Moving')

            inside_dict = {
                'a': 'Each region is inhabited by different enemies, and each region is harder than\nthe last. Be sure to level up before moving on!',
                'b': 'Movement is simple. Left, Right, Up, Down, and how many tiles you want to go.\nSome tiles have collision, and you will not be able to go through them.'
            }

            choose = input()
            if choose in inside_dict:
                print(inside_dict[choose])
            return

        codex_dict = {
            'a': fighting,
            'b': consumables,
            'c': getting_items,
            'd': items,
            'e': traveling
        }

        if chosen.lower() in codex_dict:
            clear()
            print('What do you want to read about?')
            codex_dict[chosen.lower()]()
            print('\nInput any key to exit.')
            exiting = input()
            if exiting:
                self.travel_menu()
        else:
            print('That\'s not an option.')
            print('')
            t.sleep(2)
            self.codex()
        return

    def craft(self):
        clear()
        print(stylize('FL89-P Crafting Module', fg(154), attr('bold')))
        print(stylize('By QWEGeo Inc.', fg(154)))
        print('\nWhat category would you like to see?')
        print('a) Scrap')
        print('b) Consumables')
        print('c) Shields')
        print('d) Weapons')
        print('e) Exit')
        chosen = input()

        crafting_dict = {
            'a': scrap_craft,
            'b': consume_craft,
            'c': shield_craft,
            'd': weapon_craft
        }

        if chosen.lower() in crafting_dict:
            clear()
            print('What would you like to craft? (Case-Sensitive Inputs!)')
            print('')
            dict_chosen = crafting_dict[chosen.lower()]
            if chosen.lower() == 'a' or chosen.lower() == 'b':
                for key, value in dict_chosen.items():
                    print(key + ':', value)
            elif chosen.lower() == 'c' or chosen.lower() == 'd':
                for key, value in dict_chosen.items():
                    print(key + ':', value[1])
            choose = input()

            if choose in dict_chosen:
                saved_scrap = copy.deepcopy(F7.scrap_list)
                if chosen.lower() == 'a' or chosen.lower() == 'b':
                    dict_chosen[choose].sort()
                elif chosen.lower() == 'c' or chosen.lower() == 'd':
                    dict_chosen[choose][1].sort()
                try:
                    if chosen.lower() == 'a' or chosen.lower() == 'b':
                        for i in dict_chosen[choose]:
                            F7.scrap_list.remove(i)
                    elif chosen.lower() == 'c' or chosen.lower() == 'd':
                        for i in dict_chosen[choose][1]:
                            F7.scrap_list.remove(i)

                    print('Crafting...')
                    t.sleep(2)
                    print('You crafted', choose)

                    def weapon_add():
                        # reused code from the weapons drop from combat
                        weapon_dropped = copy.deepcopy(weapon_craft[choose][0][0])
                        weapon_dropped.level = F7.level
                        weapon_dropped.damage = int(weapon_dropped.damage * (weapon_dropped.level ** 2.3))
                        print('\nPick a weapon slot to put this in.')
                        print('a) Slot 1:', F7.weapon1.name)
                        print('b) Slot 2:', F7.weapon2.name)
                        print('c) Slot 3:', F7.weapon3.name)
                        print('d) Slot 4:', F7.weapon4.name)
                        print('e) Nevermind, Discard Weapon')

                        slot_input = input()

                        # dumb fix for equipping weapons bc dicts dont work properly
                        def swap1(weapon):
                            F7.weapon1 = weapon
                            return

                        def swap2(weapon):
                            F7.weapon2 = weapon
                            return

                        def swap3(weapon):
                            F7.weapon3 = weapon
                            return

                        def swap4(weapon):
                            F7.weapon4 = weapon
                            return

                        slot_dict = {
                            'a': swap1,
                            'b': swap2,
                            'c': swap3,
                            'd': swap4
                        }

                        if slot_input.lower() in slot_dict:
                            slot_dict[slot_input.lower()](weapon_dropped)
                            print(weapon_dropped.name, 'equipped.')
                            t.sleep(2)
                            self.craft()
                        elif slot_input.lower() == 'e':
                            F7.scrap_list = copy.deepcopy(saved_scrap)
                            print('Ok, weapon discarded. Scrap returned.')
                            t.sleep(2)
                            self.craft()
                        else:
                            print('Not an option.')
                            t.sleep(2)
                            weapon_add()
                        return

                    def consume_add():
                        F7.add_consumable(choose)
                        print('Consumable added to your inventory.')
                        t.sleep(2)
                        self.craft()
                        return

                    def scrap_add():
                        F7.add_scrap(choose)
                        print('Scrap added to your inventory.')
                        t.sleep(2)
                        self.craft()
                        return

                    def shield_add():
                        shield_crafted = copy.deepcopy(shield_craft[choose][0][0])
                        print('Do you want to swap out your current shield for this shield? (y/n)')
                        decide = input()
                        if decide.lower() == 'y':
                            F7.shield = copy.deepcopy(shield_crafted)
                            print('Ok, replacing shields.')
                            t.sleep(2)
                            self.craft()
                        elif decide.lower() == 'n':
                            F7.scrap_list = copy.deepcopy(saved_scrap)
                            print('Ok, shield discarded. Scrap returned')
                            t.sleep(2)
                            self.craft()
                        else:
                            print('That\'s not an option.')
                            t.sleep(2)
                            shield_add()
                        return

                    adding_functions = {
                        'a': scrap_add,
                        'b': consume_add,
                        'c': shield_add,
                        'd': weapon_add
                    }

                    adding_functions[chosen.lower()]()

                except ValueError:
                    print('You don\'t have the required materials!')
                    F7.scrap_list = copy.deepcopy(saved_scrap)
                    t.sleep(2)
                    self.craft()
            else:
                print('That\'s not an option.')
                t.sleep(2)
                self.craft()
        elif chosen.lower() == 'e':
            print('Ok. Exiting now.')
            t.sleep(2)
            self.travel_menu()
        else:
            print('That\'s not an option.')
            t.sleep(2)
            self.craft()
        return

    def travel_menu(self):
        clear()
        print(stylize('Future Corp. Satellite | Model XKU-9990', fg(14)))
        print(stylize('Location:', attr('bold')), stylize('#%&V;}!%@( ERROR ;}=@&!(/?{', fg(1)))
        print(stylize('Region:', attr('bold')), stylize(level_names[current_level_name], fg(10)))
        draw_level(current_level)
        print('▓ = 10x10 meters')
        print(stylize('\n\nWhat would you like to do?', attr('bold')))
        print('a) Move')
        print('b) Check Inventory')
        print('c) Check Codex Tutorials')
        print('d) Fight')
        print('e) Salvage')
        print('f) Scan')
        print('g) Hack Container')
        print('h) Craft')
        print('i) Save Game')
        print('j) Exit Game')
        chosen = input()

        option_dict = {
            'a': self.activate_movement,
            'b': F7.showstats,
            'c': self.codex,
            'd': combat.start_combat,
            'e': salvage,
            'f': scan,
            'g': hack,
            'h': self.craft,
            'i': self.save,
            'j': self.exit_game
        }

        if chosen.lower() in option_dict:
            clear()
            option_dict[chosen]()
        else:
            print('That\'s not an option.')
            t.sleep(2)
            self.travel_menu()
        return


# main menu
while True:
    clear()
    print(
        stylize(
            '\n            oo++++++++++++++++++++++++++++++++sy`.s+++++++++++++++++++++++++++++o:'                  
            '\n            h.                              -s+.oo`                              /s:'                
            '\n            h.                            -s/.oo`                                  :s:'              
            '\n            h.                          -s/.o+`                                      :s:'            
            '\n            h.                        -s/.o+`                                          :s:'          
            '\n            h.      +++++++++++++++++s/.yh:------------------------------------`         /h'         
            '\n            h.      m                  `-------------------------------------:d`         y-'         
            '\n            h.      m                                                       `h.         o/'          
            '\n            h.      m                                                       h-         +o'           
            '\n            h.      m                                                      y:         :y'            
            '\n            h.      m                                                     s/         .h`'            
            '\n            h.      h+++++++++++++++o/                                   o+         `h`'             
            '\n            h.                      ++                                  /s          h.'              
            '\n            h.                      ++                                 :y          y:'               
            '\n            h.     oo+++++++++++++++o-                                -h          o/'                
            '\n            h.     y-                                                .h`         /o'                 
            '\n            h.     y-                                               `h.         :y'                  
            '\n            h.     y-                                               h.         .h`'                  
            '\n            h.     y-                                              y:         `h`'                   
            '\n            h.     y-                                             s/          h-'                    
            '\n            h.     y-                                            o+          y:'                     
            '\n            h.     y-                                           /s          o+'                      
            '\n            h-     y-                                          :y          /s'                       
            '\n          .s+      y-                                         -h          -y'                        
            '\n        `so`       y-                                        .h`         .h`'                        
            '\n       `d:         y-                                       `h`         `h`'                         
            '\n         /s-       y-                                      `h.          h.'                          
            '\n           /s-     y-                                      y-          y:'                           
            '\n             /s-   y-                                     s:          o+'                            
            '\n               /s- y-                                    o+          /s'                             
            '\n                 /sd-                                   /s          -y'                              
            '\n                   :`                                  .m+++++++++++h`', fg(50))
    )
    print('\na) New Game')
    print('\nb) Continue')
    print('\nc) Credits')
    print('\nd) Quit')

    menu_input = input('\n\nSelect an option: ')

    if menu_input == 'a':
        print('Starting...')
        t.sleep(2)
        file = open('saves.txt', 'r+')
        file.seek(0, 0)
        check = file.readline()
        if check == 'saved\n':
            print('You already have a saved game. Are you sure you want to start\na new game? Your save will be deleted! (y/n)')
            delete = input()
            if delete.lower() == 'y':
                file.truncate(0)
                file.close()
                t.sleep(3)
                clear()
                t.sleep(3)
                print('They\'ve got weapons. They\'ve got hordes. But you?\n No worries. You\'re fine. Welcome to',
                      stylize('Reliquiae', fg(50)) + '.')
                t.sleep(3)
                print('\nUnoptimized Games Presents')
                t.sleep(2)
                print('In Collaboration with No One\n')
                t.sleep(2)
                print(
                    stylize(
                        '\n            oo++++++++++++++++++++++++++++++++sy`.s+++++++++++++++++++++++++++++o:'
                        '\n            h.                              -s+.oo`                              /s:'
                        '\n            h.                            -s/.oo`                                  :s:'
                        '\n            h.                          -s/.o+`                                      :s:'
                        '\n            h.                        -s/.o+`                                          :s:'
                        '\n            h.      +++++++++++++++++s/.yh:------------------------------------`         /h'
                        '\n            h.      m                  `-------------------------------------:d`         y-'
                        '\n            h.      m                                                       `h.         o/'
                        '\n            h.      m                                                       h-         +o'
                        '\n            h.      m                                                      y:         :y'
                        '\n            h.      m                                                     s/         .h`'
                        '\n            h.      h+++++++++++++++o/                                   o+         `h`'
                        '\n            h.                      ++                                  /s          h.'
                        '\n            h.                      ++                                 :y          y:'
                        '\n            h.     oo+++++++++++++++o-                                -h          o/'
                        '\n            h.     y-                                                .h`         /o'
                        '\n            h.     y-                                               `h.         :y'
                        '\n            h.     y-                                               h.         .h`'
                        '\n            h.     y-                                              y:         `h`'
                        '\n            h.     y-                                             s/          h-'
                        '\n            h.     y-                                            o+          y:'
                        '\n            h.     y-                                           /s          o+'
                        '\n            h-     y-                                          :y          /s'
                        '\n          .s+      y-                                         -h          -y'
                        '\n        `so`       y-                                        .h`         .h`'
                        '\n       `d:         y-                                       `h`         `h`'
                        '\n         /s-       y-                                      `h.          h.'
                        '\n           /s-     y-                                      y-          y:'
                        '\n             /s-   y-                                     s:          o+'
                        '\n               /s- y-                                    o+          /s'
                        '\n                 /sd-                                   /s          -y'
                        '\n                   :`                                  .m+++++++++++h`', fg(50))
                )
                t.sleep(4)
                clear()
                # cutscene.intro()
                travel = Travel(current_level_name)
                travel.spawn(19, 8)
                travel.travel_menu()
                break
            else:
                file.close()
                print('Ok.')
                t.sleep(2)
        else:
            t.sleep(3)
            clear()
            t.sleep(3)
            print('They\'ve got weapons. They\'ve got hordes. But you?\n No worries. You\'re fine. Welcome to',
                  stylize('Reliquiae', fg(50)) + '.')
            t.sleep(3)
            print('\nUnoptimized Games Presents')
            t.sleep(2)
            print('In Collaboration with No One\n')
            t.sleep(2)
            print(
                stylize(
                    '\n            oo++++++++++++++++++++++++++++++++sy`.s+++++++++++++++++++++++++++++o:'
                    '\n            h.                              -s+.oo`                              /s:'
                    '\n            h.                            -s/.oo`                                  :s:'
                    '\n            h.                          -s/.o+`                                      :s:'
                    '\n            h.                        -s/.o+`                                          :s:'
                    '\n            h.      +++++++++++++++++s/.yh:------------------------------------`         /h'
                    '\n            h.      m                  `-------------------------------------:d`         y-'
                    '\n            h.      m                                                       `h.         o/'
                    '\n            h.      m                                                       h-         +o'
                    '\n            h.      m                                                      y:         :y'
                    '\n            h.      m                                                     s/         .h`'
                    '\n            h.      h+++++++++++++++o/                                   o+         `h`'
                    '\n            h.                      ++                                  /s          h.'
                    '\n            h.                      ++                                 :y          y:'
                    '\n            h.     oo+++++++++++++++o-                                -h          o/'
                    '\n            h.     y-                                                .h`         /o'
                    '\n            h.     y-                                               `h.         :y'
                    '\n            h.     y-                                               h.         .h`'
                    '\n            h.     y-                                              y:         `h`'
                    '\n            h.     y-                                             s/          h-'
                    '\n            h.     y-                                            o+          y:'
                    '\n            h.     y-                                           /s          o+'
                    '\n            h-     y-                                          :y          /s'
                    '\n          .s+      y-                                         -h          -y'
                    '\n        `so`       y-                                        .h`         .h`'
                    '\n       `d:         y-                                       `h`         `h`'
                    '\n         /s-       y-                                      `h.          h.'
                    '\n           /s-     y-                                      y-          y:'
                    '\n             /s-   y-                                     s:          o+'
                    '\n               /s- y-                                    o+          /s'
                    '\n                 /sd-                                   /s          -y'
                    '\n                   :`                                  .m+++++++++++h`', fg(50))
            )
            t.sleep(4)
            clear()
            # cutscene.intro()
            travel = Travel(current_level_name)
            travel.spawn(19, 8)
            travel.travel_menu()
            break
    elif menu_input == 'b':
        file = open('saves.txt', 'r+')
        file.seek(0, 0)
        check = file.readline()
        if check == 'saved\n':
            print('Loading your last save...')
            t.sleep(2)
            try:
                file.seek(0, 1)
                F7.x = int(file.readline())
                F7.y = int(file.readline())
                F7.level = int(file.readline())
                F7.exp = int(file.readline())
                F7.health = int(file.readline())
                F7.temphealth = int(file.readline())
                equipped = dict(json.loads(file.readline()))
                weapon1 = dict(json.loads(file.readline()))
                weapon2 = dict(json.loads(file.readline()))
                weapon3 = dict(json.loads(file.readline()))
                weapon4 = dict(json.loads(file.readline()))
                shield = dict(json.loads(file.readline()))
                F7.consumable_list = list(json.loads(file.readline()))
                F7.scrap_list = list(json.loads(file.readline()))

                weapons_to_convert = {
                    0: [equipped, F7.weapon_equipped],
                    1: [weapon1, F7.weapon1],
                    2: [weapon2, F7.weapon2],
                    3: [weapon3, F7.weapon3],
                    4: [weapon4, F7.weapon4]
                }

                for i in range(5):
                    weapons_to_convert[i][1].name = weapons_to_convert[i][0]['name']
                    weapons_to_convert[i][1].damage = weapons_to_convert[i][0]['damage']
                    weapons_to_convert[i][1].rarity = weapons_to_convert[i][0]['rarity']
                    weapons_to_convert[i][1].level = weapons_to_convert[i][0]['level']
                    weapons_to_convert[i][1].hitrate = weapons_to_convert[i][0]['hitrate']
                    weapons_to_convert[i][1].description = weapons_to_convert[i][0]['description']
                    weapons_to_convert[i][1].prefix = weapons_to_convert[i][0]['prefix']
                    weapons_to_convert[i][1].weptype = weapons_to_convert[i][0]['weptype']
                    weapons_to_convert[i][1].rof = weapons_to_convert[i][0]['rof']

                F7.shield.name = shield['name']
                F7.shield.resist = shield['resist']
                F7.shield.turns = shield['turns']
                F7.shield.rarity = shield['rarity']

                print('Game Loaded.')
                t.sleep(2)
                file.close()
                travel = Travel(current_level_name)
                travel.spawn(F7.x, F7.y)
                travel.travel_menu()
                break
            except IOError:
                print('There was an issue with loading your game. The file might be corrupted.')
                t.sleep(2)
        else:
            print('There is no saved game.')
            t.sleep(2)
    elif menu_input == 'c':
        print(stylize('Literally everything was by me. Music, story, gameplay, all me. \nMatthieu De Robles', attr('bold')))
        print('(let\'s thank nirjhor nath and dashiell elliott for testing tho)')
        print('(also nirjhor and dashiell are just programming gods in the ap compsci class)')
        t.sleep(10)
    elif menu_input == 'd':
        quit_input = input('Are you sure you want to quit? (y/n) ')
        if quit_input.lower() == 'y':
            sys.exit()
            break
        elif quit_input.lower() == 'n':
            print('\nOk.')
            t.sleep(2)
        else:
            print('Not an option. Game will not quit.')
            t.sleep(2)
    else:
        print('This is not an option.')
        t.sleep(2)
