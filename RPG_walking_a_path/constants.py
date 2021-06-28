ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
TITLE = "The World of Light and Darkness"
# ----
NUMBER_OF_BLOCKS_WIDE = 12 #TODO: shouldn't this be determined by the mapfile?
NUMBER_OF_BLOCKS_HIGH = 12 #TODO: shouldn't this be determined by the mapfile?
# ----
CHAR_KINDS = ["warrior", "mage"]
# ----
TILESIZE = 64
SCREEN_WIDTH = TILESIZE * NUMBER_OF_BLOCKS_WIDE
SCREEN_HEIGHT = TILESIZE * NUMBER_OF_BLOCKS_HIGH
FRAME_RATE = 5
# ----
#INVENTORY_TYPES = ["fauna", "base"]
MERCHANT_NAMES = ["laura", "alvin"]
CHARACTER_KINDS = ["player", "merchant"]
INVENTORY_KINDS = ["beginner", "normal", "advanced", None]
CONSUMABLE_KINDS = ["food", "drink"]
CONSUMABLE_NAMES = ["dry roast", "dry bread", "tough jerky", "stale lembas", "soupy stew"]
CONSUMABLE_NAMES += ["stewy soup", "bitter water", "spoiled wine"]
FOOD_SPECIES = ["roast", "bread", "jerky", "lembas", "stew", "soup"]
DRINK_SPECIES = ["water", "wine"]
# DRINK_KIND = ["water", "wine"]
WEAPON_KINDS = ["sword", "longsword"]
WEAPON_NAMES = ["rusty sword", "normal sword", "rusty longsword"]
# SOMETHING_BUYABLE = FOOD_KIND + DRINK_KIND + WEAPON_KINDS
ITEM_KINDS = ["food", "drink", "weapon"]
CONSUMABLE_ITEMS = "consumable_items.txt"
CONSUMABLE_ITEMS_ORIGINAL = "consumable_items_original.txt"
# FONT_NAME = "Courier"
FONT_NAME = None
FONT_SIZE = 30
# ----
# NPCs in the various zones
# STARTING_ZONE_NPCS = ["laura"]
ZONE_NAMES = ["env01", "env02", "env03"]
# ---- COLORS ----
UP = 90
DOWN = -90
RIGHT = 0
LEFT = 180

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (55, 55, 255)
GREEN = (0, 200, 0)
DARKGREY = (150, 150, 150)
LIGHTGREY = (210, 210, 210)
UGLY_PINK = (255, 0, 255)
BROWN = (153, 76, 0)
GOLD = (153, 153, 0)
DARKGREEN = (0, 102, 0)
DARKORANGE = (255, 128, 0)
LIGHT_PURBLE = (255, 153, 255)
ORANGE = (255, 128, 0)
PURPLE = (128,  0, 128)
# ----
BG_COLOR = UGLY_PINK

# ---- FILES ----
MAPFILE = "map02.txt"
# MAPFILE = "map_grass_and_walls.txt"
TESTING_FILE = "testing01.txt"
TESTING_WEAPONS_FILE = "testing_weapons_file.txt"
TESTING_CONSUMABLES_FILE = "testing_consumables_file.txt"

NPCS = "npcs.txt"

# ---- ENVIRONMENT ----
GRASS_IMG = "grass02.gif"
FOREST_IMG = "medievalTile_48.png"
WALL_IMG = "brick_wall.png"
DIRT_IMG = "dirt01.png"
# MERCHANT = "merchant03b.png"
BYSTANDER_IMG = "bystander01.png"
BEGINNER_MERCHANT = "merchant03b.png"
ADVANCED_MERCHANT = "merchant04b.png"
# ---- PLAYER ----
PLAYER_ORIGINAL_DATA_FILE = "player_original_data_file.txt"
PLAYER_DATA_FILE = "player_data_file.txt"
PLAYER_IMG = "warrior03_down.png"
# PLAYER_IMG_UP = "dog_up.png"
# PLAYER_IMG_DOWN = "dog_down.png"
# PLAYER_IMG_RIGHT = "dog_right.png"
# PLAYER_IMG_LEFT = "dog_left.png"
# PLAYER_IMG_DEAD = "dog02_wounded05.png"
PLAYER_IMG_UP = "warrior03_up.png"
PLAYER_IMG_DOWN = "warrior03_down.png"
PLAYER_IMG_RIGHT = "warrior03_right.png"
PLAYER_IMG_LEFT = "warrior03_left.png"
PLAYER_IMG_DEAD = "skull_and_bones.png"
PLAYER_INVENTORY = "player_inventory.txt"
PLAYER_FOOD = "player_food.txt"
PLAYER_DRINK = "player_food.txt"
PLAYER_WEAPONS = "player_weapons.txt"
WEAPONS_FILE = "weapon_items.txt"
WEAPONS_FILE_ORIGINAL = "weapon_items_original.txt"
#---- INVENTORY ITEMS ----
# FOOD_ITEMS = "food.txt"
# DRINK_ITEMS = "drink.txt"
# WEAPON_ITEMS = "weapon.txt"
DIALOG_PLAYER_COMMANDS_CHOICES = ["g", "c"]
COMMANDS = ["rpi", "rp"]
PLAYER_COMMANDS = "player_commands.txt"

# ---- MONSTERS ----
MONSTERS_ORIGINAL_DATA_FILE = "monsters_original_data_file.txt"
MONSTERS_DATA_FILE = "monsters_data_file.txt"
MONSTERS_TEMP_FILE = "monster_temp_file.txt"
# MONSTER_IMG = "Giant Bat.png"
# MONSTER_IMG_DEAD = "giant_bat_dead.png"
# ---- NPCS ----
NPC_BEGINNER_MERCHANT_INVENTORY = "npc_beginner_merchant_inventory.txt"
NPC_NORMAL_MERCHANT_INVENTORY = "npc_normal_merchant_inventory.txt"
NPC_ADVANCED_MERCHANT_INVENTORY = "npc_advanced_merchant_inventory.txt"
# -------------
DISCRIPTION_01 = ['rusty', 'normal', 'dry', 'tough', 'stale', 'soupy', 'stewy', 'bitter', 'spoiled']
DISCRIPTION_02 = ['sword', 'longsword', 'roast', 'bread', 'jerky', 'lembas']
DISCRIPTION_02 += ['stew', 'soup', 'water', 'wine']