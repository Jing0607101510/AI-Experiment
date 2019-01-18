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
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib as mpl

#读取文件，转化为列表形式
def read_file(file_name):
	'''
	:file_name:需要读取的文件
	:return :保存数据的列表
	'''
	with open(file_name, "r") as file:
		reader = csv.reader(file)
		return list(reader)


#计算熵的大小
def calc_entropy(data_set):
	'''
		:param data_set:需要计算熵的数据集
		:return :熵的大小
	'''
	class_labels = [line[-1] for line in data_set] #得到每一个样本的标签
	labels_number = len(class_labels) #获取样本的个数
	entropy = 0
	for each_label in set(class_labels):#计算熵，通过熵的公式
		this_label_num = class_labels.count(each_label)
		freq = this_label_num / labels_number
		entropy += - freq * math.log2(freq)
	return entropy #返回需要计算的熵的大小


#分裂根据特征及其属性的值划分数据集，得到这一特征为给定属性的数据集的子集
def get_new_data_set(data_set, index, value):
	'''
	:param data_set : 输入的需要划分的数据集
	:param index : 特征在列表中的索引位置
	:param value ；指定的特征的属性值
	:return : 所需的新的数据集
	'''
	new_data_set = []
	for data in data_set:
		if data[index] == value: #如果该样本的特征的值与给定的值相同，则加入新的列表中
			new_data_set.append(data[:index] + data[index+1:])
	return new_data_set


#计算条件熵
def calc_conditional_entropy(data_set, this_type, index):
	'''
	:param data_set : 需要计算条件熵的数据集
	:param this_type : 是需要什么计算的特征的在所有数据集中的所有属性值
	:param index : 选定的特征的索引
	:return : 返回条件熵
	'''
	total = len(data_set)#样本的大小
	conditional_entropy = 0#条件熵
	for type in set(this_type):#计算条件熵
		num = this_type.count(type)
		conditional_entropy += (num / total) * calc_entropy(get_new_data_set(data_set, index, type))
	return conditional_entropy#返回条件熵


#找出建立cart树下一个用于分裂的最优特征
def cart_find_next_attr(data_set):
	'''
	:param data_set : 数据集
	:return : 下一个用于划分数据集的最优特征的索引。
	'''
	min_gini = 1
	next_attr = -1
	for i in range(len(data_set[0]) - 1):
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


def c45_find_next_attr(data_set):
	data_entropy = calc_entropy(data_set)
	max_info_gain_ratio = 0
	line_number = len(data_set)
	next_attr = -1
	for i in range(len(data_set[0]) - 1):
		this_type = [data_set[j][i] for j in range(line_number)]
		conditional_entropy = calc_conditional_entropy(data_set, this_type, i)
		if calc_entropy([[item] for item in this_type]) == 0:
			return i
		info_gain_ratio = (data_entropy - conditional_entropy) / calc_entropy([[item] for item in this_type])
		if info_gain_ratio > max_info_gain_ratio:
			max_info_gain_ratio = info_gain_ratio
			next_attr = i
	return next_attr


def id3_find_next_attr(data_set):
	data_entropy = calc_entropy(data_set)
	max_information_gain = 0
	line_number = len(data_set)
	next_attr = -1
	for i in range(len(data_set[0]) - 1): #对每一个属性计算其条件熵
		this_type = [data_set[j][i] for j in range(line_number)]
		this_type_entropy = calc_conditional_entropy(data_set, this_type, i)#i：指明需要计算的某个属性的条件熵，set（this_type）指某个属性的不同取值 #条件熵
		#for type in set(this_type):#对该属性的不同取值
		#	num = this_type.count(type)#该属性的一个取值的数量
		#	this_type_entropy += (num / line_number) * calc_entropy(get_new_data_set(data_set, i, type))
		if data_entropy - this_type_entropy > max_information_gain:
			max_information_gain = data_entropy - this_type_entropy
			next_attr = i
	return next_attr#只是一个索引




def build_id3_tree(data_set, attrs, attrs_value):
	class_labels = []
	for data in data_set:
		class_labels.append(data[-1])
	mode = get_mode(class_labels)
	if len(attrs) == 0:
		return mode
	elif len(set(class_labels)) == 1:
		return class_labels[0]
	else:
		next_attr = id3_find_next_attr(data_set)
		attr_name = attrs.pop(next_attr)
		node = {attr_name:{}}
		for type in attrs_value[attr_name]:##################
			node[attr_name][type] = mode
		for type in set(data_set[i][next_attr] for i in range(len(data_set))):
			node[attr_name][type] = build_id3_tree(get_new_data_set(data_set, next_attr, type), attrs[:], attrs_value)
		return node




