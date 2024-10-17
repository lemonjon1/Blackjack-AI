import random
#have dealer hand and score built into game, game initialization accepts an instance of the ai agent as the opposing player

class Game:
    def __init__(self, agent):
        suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        self.fourDeck = [(value, suit) for suit in suits for value in values for deck in range[0:3]]
        random.shuffle(self.fourDeck)

    def handScore(self, cards, currentScore):
        score = 0
        for card in cards:
            if card[0] in ['Jack', 'Queen', 'King']:
                score += 10
            elif card[0] == 'Ace' and currentScore + 11 < 21:
                score += 11
            elif card[0] == 'Ace' and currentScore + 11 > 21:
                score += 1
            else:
                score += int(card[0])
        return score