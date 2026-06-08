import pygame
import math
import random
import os

# Инициализация
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PANEL_WIDTH = 500
PANEL_HEIGHT = 350

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (200, 60, 60)
GREEN = (50, 205, 50)
BLUE = (30, 144, 255)
DARK_BLUE = (20, 20, 40)
LIGHT_GRAY = (180, 180, 180)
BG_COLOR = (15, 15, 25)

def draw_checkmark(surface, x, y, color=GREEN, size=16):
    """Рисует галочку вручную"""
    points = [
        (x, y + size // 2),
        (x + size // 3, y + size),
        (x + size, y)
    ]
    pygame.draw.lines(surface, color, False, points, 3)

def draw_cross(screen, x, y, color=RED, size=12):
    """Рисует крестик"""
    pygame.draw.line(screen, color, (x, y), (x + size, y + size), 2)
    pygame.draw.line(screen, color, (x + size, y), (x, y + size), 2)

# # Использование
# if has_amount:
#     draw_checkmark(screen, card_rect.right - 25, card_rect.centery - 8, GREEN, 12)
# else:
#     draw_cross(screen, card_rect.right - 25, card_rect.centery - 8, RED, 12)


class CraftPanel:
    def __init__(self, item_icon, item_name, ingredients):
        self.item_icon = item_icon
        self.item_name = item_name
        self.ingredients = ingredients  # [(icon, name, required), ...]
        self.crafting = False
        self.progress = 0
        self.message = ""
        self.message_time = 0
        self.particles = []
        
    def draw(self, screen, fonts):
        # Панель с полупрозрачным фоном
        panel_rect = pygame.Rect(SCREEN_WIDTH//2 - PANEL_WIDTH//2, 
                                  SCREEN_HEIGHT//2 - PANEL_HEIGHT//2, 
                                  PANEL_WIDTH, PANEL_HEIGHT)
        
        # Фон панели
        panel_surface = pygame.Surface((PANEL_WIDTH, PANEL_HEIGHT), pygame.SRCALPHA)
        panel_surface.fill((30, 30, 50, 230))
        pygame.draw.rect(panel_surface, GOLD, panel_surface.get_rect(), 2, border_radius=10)
        screen.blit(panel_surface, panel_rect)
        
        # ===== ЛЕВАЯ ЧАСТЬ: Иконка =====
        icon_rect = pygame.Rect(panel_rect.x + 30, panel_rect.y + 50, 180, 200)
        
        # Рамка для иконки
        pygame.draw.rect(screen, GOLD, icon_rect, 2, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0, 100), icon_rect, border_radius=8)
        
        # Анимация пульсации
        if not self.crafting:
            scale = 1 + math.sin(pygame.time.get_ticks() * 0.003) * 0.03
        else:
            scale = 1 + math.sin(pygame.time.get_ticks() * 0.01) * 0.05
        
        # Иконка
        if self.item_icon:
            new_size = (int(120 * scale), int(120 * scale))
            scaled_icon = pygame.transform.scale(self.item_icon, new_size)
            icon_x = icon_rect.centerx - scaled_icon.get_width() // 2
            icon_y = icon_rect.centery - scaled_icon.get_height() // 2
            screen.blit(scaled_icon, (icon_x, icon_y))
        
        # Название
        name_text = fonts['title'].render(self.item_name, True, GOLD)
        screen.blit(name_text, (icon_rect.centerx - name_text.get_width()//2, icon_rect.bottom + 10))
        
        # ===== ПРАВАЯ ЧАСТЬ: Ингредиенты =====
        ing_rect = pygame.Rect(panel_rect.x + 240, panel_rect.y + 50, 230, 200)
        
        # Заголовок
        title_text = fonts['text'].render("Требуется:", True, WHITE)
        screen.blit(title_text, (ing_rect.x, ing_rect.y))
        
        # Список ингредиентов
        y = ing_rect.y + 35
        for icon, name, required in self.ingredients:
            # Карточка ингредиента
            card_rect = pygame.Rect(ing_rect.x, y, ing_rect.width, 50)
            pygame.draw.rect(screen, (50, 50, 70), card_rect, border_radius=5)
            pygame.draw.rect(screen, LIGHT_GRAY, card_rect, 1, border_radius=5)
            
            # Иконка
            if icon:
                small_icon = pygame.transform.scale(icon, (40, 40))
                screen.blit(small_icon, (card_rect.x + 5, card_rect.y + 5))
            
            # Название и количество
            name_text = fonts['small'].render(f"{name}", True, WHITE)
            screen.blit(name_text, (card_rect.x + 55, card_rect.y + 8))
            
            need_text = fonts['small'].render(f"x{required}", True, GOLD)
            screen.blit(need_text, (card_rect.x + 55, card_rect.y + 28))
            
            # Галочка (всегда зеленая для демо)
            draw_checkmark(screen, card_rect.right - 25, card_rect.centery - 8)
            
            y += 58
        
        # ===== КНОПКА КРАФТА =====
        button_rect = pygame.Rect(panel_rect.centerx - 100, panel_rect.bottom - 60, 200, 45)
        
        # Тень
        pygame.draw.rect(screen, BLACK, button_rect.move(3, 3), border_radius=8)
        
        if self.crafting:
            # Прогресс
            progress_width = int(200 * (self.progress / 100))
            progress_rect = pygame.Rect(button_rect.x, button_rect.y, progress_width, 45)
            pygame.draw.rect(screen, GREEN, progress_rect, border_radius=8)
            pygame.draw.rect(screen, GOLD, button_rect, 2, border_radius=8)
            
            percent_text = fonts['text'].render(f"{int(self.progress)}%", True, WHITE)
            screen.blit(percent_text, (button_rect.centerx - percent_text.get_width()//2, 
                                       button_rect.centery - 8))
            
            # Частицы
            self.update_particles()
            self.draw_particles(screen)
        else:
            # Кнопка
            pygame.draw.rect(screen, BLUE, button_rect, border_radius=8)
            pygame.draw.rect(screen, GOLD, button_rect, 2, border_radius=8)
            button_text = fonts['text'].render("КРАФТ", True, WHITE)
            screen.blit(button_text, (button_rect.centerx - button_text.get_width()//2, 
                                     button_rect.centery - 8))
        
        # Сообщение
        if self.message_time > 0:
            msg_text = fonts['small'].render(self.message, True, GREEN if "создан" in self.message else RED)
            screen.blit(msg_text, (panel_rect.centerx - msg_text.get_width()//2, panel_rect.y - 30))
            self.message_time -= 1
        
        return button_rect
    
    def draw_particles(self, screen):
        for p in self.particles:
            alpha = int(255 * p['life'])
            color = (GREEN[0], GREEN[1], GREEN[2], alpha)
            particle_surf = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (p['size'], p['size']), p['size'])
            screen.blit(particle_surf, (int(p['x'] - p['size']), int(p['y'] - p['size'])))
    
    def update_particles(self):
        # Добавляем частицы
        if self.crafting and random.randint(0, 3) == 0:
            angle = random.uniform(0, 2 * math.pi)
            radius = random.randint(80, 200)
            center_x = SCREEN_WIDTH // 2
            center_y = SCREEN_HEIGHT // 2
            self.particles.append({
                'x': center_x + math.cos(angle) * radius,
                'y': center_y + math.sin(angle) * radius,
                'life': 1.0,
                'size': random.randint(2, 5)
            })
        
        # Обновляем
        for p in self.particles[:]:
            p['life'] -= 0.03
            if p['life'] <= 0:
                self.particles.remove(p)
    
    def update(self, dt):
        if self.crafting:
            self.progress += dt * 20  # 5 секунд до 100%
            if self.progress >= 100:
                self.crafting = False
                self.progress = 0
                self.message = f"{self.item_name} создан!"
                self.message_time = 120
                return True
        return False
    
    def start_craft(self):
        if not self.crafting:
            self.crafting = True
            self.progress = 0
            self.particles = []
            return True
        return False

def load_image(path, default_color, size):
    if os.path.exists(path):
        return pygame.image.load(path).convert_alpha()
    # Создаем заглушку
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill(default_color)
    pygame.draw.rect(surf, WHITE, surf.get_rect(), 2)
    return surf

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Крафт")
    clock = pygame.time.Clock()
    
    # Шрифты
    fonts = {
        'title': pygame.font.Font(None, 28),
        'text': pygame.font.Font(None, 24),
        'small': pygame.font.Font(None, 18)
    }
    
    # Загрузка иконок (укажите свои пути)
    item_icon = load_image("items_transparent/BOOM.png", (150, 50, 50), (120, 120))
    ing1_icon = load_image("items_transparent/G117.png", (80, 80, 80), (40, 40))
    ing2_icon = load_image("items_transparent/ACCU.png", (0, 100, 0), (40, 40))
    
    # Данные
    ingredients = [
        (ing1_icon, "Геопак с красноскалом", 2),
        (ing2_icon, "Аккумулятор", 1),
    ]
    
    # Панель
    panel = CraftPanel(item_icon, "ПЛАЗМЕННАЯ БОМБА", ingredients)
    
    # Звезды для фона
    stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 
              random.randint(1, 2), random.randint(100, 255)) for _ in range(80)]
    
    running = True
    craft_request = False
    
    while running:
        # Фон
        screen.fill(BG_COLOR)
        for x, y, size, alpha in stars:
            star_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(star_surf, (255, 255, 255, alpha), (size, size), size)
            screen.blit(star_surf, (x, y))
        
        dt = clock.get_time() / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                craft_request = True
        
        # Отрисовка панели
        button_rect = panel.draw(screen, fonts)
        
        # Обработка клика
        if craft_request and button_rect.collidepoint(pygame.mouse.get_pos()):
            panel.start_craft()
        craft_request = False
        
        # Обновление
        panel.update(dt)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()