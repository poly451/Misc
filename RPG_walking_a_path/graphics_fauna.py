import os, sys
import pygame
import utils
import constants
import random
import math
from graphics_environment import Walkables, Obstacles

# -----------------------------------------------------------
#                      class Player
# -----------------------------------------------------------
"""
As you can see, class Player uses inheritance. We do this so that 
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and, 
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, or ask the folks over on 
Stack Overflow (https://stackoverflow.com/) or even on Twitter.
"""
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.init_pygame()
        self.x = -1
        self.y = -1
        self.name = ""
        self.kind = ""
        self.direction = constants.DOWN
        # ---------------------------------------------
        self.maximum_damage = 2
        self.max_hit_points = -1
        self.hit_points = -1
        self.chance_to_hit = -1
        self.experience = -1
        self.profession = None
        self.gold = -1
        # ---------------------------------------------
        # self.inventory = Inventory("player")
        # ---------------------------------------------
        # x, y = utils.get_players_position_on_map()
        # self.x = x
        # self.y = y
        # ---------------------------------------------
        self.image = None
        self.image_dead = None
        self.image_up = None
        self.image_down = None
        self.image_right = None
        self.image_left = None
        self.rect = None
        self.font = None
        # ---------------------------------------------

    def load_images(self):
        filepath = os.path.join("data", "images", constants.PLAYER_IMG)
        print("filepath: {}".format(filepath))
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ----
        filepath = os.path.join("data/images", constants.PLAYER_IMG_DEAD)
        print("filepath: {}".format(filepath))
        self.image_dead = pygame.image.load(filepath).convert_alpha()
        self.image_dead = pygame.transform.scale(self.image_dead, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ----
        filepath = os.path.join("data", "images", constants.PLAYER_IMG_UP)
        self.image_up = pygame.image.load(filepath).convert_alpha()
        self.image_up = pygame.transform.scale(self.image_up, (constants.TILESIZE, constants.TILESIZE))
        # ----
        filepath = os.path.join("data", "images", constants.PLAYER_IMG_DOWN)
        self.image_down = pygame.image.load(filepath).convert_alpha()
        self.image_down = pygame.transform.scale(self.image_down, (constants.TILESIZE, constants.TILESIZE))
        # ----
        filepath = os.path.join("data", "images", constants.PLAYER_IMG_RIGHT)
        self.image_right = pygame.image.load(filepath).convert_alpha()
        self.image_right = pygame.transform.scale(self.image_right, (constants.TILESIZE, constants.TILESIZE))
        # ----
        filepath = os.path.join("data", "images", constants.PLAYER_IMG_LEFT)
        self.image_left = pygame.image.load(filepath).convert_alpha()
        self.image_left = pygame.transform.scale(self.image_left, (constants.TILESIZE, constants.TILESIZE))

    def get_position(self):
        return [self.x * constants.TILESIZE, self.y * constants.TILESIZE]

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def read_data_first(self):
        # self.inventory.read_data()
        user_data = utils.get_user_data()
        path = os.path.join("data", user_data["character_name"], constants.PLAYER_DATA_FILE)
        # print("path: {}".format(path))
        mylist = utils.read_data_file(path, num_of_fields=11)
        mydict = mylist[0]
        # print("mydict: {}".format(mydict))
        # ----
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.name = mydict["name"]
        self.kind = mydict["kind"]
        if utils.is_int(mydict["direction"]) == True:
            self.direction = int(mydict["direction"])
        else:
            self.direction = utils.convert_direction_to_integer(mydict["direction"])
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        self.profession = mydict["profession"]
        self.gold = mydict["gold"]
        # ----
        self.load_images()

    def read_data_restart(self, x=-1, y=-1):
        # print("mydict: {}".format(mydict))
        # self.inventory = Inventory("player")
        # self.inventory.read_data()
        user_data = utils.get_user_data()
        path = os.path.join("data", user_data["character_name"], constants.PLAYER_DATA_FILE)
        mylist = utils.read_data_file(path, num_of_fields=11)
        mydict = mylist[0]
        # ----
        if x == -1 and y == -1:
            self.x = mydict["x"]
            self.y = mydict["y"]
        else:
            if x == -1 or y == -1:
                raise ValueError("Error!")
            self.x = x
            self.y = y
        # ----
        self.name = mydict["name"]
        self.kind = mydict["kind"]
        if utils.is_int(mydict["direction"]) == True:
            self.direction = -90
        else:
            self.direction = utils.convert_direction_to_integer(mydict["direction"])
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        self.profession = mydict["profession"]
        self.gold = mydict["gold"]
        # ----
        self.load_images()
        # ----
        self.direction = "DOWN"

    def calculate_damage(self):
        return self.maximum_damage

    # def inventory_display_string(self):
    #     s = self.inventory.display_string()

    def is_dead(self):
        if self.hit_points <= 0: return True
        return False

    def get_fileline(self):
        s = "x: {}\ny: {}\nname: {}\nkind: {}\ndirection: {}\nmax_hit_points: {}" \
            "\nhit_points: {}\nchance_to_hit: {}\nexperience: {}\nprofession: {}\ngold: {}\n"
        s = s.format(self.x, self.y, self.name, self.kind, "-90", self.max_hit_points,
                     self.hit_points, self.chance_to_hit, self.experience, self.profession, self.gold)
        return s

    def save_data(self):
        # save player data
        user_data = utils.get_user_data()
        player_string = self.get_fileline()
        filepath = os.path.join("data", user_data["character_name"], constants.PLAYER_DATA_FILE)
        with open(filepath, "w") as f:
            f.write(player_string)
        # save inventory data
        # self.inventory.save_data()
        # self.inventory.save_player_inventory()

    def resize(self, tilesize, new_x, new_y):
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(new_x * constants.TILESIZE, new_y * constants.TILESIZE)

    def display_list(self):
        mylist = []
        mylist.append("x,y: ({},{})".format(self.x, self.y))
        mylist.append("direction: {}".format(utils.convert_integer_to_direction(self.direction)))
        mylist.append("max hit points: {}".format(self.max_hit_points))
        mylist.append("hit points: {}".format(self.hit_points))
        mylist.append("chance to hit: {}".format(self.chance_to_hit))
        mylist.append("experience: {}".format(self.experience))
        mylist.append("profession: {}".format(self.profession))
        mylist.append("gold: {}".format(self.gold))
        return mylist

    def _collide(self, dx=0, dy=0, obstacles=None):
        for a_tile in obstacles:
            if a_tile.x == self.x + dx and a_tile.y == self.y + dy:
                return True
        return False

    def move(self, dx=0, dy=0, obstacles=None):
        if not self._collide(dx, dy, obstacles):
            self.x += dx
            self.y += dy
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)

    def move_right(self, obstacles=None):
        dx, dy = -1, 0
        self.move(dx, dy, obstacles)

    def move_left(self, obstacles=None):
        dx, dy = 1, 0
        self.move(dx, dy, obstacles)

    def move_down(self, obstacles=None):
        dx, dy = 0, 1
        self.move(dx, dy, obstacles)

    def move_up(self, obstacles=None):
        dx, dy = 0, -1
        self.move(dx, dy, obstacles)

    def move_toward(self, x, y, obstacles=None):
        # self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
        if self.x == x and self.y == y:
            return True
        if self.x == x and self.y != y:
            if self.y - y < 0:
                self.move_down(obstacles)
            else:
                self.move_up(obstacles)
        elif self.x != x and self.y == y:
            if (self.x - x) < 0:
                self.move_left(obstacles)
            else:
                self.move_right(obstacles)
        elif self.x !=x and self.y != y:
            myrand = random.randint(0, 1)
            if myrand == 0:
                if self.y - y < 0:
                    self.move_down(obstacles)
                else:
                    self.move_up(obstacles)
            elif myrand == 1:
                if (self.x - x) < 0:
                    self.move_left(obstacles)
                else:
                    self.move_right(obstacles)
            else:
                raise ValueError("Error!")
        else:
            raise ValueError("Error!")
        # if abs(self.x - x) > abs(self.y - y):
        #     self.move_right(obstacles)
        # elif abs(self.x - x) < abs(self.y - y):
        #     self.move_left(obstacles)
        # elif abs(self.x - x) == abs(self.y - y):
        #     myran = random.randint(0, 1)
        #     if myran == 0:
        #         self.move_right(obstacles)
        #     else:
        #         self.move_left(obstacles)
        # else:
        #     raise ValueError("Error!")

    def debug_print(self):
        title, length = utils.format_string("Player.debug_print()", length=50, my_divider="-")
        print(title)
        s = "x,y: ({},{}); name: {}; kind: {}; direction: {}; max_hit_points: {}; "
        s += "hit_points: {}; chance_to_hit: {}; experience: {}; profession: {}; gold: {}"
        s = s.format(self.x, self.y, self.name, self.kind, self.direction, self.max_hit_points,
                     self.hit_points, self.chance_to_hit, self.experience, self.profession, self.gold)
        print(s)
        # self.inventory.debug_print()
        title, length = utils.format_string("- END - Player.debug_print()", length=50, my_divider="-")
        print(title)

