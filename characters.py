"""
MODULE: Characters (Nhân Vật)
Hệ thống tạo và quản lý nhân vật từ các bộ phận (modular character system)
"""

import os
import pygame
import random

class CharacterPart:
    """Đại diện cho một bộ phận nhân vật"""
    def __init__(self, name, image=None):
        self.name = name
        self.image = image

class Character:
    """Tạo nhân vật từ các bộ phận khác nhau"""
    
    PART_TYPES = [
        "bodies",
        "hair",
        "eyes",
        "facialhair",
        "shirt",
        "pants",
        "boots",
        "gloves",
        "shoulders",
        "headwear",
        "waist",
        "accessories"
    ]
    
    def __init__(self, base_dir, preset_name=None):
        self.base_dir = base_dir
        self.parts = {}
        self.composite_image = None
        self.width = 60
        self.height = 60
        
        # Create fallback colored circle if assets unavailable
        self.fallback_img = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(self.fallback_img, (100, 150, 200), (30, 30), 25)
        
        # Load preset hoặc random
        try:
            if preset_name:
                self.load_preset(preset_name)
            else:
                self.generate_random()
        except Exception as e:
            print(f"⚠️ Lỗi tạo character: {e}")
            self.compose()  # Use fallback
    
    def load_image(self, path):
        """Load hình ảnh với xử lý lỗi"""
        try:
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                # Scale lên 60x60 nếu cần
                return pygame.transform.scale(img, (self.width, self.height))
        except Exception as e:
            print(f"⚠️ Lỗi tải: {path}")
        return None
    
    def get_available_parts(self, part_type):
        """Lấy danh sách các bộ phận khả dụng"""
        part_dir = os.path.join(self.base_dir, part_type)
        parts = []
        
        try:
            if os.path.isdir(part_dir):
                for subfolder in os.listdir(part_dir):
                    subfolder_path = os.path.join(part_dir, subfolder)
                    if os.path.isdir(subfolder_path):
                        try:
                            for filename in os.listdir(subfolder_path):
                                if filename.lower().endswith(('.png', '.jpg')):
                                    parts.append({
                                        'category': subfolder,
                                        'name': filename,
                                        'path': os.path.join(subfolder_path, filename)
                                    })
                        except Exception as e:
                            pass  # Skip folder if error
        except Exception as e:
            pass  # No parts available
        
        return parts
    
    def select_part(self, part_type, category=None):
        """Chọn một bộ phận ngẫu nhiên hoặc theo category"""
        try:
            available = self.get_available_parts(part_type)
        except Exception as e:
            print(f"⚠️ Lỗi load {part_type}: {e}")
            return None
        
        if not available:
            return None
        
        # Lọc theo category nếu được chỉ định
        if category:
            available = [p for p in available if p['category'].lower() == category.lower()]
        
        if not available:
            return None
        
        selected = random.choice(available)
        img = self.load_image(selected['path'])
        
        if img:
            self.parts[part_type] = {
                'category': selected['category'],
                'name': selected['name'],
                'image': img
            }
            return selected
        
        return None
    
    def generate_random(self):
        """Tạo nhân vật ngẫu nhiên từ các bộ phận"""
        for part_type in self.PART_TYPES:
            try:
                self.select_part(part_type)
            except Exception as e:
                pass  # Skip if error
        self.compose()
    
    def load_preset(self, preset_name):
        """Load preset nhân vật (nếu có file config)"""
        # Auto-detect từ folder name, ví dụ: "Unisex" trong bodies/
        for part_type in self.PART_TYPES:
            try:
                self.select_part(part_type, preset_name)
            except Exception as e:
                pass  # Skip if error
        self.compose()
    
    def compose(self):
        """Ghép tất cả các bộ phận thành một hình ảnh duy nhất"""
        # Nếu không có parts, sử dụng fallback
        if not self.parts or all(not p for p in self.parts.values()):
            self.composite_image = self.fallback_img.copy()
            return
        
        # Tạo surface trong suốt
        self.composite_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Thứ tự vẽ: bodies → hair → eyes → shirt → pants → boots → accessories
        draw_order = [
            "bodies", "shirt", "pants", "boots", "gloves",
            "shoulders", "hair", "eyes", "facialhair",
            "headwear", "waist", "accessories"
        ]
        
        for part_type in draw_order:
            if part_type in self.parts and self.parts[part_type] and self.parts[part_type].get('image'):
                self.composite_image.blit(
                    self.parts[part_type]['image'],
                    (0, 0)
                )
    
    def get_image(self):
        """Lấy hình ảnh nhân vật"""
        if self.composite_image is None:
            self.compose()
        return self.composite_image
    
    def get_info(self):
        """Lấy thông tin chi tiết về nhân vật"""
        info = {}
        for part_type, part_data in self.parts.items():
            if part_data:
                info[part_type] = part_data.get('name', 'Unknown')
        return info
    
    def export_preset(self, filename):
        """Xuất preset nhân vật ra file"""
        info = self.get_info()
        with open(filename, 'w') as f:
            f.write("# Character Preset\n")
            for part_type, name in info.items():
                f.write(f"{part_type}: {name}\n")


# ============== PRESETS ==============
PRESET_CONFIGS = {
    "default_male": {
        "bodies": "Unisex",
        "hair": "Male",
        "pants": "Unisex",
        "shirt": "Unisex"
    },
    "default_female": {
        "bodies": "Unisex",
        "hair": "Female",
        "pants": "Unisex",
        "shirt": "Unisex"
    },
    "random": None  # Random generation
}


def load_character_list(base_dir):
    """Tải danh sách tất cả các nhân vật khả dụng"""
    characters = {}
    
    for preset_name in PRESET_CONFIGS.keys():
        try:
            char = Character(base_dir, preset_name=preset_name)
            characters[preset_name] = char
        except Exception as e:
            print(f"⚠️ Lỗi tải nhân vật {preset_name}: {e}")
    
    return characters


if __name__ == "__main__":
    """Test the character system"""
    pygame.init()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tạo nhân vật random
    char = Character(base_dir)
    print("🎮 Nhân vật Random:")
    print(char.get_info())
    
    # Tạo nhân vật từ preset
    char2 = Character(base_dir, preset_name="Male")
    print("\n👨 Nhân vật Male:")
    print(char2.get_info())
    
    # Tạo nhân vật Female
    char3 = Character(base_dir, preset_name="Female")
    print("\n👩 Nhân vật Female:")
    print(char3.get_info())
