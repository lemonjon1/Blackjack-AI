import random
#Have dealer hand and score built into game, game initialization accepts an instance of the AI agent as the opposing player

suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

class Game:
    def __init__(self, agent):
        self.gameDeck = []

        self.gameDeck = [(value, suit) for suit in suits for value in values for deck in range[0:3]]
        random.shuffle(self.gameDeck)

    class Dealer:
        def __init__(self):
            self.currentScore = 0
            self.hand = []

    class Player:
        def __init__(self):
            self.currentScore = 0
            self.hand = []

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

    def dealHand(self):
        hand = []
        for i in range(2):
            card = self.gameDeck.pop()
        return hand

    def hit(self, hand):
        hand.append(self.gameDeck.pop())

def playGame(self):
    game = Game()

if __name__ == "__main__":
    playGame()




