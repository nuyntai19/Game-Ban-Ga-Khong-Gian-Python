import pygame as pg
pg.font.init()

class Button:
    #set font và màu
    FONT = [
        pg.font.Font("fonts\RetroFont.ttf", 50),
        pg.font.Font("fonts\RetroFont.ttf", 55),
    ]
    COLOR = "#27E7C9"

    #tạo các thuộc tính cơ bản cho button
    def __init__(self, surface: pg.Surface,
                center: tuple[int, int],
                text: str):
        self.surface = surface

        self.w = 300
        self.h = 80
        
        
        self.x = center[0] - self.w // 2
        self.y = center[1] - self.h // 2

        #giá trị hover
        self.hover_active = False

        #vẽ viền cho cho button
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        
        #viền của button khi hover = True
        self.hover_rect = pg.Rect(self.x - 5, self.y - 5, self.w + 10, self.h + 10)

        #nội dung được ghi trên button
        self.text_surf = self.FONT[0].render(text, True, self.COLOR)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = center

        #nội dung được ghi trên button khi hover = True
        self.hover_text_surf = self.FONT[1].render(text, True, self.COLOR)
        self.hover_text_rect = self.hover_text_surf.get_rect()
        self.hover_text_rect.center = center

    #update khi có sự kiện 
    def update(self):
        #lấy vị trí của con trỏ chuột
        x, y = pg.mouse.get_pos()

        #sự kiện hover
        if self.rect.collidepoint(x, y):
            self.hover_active = True
        else:
            self.hover_active = False

    def draw(self):
        #button khi được hover
        if self.hover_active:
            pg.draw.rect(self.surface, self.COLOR, self.hover_rect, 2, 20)
            self.surface.blit(self.hover_text_surf, self.hover_text_rect)
            
        #button ở trạng thái bình thường
        else:
            pg.draw.rect(self.surface, self.COLOR, self.rect, 2, 20)
            self.surface.blit(self.text_surf, self.text_rect)
            
class Button1:
    #set font và màu
    FONT = [
        pg.font.Font("fonts\RetroFont.ttf", 50),
        pg.font.Font("fonts\RetroFont.ttf", 55),
    ]
    COLOR = "#27E7C9"

    #tạo các thuộc tính cơ bản cho button
    def __init__(self, surface: pg.Surface,
                center: tuple[int, int],
                text: str):
        self.surface = surface

        self.w = 300
        self.h = 80
        
        
        self.x = center[0] - self.w // 2
        self.y = center[1] - self.h // 2

        #giá trị hover
        self.hover_active = False

        #vẽ viền cho cho button
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        
        #viền của button khi hover = True
        self.hover_rect = pg.Rect(self.x - 5, self.y - 5, self.w + 10, self.h + 10)

        #nội dung được ghi trên button
        self.text_surf = self.FONT[0].render(text, True, self.COLOR)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = center

        #nội dung được ghi trên button khi hover = True
        self.hover_text_surf = self.FONT[1].render(text, True, self.COLOR)
        self.hover_text_rect = self.hover_text_surf.get_rect()
        self.hover_text_rect.center = center

    #update khi có sự kiện 
    def update1(self):
        #lấy vị trí của con trỏ chuột
        x, y = pg.mouse.get_pos()

        #sự kiện hover
        if self.rect.collidepoint(x, y):
            self.hover_active = True
        else:
            self.hover_active = False

    def draw1(self):
        #button khi được hover
        if self.hover_active:
            pg.draw.rect(self.surface, self.COLOR, self.hover_rect, 2, 20)
            self.surface.blit(self.hover_text_surf, self.hover_text_rect)
            
        #button ở trạng thái bình thường
        else:
            pg.draw.rect(self.surface, self.COLOR, self.rect, 2, 20)
            self.surface.blit(self.text_surf, self.text_rect)