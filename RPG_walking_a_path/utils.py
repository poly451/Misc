import constants
import os, sys
from shutil import copyfile
import math

def is_int(mystring):
    try:
        temp = int(mystring)
        return True
    except:
        return False

def key_value(mystring, mydict):
    # print("mystring: {}".format(mystring))
    myint = mystring.find(":")
    if myint == -1:
        s = "Error! : was not found in mystring: {}".format(mystring)
        raise ValueError(s)
    tag = mystring[0:myint].strip()
    value = mystring[myint+1:].strip()
    if len(tag) == 0:
        raise ValueError("Error")
    if len(value) == 0:
        raise ValueError("Error")
    try:
        mydict[tag] = int(value) if is_int(value) else value
    except Exception as e:
        print("tag: {}; value: {}".format(tag, value))
        raise ValueError(e)
    return mydict

def copy_original_player_files():
    # copying over the player's data file
    source_file = os.path.join("data", "master_files", "player_original_data_file.txt")
    mydict = get_user_data()
    destination_file = os.path.join("data", mydict["character_name"], "player_data_file.txt")
    copyfile(source_file, destination_file)
    # ----
    source_file = os.path.join("data", "master_files", "weapon_items_original.txt")
    destination_file = os.path.join("data", mydict["character_name"], "weapon_items.txt")
    copyfile(source_file, destination_file)
    # ----
    source_file = os.path.join("data", "master_files", "consumable_items_original.txt")
    destination_file = os.path.join("data", mydict["character_name"], "consumable_items.txt")
    copyfile(source_file, destination_file)

def copy_original_player_inventory_files():
    # copying over the player's original inventory files
    mydict = get_user_data()
    source_file = os.path.join("data", "master_files", "weapon_items_original.txt")
    destination_file = os.path.join("data", mydict["character_name"], "weapon_items.txt")
    copyfile(source_file, destination_file)
    # ----
    source_file = os.path.join("data", "master_files", "consumable_items_original.txt")
    destination_file = os.path.join("data", mydict["character_name"], "consumable_items.txt")
    copyfile(source_file, destination_file)

def copy_original_monster_files():
    player_data = get_user_data()
    mysource = os.path.join("data", "master_files", "npcs", "monsters")
    myfiles = os.listdir(mysource)
    # ----
    mydestination = os.path.join("data", player_data["character_name"].lower(), "monsters")
    for a_file in myfiles:
        sf = os.path.join(mysource, a_file)
        df = os.path.join(mydestination, a_file)
        print("source_file: {}".format(sf))
        print("destination_file: {}".format(df))
        copyfile(sf, df)

def get_players_position_on_map():
    x, y = -1, -1
    filepath = os.path.join("data", constants.MAPFILE)
    with open(filepath, "r") as f:
        mytiles = f.readlines()
        mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
    for col, tiles in enumerate(mytiles):
        for row, tile in enumerate(tiles):
            if tile == 'p':
                x = row
                y = col
    return x, y

def read_data_file(filepath, num_of_fields):
    big_list = []
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    big_list = []
    for i in range(0, len(mylines), num_of_fields):
        mydict = {}
        for j in range(num_of_fields):
            elem = mylines[i + j]
            mydict = key_value(elem, mydict)
        big_list.append(mydict)
    return big_list

def convert_direction_to_integer(the_direction):
    if not the_direction.lower() in ["down", "up", "right", "left"]:
        raise ValueError("I don't recognize this: {}".format(the_direction))
    the_direction = the_direction.lower()
    myint = ""
    if the_direction == "up":
        myint = 90
    elif the_direction == "down":
        myint = -90
    elif the_direction == "right":
        myint = 0
    elif the_direction == "left":
        myint = 180
    else:
        s = "This was not found: {}".format(the_direction)
        raise ValueError(s)
    return myint

def convert_integer_to_direction(my_int):
    if type(my_int) != type(123):
        s = "Error! myint: {} ({})".format(my_int, type(my_int))
        raise ValueError(s)
    #----
    the_dir = ""
    if my_int == 90:
        the_dir = "UP"
    elif my_int == -90:
        the_dir = "DOWN"
    elif my_int == 0:
        the_dir = "RIGHT"
    elif my_int == 180:
        the_dir = "LEFT"
    else:
        raise ValueError("Error! I don't recognize this: {}".format(my_int))
    return the_dir

