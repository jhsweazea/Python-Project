from flask import Flask
from flask_app.models import location_model, character_model, item_model
import time, random
import os

things = {
    "key": item_model.Item(1, "key", "The wraught iron key looks brittle and rife with rust. It's likely going to break soon..."),
    "sword": item_model.Weapon(2, "sword", "The blade is covered with rust and nicked along the edge, but it looks serviceable enough. ATK: 6", 6, 0),
    "knife": item_model.Weapon(3, "knife", "The kitchen knife has definitely seen better days, but it still has a fine edge. ATK: 4", 4, 0), 
    "longsword": item_model.Weapon(4, "longsword", "While the craftsmanship isn't anything to write home about, the balance of the blade cannot be questioned. ATK: 8", 8, 0), 
    "pike": item_model.Weapon(5, "pike", "The pike might look plain, but it's blade is sharp and it's reach could be useful. ATK: 10", 10, 0),
    "battleaxe": item_model.Weapon(6, "battleaxe", "The weight of the axe alone speaks for itself. ATK: 12", 12, 0),
    "health": item_model.Item(7, "health potion", "The small, thin vial fits inside the palm of your hand. A feint red emenation is pulsing from within."),
    "strength": item_model.Item(8, "strength potion", "This cubic bottle is small; you can almost close your fist around it. It contains a cloudy blue liquid with what seems to be floating crystals swirling inside of it."),
    "defense": item_model.Item(9, "defense potion", "The glass flask is thin and almost fills your entire palm. It's purple liquid shimmers with a refracted light source that doesn't exist."),
    "shield": item_model.Weapon(10, "shield", "The lard wooden shield, although decorative, was definitely made to be used. DEF: 2",0, 2),
    "breastplate": item_model.Equipment(11, "breastplate", "The breastplate has seen better days, but its been maintained and remains functional. DEF: 5", 5),
    "helmet": item_model.Equipment(12, "helmet", "While it may not be the most stylish, it shows proof that it works. DEF: 2", 2),
    "boots": item_model.Equipment(13, "boots", "The boots are made of steel, rising up and above the knee with a flexible ankle for fluid movement. DEF: 2", 2),
    "gauntlets": item_model.Equipment(14, "gauntlets", "The gloves, while simplistic in their aesthetic, have a rather intricate design around the fingers and wrist, giving the wearer the freedom of movement required in combat. DEF: 2", 2),
    "dagger": item_model.Weapon(15, "dagger", "The blade of the dagger is almost prismatic to the eye. The hilt is ornate, and has a red jewel at the top of the handle near the blade. The dagger seems to emit a faint hum. It seems to be very powerful, but you feel a sense of recklessness when you hold it. ATK: 16, DEF: -5", 16, -5),
    "": item_model.Equipment(999, "", "this is nothing")
}

monsters = {
    "skeleton": character_model.Enemy("skeleton", 30, 6, 10),
    "skeleton2": character_model.Enemy("skeleton", 30, 6, 10),
    "skeleton3": character_model.Enemy("skeleton", 30, 6, 10),
    "skeleton4": character_model.Enemy("skeleton", 30, 6, 10),
    "gargoyle": character_model.Enemy("gargoyle", 25, 8, 12),
    "gargoyle2": character_model.Enemy("gargoyle", 25, 8, 12),
    "cultist": character_model.Enemy("cultist", 25, 10, 8),
    "cultist2": character_model.Enemy("cultist", 25, 10, 8),
    "cultist3": character_model.Enemy("cultist", 25, 10, 8),
    "wizard who smells quite bad": character_model.Enemy("wizard who smells quite bad", 20, 15, 8),
    "Grand Python Beast Pythulhu": character_model.Enemy("Grand Python Beast Pythulhu", 150, 15, 14), 
    "giant rat": character_model.Enemy("Rodent of Unusual Size", 25, 10, 12),
    "giant rat2": character_model.Enemy("Rodent of Unusual Size", 25, 10, 12)
}

