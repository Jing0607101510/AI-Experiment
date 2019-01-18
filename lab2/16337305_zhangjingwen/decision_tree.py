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

id3_tree = {}
c45_tree = {}
cart_tree = {}


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
	min_gini = 1#保存最小的基尼系数
	next_attr = -1#基尼系数最小的特征的索引
	for i in range(len(data_set[0]) - 1):
		this_type = [data_set[j][i] for j in range(len(data_set))]
		split_gini = calc_split_gini(data_set, this_type, i)#计算各个特征的split基尼系数
		if split_gini < min_gini: 
			min_gini = split_gini #保存最小的split基尼系数
			next_attr = i #并记录对应的索引
	return next_attr


#计算split基尼系数
def calc_split_gini(data_set, this_type, index):
	'''
	:param data_set : 输入的数据集
	:param this_type : 特征的所有属性值
	:param index : 特征的索引
	:return : split基尼系数
	'''
	total = len(data_set)
	split_gini = 0
	for type in set(this_type):#按着计算split基尼系数的公式计算split基尼系数
		num = this_type.count(type)
		split_gini += (num / total) * calc_gini(get_new_data_set(data_set, index, type))
	return split_gini


#计算基尼系数
def calc_gini(data_set):
	'''
	:param data_set: 数据集
	:return : 基尼系数
	'''
	class_labels = [line[-1] for line in data_set]#获取所有样本的标签
	labels_number = len(class_labels)
	gini = 1
	for each_label in set(class_labels):#按照基尼系数的计算公式计算基尼系数
		this_label_num = class_labels.count(each_label)
		freq = this_label_num / labels_number
		gini -= freq ** 2
	return gini


#找出建立c4.5树下一个用于分裂的最优特征
def c45_find_next_attr(data_set):
	'''
	:param data_set : 数据集
	:return : 下一个用于划分数据集的最优特征的索引。
	'''
	data_entropy = calc_entropy(data_set)#计算熵
	max_info_gain_ratio = 0#保存当前最大的信息增益率
	line_number = len(data_set)
	next_attr = -1#保存信息增益率最大的特征对应的索引
	for i in range(len(data_set[0]) - 1):
		this_type = [data_set[j][i] for j in range(line_number)]
		conditional_entropy = calc_conditional_entropy(data_set, this_type, i)#对每一个特征，计算这个特征的条件熵，
		if calc_entropy([[item] for item in this_type]) == 0:
			return i
		#按照公式计算信息增益率
		info_gain_ratio = (data_entropy - conditional_entropy) / calc_entropy([[item] for item in this_type])
		if info_gain_ratio > max_info_gain_ratio:
			max_info_gain_ratio = info_gain_ratio#最大的信息增益率
			next_attr = i#对应的索引
	return next_attr#返回该特征的索引


#找出建立id3树下一个用于分裂的最优特征
def id3_find_next_attr(data_set):
	'''
	:param data_set : 输入的特征值
	:return : 用于分割的特征的索引
	'''
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



#建立id3决策树
def build_id3_tree(data_set, attrs, attrs_value):
	'''
	:param data_set : 输入的数据集
	:attrs : 剩下的还没用到的特征
	:attrs_value : 所有特征及其所有的属性值
	:return ： 返回节点
	'''
	class_labels = []#获取所有剩下的数据集的标签
	for data in data_set:
		class_labels.append(data[-1])
	mode = get_mode(class_labels)#获取出现最多的标签值
	if len(attrs) == 0:#如果所有特征都用了，就返回出现最多的标签值
		return mode
	elif len(set(class_labels)) == 1:#如果所有的标签的取值是一样的，则返回这个标签值
		return class_labels[0]
	else:
		next_attr = id3_find_next_attr(data_set)#找出下一个用于分裂节点的最优特征
		attr_name = attrs.pop(next_attr)
		node = {attr_name:{}}
		for type in attrs_value[attr_name]:#没有出现的属性值，置为出现最多的标签值
			node[attr_name][type] = mode
		for type in set(data_set[i][next_attr] for i in range(len(data_set))):#递归建树
			node[attr_name][type] = build_id3_tree(get_new_data_set(data_set, next_attr, type), attrs[:], attrs_value)
		return node



#建立c4.5决策树
def build_c45_tree(data_set, attrs, attrs_value):
	'''
	:param data_set : 输入的数据集
	:attrs : 剩下的还没用到的特征
	:attrs_value : 所有特征及其所有的属性值
	:return ： 返回节点
	'''
	class_labels = []#获取所有剩下的数据集的标签
	for data in data_set:
		class_labels.append(data[-1])
	mode = get_mode(class_labels)
	if len(set(class_labels)) == 1:#如果所有的标签的取值是一样的，则返回这个标签值
		return class_labels[0]
	elif len(attrs) == 0:#如果所有特征都用了，就返回出现最多的标签值
		return mode
	else:
		next_attr = c45_find_next_attr(data_set)#找出下一个用于分裂节点的最优特征
		attr_name = attrs.pop(next_attr)
		node = {attr_name:{}}
		for type in attrs_value[attr_name]:#没有出现的属性值，置为出现最多的标签值
			node[attr_name][type] = mode
		for type in set(data_set[i][next_attr] for i in range(len(data_set))):#递归建树
			node[attr_name][type] = build_c45_tree(get_new_data_set(data_set, next_attr, type), attrs[:], attrs_value)
		return node

