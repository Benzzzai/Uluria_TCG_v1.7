import pygame
import sys
from config.parameters import *
from game import Game

from card_classes.unit import Unit
from card_classes.fighter import Fighter
from card_classes.structure import Structure
from card_classes.spell import Spell
from card_classes.equipment import Equipment

class App:
    def __init__(self, deck_name_1, deck_name_2):
        self.game = Game(deck_name_1, deck_name_2)

        self.selected_card_1 = None
        self.selected_card_2 = None
        self.selected_champion = None
        self.status = "main" # "summoning", "fronting", "fighting", "discover"
        self.tooltip_active = False

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Uluria TCG")
        self.background_image = pygame.image.load("grass.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.start_menu = False
        self.run = True
        self.end_menu = False
        self.clock = pygame.time.Clock()

        while self.start_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.start_menu = False
                        self.run = True
            self.display_start_menu()
            pygame.display.flip()
            self.clock.tick(30)

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        card = self.find_card_by_pos([self.game.player_2.hand, self.game.player_2.backrow, self.game.player_2.frontrow,
                                                        self.game.player_1.hand, self.game.player_1.backrow, self.game.player_1.frontrow], event.pos)
                        champion = self.find_champion_by_pos(event.pos)
                        if self.status in ["summoning", "fronting", "fighting"]:
                            self.target_3_action(card)
                        else:
                            if card:
                                if self.selected_card_1:
                                    self.selected_card_2 = card
                                    self.target_action()
                                else:
                                    self.selected_card_1 = card
                            else:
                                self.selected_card_1 = None
                                self.selected_card_2 = None
                                
                            if champion:
                                self.selected_champion = champion
                            else:
                                self.selected_champion = None

                    elif event.button == 3:
                        if self.selected_card_1:
                            self.game.encre_card(self.selected_card_1)
                            self.selected_card_1 = None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.selected_card_1 = None
                        self.selected_card_2 = None
                        self.game.change_turn()
                    elif event.key == pygame.K_t:
                        self.tooltip_active = not self.tooltip_active
                    elif event.key == pygame.K_d:
                        if self.status == "main":
                            self.status = "discover"
                    elif event.key == pygame.K_a:
                        if self.selected_champion:
                            self.game.activate_champion_action(self.selected_champion)
                            self.selected_champion = None
                    elif event.key == pygame.K_z:
                        if self.selected_champion:
                            self.game.summon_champion_incarnation(self.selected_champion)
                            self.selected_champion = None
                    elif event.key == pygame.K_e:
                        if self.selected_champion:
                            self.game.champion_leveling(self.selected_champion)
                            self.selected_champion = None
                    elif event.key == pygame.K_r:
                        if self.selected_champion:
                            self.game.activate_champion_trigger(self.selected_champion)
                            self.selected_champion = None

            self.game.check_death()
            self.check_end()
            self.display_app()
            if self.tooltip_active:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.display_tooltip(mouse_x, mouse_y)

            pygame.display.flip()
            self.clock.tick(30)

        while self.end_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.display_end_menu()
            pygame.display.flip()
            self.clock.tick(30)


    def target_action(self):
        if self.selected_card_1 in self.game.active_player.hand:
            if isinstance(self.selected_card_1, Spell):
                if self.selected_card_1 == self.selected_card_2:
                    self.game.play_spell(self.selected_card_1)
                elif (self.selected_card_2 in self.game.active_player.frontrow or self.selected_card_2 in self.game.active_player.backrow or 
                        self.selected_card_2 in self.game.ennemy_player.frontrow or self.selected_card_2 in self.game.ennemy_player.backrow):
                    self.game.play_spell(self.selected_card_1, target_card=self.selected_card_2)
            elif isinstance(self.selected_card_1, Equipment):
                if (self.selected_card_2 in self.game.active_player.backrow or self.selected_card_2 in 
                        self.game.active_player.frontrow) and isinstance(self.selected_card_2, Fighter):
                    self.game.play_equipment(self.selected_card_1, self.selected_card_2)
            else:
                if self.selected_card_1.on_inv_target:
                    self.status = "summoning"
                    return
                else:
                    if self.selected_card_1 == self.selected_card_2:
                        self.game.play_unit(self.selected_card_1)
                    elif self.selected_card_2 in self.game.active_player.frontrow or self.selected_card_2 in self.game.active_player.backrow:
                        self.game.play_unit(self.selected_card_1, target_place=self.selected_card_2)

        elif self.selected_card_1 in self.game.active_player.backrow and isinstance(self.selected_card_1, Fighter):
            if self.selected_card_1.front_target:
                self.status = "fronting"
                return
            else:
                if self.selected_card_1 == self.selected_card_2:
                    self.game.move_fighter_front(self.selected_card_1)   
                elif self.selected_card_2 in self.game.active_player.frontrow:
                    self.game.move_fighter_front(self.selected_card_1, target_place=self.selected_card_2)

        elif self.selected_card_1 in self.game.active_player.frontrow and isinstance(self.selected_card_1, Fighter):
            if self.selected_card_1 == self.selected_card_2 or self.selected_card_2 in self.game.ennemy_player.frontrow:
                self.status = "fighting"
                return
            elif self.selected_card_2 in self.game.active_player.backrow:
                self.game.move_fighter_back(self.selected_card_1, target_place=self.selected_card_2)

        self.selected_card_1 = None
        self.selected_card_2 = None

    def target_3_action(self, target_card):
        if self.status == "summoning":
            if (target_card in self.game.ennemy_player.frontrow or target_card in self.game.ennemy_player.backrow or 
                    target_card in self.game.active_player.frontrow or target_card in self.game.active_player.backrow):
                if self.selected_card_1 == self.selected_card_2:
                    self.game.play_unit(self.selected_card_1, target_effect=target_card)
                elif self.selected_card_2 in self.game.active_player.frontrow or self.selected_card_2 in self.game.active_player.backrow:
                    self.game.play_unit(self.selected_card_1, target_place=self.selected_card_2, target_effect=target_card)
        elif self.status == "fronting":
            if (target_card in self.game.ennemy_player.frontrow or target_card in self.game.ennemy_player.backrow or 
                    target_card in self.game.active_player.frontrow or target_card in self.game.active_player.backrow):
                if self.selected_card_1 == self.selected_card_2:
                    self.game.move_fighter_front(self.selected_card_1, target_effect=target_card)   
                elif self.selected_card_2 in self.game.active_player.frontrow:
                    self.game.move_fighter_front(self.selected_card_1, target_place=self.selected_card_2, target_effect=target_card)
        elif self.status == "fighting":
            interrupt_card = None
            target_attack = self.selected_card_2
            if target_card:
                if target_card in self.game.ennemy_player.hand and target_card.interrupt != None:
                    interrupt_card = target_card
                elif target_card in self.game.ennemy_player.frontrow and target_card.protecteur:
                    target_attack = target_card

            if self.selected_card_1 == self.selected_card_2:
                self.game.fight_face(self.selected_card_1, interrupt_card=interrupt_card)
            else:
                self.game.fight(self.selected_card_1, target_attack, interrupt_card=interrupt_card)

        self.status = "main"
        self.selected_card_1 = None
        self.selected_card_2 = None

    def check_end(self):
        if self.game.check_end():
            self.run = False
            self.end_menu = True

    def find_card_by_pos(self, rows, pos):
        for row in rows:
            for card in row:
                if card.rectangle.collidepoint(pos):
                    return card
        return None

    def find_champion_by_pos(self, pos):
        for champion in self.game.active_player.champions:
            if champion.rectangle.collidepoint(pos):
                return champion
        for champion in self.game.ennemy_player.champions:
            if champion.rectangle.collidepoint(pos):
                return champion
        return None
    
    def center_cards(self, row, pos_y, hand=False):
        total_width = len(row) * CARD_SIZE + (len(row) - 1) * CARD_MARGIN
        start_x = (SCREEN_WIDTH - total_width) // 2

        for i, card in enumerate(row):
            card.rectangle.x = start_x + i * (CARD_SIZE + CARD_MARGIN)
            card.rectangle.y = pos_y
            if hand:
                card.rectangle.height = CARD_SIZE + EXTRA_HEIGHT
            else:
                card.rectangle.height = CARD_SIZE

    def display_cards(self, row, hand=False):
        for card in row:
            # ACTIONABLE
            if row == self.game.active_player.backrow or row == self.game.active_player.frontrow:
                if card.actionable:
                    border_rect = card.rectangle.inflate(10, 10)
                    pygame.draw.rect(self.screen, C_GREY_LIGHT, border_rect)

            # PARA
            if row == self.game.active_player.backrow or row == self.game.active_player.frontrow or row == self.game.ennemy_player.backrow or row == self.game.ennemy_player.frontrow:
                if card.frozen or card.stunned:
                    border_rect = card.rectangle.inflate(10, 10)
                    pygame.draw.rect(self.screen, C_BLUE_COST, border_rect)

            # SELECTED
            if card == self.selected_card_1 or card == self.selected_card_2:
                border_rect = card.rectangle.inflate(10, 10)
                pygame.draw.rect(self.screen, C_GREEN_SEL, border_rect)

            # CARD RECTANGLE
            # pygame.draw.rect(self.screen, C_CLASSES[card.classe], card.rectangle)
            pygame.draw.rect(self.screen, C_GREY_CO, card.rectangle)

            if LARGE:
                # IMAGE
                img_rect = pygame.Rect(card.rectangle.left + 10, card.rectangle.top + 10, CARD_SIZE - 20, CARD_SIZE - 30)
                pygame.draw.rect(self.screen, C_BLACK, img_rect)

                if hand:
                    # NAME
                    name_rect = pygame.Rect(card.rectangle.left + 5, card.rectangle.top + CARD_SIZE - 15, CARD_SIZE - 10, 20)
                    pygame.draw.rect(self.screen, C_CLASSES[card.classe], name_rect)
                    name_surface = FONT_NAME.render(card.name, True, C_WHITE)
                    name_rect = name_surface.get_rect(center=name_rect.center)
                    self.screen.blit(name_surface, name_rect)
                else:
                    # NAME
                    name_surface = FONT_NAME.render(card.name, True, C_WHITE)
                    name_rect = name_surface.get_rect(center=img_rect.center)
                    self.screen.blit(name_surface, name_rect)
            else:
                # NAME
                name_surface = FONT_NAME.render(card.name, True, C_WHITE)
                name_rect = name_surface.get_rect(center=card.rectangle.center)
                self.screen.blit(name_surface, name_rect)

            # EQUIPED
            if isinstance(card, Fighter):
                if card.equipment:
                    equip_box_rect = pygame.Rect(card.rectangle.right - STAT_SIZE, card.rectangle.top + 5, STAT_SIZE - 5, STAT_SIZE - 5)
                    pygame.draw.rect(self.screen, C_GREY_LIGHT, equip_box_rect)

            # INTERRUPT
            if hand:
                if card.interrupt:
                    interrupt_box_rect = pygame.Rect(card.rectangle.right - STAT_SIZE, card.rectangle.top + 5, STAT_SIZE - 5, STAT_SIZE - 5)
                    pygame.draw.rect(self.screen, C_INTERRUPT, interrupt_box_rect)

                    if card.interrupt == "cancel":
                        text = "C"
                    elif card.interrupt == "boost_2":
                        text = "A2"
                    elif card.interrupt == "boost_3":
                        text = "A3"
                    elif card.interrupt == "block_2":
                        text = "B2"
                    elif card.interrupt == "block_3":
                        text = "B3"                                
                    interrupt_surface = FONT_NAME.render(text, True, C_BLACK)
                    interrupt_rect = interrupt_surface.get_rect(center=interrupt_box_rect.center)
                    self.screen.blit(interrupt_surface, interrupt_rect)
                    
            # MANA
            if hand:
                cost_box_rect = pygame.Rect(card.rectangle.left + 5, card.rectangle.top + 5, STAT_SIZE + 5, STAT_SIZE)
                pygame.draw.rect(self.screen, C_BLUE_COST, cost_box_rect)
                if card.cost < card.cost_ori:
                    color = C_GREEN_COST
                elif card.cost > card.cost_ori:
                    color = C_RED_DMG
                else:
                    color = C_BLACK
                cost_surface = FONT_STAT.render(str(card.cost), True, color)
                cost_rect = cost_surface.get_rect(center=cost_box_rect.center)
                self.screen.blit(cost_surface, cost_rect)

            # ATK
            if isinstance(card, Fighter) or isinstance(card, Equipment):
                atk_box_rect = pygame.Rect(card.rectangle.left + 5, card.rectangle.bottom - STAT_SIZE - 5, STAT_SIZE + 5, STAT_SIZE)
                pygame.draw.rect(self.screen, C_GREY_LIGHT if isinstance(card, Equipment) else C_YELLOW_ATK, atk_box_rect)
                if card.atk > card.atk_ori:
                    color = C_GREEN_BOOST
                elif card.atk < card.atk_ori:
                    color = C_RED_DMG
                else:
                    color = C_BLACK
                atk_surface = FONT_STAT.render(str(card.atk), True, color)
                atk_rect = atk_surface.get_rect(center=atk_box_rect.center)
                self.screen.blit(atk_surface, atk_rect)

            # PV
            if isinstance(card, Unit) or isinstance(card, Equipment):
                pv_box_rect = pygame.Rect(card.rectangle.right - STAT_SIZE - 10, card.rectangle.bottom - STAT_SIZE - 5, STAT_SIZE + 5, STAT_SIZE)
                pygame.draw.rect(self.screen, C_GREY_LIGHT if isinstance(card, Equipment) else C_RED_PV, pv_box_rect)
                if card.pv < card.pv_max:
                    color = C_RED_DMG
                else:
                    color = C_BLACK
                pv_surface = FONT_STAT.render(str(card.pv), True, color)
                pv_rect = pv_surface.get_rect(center=pv_box_rect.center)
                self.screen.blit(pv_surface, pv_rect)

    def display_mana_bar(self, player, bar_x, bar_y):
        mana_box = pygame.Rect(bar_x, bar_y, 30 * MANA_RAD, 4 * MANA_RAD)
        pygame.draw.rect(self.screen, C_GREY_LIGHT, mana_box)

        for i in range(10):
            circle_x = 1.5 * MANA_RAD + bar_x + i * (2.5 * MANA_RAD)
            circle_y = 2 * MANA_RAD + bar_y

            if i < player.mana:
                pygame.draw.circle(self.screen, C_BLUE_MANA, (circle_x, circle_y), MANA_RAD)
            elif i < player.mana_max:
                pygame.draw.circle(self.screen, C_BLACK, (circle_x, circle_y), MANA_RAD, 2)
            else:
                pygame.draw.circle(self.screen, C_GREY_CO, (circle_x, circle_y), MANA_RAD, 2)

        tot_box = pygame.Rect(bar_x + 26 * MANA_RAD, bar_y, 4 * MANA_RAD, 4 * MANA_RAD)
        tot_surface = FONT_STAT.render(str(player.mana) + "/" + str(player.mana_max), True, C_BLUE_MANA)
        tot_rect = tot_surface.get_rect(center=tot_box.center)
        self.screen.blit(tot_surface, tot_rect)

        if not player.encre:
            encre_box = pygame.Rect(bar_x + 31 * MANA_RAD, bar_y + MANA_RAD, 2 * MANA_RAD, 2 * MANA_RAD)
            pygame.draw.rect(self.screen, C_BLUE_MANA, encre_box)
            encre_surface = FONT_STAT.render("!", True, C_BLUE_MANA)
            encre_rect = encre_surface.get_rect(center=encre_box.center)
            self.screen.blit(encre_surface, encre_rect)

    def display_champions(self, pos_y, pos_x, player):
        champion_zone = pygame.Rect(pos_x, pos_y, 3 * CHAMPION_SIZE + 3 * CARD_MARGIN, CHAMPION_SIZE + CARD_MARGIN + 20)
        pygame.draw.rect(self.screen, C_BACKGROUND, champion_zone)
        pygame.draw.rect(self.screen, C_BORDER, champion_zone, width=2)

        for i, champion in enumerate(player.champions):
            champion.rectangle.x = pos_x + 10 + i * (CHAMPION_SIZE + CARD_MARGIN)
            champion.rectangle.y = pos_y + 10
            
            # SELECTED
            if champion == self.selected_champion:
                border_rect = champion.rectangle.inflate(10, 10)
                pygame.draw.rect(self.screen, C_GREEN_SEL, border_rect)

            pygame.draw.rect(self.screen, C_CLASSES[champion.classe], champion.rectangle)

            color = C_YELLOW_ATK if champion.evolved else C_WHITE
            name_surface = FONT_NAME.render(champion.name, True, color)
            name_rect = name_surface.get_rect(center=(champion.rectangle.centerx, champion.rectangle.centery))
            self.screen.blit(name_surface, name_rect)

            if not champion.evolved and champion.evo_target:
                evo_surface = FONT_NAME.render(str(champion.evo_count) + "/" + str(champion.evo_target), True, C_WHITE)
                evo_rect = evo_surface.get_rect(midtop=(champion.rectangle.centerx, champion.rectangle.top))
                self.screen.blit(evo_surface, evo_rect)

            if champion.action:
                act_box_rect = pygame.Rect(champion.rectangle.left + 5, champion.rectangle.bottom - 30, 25, 25)
                # pygame.draw.rect(self.screen, C_YELLOW_ATK, act_box_rect)
                pygame.draw.circle(self.screen, C_YELLOW_ATK, act_box_rect.center, 12.5)
                act_surface = FONT_NAME.render(str(champion.action_cost), True, C_BLACK)
                act_rect = act_surface.get_rect(center=act_box_rect.center)
                self.screen.blit(act_surface, act_rect)

            if champion.incarnation:
                inc_box_rect = pygame.Rect(champion.rectangle.right - 25, champion.rectangle.bottom - 30, 20, 25)
                pygame.draw.rect(self.screen, C_RED_PV, inc_box_rect)
                inc_surface = FONT_NAME.render(str(champion.incarnation_cost), True, C_BLACK)
                inc_rect = inc_surface.get_rect(center=inc_box_rect.center)
                self.screen.blit(inc_surface, inc_rect)

    def display_player_name(self, pos_x, pos_y, player, color):
        name_rect = pygame.Rect(pos_x, pos_y, 4 * HEALTH_RAD, HEALTH_RAD)
        pygame.draw.rect(self.screen, color, name_rect)
        name_surface = FONT_STAT.render(str(player.name), True, C_BLACK)
        name_rect = name_surface.get_rect(center=name_rect.center)
        self.screen.blit(name_surface, name_rect)

    def display_player_life(self, center_x, center_y, player, color, color_health):
        pygame.draw.circle(self.screen, color_health, (center_x, center_y), HEALTH_RAD)
        pygame.draw.circle(self.screen, color, (center_x, center_y), HEALTH_RAD, width=3)
        color = C_GREY_SP if player.health == 0 else C_BLACK
        health_surface = FONT_BIG.render(str(player.health), True, color)
        health_rect = health_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(health_surface, health_rect)

        if player.armor > 0:
            armor_rect = pygame.Rect(center_x + 20, center_y + 20, HEALTH_RAD - 20, HEALTH_RAD - 20)
            pygame.draw.rect(self.screen, C_BORDER, armor_rect)
            ar_surface = FONT_STAT.render(str(player.armor), True, C_WHITE)
            ar_rect = ar_surface.get_rect(center=armor_rect.center)
            self.screen.blit(ar_surface, ar_rect)

    def display_turn_info(self):
        turn_rect = pygame.Rect(LEFT_X + HEALTH_RAD, TURN_Y, 2 * HEALTH_RAD, HEALTH_RAD)
        color_turn = C_P1 if self.game.active_player == self.game.player_1 else C_P2
        pygame.draw.rect(self.screen, color_turn, turn_rect)
        turn_surface = FONT_STAT.render("tour " + str(self.game.turn), True, C_BLACK)
        turn_rect = turn_surface.get_rect(center=turn_rect.center)
        self.screen.blit(turn_surface, turn_rect)

    def display_app(self):
        self.screen.blit(self.background_image, (0, 0))

        # LEFT
        self.display_player_name(LEFT_X, POSITION_Y[1] + 10, self.game.player_2, C_P2)
        self.display_player_name(LEFT_X, BOTTOM_Y - HEALTH_RAD - 10, self.game.player_1, C_P1)

        self.display_player_life(LEFT_X + 2 * HEALTH_RAD, POSITION_Y[1] + 3 * HEALTH_RAD, self.game.player_2, C_P2, C_P2_HEALTH)
        self.display_player_life(LEFT_X + 2 * HEALTH_RAD, BOTTOM_Y - HEALTH_RAD - 2 * HEALTH_RAD, self.game.player_1, C_P1, C_P1_HEALTH)

        self.display_turn_info()

        # CENTER
        for y in (POSITION_Y[1], POSITION_Y[2], POSITION_Y[3], POSITION_Y[4]):
            row_rect = pygame.Rect((SCREEN_WIDTH - (5 * CARD_SIZE + 5 * CARD_MARGIN)) // 2, y, 5 * CARD_SIZE + 5 * CARD_MARGIN, CARD_SIZE + CARD_MARGIN)
            pygame.draw.rect(self.screen, C_BACKGROUND, row_rect)
            pygame.draw.rect(self.screen, C_BORDER, row_rect, width=2)  

        self.center_cards(self.game.player_2.hand, POSITION_Y[0] + CARD_MARGIN/2, True)
        self.center_cards(self.game.player_2.backrow, POSITION_Y[1] + CARD_MARGIN/2)
        self.center_cards(self.game.player_2.frontrow, POSITION_Y[2] + CARD_MARGIN/2)
        self.center_cards(self.game.player_1.frontrow, POSITION_Y[3] + CARD_MARGIN/2)
        self.center_cards(self.game.player_1.backrow, POSITION_Y[4] + CARD_MARGIN/2)
        self.center_cards(self.game.player_1.hand, POSITION_Y[5] + CARD_MARGIN/2, True)

        self.display_cards(self.game.player_2.hand, True)
        self.display_cards(self.game.player_2.frontrow)
        self.display_cards(self.game.player_2.backrow)
        self.display_cards(self.game.player_1.backrow)
        self.display_cards(self.game.player_1.frontrow)
        self.display_cards(self.game.player_1.hand, True)
        
        # RIGHT
        self.display_champions(POSITION_Y[2] + 10 - 60, RIGHT_X, self.game.player_2)
        self.display_champions(POSITION_Y[3] + 10 + 60, RIGHT_X, self.game.player_1)

        self.display_mana_bar(self.game.player_2, RIGHT_X, POSITION_Y[1] + 10)
        self.display_mana_bar(self.game.player_1, RIGHT_X, BOTTOM_Y - 4 * MANA_RAD - 10)

    def display_tooltip(self, mx, my):
        for card in self.game.player_1.hand:
            if card.rectangle.collidepoint(mx, my):
                self.zoom_card(card, 1)
        for card in self.game.player_1.backrow:
            if card.rectangle.collidepoint(mx, my):
                self.zoom_card(card, 1)
        for card in self.game.player_1.frontrow:
            if card.rectangle.collidepoint(mx, my):
                self.zoom_card(card, 1)
        for card in self.game.player_2.hand:
            if card.rectangle.collidepoint(mx, my):
                self.zoom_card(card, 2)
        for card in self.game.player_2.backrow:
            if card.rectangle.collidepoint(mx, my):
                self.zoom_card(card, 2)
        for card in self.game.player_2.frontrow:
            if card.rectangle.collidepoint(mx, my):
                self.zoom_card(card, 2)

    def display_start_menu(self):
        self.screen.fill(C_BACKGROUND)


    def display_end_menu(self):
        self.screen.fill(C_BACKGROUND)


app = App("PT1 : Pirates aggro", "PT 2 : Elf fortify")