# -----------------------------------------------------------
#                      class Npc
# -----------------------------------------------------------
"""
As you can see, class Merchant uses inheritance. We do this so that 
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and, 
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, ask on 
Stack Overflow (https://stackoverflow.com/) or even Twitter.
"""
class Npc(pygame.sprite.Sprite):
    def __init__(self, character_name_and_location):
        super().__init__()
        # self.init_pygame()
        self.character_name = character_name_and_location[0].strip()
        self.x = character_name_and_location[1]
        self.y = character_name_and_location[2]
        self.character_kind = ""
        self.gold = ""
        self.inventory = None
        # # ---------------------------------------------
        self.image = None
        self.rect = None
        # filepath = os.path.join("data", "images", constants.MERCHANT)
        # self.image = pygame.image.load(filepath).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        # self.rect = self.image.get_rect()
        # self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def read_data(self):
        filename = "{}.txt".format(self.character_name)
        filepath = os.path.join("data", "master_files", "npcs", "merchants", filename)
        print("Opening file: {}".format(filepath))
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        # ----
        mydict = {}
        for a_line in mylines:
            # print(a_line)
            mydict = utils.key_value(a_line, mydict)
        mydict.pop("inventory")
        # print("mydict", mydict)
        # self.x = mydict["x"]
        # self.y = mydict["y"]
        # print("{} is at x,y: ({},{})".format(self.character_name, self.x, self.y))
        # self.character_name recorded in __Init__
        self.character_kind = mydict["character_kind"]
        self.gold = mydict["gold"]
        self.image_filename = mydict["image"]
        # ---------------------------------------------
        # Images
        filepath = os.path.join("data", "images", self.image_filename)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
            self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        except Exception as e:
            print("filepath: {}".format(filepath))
            raise ValueError("Error! e: {}".format(e))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ----
        self.inventory = Inventory(self.character_kind, self.character_name)
        self.inventory.read_data()

    def resize(self, tilesize, new_x, new_y):
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(new_x * constants.TILESIZE, new_y * constants.TILESIZE)

    def add_item(self, item_index, item_kind):
        self.inventory.add_item(item_index, item_kind)

    def add_item_by_name(self, item_name, item_kind):
        self.inventory.add_item_by_name(item_name, item_kind)

    def remove_item(self, item_index, item_kind):
        self.inventory.remove_item(item_index, item_kind)

    def remove_item_by_name(self, item_name, item_kind):
        self.inventory.remove_item_by_name(item_name, item_kind)

    def debug_print(self):
        title, length = utils.format_string("Npc.debug_print()", "-")
        print(title)
        s = "x,y: ({},{}); character_name: {}; character_kind: {}; gold: {}"
        s = s.format(self.x, self.y, self.character_name, self.character_kind, self.gold)
        print(s)
        self.inventory.debug_print()
        print("-" * length)

