'''
需要保存label类型，作为节点的值，在向下传递的时候，去掉已经用过的特征属性，用一个列表来存储
递归终止条件：
1.剩下的都属于同一类，
2.保存label的列表为空，即已经将所有特征都用上了，也就是D中所有样本在A中特征都是一样的（取众数）
递归建树
发现问题：
1.在选取属性的时候，是在其他已选定的属于该属性的数据集里面计算熵 是的
2.还可以调参？
3.怎么测试准确率？K折交叉验证？
4.python的树

'''
import time
import csv
from collections import Counter
import math
import pl
from random import randrange
import random

def read_file(file_name):
	with open(file_name, "r") as file:
		reader = csv.reader(file)
		return list(reader)


def calc_entropy(data_set):
	class_labels = [line[-1] for line in data_set]
	labels_number = len(class_labels)
	entropy = 0
	for each_label in set(class_labels):
		this_label_num = class_labels.count(each_label)
		freq = this_label_num / labels_number
		entropy += - freq * math.log2(freq)
	return entropy


def get_new_data_set(data_set, index, value):
	new_data_set = []
	for data in data_set:
		if data[index] == value:
			new_data_set.append(data[:index] + data[index+1:])
	return new_data_set


def calc_conditional_entropy(data_set, this_type, index):
	total = len(data_set)
	conditional_entropy = 0
	for type in set(this_type):
		num = this_type.count(type)
		conditional_entropy += (num / total) * calc_entropy(get_new_data_set(data_set, index, type))
	return conditional_entropy


def cart_find_next_attr(data_set, k):
	min_gini = 1
	next_attr = -1

	feat_index = []
	for i in range(k):
		idx = randrange(len(data_set[0])-1)
		feat_index.append(idx)

	feat_index = set(feat_index)

	for i in feat_index:
		this_type = [data_set[j][i] for j in range(len(data_set))]
		split_gini = calc_split_gini(data_set, this_type, i)
		if split_gini < min_gini:
			min_gini = split_gini
			next_attr = i
	return next_attr

def calc_split_gini(data_set, this_type, index):
	total = len(data_set)
	split_gini = 0
	for type in set(this_type):
		num = this_type.count(type)
		split_gini += (num / total) * calc_gini(get_new_data_set(data_set, index, type))
	return split_gini


def calc_gini(data_set):
	class_labels = [line[-1] for line in data_set]
	labels_number = len(class_labels)
	gini = 1
	for each_label in set(class_labels):
		this_label_num = class_labels.count(each_label)
		freq = this_label_num / labels_number
		gini -= freq ** 2
	return gini


def c45_find_next_attr(data_set, k):
	data_entropy = calc_entropy(data_set)
	max_info_gain_ratio = 0
	line_number = len(data_set)
	next_attr = -1

	feat_index = []
	for i in range(k):
		idx = randrange(len(data_set[0])-1)
		feat_index.append(idx)

	feat_index = set(feat_index)

	for i in feat_index:
		this_type = [data_set[j][i] for j in range(line_number)]
		conditional_entropy = calc_conditional_entropy(data_set, this_type, i)
		if calc_entropy([[item] for item in this_type]) == 0:
			return i
		else:
			info_gain_ratio = (data_entropy - conditional_entropy) / calc_entropy([[item] for item in this_type])
			if info_gain_ratio > max_info_gain_ratio:
				max_info_gain_ratio = info_gain_ratio
				next_attr = i
	return next_attr


def id3_find_next_attr(data_set, k):
	data_entropy = calc_entropy(data_set)
	max_information_gain = 0
	line_number = len(data_set)
	next_attr = -1

	feat_index = []
	for i in range(k):
		idx = randrange(len(data_set[0])-1)
		feat_index.append(idx)

	feat_index = set(feat_index)


	for i in feat_index: #对每一个属性计算其条件熵
		this_type = [data_set[j][i] for j in range(line_number)]
		this_type_entropy = calc_conditional_entropy(data_set, this_type, i)#i：指明需要计算的某个属性的条件熵，set（this_type）指某个属性的不同取值 #条件熵
		#for type in set(this_type):#对该属性的不同取值
		#	num = this_type.count(type)#该属性的一个取值的数量
		#	this_type_entropy += (num / line_number) * calc_entropy(get_new_data_set(data_set, i, type))
		if data_entropy - this_type_entropy > max_information_gain:
			max_information_gain = data_entropy - this_type_entropy
			next_attr = i

	return next_attr#只是一个索引