locations= {
    "room1" : location_model.Location(1, "You awake in a cell with cold, stone walls and a lit torch in the sconce. You have no recollection of how you got here.",  "You look around in the room. Apart from the rusted sword and stone brick walls, there isn't much of interest to see. Looking around the stone room, you walk to the cell door and peer into a dark, deserted hallway. There's a faint glimmer to your right, and there you see a keyring hanging by the door with a single iron key attached to it.", "You re-enter the cell at which you began your journey. There is nothing remarkable here."),
    "hallway1" : location_model.Location(18, "You enter a hallway with a T-intersection.", "The hallway splits off into three directions: One to the south - where you began your journey, and another two rooms at the east and west ends of either hallway.", "You arrive back into the middle of the t-section. The room you started in to your south, with the other rooms to your east and west."),
    #left:
    "room3" : location_model.Location(3, "You enter what appears to be a dining hall, long since operable.", "There appear to be three tables that once resided here, though the years have caused them to deteriorate fairly heavily. The large fire place against the west wall lies cold and dormant with an ornate shield mounted above it. There is a door to the north that appears to lead to a slightly winding hallway, and a door to the east which leads back into the first hallway you had entered.", "You find yourself back in the dining hall."),
    "hallway2" : location_model.Location(19, "You enter another hallway, one passage of which seems to lead to a different hallway.", "The hallway splits off into a few directions: to the west is a door with the words 'Mess Hall', and to the east there is an unmarked door. A doorway to the north, appears to lead to another hallway.", "You're back in the hallway that led between the kitchen and the dining hall."),
    "room4" : location_model.Location(4, "You enter what you can only surmise to be the kitchen.", "The pungent, wet stench of mildew emanates from the wet dungeon walls. The counters are strewn with rotten food, and a knife stuck in a chopping block. Turning to look back at the door you entered through, you catch a glimmer of red out of the corner of your eye. Focusing on the glimmer, you see a small vial with a red liquid inside of it.", "You come back into the kitchen. You believe this to be one of the lease appetizing kitchens you've ever set foot in."),
    "hallway3" : location_model.Location(20, "You enter the hallway north of the kichen and dining hall connecting hallway.", "There is a wooden door with an iron-barred viewhole to the west. Above the door reads the sign 'Barracks'. To the east, the hallway wraps around the corner into another room with an iron door. To the south is the other hallway, leading to and from the kitchen and mess hall.", "You are back in the hallway which connects the barracks to the foyer."),
    "room5" : location_model.Location(5, "This must be the barracks. As you look around the room, all across the walls are various weapon racks, most of which are either empty, or their contents have rusted beyond use.", "Upon closer inspection of the weapon racks, there is a longsword, a pike, and a battleaxe in good condition. On the northern side of the room, there is what appears to be a short hallway. The door on the east side leads back into the hallway you entered from.", "You are back in the barracks."),
    "room6" : location_model.Location(6, "You enter a room with cots lining the wall. In the center of the room is a table strewn with dirty dishes and playing cards.", "This must be where some soldiers or militia would rest when not on watch. Walking towards the table the glimmer of a red vile catches your eye. Looking toward the only exit to the south, you see a breastplate laid out on a bench.", "You re-enter the barracks' sleeping chambers. As sleepy as you are, you don't feel like lying down to rest just yet."),
    "room7" : location_model.Location(7, "You enter what appears to be a foyer.", "There is a desk in the corner with a ledger atop it. To the east, there is a large doorway which looks like it leads to the main hallway of the dungeon. To the north there is another door leading to a lesser hallway. There is also a door on the west side of the room.", "You re-enter the foyer."),
    "hallway4" : location_model.Location(21, "You enter the main grand hallway of the dungeon.", "The walls are adorned with sconces, none of which are currently lit. The red carpet running the length of the hallway has long since been torn and soiled through the years. At the mid point of the hallway, there is a passage that leads north down another hallway, with a closed door opposite the path on the south side. There are also doors on both the eastern and western ends of the main hallway.", "You're back in the grand hallway, in the center of the dungeon."),
    "hallway6" : location_model.Location(23, "You enter the hallway to the north of the foyer.", "The hallway splits into multiple directions. To the east is an iron-barred door that appears to be a jail cell. There is also a door to the north with a sign that reads 'Contraband'. Venturing south would take you back to the foyer.", "You find yourself back in the hallway linking the jail cell, contraband storage, and foyer."),
    "room8" : location_model.Location(8, "You enter the jail cell.", "On the floor are two skeletons, prisoners long since dead with chains linking their feet to the walls. The only exit to this room is the western door.", "You enter the cell again. As before, there is nothing particularly remarkable about this room."),
    "room9" : location_model.Location(9, "You enter the storage room, where prisoners' belongings are held after their arrest.", "There are a number of crates in this room. While most of them are broken or deterioriated, there's one that's broken open that has a helmet residing inside it. The only exit to this room is to the south from whence you came.", "You re-enter the contraband storage adjacent to the jail cell."),
    #right
    "room2" : location_model.Location(2, "You enter a spacious room with a large table in the center or it.", "On the table in the center of the room is an old, dusty map with markers atop it and a pair of boots lay discarded underneath. This appears to be a sort of war room where battle plans were drawn up. The door to the west remains open, and the door to the north is shut.", "You're back in the war room."),
    "room13" : location_model.Location(13, "You enter a room with several weapon and armor racks across the walls.", "As you search around the room, you ascertain that this must be some type of armory. There are a number of rusted, inoperable old weapons and suits of armor within the room. There are doorways leading south and east from here.", "You go back into the armory."),
    "hallway5" : location_model.Location(22, "You enter a hallway with a T-intersection.", "At the center of the intersection are a number of signs which point in different directions. The sign which points north is labeled 'Laboratory'. The sign pointing west reads 'Armory'. The sign pointing south has the word 'Library' on it.", "You're back in the hallway which connects the Armory, Library, and Laboratory."),
        #secret passage
    "room14" : location_model.Location(14, "You enter a room with countless dusty bookcases across all of its walls.", "There are far too many dusty books to count in this room. The door to the north leads back to the hallway which connects the library to the Armory and Laboratory. Upon close insection, there appears to be a book untouched by dust on the eastern wall. On a separate bookcase, there is an untouched health potion, free for the taking.", "You're back in the library."),
    "secretPassage1" : location_model.Location(24, "You walk through the doorway which was hidden by a bookcase. As you clear the doorway, the bookcase closes firmly behind you.", "The long passageway is dark and narrow. You look at the bookcase that closed behind you to see that there is not a way to reopen the way west. The only way forward would be to travel to the north end of the corridor.", "You're back in the long hallway which ultimately leads to the library, but you can only travel north from here since the bookcase door is tightly shut."),
    "room15" : location_model.Location(15, "You enter a room that contains an altar with a shallow basin underneath.", "The altar is decorated with a dark purple cloth, stained in places with dried blood. The basin has a liquid with a soft, light blue tint to it. There is an intricate kris dagger resting on the lip of the basin. The south passage leads to a dead end since the bookcase closed behind you. The only way forward is north.", "You're back in the ritual room with an altar in it."),
    "secretPassage2" : location_model.Location(25, "You enter another long hallway down this secret passage.", "The hallway is just as narrow and long as the one prior to the altar room to the south. There is a lone iron door at the northern end of the hallway.", "You re-enter the northern secret passage."),
        #end secret passage
    "room12" : location_model.Location(12, "You enter what seems to be a laboratory which belonged to a wizard or an alchemist at some point.", "There are a number of bookcases adorning the walls of this room, littered with cobwebs, dusty books, and a pair of gauntlets next to an assortment of trinkets that might have been used in some ritual. In the center of the room is a small table next to a large cauldron. On the small table is a rack of vials, mostly brokem, but one is intact, gleaming with a feint red glow. There is a door on the west side of the room, and another leading south. There also seems to be a small closet on the north side of the room.", "You re-enter the laboratory."),
    "room11" : location_model.Location(11, "You enter a small storage room with several shelves and bookcases on every wall.", "This appears to be a storage room where spell components were kept for the nearby laboratory. The bookcases and shelves reach higher than your arms can reach - but there is a ladder in the room that must have been used to reach reagents that were stored up high. The only viable direction here is south to the laboratory.", "You're back in the room where spell components are kept."),
    "room10" : location_model.Location(10, "You enter a room with several beds.", "This appears to be a bed chamber for several individuals. The beds are moderately well-kept and appear to have been used recently. On one of the bedside tables is a small red vial. The northern door is the only way out of this room.", "You re-enter the sleeping chamber."),
    "room16" : location_model.Location(16, "After a long hallway, you enter a massive, rectangular room with ten pillars going down the length of it.", "For a room this large, you're surprised to find that it's ultimately empty and devoid of anything of interest. Just as you think this room is utterly empty, you see a gleam of red coming from a small vile behind a pillar.", "You find yourself back in the large pillar room."),
    "BossRoom" : location_model.Location(17, "As you enter the next room, your eyes are fixated upon what lies before you. All beneath your feet and across the floor is a massive hoard of treasure. Countless gold coins, jewels, and silver trinkets litter the entirety of the room.", "There will eventually be a boss fight here but we have to code that first.", "How... How are you doing this?")
}

