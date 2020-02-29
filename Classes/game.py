import random
import math


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, name, hp, mp, atk, df, magic, item):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atk = atk
        self.df = df
        self.magic = magic
        self.item = item
        self.actions = ['Attack', 'Magic', 'Item']
        self.name = name

    def generate_damage(self):
        atkl = self.atk - 10
        atkh = self.atk + 10
        return random.randrange(atkl, atkh)

    '''def generate_spell_damage(self, i):
        mgl = self.magic[i]['dmg']-5
        mgh = self.magic[i]['dmg']+5
        return random.randrange(mgl, mgh)'''

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -=cost

    def get_spell_name(self, i):
        return self.magic[i]['name']

    def get_spell_mp_cost(self, i):
        return self.magic[i]['cost']

    def choose_action(self):
        i=1
        print('\n' +'    ' + bcolors.BOLD + self.name + bcolors.ENDC)
        (bcolors.OKBLUE + bcolors.BOLD + 'ACTIONS' + bcolors.ENDC)
        for item in self.actions:
            print('        ' + str(i) + '.', item)
            i+=1

    def choose_magic(self):
        i = 1
        print ('\n' + bcolors.OKBLUE + bcolors.BOLD + '    MAGIC' + bcolors.ENDC)
        for spell in self.magic:
            print('        ' + str(i) + '.', str(spell.name), '(cost:', str(spell.cost) + ')')
            i+=1

    def choose_item(self):
        i = 1
        print ('\n' + bcolors.OKGREEN + bcolors.BOLD +'    ITEMS' + bcolors.ENDC)
        for item in self.item:
            print('        ' + str(i) + '.', item['item'].name + ':', item['item'].description, '(x' + str(item['quantity']) + ')')
            i+=1

    def choose_target(self, enemies):
        i = 1
        print('\n' + bcolors.FAIL + bcolors.BOLD + '    TARGET' + bcolors.ENDC)
        for enemy in enemies:
            print ('        ' + str(i) + '.', enemy.name)
            i+=1
        choice = int(input('    Choose target: ')) - 1
        return choice

    def get_stats(self, players, enemies):
        for player in players:
            player.get_player_stats()
        for enemy in enemies:
            enemy.get_enemy_stats()

    def get_enemy_stats(self):
        hp_bar_tick = math.floor((self.hp / self.maxhp) * 50)
        #mp_bar_tick = math.floor((self.mp / self.maxmp) * 10)
        hp_print_grid = (len(str(self.maxhp)) - len(str(self.hp)))
        #mp_print_grid = (len(str(self.maxmp)) - len(str(self.mp)))

        print('                          --------------------------------------------------')
        print(
            bcolors.BOLD + self.name + '      ' + str(' ' * hp_print_grid) + str(self.hp) + '/' + str(self.maxhp) + '   |'
            + bcolors.FAIL + str('█' * hp_bar_tick) + str(
                ' ' * (50 - hp_bar_tick)) + bcolors.ENDC + bcolors.BOLD + '|'+bcolors.ENDC)

    def get_player_stats(self):
        #hp_bar
        hp_bar_tick = math.floor((self.hp /self.maxhp) * 25)
        mp_bar_tick = math.floor((self.mp / self.maxmp) * 10)
        hp_print_grid = (len(str(self.maxhp)) - len(str(self.hp)))
        mp_print_grid = (len(str(self.maxmp)) - len(str(self.mp)))

        print('                          -------------------------         ---------')
        print(bcolors.BOLD + self.name + '      ' +  str(' ' * hp_print_grid) + str(self.hp) + '/' + str(self.maxhp) +'    |'
            + bcolors.OKGREEN + str('█' * hp_bar_tick) + str(' '*(25-hp_bar_tick)) + bcolors.ENDC + bcolors.BOLD + '|'
            +str(' ' * mp_print_grid) + str(self.mp) +  '/' +str(self.maxmp) + '|' + bcolors.OKBLUE +  str('█' * mp_bar_tick) + str(' ' * (10-mp_bar_tick)) + bcolors.ENDC + '|')

    def choose_enemy_spell(self):
        magic_choice = random.randrange(len(self.magic))
        print ('magic choice is: ', magic_choice)
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_spell_damage()


        pct_hp = (self.hp / self.maxhp) * 100

        #recursion if magic point is insufficient or if pct_hp is greater than 50
        if self.mp < spell.cost or spell.type == 'white' and pct_hp > 50:
            spell, magic_dmg = self.choose_enemy_spell()
            return spell, magic_dmg
        else:
            return spell, magic_dmg