def build_id3_tree(data_set, attrs, attrs_value, k):
	class_labels = []
	for data in data_set:
		class_labels.append(data[-1])
	mode = get_mode(class_labels)
	if len(attrs) == 0:
		return mode
	elif len(set(class_labels)) == 1:
		return class_labels[0]
	else:
		next_attr = id3_find_next_attr(data_set, k)
		attr_name = attrs.pop(next_attr)
		node = {attr_name:{}}
		for type in attrs_value[attr_name]:##################
			node[attr_name][type] = mode
		for type in set(data_set[i][next_attr] for i in range(len(data_set))):
			node[attr_name][type] = build_id3_tree(get_new_data_set(data_set, next_attr, type), attrs[:], attrs_value, k)
		return node




def build_c45_tree(data_set, attrs, attrs_value, k):
	class_labels = []
	for data in data_set:
		class_labels.append(data[-1])
	mode = get_mode(class_labels)
	if len(set(class_labels)) == 1:
		return class_labels[0]
	elif len(attrs) == 0:
		return mode
	else:
		next_attr = c45_find_next_attr(data_set, k)
		attr_name = attrs.pop(next_attr)
		node = {attr_name:{}}
		for type in attrs_value[attr_name]:##################
			node[attr_name][type] = mode
		for type in set(data_set[i][next_attr] for i in range(len(data_set))):
			node[attr_name][type] = build_c45_tree(get_new_data_set(data_set, next_attr, type), attrs[:], attrs_value, k)
		return node


def build_cart_tree(data_set, attrs, attrs_value, k):
	class_labels = []
	for data in data_set:
		class_labels.append(data[-1])
	mode = get_mode(class_labels)
	if len(set(class_labels)) == 1:
		return class_labels[0]
	elif len(attrs) == 0:
		return mode
	else:
		next_attr = cart_find_next_attr(data_set, k)
		attr_name = attrs.pop(next_attr)
		node = {attr_name:{}}
		for type in attrs_value[attr_name]:##################
			node[attr_name][type] = mode
		for type in set(data_set[i][next_attr] for i in range(len(data_set))):
			node[attr_name][type] = build_cart_tree(get_new_data_set(data_set, next_attr, type), attrs[:], attrs_value, k)
		return node




def get_mode(class_labels):
	return Counter(class_labels).most_common(1)[0][0];
	

#def test_tree(tree, validation_set):
#	correct_num = 0
#	for each_data in validation_set:
#		correct_num += check(tree, each_data)
#	return correct_num / len(validation_set)


def check(tree, each_data):
	if type(tree).__name__ == 'str':
		return tree 
	else:
		feature_index = {'buying':0, 'maint':1, 'doors':2, 'persons':3, 'lug_boot':4, 'safety':5}
		root = list(tree.keys())[0] #根所代表的属性
		Dict = tree[root] #根属性所对应的子字典
		value = each_data[feature_index[root]]

		if type(Dict[value]).__name__ == 'dict':
			return check(Dict[value] , each_data)
		else:
			return Dict[value]



def test_forest(forest, validation_set):
	correct_num = 0
	for each_data in validation_set:
		predict = []
		for tree in forest:
			predict.append(check(tree, each_data))
		if each_data[-1] == get_mode(predict):
			correct_num += 1
	#print("correct:", correct_num)
	#print("validation_set_size", len(validation_set))
	print(correct_num, "/", len(validation_set))
	return correct_num / len(validation_set)
			
#预测分类
def predict(tree, each_data):
	'''
	:param tree:所建立的决策树
	:each_data : 验证集中每一个测试样本
	:return : 如果相同返回1，否则为0
	'''
	if type(tree).__name__ == 'str':
		return tree
	else:
		feature_index = {'buying':0, 'maint':1, 'doors':2, 'persons':3, 'lug_boot':4, 'safety':5}
		root = list(tree.keys())[0] #根所代表的属性
		Dict = tree[root] #根属性所对应的子字典
		value = each_data[feature_index[root]]

		if type(Dict[value]).__name__ == 'dict':#如果还没有达到树的叶子节点，继续顺着树判断下去
			return predict(Dict[value] , each_data)
		else:
			return Dict[value]#到了叶子节点
		
