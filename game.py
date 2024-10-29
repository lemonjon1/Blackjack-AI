import random
#Have dealer hand and score built into game, game initialization accepts an instance of the AI agent as the opposing player

suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]


class Dealer:
    def __init__(self):
        self.currentScore = 0
        self.hand = []

class Player:
    def __init__(self):
        self.currentScore = 0
        self.hand = []
        self.money = 1000
        self.bet = 0

class Game:
    def __init__(self, agent):
        self.gameDeck = []
        self.gameDeck = [(value, suit) for suit in suits for value in values for deck in range(0,3)]
        random.shuffle(self.gameDeck)
        self.dealer = Dealer()
        self.player = Player()

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

    def dealHand(self, character):
        character.hand = []
        for i in range(2):
            card = self.gameDeck.pop()
            character.hand.append(card)
        return character.hand

    def hit(self, hand):
        hand.append(self.gameDeck.pop())

    def doubleDown(self, hand):
        hand.append(self.gameDeck.pop())
        self.player.bet = self.player.bet*2

def playGame():
    game = Game(0)
    numOfGames = 10
    for i in range(0,numOfGames):
        #If PLayer runs out of money
        if game.player.money == 0:
            break

        #Setup
        bet = input(f"Choose a bet amount from: 50 - {game.player.money}\r\n")
        game.player.bet = float(bet)
        game.player.money -= float(bet)
        print(f"Bet amount: {game.player.bet}")
        print(f"Your Hand: {game.dealHand(game.player)}, score: {game.player.currentScore}")
        #Hide second dealer card
        print(f"Dealer's Hand: {game.dealHand(game.player)[0]}, Hidden")

        #Blackjack
        if game.player.currentScore == 21:
            print(f"Dealer's Hand: {game.dealer.hand}\r\n Dealer Score: {game.dealer.currentScore}")
            if not game.dealer.currentScore == 21:
                print("You win")
                game.player.money += float(game.player.bet) * 2.5
            else:
                print("Push")
                game.player.money += game.player.bet
            continue

        #Choices for current hand
        choice = input("Choice: H for Hit, S for Stand, D for Double\r\n")
        while choice not in ["H","S","D"]:
            print("Invalid input, choose again")
            choice = input("Choice: H for Hit, S for Stand, D for Double\r\n")

        while choice == "H":
            game.hit(game.player.hand)
            print(f"Your Hand: {game.player.hand}\r\nPlayer Score: {game.player.currentScore}")
            if game.player.currentScore > 21:
                print("You Busted")
                continue
            else:
                print(f"Your Hand: {game.player.hand}\r\nPlayer score: {game.player.currentScore}")
                choice = input("Choice: H for Hit, S for Stand, D for Double\r\n")

        # elif choice == "S":
        #     pass
        #
        # elif choice == "D":
        #     pass

if __name__ == "__main__":
    playGame()