# -----------------------------------------------------------
#                      class Npcs
# -----------------------------------------------------------
class Npcs:
    def __init__(self):
        # if names_of_npcs_to_load is None:
        #     raise ValueError("Error! names_of_npcs_to_load cannot be None!")
        # if npc_names is None:
        #     raise ValueError("Error!")
        # ----
        # print("npc_names: {}".format(npc_names))
        # ----
        self.init_pygame() # <-- debugging
        # ----
        # self.npc_names = npc_names
        # self.foods = Foods()
        # self.foods.read_data()
        # # self.foods.debug_print()
        # self.drinks = Drinks()
        # self.drinks.read_data()
        # self.drinks.debug_print()
        # ----
        self.npcs = []
        # self.names_of_npcs_to_load = npc_names
        self.loop_index = 0
        # self.all_sprites = pygame.sprite.Group() # <-- debugging
        self.keep_looping = True # <-- debugging

    def read_data(self, npc_names_and_locations):
        self.npcs = []
        for an_npc_name in npc_names_and_locations:
            an_npc = Npc(an_npc_name)
            an_npc.read_data()
            self.npcs.append(an_npc)
        # print("There are {} npcs.".format(len(self.npcs)))

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def debug_print(self):
        title, length = utils.format_string("Npcs.debug.print()", "-")
        print(title)
        for elem in self.npcs:
            elem.debug_print()
        print("-" * length)

    def get_npc(self, x, y):
        # print("In get_npc: x,y: {},{}".format(x, y))
        # print("Number of npcs: {}".format(len(self.npcs)))
        for an_npc in self.npcs:
            if an_npc.x == x:
                if an_npc.y == y:
                    # print("Npc found:")
                    # an_npc.debug_print()
                    return an_npc
        return None

    def get_npc_by_name(self, npc_name):
        # print("In get_npc: x,y: {},{}".format(x, y))
        # print("Number of npcs: {}".format(len(self.npcs)))
        for an_npc in self.npcs:
            if an_npc.character_name == npc_name:
                return an_npc
        return None

    # def update_classes(self, all_sprites):
    #     for elem in self.npcs:
    #         all_sprites.add(elem)
    #     return all_sprites

    def __getitem__(self, item):
        return self.npcs[item]

    def __next__(self):
        if self.loop_index >= len(self.npcs):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.npcs[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.npcs)

    # --------------------------------------------

    def handle_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                    return True

    def update_classes(self, all_sprites):
        for elem in self.npcs:
            all_sprites.add(elem)
        return all_sprites

    # def draw(self):
    #     self.screen.fill(self.BG_COLOR)
    #     self.update_classes()
    #     # ----
    #     self.all_sprites.update()
    #     self.all_sprites.draw(self.screen)
    #     # ----
    #     pygame.display.flip()

    def main(self):
        """This is for debugging"""
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()


