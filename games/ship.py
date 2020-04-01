import pygame

class Ship():
    def __init__(self,ai_settings, screen):
        self.screen=screen
        self.ai_settings= ai_settings
        # 加载图片并获取外框
        self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()
        # 底部居中
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 存储小数
        self.center= float(self.rect.centerx)
        self.bottom= float(self.rect.bottom)
        self.move_right=False
        self.move_left=False
        self.move_up=False
        self.move_down=False
    def center_ship(self):
        # 底部居中
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def update(self):
        """根据标准移动飞船"""
        if self.move_right and self.rect.right< self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.move_left and self.rect.left>0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.move_down and self.rect.bottom<self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed_factor
        if self.move_up and self.rect.top>0:
            self.bottom -= self.ai_settings.ship_speed_factor
        self.rect.centerx= self.center
        self.rect.bottom= self.bottom
    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image,self.rect)