import pygame
from pygame.locals import *
import sys
import copy

class Button():
    def __init__(self, button_name, pos):
        self.name = button_name
        self.position = pos
        self.button_color = (255, 255, 100)
        self.font = pygame.font.SysFont(None, 40)
        self.prep_msg()
    
    def prep_msg(self):
        self.button = self.font.render(self.name, 1, self.button_color)
        self.button_rect = self.button.get_rect()
        self.button_rect.center = self.position
    
    def draw_button(self, screen):
        screen.blit(self.button, self.button_rect)


class Puzzle_15_Gui():
    def __init__(self, puzzles1, puzzles2):
        self.d = [[0,1], [1, 0], [-1, 0], [0,-1]]
        self.moves2 = [
            [2, 3, 2, 3, 1, 1, 0, 0, 2, 3, 3, 3, 1, 0, 0, 2, 3, 3, 1, 0, 2, 2,
             3, 2, 0, 0, 1, 3, 3, 2, 0, 0, 1, 0, 1, 1, 3, 2, 0, 2, 2, 3, 1, 3,
             3, 1, 0, 0, 2, 3, 2, 0, 1, 0, 1, 1],
            [3, 3, 1, 3, 2, 0, 1, 0, 2, 3, 1, 1, 3, 2, 2, 0, 1, 1, 0, 0, 2, 2, 3, 
             3, 1, 1, 1, 3, 2, 0, 1, 0, 2, 3, 1, 3, 2, 2, 0, 0, 0, 1, 3, 3, 2, 0, 1, 1, 0],
            [1, 0, 1, 3, 2, 0, 2, 3, 1, 0, 1, 1, 3, 2, 2, 0, 0, 1, 0, 1, 3, 3, 2, 0, 2, 0,
             1, 1, 3, 2, 2, 2, 0, 1, 1, 1, 3, 2, 2, 2, 3, 3, 1, 1, 0, 1, 0, 2, 2, 2, 0, 1,
            1, 1, 3, 2, 3, 3, 1, 0, 0, 0],
            [1, 3, 3, 2, 0, 0, 2, 0, 1, 1, 3, 3, 2, 0, 2, 0, 2, 3, 1, 0, 1, 3, 2, 3, 3, 1,
             1, 0, 0, 2, 3, 2, 2, 3, 1, 1, 1, 0, 2, 2, 2, 0, 0, 1, 3, 1, 0, 1]
        ]
        self.moves1 = [
            [2, 3, 1, 1, 1, 0, 0, 2, 0, 1],
            [2, 0, 2, 3, 1, 1, 1, 3, 2, 3, 2, 2, 0, 0, 0, 1, 1, 1],
            [1, 3, 3, 2, 0, 0, 0, 1, 3, 3, 3, 2, 0, 0, 0, 1, 3, 2, 2, 3, 2, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 2, 0, 2, 2, 3, 1, 3, 1, 0, 2, 3, 2, 3, 1, 1, 0, 1, 0, 0, 2, 3, 2, 3, 2, 0, 0, 1, 3, 1, 1, 0]
        ]
        self.moves = [self.moves1, self.moves2]
        self.puzzles = [puzzles1, puzzles2]
        pygame.init()
        self.screen_size = (400, 400)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("15-puzzle")
        self.pics = []
        for i in range(16):
           pic = pygame.image.load("pic/%d.png"%(i))
           pic = pygame.transform.scale(pic, (100, 100))
           self.pics.append(pic)
        #pic = pygame.image.load("pic/null.png")
        #pic = pygame.transform.scale(pic, (100, 100))
        #self.pics.append(pic)

        self.clock = pygame.time.Clock()

        self.state = [0, 0]
        
        button_positions = [(200,180), (200, 220), (200, 260), (200, 300)]
        self.button_name = ["A*", "IDA*"]
        self.buttons = []
        for i in range(len(self.button_name)):
            button = Button(self.button_name[i], button_positions[i])
            self.buttons.append(button)
        
        self.choose_button_names = ["first puzzle", "second puzzle", "third puzzle", "fourth puzzle"]
        self.choose_buttons = []
        for i in range(len(self.choose_button_names)):
            button = Button(self.choose_button_names[i], button_positions[i])
            self.choose_buttons.append(button)


        self.screen.fill((100, 200, 100))
        pygame.display.flip()

        self.rects = []
        width = self.screen_size[0] / 4
        height = self.screen_size[1] / 4
        r = 0
        for i in range(4):
            rects = []
            c = 0
            for j in range(4):
                rects.append(pygame.Rect(c, r, width, height))
                c += width
            r += height
            self.rects.append(rects)

    
    def check_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                flag = 0
                for i in range(len(self.buttons)):
                    if self.check_click(self.buttons[i], mouse_x, mouse_y, i):
                        pygame.display.set_caption(self.button_name[i])
                        flag = 1
                        break
                if flag == 1:
                    continue
                for i in range(len(self.choose_buttons)):
                    if self.check_choose_click(self.choose_buttons[i], mouse_x, mouse_y, i):
                        self.draw_procedure()
                        break
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.state[1] != 0:
                        self.state[1] = 0
                        self.draw_choose()
                        pygame.display.set_caption("15-puzzle")
                        pygame.display.flip()
                    elif self.state[1] == 0:
                        self.state = [0, 0]
                        self.draw_button()
                        pygame.display.set_caption("15-puzzle")
                        pygame.display.flip()
    
    def find_zero(self, puzzle):
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] == 0:
                    return i,j
    
    def draw_procedure(self):
        moves = self.moves[self.state[0]-1][self.state[1]-1]
        puzzle = copy.deepcopy(self.puzzles[self.state[0]-1][self.state[1]-1])
        zx, zy = self.find_zero(puzzle)
        for move in moves:
            nzx = zx + self.d[move][0]
            nzy = zy + self.d[move][1]
            shift_num = puzzle[nzx][nzy]
            puzzle[nzx][nzy] = 0
            puzzle[zx][zy] = shift_num
            self.screen.blit(self.pics[shift_num], self.rects[zx][zy])
            self.screen.blit(self.pics[0], self.rects[nzx][nzy])
            self.clock.tick(3)
            pygame.display.flip()
            zx = nzx
            zy = nzy
        return



    def check_click(self, button, x, y, index):
        if button.button_rect.collidepoint(x, y) and self.state == [0, 0]:
            self.state[0] = index+1
            self.draw_choose()
            pygame.display.flip()
            return True
        else:
            return False
    
    def check_choose_click(self, button, x, y, index):
        if button.button_rect.collidepoint(x, y) and self.state[0] != 0 and self.state[1] == 0:
            self.state[1] = index+1
            self.draw_puzzle()
            pygame.display.flip()
            return True
        else:
            return False

    def draw_choose(self):
        self.screen.fill((200, 100, 100))
        for button in self.choose_buttons:
            button.draw_button(self.screen)
 
    def draw_puzzle(self):
        puzzle = self.puzzles[self.state[0]-1][self.state[1]-1]
        for r in range(4):
            for c in range(4):
                self.screen.blit(self.pics[puzzle[r][c]], self.rects[r][c])
        
    def draw_button(self):
        self.screen.fill((100,200,100))
        for button in self.buttons:
            button.draw_button(self.screen)
    
    def main(self):
        self.draw_button()
        pygame.display.flip()
        while True:
            self.check_event()
            pygame.display.flip()



