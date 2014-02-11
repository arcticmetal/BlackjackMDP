# Blackjack Game
# Card images from: 
# http://code.google.com/p/vectorized-playing-cards/downloads/detail?name=SVG_and_EPS_Vector_Playing_Cards_Version_1.3.zip

import sys, pygame
import Buttons
import Dealer
import QLearningAgent
import FeatureAgent
import BlackjackDeck
import util

# Training

if len(sys.argv) == 2:
    Agent = FeatureAgent.Agent(int(sys.argv[1]), util.Counter(), 0.8, 0.8, 0.9)  # Training Agent   
elif len(sys.argv) == 3:
    Agent = FeatureAgent.Agent(int(sys.argv[1]), util.Counter(), 0.8, 0.8, 0.9, int(sys.argv[2])) 
elif len(sys.argv) == 4:
    if int(sys.argv[3]) == 1:
        Agent = FeatureAgent.Agent(int(sys.argv[1]), util.Counter(), 0.8, 0.8, 0.9, int(sys.argv[2])) 
    elif int(sys.argv[3]) == 2:
        print "QLearning"
        Agent = QLearningAgent.Agent(int(sys.argv[1]), util.Counter(), 0.8, 0.8, 0.9, int(sys.argv[2]))
else:
    Agent = FeatureAgent.Agent(1, util.Counter(), 0.8, 0.8, 0.9) 
    
total = 0.0
games = Agent.numTraining
while Agent.numTraining > 0:
    Agent.dealer.gameBegin()      
    while True:          
        oldState = Agent.getState()
        action = Agent.getAction(oldState)    
        if Agent.dealer.playerTurn(action):
            break
        newState = Agent.getState()
        reward = 0
        Agent.update(oldState, action, newState, reward)
    isWin = Agent.dealer.winFlag
    if isWin:
        reward = 1
        total += 1
    else:
        reward = -1
    Agent.update(oldState, action, Agent.getState(), reward)
    Agent.numTraining -= 1

print "Won", int(total), "out of", games
print (total / games)
print "\nTRAINING DONE\n"


# Exploitation of Training

total = 0.0
games = 0
Agent.setEpsilon(0)                             # Exploit all the time
Agent.setAlpha(0.2)                             # Lower learning rate
while games < 10000:
    Agent.dealer.gameBegin()
    while True:
        oldState = Agent.getState()
        action = Agent.getAction(oldState)
        if Agent.dealer.playerTurn(action):
            break
        newState = Agent.getState()
        reward = 0
        Agent.update(oldState, action, newState, reward)
    isWin = Agent.dealer.winFlag
    if isWin:
        reward = 1
        total += 1
    else:
        reward = -1
    Agent.update(oldState, action, Agent.getState(), reward)
    games += 1

print "Won", int(total), "out of", games   
print (total / games)

pygame.init()

size = width, height = 800, 640
green = 0, 210, 0
black = 0, 0, 0

screen = pygame.display.set_mode(size)
screen.fill(green)

cardImageMem = []

for i in range(52):
    cardImageMem.append(0)
    
