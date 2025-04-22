import pygame
import random
import math
import os

class Planet:
    def __init__(self, img):
        self.img = img
        self.width, self.height = img.get_size()
        
        # Vị trí ban đầu ngẫu nhiên
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-self.height, -10)  # Bắt đầu từ phía trên màn hình
        
        # Tốc độ di chuyển dọc (chậm)
        self.speed_y = random.uniform(0.2, 0.8)
        
        # Thông số xoay vòng
        self.orbit_radius = random.randint(50, 150)  # Bán kính quỹ đạo xoay
        self.orbit_speed = random.uniform(0.005, 0.02)  # Tốc độ xoay
        self.orbit_angle = random.uniform(0, 2 * math.pi)  # Góc ban đầu
        
        # Tự xoay quanh trục
        self.rotation = 0
        self.rotation_speed = random.uniform(-1, 1)
        
        # Vị trí trung tâm của quỹ đạo (sẽ di chuyển dọc theo thời gian)
        self.center_x = self.x
        self.center_y = self.y
        
    def update(self):
        # Di chuyển dọc xuống dưới
        self.center_y += self.speed_y
        
        # Cập nhật góc quỹ đạo
        self.orbit_angle += self.orbit_speed
        
        # Tính vị trí mới dựa trên quỹ đạo xoay
        self.x = self.center_x + math.cos(self.orbit_angle) * self.orbit_radius
        self.y = self.center_y + math.sin(self.orbit_angle) * self.orbit_radius
        
        # Tự xoay quanh trục
        self.rotation += self.rotation_speed
        
        # Nếu hành tinh đi ra khỏi màn hình, đặt lại phía trên
        if self.center_y > HEIGHT + self.height:
            self.center_y = random.randint(-self.height, -10)
            self.center_x = random.randint(0, WIDTH)
            self.y = self.center_y
    
    def draw(self, surface):
        rotated_img = pygame.transform.rotate(self.img, self.rotation)
        surface.blit(rotated_img, (self.x - rotated_img.get_width()/2, 
                                  self.y - rotated_img.get_height()/2))

class Meteor:
    def __init__(self):
        self.angle = random.uniform(math.pi/4, math.pi/3)
        self.speed = random.uniform(5, 10)
        self.lifetime = random.randint(30, 60)
        self.active = False
        self.reset()
        
    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT//2)
        self.active = True
        self.lifetime = random.randint(30, 60)
        
    def update(self):
        if not self.active:
            if random.random() < 0.005:
                self.reset()
            return
        
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.lifetime -= 1
        
        if self.lifetime <= 0 or self.x > WIDTH or self.y > HEIGHT:
            self.active = False
    
    def draw(self, surface):
        if not self.active or meteor_img is None:
            return
            
        angle_deg = -math.degrees(self.angle)
        rotated_meteor = pygame.transform.rotate(meteor_img, angle_deg)
        surface.blit(rotated_meteor, (self.x, self.y))

def load_space_assets(width, height):
    global WIDTH, HEIGHT, space_bg, planets_img, meteor_img, star_img
    WIDTH, HEIGHT = width, height
    
    # Tải hình ảnh nền
    try:
        space_bg = pygame.image.load(os.path.join('data','bg.jpg')).convert()
        space_bg = pygame.transform.scale(space_bg, (WIDTH, HEIGHT))
    except:
        space_bg = None

    # Tải hình ảnh các hành tinh
    planets_img = []
    for i in range(1, 3):  
        try:
            img = pygame.image.load(os.path.join('data',f'planet{i}.png')).convert_alpha()
            scale = random.uniform(0.2, 0.5)
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            planets_img.append(img)
        except:
            print(f"Không tìm thấy hình planet{i}.png")
            dummy_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(dummy_surf, (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)), 
                            (50, 50), 50)
            planets_img.append(dummy_surf)

    # Tải hình sao băng
    try:
        meteor_img = pygame.image.load(os.path.join('data','meteor.png')).convert_alpha()
        meteor_img = pygame.transform.scale(meteor_img, (60, 30))
    except:
        meteor_img = None

    # Tải hình ngôi sao
    try:
        star_img = pygame.image.load(os.path.join('data','star.png')).convert_alpha()
        star_img = pygame.transform.scale(star_img, (20, 20))
    except:
        star_img = None

    # Tạo các ngôi sao nhỏ
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]
    
    # Tạo các đối tượng
    planets = [Planet(random.choice(planets_img)) for _ in range(3)]
    meteors = [Meteor() for _ in range(5)]
    
    return {
        'bg': space_bg,
        'planets': planets,
        'meteors': meteors,
        'stars': stars,
        'star_img': star_img
    }