import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """飞船子弹管理类"""
    # Sprite精灵类
    def __init__(self,ai_settings,screen,ship):
        """在飞船所在位置创建一颗子弹"""
        # 2.7 super(Bullet,self).__init__()
        super().__init__()
        self.screen= screen
        # 在（0，0）位置创建一个子弹矩形，然后设置位置
        self.rect= pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx= ship.rect.centerx
        self.rect.top= ship.rect.top
        self.y= float(self.rect.y)
        self.color= ai_settings.bullet_color
        self.speed_factor= ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 使用Group编组的update方法将调用此方法
        self.y-= self.speed_factor
        self.rect.y= self.y
    
    def draw_bullet(self):
        """在屏幕绘制子弹"""
        #pygame.draw.rect(self.screen,self.color,self.rect)
        self.screen.fill(self.color,self.rect)
