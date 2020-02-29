from Classes.game import Person, bcolors
from Classes.magic import Spell
from Classes.Inventory import Item
import random


#Create Black Magic
fire = Spell('Fire', 25, 100, 'black')
thunder = Spell('Thunder', 25, 100, 'black')
meteor = Spell('Meteor', 25, 100, 'black')
blizzard = Spell('Blizzard', 40, 100, 'black')
quake = Spell('Quake', 18, 100, 'black')

#Create White Magic
cure = Spell ('Cure', 25, 620, 'white')
cura = Spell ('Cura', 32, 1500, 'white')

#Create some items
potion = Item('Potion', 'potion', 'Heals 50 HP', 50)
hipotion = Item('Hi-Potion', 'potion', 'Heals 100 HP', 100)
superpotion = Item('Super-Potion', 'potion', 'Heals 500 HP', 500)
elixer = Item('Elixer', 'elixer', 'Fully restores HP/MP of one party member', 9990)
hielixer = Item('Megaelixer', 'elixer', "Fully restores party's HP/MP", 9990)

grenade = Item('Grenade', 'attack', 'Deals 300 damage', 300)

player_spells = [fire, thunder, meteor, blizzard, quake,  cure, cura]
enemy_spells = [fire, meteor, cure]
player_item = [{'item': potion, 'quantity': 15}, {'item': hipotion, 'quantity': 5},
               {'item': superpotion, 'quantity': 5}, {'item': elixer, 'quantity': 5},
               {'item': hielixer, 'quantity': 5}, {'item': potion, 'quantity': 2},
               {'item': grenade, 'quantity': 5}]

#Instatiate people
player1 = Person('Valos:', 9390, 125, 125, 34, player_spells, player_item)
player2 = Person('Nick :', 9480, 475, 150, 34, player_spells, player_item)
player3 = Person('Robot:', 8460, 485, 175, 34, player_spells, player_item)
enemy1 = Person ('Imp  ', 1200, 130, 560, 35, enemy_spells, [])
enemy2 = Person ('Magos', 1200, 765, 525, 25, enemy_spells, [])
enemy3 = Person ('Imp  ', 1200, 130, 560, 35, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]


running = True
i=0

print(bcolors.FAIL + bcolors.BOLD+ "AN ENEMY ATTACKS!" + bcolors.ENDC)

#Print player and enemy stats
print('====================')
print('\n')
print('NAME                           HP                           MP')
for player in players:
    player.get_player_stats()
for enemy in enemies:
    enemy.get_enemy_stats()

while running:
    #Choose Player action
    for player in players:
        player.choose_action()
        choice = input('    Choose action: ')
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print ('\n' +'You attacked ' + enemies[enemy].name +  'for', dmg, 'points of damage.')

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(' ', '') + ' has died.')
                del enemies[enemy]

            player.get_stats(players, enemies)

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input('    Choose Magic: ')) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_spell_damage()

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + '\nNot enough MP\n' + bcolors.ENDC)
                continue

            player1.reduce_mp(spell.cost)

            if spell.type =='white':
                player.heal(magic_dmg)
                print (bcolors.OKBLUE + '\n' + spell.name + ' heals for', str(magic_dmg), 'HP.' + bcolors.ENDC)
            elif spell.type == 'black':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print (bcolors.OKBLUE + '\n' + spell.name + ' deals', str(magic_dmg), 'points of damage to ' + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(' ','') + ' has died.')
                    del enemies[enemy]
                    print ('You chose', spell.name, ', damage is', magic_dmg)

            player.get_stats(players, enemies)

        elif index == 2:
            player.choose_item()
            item_choice = int(input('    Choose item: ')) - 1
            if item_choice == -1:
                continue

            item = player_item[item_choice]['item']

            if player_item[item_choice]['quantity'] ==0:
                print (bcolors.FAIL + '\n' +'None left.....' + bcolors.ENDC)
                continue
            player_item[item_choice]['quantity'] -= 1

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name + ' heals for', str(item.prop), 'HP' + bcolors.ENDC)
            elif item.type == 'elixer':
                if item.name == 'Megaelixer':
                    for player_ in players:
                        player_.hp = player_.maxhp
                        player_.mp = player_.maxmp
                    print(bcolors.OKGREEN + '\n' + item.name + ' fully restores HP/MP for all members' + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print (bcolors.OKGREEN + '\n' + item.name + ' fully restores HP/MP' + bcolors.ENDC)
            elif item.type == 'attack':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(dmg)
                print(bcolors.FAIL + '\n' + item.name + 'deals', str(item.prop), 'points of damage to ' + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(' ','') + ' has died.')
                    del enemies[enemy]

                player.get_stats(players, enemies)
    #check if battle is over
    print ('=======================')
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp()==0:
            defeated_enemies+=1
    for player in players:
        if player.get_hp() ==0:
            defeated_players +=1

    #Check if Player won
    if defeated_enemies==3:
        print(bcolors.OKGREEN, 'You won', bcolors.ENDC)
        running=False

    #Check if Enemy won
    elif defeated_players ==3:
        print(bcolors.FAIL, 'Your enemies have defeated you',  bcolors.ENDC)
        running=False

    #Enemy attack phase
    for enemy in enemies:
        enemy_choice= random.randrange(2)
        print(enemy_choice)
        if enemy_choice ==0:
            target = random.randrange(3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(bcolors.OKBLUE + '\n' + enemy.name.replace(' ', '') + ' attacks ' + players[target].name.replace(' ','') + ' for', enemy_dmg, 'points of damage.' + bcolors.ENDC)

        elif enemy_choice ==1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            if spell:
                enemy.reduce_mp(spell.cost)

            if spell.type =='white':
                enemy.heal(magic_dmg)
                print (bcolors.OKBLUE + '\n' + spell.name + ' heals ' + enemy.name + ' for', str(magic_dmg), 'HP.' + bcolors.ENDC)
            elif spell.type == 'black':
                target = random.randrange(3)
                players[target].take_damage(magic_dmg)
                print (bcolors.OKBLUE + '\n' + enemy.name.replace(' ','') + "'s " + spell.name + ' deals', str(magic_dmg), 'points of damage to ' + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print (players[target].name.replace(' ','') + 'has died')
                    del players[target]
