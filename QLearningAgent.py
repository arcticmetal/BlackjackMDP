# QLearningAgent.py
# -----------
# Blackjack Agent without features/weights
# QLearning code appropriated from reinforcement assignment

import BlackjackDeck
import Dealer
import util
import random
import sys

class Agent:
    def __init__(self, numDecks=1, qvalues=util.Counter(), epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=100000):
        """
        Init appropriated from qlearningAgents.py from
        pacman reinforcement assignment.
        """
        self.epsilon = epsilon
        self.discount = gamma
        self.alpha = alpha
        self.numTraining = numTraining
    
        self.dealer = Dealer.Dealer(numDecks, True)          
        self.qvalues = qvalues
        
    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        
        if (util.flipCoin(self.epsilon)):               # Epsilon chance to choose random Hit or Stand, or follow policy. Epsilon 0 = Always policy
            return random.choice(legalActions)
      
        return self.getPolicy(state)
    
    def getState(self):                                 # State is Player Value and Dealer Value with Aces taken into account
        return (self.dealer.getPlayerValue(), self.dealer.getPlayerAceFlag()), \
               (self.dealer.getDealerValue(), self.dealer.getDealerAceFlag())

    def getQValue(self, state, action):                 # qvalue is the value of the state for each action
        return self.qvalues[state, action]
    
    def update(self, state, action, nextState, reward): # update is run after each action; logic must be done with higher level game class
        
        qValue = self.getQValue(state, action) + self.alpha * ( reward
               + self.discount
               * self.getValue(nextState)
               - self.getQValue(state, action))
          
        self.qvalues[state,action] = qValue
               
    def getValue(self, state):                          # returns the maximum value of the state
        maxValue = -99999999
        maxAction = None
        legalActions = self.getLegalActions(state)
    
        for action in legalActions:
            actionValue = self.getQValue(state, action)  
            if ( maxValue < actionValue ):
                maxValue = actionValue
                maxAction = action
      
        return maxValue
    
    def getPolicy(self, state):                         # returns the best action to take for each state; subtly different from getValue
        maxValue = -99999999
        maxAction = None
        legalActions = self.getLegalActions(state)
    
        for action in legalActions:
            actionValue = self.getQValue(state, action)  
            if ( maxValue < actionValue ):
                maxValue = actionValue
                maxAction = action
      
        return maxAction
        
    def getLegalActions(self, state):
        return [1, 2]                                  # Hit or Stand
        
    def getEpsilon(self):  
        return self.epsilon
    
    def setEpsilon(self, epsilon):
        self.epsilon = epsilon
        
    def getDiscount(self):
        return self.discount
        
    def setDiscount(self, discount):
        self.discount = discount
    
    def getAlpha(self):
        return self.alpha
    
    def setAlpha(self, alpha):
        self.alpha = alpha



    