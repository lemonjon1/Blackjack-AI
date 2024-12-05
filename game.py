import random

#Have dealer hand and score built into game, game initialization accepts an instance of the AI agent as the opposing player

suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
numDecks = 8

money = []
averageMoney = []

class Character:
    def __init__(self):
        self.currentScore = 0.0
        self.hand: list[tuple[str, str]] = []

class Dealer(Character):
    def __init__(self):
        super().__init__()

class Player(Character):
    def __init__(self):
        super().__init__()  # Ensure Character's __init__ is called to set currentScore
        self.money = 1000.0
        self.bet = 0.0
        self.soft_ace = False

class Game:
    def __init__(self, agent):
        self.gameDeck = [(value, suit) for suit in suits for value in values for deck in range(numDecks)]
        random.shuffle(self.gameDeck)
        self.dealer = Dealer()
        self.player = Player()
        self.count = 0
        self.is_over = False
        # self.dealHand(self.player)
        # self.dealHand(self.dealer)

    def handScore(self, cards: list[tuple[str, str]], character: Character) -> float:
        score = 0
        cards.sort(key = lambda card: "z" if card[0] == "Ace" else str.casefold(card[0])) # Sorts the list so that all aces are considered last
        for card in cards:
            if card[0] in ["Jack", "Queen", "King"]:
                score += 10
            elif card[0] == "Ace" and score + 11 <= 21:
                score += 11
                if character.__class__ == "Player":
                    self.player.soft_ace = False;
            elif card[0] == "Ace" and score + 11 > 21:
                score += 1
                if character.__class__ == "Player":
                    self.player.soft_ace = True;
            else:
                score += float(card[0])
        return score

    def countCard(self, card):
        if card[0] in ["2", "3", "4", "5", "6"]:
            self.count += 1
        elif card[0] in ["10", "Jack", "Queen", "King", "Ace"]:
            self.count -= 1

    def dealHand(self, character: Character) -> list[tuple[str, str]]:
        character.hand = []
        for _ in range(2):
            card = self.gameDeck.pop()
            character.hand.append(card)
            self.countCard(card)
        character.currentScore = self.handScore(character.hand, character)
        return character.hand

    def hit(self, character: Character) -> None:
        card = self.gameDeck.pop()
        character.hand.append(card)
        character.currentScore = self.handScore(character.hand, character)
        self.countCard(card)
        if character.currentScore > 21:
            self.is_over = True

    def doubleDown(self, player: Player) -> None:
        card = self.gameDeck.pop()
        player.currentScore = self.handScore(player.hand, player)
        player.bet *= 2
        self.countCard(card)
        self.is_over = True

    def dealerAction(self):
        while self.handScore(self.dealer.hand, self.dealer) < 17:
            self.hit(self.dealer)
        self.is_over = True

#Used to convert input into number
def StrtoFloat(userInput):
    try:
        val = float(userInput)
        return True
    except ValueError:
        return False

def playGame() -> None:
    game = Game(0)
    numOfGames = 10
    for _ in range(numOfGames):
        #If Player runs out of money/can't play another hand
        if game.player.money <= 50:
            print("\r\nYou ran out of funds! :(")
            break

        #Setup
        bet = input(f"Choose a bet amount from: 50 - {game.player.money}\r\n")

        #Check if bet is valid
        while StrtoFloat(bet)==False:
            print("\r\nThat's not a Number!")
            bet = input(f"Choose a bet amount from: 50 - {game.player.money}\r\n")
        while 50.0>float(bet) or float(bet)>game.player.money:
            print("\r\nInvalid input, choose again.")
            bet = input(f"Choose a bet amount from: 50 - {game.player.money}\r\n")
        game.player.bet = float(bet)
        game.player.money -= float(bet)
        print(f"\r\nBet amount: {game.player.bet}")
        print(f"Your Hand: {game.dealHand(game.player)}, score: {int(game.player.currentScore)}")
        #Hide second dealer card
        print(f"Dealer's Hand: {game.dealHand(game.dealer)[0]}, Hidden")

        #Blackjack
        if game.player.currentScore == 21:
            print(f"Dealer's Hand: {game.dealer.hand}\r\n Dealer Score: {game.dealer.currentScore}")
            if not game.dealer.currentScore == 21:
                print("\r\nYou Got a BlackJack! You win!")
                game.player.money += float(game.player.bet) * 2.5
            else:
                print("Push")
                game.player.money += game.player.bet
            continue

        #Choices for current hand
        while game.player.currentScore <= 21:
            print("")
            print(game.count)
            choice = ""
            if len(game.player.hand) == 2:
                choice = input("Choice: H for Hit, S for Stand, D for Double\r\n")
                while choice not in ["H","S","D"] or choice == "D" and game.player.money < game.player.bet:
                    if choice not in ["H","S","D"]:
                        print("Invalid input, choose again")
                        choice = input("Choice: H for Hit, S for Stand, D for Double\r\n")
                    else:
                        print("Not enough money to double down, choose again")
                        choice = input("Choice: H for Hit, S for Stand, D for Double\r\n")
            else:
                choice = input("Choice: H for Hit, S for Stand\r\n")
                while choice not in ["H","S"]:
                    print("Invalid input, choose again")
                    choice = input("Choice: H for Hit, S for Stand\r\n")

            if choice == "H":
                game.hit(game.player)
                print(f"\r\nYour Hand: {game.player.hand}\r\nPlayer Score: {int(game.player.currentScore)}")
                if (game.player.currentScore > 21):
                    print("Player Busted!")
                    break

            elif choice == "S":
                print(f"\r\nYour Hand: {game.player.hand}\r\nPlayer Score: {int(game.player.currentScore)}")
                break

            elif choice == "D":
                game.doubleDown(game.player)
                print(f"\r\nYour Hand: {game.player.hand}\r\nPlayer Score: {int(game.player.currentScore)}")
                break

        # Dealer draws until score is above 17
        while game.handScore(game.dealer.hand, game.dealer) < 17 and game.player.currentScore <= 21:
            game.hit(game.dealer)
            print("\r\nDealer Hit!")
            print(f"\r\nDealer's hand: {game.dealer.hand}\r\nDealer Score: {int(game.dealer.currentScore)}")

        print("The hand is over:")
        if game.dealer.currentScore > 21:
            print("Dealer busted")
            print("You win")
            game.player.money += float(game.player.bet) * 2
        elif game.player.currentScore > game.dealer.currentScore and game.player.currentScore <= 21:
            print(f"\r\nDealer's hand: {game.dealer.hand}\r\nDealer Score: {int(game.dealer.currentScore)}")
            print("You win")
            game.player.money += float(game.player.bet) * 2
        elif game.player.currentScore == game.dealer.currentScore:
            print(f"\r\nYour Hand: {game.player.hand}\r\nPlayer Score: {int(game.player.currentScore)}")
            print(f"\r\nDealer's hand: {game.dealer.hand}\r\nDealer Score: {int(game.dealer.currentScore)}")
            print("You tied")
            game.player.money += float(game.player.bet)
        else:
            print(f"\r\nYour Hand: {game.player.hand}\r\nPlayer Score: {int(game.player.currentScore)}")
            print(f"Dealer's hand: {game.dealer.hand}\r\nDealer Score: {int(game.dealer.currentScore)}")
            print("You lose")
        
if __name__ == "__main__":
    playGame()