def predict_test_set(forest):
	result = []
	with open("Car_test.csv", "r") as file:
		reader = csv.reader(file)
		test_set = [data[:-1] for data in reader]
		for each_line in test_set:
			p = []
			for tree in forest:
				p.append(predict(tree, each_line))
			result.append(get_mode(p))
	with open("result.csv", 'w', newline='') as rfile:
		writer = csv.writer(rfile)
		for r in result:
			writer.writerow([r])


#建立决策树是id3决策树的随机森林
def build_id3_forest(train_set, attrs, attrs_value, k, t):
	'''
	:param train_set : 训练集
	:param attrs : 所有的特征
	:param attrs_value : 特征及其对应的取值
	:param t : 森林中树的棵树
	:param k : 随机选取的特征数
	:return : 森林
	'''
	trees = []
	for i in range(t):
		sub_set = []
		for i in range(len(train_set)):#又放回地选取和测试集一样大的样本集用作真正训练集
			idx = random.randrange(len(train_set))
			sub_set.append(train_set[idx])
		id3_tree = build_id3_tree(sub_set, attrs[:], attrs_value, k)#建立决策树
		trees.append(id3_tree)
	return trees


def build_c45_forest(train_set, attrs, attrs_value, k, t):
	trees = []
	for i in range(t):
		sub_set = []
		for i in range(len(train_set)):
			idx = random.randrange(len(train_set))
			sub_set.append(train_set[idx])
		c45_tree = build_c45_tree(sub_set, attrs[:], attrs_value, k)
		trees.append(c45_tree)
	return trees


def build_cart_forest(train_set, attrs, attrs_value, k, t):
	trees = []
	for i in range(t):
		sub_set = []
		for i in range(len(train_set)):
			idx = random.randrange(len(train_set))
			sub_set.append(train_set[idx])
		cart_tree = build_cart_tree(sub_set, attrs[:], attrs_value, k)
		trees.append(cart_tree)
	return trees
	




def k_fold_crossValidation(data_set, attrs, choose):
	attrs_value = {
	'buying' : ['vhigh', 'high', 'med', 'low'],
	'maint' : ['vhigh', 'high', 'med', 'low'],
	'doors' : ['2', '3', '4', '5more'],
	'persons' : ['2', '4', 'more'],
	'lug_boot' :    ['small', 'med', 'big'],
	'safety' :      ['low', 'med', 'high']
	}
	data_len = len(data_set)
	data_piece_size = math.ceil(data_len / 10)
	accurary = 0
	n = 10
	t = int(input("please input the number of trees in the forest:\n"))
	k = int(input("please input the feature number when build the tree:\n"))
	for i in range(n):
		train_set = data_set[:i*data_piece_size]+data_set[data_piece_size*(i+1):]
		validation_set = data_set[i*data_piece_size:(i+1)*data_piece_size]
		if choose == 1:
			id3_forest = build_id3_forest(train_set, attrs[:], attrs_value, k, t)
			accurary += test_forest(id3_forest, validation_set)
			predict_test_set(id3_forest)

		elif choose == 2:
			c45_forest =  build_c45_forest(train_set, attrs[:], attrs_value, k, t)
			accurary += test_forest(c45_forest, validation_set)
			predict_test_set(c45_forest)
		elif choose == 3:
			cart_forest =  build_cart_forest(train_set, attrs[:], attrs_value, k, t)
			accurary += test_forest(cart_forest, validation_set)
			predict_test_set(cart_forest)
	print("accurary:%s"%(accurary / n))


def main():
	attrs = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
	train_file_name = "Car_train.csv"
	data_set = read_file(train_file_name)

	choose = input("please choose the kind of Decison Tree:\n1.id3_tree\n2.c45_tree\n3.cart_tree\n")
	choose = int(choose)

	while 0<choose<4:
		k_fold_crossValidation(data_set, attrs, choose)
		choose = int(input("please choose the kind of Decison Tree:\n1.id3_tree\n2.c45_tree\n3.cart_tree\n"))
	#pl.createPlot(cart_tree)
	



if __name__ == "__main__":
	start = time.process_time()
	main()
	end = time.process_time()
	print("The program is over after %ss"%(end - start))