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
	knn_index = []#保存
	dis = []#保存验证集/测试集的距离
	for i in range(len(all_train_lines)):
		dis.append(calc_distance(all_train_lines[i], validation_line, dis_type))
	z = list(zip(list(range(len(all_train_lines))), dis))
	z.sort(key = lambda y : y[1])
	if dis_type == 3:
		z.reverse()
	for item in z[:k]:
		knn_index.append(item[0])
	return knn_index



def find_motion(knn, motion):
	return collections.Counter([motion[i] for i in knn]).most_common(1)[0][0]

def write_to_file(result, distype):
	with open("16337305_Zhangjingwen_KNN_classification(%s)1.csv"%(distype), "w", newline='') as file:
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

	
	for dis_type in range(1, 4):
		validation_size = len(validation_motion)
		max = 0
		max_k = 0
		for k in range(1, 20):
			a = 0
			for i in range(validation_size):
				knn = find_knn(all_train_lines, all_validation_lines[i], k, dis_type)
				forecast_motion = find_motion(knn, train_motion)
				if forecast_motion == validation_motion[i]:
					a += 1
			accuracy = a/validation_size
			if max < accuracy:
				max = accuracy
				max_k = k
			print('dis_type=%d k=%d accuracy=%f'%(dis_type, k, accuracy))

		print("The Max Accuracy is %s, the K is %s"%(max, max_k))
		result = []
		for i in range(len(all_test_lines)):
			knn = find_knn(all_train_lines, all_test_lines[i], max_k, dis_type)
			test_motion = find_motion(knn, train_motion)
			result.append([i+1, test_motion])
			write_to_file(result, dis_type)






	



if __name__ == "__main__":
	start = time.process_time()
	main()
	time_elspsed = time.process_time() - start
	print("The code run %ss"%(time_elspsed))