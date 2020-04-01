import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_state import GameStat
from button import Button
#from alien import Alien
import game_functions as gf

def run_game():
    pygame.init()
    ai_settings=Settings()
    stat= GameStat(ai_settings)
    screen= pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_heigh))
    pygame.display.set_caption('外星人入侵')
    # 创建Play按钮 
    play_button= Button(ai_settings,screen,'Play')
    ship= Ship(ai_settings,screen)
    #alien = Alien(ai_settings,screen)
    # 存储子弹的编组
    bullets= Group()
    aliens=Group()
    # 创建一群多行外星人
    gf.create_fleet(ai_settings,screen,ship,aliens)
    while True:
        gf.check_events(ai_settings,screen,stat,play_button,ship,aliens,bullets)
        if stat.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stat,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stat,ship,aliens,bullets,play_button)
run_game()