def get_player_position_from_map(filepath):
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    big_list = []
    for i, line in enumerate(mylines):
        for j, element in enumerate(line):
            # print(i, j, element)
            if element == "p":
                return j, i
    raise ValueError("Player not found!")

def separate_text_into_lines(mytext, line_length):
    mylist = []
    while len(mytext) >= line_length:
        int = mytext[0:line_length].rfind(" ")
        mylist.append(mytext[0:int].strip())
        mytext = mytext[int:].strip()
    mylist.append(mytext)
    return mylist

def _top_height(text_list, font):
    if not type(text_list) == type([]):
        raise ValueError("Error")
    tallest = -1
    for elem in text_list:
        try:
            _, text_height = font.size(elem)
        except:
            raise ValueError(elem)
        if text_height > tallest:
            tallest = text_height
    return tallest

def talk_dialog(screen, text, font, width_offset, height_offset, line_length=32, color=(0,0,0)):
    # text_list = separate_text_into_lines(text, line_length)
    text_list = []
    if type(text) == type("bla"):
        text_list = separate_text_into_lines(text, line_length)
    elif type(text) == type([]):
        for line in text:
            temp = separate_text_into_lines(line, line_length)
            text_list += temp
    else:
        s = "Doh! That type of data shouldn't be here!"
        raise ValueError(s)
    # ----------------------
    text_height = _top_height(text_list, font) + 3
    for count, elem in enumerate(text_list):
        surface = font.render(elem, True, color)
        # ----------------------
        left = width_offset
        height = height_offset + (text_height * count)
        top = height + 10
        screen.blit(surface, (left, top))

def get_user_data():
    filepath = os.path.join("data", "user_data.txt")
    with open(filepath, "r") as f:
        mylines = f.readlines()
    mydict = {}
    for a_line in mylines:
        mydict = key_value(a_line, mydict)
    return mydict

def order_valid(user_text):
    print("mystring: {}".format(user_text))
    mylist = user_text.split(" ")
    mylist = [i.lower().strip() for i in mylist if len(i.strip()) > 0]
    if len(mylist) != 4:
        s = "Looks like something went wrong. This needs to be FOUR terms, you entered {}. Here's what has been entered: {}".format(len(mylist), user_text)
        return False
    # ----
    if not mylist[0] in ["b", "s"]:
        print("Error! The first term needs to be either b or s. You entered: {}".format(mylist[0]))
        return False
    if not mylist[1] in constants.DISCRIPTION_01:
        print("Error! Your second term was: {}. It needs to be one of these: {}".format(mylist[1], constants.DISCRIPTION_01))
        return False
    if not mylist[2] in constants.DISCRIPTION_02:
        print("Error! Your second term was: {}. It needs to be one of these: {}".format(mylist[2], constants.DISCRIPTION_02))
        return False
    if not is_int(mylist[3]):
        print("Error! The number of items you desire to buy must be an integer.")
        return False
    return True

def parse_player_purchase(mystring):
    print("mystring: {}".format(mystring))
    mylist = mystring.split(" ")
    mylist = [i.lower().strip() for i in mylist if len(i.strip()) > 0]
    # if len(mylist) != 4:
    #     s = "Looks like something went wrong. This needs to be FOUR terms, you entered {}. Here's what has been entered: {}".format(len(mylist), mystring)
    #     raise ValueError(s)
    # # ----
    # if not mylist[0] in ["b", "s"]:
    #     raise ValueError("Error! The first term needs to be either b or s. You entered: {}".format(mylist[0]))
    # if not mylist[1] in constants.DISCRIPTION_01:
    #     raise ValueError("Error! Your second term was: {}. It needs to be one of these: {}".format(mylist[1], constants.DISCRIPTION_01))
    # if not mylist[2] in constants.DISCRIPTION_02:
    #     raise ValueError("Error! Your second term was: {}. It needs to be one of these: {}".format(mylist[2], constants.DISCRIPTION_02))
    # if not is_int(mylist[3]):
    #     raise ValueError("Error! The number of items you desire to buy must be an integer.")
    # ----------------------------------
    new_list = ["0", "0", "0"]
    if mylist[0] == "b":
        new_list[0] = "buy"
    else:
        new_list[0] = "sell"
    new_list[1] = "{} {}".format(mylist[1], mylist[2])
    if not new_list[1] in constants.CONSUMABLE_NAMES + constants.WEAPON_NAMES:
        raise ValueError("Error!")
    new_list[2] = int(mylist[3])
    return new_list