cardImage = []
cardImage.append("images/cards/Clubs/AC.jpg")
cardImage.append("images/cards/Clubs/2C.jpg")
cardImage.append("images/cards/Clubs/3C.jpg")
cardImage.append("images/cards/Clubs/4C.jpg")
cardImage.append("images/cards/Clubs/5C.jpg")
cardImage.append("images/cards/Clubs/6C.jpg")
cardImage.append("images/cards/Clubs/7C.jpg")
cardImage.append("images/cards/Clubs/8C.jpg")
cardImage.append("images/cards/Clubs/9C.jpg")
cardImage.append("images/cards/Clubs/10C.jpg")
cardImage.append("images/cards/Clubs/JC.jpg")
cardImage.append("images/cards/Clubs/QC.jpg")
cardImage.append("images/cards/Clubs/KC.jpg")
cardImage.append("images/cards/Spades/AS.jpg")
cardImage.append("images/cards/Spades/2S.jpg")
cardImage.append("images/cards/Spades/3S.jpg")
cardImage.append("images/cards/Spades/4S.jpg")
cardImage.append("images/cards/Spades/5S.jpg")
cardImage.append("images/cards/Spades/6S.jpg")
cardImage.append("images/cards/Spades/7S.jpg")
cardImage.append("images/cards/Spades/8S.jpg")
cardImage.append("images/cards/Spades/9S.jpg")
cardImage.append("images/cards/Spades/10S.jpg")
cardImage.append("images/cards/Spades/JS.jpg")
cardImage.append("images/cards/Spades/QS.jpg")
cardImage.append("images/cards/Spades/KS.jpg")
cardImage.append("images/cards/Hearts/AH.jpg")
cardImage.append("images/cards/Hearts/2H.jpg")
cardImage.append("images/cards/Hearts/3H.jpg")
cardImage.append("images/cards/Hearts/4H.jpg")
cardImage.append("images/cards/Hearts/5H.jpg")
cardImage.append("images/cards/Hearts/6H.jpg")
cardImage.append("images/cards/Hearts/7H.jpg")
cardImage.append("images/cards/Hearts/8H.jpg")
cardImage.append("images/cards/Hearts/9H.jpg")
cardImage.append("images/cards/Hearts/10H.jpg")
cardImage.append("images/cards/Hearts/JH.jpg")
cardImage.append("images/cards/Hearts/QH.jpg")
cardImage.append("images/cards/Hearts/KH.jpg")
cardImage.append("images/cards/Diamonds/AD.jpg")
cardImage.append("images/cards/Diamonds/2D.jpg")
cardImage.append("images/cards/Diamonds/3D.jpg")
cardImage.append("images/cards/Diamonds/4D.jpg")
cardImage.append("images/cards/Diamonds/5D.jpg")
cardImage.append("images/cards/Diamonds/6D.jpg")
cardImage.append("images/cards/Diamonds/7D.jpg")
cardImage.append("images/cards/Diamonds/8D.jpg")
cardImage.append("images/cards/Diamonds/9D.jpg")
cardImage.append("images/cards/Diamonds/10D.jpg")
cardImage.append("images/cards/Diamonds/JD.jpg")
cardImage.append("images/cards/Diamonds/QD.jpg")
cardImage.append("images/cards/Diamonds/KD.jpg")

standbut = Buttons.Button(550,500,"images/STAND.bmp")
hitbut = Buttons.Button(550,375,"images/HIT.bmp")
againbut = Buttons.Button(550, 375, "images/Again.bmp")
endbut = Buttons.Button(550, 500,"images/End.bmp")
pygame.display.set_caption("Blackjack")
font = pygame.font.SysFont("Arial", 40)
winMessage = font.render("You Win!", 1, black)
loseMessage = font.render("You Lose!", 1, black)
hitMessage = font.render("Agent Suggests Hit", 1, black)
standMessage = font.render("Agent Suggests Stand", 1, black)

backimg = pygame.image.load("images/cards/Back.jpg")
backrect = backimg.get_rect()

