import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def fire_bullet(ai_settings,screen,ship,bullets):
    """发射子弹"""
    if len(bullets)< ai_settings.bullet_allowed:
        new_bullet= Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
def check_play_button(ai_settings,screen,ship,stat,playbtn,mousex,mousey,aliens,bullets):
    """在玩家单击Play按钮时开始新游戏"""
    #检查鼠标单击位置是否在 Play按钮的rect内
    if playbtn.rect.collidepoint(mousex,mousey) and not stat.game_active:
        # 隐藏光标
        pygame.mouse.set_visible(False)
        stat.reset_stats()
        stat.game_active=True
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央 
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按钮按下事件"""
    if event.key == pygame.K_RIGHT:
        ship.move_right=True
    elif event.key == pygame.K_LEFT:
        ship.move_left=True
    elif event.key == pygame.K_UP:
        ship.move_up=True
    elif event.key == pygame.K_DOWN:
        ship.move_down=True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    """响应按钮松开事件"""
    if event.key == pygame.K_RIGHT:
        ship.move_right=False
    elif event.key== pygame.K_LEFT:
        ship.move_left=False
    elif event.key == pygame.K_UP:
        ship.move_up=False
    elif event.key == pygame.K_DOWN:
        ship.move_down=False

def check_events(ai_settings,screen,stat,playbtn,ship,aliens,bullets):
    """检查退出事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,ship, stat,playbtn,mouse_x,mouse_y,aliens,bullets)

def update_screen(ai_settings,screen,stat,ship,aliens,bullets,playbtn):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环都会重新绘制
    screen.fill(ai_settings.bg_color)
    # 在飞船与外星人后面绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    #alien.blitme()
    aliens.draw(screen)
    # 如果游戏处于非活动状态，就绘制Play按钮 
    if not stat.game_active:
        playbtn.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,bullets):
    """更新子弹位置，并删除已经消失的子弹"""
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0 :
            bullets.remove(bullet)
    #print(len(bullets))
    check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)

def  check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹击中了外星人     
    # 如果是这样，就删除相应的子弹和外星人 
    collisions= pygame.sprite.groupcollide(bullets,aliens,True,True)
    if len(aliens) ==0 :
        # 删除现有的子弹并新建一群外星人 
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)

def update_aliens(ai_settings,screen,stat,ship,aliens,bullets):
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置 
    更新外星人群中所有外星人的位置
    """
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # 检测外星人和飞船之间的碰撞 
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stat,screen,ship,aliens,bullets)
    # 检查是否有外星人到达屏幕底端 
    check_aliens_bottom(ai_settings,stat,screen,ship,aliens,bullets)
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left>0:
        # 剩余飞船数目-1
        stats.ships_left-=1
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央 
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active=False
        # 光标可见
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达屏幕底端 """
    rect= screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=rect.bottom:
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direaction(ai_settings,aliens)
            break
def change_fleet_direaction(ai_settings,aliens):
    """将整群外星人下移，并改变它们的方向""" 
    for alien in aliens.sprites():
        alien.rect.y+= ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def get_alien_number(ai_settings,alien_width):
    """计算可以容纳的外星人数目"""
    allowwidth=ai_settings.screen_width-2* alien_width
    num= int(allowwidth/(2*alien_width))
    return num
def get_alien_row(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    allowheight= ai_settings.screen_heigh - 3*alien_height-ship_height
    rows= int(allowheight / (2*alien_height))
    return rows
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建外星人"""
    alien= Alien(ai_settings,screen)
    alien_width= alien.rect.width
    alien.x= alien_width+ 2* alien_width* alien_number
    alien.rect.x= alien.x
    alien.rect.y= alien.rect.height+ 2* alien.rect.height* row_number
    aliens.add(alien)
def create_fleet(ai_settings,screen,ship,aliens):
    """创建一群外星人"""
    # 创建一个外星人，并计算每行可容纳多少个外星人
    alien= Alien(ai_settings,screen)
    num= get_alien_number(ai_settings,alien.rect.width)
    rows= get_alien_row(ai_settings,ship.rect.height,alien.rect.height)
    for row in range(rows):
        for d in range(num):
            create_alien(ai_settings,screen,aliens,d,row)