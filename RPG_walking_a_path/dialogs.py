import pygame
import constants
import random
import utils
# from inventory_classes import Inventory
from shutil import copyfile
import os, sys

# ------------------------------------------------------------
#                    class DialogMerchant
# ------------------------------------------------------------

class DialogPlayerData:
    def __init__(self, player, height=900, width=500, line_width=50):
        self.width = width
        self.height = height
        # --------------------------------------
        self.init_pygame()
        # --------------------------------------
        self.player = player
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text_color = constants.ORANGE
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        # --------------------------------------
        # <Player Name> the <Species>
        # --------------------------------------
        self.display_list = []
        self.display_list.append("{} the {}".format(self.player.name, self.player.kind))
        self.display_list.append(" ")
        self.display_list += self.player.display_list()
        # --------------------------------------
        self._initialize_rectangles()
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        a_constant = 4
        self.player.resize(constants.TILESIZE * a_constant, 0, 0)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 60
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        pygame.draw.rect(self.screen, constants.LIGHTGREY, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        mytext_rect = pygame.Rect(left, top+45, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def update_classes(self):
        self.all_sprites.add(self.player)
        # -----------------------------------------

    def draw(self):
        self.update_classes()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20, height_offset=275, line_length=60,
                          color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("Return = Exit")
        mylist.append("ESC = Exit")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=750, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()

# ------------------------------------------------------------
#               class DialogDisplayConsumable
# ------------------------------------------------------------

class DialogDisplayConsumable:
    def __init__(self, player, consumable_name, height=400, width=500, line_width=50):
        self.width = width
        self.height = height
        # --------------------------------------
        self.init_pygame()
        # --------------------------------------
        self.player = player
        self.consumable_name = consumable_name
        self.consumable = self.player.inventory.get_item_by_name(consumable_name)
        # self.consumable.debug_print()
        # raise NotImplemented
        # --------------------------------------
        # title, length = utils.format_string("debugging in DialogPlayerInventory.__init__")
        # print(title)
        # self.player.inventory.debug_print()
        # print("-" * length)
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text_color = constants.ORANGE
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        # self._initialize_rectangles()
        # --------------------------------------
        mylist = []
        mylist.append("{} the {}".format(self.player.name, self.player.kind))
        mylist.append(" ")
        # mylist = mylist + self.merchant.inventory.display_string()
        # self.npc_goods = self.player.inventory.display_string()
        # self.npc_goods_display = mylist + utils.format_npc_goods(self.npc_goods)
        # self.number_range = utils.get_number_range(self.npc_goods)
        # --------------------------------------
        self._initialize_rectangles()
        # --------------------------------------
        # self.mouse_pos = None
        self.keep_looping = True
        # self.message = ""
        self.return_value = []
        # --------------------------------------
        a_constant = 4
        # self.player.resize(constants.TILESIZE * a_constant, 0, 0)
        # self.merchant.resize(constants.TILESIZE * a_constant, constants.NUMBER_OF_BLOCKS_WIDE - a_constant - 1, 0)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 60
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def process_text(self, myint):
        pass
        # print("this_good: {}".format(this_good))
        # raise NotImplemented

        # if not self.text in constants.COMMANDS:
        #     raise ValueError("Error")
        # if self.text == "rpi":
        #     pass
        # elif self.text == "rp":
        #     pass
        # else:
        #     raise ValueError("Error")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.keep_looping = False
                    # if not utils.is_int(self.user_text):
                    #     raise ValueError("Error!")
                    # myint = int(self.user_text)
                    # if not myint in self.number_range:
                    #     self.user_text = ""
                    # else:
                    #     self.text = self.user_text
                    #     # self.process_text(myint)
                    #     self.return_value = self.npc_goods[myint - 1]
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        pygame.draw.rect(self.screen, constants.LIGHTGREY, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        mytext_rect = pygame.Rect(left, top + 45, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    # def update_classes(self):
    #     self.all_sprites.add(self.player)
        # -----------------------------------------

    def draw(self):
        # self.update_classes()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        # mylist = []
        # mylist.append("{} the {} | {}".format(self.player.name, self.player.kind, self.player.profession))
        # # self.player.debug_print()
        # mylist.append(" ")
        # # mylist.append("{}".format(self.merchant.inventory.display_string()))
        utils.talk_dialog(self.screen, self.consumable.get_list(), self.font, width_offset=20, height_offset=50,
                          line_length=60,
                          color=constants.BLACK)
        # ----
        # mylist = self.player.inventory.display_string()
        # # print("&&&&&&&&&&&&&&&&&&&&&&")
        # # [print(i) for i in mylist]
        # # print("&&&&&&&&&&&&&&&&&&&&&&")
        # mylist.append("gold: {}".format(self.player.gold))
        # utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=300, line_length=60,
        #                   color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("Return = Exit")
        mylist.append("ESC = Exit")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=750, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    # def save_data(self):
    #     # self.player.debug_print()
    #     self.player.save_data()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.save_data()
        # return self.text
        return self.return_value

# ------------------------------------------------------------
#                    class DialogLobby
# ------------------------------------------------------------

class DialogLobby:
    """
    This is what starts up at the very beginning.
    Will let the programmer reload the player from scratch, etc.
    Later I would like to have commands that allow the programmer to
    change practically any stat, change any inventory item, gives the player
    more gold, and so on.
    """
    def __init__(self, choices, height=500, width=750, line_width=50):
        self.choices = choices
        self.line_width = line_width
        self.width = width
        self.height = height
        # ---------------------------
        self.mytextlist = ["Welcome to {}!".format(constants.TITLE)]
        self.mytextlist.append(" ")
        self.mytextlist.append("To play the game, press 'g'.")
        self.mytextlist.append("To create a player, press 'p'.")
        self.mytextlist.append("To alter your playing character, press 'c'.")
        self.mytextlist.append("To quit, press 'q'.")
        # ---------------------------
        self.init_pygame()
        # ---------------------------
        self.user_text = ""
        self.keep_looping = True
        self.return_message = ""
        # ---------------------------
        self.BG_COLOR = constants.BLACK
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.LIGHTGREY
        self.text_color = constants.BLACK
        # ---------------------------
        self._initialize_rectangles()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        # print("width: {}, height: {}".format(self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        top_rectangle_left = 10
        top_rectangle_top = 10
        top_rectangle_width = self.width - 20
        top_rectangle_height = self.height - (20 * 6)
        self.window_background_rect = pygame.Rect(top_rectangle_left,
                                                  top_rectangle_top,
                                                  top_rectangle_width,
                                                  top_rectangle_height)
        # ----------------------
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 100
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)
        # ----------------------

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.user_text_rect_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.return_message = "q"
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    mytext = self.user_text.lower().strip()
                    if not mytext in self.choices:
                        self.user_text_rect_background_color = constants.RED
                        self.user_text = ""
                        return False
                    self.user_text = ""
                    if mytext == "g":
                        self.keep_looping = False
                        self.return_message = "g"
                    elif mytext == "c":
                        mydialog = DialogPlayerCommands()
                        mydialog.main()
                        self.keep_looping = False
                        self.return_message = "c"
                    elif mytext == "p":
                        mydialog = DialogCreatePlayer()
                        mydialog.main()
                        self.return_message = "p"
                        self.keep_looping = False
                    elif mytext == "q" or mytext == "quit":
                        self.keep_looping = False
                        self.return_message = "q"
                    else:
                        raise ValueError("Error!")
                else:
                    self.user_text += event.unicode

    def _draw_big_window(self):
        pygame.draw.rect(self.screen, self.big_window_background_color, self.window_background_rect)
        utils.talk_dialog(self.screen, self.mytextlist, self.font, width_offset=12, height_offset=12, line_length=50)

    def _draw_user_input_window(self):
        pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        utils.talk_dialog(self.screen, [self.user_text], self.font, width_offset=14, height_offset=400)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self._draw_big_window()
        self._draw_user_input_window()
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.events()
            self.draw()
        if not self.return_message in self.choices:
            raise ValueError("Error! This was entered: {}".format(self.return_message))
        return self.return_message

# ------------------------------------------------------------
#                    class DialogPlayerCommands
# ------------------------------------------------------------

class DialogPlayerCommands:
    """
    This is going to be useful mainly for debugging. It lets the player
    change practically any stat, change their inventory, gives themselves
    more gold, and so on.
    """
    def __init__(self, height=700, line_width=50):
        # self.possible_responses = possible_responses
        self.height = height
        self.width = 750
        self.line_width = line_width
        # ---------------------------
        self.init_pygame()
        # ---------------------------
        # pygame.init()
        self.keep_looping = True
        self.text_background_color = constants.LIGHTGREY
        # ---------------------------
        # self.clock = pygame.time.Clock()
        # self.font = pygame.font.SysFont('Comic Sans', 30)
        # myfont = pygame.font.SysFont('Comic Sans MS', 30)
        # text_width, _ = self.font.size("a")
        # self.width = self.line_width * text_width
        # self.screen = pygame.display.set_mode((self.width, self.height))
        # ---------------------------
        self.user_text = ""
        self.window_text_list = []
        self.keep_looping = True
        self.mouse_pos = None
        self.mouse_pressed = None
        # ---------------------------
        self.BG_COLOR = constants.BLACK
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        # ---------------------------
        self.mytextlist = []
        filepath = os.path.join("data", constants.PLAYER_COMMANDS)
        with open(filepath, "r") as f:
            self.mytextlist = f.readlines()
            self.mytextlist = [i.strip() for i in self.mytextlist if len(i.strip()) > 0]
        # ---------------------------
        self._initialize_rectangles()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        top_rectangle_left = 10
        top_rectangle_top = 10
        top_rectangle_width = self.width - 20
        top_rectangle_height = self.height - (20 * 6)
        self.window_background_rect = pygame.Rect(top_rectangle_left,
                                                  top_rectangle_top,
                                                  top_rectangle_width,
                                                  top_rectangle_height)
        # ----------------------
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 100
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)
        # ----------------------

    # def separate_text_into_lines(self, mytext, line_length):
    #     mylist = []
    #     while len(mytext) >= line_length:
    #         myint = mytext[0:line_length].rfind(" ")
    #         mylist.append(mytext[0:myint].strip())
    #         mytext = mytext[myint:].strip()
    #     mylist.append(mytext)
    #     return mylist

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.text_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    mytext = self.user_text.lower().strip()
                    if mytext == "rp":
                        print("Resetting player")
                        utils.copy_original_player_files()
                        self.keep_looping = False
                    elif mytext == "rpi":
                        print("Resetting player's inventory files")
                        utils.copy_original_player_inventory_files()
                        self.keep_looping = False
                    elif mytext == "rm": # reset monsters
                        print("Resetting monsters")
                        utils.copy_original_monster_files()
                        self.keep_looping = False
                    elif mytext == "ra":
                        print("Resetting all (player and monsters)")
                        utils.copy_original_player_files() # player
                        utils.copy_original_monster_files() # monsters
                        self.keep_looping = False
                else:
                    self.user_text += event.unicode

    def _draw_big_window(self):
        pygame.draw.rect(self.screen, self.big_window_background_color, self.window_background_rect)
        utils.talk_dialog(self.screen, self.mytextlist, self.font, width_offset=15, height_offset=12, line_length=40)
        # # -----------------------------
        # # ---- Draw text in big window
        # for count, elem in enumerate(self.window_text_list):
        #     text_width, text_height = self.font.size(elem)
        #     surface = self.font.render(elem, True, (0, 0, 0))
        #     # ----------------------
        #     left = 20
        #     top = (text_height * count) + 20
        #     self.screen.blit(surface, (left, top))

    def _draw_user_input_window(self):
        pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        mytext_rect = pygame.Rect(left, top, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self._draw_big_window()
        self._draw_user_input_window()
        pygame.display.flip()

    def main(self):
        self.user_text = ""
        self.clock.tick(20)
        while self.keep_looping:
            self.events()
            self.draw()
        return self.user_text

# ------------------------------------------------------------
#                    class InputDialog
# ------------------------------------------------------------

class InputDialog:
    def __init__(self, height=400, line_width=50):
        self.height = height
        self.line_width = line_width
        # ---------------------------
        pygame.init()
        self.keep_looping = True
        # ---------------------------
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 35)
        text_width, _ = self.font.size("a")
        self.width = self.line_width * text_width
        self.screen = pygame.display.set_mode((self.width, self.height))
        # ---------------------------
        self.user_text = ""
        self.window_text_list = []
        self.keep_looping = True
        self.mouse_pos = None
        self.mouse_pressed = None
        # ---------------------------
        self.BG_COLOR = constants.BLACK
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        # ---------------------------
        self._initialize_rectangles()

    def separate_text_into_lines(self, mytext, line_length):
        mylist = []
        while len(mytext) >= line_length:
            myint = mytext[0:line_length].rfind(" ")
            mylist.append(mytext[0:myint].strip())
            mytext = mytext[myint:].strip()
        mylist.append(mytext)
        return mylist

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.keep_looping = False
                else:
                    self.user_text += event.unicode

    def _initialize_rectangles(self):
        top_rectangle_left = 10
        top_rectangle_top = 10
        top_rectangle_width = self.width - 20
        top_rectangle_height = self.height - (20 * 6)
        self.window_background_rect = pygame.Rect(top_rectangle_left,
                                                  top_rectangle_top,
                                                  top_rectangle_width,
                                                  top_rectangle_height)
        # ----------------------
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 100
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)
        # ----------------------

    def _draw_big_window(self):
        pygame.draw.rect(self.screen, self.big_window_background_color, self.window_background_rect)
        # -----------------------------
        # ---- Draw text in big window
        for count, elem in enumerate(self.window_text_list):
            text_width, text_height = self.font.size(elem)
            surface = self.font.render(elem, True, (0, 0, 0))
            # ----------------------
            left = 20
            top = (text_height * count) + 20
            self.screen.blit(surface, (left, top))

    def _draw_user_input_window(self):
        pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        mytext_rect = pygame.Rect(left, top, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self._draw_big_window()
        self._draw_user_input_window()
        pygame.display.flip()

    def main(self, text):
        self.user_text = ""
        self.window_text_list = self.separate_text_into_lines(
            text, self.line_width)
        while self.keep_looping:
            self.clock.tick(20)
            self.events()
            self.draw()
        return self.user_text

# ------------------------------------------------------------
#                    class TextDialog
# ------------------------------------------------------------

class TextDialog:
    def __init__(self, text, line_width=50):
        self.BG_COLOR = constants.LIGHTGREY
        self.text_list = []
        if type(text) == type("abc"):
            self.text_list = utils.separate_text_into_lines(text, line_width)
        elif type(text) == type([]):
            for elem in text:
                temp = utils.separate_text_into_lines(elem, line_length=100)
                for line in temp:
                    self.text_list.append(line)
                # self.text_list.append(temp)
        else:
            s = "Doh! That type of data shouldn't be here!"
            raise ValueError(s)
        # -------------------------
        if len(self.text_list) > 12:
            s = "Error! Textbox should not contain more than 12 lines."
            raise ValueError(s)
        # -------------------------
        pygame.init()
        self.font = pygame.font.Font(None, 35)
        # -------------------------
        text_width, text_height = self.font.size("a")
        self.width = 50 * text_width
        self.height = 400
        kind = ""
        self.screen = pygame.display.set_mode((self.width, self.height))
        # ----
        self.line_height = -1
        for elem in self.text_list:
            try:
                text_width, text_height = self.font.size(elem)
            except:
                try:
                    text_width, text_height = self.font.size(elem[0])
                except:
                    raise ValueError("Error!")
            if text_height > self.line_height:
                self.line_height = text_height
        # -------------------------
        # ----- Text Window -------
        window_left = 10
        window_top = 10
        window_width = self.width - 20
        window_height = self.height - (20 * 3)
        self.window_rect = pygame.Rect(window_left, window_top, window_width, window_height)
        # --------------------------
        # -------- OK Button -------
        button_width = 60
        button_height = 35
        button_left = int(self.height / 2)
        top = 600 - button_height
        print("width: ", button_width)
        self.okay_rect = pygame.Rect(button_left, top, button_width, button_height)
        # else:
        #     raise ValueError("I don't recognize that: ", kind)
        # -------------------------
        self.mouse_pos = None
        self.keep_looping = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                if event.key == pygame.K_RETURN:
                    self.keep_looping = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()
                elif mouse_pressed[2] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()

    def _draw_lines(self):
        # karen
        for count, elem in enumerate(self.text_list):
            try:
                surface = self.font.render(elem, True, (0, 0, 0))
            except:
                try:
                    surface = self.font.render(elem[0], True, (0, 0, 0))
                except:
                    raise ValueError("Error!")
            # ----------------------
            left = 20
            top = (self.line_height * count) + 20
            # ----------------------
            self.screen.blit(surface, (left, top), area=None)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # ----------------------
        pygame.draw.rect(self.screen, constants.WHITE, self.window_rect)
        # ----------------------
        pygame.draw.rect(self.screen, constants.PURPLE, self.okay_rect)
        # ----------------------
        self._draw_lines()
        # ---- Render the text used to label the button. ----
        surface = self.font.render("OK", True, constants.BLACK)
        self.screen.blit(surface, self.okay_rect)
        # --------------------------------------------------
        if not self.mouse_pos == None:
            okay_result = self.okay_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])
            self.mouse_pos = None
            if okay_result == 1:
                self.message = ""
                self.keep_looping = False
        # --------------------------------------------------
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.events()
            self.draw()


