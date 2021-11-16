from flask_app.models import character_model, item_model

class Location:
    def __init__(self, id, description, inspection, visited_description, already_visited=False, islocked = False):
        self.id = id
        self.description = description
        self.inspection = inspection    #description of inspecting
        self.items = []
        self.enemies = []
        self.visited_description = visited_description
        self.already_visited = False
        self.islocked = False

    # def investigate_room(self):
    #     print("You see the following items:")
    #     for idx, item in enumerate(self.items):
    #         print(f"{idx}:{item.name}")
    #     print("What do you want to take?(Use the numbers)")
    #     item_prompt = input()
    #     item = self.items.pop(int(item_prompt))
    #     return item