	def BT(self, depth):
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