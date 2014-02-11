# Got from: http://osdir.com/ml/python.pygame/2002-11/msg00051.html
# CLICKABLE BUTTON WITH AN IMAGE INSIDE IT
#

import sys, pygame

class Button:
    def __init__(self,x,y,imagefile):
        # load in the icon that will go in the middle of the button
        self.insideimg = pygame.image.load(imagefile).convert_alpha()
        self.insiderect = self.insideimg.get_rect()
        self.ix = self.insiderect.size[0]
        self.iy = self.insiderect.size[1]

# set up base values for the size of this button to the image inside it
        self.image = pygame.surface.Surface((self.ix+8,self.iy+8))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

# set button as unpressed
        self.popup()

# draw the button in an "unpressed" state
    def popup(self):
        self.image.fill((96,96,96))
        pygame.draw.line(self.image, (224,224,224), (0,0),(self.ix+8,0) )
        pygame.draw.line(self.image, (224,224,224), (0,0),(0,self.ix+8) )
        pygame.draw.line(self.image, (224,224,224), (1,1),(self.ix+7,1) )
        pygame.draw.line(self.image, (224,224,224), (1,1),(1,self.ix+7) )
        pygame.draw.line(self.image, (224,224,224), (2,2),(self.ix+6,2) )
        pygame.draw.line(self.image, (224,224,224), (2,2),(2,self.ix+6) )
        pygame.draw.rect(self.image, (160,160,160), ((3,3),(self.ix+3,self.iy+3)) )
# put the button icon on the button
        self.image.blit(self.insideimg,(4,4))

# draw the button in a "pressed" state
    def press(self):
        self.image.fill((224,224,224))
        pygame.draw.line(self.image, (96,96,96), (0,0),(self.ix+8,0) )
        pygame.draw.line(self.image, (96,96,96), (0,0),(0,self.ix+8) )
        pygame.draw.line(self.image, (96,96,96), (1,1),(self.ix+7,1) )
        pygame.draw.line(self.image, (96,96,96), (1,1),(1,self.ix+7) )
        pygame.draw.line(self.image, (96,96,96), (2,2),(self.ix+6,2) )
        pygame.draw.line(self.image, (96,96,96), (2,2),(2,self.ix+6) )
        pygame.draw.rect(self.image, (160,160,160), ((3,3),(self.ix+3,self.iy+3)) )
# put the button icon on the button
        self.image.blit(self.insideimg,(4,4))

# this gets called if the mouse is clicked - check if the button was hit
    def clicked(self,pos):
        if (self.rect.left < pos[0] < self.rect.right) and (self.rect.top < pos[1] <
        self.rect.bottom):
            return 1

