# Dealer.py
# -----------
# Dealer for Blackjack

import BlackjackDeck

class Dealer:
    def __init__(self, numDecks=1, isSilent=False):
        self.numDecks = numDecks
        self.Shoe = BlackjackDeck.Shoe(numDecks)
        self.playerHand = []
        self.dealerHand = []
        self.playerValue = 0
        self.playerAceFlag = False
        self.dealerValue = 0
        self.dealerAceFlag = False
        self.winFlag = False
        self.isSilent = isSilent                        # isSilent used for Agent and GUI
        self.discardedCards = []
        self.doneFlag = False
        
        self.Shoe.shuffleShoe()

    def __repr__(self):                                 # Different printouts for aces
        
        if not self.playerAceFlag and not self.dealerAceFlag:
            return "PLAYER HAND: %s \nVALUE: %s\nDEALER HAND: %s \nVALUE: %s" \
                    % (self.playerHand, self.playerValue, self.dealerHand, self.dealerValue)  

        if self.playerAceFlag and self.dealerAceFlag:
            return "PLAYER HAND: %s \nVALUE: %s OR %s\nDEALER HAND: %s \nVALUE: %s OR %s" \
                    % (self.playerHand, self.playerValue, self.playerValue + 10,
                    self.dealerHand, self.dealerValue, self.dealerValue + 10)

        if self.playerAceFlag and not self.dealerAceFlag:
            return "PLAYER HAND: %s \nVALUE: %s OR %s\nDEALER HAND: %s \nVALUE: %s" \
                    % (self.playerHand, self.playerValue, self.playerValue + 10,
                    self.dealerHand, self.dealerValue)
                  
        if not self.playerAceFlag and self.dealerAceFlag:
            return "PLAYER HAND: %s \nVALUE: %s\nDEALER HAND: %s \nVALUE: %s OR %s" \
                    % (self.playerHand, self.playerValue,
                    self.dealerHand, self.dealerValue, self.dealerValue + 10)
                    
    def gameBegin(self):
        self.winFlag = False
        self.doneFlag = False                   
        self.playerHand = []
        self.dealerHand = []
        
        while True:
            self.deal()
            self.handValue()
            
            if self.isSilent:                           # Silent mode requires agent input
                return                                  # Need to return so agent can call functions
            else:
                self.playerTurn()                       # Else begin game
            
            str = input("\nAnother Game? 1: Yes, 2: No: ")
            if str == 2:
                break

    def deal(self):
        for i in range(2):                             
            self.playerHand.append(self.drawFromShoe()) # Draw from shoe is a safe draw; checks if shoe is empty first                  
       
        self.dealerHand.append(self.drawFromShoe())
        
    def drawFromShoe(self):
        newCard = self.Shoe.draw()
        
        if newCard is None:                             # Shoe's empty, reshuffle
            self.reshuffle()
            newCard = self.Shoe.draw()                  
        
        return newCard
    
    def reshuffle(self):
        self.Shoe = BlackjackDeck.Shoe(self.numDecks)   # Shuffles decks and shoes in decks
        self.Shoe.shuffleShoe()
        self.discardedCards = []
    
    def handValue(self):                                # Computes actual value of hand based on card objects
        totalPlayerValue = 0
        totalDealerValue = 0
        self.playerAceFlag = False                      # Aces treated as low in hand value, but an ace flag is set for possible blackjacks
        self.dealerAceFlag = False
        
        for card in self.playerHand:
            if card.rank is 11 or card.rank is 12 or card.rank is 13:   # card.rank is "normal" rank of cards (these are face cards)
                totalPlayerValue += 10                                  # value changed for blackjack rules
            elif card.rank is 1:
                self.playerAceFlag = True
                totalPlayerValue += 1
            else:
                totalPlayerValue += card.rank
                
        for card in self.dealerHand:
            if card.rank is 11 or card.rank is 12 or card.rank is 13:
                totalDealerValue += 10
            elif card.rank is 1:
                self.dealerAceFlag = True
                totalDealerValue += 1
            else: 
                totalDealerValue += card.rank
                
        self.playerValue = totalPlayerValue
        self.dealerValue = totalDealerValue
         
    def dealerTurn(self):                                               # Dealer goes after player and then calls gameEnd
        highAce = False                                                 # Used to keep track of possible high ace blackjacks 
        self.dealerHand.append(self.drawFromShoe())
        self.handValue()   
        
        if self.dealerValue > 21:                                       # Dealer bust; should never actually happen right here
            if self.isSilent:                                           
                return self.gameEndSilent()
            else:
                return self.gameEnd()
        
        if self.dealerValue > 16:                                       # Dealer stands on 17
            if self.isSilent:
                return self.gameEndSilent()
            else:
                return self.gameEnd()
        
        while self.dealerValue < 17:
            self.dealerHand.append(self.drawFromShoe())
            self.handValue()
            
            if self.dealerAceFlag:                                      # Consideration for how dealer deals with aces
                if highAce:                                             # If 21 with high ace value, get blackjack
                    if self.dealerValue == 21:
                        if self.isSilent: 
                            return self.gameEndSilent()
                        else:
                            self.dealerAceFlag = False
                            return self.gameEnd()
                    if self.dealerValue > 21:                           # Else, continue to hit until high ace bust, go to low ace
                        highAce = False
                        self.dealerValue -= 10
                if self.dealerValue + 10 < 22:
                    highAce = True
                    self.dealerValue += 10
                    
            if self.dealerValue > 21:                                  
                if self.isSilent:
                    return self.gameEndSilent()
                else:
                    return self.gameEnd()
        
            if self.dealerValue > 16:
                if highAce:
                    self.dealerValue -= 10
                else:
                    if self.isSilent:
                        return self.gameEndSilent()
                    else:
                        return self.gameEnd()
    
    def playerTurn(self, action=2):                                     # playerTurn takes action for agent
        self.handValue()                                
        
        if self.playerValue > 21:                                       # Need this here to catch agent busts/blackjacks
            if self.isSilent:
                return self.gameEndSilent()
            else:
                return self.gameEnd()
        
        if self.playerValue is 21:
            if self.isSilent:
                return self.gameEndSilent()
            else:
                return self.gameEnd()
            
        if self.playerAceFlag:
            if self.isSilent:
                if self.playerValue + 10 is 21:
                    return self.gameEndSilent()
            else:
                if self.playerValue + 10 is 21:
                    self.playerValue += 10
                    self.playerAceFlag = False                          # Solely for printout reasons
                    return self.gameEnd()
        
        while self.playerValue < 22:
            if self.isSilent:
                if action is 2:
                    return self.dealerTurn()
                else:
                    self.playerHand.append(self.drawFromShoe())
                    self.handValue()
                    if self.playerValue > 21:                                       # Need this here to catch agent busts/blackjacks
                        return self.gameEndSilent()
        
                    if self.playerValue == 21:
                        return self.gameEndSilent()
            
                    if self.playerAceFlag:
                        if self.playerValue + 10 is 21:
                            return self.gameEndSilent()
                    return False                                        # Agent only uses code up to here
            else:
                print self
            
                str = input("\nPlease Enter 1 to Hit, 2 to Stand: ")
                if str is 2:
                    self.dealerTurn()
                    return

                self.playerHand.append(self.drawFromShoe())
                self.handValue()           
                    
                if self.playerValue > 21:

                    self.gameEnd()
                    return
        
                if self.playerValue is 21:
                    self.dealerTurn()
                    return
            
                if self.playerAceFlag:    
                    if self.playerValue + 10 is 21:
                        self.playerValue += 10
                        self.playerAceFlag = False
                        self.dealerTurn()
                        return

                
    def gameEnd(self):                                                  # Gameend for command line play
        print self
        
        self.playerHand = []
        self.dealerHand = []
        
        if self.playerValue > 21:
            self.winFlag = False
            print "\nBust!\n"
        elif self.dealerValue > 21:
            self.winFlag = True
            print "\nDealer Bust!\n"
        elif self.playerValue == self.dealerValue:
            self.winFlag = False
            print "\nPush\n"
            return True
        elif self.playerValue == 21:
            self.winFlag = True
            print "\nBlackjack!\n"
        elif self.dealerValue == 21:
            self.winFlag = False
            print "\nDealer Blackjack!\n"
        elif self.playerValue > self.dealerValue:
            self.winFlag = True
        elif self.playerValue < self.dealerValue:
            self.winFlag = False
            
        if self.winFlag:
            print "\nYOU WIN!\n"
        else:
            print "\nYOU LOSE!\n"
            
        return True
        
    def gameEndSilent(self):                                          # Gameend for silent play; no printouts
        for i in range( len(self.playerHand) ):
            self.discardedCards.append(self.playerHand[i])
            
        for i in range( len(self.dealerHand) ):
            self.discardedCards.append(self.dealerHand[i])
                
        if self.playerValue > 21:
            self.winFlag = False
        elif self.dealerValue > 21:
            self.winFlag = True
        elif self.playerValue == self.dealerValue:
            self.winFlag = False
            return True
        elif self.playerValue == 21:
            self.winFlag = True
        elif self.dealerValue == 21:
            self.winFlag = False
        elif self.playerValue > self.dealerValue:
            self.winFlag = True
        elif self.playerValue < self.dealerValue:
            self.winFlag = False
            
        return True                                                  # Returns True for agent win/false for agent loss
            
    def getPlayerValue(self):                                        # Needed for state
        return self.playerValue
        
    def getDealerValue(self):
        return self.dealerValue
    
    def getPlayerAceFlag(self):
        return self.playerAceFlag
        
    def getDealerAceFlag(self):
        return self.dealerAceFlag
        
    def getDiscardedCards(self):
        for card in self.playerHand:
            self.discardedCards.append(card)
        for card in self.dealerHand:
            self.discardedCards.append(card)
        return self.discardedCards
        
    def getPlayerHand(self):
        return self.playerHand
        
    def getDealerHand(self):
        return self.dealerHand
