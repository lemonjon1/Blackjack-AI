import random

#Creates deck
suits = ["Spades","Clubs","Diamonds","Hearts"]
values = ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"]
fourDeck = [(value,suit) for suit in suits for value in values for deck in range[0:3]]

#Calculates current hands value
def handScore(card, currentScore):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace' and currentScore + 11 < 21:
        return 11
    elif card[0] == 'Ace' and currentScore + 11 > 21:
        return 1
    else:
        return int(card[0])

