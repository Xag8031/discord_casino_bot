#seperate diffrent games of blackjack going on at once. also used to store the main info for new games ie game class.
import modules.hand

from modules.hand import Hand
from modules.deck import Deck
# this still needs to deal with dealer logic
class Game:
    def __init__(self):
        self.playerHand = Hand()
        self.dealerHand = Hand()
        self.bet = 0
        self.turn = 0
        # init the deck
        self.deck = Deck()
        self.dealerMessage = None
        self.playerMessage = None
        
    def initialDeal(self):
        # TODO: Implement dealing initial cards to player and dealer
        self.dealerHand.hand.append(self.deck.draw())
        self.dealerHand.hand.append(self.deck.draw())
        self.playerHand.hand.append(self.deck.draw())
        self.playerHand.hand.append(self.deck.draw())
        
    def hit(self):
        if self.turn == 0:
            self.playerHand.hand.append(self.deck.draw())
        else:
            self.dealerHand.hand.append(self.deck.draw())
        
    def stand(self):
        self.turn = 1
        self.dealerTurn()
    
    def dealerTurn(self):
        while self.dealerHand.countHand() < 17:
            self.dealerHand.hand.append(self.deck.draw())
        #check the winner and display it.
    
    def raiseBet(self, amount):
        self.bet += amount
    
    def check_winner(self):
        # TODO: Implement check for winner
        playerHand = self.playerHand.countHand()[0]
        dealerHand = self.dealerHand.countHand()[0]
        winner = 0
        if playerHand > 21:
            winner = 2
        elif dealerHand > 21:
            winner = 1
        elif playerHand > dealerHand:
            winner = 1
        elif playerHand < dealerHand:
            winner = 2
        return winner
    
    def interact(self, response):
        if response == "hit":
            self.hit()
        elif response == "stand":
            self.stand()
        elif isinstance(response, int):
            self.raiseBet(response)