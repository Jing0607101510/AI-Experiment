from gui import Maze
import pygame
import copy
import math

time_count = 0
space_count = 0
class Search():
    def __init__(self, maze_file):
        self.original_maze, self.S_locate, self.E_locate = self.read_maze(maze_file)
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] #下，上，右，左
        self.methods = [self.BFS, self.DFS, self.uninformed_search, self.bidirectiondal_search, self.iterative_deepening_search, self.A_star]
        self.maze_gui = Maze(self, self.original_maze, self.E_locate, self.S_locate)
        self.maze_gui.main()
        

    def read_maze(self, maze_file):
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

        global s_locate
        s_locate = S_locate

        return maze, S_locate, E_locate

    def check_legel(self, pos, type=2):
        if pos[0] < 0 or pos[0] >= len(self.maze) or pos[1] < 0 or pos[1] >= len(self.maze[0]):
            return False
        elif self.maze[pos[0]][pos[1]] == 1 or self.maze[pos[0]][pos[1]] == type:
            return False
        else:
            return True

    #A*算法
    def A_star(self):
        if self.S_locate == self.E_locate:#
            return
        self.maze = copy.deepcopy(self.original_maze)
        
        time_count = 0
        space_count = 0

        boundary = []
        cost = []
        f = []
        g = []
        boundary.append(self.S_locate)
        g.append(0)
        f.append((abs(self.S_locate[0]-self.E_locate[0])+abs(self.S_locate[1]-self.E_locate[1])))

        self.maze[self.S_locate[0]][self.S_locate[1]] = 2
        flag = 0
        while len(boundary) and (not flag):
            min_cost = min(f)
            index = f.index(min_cost)
            min_node = boundary[index]
            boundary.pop(index)
            g_cost = g.pop(index)
            f.pop(index)

            time_count += 1
            space_count = max(len(boundary) + 1, space_count)
            if list(min_node) == list(self.E_locate):
                flag = 1
                break
            else:
                self.maze[min_node[0]][min_node[1]] = 2
                self.maze_gui.screen.blit(self.maze_gui.walkby2, self.maze_gui.rects[min_node[0]][min_node[1]])
                self.maze_gui.clock.tick(80)
                pygame.display.flip()

                for direction in self.directions:
                    next_pos = list(map(lambda x:x[1]+x[0], zip(direction, min_node)))
                    if self.check_legel(next_pos):
                        if next_pos not in boundary:
                            boundary.append(next_pos)
                            g.append(g_cost+1)
                            f.append(g_cost+1+abs(next_pos[0]-self.E_locate[0])+abs(next_pos[1]-self.E_locate[1]))
                        elif f[boundary.index(next_pos)] > g_cost+1+abs(next_pos[0]-self.E_locate[0])+abs(next_pos[1]-self.E_locate[1]):
                            f[boundary.index(next_pos)] = g_cost+1+abs(next_pos[0]-self.E_locate[0])+abs(next_pos[1]-self.E_locate[1])
                            g[boundary.index(next_pos)] = g_cost + 1
        print("A*")
        print("node had been visited:", time_count)
        print("space to save node:", space_count)
        print()

    #一致代价搜索
    def uninformed_search(self):
        if self.S_locate == self.E_locate:
            return
        self.maze = copy.deepcopy(self.original_maze)
        boundary = []
        cost = []
        boundary.append(self.S_locate)
        cost.append(0)

        time_count = 0
        space_count = 0

        self.maze[self.S_locate[0]][self.S_locate[1]] = 2
        flag = 0
        while len(boundary) and (not flag):
            min_cost = min(cost)
            min_node = boundary[cost.index(min_cost)]
            boundary.pop(cost.index(min_cost))
            cost.pop(cost.index(min_cost))

            time_count += 1
            space_count = max(space_count, len(boundary) + 1)
            #判断当前节点是否未目标节点
            if list(min_node) == list(self.E_locate):
                flag = 1
                break
            else:
                self.maze[min_node[0]][min_node[1]] = 2
                self.maze_gui.screen.blit(self.maze_gui.walkby, self.maze_gui.rects[min_node[0]][min_node[1]])
                self.maze_gui.clock.tick(140)
                pygame.display.flip()
                #遍历四个方向
                for direction in self.directions:
                    #获得四个方向上的节点的坐标
                    next_pos = list(map(lambda x:x[1]+x[0], zip(direction, min_node)))
                    #判断位置节点是否合法或者是否访问过
                    if self.check_legel(next_pos):
                        #如果还没姐如果边界集合里，则直接加入边界集合
                        if next_pos not in boundary:
                            boundary.append(next_pos)
                            cost.append(min_cost+1)
                        #否则已经加入过边界集合里，还要比较集合里面的这个节点的花费和现在所算的花费，
                        #用小的值替换花费
                        elif cost[boundary.index(next_pos)] > min_cost+1:
                            cost[boundary.index(next_pos)] = min_cost+1
        
        print("uninformed_search")
        print("node had been visited:", time_count)
        print("space to save node:", space_count)
        print()




    
    def BFS(self):
        if self.S_locate == self.E_locate:
            return
        self.maze = copy.deepcopy(self.original_maze)
        queue = []
        queue.append(self.S_locate)
        self.maze[self.S_locate[0]][self.S_locate[1]] = 2
        flag = 0
        time_count = 1
        space_count = 0
        #节点还没完全遍历过则继续遍历
        while len(queue):
            space_count = max(space_count, len(queue))
            top = queue.pop(0)#获得队列中第一个节点
            for direction in self.directions:
                #对当前节点每一个方向得到一个位置节点
                next_pos = list(map(lambda x:x[0]+x[1], zip(top, direction)))
                #判断这个位置是否合法，是否已经遍历过
                if self.check_legel(next_pos):
                    #如果这个位置的位置节点就是目标节点，已经找到，退出
                    time_count += 1
                    if next_pos == list(self.E_locate):
                        flag = 1
                        break
                    else:#如果不是目标节点
                        queue.append(next_pos)#否则加入到队列之中
                        self.maze[next_pos[0]][next_pos[1]] = 2#标识为已经访问过
                        self.maze_gui.screen.blit(self.maze_gui.walkby, self.maze_gui.rects[next_pos[0]][next_pos[1]])
                        self.maze_gui.clock.tick(100)
                        pygame.display.flip()            
            if flag == 1:
                break
        
        print("BFS")
        print("node had been visited:", time_count)
        print("space to save node:", space_count)
        print()
        


    def DFS(self, pos):     
        global time_count
        global space_count     
        time_count += 1
        space_count += 1          
        if list(pos) == list(self.E_locate):
            print("DFS")
            print("node had been visited:", time_count)
            print("space to save node:", space_count)
            print()
            return True
        if list(pos) != list(self.S_locate):
            self.maze_gui.screen.blit(self.maze_gui.walkby2, self.maze_gui.rects[pos[0]][pos[1]])
            self.maze_gui.clock.tick(50)
            pygame.display.flip()
        else:
            self.maze = copy.deepcopy(self.original_maze)
            time_count = 0
            space_count = 0
        self.maze[pos[0]][pos[1]] = 2

        #对于当前节点的每一个方向上的子节点
        for direction in self.directions:
            #获取这个方向上的位置节点
            next_pos = list(map(lambda x:x[0]+x[1], zip(pos, direction)))
            #判断这个节点是否合法，同时是否访问过
            if self.check_legel(next_pos):
                #在未访问过的情况下，递归搜索这个子节点
                if self.DFS(next_pos):
                    return True
        return False

        
        
    
    def bidirectiondal_search(self):
        if self.S_locate == self.E_locate:
            return
        self.maze = copy.deepcopy(self.original_maze)
        queue_start = []
        queue_end = []
        queue_start.append(self.S_locate)
        queue_end.append(self.E_locate)
        self.maze[self.S_locate[0]][self.S_locate[1]] = 2
        self.maze[self.E_locate[0]][self.E_locate[1]] = 3
        time_count = 2
        space_count = 0
        flag = 0
        #在没找到两个搜索还没有相交的时候，而且两个搜索的队列都不为空的时候
        while len(queue_end) or len(queue_start):
            space_count = len(queue_end) + len(queue_start)
            #起点处的宽度优先搜索一层
            if len(queue_start):
                top = queue_start.pop(0)#获取这一个队列中的第一个节点
                for direction in self.directions:
                    #得到其合法的未遍历的节点
                    next_pos = list(map(lambda x:x[0]+x[1], zip(top, direction)))
                    if self.check_legel(next_pos, 2):
                        #判断是否相交
                        time_count += 1
                        if self.maze[next_pos[0]][next_pos[1]] == 3:
                            flag = 1
                            break
                        else:#未相交则加入队列之中
                            queue_start.append(next_pos)
                            self.maze[next_pos[0]][next_pos[1]] = 2
                            self.maze_gui.screen.blit(self.maze_gui.walkby, self.maze_gui.rects[next_pos[0]][next_pos[1]])
                            self.maze_gui.clock.tick(80)
                            pygame.display.flip()
            if flag: break   #相交则退出
            #终点处的宽度优先搜索一层
            if len(queue_end):
                top = queue_end.pop(0)
                for direction in self.directions:
                    next_pos = list(map(lambda x:x[0]+x[1], zip(top, direction)))
                    if self.check_legel(next_pos, 3):
                        time_count += 1
                        if self.maze[next_pos[0]][next_pos[1]] == 2:
                            flag = 1
                            break
                        else:
                            queue_end.append(next_pos)
                            self.maze[next_pos[0]][next_pos[1]] = 3
                            self.maze_gui.screen.blit(self.maze_gui.walkby2, self.maze_gui.rects[next_pos[0]][next_pos[1]])
                            self.maze_gui.clock.tick(80)
                            pygame.display.flip()
            if flag: break
        print("bidirectiondal_search")
        print("node had been visited:", time_count)
        print("space to save node:", space_count)
        print()

    def iterative_deepening_search(self):
        global time_count
        global space_count
        time_count = 0
        space_count = 0
        self.maze = copy.deepcopy(self.original_maze)
        max_deep = 1#当前的最大深度
        flag = 0#是否找的目标
        while not flag:#如果没找的目标则继续循环
            if self.deepening_DFS(self.S_locate, max_deep=max_deep):
                flag = 1#如果找到目标则退出
            max_deep += 1#如果没有找到目标，则限制的最大深度加一
        print("iterative_deepening_search")
        print("node had been visited:", time_count)
        print("space to save node:", space_count)
        print()



    def deepening_DFS(self, pos, max_deep, cur_deep=1):
        global time_count
        global space_count
        time_count += 1
        space_count += 1
        if list(pos) == list(self.E_locate):
            return True
        if list(pos) != list(s_locate):
            self.maze_gui.screen.blit(self.maze_gui.walkby2, self.maze_gui.rects[pos[0]][pos[1]])
            #self.maze_gui.clock.tick(100)
            pygame.display.flip()
        else:
            self.maze = copy.deepcopy(self.original_maze)
        self.maze[pos[0]][pos[1]] = 2

        if cur_deep != max_deep:
            for direction in self.directions:
                next_pos = list(map(lambda x:x[0]+x[1], zip(pos, direction)))
                if self.check_legel(next_pos):
                    if self.deepening_DFS(next_pos, max_deep, cur_deep+1):
                        return True
        return False

            


if __name__ == "__main__":
    maze_file = "MazeData.txt"
    search = Search(maze_file)