while True:
    screen.fill(green)
    screen.blit(standbut.image,standbut.rect)
    screen.blit(hitbut.image,hitbut.rect)
    pygame.display.flip() 
    Agent.dealer.gameBegin()
    playerHand = Agent.dealer.getPlayerHand()
    dealerHand = Agent.dealer.getDealerHand()
    playerX = 30
    playerY = 300
    dealerX = 450
    dealerY = 0
    
    oldState = Agent.getState()
    agentAction = Agent.getAction(oldState)

    if agentAction == 1:
        screen.blit(hitMessage,(20,100))
    else:
        screen.blit(standMessage,(20,100))
        
    for card in playerHand:
        id = card.id
        if cardImageMem[id] != 0:
            screen.blit(cardImageMem[id], cardImageMem[id].get_rect().move(playerX, playerY))
        else:
            cardimg = pygame.image.load(cardImage[id])
            cardrect = cardimg.get_rect()
            screen.blit(cardimg, cardrect.move(playerX, playerY))
            cardImageMem[id] = cardimg
        playerX += 60
        pygame.display.flip()
        
    id = dealerHand[0].id
    if cardImageMem[id] != 0:
        screen.blit(cardImageMem[id], cardImageMem[id].get_rect().move(dealerX, dealerY))
    else:
        cardimg = pygame.image.load(cardImage[id])
        cardrect = cardimg.get_rect()
        screen.blit(cardimg, cardrect.move(dealerX, dealerY))
    dealerX += 60
    screen.blit(backimg, backrect.move(dealerX, dealerY))
    pygame.display.flip()
    
    while True:   

        exitLoop = False
        doneFlag = False
        
        while exitLoop is False:
            k = pygame.event.poll() 
            if k.type == pygame.MOUSEBUTTONDOWN: 
                if k.button == 1: 
                    if standbut.clicked(k.pos): 
                        standbut.press() 
                        screen.blit(standbut.image,standbut.rect) 
                        pygame.display.flip()
                        doneFlag = Agent.dealer.playerTurn(2)
                        winFlag = Agent.dealer.winFlag
                        exitLoop = True
                        
                    elif hitbut.clicked(k.pos):
                        hitbut.press()
                        screen.blit(hitbut.image,hitbut.rect)
                        pygame.display.flip()
                        doneFlag = Agent.dealer.playerTurn(1)
                        winFlag = Agent.dealer.winFlag
                        exitLoop = True
                        
            if k.type == pygame.MOUSEBUTTONUP:
                if k.button == 1:
                    standbut.popup()
                    hitbut.popup()
                    screen.blit(hitbut.image,hitbut.rect)
                    screen.blit(standbut.image,standbut.rect)
                    pygame.display.flip()
        
        screen.fill(green)
        oldState = Agent.getState()
        agentAction = Agent.getAction(oldState)
        if agentAction == 1:
            screen.blit(hitMessage,(20,100))
        else:
            screen.blit(standMessage,(20,100))
            
        pygame.display.flip()
        playerHand = Agent.dealer.getPlayerHand()
        dealerHand = Agent.dealer.getDealerHand()
        playerX = 30
        for card in playerHand:
            id = card.id
            if cardImageMem[id] != 0:
                screen.blit(cardImageMem[id], cardImageMem[id].get_rect().move(playerX, playerY))
            else:
                cardimg = pygame.image.load(cardImage[id])
                cardrect = cardimg.get_rect()
                screen.blit(cardimg, cardrect.move(playerX, playerY))
                cardImageMem[id] = cardimg
            playerX += 60
            pygame.display.flip()
        
        dealerX = 450
        if doneFlag:
            screen.fill(green)
            
            playerX = 30
            for card in playerHand:
                id = card.id
                if cardImageMem[id] != 0:
                    screen.blit(cardImageMem[id], cardImageMem[id].get_rect().move(playerX, playerY))
                else:
                    cardimg = pygame.image.load(cardImage[id])
                    cardrect = cardimg.get_rect()
                    screen.blit(cardimg, cardrect.move(playerX, playerY))
                    cardImageMem[id] = cardimg
                playerX += 60
            
            pygame.display.flip()
            
            if len(dealerHand) == 1:
                Agent.dealer.dealerHand.append(Agent.dealer.drawFromShoe())
            for card in dealerHand:
                id = card.id
                if cardImageMem[id] != 0:
                    screen.blit(cardImageMem[id], cardImageMem[id].get_rect().move(dealerX, dealerY))
                else:
                    cardimg = pygame.image.load(cardImage[id])
                    cardrect = cardimg.get_rect()
                    screen.blit(cardimg, cardrect.move(dealerX, dealerY))
                    cardImageMem[id] = cardimg
                dealerX += 60
                screen.blit(againbut.image,againbut.rect)
                screen.blit(endbut.image,endbut.rect)
                if winFlag:
                    screen.blit(winMessage, (100, 100))
                else:
                    screen.blit(loseMessage, (100, 100))
                pygame.display.flip()
            
            break
        else:
            id = dealerHand[0].id
            if cardImageMem[id] != 0:
                screen.blit(cardImageMem[id], cardImageMem[id].get_rect().move(dealerX, dealerY))
            else:
                cardimg = pygame.image.load(cardImage[id])
                cardrect = cardimg.get_rect()
                screen.blit(cardimg, cardrect.move(dealerX, dealerY))
            dealerX += 60
            screen.blit(backimg, backrect.move(dealerX, dealerY))
            pygame.display.flip()
            
    exitLoop = False 
    while exitLoop is False:
        k = pygame.event.poll() 
        if k.type == pygame.MOUSEBUTTONDOWN: 
            if k.button == 1: 
                if againbut.clicked(k.pos): 
                    againbut.press() 
                    screen.blit(againbut.image,againbut.rect) 
                    pygame.display.flip()
                    exitLoop = True
                    
                elif endbut.clicked(k.pos):
                    endbut.press()
                    screen.blit(endbut.image,endbut.rect)
                    pygame.display.flip()
                    sys.exit()
                        
        if k.type == pygame.MOUSEBUTTONUP:
            if k.button == 1:
                againbut.popup()
                endbut.popup()
                screen.blit(againbut.image,againbut.rect)
                screen.blit(endbut.image,endbut.rect)
                pygame.display.flip()
        
        
 