# -----------------------------------------------------------
#                      class Monster
# -----------------------------------------------------------
"""
As you can see, class Monster uses inheritance. We do this so that 
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and, 
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, ask on 
Stack Overflow (https://stackoverflow.com/) or even Twitter.
"""
class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = -1
        self.y = -1
        self.name = ""
        self.kind = ""
        self.max_hit_points = -1
        self.hit_points = -1
        # ---------------------------------------------
        self.maximum_damage = -1
        self.chance_to_hit = -1
        self.experience = -1
        # ---------------------------------------------
        self.image = None
        self.image_dead_monster = None
        self.rect = None
        # ---------------------------------------------

    def read_data(self, name_and_location):
        # filepath = os.path.join("data", constants.MONSTERS_DATA_FILE)
        # number_of_fields = 8
        # mylist = utils.read_data_file(filepath, number_of_fields)
        # mydict = mylist[0]
        filename = "{}.txt".format(name_and_location[0].strip())
        player_data = utils.get_user_data()
        filepath = os.path.join("data", player_data["character_name"], "monsters", filename)
        number_of_fields = 11
        mylist = utils.read_data_file(filepath, number_of_fields)
        mydict = mylist[0]
        # ----
        # self.x = mydict["x"]
        # self.y = mydict["y"]
        self.x = name_and_location[1]
        self.y = name_and_location[2]
        # self.name = mydict["name"]
        if mydict["name"].lower() != name_and_location[0].lower().strip():
            raise ValueError("Error! mydict[name]: {}; name_and_location[0].strip(): {}".format(mydict["name"], name_and_location[0].strip()))
        self.name = mydict["name"].lower()
        self.kind = mydict["kind"]
        self.maximum_damage = mydict["maximum_damage"]
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        # ---------------------------------------------
        self.monster_image = mydict["monster_image"]
        self.monster_image_dead = mydict["monster_image_dead"]
        # ---------------------------------------------
        filepath = os.path.join("data", "images", self.monster_image)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ---------------------------------------------
        filepath = os.path.join("data", "images", self.monster_image_dead)
        print("reading filepath: {}".format(filepath))
        self.image_dead_monster = pygame.image.load(filepath).convert_alpha()
        self.image_dead_monster = pygame.transform.scale(self.image_dead_monster, (constants.TILESIZE, constants.TILESIZE))
        # ---------------------------------------------
        if self.hit_points <= 0:
            self.image = self.image_dead_monster


    def calculate_damage(self):
        return self.maximum_damage

    def resize(self, tilesize, new_x, new_y):
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(new_x * constants.TILESIZE, new_y * constants.TILESIZE)

    def is_dead(self):
        if self.hit_points <= 0: return True
        return False

    def collide_with_walls(self, dx=0, dy=0, walls=None):
        for wall in walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def check_for_collision(self, dx, dy, walls):
        if not self.collide_with_walls(dx, dy, walls):
            self.x += dx
            self.y += dy
            # self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
            print("Monster has moved. x,y: {},{}. dx={}, dy={}".format(self.x, self.y, dx, dy))

    def move(self, walls):
        myran = random.randint(0, 4)
        if myran == 0:
            self.check_for_collision(0, 1, walls)
        elif myran == 1:
            self.check_for_collision(1, 0, walls)
        elif myran == 2:
            self.check_for_collision(0, -1, walls)
        elif myran == 3:
            self.check_for_collision(-1, 0, walls)
        elif myran == 4:
            pass
        else:
            raise ValueError("Error!")

    def monster_tries_to_hit_player(self, player):
        myran = random.randint(1, 100)
        if myran <= self.chance_to_hit:
            return True
        else:
            return False

    def get_fileline(self):
        s = "x: {}\ny: {}\nname: {}\nkind: {}\nmaximum_damage: {}\nmax_hit_points: {}\nhit_points: {}\nchance_to_hit: {}\n" \
            "experience: {}\nmonster_image: {}\nmonster_image_dead: {}\n"
        s = s.format(self.x, self.y, self.name, self.kind, self.maximum_damage, self.max_hit_points, self.hit_points,
                     self.chance_to_hit, self.experience, self.monster_image, self.monster_image_dead)
        return s

    def save_data(self):
        player_data = utils.get_user_data()
        filename = "{}.txt".format(self.name)
        filepath = os.path.join("data", player_data["character_name"], "monsters", filename)
        fileline = self.get_fileline()
        with open(filepath, "w") as f:
            f.write(fileline)

    # def save_temp_data(self):
    #     player_data = utils.get_user_data()
    #     filepath = os.path.join("data", player_data["character_name"], "monsters")
    #     # filepath = os.path.join("data", constants.MONSTERS_TEMP_FILE)
    #     # fileline = self.get_fileline()
    #     # with open(filepath, "w") as f:
    #     #     f.write(fileline)

    def debug_print(self):
        s = "Debug Print Monster"
        print("-" * 10, s, "-" * 10)
        # print("filepath: {}".format(self.filepath))
        print("monster name: {}; monster kind: {}\n".format(self.name, self.kind))
        print("maximum_damage: {}".format(self.maximum_damage))
        print("x,y: {},{}".format(self.x, self.y))
        print("max_hp: {}; hp: {}; chance_to_hit: {}; exp: {}".format(self.max_hit_points, self.hit_points, self.chance_to_hit, self.experience))
        print("image: {}".format(self.monster_image))
        print("image: {}".format(self.monster_image_dead))
        print(("-" * (len(s) + 20 + 2)))