def build_c45_tree(data_set, attrs, attrs_value):
	class_labels = []
	for data in data_set:
		class_labels.append(data[-1])
	mode = get_mode(class_labels)
	if len(set(class_labels)) == 1:
		return class_labels[0]
	elif len(attrs) == 0:
		return mode
	else:
		next_attr = c45_find_next_attr(data_set)
		attr_name = attrs.pop(next_attr)
		node = {attr_name:{}}
		for type in attrs_value[attr_name]:##################
			node[attr_name][type] = mode
		for type in set(data_set[i][next_attr] for i in range(len(data_set))):
			node[attr_name][type] = build_c45_tree(get_new_data_set(data_set, next_attr, type), attrs[:], attrs_value)
		return node


def build_cart_tree(data_set, attrs, attrs_value):
	class_labels = []
	for data in data_set:
		class_labels.append(data[-1])
	mode = get_mode(class_labels)
	if len(set(class_labels)) == 1:
		return class_labels[0]
	elif len(attrs) == 0:
		return mode
	else:
		next_attr = cart_find_next_attr(data_set)
		attr_name = attrs.pop(next_attr)
		node = {attr_name:{}}
		for type in attrs_value[attr_name]:##################
			node[attr_name][type] = mode
		for type in set(data_set[i][next_attr] for i in range(len(data_set))):
			node[attr_name][type] = build_cart_tree(get_new_data_set(data_set, next_attr, type), attrs[:], attrs_value)
		return node




def get_mode(class_labels):
	return Counter(class_labels).most_common(1)[0][0];
	

	



def test_tree(tree, validation_set):
	correct_num = 0
	for each_data in validation_set:
		correct_num += check(tree, each_data)
	return correct_num / len(validation_set)


def check(tree, each_data):
	feature_index = {'buying':0, 'maint':1, 'doors':2, 'persons':3, 'lug_boot':4, 'safety':5}
	root = list(tree.keys())[0] #根所代表的属性
	Dict = tree[root] #根属性所对应的子字典
	value = each_data[feature_index[root]]
	try:
		if type(Dict[value]).__name__ == 'dict':
			return check(Dict[value] , each_data)
		else:
			return 1 if Dict[value] == each_data[-1] else 0
	except Exception:
		return 0




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
	accurary = []
	k = 10
	for i in range(k):
		train_set = data_set[:i*data_piece_size]+data_set[data_piece_size*(i+1):]
		validation_set = data_set[i*data_piece_size:(i+1)*data_piece_size]
		if choose == 1:
			id3_tree = build_id3_tree(train_set, attrs[:], attrs_value)
			accurary.append(test_tree(id3_tree, validation_set))

		elif choose == 2:
			c45_tree =  build_c45_tree(train_set, attrs[:], attrs_value)
			accurary.append(test_tree(c45_tree, validation_set))

		elif choose == 3:
			cart_tree =  build_cart_tree(train_set, attrs[:], attrs_value)
			accurary.append(test_tree(cart_tree, validation_set))

	#print("accurary:%s"%(accurary / k))
	print("accurary:%s"%(accurary), 'average accurary:', sum(accurary) / 10)
	return accurary

def draw_figure(y):
	#mpl.rcParams['font.size'] = 10
	figure = plt.figure()
	ax = figure.add_subplot(111, projection='3d')
	k = 0
	for c, z in zip(['r', 'g', 'b'], [1, 2, 3]):
	    xs = np.arange(1, 11)
	    ys = y[k]
	 
	    # You can provide either a single color or an array. To demonstrate this,
	    # the first bar of each set will be colored cyan.
	    cs = [c] * len(xs)
	    ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8)
	    k += 1
	

	ax.set_xlabel('k th')
	ax.set_ylabel('kind of decision tree, the 1 is id3, 2 is c4.5, 3 is cart')
	ax.set_zlabel('accurary')
	 
	plt.show()




def main():
	attrs = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
	train_file_name = "Car_train.csv"
	data_set = read_file(train_file_name)

	choose = input("please choose the kind of Decison Tree:\n1.id3_tree\n2.c45_tree\n3.cart_tree\n")
	choose = int(choose)

	accurary = []
	while 0<choose<4:
		accurary.append(k_fold_crossValidation(data_set, attrs, choose))
		choose = int(input("please choose the kind of Decison Tree:\n1.id3_tree\n2.c45_tree\n3.cart_tree\n"))
	#pl.createPlot(cart_tree)
	

	draw_figure(accurary)
	



if __name__ == "__main__":
	start = time.process_time()
	main()
	end = time.process_time()
	print("The program is over after %ss"%(end - start))