#? renderer.py draws all game screens, icons, grids, and preview shapes
import pygame
import config
import math

_font_large=None
_font_small=None

def get_fonts(): # lazy loader to prevent initialization crashes before pygame.init runs
    global _font_large,_font_small
    if _font_large is None:
        _font_large=pygame.font.SysFont("arial",72,bold=True)
        _font_small=pygame.font.SysFont("arial",24,bold=True)
    return _font_large,_font_small

def draw_block(surface,x,y,size,color_hex): # dynamic tile block with border bevel shadows
    c=pygame.Color(color_hex)
    s_clr=(max(0,int(c.r*0.7)),max(0,int(c.g*0.7)),max(0,int(c.b*0.7))) # dynamic bevel shading
    pygame.draw.rect(surface,c,    (x,y,size,size),  border_radius=4)
    pygame.draw.rect(surface,s_clr,(x,y,size,size),2,border_radius=4)

def draw_gear(surface,center_x,center_y,radius,color): # for the settings button (credits to gemini)
    pygame.draw.circle(surface,color,(center_x,center_y),radius,   3)
    pygame.draw.circle(surface,color,(center_x,center_y),radius//3,2)

    num_teeth=   8
    tooth_width= 6
    tooth_height=5

    for i in range(num_teeth):
        angle=      i*(2*math.pi/num_teeth)
        start_x=    center_x+radius* math.cos(angle)
        start_y=    center_y+radius* math.sin(angle)
        end_x=      center_x+(radius+tooth_height)*math.cos(angle)
        end_y=      center_y+(radius+tooth_height)*math.sin(angle)
        
        pygame.draw.line(surface,color,(start_x,start_y),(end_x,end_y),tooth_width)

def draw_game(
        screen,
        board_obj,
        active_buffer,
        dragged_piece=None,
        dragged_pos=  (0,0),
        dragged_idx=  None,
        hover_pos=    None,
        score=        0,
        high_score=   922,   # placeholder pb
        game_over=    False,
    ):
    # background clear
    screen.fill(pygame.Color(config.BG_CLR))
    font_large,font_small=get_fonts()

    crown_points=[ # top bar headers (crown + highscore)
        (25,52),
        (25,37),
        (32,44),
        (40,34),
        (48,44),
        (55,37),
        (55,52),
    ]

    pygame.draw.polygon(
        screen,
        pygame.Color(config.PB_CLR),
        crown_points,
    )

    high_score_text=font_small.render(
        str(high_score),
        True,
        pygame.Color(config.PB_CLR),
    )
    screen.blit(high_score_text,(65,32))

    # settings icon
    draw_gear(
        screen,
        config.SCREEN_W-40,
        42,
        12,
        pygame.Color(config.GEAR_CLR),
    )

    # game over header alert text
    if game_over:
        go_text=font_small.render("GAME OVER",True,pygame.Color("#FF3F3F"))
        go_rect=go_text.get_rect(center=(config.SCREEN_W//2,90))
        screen.blit(go_text,go_rect)

    # current large score display
    score_text=font_large.render(
        str(score),
        True,
        pygame.Color("#FFFFFF"),
    )
    score_rect=score_text.get_rect(center=(config.SCREEN_W//2,140))
    screen.blit(score_text,score_rect)

    # main board frame rendering
    pygame.draw.rect(
        screen,
        pygame.Color(config.GRID_BG_CLR),
        (
            config.GRID_X-6,
            config.GRID_Y-6,
            config.GRID_W+12,
            config.GRID_H+12,
        ),
        border_radius=8,
    )

    for row in range(config.GRID_ROWS):
        for col in range(config.GRID_COLS):
            x=config.GRID_X+col*config.TILE_SIZE
            y=config.GRID_Y+row*config.TILE_SIZE

            cell=board_obj.grid[row][col]

            if cell["tile"]:
                draw_block(screen,x,y,config.TILE_SIZE-2,cell["color"])
            else:
                pygame.draw.rect(
                    screen,
                    pygame.Color(config.GRID_LINES_CLR),
                    (
                        x,
                        y,
                        config.TILE_SIZE-2,
                        config.TILE_SIZE-2,
                    ),
                    border_radius=4
                )

    if dragged_piece and hover_pos: # grid shadow preview (shows ghost alpha shape when hovering a piece)
        hr,hc=hover_pos
        p_clr=[cell["color"] for row in dragged_piece for cell in row if cell["tile"]][0]
        c=pygame.Color(p_clr)

        shadow_surf=pygame.Surface((config.TILE_SIZE-2,config.TILE_SIZE-2),pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surf,
            (c.r,c.g,c.b,90),
            (
                0,
                0,
                config.TILE_SIZE-2,
                config.TILE_SIZE-2
            ),
            border_radius=4,
        )

        p_rows=len(dragged_piece)
        p_cols=len(dragged_piece[0])

        for r in range(p_rows):
            for c in range(p_cols):
                if dragged_piece[r][c]["tile"]:
                    tr=hr+r
                    tc=hc+c
                    if 0<=tr<config.GRID_ROWS and 0<=tc<config.GRID_COLS:
                        px=config.GRID_X+tc*config.TILE_SIZE
                        py=config.GRID_Y+tr*config.TILE_SIZE
                        screen.blit(shadow_surf,(px,py))

    # bottom spawn slot indicators (at 50% miniature layout scale) - reverted to 650
    buffer_y=          650
    slot_width=        config.SCREEN_W//3
    preview_tile_size= config.TILE_SIZE  //2

    for idx,piece in enumerate(active_buffer):
        if piece is not None and idx!=dragged_idx:
            p_rows=len(piece)
            p_cols=len(piece[0])

            slot_cx=(idx*slot_width)+(slot_width//2)

            start_x=slot_cx-(p_cols*preview_tile_size)//2
            start_y=buffer_y+(44-p_rows*preview_tile_size)//2 

            for r in range(p_rows):
                for c in range(p_cols):
                    if piece[r][c]["tile"]:
                        px=start_x+c*preview_tile_size
                        py=start_y+r*preview_tile_size
                        draw_block(
                            screen,
                            px,
                            py,
                            preview_tile_size-1,
                            piece[r][c]["color"],
                        )

    # game over overlay screens adjusted for the lower buffer layout
    if game_over:
        # semi-transparent tray block overlay covering the lower buffer bounds
        overlay=pygame.Surface((config.SCREEN_W,110),pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        ns_text=font_small.render("No Space Left",True,pygame.Color("#FFFFFF"))
        ns_rect=ns_text.get_rect(center=(config.SCREEN_W//2,55))
        overlay.blit(ns_text,ns_rect)
        screen.blit(overlay,(0,620))

        # green action button layout placed comfortably below the overlay area
        reset_rect=pygame.Rect(config.SCREEN_W//2-80,740,160,45)
        pygame.draw.rect(screen,pygame.Color("#2ECC71"),reset_rect,border_radius=8)
        pygame.draw.rect(screen,pygame.Color("#27AE60"),reset_rect,2,border_radius=8)
        
        btn_text=font_small.render("RESET",True,pygame.Color("#FFFFFF"))
        btn_rect=btn_text.get_rect(center=reset_rect.center)
        screen.blit(btn_text,btn_rect)

    if dragged_piece: # full-scale dragged piece overlay (follows mouse pointer absolute screen pos)
        dx,dy=dragged_pos

        p_rows=len(dragged_piece)
        p_cols=len(dragged_piece[0])

        for r in range(p_rows):
            for c in range(p_cols):
                if dragged_piece[r][c]["tile"]:
                    px=dx+c*config.TILE_SIZE
                    py=dy+r*config.TILE_SIZE
                    draw_block(screen,px,py,config.TILE_SIZE-2,dragged_piece[r][c]["color"])