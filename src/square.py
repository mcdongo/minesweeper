import math
import pygame as pg


class Square:
    def __init__(self, width, height, FONT, BIGFONT):
        self.width = width
        self.height = height
        self.FONT = FONT
        self.BIGFONT = BIGFONT

        self.surface = pg.Surface([self.width, self.height])
        self.surface.fill((0, 0, 100))
        pg.draw.rect(self.surface, (0, 0, 0), [0, 0, 35, 35], 2, 2, 2, 2)

        self.mine = False
        self.neighbors = 0
        self.text = ''
        self.revealed = False
        self.flagged = False
        self.highlighted = False

    def is_mine(self):
        return self.mine

    def set_mine(self):
        self.mine = True
        self.set_text('*')

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        if neighbors != 0:
            self.set_text(f'{neighbors}')

    def get_neighbors(self):
        return self.neighbors

    def set_revealed(self):
        self.revealed = True

    def get_revealed(self):
        return self.revealed

    def set_flagged(self):
        if not self.get_revealed():
            if not self.get_flagged():
                self.flagged = True
                self.set_text('@')
            else:
                self.flagged = False
                self.set_text('')

    def get_flagged(self):
        return self.flagged

    def reset(self):
        self.__init__(35, 35)

    def get_highlighted(self):
        return self.highlighted

    def set_highlighted(self, value):
        if not self.get_revealed():
            self.highlighted = value

    def update(self):
        if self.get_text() == '*' and self.get_revealed():
            self.to_blit = self.BIGFONT.render(
                str(self.get_text()), True, (255, 255, 255))
        else:
            self.to_blit = self.FONT.render(
                str(self.get_text()), True, (255, 255, 255))
        text_rect = self.to_blit.get_rect()
        text_rect.center = (math.ceil(35 / 2), math.ceil(35 / 2))
        self.surface.fill((0, 0, 100))

        if self.get_revealed():
            self.surface.fill((0, 0, 255))
            self.surface.blit(self.to_blit, text_rect)

        if self.get_flagged():
            self.surface.blit(self.to_blit, text_rect)

        if not self.get_revealed():
            if self.get_highlighted():
                pg.draw.rect(self.surface, (255, 255, 255),
                             [0, 0, 35, 35], 2, 2, 2, 2)
            else:
                pg.draw.rect(self.surface, (0, 0, 0), [
                             0, 0, 35, 35], 2, 2, 2, 2)
