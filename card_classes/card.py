import pygame
from config.parameters import CARD_SIZE

class Card:
    def __init__(self, name, classe, cost, interrupt, description):
        self.name = name
        self.classe = classe  
        self.cost = cost
        self.cost_ori = cost
        self.interrupt = interrupt
        self.description = description

        self.rectangle = pygame.Rect(0, 0, CARD_SIZE, CARD_SIZE)

