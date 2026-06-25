#? interactions.py handles dragging, dropping, and grid snapping logic
import pygame
import config
import random
from pieces import gen_valid_buffer

# load sound effects framework safely matching volume parameters
_sounds={}
def init_sounds():
    global _sounds
    names=["start game.ogg","release.ogg","drop.ogg","combo 1.ogg","combo 2.ogg","combo 3.ogg","combo 4.ogg","combo 5.ogg","combo 6.ogg","combo 7.ogg","combo 8.ogg","combo 9.ogg","combo 10.ogg","game over.mp3"]
    for n in names:
        try:
            _sounds[n]=pygame.mixer.Sound(f"assets/{n}")
        except Exception as e:
            print(f"sfx load error for {n}: {e}")
            _sounds[n]=None

def play_sfx(name):
    if not _sounds:
        init_sounds()
    snd=_sounds.get(name)
    if snd and config.SFX_VOL>0:
        snd.set_volume(config.SFX_VOL)
        snd.play()

def handle_interaction(event,board_obj,active_buffer,drag_state,score_obj,game_over=False): # processes pygame mouse events to mutate dragging states and board placement
    if not _sounds:
        init_sounds()

    if game_over:
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            mx,my=event.pos
            if config.SCREEN_W//2-80<=mx<=config.SCREEN_W//2+80 and 740<=my<=785:
                board_obj.__init__()
                score_obj.score=0
                score_obj.combo=0
                config.randtheme()
                active_buffer[:]=gen_valid_buffer(board_obj)
                play_sfx("start game.ogg")
                return True
        return False

    if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
        mx,my=event.pos
        if my>=650:
            slot_width=config.SCREEN_W//3
            idx=mx//slot_width
            
            if 0<=idx<3 and active_buffer[idx] is not None:
                piece=active_buffer[idx]
                drag_state["idx"]=idx
                drag_state["piece"]=piece
                drag_state["pos"]=(mx-(len(piece[0])*config.TILE_SIZE)//2,my-(len(piece)*config.TILE_SIZE)//2)

    elif event.type==pygame.MOUSEMOTION and drag_state["piece"] is not None:
        mx,my=event.pos
        piece=drag_state["piece"]

        dx=mx-(len(piece[0])*config.TILE_SIZE)//2
        dy=my-(len(piece)*config.TILE_SIZE)//2
        drag_state["pos"]=(dx,dy)

        col=round((dx-config.GRID_X)/config.TILE_SIZE)
        row=round((dy-config.GRID_Y)/config.TILE_SIZE)

        if board_obj.can_place(piece,row,col):
            drag_state["hover"]=(row,col)
        else:
            drag_state["hover"]=None

    elif event.type==pygame.MOUSEBUTTONUP and event.button==1 and drag_state["piece"] is not None:
        piece=drag_state["piece"]
        idx=drag_state["idx"]
        hover=drag_state["hover"]

        if hover is not None:
            row,col=hover
            color_hex=[cell["color"] for r in piece for cell in r if cell["tile"]][0]

            board_obj.place_piece(piece,row,col,color_hex)
            active_buffer[idx]=None

            cleared_lines=board_obj.check_and_clear_lines()
            score_obj.update(piece,cleared_lines)

            if cleared_lines>0:
                c_idx=min(10,score_obj.combo)
                play_sfx(f"combo {c_idx}.ogg")
            else:
                play_sfx("release.ogg")

            if board_obj.is_completely_clear():
                config.randtheme()
                for p in active_buffer:
                    if p is not None:
                        new_color=random.choice(config.TILES_CLRS)
                        for r in range(len(p)):
                            for c in range(len(p[r])):
                                if p[r][c]["tile"]:
                                    p[r][c]["color"]=new_color

            if all(p is None for p in active_buffer):
                active_buffer[:]=gen_valid_buffer(board_obj)
        else:
            play_sfx("drop.ogg")

        drag_state["idx"]=None
        drag_state["piece"]=None
        drag_state["pos"]=(0,0)
        drag_state["hover"]=None
    return False