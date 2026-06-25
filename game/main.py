#? main.py forms the master executable loop wrapper
import pygame
import sys
import config
from board import Board
from pieces import gen_valid_buffer
from score import ScoreManager
from interactions import handle_interaction,play_sfx
from renderer import draw_game
from settings import SettingsMenu

def main():
    pygame.mixer.pre_init(44100,-16,2,512)
    pygame.init()
    pygame.mixer.init()
    
    screen=pygame.display.set_mode((config.SCREEN_W,config.SCREEN_H))
    pygame.display.set_caption("Block Puzzle")
    clock=pygame.time.Clock()

    board_obj=    Board()
    score_obj=    ScoreManager()
    active_buffer=gen_valid_buffer(board_obj)
    settings_menu=SettingsMenu()
    
    drag_state={"idx":None,"piece":None,"pos":(0,0),"hover":None}
    game_over=False

    try:
        pygame.mixer.music.load      ("assets/bg music.mp3")
        pygame.mixer.music.set_volume(config.MUSIC_VOL)
        pygame.mixer.music.play      (-1)
    except Exception as e:
        print(f"music load error: {e}")

    play_sfx("start_game")

    def force_reset_buffer_and_theme():
        config.randtheme()
        active_buffer[:]=gen_valid_buffer(board_obj)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if settings_menu.active:
                did_reset=settings_menu.handle_event(event,board_obj,score_obj,active_buffer,force_reset_buffer_and_theme)
                if did_reset:
                    game_over=False
                continue

            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                mx,my=event.pos
                if config.SCREEN_W-60<=mx<=config.SCREEN_W-20 and 20<=my<=60:
                    settings_menu.trigger(screen)
                    continue

            did_reset=handle_interaction(event,board_obj,active_buffer,drag_state,score_obj,game_over)
            if did_reset:
                game_over=False

        if not game_over and not settings_menu.active and drag_state["piece"] is None:
            if not board_obj.can_any_piece_fit(active_buffer):
                game_over=True
                play_sfx("game_over")

        draw_game(
            screen,
            board_obj,
            active_buffer,
            drag_state["piece"],
            drag_state["pos"],
            drag_state["idx"],
            drag_state["hover"],
            score_obj.score,
            score_obj.high_score,
            game_over,
        )

        if settings_menu.active:
            settings_menu.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__=="__main__":
    main()
