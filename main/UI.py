import pygame as pg
import os

pg.font.init()

class Button:
    FONT = [
        pg.font.Font(os.path.join("fonts", "RetroFont.ttf"), 50),
        pg.font.Font(os.path.join("fonts", "RetroFont.ttf"), 55),
    ]
    COLOR = (255, 255, 255)  #"GRAY"

    def __init__(self, center: tuple[int, int], text: str, image: pg.Surface = None):
        self.w = 298.5
        self.h = 135.5

        self.center = center  # thêm center thay vì (x, y)
        self.x = center[0] - self.w // 2
        self.y = center[1] - self.h // 2

        self.image = image
        self.hover_active = False

        # Button rect (dùng để detect mouse click / hover)
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

        # Font settings
        self.text = text
        self.text_surf = self.FONT[1].render(self.text, True, self.COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.center)

        # Default button image
        if self.image:
            self.base_image = pg.transform.scale(self.image, (self.w, self.h))

    def draw(self, screen: pg.Surface):
        if self.image:
            # Nếu đang hover, phóng to ảnh
            if self.hover_active:
                scaled_image = pg.transform.scale(self.base_image, (int(self.w * 1.1), int(self.h * 1.1)))  # phóng to 10%
                scaled_rect = scaled_image.get_rect(center=self.center)  # Giữ vị trí trung tâm
                screen.blit(scaled_image, scaled_rect.topleft)
            else:
                screen.blit(self.base_image, (self.x, self.y))
        else:
            # Nếu không có ảnh, vẽ rect cơ bản
            pg.draw.rect(screen, (100, 100, 100), self.rect)
            screen.blit(self.text_surf, self.text_rect)

    def update(self):
        x, y = pg.mouse.get_pos()
        self.hover_active = self.rect.collidepoint(x, y)
