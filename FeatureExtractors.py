# Feature Extractor taken from 
# http://www-inst.eecs.berkeley.edu/~cs188/sp11/projects/reinforcement/reinforcement.html

import util 

class FeatureExtractor:  
  def getFeatures(self, state, action, discard):    
    """
      Returns a dict from features to counts
      Usually, the count will just be 1.0 for
      indicator functions.  
    """
    util.raiseNotDefined()
    
class IdentityExtractor(FeatureExtractor):
  def getFeatures(self, state, action, discard):
    feats = util.Counter()
    feats[(state,action)] = 1.0
    return feats
    
class SimpleExtractor(FeatureExtractor):

  def getFeatures(self, state, action, discard):
    playerValue = state[0][0]
    dealerValue = state[1][0]
    playerAceFlag = state[0][1]
    dealerAceFlag = state[1][0]
    totalDiscardValue = 0

    features = util.Counter()
    
    features["bias"] = 1.0
    for card in discard:
        if card.rank is 11 or card.rank is 12 or card.rank is 13:   # card.rank is "normal" rank of cards (these are face cards)
            totalDiscardValue += 10                                  # value changed for blackjack rules
        elif card.rank is 1:
            totalDiscardValue += 1
        else:
            totalDiscardValue += card.rank
    
    if action == 1:
    
        if playerAceFlag:
            features["playerValue"] = (31.0 - playerValue)/10
        else:
            features["playerValue"] = (21.0 - playerValue)/10
         
        if float(totalDiscardValue) / len(discard) > 9.0:
            features["discard"] = 1.0
        else:
            features["discard"] = 0

    
    elif action == 2:
        
        if playerAceFlag:
            features["playerValue"] = 1.0/(31.0 - playerValue)
        elif playerValue != 22:
            features["playerValue"] = 1.0/(22.0 - playerValue)

        if float(totalDiscardValue) / len(discard) > 9.0:
            features["discard"] = 0
        else:
            features["discard"] = 1.0

    features.divideAll(10.0)
    return features