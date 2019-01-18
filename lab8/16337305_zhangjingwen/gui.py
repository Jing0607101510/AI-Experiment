import pygame
from pygame.locals import *
import os
import math
import sys
from WhiteBlack import WhiteBlack
import time

WIDTH = 1000
HEIGHT = 720
FPS = 30
GRID_WIDTH = HEIGHT // 8

PEOPLE = -1
AI = 1
NULL = 0

BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 50, 50)
GREEN_COLOR = (50, 255, 50)
GRAY_COLOR = (200, 200, 200)
BLUE_COLOR = (50, 50, 255)

class Scoreboard():
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)


    def show_score(self, score=[0,0], people_step='-', AI_step='-'):#score是拥有两个元素的列表
        play_str = "People : AI"
        score_str = "%d : %d" % (score[0], score[1]) 
        self.score_img = self.font.render(score_str, True, self.text_color)
        self.play_img = self.font.render(play_str, True, self.text_color)
        self.score_rect = self.score_img.get_rect()
        self.play_rect = self.play_img.get_rect()

        self.play_rect.right = self.screen_rect.right - 100
        self.play_rect.top = 100

        self.score_rect.right = self.screen_rect.right - 100
        self.score_rect.top = self.play_rect.bottom + 10

        
        self.people_step_img = self.font.render("People Move: "+people_step, True, self.text_color)
        self.people_step_rect = self.people_step_img.get_rect()
        self.people_step_rect.right = self.screen_rect.right - 50
        self.people_step_rect.top = self.score_rect.bottom + 100
        self.screen.blit(self.people_step_img, self.people_step_rect)
        
        self.AI_step_img = self.font.render("AI Move: "+AI_step, True, self.text_color)
        self.AI_step_rect = self.AI_step_img.get_rect()
        self.AI_step_rect.right = self.screen_rect.right - 50
        self.AI_step_rect.top = self.people_step_rect.bottom + 10
        self.screen.blit(self.AI_step_img, self.AI_step_rect)

        self.screen.blit(self.play_img, self.play_rect)
        self.screen.blit(self.score_img, self.score_rect)
    
    def draw_who_turn(self, turn):
        if turn == AI:
            turn_msg = self.font.render("AI Turn!", True, RED_COLOR)
            turn_msg_rect = turn_msg.get_rect()
            turn_msg_rect.bottom =  self.screen_rect.bottom - 200
            turn_msg_rect.right = self.screen_rect.right - 50
            self.screen.blit(turn_msg, turn_msg_rect)
        elif turn == PEOPLE:
            turn_msg = self.font.render("People Turn!", True, RED_COLOR)
            turn_msg_rect = turn_msg.get_rect()
            turn_msg_rect.bottom =  self.screen_rect.bottom - 200
            turn_msg_rect.right = self.screen_rect.right - 50
            self.screen.blit(turn_msg, turn_msg_rect)






class Button():
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (0, 0, 255)
        self.text_color = (50, 200, 50)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)
    
    def prep_msg(self, msg):
        #指定文本颜色，背景颜色
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        #填充按钮颜色
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)



