"""
saboteur_game.py

Reference: This class was built off the Connect Four Game class by Johnathon Vitale from COSC350 Assignment 2.

Purpose: Builds and updates the GUI for the game, as well as controlling the game loop.
"""

import pygame

from shared import DEBUG

BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
DISPLAY_WIDTH = 1120
DISPLAY_HEIGHT = 800
INFO_BAR_HEIGHT = 55
CARD_WIDTH = 56
CARD_HEIGHT = 40

pygame.init()
window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT+INFO_BAR_HEIGHT))

# Saboteur Game Class for handling the GUI and game loop
class SaboteurGame:

    def __init__(self, environment, agents, display_w=DISPLAY_WIDTH, display_h=DISPLAY_HEIGHT,
                 card_h=CARD_HEIGHT, card_w=CARD_WIDTH):
        pygame.display.set_caption('Saboteur Game')
        window_clock = pygame.time.Clock()

        self._display = window
        self._window_clock = window_clock
        self._display_size = (display_w, display_h)
        self._environment = environment
        self._card_size = (card_w, card_h)
        self._agents = agents
        self._background_image = pygame.image.load("images/bg.png").convert()

        fonts = pygame.font.get_fonts()
        self._font = fonts[0]
        test_fonts = ['arial', 'couriernew', 'verdana', 'helvetica', 'roboto']
        for font in test_fonts:
            if font in fonts:
                self._font = font
                break

        self.main()

    def _reset_bg(self):
        self._display.blit(self._background_image, (0, 0))

    def _draw_board(self):
        board = self._environment.get_game_board().get_board()
        # Getting the flipped cards to rotate the images
        flipped = self._environment.get_game_board().get_flipped_cards()
        for (row, col), card in board.items():
            if card is not None:
                x = col * CARD_WIDTH
                y = row * CARD_HEIGHT
                image = card.image
                if (row, col) in flipped:
                    flipped_image = pygame.transform.flip(image, True, True)  # Flip the image horizontally
                    self._display.blit(flipped_image, (x, y))
                else:
                    self._display.blit(image, (x, y))

    # Steps in the agents turn to get the new game state
    def _play_step(self):
        game_state = self._environment.get_game_state()
        if self._environment.is_terminal():
            return

        # Current agent type
        cur_type = type(self._environment).turn(game_state)

        # Sense using the current agent type
        self._agents[cur_type].sense(self._environment)

        # Think using the current agent type
        actions = self._agents[cur_type].think()

        # Take the actions
        self._agents[cur_type].act(actions, self._environment)

    def _draw_game_over(self):
        winner = self._environment.get_winner()
        self._draw_text("GAME OVER", 100, 'center', 'middle', 45)
        self._draw_text("Winner: {0}".format(winner), 150, 'center', 'middle', 30)


    def _draw_text(self, text_message, padding_top, orientation='left', align='top', font_size=20):
        font = pygame.font.SysFont(self._font, font_size)
        text_size = font.size(text_message)
        text = font.render(text_message, True, WHITE)

        # Align top or bottom of the window
        if align == 'bottom':
            top = self._display_size[1] + INFO_BAR_HEIGHT - text_size[1] - padding_top
        else:
            top = padding_top

        # Align left, right or center of the window
        if orientation == 'center':
            left = int((self._display_size[0] - text_size[0])/2)
        elif orientation == 'left':
            left = 10
        else:
            left = self._display_size[0] - text_size[0] - 10

        self._display.blit(text, (left, top))

    # Draws a frame of the game play
    def _draw_frame(self):
        self._reset_bg()
        self._draw_board()
        if self._environment.is_terminal():
            self._draw_game_over()
        else:
            gs = self._environment.get_game_state()
            player_turn = gs['player-turn']
            player_cards = gs['player-cards']
            # Clear the info bar
            self._display.fill(BLACK, (0, self._display_size[1], self._display_size[0], INFO_BAR_HEIGHT))
            # Add player turn and previous move to the info bar
            self._draw_text("Player turn: {0}".format(player_turn), 10, 'left', 'bottom', 15)
            move = self._environment.get_previous_move()
            player_type = self._environment.get_last_player_type()
            self._draw_text("Previous move was: {0} by a {1}".format(move, player_type), 10, 'right', 'bottom', 15)
            if DEBUG:
                print("Previous move was: {0} by a {1}".format(move, player_type))

            # Padding for the images of player cards in hand
            x_padding = 200
            y_padding = self._display_size[1] + 10

            # Adding images of the players cards in their hand
            for i in range(len(player_cards)):
                card = player_cards[i]
                self._display.blit(card.image, (x_padding, y_padding))
                x_padding += CARD_WIDTH + 10  # Increase the x padding for the next card

    # Main loop for the game window
    def main(self):
        running = True

        while running:
            # Update frame
            self._draw_frame()
            pygame.display.update()
            self._window_clock.tick(1)
            # Event Tasking
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    quit()

            self._play_step()
