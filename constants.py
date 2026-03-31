"""
MODULE: Constants (Hằng Số)
Các hằng số và cấu hình game
"""

# ============== SCREEN SETTINGS ==============
WIDTH = 1000
HEIGHT = 600
FPS = 60

# ============== MAP SETTINGS ==============
MAP_WIDTH = 4000

# ============== COLORS ==============
COLOR_BG = (10, 14, 28)
COLOR_PURPLE_LIGHT = (120, 80, 160)
COLOR_PURPLE_DARK = (140, 100, 180)
COLOR_PINK_BRIGHT = (255, 100, 150)
COLOR_PINK_DARK = (200, 80, 120)
COLOR_YELLOW = (255, 200, 100)
COLOR_CYAN = (0, 210, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GOLD = (255, 215, 0)

# ============== DIFFICULTY SETTINGS ==============
DIFFICULTY_SETTINGS = {
    'Easy': {
        'player_speed': 5,
        'monster_speed': 4,
        'gravity': 0.8,
        'jump_power': -20
    },
    'Normal': {
        'player_speed': 6,
        'monster_speed': 6,
        'gravity': 1,
        'jump_power': -18
    },
    'Hard': {
        'player_speed': 7,
        'monster_speed': 8,
        'gravity': 1.2,
        'jump_power': -16
    },
    'Insane': {
        'player_speed': 9,
        'monster_speed': 10,
        'gravity': 1.4,
        'jump_power': -14
    },
}

# ============== PLAYER SETTINGS ==============
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 60
DOUBLE_JUMP_ENABLED = True

# ============== MONSTER SETTINGS ==============
MONSTER_WIDTH = 60
MONSTER_HEIGHT = 60
MONSTER_CHASE_RANGE = 400
MONSTER_CHASE_PROBABILITY = 0.8  # 80% chasing, 20% random
MONSTER_JUMP_PROBABILITY = 0.015  # 1.5% to jump

# ============== GAME MECHANICS ==============
MAX_PLAYER_NAME_LENGTH = 15
COIN_SIZE = 30
PORTAL_SIZE = 60
RESURRECTION_BONUS = 50
COIN_BONUS = 10

# ============== UI SETTINGS ==============
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 75
BUTTON_RADIUS = 15
BUTTON_BORDER_WIDTH_SELECTED = 4
BUTTON_BORDER_WIDTH_NORMAL = 2
