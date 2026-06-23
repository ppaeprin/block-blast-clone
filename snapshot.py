import pygame
import sys
import math

# setup
WIDTH=450
HEIGHT=800
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("\"Block Blast!\" clone ui draft")
clock=pygame.time.Clock()

# Colors (Matching the dark blue theme from the reference)
BG_COLOR=           (36, 54, 101)           # deep blue bg
GRID_BG=            (24, 34, 64 )           # darker grid container bg
GRID_LINE=          (32, 46, 84 )           # grid lines
BLOCK_COLOR=        (242,110,34 )           # orange blocks
TEXT_COLOR=         (255,255,255)
SHADOW_COLOR=       (180,70, 10 )           # darker orange for block bevels

# grid calcs (8x8 centered)
GRID_COLS,GRID_ROWS=8,8
TILE_SIZE=          44                      # fits nicely inside 450 width
GRID_WIDTH=         GRID_COLS*TILE_SIZE
GRID_HEIGHT=        GRID_ROWS*TILE_SIZE
GRID_X=             (WIDTH-GRID_WIDTH)//2
GRID_Y=             220                     # a bit lowered to leave room for massive score

# mock board data (0=empty,1=filled block)
board=[]
for tile in range(8):
    board.append([0]*8)

for c in range(5):
    board[6][c]=1

for c in range(4,8):
    board[5][c]=1

board[4][7]=1
board[6][7]=1

def draw_block(surface,x,y,size):
    pygame.draw.rect(surface,BLOCK_COLOR, (x,y,size,size),  border_radius=4)
    pygame.draw.rect(surface,SHADOW_COLOR,(x,y,size,size),2,border_radius=4)

def draw_gear(surface, center_x, center_y, radius, color): # for the settings button
    pygame.draw.circle(surface,color,(center_x,center_y),radius,   3)
    pygame.draw.circle(surface,color,(center_x,center_y),radius//3,2)

    num_teeth=   8
    tooth_width= 6
    tooth_height=5

    # render settings gear teeth (credits to gemini)
    for i in range(num_teeth):
        angle=      i*(2*math.pi/num_teeth)
        start_x=    center_x+radius*               math.cos(angle)
        start_y=    center_y+radius*               math.sin(angle)
        end_x=      center_x+(radius+tooth_height)*math.cos(angle)
        end_y=      center_y+(radius+tooth_height)*math.sin(angle)
        
        pygame.draw.line(surface,color,(start_x,start_y),(end_x,end_y),tooth_width)

def render_ui():
    screen.fill(BG_COLOR)
    
    # header fonts
    font_large=pygame.font.SysFont("arial",72,bold=True)
    font_small=pygame.font.SysFont("arial",24,bold=True)

    # crown icon for best high score (credits to gemini)
    crown_points=[
        (25,52),
        (25,37),
        (32,44),
        (40,34),
        (48,44),
        (55,37),
        (55,52),
    ]
    pygame.draw.polygon(screen,BLOCK_COLOR,crown_points)

    # pb score next to crown
    high_score_text=font_small.render("922",True,BLOCK_COLOR)
    screen.blit(
        high_score_text,
        (65,32),
    )

    # settings gear (credits to gemini)
    draw_gear(
        screen,
        WIDTH-40,
        42,12,
        TEXT_COLOR,
    )

    # current score (big and centered)
    score_text=font_large.render("922",True,TEXT_COLOR)
    score_rect=score_text.get_rect(center=(WIDTH//2,130))
    screen.blit(score_text,score_rect)

    # grid renderer that shecks if it should draw a tile or leave it empty 
    pygame.draw.rect(
        screen,
        GRID_BG,
        (
            GRID_X     -6,
            GRID_Y     -6,
            GRID_WIDTH +12,
            GRID_HEIGHT+12,
        ),
        border_radius=8,
    )

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x=GRID_X+col*TILE_SIZE
            y=GRID_Y+row*TILE_SIZE
            
            if board[row][col]==1:
                draw_block(screen,x,y,TILE_SIZE-2)
            else:
                pygame.draw.rect(
                    screen,
                    GRID_LINE,
                    (
                        x,
                        y,
                        TILE_SIZE-2,
                        TILE_SIZE-2,
                    ),
                    border_radius=4
                )

    # bottom (spawn buffer)
    buffer_y=           650
    slot_width=         WIDTH    //3
    preview_tile_size=  TILE_SIZE//2

    # i was too lazy to make the pieces so i asked it to make me some (credits to gemini)
    # piece 1: bottom left corner
    p1_x = (slot_width // 2) - preview_tile_size + 10
    draw_block(screen, p1_x, buffer_y, preview_tile_size)
    draw_block(screen, p1_x, buffer_y + preview_tile_size, preview_tile_size)
    draw_block(screen, p1_x + preview_tile_size, buffer_y + preview_tile_size, preview_tile_size)

    # piece 2: 2x2 square
    p2_x = slot_width + (slot_width // 2) - preview_tile_size
    draw_block(screen, p2_x, buffer_y, preview_tile_size)
    draw_block(screen, p2_x + preview_tile_size, buffer_y, preview_tile_size)
    draw_block(screen, p2_x, buffer_y + preview_tile_size, preview_tile_size)
    draw_block(screen, p2_x + preview_tile_size, buffer_y + preview_tile_size, preview_tile_size)

    # piece 3: T shape
    p3_x = (slot_width * 2) + (slot_width // 2) - (preview_tile_size * 1.5)
    draw_block(screen, p3_x + preview_tile_size, buffer_y, preview_tile_size)
    draw_block(screen, p3_x, buffer_y + preview_tile_size, preview_tile_size)
    draw_block(screen, p3_x + preview_tile_size, buffer_y + preview_tile_size, preview_tile_size)
    draw_block(screen, p3_x + (preview_tile_size * 2), buffer_y + preview_tile_size, preview_tile_size)

# main loop
running=True

while running==True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    render_ui()
    pygame.display.flip()
    clock.tick(60) # sets it to 60 fps

pygame.quit()
sys.exit()