# -----------------------------------------------------------
#                      class Monsters
# -----------------------------------------------------------
class Monsters:
    def __init__(self):
        self.init_pygame() # <-- debugging
        self.monsters = []
        self.loop_index = 0

    def read_data(self, monster_info):
        # Eg: [("nether", 2, 2), ("mordbog", 7, 8)]
        if monster_info is None:
            raise ValueError("Error!")
        # ----
        big_list = []
        for a_monster in monster_info:
            new_monster = Monster()
            new_monster.read_data(a_monster)
            big_list.append(new_monster)
        self.monsters = big_list

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)

    def get_monster(self, x, y):
        # print("In get_monster: x,y: {},{}".format(x, y))
        # print("Number of monsters: {}".format(len(self.monsters)))
        for a_monster in self.monsters:
            if a_monster.x == x:
                if a_monster.y == y:
                    # print("Monster found:")
                    # a_monster.debug_print()
                    return a_monster
        return None

    def get_monster_by_name(self, name):
        for a_monster in self.monsters:
            if a_monster.name == name:
                return a_monster
        return None

    def get_filelines(self):
        s = ""
        for a_monster in self.monsters:
            s += "{}\n".format(a_monster.get_fileline())
        return s

    def update_classes(self, all_sprites):
        for elem in self.monsters:
            all_sprites.add(elem)
        return all_sprites

    def debug_print(self):
        for elem in self.monsters:
            elem.debug_print()

    def debug_print_names(self):
        for elem in self.monsters:
            print(elem.name)

    def save_data(self):
        for a_monster in self.monsters:
            a_monster.save_data()

    def __getitem__(self, item):
        return self.monsters[item]

    def __next__(self):
        if self.loop_index >= len(self.monsters):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.monsters[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

# -----------------------------------------------------------
#                      class Environment
# -----------------------------------------------------------

class Fauna:
    def __init__(self, zone_name):
        if not zone_name in constants.ZONE_NAMES:
            s = "Error! This isn't a valid zone name: {}\n".format(zone_name)
            s += "Here are the valid zone names: {}".format(constants.ZONE_NAMES)
            raise ValueError(s)
        # ----
        self.init_pygame()
        self.zone_name = zone_name
        self.zone_description = ""
        self.merchants = Npcs()
        self.monsters = Monsters()
        # self.player_starting_coords = (-1, -1)
        # ----
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping = True

    def read_data(self):
        filepath = os.path.join("data", "zones", self.zone_name, "zone_init.txt")
        file_list = utils.read_data_file(filepath, 4)
        mydict = file_list[0]
        self.zone_description = mydict["zone_description"]
        # -------------------
        # # ---- MERCHANTS ----
        # if mydict["merchants"] == None:
        #     pass
        # elif mydict["merchants"] == "none":
        #     self.merchants = None
        # else:
        #     self.merchants = mydict["merchants"].split(";")
        #     self.merchants = [i.strip() for i in self.merchants if len(i.strip()) > 0]
        # # ----
        # big_list = []
        # for a_merchant in self.merchants:
        #     # print("a_merchant: {}".format(a_merchant))
        #     mylist = a_merchant.split(" ")
        #     mylist = (mylist[0], int(mylist[1]), int(mylist[2]))
        #     big_list.append(mylist)
        # print("big_list: {}".format(big_list))
        # # self.merchants = Npcs(["laura", "alvin"])
        # self.merchants = Npcs()
        # self.merchants.read_data(big_list)
        # ------------------
        # ---- MONSTERS ----
        # print("mydict: {}".format(mydict))
        temp_list = []
        if mydict["monsters"] == "none":
            self.monsters = None
        else:
            temp_list = mydict["monsters"].split(";")
            temp_list = [i.strip() for i in temp_list if len(i.strip()) > 0]
        # ----
        print("temp_list: {}".format(temp_list))
        big_list = []
        for a_monster in temp_list:
            print("a_monster: {}".format(a_monster))
            mylist = a_monster.split(" ")
            mylist = (mylist[0], int(mylist[1]), int(mylist[2]))
            big_list.append(mylist)
        print("big_list MONSTERS: {}".format(big_list))
        # self.merchants = Npcs(["laura", "alvin"])
        self.monsters = Monsters()
        self.monsters.read_data(big_list)
        # debugging self.monsters
        # self.monsters = Monsters()
        # self.monsters.read_data([("nether", 2, 2), ("mordbog", 2, 3)])
        # self.monsters = mydict["monsters"]
        # self.player_starting_coords = mydict["player_starting_coords"]

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def handle_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                    return True
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))

    def update_classes(self, all_sprites):
        if not self.merchants is None:
            all_sprites = self.merchants.update_classes(all_sprites)
        if not self.monsters is None:
            all_sprites = self.monsters.update_classes(all_sprites)
        return all_sprites

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.all_sprites = self.update_classes(self.all_sprites)
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping == True:
            self.handle_events()
            self.draw()
        self.goodbye()
        self.myquit()

    def goodbye(self):
        print("Goodbye!")

    def myquit(self):
        pygame.quit()

    def debug_print(self):
        s = "zone_name: {}\nzone_description: {}"
        s = s.format(self.zone_name, self.zone_description)
        print(s)
        self.merchants.debug_print()

# **************************************************
# **************************************************

if __name__ == "__main__":
    fauna = Fauna("env01")
    fauna.read_data()
    fauna.main()