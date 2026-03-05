import pygame
import sys
from my_lib.GameObjectRenderer import GameObject


class TextInput(GameObject):
    def __init__(self, ctx, screen, x, y, width, height, max_length=20):
        super().__init__(1000)
        self.ctx = ctx
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.max_length = max_length
        self.active = False
        self.color_inactive = (100, 100, 100)
        self.color_active = (200, 200, 200)
        self.color = self.color_inactive
        self.cursor_visible = True
        self.cursor_timer = 0
        self.font = pygame.font.Font(None, 20)
        self.is_active = False
        self.id_cmd = None
        self.num_cmd = 0

        # Новые атрибуты для выделения текста
        self.text_selected = False
        self.selection_start = 0
        self.selection_end = 0
        self.cursor_position = 0  # Позиция курсора в тексте

    def _execute(self):
        pass

    def _update(self):
        if self.is_active and self.active:
            self.cursor_timer += 1
            if self.cursor_timer >= 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

    def _draw(self):
        if self.is_active:
            # Матричный зеленый
            text_color = (0, 255, 255)  # Ярко-зеленый
            glow_color = (0, 150, 0)  # Темно-зеленый для свечения
            
            text_surface = self.font.render(self.text, True, text_color)
            
            # Эффект свечения
            glow_surface = self.font.render(self.text, True, glow_color)

            # center
            x, y = self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2
            text_rect = glow_surface.get_rect(center=(x, y))
            self.screen.blit(glow_surface, text_rect)
            text_rect.centerx = x - 1
            text_rect.centery = y - 1
            self.screen.blit(glow_surface, text_rect)
            text_rect.centerx = x + 1
            text_rect.centery = y + 1
            self.screen.blit(glow_surface, text_rect)
            
            # Основной текст поверх
            text_rect.centerx = x
            text_rect.centery = y
            self.screen.blit(text_surface, text_rect)
            
            # Курсор
            if self.active and self.cursor_visible:
                cursor_x = x + text_surface.get_width() // 2
                cursor_y = y - text_surface.get_height() // 2
                cursor_height = text_surface.get_height()
                pygame.draw.line(self.screen, text_color, 
                            (cursor_x, cursor_y), 
                            (cursor_x, cursor_y + cursor_height), 3)
            pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.ctx.pro._values[self.id_cmd][self.num_cmd] = self.text
                self.ctx.grid.update_cell_image(self.id_cmd, self.ctx.cmd_list[self.id_cmd])
                self.ctx.re_grid = True
                print(f"Введенный текст: {self.text}")
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length and event.unicode.isprintable():
                self.text += event.unicode
    
    def set_max_length(self, num):
        self.max_length = num

    def set_rect(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def on_active(self):
        self.is_active = True
    
    def off_active(self):
        self.is_active = False

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    input_field = TextInput(100, 100, 64, 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            input_field.handle_event(event)
        
        input_field._update()
        
        screen.fill((30, 30, 30))
        input_field._draw(screen)
        
        pygame.display.flip()
        clock.tick(60)