#--coding:utf-8--
import pygame
from pygame.locals import *
import sys
import math
import copy

class Button():
    def __init__(self, button_name, pos):
        self.button_color = (255, 255, 100)
        self.button_pos = pos
        self.button_name = button_name

        self.font = pygame.font.SysFont(None, 40)
        self.prep_msg()
    
    def prep_msg(self):
        self.button = self.font.render(self.button_name, 1, self.button_color)
        self.button_rect = self.button.get_rect()
        self.button_rect.center = self.button_pos
    
    def draw_button(self, screen):
        screen.blit(self.button, self.button_rect)

class Maze:
    def __init__(self, search, maze, E_locate, S_locate):
        pygame.init()
        screen_size = (1200, 600)
        
        self.original_maze = maze
        self.maze = copy.deepcopy(self.original_maze)
        self.state = 0
        self.E_locate = E_locate
        self.S_locate = S_locate
        self.end = pygame.image.load("end.jpg")
        self.start = pygame.image.load("start.png")
        self.grass = pygame.image.load("grass.jpg")
        self.road = pygame.image.load("road.jpg")
        self.walkby = pygame.image.load("walkby.png")
        self.walkby2 = pygame.image.load("walkby2.png")
        self.search = search
        self.clock = pygame.time.Clock()

        button_positions = [(600, 150), (600, 180), (600, 210), (600, 240), (600, 270), (600, 300)]
        self.button_names = ['BFS', 'DFS', "Uninformed Search", "Bidirectional Search", 'Iterative Deepening Search', 'A*']
        self.buttons = []
        for i in range(len(self.button_names)):
            button = Button(self.button_names[i], button_positions[i])
            self.buttons.append(button)

        self.screen = pygame.display.set_mode(screen_size)
        
        self.screen.fill((100, 200, 200))
        pygame.display.flip()
        pygame.display.set_caption("Maze")

        self.rects = []
        width =  self.screen.get_rect()[2] / len(self.maze[0]) 
        height = self.screen.get_rect()[3] / len(self.maze)
        self.end = pygame.transform.scale(self.end, (math.floor(width), math.floor(height)))
        self.start = pygame.transform.scale(self.start, (math.floor(width), math.floor(height)))
        self.walkby = pygame.transform.scale(self.walkby, (math.floor(width), math.floor(height)))
        self.walkby2 = pygame.transform.scale(self.walkby2, (math.floor(width), math.floor(height)))

        r = 0
        for i in range(len(self.maze)):#行
            rect = []
            c = 0
            for j in range(len(self.maze[0])):#列
                rect.append(pygame.Rect(c, r, width, height))
                c += width
            r += height
            self.rects.append(rect)



    def check_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if self.check_click_button(button, mouse_x, mouse_y, self.buttons.index(button)+1):
                        pygame.display.set_caption(self.button_names[self.buttons.index(button)])
                        pygame.display.flip()
                        if self.buttons.index(button) != 1:
                            self.search.methods[self.buttons.index(button)]()
                        else:
                            self.search.methods[1](self.S_locate)
                        break
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE and self.state != 0:
                    self.state = 0
                    self.maze = copy.deepcopy(self.maze)
                    #pygame.mouse.set_visible(True)
                    self.screen.fill((100, 200, 200))
                    pygame.display.set_caption("Maze")
                    pygame.display.flip()
                    


    def check_click_button(self, button, x, y, index):
        if button.button_rect.collidepoint(x, y) and self.state == 0:
            self.draw_map()
            pygame.display.flip()
            self.state = index
            #pygame.mouse.set_visible(False)
            return True
        else:
            return False
    


    def draw_map(self):        
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 1:
                    self.screen.blit(self.grass, self.rects[i][j])
                elif self.maze[i][j] == 0:
                    self.screen.blit(self.road, self.rects[i][j])
                elif self.maze[i][j] == 2:
                    self.screen.blit(self.walkby, self.rects[i][j])
        self.screen.blit(self.end, self.rects[self.E_locate[0]][self.E_locate[1]])
        self.screen.blit(self.start, self.rects[self.S_locate[0]][self.S_locate[1]])



    def main(self):
        while True:
            self.check_event()            
            if self.state == 0:
                for button in self.buttons:
                    button.draw_button(self.screen)
            pygame.display.flip()



if __name__ == '__main__':
    with open("MazeData.txt", 'r') as file:
        maze = file.read()
    E_locate = maze.index("E")
    S_locate = maze.index("S")

    maze = maze.strip().replace("S", '0')
    maze = maze.replace("E", '0')

    maze = maze.split("\n")
    for i in range(len(maze)):
        maze[i] = list(map(int, list(maze[i])))
    
    E_locate = (E_locate//(len(maze[0])+1), E_locate%(len(maze[0])+1))
    S_locate = (S_locate//(len(maze[0])+1), S_locate%(len(maze[0])+1))

    maze_gui = Maze(maze, E_locate, S_locate)
    maze_gui.main()
    





        



