# BlackjackDeck.py
# -----------
# Data Structure for Card/Deck/Shoe in Blackjack
# Card Data Structure Attributed from: 
# http://stackoverflow.com/questions/2518753/best-way-to-implement-a-deck-for-a-card-game-in-python

import random

class Card:
    def __init__(self, rank, suit, id):
        self.rank = rank
        self.suit = suit
        self.id = id
    
    def __repr__(self):
            letters = {1:'Ace', 11:'Jack', 12:'Queen', 13:'King'}
            letter = letters.get(self.rank, str(self.rank))
            suits = {1:'Clubs', 2:'Spades', 3:'Hearts', 4:'Diamonds'}
            suitstr = suits.get(self.suit, str(self.suit))
            return "<%s of %s>" % (letter, suitstr)            

class Deck:
    def __init__(self):
        self.Cards = []
        id = 0
        
        for enum in range(1, 5):
            for enum2 in range(1, 14):
                self.Cards.append(Card(enum2, enum, id))
                id += 1
        
    def __repr__(self):
        deckStr = ''
        
        for card in self.Cards:
            deckStr += str(card)
            deckStr += ' '
        return deckStr
        
    def shuffleDeck(self):
        random.shuffle(self.Cards)
        
    def draw(self):
        return self.Cards.pop()
    
    def returnToDeck(self, card):
        return self.Cards.append(card)
      
    def isEmpty(self):
        return not self.Cards
        
class Shoe:
    def __init__(self, numDecks):
        self.numDecks = numDecks
        self.Decks = [Deck() for i in range(numDecks)]
    
    def __repr__(self):
        shoeStr = ''
        
        for deck in self.Decks:
            shoeStr += str(deck)
            shoeStr += "\n\n"
        
        return shoeStr
        
    def shuffleShoe(self):
        random.shuffle(self.Decks)
        
        for deck in self.Decks:
            deck.shuffleDeck()
            
    def draw(self):
        for deck in self.Decks:
            if not deck.isEmpty():
                return deck.draw()
    
    def returnToShoe(self, card):
        for deck in self.Decks:
            if length(deck) < 52:
                deck.returnToDeck(card)
                break
                
        return None
