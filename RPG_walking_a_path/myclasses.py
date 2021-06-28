import pygame
import constants
import utils
from graphics_environment import Enviornment
from shutil import copyfile
import os, sys
import math, time
from graphics_fauna import Player, Monsters, Npcs, Fauna
from dialogs import DialogFight, TextDialog
# from dialogs import DialogFight, TextDialog, DialogMerchant, \
#     DialogPlayerInventory, DialogPlayerCommands, DialogPlayerData
# from inventory_classes import Inventory
# -----------------------------------------------------------
#                      class Game
# -----------------------------------------------------------
class Game:
    def __init__(self, zone_name):
        # self.npcs_to_load = npcs_to_load
        # ----
        self.init_pygame()
        self.zone_name = zone_name
        self.environment = Enviornment(self.zone_name)
        self.fauna = Fauna(self.zone_name)
        # ----
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        # -------------------------------------
        self.keep_looping = True
        self.current_monster = None
        # -------------------------------------

    def reset_data_files(self):
        self.environment.read_data()
        self.fauna.read_data()
        # ----
        user_data = utils.get_user_data()
        # source_file = os.path.join("data", constants.MONSTERS_ORIGINAL_DATA_FILE)
        # destination_file = os.path.join("data", user_data["character_name"], constants.MONSTERS_DATA_FILE)
        # copyfile(source_file, destination_file)
        # ---- copy original file to player's directory ---
        source_file = os.path.join("data", constants.PLAYER_ORIGINAL_DATA_FILE)
        destination_file = os.path.join("data", user_data["character_name"], constants.PLAYER_DATA_FILE)
        copyfile(source_file, destination_file)
        # ---- ----
        self.all_sprites = pygame.sprite.Group()

    def read_data(self):
        self.environment.read_data()
        self.fauna.read_data()
        self.player.read_data_first()
        # self.monsters.read_data()
        # ----
        # self.walkables.read_data()
        # self.obstacles.read_data()
        # self.npcs.read_data()

    def player_died(self):
        s = "You're dead! Game over."
        mydialog = TextDialog(s)
        mydialog.main()
        self.init_pygame()
        self.keep_looping = False
        # pygame.quit()
        # sys.exit()

    def restart_game(self):
        player_x = self.player.x
        player_y = self.player.y
        # ----
        self.init_pygame()
        self.keep_looping = True
        self.environment = Enviornment(self.zone_name)
        self.fauna = Fauna(self.zone_name)
        self.player = Player()
        self.fight = False
        # ----
        self.player.read_data_restart(player_x, player_y)
        self.environment.read_data()
        self.fauna.read_data()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    # def get_monster(self, x, y):
    #     self.monsters.get_monster(x, y)

    def there_is_a_monster_on_this_tile(self, x, y):
        this_monster = self.fauna.monsters.get_monster(x, y)
        if this_monster is None: return False
        return True

    def there_is_an_npc_on_this_tile(self, x, y):
        this_npc = self.fauna.merchants.get_npc(x, y)
        if this_npc is None: return False
        return True

    def move_to(self, x, y):
        present_coords = (self.player.x, self.player.y)
        end_coords = (x, y)
        possibilities = [[(x-1), (y-1)], [(x-1), (y)], [(x-1), (y+1)], [(x), (y-1)], [(x), (y)], [(x), (y+1)], [(x+1), (y-1)], [(x+1), (y)], [(x+1), (y+1)]]
        distance = -1
        chosen_vector = None
        for a_coord_pair in possibilities:
            temp = utils.distance_between_two_points(a_coord_pair, end_coords)
            if temp < distance:
                distance = temp
                chosen_vector = a_coord_pair
        self.player.move_to(chosen_vector)

    def dialog_have_a_fight(self):
        fight_dialog = DialogFight(self.player, self.current_monster)
        fight_dialog.main()
        # message = fight_dialog.main()
        # ----
        print("in myclasses in dialog_have_a_fight. monster.hit_points: {}".format(self.current_monster.hit_points))

    def monster_encounter(self):
        self.current_monster = self.fauna.monsters.get_monster(self.player.x, self.player.y)
        if self.current_monster is None:
            raise ValueError("Error! Current_monster shouldn't be None.")
        if self.current_monster.is_dead() == True:
            return False
        # ----
        print("Fight!!!")
        self.dialog_have_a_fight()
        if self.current_monster.is_dead() == True:
            print("Monster is dead")
            self.save_data()
            self.restart_game()
            self.current_monster.image = self.current_monster.image_dead_monster
            return ""
        if self.player.is_dead() == True:
            print("Player is dead")
            self.player_died()
            self.save_data()
            # self.restart_game()
            self.player.image = self.player.image_dead
            # self.goodbye()
            return ""
        self.save_data()
        self.init_pygame()
        self.restart_game()

    def npc_encounter(self):
        current_npc = self.fauna.merchants.get_npc(self.player.x, self.player.y)
        if current_npc is None:
            raise ValueError("Error! There should be an NPC here, but there isn't.")
        if current_npc.character_kind == "bystander":
            # Bystanders are people who fill up the town but who do not have a specific function.
            mydialog = TextDialog("Nothing to see here, move along.")
            mydialog.main()
            self.init_pygame()
        elif current_npc.character_kind == "merchant":
            mydialog = DialogMerchant(self.player, current_npc)
            mydialog.main()
            self.player.save_data()
            self.restart_game()
        else:
            s = "I don't recognize this: {}".format(current_npc.kind)
            raise ValueError(s)

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
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.image = self.player.image_left
                    self.player.move(dx=-1, dy=0, obstacles=self.environment.obstacles)
                    self.player.direction = constants.LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.image = self.player.image_right
                    self.player.move(dx=1, obstacles=self.environment.obstacles)
                    self.player.direction = constants.RIGHT
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.image = self.player.image_down
                    self.player.move(dy=1, obstacles=self.environment.obstacles)
                    self.player.direction = constants.DOWN
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.image = self.player.image_up
                    self.player.move(dy=-1, obstacles=self.environment.obstacles)
                    self.player.direction = constants.UP
                elif event.key == pygame.K_h: # <=================================================
                    if self.there_is_a_monster_on_this_tile(self.player.x, self.player.y) == True:
                        self.monster_encounter()
                    elif self.there_is_an_npc_on_this_tile(self.player.x, self.player.y) == True:
                        self.npc_encounter()
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print("===========")
                print("This is the position of the mouse: {}".format(pos))
                print("This is the position of the player: {}".format(self.player.get_position()))
                print("--------")
                myint_x = math.floor(pos[0]/constants.TILESIZE)
                myint_y = math.floor(pos[1]/constants.TILESIZE)
                print("These are the x,y coords of the mouse: {},{}".format(myint_x, myint_y))
                print("These are the x,y coords of the plyaer: {},{}".format(self.player.x, self.player.y))
                print("===========")

    def update_classes(self):
        self.all_sprites = self.environment.update_classes(self.all_sprites)
        self.all_sprites = self.fauna.update_classes(self.all_sprites)
        self.all_sprites.add(self.player)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes()
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self, move_player_to_x, move_player_to_y):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            time.sleep(0.5)
            self.handle_events()
            self.draw()
            self.player.move_toward(move_player_to_x, move_player_to_y, self.environment.obstacles)
        self.goodbye()
        self.myquit()

    def save_data(self):
        # self.monsters.save_data()
        self.player.save_data()

    def myquit(self):
        pygame.quit()
        # sys.exit()

    def goodbye(self):
        mylist = []
        mylist.append("Thank you for playing")
        mylist.append("{}".format(constants.TITLE))
        mydialog = TextDialog(mylist)
        mydialog.main()

