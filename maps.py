"""
MODULE: Maps (Bản Đồ)
Cấu hình và quản lý bản đồ game
"""
import os
from constants import MAP_WIDTH

MAPS = [
    {
        'id': 0,
        'name': u'Bản Đồ 1 - Cũ (sprites)',
        'description': u'Bản đồ với platform tăng dần',
        'platforms': [
            (0, 520, MAP_WIDTH, 80),
            (350, 470, 200, 20),
            (700, 440, 180, 20),
            (1050, 410, 180, 20),
            (1400, 380, 180, 20),
            (1750, 350, 180, 20),
            (2100, 320, 180, 20),
            (2450, 290, 180, 20),
            (2800, 260, 180, 20),
            (3150, 230, 180, 20),
        ],
        'background_file': os.path.join('sprites', 'Background', 'background.png'),
        'background_color': (10, 14, 28),
        'portal_x': MAP_WIDTH - 250,
        'jump_pads': [
            (750, 410, 40, 10, -26),
            (1850, 330, 40, 10, -28),
            (2650, 280, 40, 10, -30),
        ],
    },
    {
        'id': 1,
        'name': u'Bản Đồ 2 - Mới',
        'description': u'Bản đồ zigzag phức tạp',
        'platforms': [
            (0, 520, MAP_WIDTH, 80),
            (450, 470, 150, 20),
            (650, 430, 150, 20),
            (850, 390, 150, 20),
            (1050, 350, 150, 20),
            (1250, 310, 150, 20),
            (1450, 270, 150, 20),
            (1650, 230, 150, 20),
            (1850, 270, 150, 20),
            (2050, 310, 150, 20),
            (2250, 350, 150, 20),
            (2450, 390, 150, 20),
            (2650, 430, 150, 20),
            (2850, 470, 150, 20),
            (3050, 430, 150, 20),
            (3250, 390, 150, 20),
        ],
        'background_file': os.path.join('Backgrounds', 'map2', 'blue_shroom.png'),
        'background_color': (5, 25, 45),
        'portal_x': MAP_WIDTH - 220,
        'jump_pads': [
            (1250, 290, 40, 10, -26),
            (2050, 330, 40, 10, -28),
            (2850, 470, 40, 10, -32),
        ],
    },
    {
        'id': 2,
        'name': u'Bản Đồ 3 - Rush (Khó)',
        'description': u'Bản đồ ngoại lệ với platform nhỏ',
        'platforms': [
            (0, 520, MAP_WIDTH, 80),
            (250, 480, 100, 15),
            (400, 450, 100, 15),
            (550, 420, 100, 15),
            (700, 390, 100, 15),
            (850, 360, 100, 15),
            (1000, 330, 100, 15),
            (1150, 300, 100, 15),
            (1300, 270, 100, 15),
            (1450, 240, 100, 15),
            (1600, 210, 100, 15),
            (1750, 240, 100, 15),
            (1900, 270, 100, 15),
            (2050, 300, 100, 15),
            (2200, 330, 100, 15),
            (2350, 360, 100, 15),
            (2500, 390, 100, 15),
            (2650, 420, 100, 15),
            (2800, 450, 100, 15),
            (2950, 480, 100, 15),
        ],
        'background_file': os.path.join('Backgrounds', 'map2', 'blue_grass.png'),
        'background_color': (15, 25, 50),
        'portal_x': MAP_WIDTH - 200,
        'jump_pads': [
            (400, 430, 40, 10, -24),
            (1150, 280, 40, 10, -26),
            (2200, 310, 40, 10, -28),
        ],
    },
    {
        'id': 3,
        'name': u'Bản Đồ 4 - Sky Bridge (Cực Khó)',
        'description': u'Bản đồ trên bầu trời, khó nhất',
        'platforms': [
            (0, 520, MAP_WIDTH, 80),
            (200, 450, 120, 15),
            (400, 400, 120, 15),
            (600, 350, 120, 15),
            (800, 300, 120, 15),
            (1000, 250, 120, 15),
            (1200, 300, 120, 15),
            (1400, 350, 120, 15),
            (1600, 400, 120, 15),
            (1800, 450, 120, 15),
            (2000, 400, 120, 15),
            (2200, 350, 120, 15),
            (2400, 300, 120, 15),
            (2600, 250, 120, 15),
            (2800, 300, 120, 15),
            (3000, 350, 120, 15),
        ],
        'background_file': os.path.join('Backgrounds', 'map2', 'blue_land.png'),
        'background_color': (20, 15, 35),
        'portal_x': MAP_WIDTH - 200,
        'jump_pads': [
            (600, 330, 40, 10, -22),
            (1400, 330, 40, 10, -24),
            (2600, 230, 40, 10, -26),
        ],
    },
]

def get_map(map_id):
    """Lấy thông tin bản đồ"""
    if 0 <= map_id < len(MAPS):
        return MAPS[map_id]
    return MAPS[0]  # Mặc định bản đồ 1

def get_map_count():
    """Lấy số lượng bản đồ"""
    return len(MAPS)

def get_map_names():
    """Lấy danh sách tên bản đồ"""
    return [m['name'] for m in MAPS]
