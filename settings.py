class Settings():
    def __init__(self):
        self.screen_width=1000
        self.screen_heigh=600
        self.bg_color=(230,230,230)
        # 飞船移动速度
        self.ship_speed_factor=1.5
        self.ship_limit=3
        # 子弹设置
        self.bullet_speed_factor=1
        self.bullet_width=3
        self.bullet_height=15
        # 深灰色
        self.bullet_color=60,60,60
        self.bullet_allowed=3
        # 外星人设置
        self.alien_speed_factor=1
        self.fleet_drop_speed=10
        self.fleet_direction=1
