import sys
import copy
import time
import psutil
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt;
import pylab as pl 

def draw_figure():
	pl.mpl.rcParams['font.sans-serif'] = ['SimHei']
	plt.style.use('ggplot')

	columns = ["n", "solution_cnt", "visited_cnt", "time_used"]
	bt = pd.read_csv("bt_data.csv", header=None, names=columns, index_col="n")
	bt_fc = pd.read_csv("bt_fc_data.csv", header=None, names=columns, index_col="n")
	bt_bit = pd.read_csv("bt_use_bit_data.csv", header=None, names=columns, index_col="n")
	bt_fc_bit = pd.read_csv("bt_fc_use_bit_data.csv", header=None, names=columns, index_col="n")

	fig1 = plt.figure(num=1, figsize=(8,6))
	bt_time = bt.visited_cnt[:8]
	bt_fc_time = bt_fc.visited_cnt[:8]
	bt_bit_time = bt_bit.visited_cnt[:8]
	bt_fc_bit_time = bt_fc_bit.visited_cnt[:8]
	print(len(list(bt_fc_time)))
	plt.plot(range(1, 9), list(bt_time), marker='o', color="r", label="一般回溯")
	plt.plot(range(1, 9), list(bt_fc_time), marker='o', color='g', label="带FC的回溯")
	# plt.plot(range(1, 13), list(bt_bit_time), marker='o', color='b', label="使用位运算的一般回溯")
	# plt.plot(range(1, 13), list(bt_fc_bit_time), marker='o', color='c', label="使用位运算的带FC的回溯")
	plt.ylabel("递归次数/次")
	plt.xlabel("n的大小")
	plt.title("不同的n，不同的方法所递归次数")
	plt.legend()
	plt.tight_layout()
	plt.savefig("visit_cnt_partial.png")
	plt.show()



if __name__ == "__main__":
    draw_figure()