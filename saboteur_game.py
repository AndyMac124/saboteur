import pygame
import random

BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (125, 125, 125)
BLUE = (10, 20, 200)
GREEN = (255, 125, 125)

DISPLAY_WIDTH = 1120
DISPLAY_HEIGHT = 800
INFO_BAR_HEIGHT = 35
CARD_WIDTH = 56
CARD_HEIGHT = 40

pygame.init()
window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT+INFO_BAR_HEIGHT))

class SaboteurGame:

    def __init__(self, environment, agents, display_w=DISPLAY_WIDTH, display_h=DISPLAY_HEIGHT, card_h=CARD_HEIGHT, card_w=CARD_WIDTH):
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
        self._font = fonts[0] # default to a random font
        # try to look among the most common fonts
        test_fonts = ['arial', 'couriernew', 'verdana', 'helvetica', 'roboto']
        for font in test_fonts:
            if font in fonts:
                self._font = font
                break

        self.main()

    def _reset_bg(self):
        self._display.blit(self._background_image, (0, 0))

    def _draw_board(self):
        board = self._environment.get_game_board()
        for (row, col), card in board.items():
            if card is not None:
                x = col * self._card_size[0]
                y = row * self._card_size[1]
                image = card.image
                self._display.blit(image, (x, y))

    def place_card(game_cells, card_name, pos):
        game_cells[pos] = card_name

    def _play_step(self):
        game_state = self._environment.get_game_state()
        if type(self._environment).is_terminal(game_state):
            return

        cur_player = type(self._environment).turn(game_state)

        # TODO Sense

        # TODO Think

        # TODO act


    def _draw_game_over(self):
        # TODO game over display
        pass

    def _draw_text(self):
        # TODO Player turn
        pass

    def _draw_frame(self):
        self._reset_bg()
        self._draw_board()
        self._draw_text()
        if type(self._environment).is_terminal(self._environment.get_game_state()):
            self._draw_game_over()
        else:
            # TODO Change player turn in gamestate
            pass

    def main(self):
        running = True

        while running:
            # update frame
            self._draw_frame()
            pygame.display.update()
            self._window_clock.tick(1)
            #Event Tasking
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    quit()

            self._play_step()
        # TODO game over display
        pass
