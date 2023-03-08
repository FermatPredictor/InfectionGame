# -*- coding: utf-8 -*-
import pygame
from pygame import Color
"""
For more color keyword, See
print(pygame.color.THECOLORS) or
https://htmlcolorcodes.com/color-names/
"""
import numpy as np


class AbstactSprite(pygame.sprite.Sprite):
    
    def __init__(self, ini_pos, size, pic_path=None, color=None, *groups):
        """
        初始化pygame.sprite.Sprite物件
        ini_pos(tuple): 初始x,y座標(左上角)
        size(tuple): 物件之矩形框大小
        picture_path: 若存在，則讀取指定圖檔
        color(RGB): 顏色
        *groups: 源碼定義的參數，sprite屬於哪些group
        """
        super().__init__(*groups)
        self.image = pygame.Surface(size).convert_alpha() #支援透明色彩
        self.image.fill((255,255,255,0)) # 背景透明
        self.size = size
        if color:
            self.image.fill(color)
        if pic_path:
            self.image = pygame.image.load(pic_path)
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = ini_pos
        
    def text(self, txt, font_size=24, font_color=(0,0,0), bg_color=None, font_type="simhei"):
        """
        在角色的中間填寫文字(通常拿來做按鈕之類的角色物件)
        """
        font = pygame.font.SysFont(font_type, font_size)  #下方訊息字體
        txt = font.render(txt, True, font_color, bg_color)
        text_rect = txt.get_rect(center=(self.size[0]/2, self.size[1]/2))
        self.image.blit(txt, text_rect) #繪製訊息
        return txt.get_rect()
    
    def isClick(self):
        """
        檢查物件是否被滑鼠點擊了
        """
        return self.rect.collidepoint(pygame.mouse.get_pos())


class Block(AbstactSprite):
    def __init__(self, pos, size, color, chess, border_radius=0, mode = 'standard', customer_dict=None, hint=False, last_move=False):
        """
        chess: int，表示棋子種類。
        mode: 有'standard', 'txt', 'pic'三種可以選。
        * 'standard': 標準圓形棋子，標準情況下 0為空格、1為黑棋、2為白棋
        * txt: 顯示文字，而非以「1為黑棋、2為白棋」來畫(如2048棋盤即為此形式)
        * pic: 顯示圖片，需自備圖檔及傳入自定義字典表示顯示哪些圖
        customer_dict: 自定義字典
        hint: 值為True 時，畫黑圈提示可落子點
        last_move: 提示上一手棋的位置
        """
        super().__init__(pos, size)
        pygame.draw.rect(self.image, color, pygame.Rect(0,0, *size), border_radius=border_radius)
        if hint:
            pygame.draw.circle(self.image, Color('black'), center=(self.size[0]/2, self.size[1]/2), radius= size[0]//2-4, width=3)
        if not chess:
            return
        
        if mode=='standard':
            color = Color('black' if chess == 1 else 'white')
            pygame.draw.circle(self.image, color, center=(self.size[0]/2, self.size[1]/2), radius= size[0]//2-4)   
        elif mode=='txt':
            self.text(str(customer_dict[chess] if customer_dict else chess), font_size=30, font_type='Comic Sans MS')
        elif mode=='pic':
            print('此功能開發中')
            
        if last_move:
            pygame.draw.circle(self.image, Color('red'), center=(self.size[0]/2, self.size[1]/2), radius= size[0]//4-4)

            
class ChessBoard(pygame.sprite.Sprite):

    def __init__(self, grid, pos: tuple, size: int, color = Color('BurlyWood'), \
                 color_board = None,
                 spacing = 1, border_radius=0, mode= 'standard', customer_dict=None,
                 hint=None, last_move=None, *groups):
        """
        棋盤GUI物件: 
        grid: 一個二維矩陣，用來標示方格內的棋子種類(標準1為黑棋、2為白棋)
        pos: 棋盤左上角座標
        size: 棋盤邊長
        color: 棋格顏色(一個tuple或一個自定義的字典)
        color_board: 優先權比color更大，用來指定哪一格要什麼顏色(用在感染棋按下棋格要變色的遊戲)
        spacing: 棋格之間的空格
        
        mode: 有'standard', 'txt', 'pic'三種可以選。
        * 'standard': 標準圓形棋子，標準情況下 0為空格、1為黑棋、2為白棋
        * txt: 顯示文字，而非以「1為黑棋、2為白棋」來畫(如2048棋盤即為此形式)
        * pic: 顯示圖片，需自備圖檔及傳入自定義字典表示顯示哪些圖
        
        customer_dict: 自定義字典
        hint: 用於像黑白棋的遊戲，提示可以落子的座標
        last_move: 提示上一手棋的位置
        """
        super().__init__(*groups)
        self.image = pygame.Surface((size, size)).convert_alpha() #支援透明色彩
        self.image.fill((255,255,255,0)) # 背景透明
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.grid = np.array(grid)
        self.board_sz = size
        self.color = color
        self.color_board = color_board
        self.spacing = spacing
        self.border_radius = border_radius
        self.mode = mode
        self.customer_dict = customer_dict
        self.hint = hint
        self.last_move = last_move
        
    def update(self):
        blockgroup = pygame.sprite.Group()
        
        r, c = self.grid.shape
        grid_sz_plus = self.board_sz/max(r,c)

        for i in range(r):
            for j in range(c):
                rect_x = j * grid_sz_plus + self.spacing
                rect_y = i * grid_sz_plus + self.spacing
                grid_sz = grid_sz_plus - 2 * self.spacing
                
                hint_bool = bool(self.hint) and (i,j) in self.hint
                last_move_bool = bool(self.last_move) and (i,j)==self.last_move

                color = self.color[self.grid[i][j]] if type(self.color)==dict else self.color
                if self.color_board and self.color_board[i][j]:
                    color = self.color_board[i][j]
                block = Block((rect_x, rect_y), (grid_sz, grid_sz), color, self.grid[i][j], 
                              self.border_radius, self.mode, self.customer_dict, hint_bool, last_move_bool)
                blockgroup.add(block)  #加入全部角色群組
        blockgroup.draw(self.image)  #繪製所有角色
    
    def click_cood(self):
        """
        回傳滑鼠點擊的棋盤格座標
        """
        x, y = pygame.mouse.get_pos()
        r, c = self.grid.shape
        grid_sz_plus = self.board_sz/max(r,c)
        for i in range(r):
            for j in range(c):
                rect_x = j * grid_sz_plus + self.spacing
                rect_y = i * grid_sz_plus + self.spacing
                grid_sz = grid_sz_plus - 2 * self.spacing
                if rect_x <= x <= rect_x+grid_sz and rect_y <= y <= rect_y+grid_sz:
                    return (i,j)
    
        
        