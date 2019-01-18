带FC的回溯算法
BT_FC(depth, total_board)
输入：已经遍历过的变量个数depth, 整个棋盘可行的位置total_board
	if depth就是棋盘的大小：
		打印n个皇后的位置
		return
	else:
		row = mrv()使用MRV方法找到下一个被赋值的变量
		for 对于这一变量的可行域里面的每一个值：
			调用FC方法，改变还没有被赋值的变量的取值范围
			if 存在某一个未赋值变量的取值范围变为0：
				回溯
			else:
				递归调用BT_FC（depth+1， total_board）
				


	