if __name__ == "__main__":
    puzzle5 = [[11, 3, 1, 7], [4, 6, 8, 2], [15, 9, 10, 13], [14, 12, 5, 0]]
    puzzle6 = [[14, 10, 6, 0], [4, 9, 1, 8], [2, 3, 5, 11], [12, 13, 7, 15]]
    puzzle7 = [[0, 5, 15, 14], [7, 9, 6, 13], [1, 2, 12, 10], [8, 11, 4, 3]]
    puzzle8 = [[6, 10, 3, 15], [14, 8, 7, 11], [5, 1, 0, 2], [13, 12, 9, 4]]
    puzzle1 = [ [2,   6,   3,   4],
                    [1,   0,   7,   8],
                    [5,  10,  15,  11],
                    [9,  13,  14,  12]]
    puzzle2 = [ [5,   1,   3,   4],
                [9,   6,   7,   2],
                [10,  14,   0,   8],
                [13,  15,  11,  12]]
    puzzle3 = [[1,   6,   2,   3],
                [5,   7,  11,   4],
                [14,  13,   0,  10],
                [12,   8,   9,  15]]
    puzzle4 = [  [0,   8,   3,   4],
                [6,  12,   2,  15],
                [1,   7,  14,   9],
                [5,  13,  10,  11]]
    puzzles1 = [puzzle1, puzzle2, puzzle3, puzzle4]
    puzzles2 = [puzzle5, puzzle6, puzzle7, puzzle8]
    gui = Puzzle_15_Gui(puzzles1, puzzles2)
    gui.main()

    
