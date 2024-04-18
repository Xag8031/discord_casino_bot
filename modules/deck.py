#building an oop compliant way to shuffle a standard 52 card deck without jokers (because nobody likes jokers.)

from random import shuffle

class Deck:
    #start the deck here.
    def __init__(self):
        self.suites = ["H", "D", "S", "C"]
        self.cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q" , "K"]
        self.deck = []
        self.startDeck()
        
    def startDeck(self):
        for i in self.suites:
            for o in self.cards:
                self.deck.append(i + o)
        self.deck.append(self.deck)
        shuffle(self.deck)        
    def draw(self):
        # move -1 from deck to user hand
        card = self.deck.pop()
        return card
