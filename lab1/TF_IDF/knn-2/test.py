import csv
import pandas as pd
import numpy as np

def read_file(file_name):
	data = pd.read_csv(file_name)
	motion = data.values[:, 1:]
	col = data.values[:,0]
	print(col.shape)
	print(col)

	l = [1,2,3,4,5,6]
	a = np.array(l)
	print(a.shape)
	a.reshape(1,6)
	print(a/10)




read_file('train_set.csv')