#------------------ENEMY CONNECTIONS-----------------------#
locations["hallway1"].enemies.append(monsters["skeleton"])
    #left
locations["room3"].enemies.append(monsters["cultist"])
locations["room6"].enemies.append(monsters["cultist2"])
locations["room7"].enemies.append(monsters["gargoyle"])
locations["room9"].enemies.append(monsters["skeleton3"])
    #right
locations["room2"].enemies.append(monsters["skeleton2"])
locations["room10"].enemies.append(monsters["gargoyle2"])
locations["room12"].enemies.append(monsters["cultist3"])
locations["room11"].enemies.append(monsters["skeleton4"])
locations["secretPassage1"].enemies.append(monsters["giant rat"])
locations["secretPassage2"].enemies.append(monsters["giant rat2"])
    #to the boss
locations["room16"].enemies.append(monsters["wizard who smells quite bad"])
locations["BossRoom"].enemies.append(monsters["Grand Python Beast Pythulhu"])
#-----------------END ENEMY CONNECTIONS--------------------#

#----------------------ITEM CONNECTIONS--------------------#
locations["room1"].items.append(things["key"])
locations["room1"].items.append(things["sword"])
locations["room2"].items.append(things["boots"])
locations["room3"].items.append(things["shield"])
locations["room4"].items.append(things["knife"])
locations["room4"].items.append(things["health"])
locations["room5"].items.append(things["longsword"])
locations["room5"].items.append(things["pike"])
locations["room5"].items.append(things["battleaxe"])
locations["room6"].items.append(things["health"])
locations["room6"].items.append(things["breastplate"])
locations["room9"].items.append(things["helmet"])
locations["room10"].items.append(things["health"])
locations["room12"].items.append(things["gauntlets"])
locations["room12"].items.append(things["health"])
locations["room14"].items.append(things["health"])
locations["room15"].items.append(things["dagger"])
locations["room16"].items.append(things["health"])
#-------------------END ITEM CONNECTIONS-------------------#

