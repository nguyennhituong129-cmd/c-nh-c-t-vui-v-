"""
MODULE: Items (Vật Phẩm)
Quản lý các vật phẩm, coins, power-ups trong game
"""

import pygame
import random
import math
from enum import Enum

class ItemType(Enum):
    """Loại vật phẩm"""
    COIN = "coin"          # Tiền vàng
    POWERUP_SHIELD = "shield"   # Lá chắn bảo vệ
    POWERUP_SPEED = "speed"     # Tăng tốc độ
    POWERUP_JUMP = "jump"       # Tăng cao độ nhảy
    POWERUP_SLOW = "slow"       # Giảm tốc độ quái
    HEAL = "heal"               # Phục hồi điểm máu

class Item:
    """Một vật phẩm trong game"""
    
    def __init__(self, x, y, item_type, value=1):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.value = value
        self.rect = pygame.Rect(x, y, 30, 30)
        self.collected = False
        self.animation_timer = 0
        self.collected_at = None
    
    def update(self):
        """Update item state"""
        self.animation_timer += 1
        if self.animation_timer > 1000:
            self.animation_timer = 0
    
    def draw(self, screen, camera_x, coin_img=None):
        """Vẽ vật phẩm"""
        if self.collected:
            return
        
        # Floating animation
        float_offset = 5 * math.sin(self.animation_timer * 0.02)
        y_pos = self.y + float_offset - camera_x
        
        if self.item_type == ItemType.COIN and coin_img:
            screen.blit(coin_img, (self.x - camera_x, y_pos))
        else:
            # Fallback colored circles cho các power-up
            color_map = {
                ItemType.POWERUP_SHIELD: (100, 255, 100),  # Green
                ItemType.POWERUP_SPEED: (255, 100, 100),   # Red
                ItemType.POWERUP_JUMP: (100, 100, 255),    # Blue
                ItemType.POWERUP_SLOW: (255, 255, 100),    # Yellow
                ItemType.HEAL: (255, 150, 200)             # Pink
            }
            
            color = color_map.get(self.item_type, (200, 200, 200))
            pygame.draw.circle(screen, color, (int(self.x - camera_x + 15), int(y_pos + 15)), 15)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x - camera_x + 15), int(y_pos + 15)), 15, 2)
    
    def check_collision(self, player_rect):
        """Kiểm tra va chạm với player"""
        return self.rect.colliderect(player_rect)


