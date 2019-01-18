import math
import time
def parse_each_line():
	all = []
	each_line_words = []
	with open("semeval.txt", "r") as data:
		for each_line in data:
			each_line = each_line.strip('\n')
			words = each_line.split('\t')[2].split(' ')
			each_line_words.append(words)
			all.extend(words)
	all_words = list(set(all))
	all_words.sort(key=all.index)
	return [all_words, each_line_words]

#计算每一行文本出现的单词在该行中的频率
def get_tf(data):
	'''
	data:储存每一行词汇的二维列表
	'''
	tf = []
	for line in data:
		size = len(line)
		freq = {} #保存每一行中，各个单词出现的次数
		for word in line:
			if word in freq:
				freq[word] += 1
			else:
				freq[word] = 1
		for key in freq.keys(): #计算每一行中单词出现的频率
			freq[key] = freq[key] / size
		tf.append(freq)
	return tf #返回所有行中单词出现的频率

#计算每一个不同的单词的反向文件频率
def get_idf(all_words, each_line_words):
	'''
	all_words : 一维列表，保存了所有文本中出现过的词汇，不重复
	each_line_words:二维列表，保存了文本中每一行词汇的二维列表
	'''
	article_size = len(each_line_words) #得到文本的行数
	idf = {}#保存每一个单词出现的行数的字典
	#统计每一个词汇出现的行的数量
	for words in each_line_words:
		for word in set(words):#用set（）不重复计算在同一行里出现的单词
			if word in idf:
				idf[word] += 1
			else:
				idf[word] = 1
	#计算每一个词汇的TF-IDF值
	for key in idf.keys():
		idf[key] = math.log(article_size/(idf[key]+1))
	return idf

#计算tf-idf并且写入文件之中
def write_tfidf(tf, idf, all_words):
	with open("16337305_ZhangJingwen_TFIDF.txt",'w') as file:
		for i in range(len(tf)):#计算每一行单词的tf-idf
			keys = list(tf[i].keys())
			keys.sort(key=all_words.index)#按照出现的顺序排序
			for key in keys:#计算每一个单词的tf-idf
				word_tfidf = tf[i][key] * idf[key]
				if word_tfidf != 0:#非0值写入文件
					file.write(str(word_tfidf)+' ')
			file.write('\n')

		



def main():

	[all_words, each_line_words] = parse_each_line()
	tf = get_tf(each_line_words)
	idf = get_idf(all_words, each_line_words)
	write_tfidf(tf, idf, all_words)

if __name__ == '__main__':	
	start = time.process_time()
	main()
	time_elspsed = time.process_time() - start
	print("The code run " + str(time_elspsed)+"s")