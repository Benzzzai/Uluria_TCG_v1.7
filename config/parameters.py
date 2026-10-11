import pygame

# Size and position of element on the screen
LARGE = True

if LARGE:
    SCREEN_WIDTH = 1550
    SCREEN_HEIGHT = 950

    POSITION_Y = [20, 195, 335, 485, 625, 760]

    CARD_SIZE = 110
    EXTRA_HEIGHT = 40
    CARD_MARGIN = 20
    STAT_SIZE = 25

    RIGHT_X = 1150
    LEFT_X = 200

    MANA_RAD = 10
    CHAMPION_SIZE = 90
    HEALTH_RAD = 50

else:
    SCREEN_WIDTH = 1230
    SCREEN_HEIGHT = 720

    POSITION_Y = [5, 120, 240, 370, 490, 605]

    CARD_SIZE = 90
    EXTRA_HEIGHT = 30
    CARD_MARGIN = 20
    STAT_SIZE = 20

    RIGHT_X = 920
    LEFT_X = 150

    MANA_RAD = 8
    CHAMPION_SIZE = 70
    HEALTH_RAD = 40


TURN_Y = SCREEN_HEIGHT // 2 - HEALTH_RAD // 2
BOTTOM_Y = POSITION_Y[4] + CARD_SIZE + CARD_MARGIN

DECK_SIZE = 50

# Colors
C_BACKGROUND = (245, 255, 205)
C_BORDER = (90, 70, 50)

C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_GREY_LIGHT = (180, 180, 180)
C_GREY_CO = (90, 80, 80) # rename and adjust
C_GREY_ST = (60, 60, 60)
C_GREY_SP = (110, 120, 140) # rename and adjust

C_BLUE_COST = (0, 180, 255)
C_BLUE_MANA = (0, 80, 255)
C_YELLOW_ATK = (255, 210, 0)
C_RED_PV = (255, 0, 0)
C_RED_DMG = (155, 0, 0)
C_GREEN_BOOST = (0, 190, 0)
C_GREEN_COST = (0, 110, 0)
C_INTERRUPT = (180, 51, 255)
C_GREEN_SEL = (0, 255, 0)

C_CLASSES = {
    "Pourpre" : (184, 0, 0),
    "Ocre" : (200, 128, 20),
    "Turquoise" : (69, 129, 142),
    "Zéphyr" : (85, 143, 67),
    # "Verdant" : (110, 67, 10),
    "Verdant" : (85, 143, 67),
    "Azur" : (24, 69, 121),
    "Nébuleux" : (103, 78, 167),
    "Obsidienne" : (67, 67, 67),

}

C_P2 = (0, 130, 255)
C_P1 = (255, 120, 0)
C_P2_HEALTH = (200, 230, 255)
C_P1_HEALTH = (255, 230, 200)


# Font
pygame.font.init()

if LARGE:
    FONT_NAME = pygame.font.SysFont("Arial", 16)
    FONT_STAT = pygame.font.SysFont("Arial", 24)
else:
    FONT_NAME = pygame.font.SysFont("Arial", 14)
    FONT_STAT = pygame.font.SysFont("Arial", 22)

FONT_BIG = pygame.font.SysFont("Arial", 36)
FONT_BIG.set_bold(True)