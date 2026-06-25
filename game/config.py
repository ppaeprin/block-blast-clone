#? config.py handles screen layout dimensions, grid parameters, and theme presets
import random

SCREEN_W=460
SCREEN_H=800

GRID_ROWS=8
GRID_COLS=8
TILE_SIZE=45

GRID_W=GRID_COLS*TILE_SIZE
GRID_H=GRID_ROWS*TILE_SIZE

GRID_X=(SCREEN_W-GRID_W)//2
GRID_Y=200

PB_CLR="#FFD700"
GEAR_CLR="#8E8E93"

# audio settings
MUSIC_VOL,SFX_VOL=0.5,0.5

THEMES=[
    {
        "name":"classic_mode",
        "bg": "#475EA2","grid_bg":"#242D54","grid_lines":"#1C264D",
        "tiles":["#FF5733","#E29E21","#F1F52D","#1BE914","#53B9D3","#314BDF","#9317C4"]
    },
    {
        "name":"arcade",
        "bg":"#0B0C10","grid_bg":"#1F2833","grid_lines":"#2C3539",
        "tiles":["#66FCF1","#45A29E","#FF007F","#00FF00","#FFD700","#9400D3"]
    },
    {
        "name":"pastel",
        "bg":"#F7F5F0","grid_bg":"#E8E5DA","grid_lines":"#D5D1C1",
        "tiles":["#FFB7B2","#FFDAC1","#E2F0CB","#B5EAD7","#C7CEEA","#FFC6FF"]
    },
    {
        "name":"cyberpunk",
        "bg":"#120136","grid_bg":"#03001C","grid_lines":"#301E67",
        "tiles":["#00FF66","#FE019A","#00F0FF","#EAE509","#FF3F3F","#7B2CBF"]
    },
    {
        "name":"autumn",
        "bg":"#2B1B17","grid_bg":"#3E2723","grid_lines":"#4E342E",
        "tiles":["#D84315","#FF8F00","#FFB300","#558B2F","#A0522D","#8B0000"]
    },
    {
        "name":"deep_ocean",
        "bg":"#011627","grid_bg":"#0A2540","grid_lines":"#10375C",
        "tiles":["#00D2FF","#0072FF","#2AF598","#087E8B","#FF6B6B","#4A00E0"]
    },
    {
        "name":"retro",
        "bg":"#0D1117","grid_bg":"#161B22","grid_lines":"#21262D",
        "tiles":["#39FF14","#00FF00","#32CD32","#228B22","#006400","#ADFF2F"]
    },
    {
        "name":"synthwave",
        "bg":"#1A0B2E", "grid_bg":"#240046","grid_lines":"#3C096C",
        "tiles":["#FF0055","#00FFCC","#9900FF","#FFCC00","#FF6600","#FF00AA"]
    },
    {
        "name":"minimal",
        "bg":"#F5F5F7","grid_bg":"#E5E5EA","grid_lines":"#D1D1D6",
        "tiles":["#1C1C1E","#3A3A3C","#48484A","#636366","#8E8E93","#AEAEB2"]
    }
]

# global color references accessed during drawing cycles
BG_CLR=""
GRID_BG_CLR=""
GRID_LINES_CLR=""
TILES_CLRS=[]

def randtheme(): # dynamically selects a preset theme from the const list and updates global attributes
    global BG_CLR,GRID_BG_CLR,GRID_LINES_CLR,TILES_CLRS
    t=random.choice(THEMES)
    BG_CLR=t["bg"]
    GRID_BG_CLR=t["grid_bg"]
    GRID_LINES_CLR=t["grid_lines"]
    TILES_CLRS=t["tiles"]

# trigger a base generation right at startup
randtheme()