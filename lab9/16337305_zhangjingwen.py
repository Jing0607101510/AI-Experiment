import sys
import copy
import time
import psutil
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt;
import pylab as pl 

class N_Queen():
	def __init__(self, n):
		self.init_board(n)

	def init_board(self, size):
		self.size = size
		self.board = [-1] * self.size
		self.solve_cnt = 0
		self.bit = (1 << self.size) - 1
		self.visited_node = 0
		

	def print_board(self):
		for i in range(self.size):
			for j in range(self.size):
				if self.board[i] != j:
					print("○", end='')
				else:
					print("●", end='')
			print()
		print()

	def get_unassign_row(self):
		for i in range(self.size):
			if self.board[i] == -1:
				return i

	def check(self, row, col):
		for i in range(row):
			if self.board[i] == col:
				return False
			elif abs(i-row) == abs(self.board[i]-col):
				return False
		return True


	def BT(self, depth):
		self.visited_node += 1
		if depth == self.size:#如果所有的变量都被赋值，则打印结果并返回
			self.solve_cnt += 1
			self.print_board()
			return
		
		row = self.get_unassign_row()#找到下一个没有被赋值的变量
		#遍历每一列
		for col in range(self.size):
			#判断这个变量是否还可以取一个可行的值
			if self.check(row, col):
				self.board[row] = col
				self.BT(depth+1)
				self.board[row] = -1
			#如果没有则回溯

	def mrv(self, total_board):
		min_index = -1
		min_remain = sys.maxsize
		for i in range(self.size):
			if self.board[i] == -1 and total_board[i].count(0) < min_remain:
				min_remain = total_board[i].count(0)
				min_index = i
		return min_index


	def BT_FC(self, depth, total_board):
		self.visited_node += 1
		if depth == self.size:#判断是否给所有变量赋值
			self.solve_cnt += 1#可行解数加一
			self.print_board()#打印棋盘
		else:
			row = self.mrv(total_board)#使用mrv找到下一个被赋值的变量
			for col in range(self.size):
				if total_board[row][col] == 0:#对于取值范围的每一个值
					self.board[row] = col
					next_total_board = copy.deepcopy(total_board)
					#使用FC算法改变未赋值的变量的取值范围
					#某个变量的取值范围为空，则需要回溯
					if self.FC(next_total_board, row, col) == False:
						self.board[row] = -1
						continue
					else:#递归
						self.BT_FC(depth+1, next_total_board)
						self.board[row] = -1

	def FC(self, total_board, row, col):
		for i in range(self.size):
			if self.board[i] == -1:
				total_board[i][col] = 1
				diff = i - row
				if 0 <= col + diff < self.size:
					total_board[i][col+diff] = 1
				if 0 <= col - diff < self.size:
					total_board[i][col-diff] = 1
				if total_board[i].count(0) == 0:
					return False
		return True

	def mrv_bit(self, rows, lds, rds):
		min_index = -1
		min_remain = sys.maxsize
		for i in range(self.size):
			if self.board[i] == -1:
				one_cnt = bin((self.bit & (~(rows[i] | lds[i] | rds[i])))).count('1')
				if one_cnt < min_remain:
					min_remain = one_cnt
					min_index = i
		return min_index


	#这里要使用mrv选择下一个需要被赋值的变量
	def BT_FC_use_bit(self, depth, rows, lds, rds):
		self.visited_node += 1
		if depth == self.size:
			self.solve_cnt += 1
			self.print_board()
		else:
			r = self.mrv_bit(rows, lds, rds)
			pos = self.bit & (~(rows[r] | lds[r] | rds[r]))
			while pos:
				one_index = 0
				next_pos = 1
				while next_pos & pos == 0:
					next_pos <<= 1
					one_index += 1
				pos -= next_pos
				self.board[r] = self.size - one_index - 1

				new_rows = copy.deepcopy(rows)
				new_lds = copy.deepcopy(lds)
				new_rds = copy.deepcopy(rds)
				if self.FC_bit(new_rows, new_lds, new_rds, r, next_pos):
					self.BT_FC_use_bit(depth+1, new_rows, new_lds, new_rds)
					self.board[r] = -1
				else:
					self.board[r] = -1


	def FC_bit(self, rows, lds, rds, r, pos):
		for i in range(self.size):
			if self.board[i] == -1:
				rows[i] |= pos	
				if i - r > 0:			
					lds[i] |= pos << (i-r) 
					rds[i] |= pos >> (i-r)
				elif i - r < 0:
					lds[i] |= pos >> (r-i)
					rds[i] |= pos << (r-i)
				if self.bit & (~(rows[i] | lds[i] | rds[i])) == 0:
					return False
		return True




	#这里是按照行的顺序选择下一个赋值的变量
	def BT_use_bit(self, depth, row, ld, rd):
		self.visited_node += 1
		if row == self.bit:
			self.solve_cnt += 1
			self.print_board()
		else:
			pos = self.bit & (~(row | ld | rd))#为1的位置就是可以放置的位置。
			while pos:
				one_index = 0
				next_pos = 1
				while next_pos & pos == 0:
					next_pos <<= 1
					one_index += 1
				pos -= next_pos
				self.board[depth] = self.size - one_index - 1
				self.BT_use_bit(depth+1, row|next_pos, (ld|next_pos)<<1, (rd|next_pos)>>1)
				self.board[depth] = -1

	def draw_figure(self):
		pl.mpl.rcParams['font.sans-serif'] = ['SimHei']
		plt.style.use('ggplot')

		columns = ["n", "solution_cnt", "visited_cnt", "time_used"]
		bt = pd.read_csv("bt_data.csv", header=None, names=columns, index_col="n")
		bt_fc = pd.read_csv("bt_fc_data.csv", header=None, names=columns, index_col="n")
		bt_bit = pd.read_csv("bt_use_bit.csv", header=None, names=columns, index_col="n")
		bt_fc_bit = pd.read_csv("bt_fc_use_bit.csv", header=None, names=columns, index_col="n")

		fig1 = plt.figure(num=1, figsize=(8,6))
		bt_time = bt.time_used
		bt_fc_time = bt_fc.time_used
		bt_bit_time = bt_bit.time_used
		bt_fc_bit_time = bt_fc_bit.time_used
		plt.plot(range(1, 13), list(bt_time), marker='o', color="r")
		plt.plot(range(1, 13), list(bt_fc_time), marker='o', color='g')
		plt.plot(range(1, 13), list(bt_bit_time), marker='o', color='b')
		plt.plot(range(1, 13), list(bt_fc_bit_time), marker='o', color='c')
		plt.tight_layout()
		plt.show()







