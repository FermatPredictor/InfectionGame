# -*- coding: utf-8 -*-
import pygame
from pygame import Color
from abc import ABC, abstractmethod

        
class AbstactScene(ABC):
    """
    遊戲場景
    """
    def __init__(self, screen):
        self.screen = screen
        self.FPS = 30 # 定義每秒鐘執行遊戲迴圈30次
        self.clk = 0 # 計時，過了幾個單位時間
        
    
    def text(self, pos, txt, font_size=24, font_color=(0,0,0), bg_color=None):
        """
        在指定位置顯示msg
        pos(tuple of x,y): 位置
        txt(str): 欲顯示的訊息
        font_size(int): 字體大小
        font_color(tuple of RGB): 字體顏色
        bg_color(tuple of RGB): 字體底色
        """
        font = pygame.font.SysFont("simhei", font_size)  #下方訊息字體
        txt = font.render(txt, True, font_color, bg_color)
        self.screen.blit(txt, pos)  #繪製訊息
        return txt.get_rect()
        
    def background(self, color = (255,255,255)):
        """
        可以取得一張指定背景色的畫布。
        """
        background = pygame.Surface(self.screen.get_size())  
        background = background.convert() #為畫布建立副本，加快顯示速度
        background.fill(color)
        self.screen.blit(background, (0,0))
        
    @abstractmethod
    def wait_for_key(self):
        """
        等待外來之滑鼠、鍵盤指令。
        回傳一個數字切換楊景、或回傳一個字串表示指令
        """
        pass
    
    @abstractmethod
    def per_run(self, cmd):
        """
        定義在一個單位時間裡面做什麼事。
        cmd: 接收到的外部指令，以字串表示
        
        讓繼承的class覆寫此方法，讓遊戲開發更專注遊戲邏輯本身
        (標準定為每秒有30個單位時間)
        """
        pass
        
        
    def run(self):
        """
        透過回傳一個數字切換楊景
        """
        clock = pygame.time.Clock() #重要，計時物件
        while True:
            clock.tick(30)
            self.clk += 1
            cmd = self.wait_for_key()
            if type(cmd)==int:
                return cmd
            self.per_run(cmd)
            pygame.display.update()  #更新繪圖視窗

class Sample_Scene(AbstactScene):
    def wait_for_key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed()  #檢查滑鼠按鈕
                if buttons[0]:  #滑鼠左鍵
                    return 'click'
            
    def per_run(self, cmd):
        self.background(Color('green')) #在繪圖視窗繪製畫布
        rect = self.text((20,10), "這是一個範例測試", 32, Color('red'),Color('white')) #紅字白底
        if cmd=='click' and rect.collidepoint(pygame.mouse.get_pos()):
            print('文字被點擊')
        

class SceneFactory():
    MAP = {}
    
    @staticmethod
    def run(scene_id, screen, *arg):
        scene = SceneFactory.MAP[scene_id](screen, *arg)
        return scene.run()


class Game():
    """
    遊戲主體，控制切換場景。
    class Scene透過回傳數字決定跳至哪個場景，回傳0時結束pygame
    """
    def __init__(self, title="Sample", width=640, height=320):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))  #建立繪圖視窗
        self.scene_arg = {} # 記錄每個scene_id是否有額外的參數要給
        pygame.display.set_caption(title)  #繪圖視窗標題
        pygame.font.init()
        pygame.init() # 初始化，必寫
        
    def add_scene(self, scene_id, Scene, *arg):
        SceneFactory.MAP[scene_id] = Scene
        self.scene_arg[scene_id] = arg if arg else tuple()
        
        
    def run(self):
        assert 1 in SceneFactory.MAP, "請先創建一個編號為1的遊戲場景以開始遊戲"
        scene_id = SceneFactory.run(1, self.screen, *self.scene_arg[1])
        while scene_id:
            scene_id = SceneFactory.run(scene_id, self.screen, *self.scene_arg[scene_id])
        pygame.quit()


if __name__=='__main__':
    game = Game()
    game.add_scene(1, Sample_Scene)
    game.run()