#--------------------ROOM CONNECTIONS--------------------#
locations["room1"].n_to = locations["hallway1"]
locations["room1"].n_to.islocked = True
locations["hallway1"].s_to = locations["room1"]
locations["hallway1"].e_to = locations["room2"]
locations["hallway1"].w_to = locations["room3"]
#left
locations["room3"].e_to = locations["hallway1"]
locations["room3"].n_to = locations["hallway2"]
locations["hallway2"].s_to = locations["room3"]
locations["hallway2"].e_to = locations["room4"]
locations["room4"].w_to = locations["hallway2"]
locations["hallway2"].n_to = locations["hallway3"]
locations["hallway3"].s_to = locations["hallway2"]
locations["hallway3"].w_to = locations["room5"]
locations["room5"].e_to = locations["hallway3"]
locations["room5"].n_to = locations["room6"]
locations["room6"].s_to = locations["room5"]
locations["hallway3"].e_to = locations["room7"]
locations["room7"].w_to = locations["hallway3"]
locations["room7"].n_to = locations["hallway6"]
locations["hallway6"].s_to = locations["room7"]
locations["hallway6"].e_to = locations["room8"]
locations["room8"].w_to = locations["hallway6"]
locations["hallway6"].n_to = locations["room9"]
locations["room9"].s_to = locations["hallway6"]
locations["room7"].e_to = locations["hallway4"]
#right
locations["room2"].w_to = locations["hallway1"]
locations["room2"].n_to = locations["room13"]
locations["room13"].s_to = locations["room2"]
locations["room13"].e_to = locations["hallway5"]
locations["hallway5"].w_to = locations["room13"]
locations["hallway5"].s_to = locations["room14"]
#secret passage
locations["room14"].n_to = locations["hallway5"]
locations["room14"].e_to = locations["secretPassage1"]
locations["room14"].e_to.islocked = True
locations["secretPassage1"].n_to = locations["room15"]
locations["room15"].s_to = locations["secretPassage1"]
locations["room15"].n_to = locations["secretPassage2"]
locations["secretPassage2"].s_to = locations["room15"]
locations["secretPassage2"].n_to = locations["BossRoom"]
#end of secret passage
locations["hallway5"].n_to = locations["room12"]
locations["room12"].s_to = locations["hallway5"]
locations["room12"].n_to = locations["room11"]
locations["room11"].s_to = locations["room12"]
locations["room12"].w_to = locations["hallway4"]
locations["hallway4"].w_to = locations["room7"]
locations["hallway4"].e_to = locations["room12"]
locations["hallway4"].s_to = locations["room10"]
locations["room10"].n_to = locations["hallway4"]
locations["hallway4"].n_to = locations["room16"]
locations["room16"].s_to = locations["hallway4"]
locations["room16"].n_to = locations["BossRoom"]
#------------------END ROOM CONNECTIONS--------------------#





