import random

filename_all_tarot_cards = "/Users/BigBlue/Documents/Programming/Python/data/rider_waite_tarot_cards_all.txt"
filename_used_tarot_cards = "/Users/BigBlue/Documents/Programming/Python/data/rider_waite_tarot_cards_used.txt"

# Pick Card
with open(filename_all_tarot_cards, 'r') as f:
    mylist = f.readlines()
mylist = [i.strip() for i in mylist if len(i) > 0]

random_index = random.randint(1, len(mylist))
tarot_card = mylist[random_index - 1]
s = "This is your card: {}".format(tarot_card)
print(s)

# Put picked card into the "used" file.
with open(filename_used_tarot_cards, 'w') as f:
    f.write(tarot_card)

# Remove Card that was chosen.
newlist = []
for i in mylist:
    if tarot_card == i:
        pass
    else:
        newlist.append(i)
mylist = newlist
newlist = []

s = "There are {} cards left in the deck.".format(len(mylist))
print(s)

# Save cards back to deck.
with open(filename_all_tarot_cards, 'w') as f:
    for i in mylist:
        f.write("{}\n".format(i))

#[print(i) for i in mylist]
