import math
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

def get_tf(data):
	tf = []
	for line in data:
		size = len(line)
		freq = {}
		for word in line:
			if word in freq:
				freq[word] += 1
			else:
				freq[word] = 1
		for key in freq.keys():
			freq[key] = freq[key] / size
		tf.append(freq)
	return tf

def get_idf(all_words, each_line_words):
	article_size = len(each_line_words)
	idf = {}
	for words in each_line_words:
		for word in set(words):
			if word in idf:
				idf[word] += 1
			else:
				idf[word] = 1
	for key in idf.keys():
		idf[key] = math.log(article_size/(idf[key]+1))
	return idf

def write_tfidf(tf, idf, all_words):
	with open("16337305_ZhangJingwen_TFIDF.txt",'w') as file:
		for i in range(len(tf)):
			keys = list(tf[i].keys())
			keys.sort(key=all_words.index)
			for key in keys:
				word_tfidf = tf[i][key] * idf[key]
				if word_tfidf != 0:
					file.write(str(word_tfidf)+' ')
			file.write('\n')

		



def main():
	[all_words, each_line_words] = parse_each_line()
	tf = get_tf(each_line_words)
	idf = get_idf(all_words, each_line_words)
	write_tfidf(tf, idf, all_words)
	

main()