#starting room#
position = locations["room1"]
locations["room1"].already_visited = True

# def quit():
#     print("Quitting the game")
#     return False

def valid_directions():
    validDirs = directions()

    if validDirs.__contains__("n"):
        validDirs.extend(["north"])

    if validDirs.__contains__("s"):
        validDirs.extend(["south"])

    if validDirs.__contains__("e"):
        validDirs.extend(["east"])

    if validDirs.__contains__("w"):
        validDirs.extend(["west"])

    return validDirs

def directions():
    directions = []

    if hasattr(player.position, "n_to"):
        directions.append("n")
    if hasattr(player.position, "s_to"):
        directions.append("s")
    if hasattr(player.position, "e_to"):
        directions.append("e")
    if hasattr(player.position, "w_to"):
        directions.append("w")

    return directions

def inspect(item):
    if isinstance(item, item_model.Item):
        print(f"You inspect the {item.name}")
        print(item.description)

def travel(input):
    input = input.lower()
    if input not in valid_directions():
        print("There is not an exit in that direction. Please try again.")
        time.sleep(0.5)
        print()
    if input in valid_directions():
        if input =="n" or input == "north":
            if player.position.n_to.islocked == True:
                print("You cannot go that direction - the door is locked!")
                time.sleep(0.5)
                print()
                return
            player.position = player.position.n_to
            if player.position.already_visited == False:
                print(player.position.description)
                time.sleep(0.5)
                print()
                player.position.already_visited = True
            else:
                print(player.position.visited_description)
                time.sleep(0.5)
                print()
            if len(player.position.enemies) > 0: # here
                player.in_combat = True
                combat(player, enemy=player.position.enemies[0])
                time.sleep(1.0)
        if input =="s" or input == "south":
            if player.position.s_to.islocked == True:
                print("You cannot go that direction - the door is locked!")
                time.sleep(0.5)
                print()
                return
            player.position = player.position.s_to
            
            if player.position.already_visited == False:
                print(player.position.description)
                time.sleep(0.5)
                print()
                player.position.already_visited = True
            else: 
                print(player.position.visited_description)
                time.sleep(0.5)
                print()
            if len(player.position.enemies) > 0: # here
                player.in_combat = True
                combat(player, enemy=player.position.enemies[0])
                time.sleep(1.0)
        if input =="e" or input == "east":
            if player.position.e_to.islocked == True:
                print("You cannot go that direction - the door is locked!")
                time.sleep(0.5)
                print()
                return
            player.position = player.position.e_to
            
            if player.position.already_visited == False:
                print(player.position.description)
                player.position.already_visited = True
                time.sleep(0.5)
                print()
            else: 
                print(player.position.visited_description)
                time.sleep(0.5)
                print()
            if len(player.position.enemies) > 0: # here
                player.in_combat = True
                combat(player, enemy=player.position.enemies[0])
                time.sleep(1.0)
        if input =="w" or input == "west":
            if player.position.w_to.islocked == True:
                print("You cannot go that direction - the door is locked!")
                time.sleep(0.5)
                print()
                return
            player.position = player.position.w_to
            
            if player.position.already_visited == False:
                print(player.position.description)
                player.position.already_visited = True
                time.sleep(0.5)
                print()
            else: 
                print(player.position.visited_description)
                time.sleep(0.5)
                print()
            if len(player.position.enemies) > 0: # here
                player.in_combat = True
                combat(player, enemy=player.position.enemies[0])
                time.sleep(1.0)

