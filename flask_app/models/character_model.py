from types import NoneType
from flask_app.models import location_model, item_model
import math
import random
import time

class Being:
    def __init__(self, name, health, attack=0, AC=0):
        self.name = name
        self.health = health
        self.attack = attack
        self.AC = AC



class Character(Being):
    fist = item_model.Weapon(0, "fist", "Your closed fist. You're so strong!", 1, 0)

    def __init__(self, name, position, health):
        super().__init__(name, health, attack = 0, AC = 10)
        self.position = position
        self.inventory = []
        self.leftHand = self.fist
        self.rightHand = self.fist
        self.in_combat = False

    def attack_damage(self):
        return self.leftHand.attack + self.rightHand.attack

    def defense(self):
        return self.AC

    def take(self, item):
        self.inventory.append(item)
        return item

    def list_inventory(self):
        print("You have the following items in your inventory:")
        print()
        for item in self.inventory:
            print(f"{item.name}")

    def use_from_inventory(self, item):
        if item not in self.inventory:
            # no clue why this method works, but I guess it does.
            for x in self.inventory:
                if item == x.name:
                    return x
            if item == self.leftHand:
                return self.leftHand
            if item == self.rightHand:
                return self.rightHand
        else:
            print(f"{item} not found in your inventory.")
            print()

    def use_item(self, item):
        self.inventory.pop(item)
        print(f"")

    def equip(self, item):
        if hasattr(item, "attack") == False: #yo this is neat
            print(f"You can only 'equip' weapons and shields, and {item.name} is neither of those. Try 'wear' to put on armor, and 'use' or 'drink' for any other items you may find.")
            print()
            time.sleep(0.3)
            return
        else:
            hand = input("Equip to which hand?\n").lower()
            orig_attack = self.attack_damage()
            if hand == "left" or hand == "right":
                if item in self.inventory:
                    self.inventory.remove(item)
                if hand == "left":
                    if self.leftHand != self.fist:
                        self.inventory.append(self.rightHand)
                    self.leftHand = item
                if hand == "right":
                    if self.rightHand != self.fist:
                        self.inventory.append(self.rightHand)
                    self.rightHand = item
            else:
                print(f"`{hand}` isn't a hand you can equip to. Please choose left or right.")
                print()
                return
            if orig_attack != self.attack_damage():
                print(f"Your original attack damage was {orig_attack}, and after equipping the {item.name} it is now {self.attack_damage()}.")
            print()
            print(f"You equip the {item.name}.")
            print()
            time.sleep(0.5)

    def wear(self, item):
        if hasattr(item, "defense") == True:
            orig_def = self.defense()
            if item in self.inventory:
                self.inventory.remove(item)
            self.AC += item.defense
            print()
            print(f"You equip the {item.name}.")
            time.sleep(0.5)
            print()
            print(f"Your original defense rating was {orig_def}, and after wearing the {item.name} it is now {self.defense()}.")
            time.sleep(0.5)
        else:
            print("You can't wear that!")
            time.sleep(0.5)
            return

    def heal(self, item):
        if self.health >= 100:
            print("Your health is already full - you can't drink any potions or you'd probably be sick.")
            return
        else:
            if item in self.inventory:
                healing = random.randint(16, 41)
                self.inventory.remove(item)
                self.health += healing + 30
                print("You drink a health potion, immediately feeling reinvigorated.")
                print()
                time.sleep(0.5)
                if self.health > 100:
                    self.health = 100
                    print(f"Your new health amount is {self.health}")
                    print()
                    time.sleep(0.3)
                    return
                print(f"Your new health amount is {self.health}")
                print()
                time.sleep(0.3)
                return

    def strength_pot(self, item):
        pass

    def defense_pot(self, item):
        pass

    def swing(self, enemy):
        roll_to_hit = random.randint(1, 21) #possibly add toHit bonuses#
        if roll_to_hit == 20:
            damage = random.randint(1, self.attack_damage()+1)
            damage = damage * 2
            enemy.health -= damage
            print(f"You deal a CRITICAL {damage} points of damage to the {enemy.name}!")
            print()
            time.sleep(0.5)
            return
        if roll_to_hit > enemy.AC:
            damage = random.randint(1, self.attack_damage()+1)
            enemy.health -= damage
            print(f"The attack hits! You deal {damage} points of damage to the {enemy.name}!")
            print()
            time.sleep(0.5)
            return
        else:
            print(f"You attack the {enemy.name}, but alas, the attacked missed!")
            print()
            time.sleep(0.5)
            return

    def smash(self, enemy):
        roll_to_hit = random.randint(10, 21) #possibly add toHit bonuses#
        if roll_to_hit == 20:
            damage = random.randint(5, self.attack_damage()+1)
            damage = (damage * 2) + 10
            enemy.health -= damage
            print(f"You absolutely SMASH the chair into the {enemy.name}, sending splinters flying everywhere, and dealing a CRITICAL {damage} points of damage!")
            print()
            time.sleep(0.5)
            return
        if roll_to_hit > enemy.AC:
            damage = random.randint(1, self.attack_damage()+1)
            enemy.health -= damage
            print(f"The chair connects with the {enemy.name} clear in the face! You dealt {damage} points of damage!")
            print()
            time.sleep(0.5)
            return
        else:
            print(f"You throw the chair at the {enemy.name}, but it deftly dodged out of the way!")
            print()
            time.sleep(0.5)
            return
        
    def kill(self, enemy):
        enemy.health = 0
        return

class Enemy(Being):
    def __init__(self, name, health, attack, AC):
        super().__init__(name, health, attack=0, AC=0)
        self.name = name
        self.health = health
        self.attack = attack
        self.AC = AC

    def enemy_attack(self, player):
        roll_to_hit = random.randint(1, 21) #possibly add toHit bonuses#
        if roll_to_hit == 20:
            damage = random.randint(1, self.attack+1)
            damage = damage * 2
            player.health -= damage
            print(f"{self.name} deals a CRITICAL {damage} points of damage to you!")
            return
        if roll_to_hit > player.AC:
            damage = random.randint(1, self.attack+1)
            player.health -= damage
            print(f"{self.name} attacks you for {damage} points of damage!")
            return
        else:
            print(f"{self.name} attacks you, but the attack misses!")
            return

# player1 = Character("Jeff", 1, 100)
# player1.attack()