if __name__ == "__main__":
	while(True):
		n = input("请输入棋盘的长度")
		if str.isdigit(n):
			n = int(n)
			if n == 0:
				break
			else:
				for n in range(1, 13):
					n_queen = N_Queen(n)
					start = time.clock()
					n_queen.BT(0)
					end = time.clock()
					time_used = end - start
					print("一共%s个解"%(n_queen.solve_cnt), "用时%ss"%(end-start))
					print("递归次数：", n_queen.visited_node)
					print("使用内存", psutil.Process(os.getpid()).memory_info().rss)
					
					with open('bt_data.csv', 'a', encoding='utf-8', newline='') as file:
						writer = csv.writer(file)
						writer.writerow([n, n_queen.solve_cnt, n_queen.visited_node, time_used])
					
					n_queen.init_board(n)

					start = time.clock()
					n_queen.BT_use_bit(0, 0, 0, 0)
					end = time.clock()
					time_used = end - start
					print("一共%s个解"%(n_queen.solve_cnt), "用时%ss"%(end-start))
					print("递归次数：", n_queen.visited_node)
					print("使用内存", psutil.Process(os.getpid()).memory_info().rss)
					with open('bt_use_bit_data.csv', 'a', encoding='utf-8', newline='') as file:
							writer = csv.writer(file)
							writer.writerow([n, n_queen.solve_cnt, n_queen.visited_node, time_used])
					n_queen.init_board(n)
				
					total_board = [[0] * n for i in range(n)]
					start = time.clock()
					n_queen.BT_FC(0, total_board)
					end = time.clock()
					time_used = end - start
					print("一共%s个解"%(n_queen.solve_cnt), "用时%ss"%(end-start))
					print("递归次数：", n_queen.visited_node)
					print("使用内存", psutil.Process(os.getpid()).memory_info().rss)
					with open('bt_fc_data.csv', 'a', encoding='utf-8', newline='') as file:
							writer = csv.writer(file)
							writer.writerow([n, n_queen.solve_cnt, n_queen.visited_node, time_used])
					n_queen.init_board(n)
					
					rows = [0] * n
					lds = [0] * n
					rds = [0] * n 
					start = time.clock()	
					n_queen.BT_FC_use_bit(0, rows, lds, rds)
					end = time.clock()
					time_used = end - start
					print("一共%s个解"%(n_queen.solve_cnt), "用时%ss"%(end-start))
					print("递归次数：", n_queen.visited_node)
					print("使用内存", psutil.Process(os.getpid()).memory_info().rss)
					with open('bt_fc_use_bit_data.csv', 'a', encoding='utf-8', newline='') as file:
							writer = csv.writer(file)
							writer.writerow([n, n_queen.solve_cnt, n_queen.visited_node, time_used])
					n_queen.init_board(n)

