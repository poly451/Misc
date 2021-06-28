import sys, os
import pygame
import constants
import utils

# -----------------------------------------------------------
#                      class Grass
# -----------------------------------------------------------

"""
As you can see, class Grass uses inheritance. We do this so that 
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and, 
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, ask on 
Stack Overflow (https://stackoverflow.com/) or even Twitter.
"""
class Walkable(pygame.sprite.Sprite):
    def __init__(self, mydict):
        super().__init__()
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.kind = mydict["kind"]
        # ----
        if self.kind == "grass":
            self.filepath = os.path.join("data", "images", constants.GRASS_IMG)
        elif self.kind == "dirt":
            self.filepath = os.path.join("data", "images", constants.DIRT_IMG)
        else:
            raise ValueError("I don't recognize this: {}".format(self.kind))
        # ----
        try:
            self.image = pygame.image.load(self.filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(self.filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def _collide(self, dx=0, dy=0, obstacles=None):
        for a_tile in obstacles:
            if a_tile.x == self.x + dx and a_tile.y == self.y + dy:
                return True
        return False

    def move(self, dx=0, dy=0, obstacles=None):
        if not self._collide(dx, dy, obstacles):
            self.x += dx
            self.y += dy
            # self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
            # print("Player has moved. x,y: {},{}; dx={}, dy={}".format(self.x, self.y, dx, dy))

    def debug_print(self):
        print("filepath: {}".format(self.filepath))
        print("x,y: {},{}".format(self.x, self.y))

# -----------------------------------------------------------
#                      class Grasses
# -----------------------------------------------------------
class Walkables:
    def __init__(self, zone_name):
        self.zone_name = zone_name
        self.init_pygame()
        self.loop_index = 0
        # self.walkables = self.read_data()
        self.walkables = None
        # if self.walkables is None:
        #     raise ValueError("Doh!")

    def read_data(self):
        filepath = os.path.join("data", "zones", self.zone_name, "map.txt")
        # filepath = os.path.join("data", constants.MAPFILE)
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles]
        # ------------------------------------------------------------------
        big_list = []
        for col, tiles in enumerate(mytiles):
            for row, tile in enumerate(tiles):
                if tile in ['.', 'p', 'c']:
                    # print("grass")
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "grass"
                    mywalk = Walkable(mydict)
                    # mygrass.debug_print()
                    big_list.append(mywalk)
                    # print("row: {}, col: {}".format(row, col))
                elif tile in ["d", "e"]:
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "dirt"
                    mywalk = Walkable(mydict)
                    big_list.append(mywalk)
        self.walkables = big_list

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def update_classes(self, all_sprites):
        for elem in self.walkables:
            all_sprites.add(elem)
        return all_sprites

    def __len__(self):
        return len(self.walkables)

    def __getitem__(self, item):
        return self.walkables[item]

    def __next__(self):
        if self.loop_index >= len(self.walkables):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.walkables[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

    def debug_print(self):
        print("Number of grasses: {}".format(len(self.walkables)))
        if len(self.walkables) == 0:
            s = "Error! There are no grasses to print."
            raise ValueError(s)
        for grass in self.walkables:
            grass.debug_print()

# -----------------------------------------------------------
#                      class Obstacle
# -----------------------------------------------------------
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, mydict):
        super().__init__()
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.kind = mydict["kind"]
        filepath = ""
        if self.kind == "forest":
            filepath = os.path.join("data", "images", constants.FOREST_IMG)
        elif self.kind == "wall":
            filepath = os.path.join("data", "images", constants.WALL_IMG)
        else:
            raise ValueError("Error! I don't recognize this: {}".format(self.kind))
        # ----
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def debug_print(self):
        print("(x,y): {},{}; kind:{}".format(self.x, self.y, self.kind))

# -----------------------------------------------------------
#                      class Obstacles
# -----------------------------------------------------------
class Obstacles:
    def __init__(self, zone_name):
        self.zone_name = zone_name
        self.init_pygame()
        self.obstacles = []
        self.loop_index = 0

    def read_data(self):
        filepath = os.path.join("data", "zones", self.zone_name, "map.txt")
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles]
        # ------------------------------------------------------------------
        self.obstacles = []
        for col, tiles in enumerate(mytiles):
            for row, tile in enumerate(tiles):
                # print("row: {}, tile: {}".format(row, tile))
                if tile == 'm':
                    # print("walls")
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "forest"
                    my_obstacle = Obstacle(mydict)
                    self.obstacles.append(my_obstacle)
                    # print("row: {}, col: {}".format(row, col))
                elif tile == 'w':
                    mydict = {}
                    mydict["x"] = row
                    mydict["y"] = col
                    mydict["kind"] = "wall"
                    my_obstacle = Obstacle(mydict)
                    self.obstacles.append(my_obstacle)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def update_classes(self, all_sprites):
        for elem in self.obstacles:
            all_sprites.add(elem)
        return all_sprites

    def __len__(self):
        return len(self.obstacles)

    def __getitem__(self, item):
        return self.obstacles[item]

    def __next__(self):
        if self.loop_index >= len(self.obstacles):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.obstacles[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

    def debug_print(self):
        for elem in self.obstacles:
            elem.debug_print()

# -----------------------------------------------------------
#                      class Environment
# -----------------------------------------------------------

class Enviornment:
    def __init__(self, zone_name):
        if not zone_name in constants.ZONE_NAMES:
            s = "Error! This isn't a valid zone name: {}\n".format(zone_name)
            s += "Here are the valid zone names: {}".format(constants.ZONE_NAMES)
            raise ValueError(s)
        # ----
        self.init_pygame()
        # ----
        self.zone_name = zone_name
        self.zone_description = ""
        self.obstacles = Obstacles(self.zone_name)
        self.walkables = Walkables(self.zone_name)
        # ----
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping = True

    def read_data(self):
        filepath = os.path.join("data", "zones", self.zone_name, "zone_init.txt")
        mylist = utils.read_data_file(filepath, 4)
        mydict = mylist[0]
        self.zone_description = mydict["zone_description"]
        self.obstacles.read_data()
        self.walkables.read_data()

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
                # else:
                #     print("I don't recognize this event.key in handle_events: {}".format(event.key))

    def update_classes(self, all_sprites):
        all_sprites = self.obstacles.update_classes(all_sprites)
        all_sprites = self.walkables.update_classes(all_sprites)
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
        self.obstacles.debug_print()
        self.walkables.debug_print()

# *********************************************************
# *********************************************************

if __name__ == "__main__":
    zone_name = "swindon"
    myenvironment = Enviornment(zone_name)
    myenvironment.read_data()
    myenvironment.main()
    # myenvironment.debug_print()
