#? settings.py handles the menu overlay, sound sliders, and resets
import pygame
import config
from interactions import play_sfx

class SettingsMenu:
    def __init__(self):
        self.active=False
        self.blur_bg=None
        self.music_slider=   pygame.Rect(120,250,200,10)
        self.sfx_slider=     pygame.Rect(120,350,200,10)
        self.round_reset_btn=pygame.Rect(100,450,240,40)
        self.data_reset_btn= pygame.Rect(100,520,240,40)
        self.close_btn=      pygame.Rect(100,620,240,40)

    def trigger(self,screen):
        self.active=not self.active
        if self.active:
            raw_snap=screen.copy()
            small=pygame.transform.smoothscale(raw_snap,(config.SCREEN_W//10,config.SCREEN_H//10))
            self.blur_bg=pygame.transform.smoothscale(small,(config.SCREEN_W,config.SCREEN_H))

    def handle_event(self,event,board_obj,score_obj,active_buffer,on_reset_callback):
        if not self.active:
            return False

        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            mx,my=event.pos
            if self.close_btn.collidepoint(mx,my):
                self.active=False
                return False

            if self.round_reset_btn.collidepoint(mx,my) or self.data_reset_btn.collidepoint(mx,my):
                board_obj.__init__()
                score_obj.score=0
                score_obj.combo=0
                active_buffer[:]=[None,None,None]
                
                if self.data_reset_btn.collidepoint(mx,my):
                    score_obj.delete_save()
                
                on_reset_callback()
                play_sfx("start_game")
                self.active=False
                return True

        if pygame.mouse.get_pressed()[0]:
            mx,my=pygame.mouse.get_pos()
            if 220<=my<=280:
                val=max(0.0,min(1.0,(mx-120)/200.0))
                config.MUSIC_VOL=val
                try:
                    pygame.mixer.music.set_volume(val)
                except:
                    pass
            elif 320<=my<=380:
                config.SFX_VOL=max(0.0,min(1.0,(mx-120)/200.0))

        return False

    def draw(self,screen):
        if not self.active:
            return
        screen.blit(self.blur_bg,(0,0))
        tint=pygame.Surface((config.SCREEN_W,config.SCREEN_H),pygame.SRCALPHA)
        tint.fill((0,0,0,150))
        screen.blit(tint,(0,0))

        font=pygame.font.SysFont("arial",24,bold=True)
        title_font=pygame.font.SysFont("arial",36,bold=True)

        panel_rect=pygame.Rect(40,120,config.SCREEN_W-80,570)
        pygame.draw.rect(screen,pygame.Color("#2C3E50"),panel_rect,border_radius=12)
        pygame.draw.rect(screen,pygame.Color("#34495E"),panel_rect,4,border_radius=12)

        t_surf=title_font.render("SETTINGS",True,pygame.Color("#FFFFFF"))
        screen.blit(t_surf,t_surf.get_rect(center=(config.SCREEN_W//2,160)))

        m_lbl=font.render(f"Music Volume: {int(config.MUSIC_VOL*100)}%",True,pygame.Color("#FFFFFF"))
        screen.blit(m_lbl,(60,210))
        pygame.draw.rect(screen,pygame.Color("#7F8C8D"),self.music_slider,border_radius=4)
        pygame.draw.circle(screen,pygame.Color("#3498DB"),(int(self.music_slider.x+config.MUSIC_VOL*200),self.music_slider.centery),8)

        s_lbl=font.render(f"SFX Volume: {int(config.SFX_VOL*100)}%",True,pygame.Color("#FFFFFF"))
        screen.blit(s_lbl,(60,310))
        pygame.draw.rect(screen,pygame.Color("#7F8C8D"),self.sfx_slider,border_radius=4)
        pygame.draw.circle(screen,pygame.Color("#3498DB"),(int(self.sfx_slider.x+config.SFX_VOL*200),self.sfx_slider.centery),8)

        pygame.draw.rect(screen,pygame.Color("#E67E22"),self.round_reset_btn,border_radius=6)
        rr_txt=font.render("RESET ROUND",True,pygame.Color("#FFFFFF"))
        screen.blit(rr_txt,rr_txt.get_rect(center=self.round_reset_btn.center))

        pygame.draw.rect(screen,pygame.Color("#E74C3C"),self.data_reset_btn,border_radius=6)
        dr_txt=font.render("DELETE ALL DATA",True,pygame.Color("#FFFFFF"))
        screen.blit(dr_txt,dr_txt.get_rect(center=self.data_reset_btn.center))

        pygame.draw.rect(screen,pygame.Color("#95A5A6"),self.close_btn,border_radius=6)
        c_txt=font.render("BACK TO GAME",True,pygame.Color("#FFFFFF"))
        screen.blit(c_txt,c_txt.get_rect(center=self.close_btn.center))