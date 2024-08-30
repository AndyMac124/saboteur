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

        self._padding_left = int((self._display_size[0])/2)
        self._padding_top = int((self._display_size[1])/2)

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
        board = self._environment.get_game_board().get_board()
        flipped = self._environment.get_game_board().get_flipped_cards()
        for (row, col), card in board.items():
            if card is not None:
                x = col * self._card_size[0]
                y = row * self._card_size[1]
                image = card.image
                if (row, col) in flipped:
                    flipped_image = pygame.transform.flip(image, True, True)  # Flip the image horizontally
                    self._display.blit(flipped_image, (x, y))
                else:
                    self._display.blit(image, (x, y))

    def place_card(game_cells, card_name, pos):
        game_cells[pos] = card_name

    def _play_step(self):
        game_state = self._environment.get_game_state()
        if self._environment.is_terminal():
            return

        cur_type = type(self._environment).turn(game_state)

        # SENSE
        self._agents[cur_type].sense(self._environment)

        # THINK
        actions = self._agents[cur_type].think()
        print(actions)

        # ACT
        self._agents[cur_type].act(actions, self._environment)

    def _draw_game_over(self):
        # TODO game over display
        pass

    def _draw_text(self, text_message, padding_top, orientation, vertical_align='top', font_size=20):
        font = pygame.font.SysFont(self._font, font_size)
        text_size = font.size(text_message)
        text = font.render(text_message, True, WHITE)

        if vertical_align == 'bottom':
            top = self._display_size[1] + INFO_BAR_HEIGHT - text_size[1] - padding_top
        else:
            top = padding_top

        if orientation == 'center':
            left = (self._display_size[0] - text_size[0]) // 2
        elif orientation == 'left':
            left = 10  # Small padding from the left edge
        elif orientation == 'right':
            left = self._display_size[0] - text_size[0] - 10  # Small padding from the right edge
        else:
            left = 0

        self._display.blit(text, (left, top))

    def _draw_frame(self):
        self._reset_bg()
        self._draw_board()
        if self._environment.is_terminal():
            self._draw_game_over()
        else:
            gs = self._environment.get_game_state()
            player_turn = gs['player-turn']
            self._draw_text("Player Turn: {0}".format(player_turn), 10, 'left', 'bottom', 15)


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