def help():
    return  '''
            You hear a voice that surrounds and envelopes you, internally and externally, and says:

            *[travel, go] to move from place to place
            *[n,s,e,w] [North, South, East, West] to signify which direction to travel
            *[investigate, search, inspect] to further inspect your surroundings
            *[equip] [item name] to equip a weapon or shield to your left or right hands
            *[wear] [item name] to don a piece of armor you may find in the dungeon
            *[drink] [item name] to drink any potions you may find

            There may be other commands you can issue, but they're our secret...
            '''

def commands(input):
    available_commands = [
        "travel","go", "walk",
        "investigate", "search", "inspect",
        "get","grab", "take", "pickup", "loot",
        "inventory", "use", "key", "book", "equip", "wear",
        "drink", "potion", "attack", "help", "chair",
        "explain", "ska"
    ]
    available_commands.extend(valid_directions())
    available_commands.extend([item.name for item in player.inventory])
    available_commands.extend([item.name for item in player.position.items])

    input = input.lower()
    inputList = input.split(" ")
    
    cmd1 = ""
    cmd2 = ""
    cmd3 = ""

    commands = []
    for cmd in inputList:
        # if cmd in available_commands:
        commands.append(cmd)

    if len(commands) >= 1:
        cmd1 = commands[0]

    if len(commands) > 1:
        cmd2 = commands[1]

    if len(commands) > 2:
        cmd3 = commands[2]

    if cmd1 == "travel" or cmd1 == "go" or cmd1 == "walk":
        if player.in_combat == True:
            print("You try to make a break for it, but the enemy blocks your path and continues its attack!")
            time.sleep(1.0)
            return
        if cmd2 not in valid_directions():
            print("Input not valid - Please specify a valid direction in which to travel or go.")
            return
        if cmd2 in valid_directions():
            travel(cmd2)
            return

    if cmd1 not in available_commands:
        print(f"'{input}' is an invalid command. Try again and speak more clearly.")

    if cmd1 == "investigate" or cmd1 == "search":
        print("You look about your surroundings...")
        # time.sleep(1.0)
        print(player.position.inspection)
        # if len(player.position.items) > 0:
        #     item = player.position.investigate_room()
        #     player.inventory.append(item)
        return

    # if cmd1 == "inspect":
    #     item = player.discover(cmd2)
    #     inspect(item)
    #     return
        
    if cmd1 == "get" or cmd1 == "take" or cmd1 == "pickup" or cmd1 == "loot":
        if cmd2 in things:
            if things[cmd2] in player.position.items:
                item = player.take(things[cmd2])
                print(f"You pick up the {item.name}.")
                time.sleep(0.5)
                print()
                print(f"{item.description}")
                print()
                player.position.items.remove(item)
                return
        print(f"There are no {cmd2}s for you to take.")
        return

    if cmd1 == "inventory":
        if (len(player.inventory) == 0):
            print("Your inventory is empty.")
            # time.sleep(0.5)
            return
        player.list_inventory()
        return

    if cmd1 == "use" and cmd2 == "key":
        if things["key"] not in player.inventory:
            print("You don't have a key in your inventory.")
            print()
            return
        if player.position.n_to.islocked == True:
            player.position.n_to.islocked = False
            print("The key turns with a satisfying click then snaps in two... But the north door still swings open.")
            print()
            return
        elif player.position.s_to.islocked == True:
            player.position.s_to.islocked = False
            print("The key turns with a satisfying click then snaps in two... But the south door still swings open.")
            print()
            return
        elif player.position.e_to.islocked == True:
            player.position.e_to.islocked = False
            print("The key turns with a satisfying click then snaps in two... But the east door  stillswings open.")
            print()
            return
        elif player.position.w_to.islocked == True:
            player.position.w_to.islocked = False
            print("The key turns with a satisfying click then snaps in two... But the west door  stillswings open.")
            print()
            return
    if cmd1 == "use" and cmd2 == "book":
        if player.position != locations["room14"]:
            print("You rip a page out of the book... And wipe your nose with it.")
            print()
        else:
            print("You pull the book towards you, and the bookcase opens wide enough for you to walk through. You're not sure how long it will stay open...")
            print()
            time.sleep(1.0)
            player.position.e_to.islocked = False
            return

    if cmd1 == "equip":
        if cmd2 in things:
            if things[cmd2] in player.inventory:
                item = player.use_from_inventory(cmd2)
                player.equip(item)
                return
            else:
                print(f"You don't have {cmd2} in your inventory.")
                time.sleep(0.5)
                return
        else:
            print(f"You don't have {cmd2} in your inventory.")
            time.sleep(0.5)
            return

    if cmd1 == "wear":
        if cmd2 in things:
            item = player.use_from_inventory(cmd2)
            player.wear(item)
            return
        else:
            print("You can't equip that.")
            print()
            time.sleep(0.5)
            return

    if cmd1 == "drink" and cmd3 == "potion":
        if cmd2 in things:
            item = player.use_from_inventory(cmd2 + " " + cmd3)
            if cmd2 == "health":
                player.heal(item)
                return
            if cmd2 == "strength":
                player.strength_pot(item)
                return
            if cmd2 == "defense":
                player.defense_pot(item)
                return
        else:
            print("You can't drink that...")
            # time.sleep(1.0)
            return

    if cmd1 == "drink" and cmd2 == "liquid":
        if player.position != locations["room15"]:
            print("Drink what liquid? Do you mean a potion?")
            print()
            time.sleep(0.5)
        else:
            print("You drink the mysterious glowing liquid from the basin.")
            print()
            time.sleep(1.0)
            print("It doesn't taste very good, but you're a bit less thirsty than you were.")
            print()
            time.sleep(1.0)
            print("You also notice there's just a light underneath the basin, to make the liquid look like it was glowing.")
            print()
            time.sleep(1.0)
            print("Overall, you still feel fine, and keep moving.")
            print()
            time.sleep(0.5)
            return

    if cmd1 == "grab" and cmd2 == "chair":
        if player.position != locations["room3"] or len(player.position.enemies) < 1:
            print("I know you want to grab a chair, but there isn't one around.")
            print()
            time.sleep(1.0)
        else:
            enemy = player.position.enemies[0]
            print(f"You grab a chair off of the ground, and swing it as hard as you can at the {enemy.name}!")
            print()
            time.sleep(1.0)
            player.smash(enemy)
            return

    if cmd1 == "explain" and cmd2 == "ska":
        if player.position != locations["BossRoom"]:
            print("You try to explain the intricacies of ska out loud, but nobody is listening.")
            time.sleep(1.0)
            print()
        else:
            enemy = player.position.enemies[0]
            print(f"You start to explain the background and origins of ska music to {enemy.name}")
            time.sleep(1.0)
            print()
            print(f"{enemy.name} looks unbelievably bored while you keep talking about Reel Big Fish and the Aquabats.")
            print()
            time.sleep(1.0)
            print(f"The {enemy.name} lets out a long, exasperated sigh and leaves the room.")
            print()
            time.sleep(1.0)
            player.kill(enemy)
            return


    if cmd1 == "attack":
        if len(player.position.enemies) < 1:
            print("There is nothing to attack here.")
            time.sleep(0.5)
            print()
            return
        enemy = player.position.enemies[0]
        print(f"Your current health is: {player.health}.")
        print()
        player.swing(enemy)
        return

    if cmd1 == "help":
        print(help())
        time.sleep(1.0)
        return

