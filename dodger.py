"""
PYTHON ADVENTURE - GIẢI CỨU CHIM CÁNH CỤT
Main Game File (Refactored & Modular)

Modules used:
- maps.py: Map configurations
- question.py: Question system  
- menus.py: UI/Menu functions
- constants.py: Game constants
- characters.py: Character customization system
"""

import pygame
import sys
import os
import random
import math

# Initialize pygame
pygame.init()

# Import from modules
from constants import (
    WIDTH, HEIGHT, FPS, MAP_WIDTH,
    DIFFICULTY_SETTINGS,
    COLOR_BG, COLOR_PURPLE_LIGHT, COLOR_PURPLE_DARK,
    PLAYER_WIDTH, PLAYER_HEIGHT, MONSTER_WIDTH, MONSTER_HEIGHT,
    COIN_SIZE, PORTAL_SIZE, MAX_PLAYER_NAME_LENGTH
)
from maps import MAPS, get_map, get_map_names
from question import QuestionSystem, QUESTIONS_DB
from menus import draw_checkerboard_bg, draw_button, help_screen
from items import ItemManager, ItemType, apply_item_effects
from enemies import MonsterManager, Monster

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PYTHON ADVENTURE")
clock = pygame.time.Clock()

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITES_DIR = os.path.join(BASE_DIR, "sprites")

# ============== FONT & ASSETS ==============
font = pygame.font.SysFont("segoe ui", 27)
big_font = pygame.font.SysFont("segoe ui", 52)

def load_img(path):
    """Load image with error handling"""
    try:
        if os.path.exists(path):
            return pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"⚠️  Lỗi tải: {path}")
    return None

def nearest_scale(img, size):
    """Scale pixel art with nearest-neighbor"""
    if img is None:
        return None
    img = img.convert_alpha()
    src_w, src_h = img.get_size()
    dst_w, dst_h = size
    if src_w > 0 and src_h > 0 and dst_w % src_w == 0 and dst_h % src_h == 0:
        return pygame.transform.scale(img, (dst_w, dst_h)).convert_alpha()
    return pygame.transform.scale(img, size).convert_alpha()

# Load essential sprites
player_idle_img = load_img(os.path.join(SPRITES_DIR, "Player", "Idle_1.png"))
player_run_imgs = [load_img(os.path.join(SPRITES_DIR, "Player", f"run_{i}.png")) for i in range(1, 7)]
player_jump_img = load_img(os.path.join(SPRITES_DIR, "Player", "jump_1.png"))

# Monster images
monster_images = []
for i in range(1, 5):
    monster_path = os.path.join(BASE_DIR, f"{i}_0.png")
    img = load_img(monster_path)
    if img:
        monster_images.append(nearest_scale(img, (60, 60)))
if not monster_images:
    monster_images = [None]

# Coin image - optimized with transparency and colorkey
coin_img = load_img(os.path.join(BASE_DIR, "xu.png"))
if coin_img:
    coin_img = coin_img.convert_alpha()  # Preserve alpha/transparency
    # Remove white background using colorkey
    coin_img.set_colorkey((255, 255, 255))
    coin_img = nearest_scale(coin_img, (30, 30))
    coin_img = coin_img.convert_alpha()  # Final optimization

# Load background tiles
def load_tile_set(subfolder, prefix):
    """Load tile set from sprites folder"""
    path = os.path.join(SPRITES_DIR, "Tile", subfolder)
    tiles = []
    if os.path.isdir(path):
        for fname in sorted(os.listdir(path)):
            if fname.lower().startswith(prefix.lower()) and fname.lower().endswith(('.png', '.jpg')):
                img = load_img(os.path.join(path, fname))
                if img:
                    tiles.append(nearest_scale(img, (40, 40)))
    return tiles

ground_tiles = load_tile_set("Ground", "ground_")
if not ground_tiles:
    ground_tiles = [None]

