"""
MODULE: Enemies (Quái Vật)
Hệ thống quái vật với AI cải thiện và behavior tối ưu
"""

import pygame
import random
import math
from enum import Enum

class MonsterState(Enum):
    """Trạng thái của quái vật"""
    IDLE = "idle"              # Đứng yên
    CHASE = "chase"            # Đuổi theo
    PATROL = "patrol"          # Tuần tra
    JUMP = "jump"              # Nhảy

class Monster:
    """Quái vật với AI nâng cao"""
    
    def __init__(self, x, y, width=60, height=60, difficulty="Normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.difficulty = difficulty
        
        # Physics
        self.vel_y = 0
        self.vel_x = 0
        self.gravity = 1.0
        
        # AI
        self.state = MonsterState.IDLE
        self.target_x = x
        self.chase_range = 400  # Phạm vi phát hiện
        self.last_jump_time = 0
        self.jump_cooldown = 30  # Ticks giữa các bước nhảy
        self.facing_right = True
        
        # Behavior
        self.patrol_left = max(0, x - 200)
        self.patrol_right = min(4000, x + 200)
        self.animation_frame = 0
        self.animation_counter = 0
        
        # Difficulty modifiers
        self.setup_difficulty()
    
    def setup_difficulty(self):
        """Setup các thông số dựa trên độ khó"""
        difficulty_config = {
            "Easy": {
                "speed": 3,
                "jump_power": -16,
                "chase_probability": 0.6,
                "jump_probability": 0.02,
                "dead_zone": 30
            },
            "Normal": {
                "speed": 5,
                "jump_power": -18,
                "chase_probability": 0.8,
                "jump_probability": 0.05,
                "dead_zone": 20
            },
            "Hard": {
                "speed": 7,
                "jump_power": -20,
                "chase_probability": 0.95,
                "jump_probability": 0.08,
                "dead_zone": 10
            },
            "Insane": {
                "speed": 9,
                "jump_power": -22,
                "chase_probability": 1.0,
                "jump_probability": 0.15,
                "dead_zone": 5
            }
        }
        
        config = difficulty_config.get(self.difficulty, difficulty_config["Normal"])
        self.speed = config["speed"]
        self.jump_power = config["jump_power"]
        self.chase_probability = config["chase_probability"]
        self.jump_probability = config["jump_probability"]
        self.dead_zone = config["dead_zone"]
    
    def calculate_distance_to_player(self, player_x):
        """Tính khoảng cách đến player"""
        return abs(self.x - player_x)
    
    def can_see_player(self, player_x):
        """Kiểm tra xem quái có nhìn thấy player không"""
        distance = self.calculate_distance_to_player(player_x)
        return distance < self.chase_range
    
    def update_state(self, player_x, player_y):
        """Cập nhật trạng thái dựa trên vị trí player"""
        distance = self.calculate_distance_to_player(player_x)
        
        if self.can_see_player(player_x):
            self.state = MonsterState.CHASE
            self.target_x = player_x
        else:
            self.state = MonsterState.PATROL
    
    def update_movement(self, platforms, player_x):
        """Cập nhật movement của quái"""
        
        # Update animation
        self.animation_counter += 1
        if self.animation_counter > 10:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_counter = 0
        
        # Horizontal movement dựa trên state
        if self.state == MonsterState.CHASE:
            self._update_chase(player_x)
        elif self.state == MonsterState.PATROL:
            self._update_patrol()
        
        # Vertical movement (gravity)
        self.vel_y += self.gravity
        self.y += self.vel_y
        
        # Platform collisions
        on_platform = False
        for platform in platforms:
            if self.rect.colliderect(platform) and self.vel_y > 0:
                self.y = platform.top - self.height
                self.vel_y = 0
                on_platform = True
                
                # Smart jumping logic
                if self.state == MonsterState.CHASE and random.random() < self.jump_probability * 3:
                    self.vel_y = self.jump_power
                elif self.state == MonsterState.PATROL and random.random() < self.jump_probability:
                    self.vel_y = self.jump_power
                
                break
        
        # Fall detection - điều chỉnh behavior nếu rơi
        if self.y > 600:  # Out of bounds
            self.y = 450  # Reset
            self.target_x = self.x
        
        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y
    
    def _update_chase(self, player_x):
        """Chase logic - đuổi theo player"""
        distance = self.calculate_distance_to_player(player_x)
        
        # Dead zone để tránh stuttering
        if distance > self.dead_zone:
            if random.random() < self.chase_probability:
                if self.x < player_x:
                    self.vel_x = self.speed
                    self.facing_right = True
                else:
                    self.vel_x = -self.speed
                    self.facing_right = False
        else:
            self.vel_x = 0
        
        self.x += self.vel_x
    
    def _update_patrol(self):
        """Patrol logic - tuần tra giữa hai điểm"""
        # Simple left-right patrol pattern
        if random.random() < 0.02:
            if self.x < self.patrol_right:
                self.vel_x = self.speed * 0.3
                self.facing_right = True
            else:
                self.vel_x = -self.speed * 0.3
                self.facing_right = False
        
        self.x += self.vel_x
    
    def draw(self, screen, camera_x, image=None):
        """Vẽ quái vật"""
        x_pos = self.x - camera_x
        
        if image:
            if self.facing_right:
                screen.blit(image, (x_pos, self.y))
            else:
                flipped = pygame.transform.flip(image, True, False)
                screen.blit(flipped, (x_pos, self.y))
        else:
            # Fallback circle
            color = (255, 100, 100) if self.state == MonsterState.CHASE else (150, 100, 100)
            pygame.draw.circle(screen, color, (int(x_pos + self.width // 2), int(self.y + self.height // 2)), 30)
    
    def reset_position(self, x, y):
        """Reset vị trí quái"""
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.state = MonsterState.IDLE


class MonsterManager:
    """Quản lý nhóm quái vật"""
    
    def __init__(self, difficulty="Normal"):
        self.monsters = []
        self.difficulty = difficulty
    
    def add_monster(self, x, y, width=60, height=60):
        """Thêm quái vật"""
        monster = Monster(x, y, width, height, self.difficulty)
        self.monsters.append(monster)
        return monster
    
    def create_from_positions(self, positions):
        """Tạo quái từ danh sách vị trí"""
        for x, y in positions:
            self.add_monster(x, y)
    
    def add_wave(self, count, start_x=700, spacing=200):
        """Thêm một nhóm quái"""
        for i in range(count):
            self.add_monster(start_x + i * spacing, 450)
    
    def update_all(self, platforms, player_x, player_y):
        """Cập nhật tất cả quái"""
        for monster in self.monsters:
            monster.update_state(player_x, player_y)
            monster.update_movement(platforms, player_x)
    
    def check_collisions(self, player_rect):
        """Kiểm tra va chạm với player"""
        collided = []
        for monster in self.monsters:
            if monster.rect.colliderect(player_rect):
                collided.append(monster)
        return collided
    
    def draw_all(self, screen, camera_x, image=None):
        """Vẽ tất cả quái"""
        for monster in self.monsters:
            monster.draw(screen, camera_x, image)
    
    def reset_monster(self, index, player_x):
        """Reset một quái sau va chạm"""
        if index < len(self.monsters):
            # Đặt quái ở xa player
            self.monsters[index].reset_position(max(0, player_x - 300), 450)
    
    def get_alive_monsters(self):
        """Lấy danh sách quái còn sống"""
        return self.monsters
    
    def increase_difficulty(self):
        """Tăng độ khó (cho các bản của game khác)"""
        for monster in self.monsters:
            monster.speed += 1
            monster.jump_probability += 0.01


# ============== AI UTILITY FUNCTIONS ==============
def predict_player_position(player_x, player_vel, time_steps=10):
    """Dự đoán vị trí của player sau một số ticks"""
    predicted_x = player_x + player_vel * time_steps
    return max(0, min(predicted_x, 4000))  # Keep within map bounds


def calculate_pursuit_intercept(monster_x, player_x, monster_speed, player_speed):
    """Tính toán điểm giao cắt để đuổi player hiệu quả"""
    distance = abs(monster_x - player_x)
    
    if distance == 0:
        return monster_x
    
    # Simple intercept calculation
    pursuit_direction = 1 if player_x > monster_x else -1
    
    # Adjust for relative speeds
    if player_speed > 0:
        intercept_x = player_x + (distance / monster_speed) * player_speed * pursuit_direction
    else:
        intercept_x = player_x
    
    return max(0, min(intercept_x, 4000))


if __name__ == "__main__":
    """Test enemy system"""
    print("🎮 Enemy System Initialized")
    
    # Test Monster
    monster = Monster(700, 450, difficulty="Normal")
    print(f"Monster created at ({monster.x}, {monster.y})")
    print(f"Monster state: {monster.state.value}")
    print(f"Chase range: {monster.chase_range}")
    
    # Test MonsterManager
    manager = MonsterManager("Hard")
    manager.add_wave(3)
    print(f"Monsters spawned: {len(manager.monsters)}")
