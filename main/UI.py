import pygame as pg
import os

pg.font.init()
class Button:
    FONT = [
        pg.font.Font(os.path.join("fonts", "RetroFont.ttf"), 50),
        pg.font.Font(os.path.join("fonts", "RetroFont.ttf"), 55),
    ]
    COLOR = "GRAY"

    def __init__(self, center: tuple[int, int], text: str, image: pg.Surface = None):
        self.w = 300
        self.h = 80

        self.x = center[0] - self.w // 2
        self.y = center[1] - self.h // 2
        
        self.image = image

        # Nếu có image thì dùng image, không thì tạo surface trống
        if self.image:
            self.surface = pg.transform.scale(self.image, (self.w, self.h))
        else:
            self.surface = pg.Surface((self.w, self.h), pg.SRCALPHA)

        self.hover_active = False

        # Button rect (dùng để detect mouse click / hover)
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

        # Font settings
        self.FONT = [pg.font.Font(None, 36), pg.font.Font(None, 48)]  # giả sử bạn dùng kiểu này
        self.COLOR = (255, 255, 255)  # Màu text, giả sử trắng

        # Text surfaces
        self.text_surf = self.FONT[1].render("", True, self.COLOR)
        self.text_rect = self.text_surf.get_rect(center=(self.w // 2, self.h // 2))

        self.hover_text_surf = self.FONT[1].render("", True, (255, 200, 0))  # Text hover màu vàng cam
        self.hover_text_rect = self.hover_text_surf.get_rect(center=(self.w // 2, self.h // 2))

    def draw(self, screen: pg.Surface):
        # Vẽ ảnh hoặc nền
        if self.image:
            screen.blit(self.surface, (self.x, self.y))
        else:
            pg.draw.rect(screen, (100, 100, 100), self.rect)  # màu xám nếu không có ảnh

        screen.blit(self.surface, (self.x, self.y))

    def update(self):
        x, y = pg.mouse.get_pos()
        self.hover_active = self.rect.collidepoint(x, y)