# ------------------------------------------------------------
#                    class DialogFight
# ------------------------------------------------------------

class DialogFight:
    """Takes the player and a monster and lets them fight."""
    def __init__(self, player, monster, width=768, height=768):
        self.width = width
        self.height = height
        self.player = player
        self.monster = monster
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.init_pygame()
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text = ""
        self.input_text_color = constants.ORANGE
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        multiplier = 4
        self.player.resize(constants.TILESIZE * multiplier, 0, 0)
        self.monster.resize(constants.TILESIZE * multiplier, constants.NUMBER_OF_BLOCKS_WIDE-multiplier, 0)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_h:
                    myran = random.randint(0, 99)
                    if myran <= self.player.chance_to_hit:
                        self.monster.hit_points -= self.player.calculate_damage()
                    myran = random.randint(0, 99)
                    if myran <= self.monster.chance_to_hit:
                        self.player.hit_points -= self.monster.calculate_damage()
                    if self.monster.hit_points <= 0:
                        self.keep_looping = False
                    elif self.player.hit_points <= 0:
                        self.keep_looping = False
                else:
                    pass

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.monster)
        # -----------------------------------------
        monster_list = []
        monster_list.append("{} hit points:".format(self.monster.kind.capitalize()))
        monster_list.append("hp: {}".format(self.monster.hit_points))
        utils.talk_dialog(self.screen, monster_list, self.font, width_offset=475, height_offset=250, line_length=60,
                          color=constants.BLACK)
        # ----
        player_list = []
        player_list.append("Player hit points:")
        player_list.append("hp: {}".format(self.player.hit_points))
        utils.talk_dialog(self.screen, player_list, self.font, width_offset=20, height_offset=250, line_length=60,
                          color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("What would you like to do?")
        mylist.append("H = Hit")
        # mylist.append("X = Exit (Exiting will cost 2 hitpoints)")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=350, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def save_data(self):
        self.monster.save_data()
    #     self.player.save_data()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        self.save_data()
        # self.init_pygame()

# ------------------------------------------------------------
#                    class DialogMerchant
# ------------------------------------------------------------

class DialogMerchant:
    def __init__(self, player, merchant, height=700, width=800, line_width=50):
        self.player = player
        self.player.image = self.player.image_down
        if len(self.player.inventory) == 0:
            raise ValueError("Doh! The player has lost their inventory!")
        self.merchant = merchant
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text_color = constants.ORANGE
        self.text_background_color = constants.LIGHTGREY
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        self._initialize_rectangles()
        # --------------------------------------
        mylist = []
        mylist.append("{} the {}".format(self.merchant.character_name, self.merchant.character_kind))
        mylist.append(" ")
        # mylist = mylist + self.merchant.inventory.display_string()
        self.npc_goods = self.merchant.inventory.display_string()
        self.npc_goods_display = mylist + utils.format_npc_goods(self.npc_goods)
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        a_constant = 4
        self.player.resize(constants.TILESIZE * a_constant, 0, 0)
        self.merchant.resize(constants.TILESIZE * a_constant, constants.NUMBER_OF_BLOCKS_WIDE - a_constant - 1, 0)

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 100
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    # def separate_text_into_lines(self, mytext, line_length):
    #     mylist = []
    #     while len(mytext) >= line_length:
    #         myint = mytext[0:line_length].rfind(" ")
    #         mylist.append(mytext[0:myint].strip())
    #         mytext = mytext[myint:].strip()
    #     mylist.append(mytext)
    #     return mylist

    def process_order(self):
        print("This is what the user typed: {}".format(self.text))
        parsed_result = utils.parse_player_purchase(self.text)
        print("This is the parsed result: {}".format(parsed_result))
        # ----
        this_item = self.merchant.inventory.get_item_by_name(parsed_result[1])
        if this_item is None:
            raise ValueError("This shoudln't be happening!")
        if parsed_result[0] == "buy":
            print("parsed_result[2]: {}".format(parsed_result[2]))
            gold_required = this_item.cost * int(parsed_result[2])
            print("This is the gold_required: {}".format(gold_required))
            if type(gold_required) != type(123):
                raise ValueError("Error! This needs to be int: {}, it is of type {}.".format(gold_required, type(gold_required)))
            if (self.player.gold - gold_required) < 0:
                mydialog = TextDialog("Doh! You don't have eough money to buy that!")
                mydialog.main()
            else:
                self.player.gold -= gold_required
                s = "bought {} items of {} ({}|{}) for {} gold.".format(parsed_result[2], this_item.name, this_item.item_kind, this_item.species, gold_required)
                print(s)
                for _ in range(parsed_result[2]):
                    print("parsed_result: {}".format(parsed_result))
                    print("Adding {} ...".format(parsed_result[1]))
                    print("This is what is being passed off to inventory.add_item:")
                    print("first argument: {}; second argument: {}; third argument: {}".format(parsed_result[2], parsed_result[1], parsed_result[2]))
                    self.player.inventory.add_item(parsed_result[1])
                    print("Item ({}) added.".format(parsed_result[1]))
        elif parsed_result[0] == "sell":
            self.player.gold += this_item.cost * parsed_result[2]
            print("sold {} items of {} for {} gold.".format(parsed_result[2], this_item.name,
                                                            (this_item.cost * parsed_result[2])))
            if self.player.inventory.remove_item_by_name(this_item.name, parsed_result[2]) == False:
                self.text_background_color = constants.RED
        else:
            raise ValueError("Error! Could not understand this: {}".format(parsed_result[0]))
        # ----

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.text = self.user_text
                    if utils.order_valid(self.text):
                        self.text_background_color = constants.LIGHTGREY
                        self.process_order()
                        self.user_text = ""
                    else:
                        self.text_background_color = constants.RED
                        self.user_text = ""
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        mytext_rect = pygame.Rect(left, top, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def update_classes(self):
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.merchant)
        # -----------------------------------------

    def draw(self):
        self.update_classes()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        # mylist = []
        # mylist.append("{} the {}".format(self.merchant.character_name, self.merchant.character_kind))
        # mylist.append(" ")
        # mylist = mylist + self.merchant.inventory.display_string()
        # ----
        # print("dkdkd: ", self.merchant.inventory.display_string())
        # raise NotImplemented
        utils.talk_dialog(self.screen, self.npc_goods_display, self.font, width_offset=475, height_offset=250, line_length=60,
                          color=constants.BLACK)
        # ----
        player_list = []
        player_list.append("{} the {}".format(self.player.name, self.player.kind))
        player_list.append("Profession: {}".format(self.player.profession))
        player_list.append("gold: {}".format(self.player.gold))
        utils.talk_dialog(self.screen, player_list, self.font, width_offset=20, height_offset=250, line_length=60,
                          color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("b = Buy")
        mylist.append("s = Sell")
        mylist.append("ESC = Exit")
        mylist.append(" ")
        mylist.append("Examples:")
        mylist.append("b bread 2 --> Buys two bread items")
        mylist.append("s water 1 --> Sells one item of bread")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=350, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def save_data(self):
        # self.merchant.save_temp_data()
        self.player.save_data()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        self.player.debug_print()
        # print("akdf;aksjdf;kajsdfkjas;dfkja;sdlkfja;lsdkjf;lksdjflkdjf")
        self.save_data()
        return self.text

# ------------------------------------------------------------
#                    class DialogMerchant
# ------------------------------------------------------------

class DialogPlayerInventory:
    def __init__(self, player, height=900, width=500, line_width=50):
        self.width = width
        self.height = height
        # --------------------------------------
        self.init_pygame()
        # --------------------------------------
        self.player = player
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.user_text = ""
        self.text_color = constants.BLACK
        # --------------------------------------
        mylist = []
        mylist.append("{} the {}".format(self.player.name, self.player.kind))
        mylist.append("index | name | (cost) | hps | #")
        mylist.append(" ")
        self.npc_goods = self.player.inventory.display_string()
        self.npc_goods_display = mylist + utils.format_npc_goods(self.npc_goods)
        self.number_range = utils.get_number_range(self.npc_goods)
        # --------------------------------------
        self._initialize_rectangles()
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        a_constant = 4
        self.player.resize(constants.TILESIZE * a_constant, 0, 0)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 60
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if not utils.is_int(self.user_text):
                        raise ValueError("Error!")
                    myint = int(self.user_text)
                    if not myint in self.number_range:
                        self.user_text = ""
                    else:
                        mytext = self.npc_goods[myint - 1][1]
                        consumable_name = mytext.split(": ")
                        consumable_name = consumable_name[0].lower().strip()
                        mydialog = DialogDisplayConsumable(self.player, consumable_name)
                        mydialog.main()
                        self.init_pygame()
                        self.user_text = ""
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        pygame.draw.rect(self.screen, constants.LIGHTGREY, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        mytext_rect = pygame.Rect(left, top+45, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def update_classes(self):
        self.all_sprites.add(self.player)
        # -----------------------------------------

    def draw(self):
        self.update_classes()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        # mylist = []
        # mylist.append("{} the {} | {}".format(self.player.name, self.player.kind, self.player.profession))
        # # self.player.debug_print()
        # mylist.append(" ")
        # # mylist.append("{}".format(self.merchant.inventory.display_string()))
        utils.talk_dialog(self.screen, self.npc_goods_display, self.font, width_offset=20, height_offset=275, line_length=60,
                          color=constants.BLACK)
        # ----
        # mylist = self.player.inventory.display_string()
        # # print("&&&&&&&&&&&&&&&&&&&&&&")
        # # [print(i) for i in mylist]
        # # print("&&&&&&&&&&&&&&&&&&&&&&")
        # mylist.append("gold: {}".format(self.player.gold))
        # utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=300, line_length=60,
        #                   color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("Return = Exit")
        mylist.append("ESC = Exit")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=750, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    # def save_data(self):
    #     # self.player.debug_print()
    #     self.player.save_data()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.save_data()
        # return self.text
        # return self.return_value

# ============================================================

def init_pygame():
    pygame.init()
    pygame.display.set_caption("Enter {}".format(constants.TITLE))

def debug_DialogFight():
    from graphics_fauna import Player, Npc, Monsters
    myplayer = Player()
    myplayer.read_data_first()
    mymonsters = Monsters()
    mymonsters.read_data()
    mymonster = mymonsters.get_monster_by_name("Nether")
    # ----
    myplayer.read_data_first()
    mydialog = DialogFight(myplayer, mymonster)
    mydialog.main()

# ************************************************

def test_dialog_player_data():
    from graphics_fauna import Player, Npc
    myplayer = Player()
    myplayer.read_data_first()
    # ----
    name = "alvin"
    x = 4
    y = 4
    mylist = [name, x, y]
    mynpc = Npc(mylist)
    mynpc.read_data()
    # ----
    mydialog = DialogPlayerData(myplayer)
    mydialog.main()
    # mydialog = DialogDisplayConsumable(myplayer, "dry bread")
    # mydialog.main()
    # mydialog.main()
    # ----
    # mydialog = DialogPlayerInventory(myplayer)
    # mydialog.main()

def test_dialog_lobby():
    mydialog = DialogLobby(["g", "c", "q"])
    mydialog.main()

if __name__ == "__main__":
    test_dialog_lobby()