def combat(player, enemy):
    if enemy == monsters["Grand Python Beast Pythulhu"]:
        print(f"As you enter the grand chamber, filled with riches, you lock eyes with The {enemy.name}, who moves in to attack!")
        print()
        time.sleep(2.0)
    else:
        print(f"As you enter the room, you immediately see a {enemy.name}, waiting to attack!")
        print()
        time.sleep(1.0)
    turn = random.randint(1, 2)
    # turn = 1
    if turn == 1:
        player_turn = True
        enemy_turn = False
        print("You surprised the enemy! You can attack first.")
        time.sleep(0.5)
        print()
    else: 
        player_turn = False
        enemy_turn = True
        print("The enemy in the room catches you off-guard, and moves to attack!")
        time.sleep(0.5)
        print()
    while player.health > 0 or enemy.health > 0:
        if player_turn:
            print("The combat rages on. What do you do?!")
            print()
            p = input()
            commands(p)
            
        if enemy_turn: #enemy turn#
            enemy.enemy_attack(player)

        if player.health <= 0:
            print("You have died a painful death. The dungeon devours yet another soul. Play again if you dare!")
            print()
            game_over()  
        if enemy.health <= 0: 
            if enemy == monsters["Grand Python Beast Pythulhu"]:
                print("You have slain the Almighty Grand Beast Pythulhu!")
                time.sleep(0.5)
                print("You gaze upon the riches encased in the tomb, and claim them as your own. Congratulations!")
                print()
                time.sleep(1.0)
                print(f"All hail {player.name}, conqueror of the Lair of the Python!")
                time.sleep(1.0)
                print("Thanks for playing, feel free to play again any time!")
                time.sleep(1.5)
                game_over()
            print(f"You have slain the {enemy.name}, and are safe to traverse the dungeon further.")
            print()
            player.position.enemies.clear()
            player.in_combat = False
            return
        player_turn = not player_turn
        enemy_turn = not enemy_turn