#建立cart决策树
def build_cart_tree(data_set, attrs, attrs_value):
	'''
	:param data_set : 输入的数据集
	:attrs : 剩下的还没用到的特征
	:attrs_value : 所有特征及其所有的属性值
	:return ： 返回节点
	'''
	class_labels = []#获取所有剩下的数据集的标签
	for data in data_set:
		class_labels.append(data[-1])
	mode = get_mode(class_labels)
	if len(set(class_labels)) == 1:#如果所有的标签的取值是一样的，则返回这个标签值
		return class_labels[0]
	elif len(attrs) == 0:#如果所有特征都用了，就返回出现最多的标签值
		return mode
	else:
		next_attr = cart_find_next_attr(data_set)#找出下一个用于分裂节点的最优特征
		attr_name = attrs.pop(next_attr)
		node = {attr_name:{}}
		for type in attrs_value[attr_name]:##没有出现的属性值，置为出现最多的标签值
			node[attr_name][type] = mode
		for type in set(data_set[i][next_attr] for i in range(len(data_set))):#递归建树
			node[attr_name][type] = build_cart_tree(get_new_data_set(data_set, next_attr, type), attrs[:], attrs_value)
		return node



#获取给定的数据中，出现最多的一项
def get_mode(class_labels):
	'''
	:param class_labels : 所有的标签
	:return : 出现最多的标签
	'''
	return Counter(class_labels).most_common(1)[0][0];
	

	


#使用验证集验证所建立的树的准确性
def test_tree(tree, validation_set):
	'''
	:param tree : 所建立的决策树
	:param validation_set : 验证集
	:return : 返回正确率
	'''
	correct_num = 0 #保存正确的分类个数
	for each_data in validation_set:
		correct_num += check(tree, each_data)
	print(correct_num,"/",len(validation_set))
	return correct_num / len(validation_set)


#判断真实分类和预测分类是否相同
def check(tree, each_data):
	'''
	:param tree:所建立的决策树
	:each_data : 验证集中每一个测试样本
	:return : 如果相同返回1，否则为0
	'''
	if type(tree).__name__ == 'str':
		return 1 if tree == each_data[-1] else 0 
	else:
		feature_index = {'buying':0, 'maint':1, 'doors':2, 'persons':3, 'lug_boot':4, 'safety':5}
		root = list(tree.keys())[0] #根所代表的属性
		Dict = tree[root] #根属性所对应的子字典
		value = each_data[feature_index[root]]
		try:
			if type(Dict[value]).__name__ == 'dict':#如果还没有达到树的叶子节点，继续顺着树判断下去
				return check(Dict[value] , each_data)
			else:
				return 1 if Dict[value] == each_data[-1] else 0#到了叶子节点，判断所预测的值和真实值是否相同
		except Exception:
			return 0

#预测分类
def predict(tree, each_data):
	'''
	:param tree:所建立的决策树
	:each_data : 验证集中每一个测试样本
	:return : 如果相同返回1，否则为0
	'''
	#pl.createPlot(tree)
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




#使用10折交叉验证
def k_fold_crossValidation(data_set, attrs, choose):
	'''
	:param data_set : 数据集
	:param attrs : 特征集合
	:param choose : 建立什么树
	'''
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
	accurary = 0#平均的正确率
	k = 10
	for i in range(k):
		train_set = data_set[:i*data_piece_size]+data_set[data_piece_size*(i+1):]#将数据9份作为训练集
		validation_set = data_set[i*data_piece_size:(i+1)*data_piece_size]#一份作为验证集
		if choose == 1:#建立id3决策树
			id3_tree = build_id3_tree(train_set, attrs[:], attrs_value)
			accurary += test_tree(id3_tree, validation_set)
			predict_test_set(id3_tree)

		elif choose == 2:#建立c4.5决策树
			c45_tree =  build_c45_tree(train_set, attrs[:], attrs_value)
			accurary += test_tree(c45_tree, validation_set)
			predict_test_set(c45_tree)

		elif choose == 3:#建立cart决策树
			cart_tree =  build_cart_tree(train_set, attrs[:], attrs_value)
			accurary += test_tree(cart_tree, validation_set)
			predict_test_set(cart_tree)

	print("accurary:%s"%(accurary / k))#打印平均准确率

def predict_test_set(tree):
	result = []
	with open("Car_test.csv", "r") as file:
		reader = csv.reader(file)
		test_set = [data[:-1] for data in reader]
		for each_line in test_set:
			result.append(predict(tree, each_line))
	with open("result.csv", 'w', newline='') as rfile:
		writer = csv.writer(rfile)
		for r in result:
			writer.writerow([r])

#主函数
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