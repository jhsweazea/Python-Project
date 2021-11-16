class Item:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def added(self):        #prints that the item was added to players inventory
        return  f"{self.name} is added into your inventory."
    
    def remove(self):
        return f"{self.name} is placed onto the floor."

class Equipment(Item):
    def __init__(self, id, name, description, defense=0):
        super().__init__(id, name, description)
        self.defense = defense 

class Weapon(Item):
    def __init__(self, id, name, description, attack=0, defense=0):
        super().__init__(id, name, description)
        self.attack = attack
        self.defense = defense 