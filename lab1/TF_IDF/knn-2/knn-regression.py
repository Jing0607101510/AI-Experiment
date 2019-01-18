import csv
import time
import math
import collections
import pandas as pd
import numpy as np
import csv

#正确
def read_file(file_name):
	data = pd.read_csv(file_name)
	motion = data.values[:, 1:]
	sentence = data.values[:, 0]
	for i in range(len(sentence)):
		sentence[i] = set(sentence[i].split(' '))
	return [sentence, motion]

	


def read_test_file(file_name):
	data = pd.read_csv(file_name)
	sentence = data.values[:,1]
	for i in range(len(sentence)):
		sentence[i] = set(sentence[i].split(' '))
	return sentence


#计算验证集/测试集与训练集的距离
def calc_distance(train, test, dis_type):
	#dis_type=1街区距离
	if dis_type == 1:
		return len(train^test)
		

	#dis_type=2欧式距离
	elif dis_type == 2:
		return math.sqrt(len(train^test))
		
	#dis_type=3余弦相似度
	elif dis_type == 3:
		return (len(train&test))/(math.sqrt(len(train)*len(test)))


##找出k个距离最近的训练集文本
def find_knn(all_train_lines, validation_line, k, dis_type):
	dis = []#保存验证集/测试集的距离
	for i in range(len(all_train_lines)):#计算与训练集的距离
		dis.append(calc_distance(all_train_lines[i], validation_line, dis_type))

	z = list(zip(list(range(len(all_train_lines))), dis))#将距离和下标连结
	z.sort(key = lambda y : y[1])#按照距离从小到大排序
	if dis_type == 3:#如果用的是余弦相似度，则按从大到小排序
		z.reverse()
	return z[:k] #列表，形式：[(下标，距离)，...] #返回前k个训练集文本的下标和距离

	


#找出每一行验证集/测试集的各个情感label的概率
def find_motion(knn, motion, dis_type):
	knn_index = []#记录k个下标
	knn_dis = []#记录k个最小距离
	for index, distance in knn:
		knn_index.append(index)
		knn_dis.append(distance)

	#如果不是用余弦相似度算距离
	if dis_type != 3:
		if 0 in knn_dis:#距离为零的情况，直接选区其label的概率
			index = knn_dis.index(0)
			return motion[knn_index[index]]
		else:#否则对k个label的概率加权并归一化
			motion_array = (motion[knn_index,:]).transpose()
			motion_array = sum((motion_array / knn_dis).transpose())
			motion_array = motion_array / sum(motion_array)
			return motion_array
	#用余弦相似度算的距离
	else:
		#如果距离为0，直接选区其label的概率
		if 1 in knn_dis:
			index = knn_dis.index(1)
			return motion[knn_index[index]]
		else:#否则对k个label的概率加权并归一化
			knn_dis = np.array(knn_dis)
			knn_dis = (knn_dis + 1) / 2
			motion_array = (motion[knn_index,:]).transpose()
			motion_array = sum((motion_array * knn_dis).transpose())#这里我们乘以余弦相似度
			motion_array = motion_array / sum(motion_array)
			return motion_array


def write_to_file(result, dis_type):
	label = ["textid", "anger", "disgust", "fear", "joy", "sad", "surprise"]
	with open("16337305_Zhangjingwen_KNN_regression(%s).csv"%(dis_type), "w", newline='') as file:
		writer = csv.writer(file)
		writer.writerow(label)
		for r in result:
			writer.writerow(r)





def main():
	train_file_name = "train_set.csv"
	validation_file_name = "validation_set.csv"
	test_file_name = "test_set.csv"
	[all_train_lines,train_motion] = read_file(train_file_name)
	[all_validation_lines, validation_motion] = read_file(validation_file_name)
	all_test_lines = read_test_file(test_file_name)
	

	for dis_type in range(1, 4):
		validation_size = len(validation_motion)
		for k in range(2, 18):
			data = np.empty([0, 6])
			for i in range(validation_size):
				knn = find_knn(all_train_lines, all_validation_lines[i], k, dis_type) #knn[(index, distance),(,)] all_train_lines是列向量集合
				forecast_motion = find_motion(knn, train_motion, dis_type)
				data = np.row_stack((data, forecast_motion))
			np.savetxt("dis_type=%s k=%s.csv"%(dis_type, k), data, delimiter=",")
		result = []
		if dis_type == 3:
			for i in range(len(all_test_lines)):
				knn = find_knn(all_train_lines, all_test_lines[i], 3, dis_type)
				forecast_motion = list(find_motion(knn, train_motion, dis_type))
				forecast_motion.insert(0, i+1)
				result.append(forecast_motion)
		else:
			for i in range(len(all_test_lines)):
				knn = find_knn(all_train_lines, all_test_lines[i], 4, dis_type)
				forecast_motion = list(find_motion(knn, train_motion, dis_type))
				forecast_motion.insert(0, i+1)
				result.append(forecast_motion)
		
		write_to_file(result, dis_type)




			




	



if __name__ == "__main__":
	start = time.process_time()
	print("start running...")
	main()
	time_elspsed = time.process_time() - start
	print("over")
	print("The code run %ss"%(time_elspsed))