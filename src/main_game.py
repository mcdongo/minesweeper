import pygame as pg
import math
from game_logic import *
from square import Square
from math import ceil
from time import sleep

pg.init()
FONT = pg.font.SysFont('Caladea', 20)
BIGFONT = pg.font.SysFont('Caladea', 42)


class Game:
    def __init__(self):
        while True:
            grid_size = int(input("How many rows (min 10, max 25): "))
            if grid_size > 25 or grid_size < 10:
                print("Invalid grid size!")
                continue
            break

        self.rows = grid_size
        self.cols = ceil(self.rows * 1.2)

        min_mines = ceil(self.rows * self.cols / 10)
        max_mines = ceil(self.rows * self.cols * 3 / 10)

        while True:
            self.mines = int(
                input(f"How many mines (min: {min_mines}, max: {max_mines}): "))
            if self.mines < min_mines or self.mines > max_mines:
                print("Invalid amount of mines!")
                continue
            break

        sleep(0.1)
        self.run()

    def run(self):
        self.highlighted_square = None
        self.level = [[] for _ in range(self.rows)]

        for y in range(self.rows):
            for _ in range(self.cols):
                self.level[y].append(Square(35, 35, FONT, BIGFONT))

        self.dug_pos_list = set()
        self.window_width = self.cols * 35
        self.window_height = self.rows * 35 + 50
        self.display = pg.display.set_mode(
            [self.window_width, self.window_height])

        pg.display.set_caption('Budget Minesweeper')

        self.tiles_left = self.rows * self.cols - self.mines
        self.text = f'{self.tiles_left} tiles left'

        self.bottom_text = BIGFONT.render(self.text, True, (0, 0, 0))
        self.bottom_text_rect = self.bottom_text.get_rect()
        self.bottom_text_rect.center = (
            math.ceil(self.window_width / 2), self.window_height - 25)

        self.start_time = 0
        self.counting_text = FONT.render('0s', True, (0, 0, 0))
        self.counting_rect = self.counting_text.get_rect(
            center=(30, self.window_height - 25))

        clock = pg.time.Clock()
        running = True

        while running:
            running = self.event_loop()
            self.update_clock()
            self.update_board()
            self.render_level()
            clock.tick(60)

        pg.quit()

    def update_clock(self):
        if len(self.dug_pos_list) > 0 and self.tiles_left > 0:
            counting_time = pg.time.get_ticks() - self.start_time
            counting_seconds = str(
                round((counting_time % 600000) / 1000, 1)).zfill(2)
            self.counting_text = FONT.render(
                f'{counting_seconds}s', True, (0, 0, 0))
            # self.counting_rect = self.counting_text.get_rect(center = (30, self.window_height - 25))

    def render_level(self):
        self.display.fill((255, 255, 255))
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                self.display.blit(self.level[y][x].surface, (35 * x, 35 * y))

        self.display.blit(self.bottom_text, self.bottom_text_rect)
        self.display.blit(self.counting_text, self.counting_rect)
        pg.display.flip()

    def event_loop(self):
        for e in pg.event.get():
            mouse_pos = pg.mouse.get_pos()
            mouse_pos = (
                math.ceil(mouse_pos[1] / 35) - 1, math.ceil(mouse_pos[0] / 35) - 1)
            self.check_for_highlight(mouse_pos)
            if e.type == pg.QUIT:
                return False
            if pg.mouse.get_pressed()[0]:
                self.dig_board(mouse_pos, 'left')
            if pg.mouse.get_pressed()[2]:
                self.dig_board(mouse_pos, 'right')
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_r:
                    self.run()
                if e.key == pg.K_ESCAPE:
                    return False
        return True

    def check_for_highlight(self, mouse_pos):
        if mouse_pos[0] >= self.rows:
            return

        if self.highlighted_square != mouse_pos:
            if self.highlighted_square != None:
                self.level[self.highlighted_square[0]
                           ][self.highlighted_square[1]].set_highlighted(False)
            self.highlighted_square = mouse_pos
            self.level[self.highlighted_square[0]
                       ][self.highlighted_square[1]].set_highlighted(True)

    def dig_board(self, mouse_pos, action):
        result = None
        if mouse_pos[0] >= len(self.level):
            return
        if action == 'left':
            if len(self.dug_pos_list) == 0:
                mine_cords = randomize_mines(self.level, self.mines, mouse_pos)
                self.level = create_mine_map(self.level, mine_cords)
                self.start_time = pg.time.get_ticks()
            result = dig(self.level, mouse_pos, self.dug_pos_list)
            self.dug_pos_list.add(mouse_pos)

        if action == 'right':
            self.level[mouse_pos[0]][mouse_pos[1]].set_flagged()

        self.update_win_condition()
        if result == -1:
            self.game_over()
        if self.tiles_left == 0 and result != -1:
            self.victory()

        # self.update_board()

    def update_board(self):
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x].get_revealed():
                    if self.level[y][x].get_neighbors() != 0:
                        self.level[y][x].set_text(
                            self.level[y][x].get_neighbors())
                self.level[y][x].update()

    def game_over(self):
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                self.level[y][x].set_revealed()

        self.tiles_left = 0
        self.bottom_text = BIGFONT.render(
            'Game over! (press R to restart)', True, (0, 0, 0))
        self.bottom_text_rect = self.bottom_text.get_rect()
        self.bottom_text_rect.center = (
            math.ceil(self.window_width / 2), self.window_height - 25)

    def victory(self):
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                self.level[y][x].set_revealed()

        self.bottom_text = BIGFONT.render(
            'You win! (R to restart)', True, (0, 0, 0))
        self.bottom_text_rect = self.bottom_text.get_rect()
        self.bottom_text_rect.center = (
            math.ceil(self.window_width / 2), self.window_height - 25)

    def update_win_condition(self):
        total_tiles_left = 0
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if not self.level[y][x].get_revealed():
                    total_tiles_left += 1

        self.tiles_left = total_tiles_left - self.mines
        if self.tiles_left != 0:
            self.text = f'{self.tiles_left} tiles left'
            self.bottom_text = BIGFONT.render(self.text, True, (0, 0, 0))
            self.bottom_text_rect = self.bottom_text.get_rect()
            self.bottom_text_rect.center = (
                math.ceil(self.window_width / 2), self.window_height - 25)


if __name__ == '__main__':
    game = Game()
