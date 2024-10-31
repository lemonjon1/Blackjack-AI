import random
#Have dealer hand and score built into game, game initialization accepts an instance of the AI agent as the opposing player

suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
numDecks = 3

class Character:
    def __init__(self) -> None:
        self.currentScore = 0.0
        self.hand: list[tuple[str,str]] = []

class Dealer(Character):
    def __init__(self) -> None:
        super()

class Player(Character):
    def __init__(self) -> None:
        super()
        self.money = 1000.0
        self.bet = 0.0

class Game:
    def __init__(self, agent) -> None:
        self.gameDeck = [(value, suit) for suit in suits for value in values for deck in range(numDecks)]
        random.shuffle(self.gameDeck)
        self.dealer = Dealer()
        self.player = Player()

    def handScore(self, cards: list[tuple[str, str]]) -> float:
        score = 0
        cards.sort(key = lambda card: "z" if card[0] == "Ace" else str.casefold(card[0])) # Sorts the list so that all aces are considered last
        for card in cards:
            if card[0] in ["Jack", "Queen", "King"]:
                score += 10
            elif card[0] == "Ace" and score + 11 <= 21:
                score += 11
            elif card[0] == "Ace" and score + 11 > 21:
                score += 1
            else:
                score += float(card[0])
        return score

    def dealHand(self, character: Character) -> list[tuple[str, str]]:
        character.hand = []
        for _ in range(2):
            card = self.gameDeck.pop()
            character.hand.append(card)
        character.currentScore = self.handScore(character.hand)
        return character.hand

    def hit(self, character: Character) -> None:
        character.hand.append(self.gameDeck.pop())
        character.currentScore = self.handScore(character.hand)

    def doubleDown(self, player: Player) -> None:
        player.hand.append(self.gameDeck.pop())
        player.currentScore = self.handScore(player.hand)
        player.bet *= 2

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
        while (StrtoFloat(bet)==False):
            print("\r\nThat's not a Number!")
            bet = input(f"Choose a bet amount from: 50 - {game.player.money}\r\n")
        while (50.0>float(bet) or float(bet)>game.player.money):
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
                game.player.money -= game.player.bet
                game.doubleDown(game.player)
                print(f"\r\nYour Hand: {game.player.hand}\r\nPlayer Score: {int(game.player.currentScore)}")
                break
            
        # Dealer draws until score is above 17
        while 21 > game.handScore(game.dealer.hand) < 17 and game.player.currentScore <= 21:
            game.hit(game.dealer)
            print("\r\nDealer Hit!")
            print(f"\r\nDealer's hand: {game.dealer.hand}\r\nDealer Score: {int(game.dealer.currentScore)}")

        print("The hand is over:")
        if game.dealer.currentScore > 21:
            print("Dealer busted")
            print("You win")
            game.player.money += float(game.player.bet) * 2
        elif game.player.currentScore > game.dealer.currentScore:
            print(f"\r\nDealer's hand: {game.dealer.hand}\r\nDealer Score: {int(game.dealer.currentScore)}")
            print("You win")
            game.player.money += float(game.player.bet) * 2
        else:
            print(f"\r\nYour Hand: {game.player.hand}\r\nPlayer Score: {int(game.player.currentScore)}")
            print(f"Dealer's hand: {game.dealer.hand}\r\nDealer Score: {int(game.dealer.currentScore)}")
            print("You lose")
        
if __name__ == "__main__":
    playGame()