os.system('clear')
print("What is your name, adventurer?")
x = input()
print("Creating character...")
time.sleep(1.0)
print("Complete!")
print()
time.sleep(1.0)
os.system('clear')
player = character_model.Character(x, position, 100)
print(f"Hello, {player.name}, and welcome to...")
time.sleep(2.0)
os.system('clear')


print("HISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
print()
print(' ██▓    ▄▄▄       ██▓ ██▀███      ▒█████    █████▒   ▄▄▄█████▓ ██░ ██ ▓█████     ██▓███ ▓██   ██▓▄▄▄█████▓ ██░ ██  ▒█████   ███▄    █ ')
print('▓██▒   ▒████▄    ▓██▒▓██ ▒ ██▒   ▒██▒  ██▒▓██   ▒    ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀    ▓██░  ██▒▒██  ██▒▓  ██▒ ▓▒▓██░ ██▒▒██▒  ██▒ ██ ▀█   █ ')
print('▒██░   ▒██  ▀█▄  ▒██▒▓██ ░▄█ ▒   ▒██░  ██▒▒████ ░    ▒ ▓██░ ▒░▒██▀▀██░▒███      ▓██░ ██▓▒ ▒██ ██░▒ ▓██░ ▒░▒██▀▀██░▒██░  ██▒▓██  ▀█ ██▒')
print('▒██░   ░██▄▄▄▄██ ░██░▒██▀▀█▄     ▒██   ██░░▓█▒  ░    ░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄    ▒██▄█▓▒ ▒ ░ ▐██▓░░ ▓██▓ ░ ░▓█ ░██ ▒██   ██░▓██▒  ▐▌██▒')
print('░██████▒▓█   ▓██▒░██░░██▓ ▒██▒   ░ ████▓▒░░▒█░         ▒██▒ ░ ░▓█▒░██▓░▒████▒   ▒██▒ ░  ░ ░ ██▒▓░  ▒██▒ ░ ░▓█▒░██▓░ ████▓▒░▒██░   ▓██░')
print('░ ▒░▓  ░▒▒   ▓▒█░░▓  ░ ▒▓ ░▒▓░   ░ ▒░▒░▒░  ▒ ░         ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░   ▒▓▒░ ░  ░  ██▒▒▒   ▒ ░░    ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ')
print('░ ░ ▒  ░ ▒   ▒▒ ░ ▒ ░  ░▒ ░ ▒░     ░ ▒ ▒░  ░             ░     ▒ ░▒░ ░ ░ ░  ░   ░▒ ░     ▓██ ░▒░     ░     ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░')
print('  ░ ░    ░   ▒    ▒ ░  ░░   ░    ░ ░ ░ ▒   ░ ░         ░       ░  ░░ ░   ░      ░░       ▒ ▒ ░░    ░       ░  ░░ ░░ ░ ░ ▒     ░   ░ ░ ')
print('    ░  ░     ░  ░ ░     ░            ░ ░                       ░  ░  ░   ░  ░            ░ ░               ░  ░  ░    ░ ░           ░ ')
print('                                                                                         ░ ░                                          ')
print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")

time.sleep(3.0)
os.system("clear")
print()
print(f"{player.position.description}")
print()
print("You may type 'help' at any time during your play for a list of available commands.")
print()

def game_over():
    print("Exiting game...")
    time.sleep(1.5)
    exit()

def game():
    running = True
    while running:
        time.sleep(1.0)
        print("What would you like to do?")
        print()
        p = input()
        print() #does this work here?
        commands(p)

game()