def format_string(string_title, my_divider="-", length=50):
    if length < len(string_title):
        raise ValueError("length ({}) < len(string_title) ({})".format(length, len(string_title)))
    new_length = int((length - len(string_title)) / 2)
    s = "{} {} {}".format(my_divider * new_length, string_title, my_divider * new_length)
    return s, len(s)

def get_merchant_inventory_data(merchant_name, kind):
    """
    Retrieves the inventory of a specific merchant.
    :param merchant_name: the name of the merchant
    :return: A list of dictionaries
    """
    filename = "{}.txt".format(merchant_name)
    filepath = os.path.join("data", "npcs", filename)
    with open(filepath, "r") as f:
        mylines = f.readlines()
        mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
    my_dictionaries = []
    inventory_list = []
    for a_line in mylines:
        this_line = a_line.split(":")
        if this_line[0] == "inventory":
            # print(a_line)
            myint = a_line.find("inventory:")
            myposition = myint + len("inventory:")
            new_line = a_line[myposition:].strip()
            # print(new_line)
            inventory_list.append(new_line)
    new_list = []
    for elem in inventory_list:
        mydict = {}
        # print(elem)
        mylist = elem.split(";")
        mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
        # print(mylist)
        # print(type(mylist[0]))
        mydict = {}
        for an_element in mylist:
            # mydict = {}
            # print("an_element: {}".format(an_element))
            mydict = key_value(an_element, mydict)
            # mydict = key_value(an_element, mydict)
            # print("mydict: {}".format(mydict))
            # print("---------")
        new_list.append(mydict)
    big_list = []
    for a_dict in new_list:
        if a_dict["kind"] == kind:
            big_list.append(a_dict)
        # print(a_dict)
    # print("at the end", new_list)
        # print(new_list[0]["kind"])
    return big_list

# def display_inventory():
#     consumables = []
#     consumables.append(("consumable_01", 2))
#     consumables.append(("consumable_02", 9))
#     consumables.append(("consumable_03", 4))
#     weapons = []
#     weapons.append(("weapon_01", 1))
#     weapons.append(("weapon_02", 2))
#     weapons.append(("weapon_03", 5))
#     ret_list = consumables + weapons
#     return ret_list

def _pad_string(mystring, desired_length):
    s = mystring
    if len(s) < desired_length:
        while len(s) < desired_length:
            s += "-"
    elif len(s) > desired_length:
        s = s[0:desired_length]
    return s

# def _get_spaces(number_of_spaces):
#     s = ""
#     for i in range(number_of_spaces):
#         s += " "
#     return s

def format_npc_goods(npc_goods):
    mylist = []
    for elem in npc_goods:
        s = "{}) {}".format(elem[0], elem[1])
        mylist.append(s)
    return mylist

def format_inventory_list(mylist):
    new_list = []
    for count, elem in enumerate(mylist):
        s = "{}: ({}) {} - {}".format(elem[0], elem[2], elem[3], elem[1])
        new_list.append([count+1, s])
    return new_list

def get_number_range(npc_goods):
    mylist = []
    for elem in npc_goods:
        mylist.append(elem[0])
    return mylist

def distance_between_two_points(A, B):
    dA = B[0] - A[0]
    dB = B[1] - A[1]
    dA = dA * dA
    dB = dB * dB
    return math.sqrt(dA + dB)

if __name__ == "__main__":
    A = (1, 1)
    B = (6, 2)
    temp = distance_between_two_points(A, B)
    print("The distance between A and B is: {}".format(temp))