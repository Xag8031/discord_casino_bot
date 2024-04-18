#stores users hand and counts it depending on the game.
class Hand:
    def __init__(self):
        self.hand = []
    def countHand(self):
        # TODO: Implement counting of hand
        #map hand to values and then just add all values until theres only one in the list
        # using jack as 1 or 11, Aces are just 1 and face cards are 10
        
        #truncate the hand to just the values without the suits
        hand = list(map(lambda x: x[1], self.hand))
        handValues = list(map(lambda x: 11 if x == 'J' else 10 if x in ['K', 'Q'] else 1 if x == "A" else int(x), hand))
        while len(handValues) > 1 and sum(handValues) > 21:
            handValues[handValues.index(11)] = 1 # replace the first 11 with 1 if the sum is over 21
        # I want to return the hand value and the hand value - 10 if j is in the hand
        if 11 in handValues:
            return sum(handValues), sum(handValues) - 10
        else:
            return sum(handValues), sum(handValues)