class Game_GUI():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("黑白棋")
        self.clock = pygame.time.Clock()

        base_dir = os.path.dirname(__file__)
        img_dir = os.path.join(base_dir, "img")
        self.background_img = pygame.image.load(os.path.join(img_dir, "back.png")).convert()
        
        self.font_name = pygame.font.get_default_font()

        self.play_button = Button(self.screen, "Play")
        self.scoreboard = Scoreboard(self.screen)

        self.game_stats = 0
        self.movements = []

        self.score = [0, 0]#第一个是people分数，第二个是AI分数#不用在whiteblack里
        self.people_step = ['-']
        self.AI_step = ['-']
        self.turn = -1 #人类玩家先下//不用在whiteblack里
        self.possible_place = []

        self.whiteBlack = WhiteBlack(self)


    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if self.game_stats == 1 and self.turn == PEOPLE:
                        self.draw_possible_place()
                        self.scoreboard.draw_who_turn(self.turn)
                        self.turn = self.whiteBlack.start_game(self.turn, event)
                        if self.turn == NULL:
                            self.show_game_over()

                    elif self.game_stats == 0:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if self.check_play_button(mouse_x, mouse_y):
                            self.game_stats = 1
                elif event.type == KEYDOWN:#做清空初始化操作
                    if event.key == K_ESCAPE and self.game_stats != 0:
                        self.init_stats()
                    elif self.game_stats == 2:#游戏结束了,按任意键回到初始界面
                        self.game_stats = 0
                    #测试用
                    elif event.key == K_SPACE and self.game_stats == 1:
                        self.show_game_over()

                        
            if self.game_stats == 0:#开始状态
                self.screen.fill((255, 200, 100))
                self.play_button.draw_button()
            elif self.game_stats == 1:#游戏状态
                if self.turn == AI:
                    self.draw_possible_place()
                    self.turn = self.whiteBlack.start_game(self.turn, event)
                    if self.turn == NULL:
                        self.show_game_over()
                    else:
                        self.draw_background()
                        self.draw_movements()
                        self.draw_possible_place()
                else:
                    self.draw_background()
                    self.draw_movements()
                    self.draw_possible_place()
                self.scoreboard.show_score(self.score, str(self.people_step[-1]), str(self.AI_step[-1]))
                self.scoreboard.draw_who_turn(self.turn)
            elif self.game_stats == 2:#结束状态
                self.show_game_over()
            self.clock.tick(FPS)
            pygame.display.flip()

    
    def init_stats(self):
        self.movements.clear()
        self.AI_step = ['-']
        self.people_step = ['-']
        self.game_stats = 0
        self.score = [0, 0]
        self.turn = -1#人类先下
        self.possible_place = []
        self.whiteBlack.init_board()


    def show_game_over(self):
        self.game_stats = 2#游戏结束状态
        font = pygame.font.Font(self.font_name, 50)
        if self.score[0] > self.score[1]:
            win_msg = font.render("%s : %s, You Win!"%(self.score[0], self.score[1]), True, RED_COLOR)
        elif self.score[0] < self.score[1]:
            win_msg = font.render("%s : %s, AI Win!"%(self.score[0], self.score[1]), True, GREEN_COLOR)
        else:
            win_msg = font.render("%s : %s, Tie!"%(self.score[0], self.score[1]), True, GRAY_COLOR)

        win_rect = win_msg.get_rect()
        win_rect.center = self.screen.get_rect().center

        w = pygame.Rect(win_rect)
        w.center = self.screen.get_rect().center

        self.screen.fill(BLUE_COLOR, w)
        self.screen.blit(win_msg, win_rect)





    def check_play_button(self, x, y):
        if self.play_button.rect.collidepoint(x, y):
            return True
        else:
            return False

    def draw_chess(self, pos, player):#注意这里的行列是对换的
        circle_pos = [int((pos[0]+1.5)*GRID_WIDTH), int((pos[1]+1.5)*GRID_WIDTH)]
        if player == PEOPLE:
            color = WHITE_COLOR
        else:
            color = BLACK_COLOR
        self.movements.append([circle_pos, color])
        pygame.draw.circle(self.screen, color, circle_pos, int(GRID_WIDTH*0.4))
    
    def draw_movements(self):
        for m in self.movements:
            pygame.draw.circle(self.screen, m[1], m[0], int(GRID_WIDTH*0.4))

    def draw_background(self):
        #加载背景图片        
        self.screen.blit(self.background_img, (0, 0))
        #画网格线
        rect_lines = [
            ((GRID_WIDTH, GRID_WIDTH), (GRID_WIDTH, HEIGHT-GRID_WIDTH)),#|
            ((GRID_WIDTH, GRID_WIDTH), (HEIGHT-GRID_WIDTH, GRID_WIDTH)),#——
            ((GRID_WIDTH, HEIGHT-GRID_WIDTH), (HEIGHT-GRID_WIDTH, HEIGHT-GRID_WIDTH)),#-
            ((HEIGHT-GRID_WIDTH, GRID_WIDTH), (HEIGHT-GRID_WIDTH, HEIGHT-GRID_WIDTH))#|
        ]
        for line in rect_lines:
            pygame.draw.line(self.screen, BLACK_COLOR, line[0], line[1], 2)
        for i in range(5):
            line1 = ((GRID_WIDTH, (i+2) * GRID_WIDTH), (HEIGHT-GRID_WIDTH, (i+2)*GRID_WIDTH))
            line2 = (((i+2)*GRID_WIDTH, GRID_WIDTH), ((i+2)*GRID_WIDTH, HEIGHT-GRID_WIDTH))
            pygame.draw.line(self.screen, BLACK_COLOR, line1[0], line1[1], 2)
            pygame.draw.line(self.screen, BLACK_COLOR, line2[0], line2[1], 2)

        font = pygame.font.Font(self.font_name, 50)
        for i in range(6):
            text_surface1 = font.render("%d"%i, True, BLACK_COLOR)
            text_rect1 = text_surface1.get_rect()
            text_rect1.center = (int(0.5*GRID_WIDTH), int((i+1.5)*GRID_WIDTH))
            self.screen.blit(text_surface1, text_rect1)

            text_surface2 = font.render("%d"%i, True, BLACK_COLOR)
            text_rect2 = text_surface2.get_rect()
            text_rect2.center = (int((i+1.5)*GRID_WIDTH), int(0.5*GRID_WIDTH))
            self.screen.blit(text_surface2, text_rect2)


        pygame.draw.circle(self.screen, WHITE_COLOR,(int(3.5*GRID_WIDTH), int(3.5*GRID_WIDTH)) ,int(GRID_WIDTH*0.4))
        pygame.draw.circle(self.screen, BLACK_COLOR, (int(4.5*GRID_WIDTH), int(3.5*GRID_WIDTH)), int(GRID_WIDTH*0.4))
        pygame.draw.circle(self.screen, BLACK_COLOR, (int(3.5*GRID_WIDTH), int(4.5*GRID_WIDTH)), int(GRID_WIDTH*0.4))
        pygame.draw.circle(self.screen, WHITE_COLOR, (int(4.5*GRID_WIDTH), int(4.5*GRID_WIDTH)), int(GRID_WIDTH*0.4))
    

    #待更改
    def draw_possible_place(self):
        if self.turn == PEOPLE:
            color = WHITE_COLOR
        else:
            color = BLACK_COLOR
        self.possible_place = self.whiteBlack.find_legal_positions(self.whiteBlack.board, self.turn)#x和y需要互换
  
        for place in self.possible_place:
            pos = [int((place[1]+1.5)*GRID_WIDTH), int((place[0]+1.5)*GRID_WIDTH)]
            pygame.draw.circle(self.screen, color, pos, int(GRID_WIDTH*0.4), 4)

        
    



if __name__ == "__main__":
    game = Game_GUI()
    game.main()





