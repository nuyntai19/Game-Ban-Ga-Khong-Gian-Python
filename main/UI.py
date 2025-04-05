import pygame as pg
import os

pg.font.init()

class Button:
    FONT = [
        pg.font.Font(os.path.join("fonts", "RetroFont.ttf"), 50),
        pg.font.Font(os.path.join("fonts", "RetroFont.ttf"), 55),
    ]
    COLOR = "#27E7C9"

    def __init__(self, center: tuple[int, int], text: str):
        self.w = 300
        self.h = 80

        self.x = center[0] - self.w // 2
        self.y = center[1] - self.h // 2

        # Create a surface with button size
        self.surface = pg.Surface((self.w, self.h), pg.SRCALPHA)

        self.hover_active = False

        # Button rect (used for mouse detection)
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

        # Text surfaces
        self.text_surf = self.FONT[0].render(text, True, self.COLOR)
        self.text_rect = self.text_surf.get_rect(center=(self.w // 2, self.h // 2))

        self.hover_text_surf = self.FONT[1].render(text, True, self.COLOR)
        self.hover_text_rect = self.hover_text_surf.get_rect(center=(self.w // 2, self.h // 2))

    def update(self):
        x, y = pg.mouse.get_pos()
        self.hover_active = self.rect.collidepoint(x, y)

    def draw(self, target_surface: pg.Surface):
        # Clear button surface
        self.surface.fill((0, 0, 0, 0))  # Transparent fill

        # Draw to button surface
        if self.hover_active:
            pg.draw.rect(self.surface, self.COLOR, pg.Rect(-5, -5, self.w + 10, self.h + 10), 2, 20)
            self.surface.blit(self.hover_text_surf, self.hover_text_rect)
        else:
            pg.draw.rect(self.surface, self.COLOR, pg.Rect(0, 0, self.w, self.h), 2, 20)
            self.surface.blit(self.text_surf, self.text_rect)

        # Blit button surface to target surface
        target_surface.blit(self.surface, (self.x, self.y))
