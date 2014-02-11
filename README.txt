Files Included:

Blackjack.py - GUI/Agent Training
BlackjackDeck.py - Card/Deck/Shoe classes
Buttons.py - GUI class taken from another source
Dealer.py - Blackjack game world/rules
FeatureAgent.py - Feature Extraction Agent
FeatureExtractors.py - Features used by FeatureAgent
QLearningAgent.py - Q-Learning Agent
util.py - Some utility functions

images folder contains images for GUI.

You need pygame to run the game.

You can run the game with

python Blackjack.py

There are 3 possible arguments, first one is number of decks in play,
second one is number of test games, and the third one is which agent
you're using. 1 is the Feature Agent, 2 is the QLearning Agent.

So to run a game with 4 decks, 10000 training games and the QLearningAgent you'd enter:

python Blackjack.py 4 10000 2

The default is 1 deck, 1000 games, and the Feature Agent.