# -----------------------------------------------------------
#                      class DebugDriver
# -----------------------------------------------------------

class DebugDriver:
    def __init__(self, zone_name):
        self.init_pygame()
        self.environment = Enviornment(zone_name)
        self.fauna = Fauna(zone_name)
        self.keep_looping = True
        self.all_sprites = pygame.sprite.Group()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def read_data(self):
        self.environment.read_data()
        self.fauna.read_data()

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

    def update_classes(self):
        self.all_sprites = self.environment.update_classes(self.all_sprites)
        self.all_sprites = self.fauna.update_classes(self.all_sprites)
        # for elem in self.environment:
        #     self.all_sprites.add(elem)
        # for elem in self.obstacles:
        #     self.all_sprites.add(elem)
        # for elem in self.monsters:
        #     self.all_sprites.add(elem)
        # # print("number of npcs: {}".format(len(self.npcs)))
        # for elem in self.npcs:
        #     self.all_sprites.add(elem)
        # # self.all_sprites.add(self.monster)
        # self.all_sprites.add(self.player)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes()
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

# **************************************************
# **************************************************

if __name__ == "__main__":
    zone_name = "env01"
    # mydriver = DebugDriver(zone_name)
    mydriver = Game(zone_name)
    mydriver.read_data()
    mydriver.main()
