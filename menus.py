"""Menu and UI screens for Dodger game"""
import pygame
import sys

# Cache checkerboard pattern globally to avoid redrawing every frame
_checkerboard_cache = {}

def _create_checkerboard_surface(WIDTH, HEIGHT):
    """Create a cached checkerboard surface"""
    key = (WIDTH, HEIGHT)
    if key not in _checkerboard_cache:
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill((120, 80, 160))
        for x in range(0, WIDTH, 40):
            for y in range(0, HEIGHT, 40):
                if (x // 40 + y // 40) % 2 == 0:
                    pygame.draw.rect(surface, (140, 100, 180), (x, y, 40, 40))
        _checkerboard_cache[key] = surface
    return _checkerboard_cache[key]

def draw_checkerboard_bg(screen, WIDTH, HEIGHT):
    """Draw purple checkerboard background (cached for performance)"""
    cached_bg = _create_checkerboard_surface(WIDTH, HEIGHT)
    screen.blit(cached_bg, (0, 0))

def draw_button(screen, rect, text, is_selected, font, text_color=(255, 255, 255)):
    """Draw a button with selection state"""
    if is_selected:
        btn_color = (255, 100, 150)
        border_color = (255, 200, 100)
        border_width = 4
    else:
        btn_color = (200, 80, 120)
        border_color = (200, 200, 200)
        border_width = 2
    
    pygame.draw.rect(screen, btn_color, rect, border_radius=15)
    pygame.draw.rect(screen, border_color, rect, border_width, border_radius=15)
    
    text_obj = font.render(text, True, text_color)
    text_rect = text_obj.get_rect(center=rect.center)
    screen.blit(text_obj, text_rect)

def help_screen(screen, font, big_font, WIDTH, HEIGHT, clock):
    """Display help/instructions screen"""
    while True:
        clock.tick(60)
        draw_checkerboard_bg(screen, WIDTH, HEIGHT)
        
        title = big_font.render(u"TRỢ GIÚP", True, (255, 150, 100))
        title_rect = title.get_rect(center=(WIDTH//2, 50))
        screen.blit(title, title_rect)
        
        helps = [
            u"← → : Chuyển động trái/phải",
            u"SPACE : Nhảy (bấm 2 lần = Nhảy kép cao gấp đôi)",
            u"ESC : Tạm dừng trò chơi",
            u"Thu thập toàn bộ coin để mở cổng đích",
            u"Trả lời câu hỏi Python khi gặp quái vật",
            u"Trả lời đúng 1 câu để hồi sinh và tiếp tục",
        ]
        
        y_pos = 130
        for line in helps:
            text = font.render(line, True, (255, 255, 200))
            text_rect = text.get_rect(center=(WIDTH//2, y_pos))
            screen.blit(text, text_rect)
            y_pos += 60
        
        hint = font.render(u"Nhấn ENTER để quay lại", True, (200, 200, 255))
        hint_rect = hint.get_rect(center=(WIDTH//2, 550))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
