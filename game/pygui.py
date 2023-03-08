import numpy as np
import pygame
from pygame import Color

import sys
sys.path.append('..')
from __package__ import abstract_scene
from __package__.abstract_sprite import AbstactSprite, ChessBoard
from infection import is_valid, action, is_over

        
class Button(AbstactSprite):
    
     def __init__(self, txt, pos, size, color):
        super().__init__(pos, size, color=color)
        self.text(txt)


class PyInfection(abstract_scene.AbstactScene):
    
    def __init__(self, screen, R, C):
        super().__init__(screen)
        self.R = R
        self.C = C
        
        self.grid = np.array([[0]*C for _ in range(R)])
        self.color_board = [[None]*C for _ in range(R)] # gui繪製指定顏色
        
        self.grid[0][0]= 1
        self.grid[R-1][C-1]= 2
        
        self.next_player = 1
        
        self.pass_turn = 0
        
        self.ai_on = [False,False]
        self.STATUS = 'IDLE'
        
        self.button_group = pygame.sprite.Group()
        self.button_dict = {
            0: Button('Black AI', (420, 140), (150,50), Color('RoyalBlue')),
            1: Button('White AI', (580, 140), (150,50), Color('RoyalBlue'))
            }
        for button in self.button_dict.values():
            self.button_group.add(button)
            
        self.last_move = None



    def draw_game(self):
        self.background(Color('DarkGray'))
        self.gp = pygame.sprite.Group()
        self.board = ChessBoard(self.grid, (10,10), 400, color_board=self.color_board,
                                last_move = self.last_move)
        self.gp.add(self.board)
        self.gp.update()
        self.gp.draw(self.screen) # 繪製棋盤角色
        
        self.text((410, 10), f'score: B[{np.count_nonzero(self.grid == 1)}], W[{np.count_nonzero(self.grid == 2)}]'
                  , font_size=36)
        self.text((410, 50), f'Black ai: {self.ai_on[0]}, White ai: {self.ai_on[1]}', font_size=36)
        self.text((410, 90), f'Turn: {"Black" if self.next_player==1 else "White"}', font_size=36)
        self.button_group.draw(self.screen)

    def wait_for_key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed()  #檢查滑鼠按鈕
                if buttons[0]:  #滑鼠左鍵
                    return 'click'

    def per_run(self, cmd):
        self.draw_game()
        if self.STATUS!='OVER':
            if is_over(self.next_player, self.grid):
                self.pass_turn += 1
                self.next_player = 3-self.next_player
            else:
                self.pass_turn = 0
        if self.pass_turn==2:
            self.STATUS='OVER'
        if cmd=='click':
            if self.STATUS=='IDLE' and self.board.click_cood():
                r, c = self.board.click_cood()
                if self.grid[r][c]==self.next_player:
                    self.color_board[r][c]= Color('LightSkyBlue')
                    self.STATUS = 'PRESS'
                    self.press = (r,c)
            elif self.STATUS == 'PRESS' and self.board.click_cood():
                r, c = self.board.click_cood()
                jr, jc = self.press
                move = None
                if is_valid(self.next_player, self.grid, (jr, jc,r,c)):
                    move = (jr, jc,r,c)
                elif is_valid(self.next_player, self.grid, (-1, -1,r,c)):
                    move = (-1,-1,r,c)
                if move:
                    action(self.next_player, self.grid, move)
                    self.next_player = 3 - self.next_player
                    self.last_move = (r, c)
                self.STATUS='IDLE'
                self.color_board = [[None]*self.C for _ in range(self.R)]
            #print(self.board.click_cood())
            #print(self.STATUS)
            
            for key, button in self.button_dict.items():
                if button.isClick():
                     self.ai_on[key] = not self.ai_on[key]

            
def main():
    game = abstract_scene.Game("感染棋遊戲", 800,600)
    game.add_scene(1, PyInfection, 3,4)
    game.run()


if __name__ == '__main__':
    main()