class ItemManager:
    """Quản lý tất cả các vật phẩm trong game"""
    
    def __init__(self):
        self.items = []
        self.coin_count = 0
        self.active_powerups = {}  # {powerup_type: duration_remaining}
    
    def add_item(self, x, y, item_type, value=1):
        """Thêm một vật phẩm vào game"""
        item = Item(x, y, item_type, value)
        self.items.append(item)
        return item
    
    def add_coin(self, x, y):
        """Thêm một coin"""
        return self.add_item(x, y, ItemType.COIN, 1)
    
    def add_coins_from_platforms(self, platforms, spacing=80):
        """Tạo coins từ danh sách platforms"""
        for platform in platforms[1:]:  # Skip first platform
            coin = self.add_coin(platform.x + spacing, platform.y - 40)
    
    def add_random_powerups(self, platforms, chance=0.1):
        """Thêm random power-ups từ platforms"""
        powerup_types = [
            ItemType.POWERUP_SHIELD,
            ItemType.POWERUP_SPEED,
            ItemType.POWERUP_JUMP,
            ItemType.POWERUP_SLOW
        ]
        
        for platform in platforms[2::2]:  # Every other platform
            if random.random() < chance:
                powerup = random.choice(powerup_types)
                self.add_item(platform.x + 40, platform.y - 50, powerup)
    
    def collect(self, item, player):
        """Collect một vật phẩm"""
        if item.item_type == ItemType.COIN:
            self.coin_count += item.value
        
        elif item.item_type == ItemType.POWERUP_SHIELD:
            # Bảo vệ trong 300 ticks
            self.active_powerups[ItemType.POWERUP_SHIELD] = 300
        
        elif item.item_type == ItemType.POWERUP_SPEED:
            # Tăng tốc độ trong 200 ticks
            self.active_powerups[ItemType.POWERUP_SPEED] = 200
        
        elif item.item_type == ItemType.POWERUP_JUMP:
            # Tăng nhảy trong 150 ticks
            self.active_powerups[ItemType.POWERUP_JUMP] = 150
        
        elif item.item_type == ItemType.POWERUP_SLOW:
            # Giảm tốc độ quái trong 250 ticks
            self.active_powerups[ItemType.POWERUP_SLOW] = 250
        
        item.collected = True
        item.collected_at = pygame.time.get_ticks()
    
    def update(self):
        """Cập nhật trạng thái vật phẩm"""
        for item in self.items:
            item.update()
        
        # Update active powerups
        expired = []
        for powerup_type, duration in self.active_powerups.items():
            duration -= 1
            if duration <= 0:
                expired.append(powerup_type)
            else:
                self.active_powerups[powerup_type] = duration
        
        for powerup in expired:
            del self.active_powerups[powerup]
    
    def draw_all(self, screen, camera_x, coin_img=None):
        """Vẽ tất cả vật phẩm"""
        for item in self.items:
            if not item.collected:
                item.draw(screen, camera_x, coin_img)
    
    def check_collisions(self, player_rect):
        """Kiểm tra va chạm với player"""
        collected = []
        for item in self.items:
            if not item.collected and item.check_collision(player_rect):
                collected.append(item)
        
        return collected
    
    def get_uncollected_items(self):
        """Lấy danh sách vật phẩm chưa collected"""
        return [item for item in self.items if not item.collected]
    
    def get_powerup_multiplier(self, powerup_type):
        """Lấy multiplier cho một powerup"""
        if powerup_type not in self.active_powerups:
            return 1.0
        
        if powerup_type == ItemType.POWERUP_SPEED:
            return 1.5  # 50% tăng tốc độ
        elif powerup_type == ItemType.POWERUP_JUMP:
            return 1.3  # 30% tăng cao độ nhảy
        elif powerup_type == ItemType.POWERUP_SLOW:
            return 0.6  # 40% giảm tốc độ quái
        
        return 1.0
    
    def is_protected(self):
        """Kiểm tra xem player có được bảo vệ không"""
        return ItemType.POWERUP_SHIELD in self.active_powerups
    
    def draw_powerup_status(self, screen, font, width=1000, height=600):
        """Vẽ status của active powerups"""
        x = width - 250
        y = 20
        
        if not self.active_powerups:
            return
        
        for powerup_type, duration in self.active_powerups.items():
            text = f"⭐ {powerup_type.value.upper()}: {duration // 6}s"
            color_map = {
                ItemType.POWERUP_SHIELD: (0, 255, 100),
                ItemType.POWERUP_SPEED: (255, 100, 0),
                ItemType.POWERUP_JUMP: (100, 150, 255),
                ItemType.POWERUP_SLOW: (255, 255, 100)
            }
            
            color = color_map.get(powerup_type, (200, 200, 200))
            powerup_text = font.render(text, True, color)
            screen.blit(powerup_text, (x, y))
            y += 30


# ============== ITEM EFFECT FUNCTIONS ==============
def apply_item_effects(item_manager, player_stats):
    """Áp dụng các effect từ active powerups"""
    
    speed_mult = item_manager.get_powerup_multiplier(ItemType.POWERUP_SPEED)
    jump_mult = item_manager.get_powerup_multiplier(ItemType.POWERUP_JUMP)
    
    # Apply multipliers to player stats
    adjusted_speed = player_stats['speed'] * speed_mult
    adjusted_jump = player_stats['jump_power'] * jump_mult
    
    return adjusted_speed, adjusted_jump


if __name__ == "__main__":
    """Test item system"""
    print("🎮 Item System Initialized")
    
    # Test ItemManager
    manager = ItemManager()
    manager.add_coin(100, 100)
    manager.add_item(200, 100, ItemType.POWERUP_SPEED)
    
    print(f"Items created: {len(manager.items)}")
    print(f"Item types: {[item.item_type.value for item in manager.items]}")