# Scale player images
if player_idle_img:
    player_idle_img = nearest_scale(player_idle_img, (60, 60))
if player_jump_img:
    player_jump_img = nearest_scale(player_jump_img, (60, 60))
player_run_imgs = [nearest_scale(img, (60, 60)) if img else player_idle_img for img in player_run_imgs]

# Fallback images
player_img = player_idle_img if player_idle_img else pygame.Surface((60, 60))

# ============== MENU SCREENS ==============
def player_name_screen():
    """Input player name screen"""
    player_name = ""
    pygame.key.set_text_input_rect(pygame.Rect(WIDTH//2 - 150, 250, 300, 60))
    
    while True:
        clock.tick(FPS)
        draw_checkerboard_bg(screen, WIDTH, HEIGHT)
        
        title = big_font.render(u"NHẬP TÊN CỦA BẠN", True, (255, 100, 150))
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        screen.blit(title, title_rect)
        
        subtitle = font.render(u"Nhập tên người chơi:", True, (255, 255, 255))
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 180))
        screen.blit(subtitle, subtitle_rect)
        
        # Input box
        input_box = pygame.Rect(WIDTH//2 - 150, 250, 300, 60)
        pygame.draw.rect(screen, (200, 200, 200), input_box, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 3, border_radius=10)
        
        display_name = player_name if player_name else u"Nhập tên..."
        name_text = font.render(display_name, True, (0, 0, 0))
        screen.blit(name_text, (input_box.x + 20, input_box.y + 15))
        
        char_count = font.render(f"{len(player_name)}/{MAX_PLAYER_NAME_LENGTH}", True, (200, 255, 200))
        screen.blit(char_count, (WIDTH//2 + 160, 260))
        
        hint = font.render(u"Nhấn ENTER để tiếp tục, ESC để bỏ qua", True, (180, 180, 180))
        hint_rect = hint.get_rect(center=(WIDTH//2, 390))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    return player_name.strip() if player_name.strip() else u"Người Chơi"
                elif event.key == pygame.K_ESCAPE:
                    return u"Người Chơi"
            elif event.type == pygame.TEXTINPUT:
                if len(player_name) < MAX_PLAYER_NAME_LENGTH and event.text not in ('\r', '\n'):
                    player_name += event.text


def difficulty_popup():
    """Select difficulty popup"""
    selected = 0
    difficulty_names = [u"Dễ", u"Bình Thường", u"Khó", u"Cực Khó"]
    difficulty_keys = list(DIFFICULTY_SETTINGS.keys())
    
    while True:
        clock.tick(FPS)
        draw_checkerboard_bg(screen, WIDTH, HEIGHT)
        
        title = big_font.render(u"CHỌN CHẾ ĐỘ", True, (255, 200, 100))
        title_rect = title.get_rect(center=(WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        for idx, diff_name in enumerate(difficulty_names):
            btn = pygame.Rect(WIDTH//2 - 180, 200 + idx * 80, 360, 70)
            is_selected = (idx == selected)
            draw_button(screen, btn, diff_name, is_selected, font)
        
        hint = font.render(u"↑↓ chọn, ENTER xác nhận", True, (200, 200, 255))
        hint_rect = hint.get_rect(center=(WIDTH//2, 540))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulty_names)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulty_names)
                elif event.key == pygame.K_RETURN:
                    return difficulty_keys[selected]
                elif event.key == pygame.K_ESCAPE:
                    return "Normal"


def map_popup():
    """Select map popup"""
    selected = 0
    
    while True:
        clock.tick(FPS)
        draw_checkerboard_bg(screen, WIDTH, HEIGHT)
        
        title = big_font.render(u"CHỌN BẠN ĐỖ", True, (255, 200, 100))
        title_rect = title.get_rect(center=(WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        for idx, map_info in enumerate(MAPS):
            btn = pygame.Rect(WIDTH//2 - 180, 200 + idx * 80, 360, 70)
            is_selected = (idx == selected)
            draw_button(screen, btn, map_info['name'], is_selected, font)
        
        hint = font.render(u"↑↓ chọn, ENTER xác nhận", True, (200, 200, 255))
        hint_rect = hint.get_rect(center=(WIDTH//2, 540))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(MAPS)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(MAPS)
                elif event.key == pygame.K_RETURN:
                    return selected
                elif event.key == pygame.K_ESCAPE:
                    return 0


def main_menu():
    """Main menu with difficulty and map selection"""
    selected = 0
    current_difficulty = "Normal"
    current_map = 0
    
    difficulty_names = {
        "Easy": u"Dễ",
        "Normal": u"Bình Thường",
        "Hard": u"Khó",
        "Insane": u"Cực Khó"
    }
    
    while True:
        clock.tick(FPS)
        draw_checkerboard_bg(screen, WIDTH, HEIGHT)
        
        # Draw penguin icons beside title
        if player_idle_img:
            screen.blit(player_idle_img, (50, 10))
            flipped = pygame.transform.flip(player_idle_img, True, False)
            screen.blit(flipped, (WIDTH - 110, 10))
        
        # Title
        title = big_font.render(u"GIẢI CỨU CHIM CÁNH CỤT", True, (255, 100, 150))
        title_rect = title.get_rect(center=(WIDTH//2, 50))
        screen.blit(title, title_rect)
        
        # Menu buttons
        buttons = [
            (u"Bản Đồ: " + MAPS[current_map]['name'].split(" - ")[0], 0),
            (u"Chế Độ: " + difficulty_names[current_difficulty], 1),
            (u"BẮT ĐẦU", 2),
            (u"TRỢ GIÚP", 3)
        ]
        
        for idx, (text_str, _) in enumerate(buttons):
            btn = pygame.Rect(WIDTH//2 - 200, 180 + idx * 90, 400, 80)
            is_selected = (idx == selected)
            draw_button(screen, btn, text_str, is_selected, font)
        
        hint = font.render(u"↑↓ chọn, ENTER xác nhận", True, (200, 200, 255))
        hint_rect = hint.get_rect(center=(WIDTH//2, 560))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(buttons)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        current_map = map_popup()
                    elif selected == 1:
                        current_difficulty = difficulty_popup()
                    elif selected == 2:
                        return (current_difficulty, current_map)
                    elif selected == 3:
                        help_screen(screen, font, big_font, WIDTH, HEIGHT, clock)


# ============== GAME SCREENS ==============
def show_game_over():
    """Game Over screen"""
    selected = 0
    buttons = [u"QUAY LẠI MENU", u"THOÁT GAME"]
    
    while True:
        clock.tick(FPS)
        draw_checkerboard_bg(screen, WIDTH, HEIGHT)
        
        title = big_font.render(u"HẾT CUỘC", True, (255, 100, 150))
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        screen.blit(title, title_rect)
        
        info = font.render(u"Bạn trả lời sai! Hãy thử lại...", True, (255, 255, 255))
        info_rect = info.get_rect(center=(WIDTH//2, 200))
        screen.blit(info, info_rect)
        
        for idx, btn_text in enumerate(buttons):
            btn = pygame.Rect(WIDTH//2 - 150, 300 + idx * 90, 300, 70)
            is_selected = (idx == selected)
            
            if is_selected:
                btn_color = (100, 200, 100) if idx == 0 else (200, 100, 100)
                border_color = (255, 255, 100)
                border_width = 4
            else:
                btn_color = (80, 160, 80) if idx == 0 else (160, 80, 80)
                border_color = (200, 200, 200)
                border_width = 2
            
            pygame.draw.rect(screen, btn_color, btn, border_radius=15)
            pygame.draw.rect(screen, border_color, btn, border_width, border_radius=15)
            
            text = font.render(btn_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=btn.center)
            screen.blit(text, text_rect)
        
        hint = font.render(u"↑↓ chọn, ENTER xác nhận", True, (200, 200, 255))
        hint_rect = hint.get_rect(center=(WIDTH//2, 540))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(buttons)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return True
                    else:
                        pygame.quit(); sys.exit()


def show_map_complete():
    """Level completion screen"""
    while True:
        clock.tick(FPS)
        draw_checkerboard_bg(screen, WIDTH, HEIGHT)
        
        title = big_font.render(u"HOÀN THÀNH BẠN ĐỖ!", True, (0, 255, 100))
        title_rect = title.get_rect(center=(WIDTH//2, 150))
        screen.blit(title, title_rect)
        
        subtitle = font.render(u"Bạn đã thu thập tất cả coin!", True, (255, 255, 255))
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 250))
        screen.blit(subtitle, subtitle_rect)
        
        continue_text = font.render(u"Nhấn ENTER để tiếp tục", True, (255, 200, 0))
        continue_rect = continue_text.get_rect(center=(WIDTH//2, 350))
        screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return


# ============== GAME LOOP ==============
def game(map_index=0, player_name="Người Chơi", difficulty="Normal"):
    """Main game loop"""
    
    map_info = get_map(map_index)
    current_bg = map_info.get('background_img')
    
    # Load map background
    if map_info.get('background_file'):
        map_bg_path = os.path.join(BASE_DIR, map_info['background_file'])
        current_bg = load_img(map_bg_path)
    
    # Player setup
    player_size = (PLAYER_WIDTH, PLAYER_HEIGHT)
    player = pygame.Rect(100, 450, *player_size)
    vel_y = 0
    jump_count = 0
    run_frame = 0
    run_counter = 0
    player_facing_right = True
    last_player_x = player.x
    
    # Monster setup - using new MonsterManager
    monster_img = monster_images[map_index % len(monster_images)]
    monster_manager = MonsterManager(difficulty)
    monster_manager.add_monster(700, 450)  # Spawn initial monster
    
    # Item setup - using new ItemManager
    item_manager = ItemManager()
    platforms_list = [pygame.Rect(*p) for p in map_info['platforms']]
    item_manager.add_coins_from_platforms(platforms_list)
    item_manager.add_random_powerups(platforms_list, chance=0.15)
    
    # Game settings
    diff_settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])
    speed = diff_settings['player_speed']
    gravity = diff_settings['gravity']
    jump_power = diff_settings['jump_power']
    monster_speed = diff_settings['monster_speed']
    
    # Level setup
    platforms = platforms_list
    coins = item_manager.get_uncollected_items()
    jump_pads_data = map_info.get('jump_pads', [])
    jump_pads = [pygame.Rect(x, y, w, h) for x, y, w, h, _ in jump_pads_data]
    
    portal = None
    portal_x = map_info.get('portal_x', MAP_WIDTH - 200)
    camera_x = 0
    pause = False
    question_system = QuestionSystem()
    
    # ===== Game Loop =====
    while True:
        clock.tick(FPS)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
                elif event.key == pygame.K_SPACE and not pause and jump_count < 2:
                    vel_y = jump_power
                    jump_count += 1
        
        if pause:
            continue
        
        # Player movement
        keys = pygame.key.get_pressed()
        player_moving = False
        
        if keys[pygame.K_LEFT]:
            player.x -= speed
            player_facing_right = False
            player_moving = True
        elif keys[pygame.K_RIGHT]:
            player.x += speed
            player_facing_right = True
            player_moving = True
        
        # Keep player in bounds
        player.x = max(0, min(player.x, MAP_WIDTH - player.width))
        
        # Update animation frame
        if player_moving:
            run_counter += 1
            if run_counter >= 8:  # Change frame every 8 ticks
                run_frame = (run_frame + 1) % len(player_run_imgs)
                run_counter = 0
        else:
            run_frame = 0
            run_counter = 0
        
        # Apply gravity
        vel_y += gravity
        player.y += vel_y
        
        # Platform collisions
        for p in platforms:
            if player.colliderect(p) and vel_y > 0:
                player.bottom = p.top
                vel_y = 0
                jump_count = 0
        
        # Jump pad collisions
        for pad_rect, pad_data in zip(jump_pads, jump_pads_data):
            if player.colliderect(pad_rect) and vel_y > 0 and player.bottom <= pad_rect.top + 12:
                player.bottom = pad_rect.top
                vel_y = pad_data[4]
                jump_count = 1
        
        # Update items
        item_manager.update()
        
        # Check item collection
        collected_items = item_manager.check_collisions(player)
        for item in collected_items:
            item_manager.collect(item, player)
        
        # Create portal when all items collected
        if not item_manager.get_uncollected_items() and portal is None:
            portal = pygame.Rect(portal_x, 300, PORTAL_SIZE, PORTAL_SIZE)
        
        # Check portal collision - win condition
        if portal and player.colliderect(portal):
            show_map_complete()
            return
        
        # Update monster AI using MonsterManager
        monster_manager.update_all(platforms, player.x, player.y)
        
        # Apply powerup effects to player
        adjusted_speed, adjusted_jump = apply_item_effects(item_manager, {
            'speed': speed,
            'jump_power': jump_power
        })
        
        # Check monster collisions with player
        collided_monsters = monster_manager.check_collisions(player)
        if collided_monsters and not item_manager.is_protected():
            question_system.get_question(difficulty)
            # Show question screen
            if not ask_python_question(question_system, difficulty):
                show_game_over()
                return
            # Reset monster position after collision
            monster_manager.reset_monster(0, player.x)
        
        # Update camera to follow player (centered on screen)
        camera_x = max(0, min(player.x - WIDTH // 3, MAP_WIDTH - WIDTH))
        
        screen.fill(map_info.get('background_color', COLOR_BG))
        
        if current_bg:
            bg_width = current_bg.get_width()
            for x in range(0, MAP_WIDTH + WIDTH, bg_width):
                screen.blit(current_bg, (x - camera_x, 0))
        
        # Draw platforms with proper tiles
        for p in platforms:
            if ground_tiles and len(ground_tiles) > 0:
                for i in range(0, p.width, 40):
                    tile_idx = (i // 40) % len(ground_tiles)
                    if ground_tiles[tile_idx]:
                        screen.blit(ground_tiles[tile_idx], (p.x + i - camera_x, p.y))
                    else:
                        # Fallback: draw colored rectangle
                        pygame.draw.rect(screen, (100, 150, 100), (p.x + i - camera_x, p.y, min(40, p.width - i), p.height))
            else:
                # Fallback: solid colored platforms
                pygame.draw.rect(screen, (100, 150, 100), (p.x - camera_x, p.y, p.width, p.height))
        
        # Draw jump pads with glow effect
        for pad in jump_pads:
            # Main pad
            pygame.draw.rect(screen, (0, 210, 255), (pad.x - camera_x, pad.y, pad.width, pad.height))
            # Border glow
            pygame.draw.rect(screen, (100, 255, 255), (pad.x - camera_x, pad.y, pad.width, pad.height), 3)
        
        # Draw items (coins and powerups) - with improved rendering
        for item in item_manager.items:
            if item.collected:
                continue
            
            float_offset = 5 * math.sin(item.animation_timer * 0.02)
            y_pos = item.y + float_offset
            
            # Draw item without white background
            if item.item_type == ItemType.COIN:
                # Draw coin as beautiful golden circle
                x_center = int(item.x - camera_x + 15)
                y_center = int(y_pos + 15)
                
                # Outer golden glow
                pygame.draw.circle(screen, (255, 200, 0), (x_center, y_center), 14)
                # Coin body - bright yellow
                pygame.draw.circle(screen, (255, 255, 0), (x_center, y_center), 12)
                # Highlight for 3D effect
                pygame.draw.circle(screen, (255, 255, 100), (x_center - 3, y_center - 3), 5)
                # Border
                pygame.draw.circle(screen, (200, 180, 0), (x_center, y_center), 12, 2)
            else:
                # Draw powerup as colored circle with border
                color_map = {
                    ItemType.POWERUP_SHIELD: (0, 255, 100),
                    ItemType.POWERUP_SPEED: (255, 100, 0),
                    ItemType.POWERUP_JUMP: (100, 150, 255),
                    ItemType.POWERUP_SLOW: (255, 255, 100),
                    ItemType.HEAL: (255, 150, 200)
                }
                
                color = color_map.get(item.item_type, (200, 200, 200))
                x_center = int(item.x - camera_x + 15)
                y_center = int(y_pos + 15)
                
                # Draw glowing powerup
                pygame.draw.circle(screen, color, (x_center, y_center), 14)
                pygame.draw.circle(screen, (255, 255, 255), (x_center, y_center), 14, 2)
                
                # Inner highlight
                pygame.draw.circle(screen, (255, 255, 255), (x_center - 3, y_center - 3), 4)
        
        # Draw portal with animation
        if portal:
            portal_screen_x = portal.x - camera_x
            portal_screen_y = portal.y
            
            # Only draw if visible on screen
            if -PORTAL_SIZE < portal_screen_x < WIDTH:
                ticks = pygame.time.get_ticks()
                
                # Outer glowing aura
                aura_size = int(PORTAL_SIZE * 1.2 + 30 * math.sin(ticks / 500))
                pygame.draw.circle(screen, (100, 150, 255), 
                                  (int(portal_screen_x + PORTAL_SIZE//2), int(portal_screen_y + PORTAL_SIZE//2)), 
                                  aura_size // 2, 4)
                
                # Middle pulsing ring
                pulse_size = int(PORTAL_SIZE * (0.7 + 0.3 * math.sin(ticks / 400)))
                pygame.draw.circle(screen, (150, 200, 255), 
                                  (int(portal_screen_x + PORTAL_SIZE//2), int(portal_screen_y + PORTAL_SIZE//2)), 
                                  pulse_size // 2, 3)
                
                # Core portal circle with gradient effect
                core_size = PORTAL_SIZE // 2
                pygame.draw.circle(screen, (200, 255, 255), 
                                  (int(portal_screen_x + PORTAL_SIZE//2), int(portal_screen_y + PORTAL_SIZE//2)), 
                                  core_size)
                pygame.draw.circle(screen, (100, 200, 255), 
                                  (int(portal_screen_x + PORTAL_SIZE//2), int(portal_screen_y + PORTAL_SIZE//2)), 
                                  core_size - 8)
                
                # Inner rotating stars
                for i in range(3):
                    angle = (ticks / 100 + i * 120) * math.pi / 180
                    star_x = portal_screen_x + PORTAL_SIZE//2 + 25 * math.cos(angle)
                    star_y = portal_screen_y + PORTAL_SIZE//2 + 25 * math.sin(angle)
                    pygame.draw.circle(screen, (255, 255, 200), (int(star_x), int(star_y)), 4)
                
                # Portal label
                portal_text = font.render(u"CỔNG THOÁT", True, (255, 255, 100))
                portal_text_rect = portal_text.get_rect(center=(int(portal_screen_x + PORTAL_SIZE//2), 
                                                              int(portal_screen_y + PORTAL_SIZE + 25)))
                screen.blit(portal_text, portal_text_rect)
        
        
        # Draw monsters using MonsterManager
        monster_manager.draw_all(screen, camera_x, monster_img)
        
        # Draw player with running animation
        if jump_count > 0 or vel_y < 0:
            # Jumping state
            if player_jump_img:
                if player_facing_right:
                    screen.blit(player_jump_img, (player.x - camera_x, player.y))
                else:
                    flipped_jump = pygame.transform.flip(player_jump_img, True, False)
                    screen.blit(flipped_jump, (player.x - camera_x, player.y))
        elif player_moving:
            # Running animation
            if run_frame < len(player_run_imgs) and player_run_imgs[run_frame]:
                run_img = player_run_imgs[run_frame]
                if player_facing_right:
                    screen.blit(run_img, (player.x - camera_x, player.y))
                else:
                    flipped_run = pygame.transform.flip(run_img, True, False)
                    screen.blit(flipped_run, (player.x - camera_x, player.y))
        else:
            # Idle state
            if player_idle_img:
                if player_facing_right:
                    screen.blit(player_idle_img, (player.x - camera_x, player.y))
                else:
                    flipped_idle = pygame.transform.flip(player_idle_img, True, False)
                    screen.blit(flipped_idle, (player.x - camera_x, player.y))
        
        # Draw UI
        player_info = font.render(f"{player_name} | {difficulty}", True, (100, 200, 255))
        coins_text = font.render(f"Coins: {item_manager.coin_count} | Items: {len(item_manager.get_uncollected_items())}", True, (255, 255, 255))
        screen.blit(player_info, (20, 20))
        screen.blit(coins_text, (20, 50))
        
        # Draw coin icon on top right
        coin_icon_x = WIDTH - 180
        coin_icon_y = 25
        pygame.draw.circle(screen, (255, 200, 0), (coin_icon_x, coin_icon_y), 12)  # Coin body
        pygame.draw.circle(screen, (255, 255, 100), (coin_icon_x, coin_icon_y), 8)  # Coin highlight
        pygame.draw.circle(screen, (255, 255, 200), (coin_icon_x - 4, coin_icon_y - 4), 3)  # Shine
        # Coin count next to icon
        coin_count_text = font.render(f"x {item_manager.coin_count}", True, (255, 255, 100))
        screen.blit(coin_count_text, (coin_icon_x + 20, coin_icon_y - 15))
        
        # Draw active powerups as separate icons
        powerup_y = 20
        for powerup_type, duration in item_manager.active_powerups.items():
            color_map = {
                ItemType.POWERUP_SHIELD: (0, 255, 100),
                ItemType.POWERUP_SPEED: (255, 100, 0),
                ItemType.POWERUP_JUMP: (100, 150, 255),
                ItemType.POWERUP_SLOW: (255, 255, 100)
            }
            
            color = color_map.get(powerup_type, (200, 200, 200))
            # Draw powerup icon next to player
            pygame.draw.circle(screen, color, (int(player.x - camera_x + 80), int(player.y - 20)), 8)
            pygame.draw.circle(screen, (255, 255, 255), (int(player.x - camera_x + 80), int(player.y - 20)), 8, 1)
            
            # Draw powerup label
            label = font.render(f"{powerup_type.value.upper()}: {duration // 6}s", True, color)
            screen.blit(label, (WIDTH - 250, powerup_y))
            powerup_y += 25
        
        # Draw collected items inventory on right side
        inventory_title = font.render(u"Vật Phẩm Thu Thập:", True, (255, 200, 100))
        screen.blit(inventory_title, (WIDTH - 200, 100))
        
        # Count collected items by type
        collected = {}
        for item in item_manager.items:
            if item.collected:
                item_type = item.item_type.value
                collected[item_type] = collected.get(item_type, 0) + 1
        
        inv_y = 130
        for item_name, count in collected.items():
            item_text = font.render(f"✓ {item_name}: {count}", True, (100, 255, 100))
            screen.blit(item_text, (WIDTH - 200, inv_y))
            inv_y += 25
        
        # Check if all coins collected for portal
        if portal and len(item_manager.get_uncollected_items()) == 0:
            hint = font.render(u"Cổng đích → Hoàn thành!", True, (0, 255, 100))
            screen.blit(hint, (20, 80))
        
        pygame.display.flip()


def ask_python_question(question_system, difficulty):
    """Ask Python question screen (simplified & robust)"""
    pygame.key.start_text_input()
    input_rect = pygame.Rect(WIDTH//2 - 150, 330, 300, 50)
    pygame.key.set_text_input_rect(input_rect)
    
    while True:
        clock.tick(FPS)
        
        # Clear and draw background
        screen.fill((120, 80, 160))
        
        # Draw checkerboard pattern
        for x in range(0, WIDTH, 40):
            for y in range(0, HEIGHT, 40):
                if (x // 40 + y // 40) % 2 == 0:
                    pygame.draw.rect(screen, (140, 100, 180), (x, y, 40, 40))
        
        # Draw title
        title = big_font.render(u"CÂU HỎI PYTHON", True, (255, 255, 0))
        title_rect = title.get_rect(center=(WIDTH//2, 150))
        screen.blit(title, title_rect)
        
        # Draw question
        question_text = question_system.get_display_question()
        qtxt = font.render(question_text, True, (255, 255, 255))
        qtxt_rect = qtxt.get_rect(center=(WIDTH//2, 240))
        screen.blit(qtxt, qtxt_rect)
        
        # Draw input box
        pygame.draw.rect(screen, (80, 80, 80), input_rect)
        pygame.draw.rect(screen, (200, 200, 200), input_rect, 3)
        
        # Draw answer INSIDE input box
        answer_text = question_system.user_answer
        if answer_text:  # Only render if there's text
            atxt = font.render(answer_text, True, (100, 255, 100))
            answer_rect = atxt.get_rect(topleft=(input_rect.x + 10, input_rect.y + 8))
            screen.blit(atxt, answer_rect)
        
        # Draw hint
        hint = font.render(u"ENTER xác nhận | Backspace sửa", True, (180, 180, 180))
        hint_rect = hint.get_rect(center=(WIDTH//2, 420))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.key.stop_text_input()
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    question_system.remove_character()
                elif event.key == pygame.K_RETURN:
                    pygame.key.stop_text_input()
                    return question_system.check_answer()
                # Number keys
                elif event.key in (pygame.K_0, pygame.K_KP_0): question_system.add_character('0')
                elif event.key in (pygame.K_1, pygame.K_KP_1): question_system.add_character('1')
                elif event.key in (pygame.K_2, pygame.K_KP_2): question_system.add_character('2')
                elif event.key in (pygame.K_3, pygame.K_KP_3): question_system.add_character('3')
                elif event.key in (pygame.K_4, pygame.K_KP_4): question_system.add_character('4')
                elif event.key in (pygame.K_5, pygame.K_KP_5): question_system.add_character('5')
                elif event.key in (pygame.K_6, pygame.K_KP_6): question_system.add_character('6')
                elif event.key in (pygame.K_7, pygame.K_KP_7): question_system.add_character('7')
                elif event.key in (pygame.K_8, pygame.K_KP_8): question_system.add_character('8')
                elif event.key in (pygame.K_9, pygame.K_KP_9): question_system.add_character('9')
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS): question_system.add_character('-')
                elif event.key in (pygame.K_PERIOD, pygame.K_KP_PERIOD): question_system.add_character('.')
                elif event.key == pygame.K_SPACE: question_system.add_character(' ')
                elif event.key == pygame.K_LBRACKET: question_system.add_character('[')
                elif event.key == pygame.K_RBRACKET: question_system.add_character(']')
                elif event.key == pygame.K_COMMA: question_system.add_character(',')
            
            elif event.type == pygame.TEXTINPUT:
                if event.text not in ('\r', '\n'):
                    question_system.add_character(event.text)


# ============== MAIN =================
if __name__ == "__main__":
    while True:
        difficulty, map_index = main_menu()
        player_name = player_name_screen()
        game(map_index, player_name, difficulty)
