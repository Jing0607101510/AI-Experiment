import csv
import time
import math
import collections

def read_file(file_name):
	all_words = []
	motion = []
	with open(file_name, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			if reader.line_num == 1:
				continue
			all_words.append(set(row[0].strip().split(' ')))
			motion.append(row[1].strip())
	return [all_words, motion]


def read_test_file(file_name):
	all_words = []
	with open(file_name, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			if reader.line_num == 1:
				continue
			all_words.append(set(row[0].strip().split(" ")))
	return all_words



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


#找出k个距离最近的训练集文本
def find_knn(all_train_lines, validation_line, k, dis_type):
	dis = []#保存验证集/测试集的距离
	for i in range(len(all_train_lines)):#计算与训练集的距离
		dis.append(calc_distance(all_train_lines[i], validation_line, dis_type))
	z = list(zip(list(range(len(all_train_lines))), dis))#将距离和下标连结
	z.sort(key = lambda y : y[1])#按照距离从小到大排序
	if dis_type == 3:#如果用的是余弦相似度，则按从大到小排序
		z.reverse()
	return z[:k] #列表，形式：[(下标，距离)，...] #返回前k个训练集文本的下标和距离


#按照k个里面lable的众数，找出验证集/测试集的label
def find_motion(knn, motion, dis_type):
	motion_number = {}
	min_dis = {}
	#用的是余弦相似度求的距离
	if dis_type == 3:
		for item in knn:#计算每一种label出现的次数，并记录该label对应的训练集文本与其最小的距离
			if motion[item[0]] in motion_number:
				motion_number[motion[item[0]]] += 1
				if min_dis[motion[item[0]]] < item[1]:#记录该label对应的训练集文本与其最小的距离
					min_dis[motion[item[0]]] = item[1]
			else:
				motion_number[motion[item[0]]] = 1
				min_dis[motion[item[0]]] = item[1]

		num = 0
		min_d = -1000000000
		for key, value in motion_number.items():
			#找出出现次数最多的label
			if value > num:
				num = value
				min_d = min_dis[key]
				target = key
			#如果出现的label一样多的时候，取距离最小的（即余弦相似度最大的）
			elif value == num:
				if min_d < min_dis[key]:
					min_d = min_dis[key]
					target = key
		return target

	else:
		#用的街区距离或者欧式距离求的距离
		for item in knn:#计算每一种label出现的次数，并记录该label对应的训练集文本与其最小的距离
			if motion[item[0]] in motion_number:
				motion_number[motion[item[0]]] += 1
				if min_dis[motion[item[0]]] > item[1]:#记录该label对应的训练集文本与其最小的距离
					min_dis[motion[item[0]]] = item[1]
			else:
				motion_number[motion[item[0]]] = 1
				min_dis[motion[item[0]]] = item[1]

		num = 0
		min_d = 1000000000
		for key, value in motion_number.items():
			#找出出现次数最多的label
			if value > num:
				num = value
				target = key
				min_d = min_dis[key]
			#如果出现的label一样多的时候，取距离最小的
			elif value == num:
				if min_d > min_dis[key]:
					min_d = min_dis[key]
					target = key
		return target






def write_to_file(result, distype):
	with open("16337305_Zhangjingwen_KNN_classification(%s).csv"%(distype), "w", newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['textid', 'label'])
		for r in result:
			writer.writerow(r)



def main():
	train_file_name = "train_set.csv"
	validation_file_name = "validation_set.csv"
	test_file_name = "test_set.csv"
	[all_train_lines,train_motion] = read_file(train_file_name)
	[all_validation_lines, validation_motion] = read_file(validation_file_name)
	all_test_lines = read_test_file(test_file_name)

	
	#固定一种求距离的方法
	for dis_type in range(1, 4):
		validation_size = len(validation_motion)
		max = 0
		max_k = 0
		for k in range(1, 20):#对每一个K值，计算与验证集的准确率
			a = 0
			for i in range(validation_size):
				knn = find_knn(all_train_lines, all_validation_lines[i], k, dis_type)
				forecast_motion = find_motion(knn, train_motion, dis_type)
				if forecast_motion == validation_motion[i]:
					a += 1
			accuracy = a/validation_size
			if max < accuracy:
				max = accuracy
				max_k = k
			print('dis_type=%d k=%d accuracy=%f'%(dis_type, k, accuracy))

		print("The Max Accuracy is %s, the K is %s"%(max, max_k))
		result = []
		#将给定距离公式，求出能够使验证集准确率最高的K值，运用于测试集中
		print("Apply this K=%s to the test set"%(max_k))
		for i in range(len(all_test_lines)):
			knn = find_knn(all_train_lines, all_test_lines[i], max_k, dis_type)
			test_motion = find_motion(knn, train_motion, dis_type)
			result.append([i+1, test_motion])
		write_to_file(result, dis_type)






	



if __name__ == "__main__":
	start = time.process_time()
	main()
	time_elspsed = time.process_time() - start
	print("The code run %ss"%(time_elspsed))