import numpy as np
import pygame
from pygame import Color

import sys
sys.path.append('..')
from __package__ import abstract_scene
from __package__.abstract_sprite import AbstactSprite, ChessBoard

        
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
        self.grid[0][0]= 1
        self.grid[R-1][C-1]= 2
        
        self.next_player = 1
        
        self.ai_on = [False,False]
        self.STATUS = 'IDLE'
        
        self.button_group = pygame.sprite.Group()
        self.button_dict = {
            1: Button('Black AI', (420, 140), (150,50), Color('RoyalBlue')),
            2: Button('White AI', (580, 140), (150,50), Color('RoyalBlue'))
            }
        for button in self.button_dict.values():
            self.button_group.add(button)
            
        self.last_move = None



    def draw_game(self):
        self.background(Color('DarkGray'))
        self.gp = pygame.sprite.Group()
        self.board = ChessBoard(self.grid, (10,10), 400, 
                                last_move = self.last_move)
        self.gp.add(self.board)
        self.gp.update()
        self.gp.draw(self.screen) # 繪製棋盤角色
        
        self.text((410, 10), f'score: B[{np.count_nonzero(self.grid == 1)}], W[{np.count_nonzero(self.grid == 2)}]'
                  , font_size=36)
        self.text((410, 50), f'Black ai: {self.ai_on[0]}', font_size=36)
        self.text((410, 90), f'White ai: {self.ai_on[1]}', font_size=36)
        self.button_group.draw(self.screen)

    def wait_for_key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed()  #檢查滑鼠按鈕
                if buttons[0]:  #滑鼠左鍵
                    return 0 if self.STATUS == 'OVER' else 'click'

    def per_run(self, cmd):
        self.draw_game()
        if cmd=='click':
            if self.STATUS=='IDLE' and self.board.click_cood():
                self.STATUS = 'PRESS'
            print(self.board.click_cood())
            print(self.STATUS)
        """
        if self.game.is_over(self.next_player):
            self.next_player = self.next_player.other
        if cmd=='click':
            # print(self.board.click_cood())
            click_pt = self.board.click_cood()
            if click_pt and not self.ai_on[self.next_player] and self.game.is_legal_moves(self.next_player, Move(click_pt)):
                self.last_move = click_pt
                self.game.place(self.next_player, Move(click_pt))
                self.next_player = self.next_player.other
                
            for key, button in self.button_dict.items():
                if button.isClick():
                     self.ai_on[key] = not self.ai_on[key]
        """

            
def main():
    game = abstract_scene.Game("感染棋遊戲", 800,600)
    game.add_scene(1, PyInfection, 3,4)
    game.run()


if __name__ == '__main__':
    main()