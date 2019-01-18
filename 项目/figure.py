import matplotlib.pyplot as plt
import matplotlib
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from mpl_toolkits.mplot3d import Axes3D
import random
def figure():
    accuracies = [[78.2833333333333,80.75,80.9833333333333,80.7,80.6166666666666],[78.2833333333333, 80.75, 80.9833333333333,80.7,80.6166666666666]]
    print(sum(accuracies[0])/5, sum(accuracies[1])/5)
    plt.rcParams['font.size'] = 10
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = []
    for z in range(2):
        x = range(1, 6)
        y = accuracies[z]
        color = plt.cm.Set2(random.choice(range(plt.cm.Set2.N)))
        while color in colors:
            color = plt.cm.Set2(random.choice(range(plt.cm.Set2.N)))
        colors.append(color)
        ax.bar(x, y, z, zdir='y', color=color, alpha=0.8)#y才是需要表现的数值 #x和z是平面的坐标
    ax.set_xlabel('最大迭代次数')
    ax.set_ylabel('学习率选择')
    ax.set_zlabel('正确率')
    plt.xticks(range(6), range(0, 300, 50))
    plt.yticks(range(2), ["step:0.5", "step:1"])
    plt.show()


def figure_bar_solo():  
	X = np.arange(800, 2000, 100)
	Y = [65.1251
,65.6263
,65.6768
,65.6684
,65.7273
,65.6336
,65.81255
,65.79530187
,65.78497621
,65.78288811
,65.78638996
,65.83626713
]  

	fig = plt.figure()  
	plt.bar(X, Y, 40, color="#0FF0F0")  

	plt.title("NN回归 ")
	#使用text显示数值  
	for a,b in zip(X,Y):  
		plt.text(a, b+0.05, '%.5f' % b, ha='center', va= 'bottom',fontsize=10)  	
	plt.ylim(64,66)    #设置Y轴上下限
	plt.xlabel("最大迭代次数")
	plt.ylabel("相关系数")
	plt.show()

def figure_bar():  
	X = np.arange(100, 1600, 100) -20
	XX = X+40
	Y = [64.6287
,65.436
,65.4332
,65.5348
,65.6054
,65.5394
,65.6139
,65.61921
,65.6566
,65.6558
,65.68692025
,65.66405226
,65.69722786
,65.71073225
,65.6911551
]  
	YY=[
65.3598
,65.5026
,65.5189
,65.5645
,65.6212
,65.62912286
,65.6355896
,65.63174668
,65.63066364
,65.6342294
,65.63712004
,65.62855513
,65.63616275
,65.63645729
,65.63853168
]  
	fig = plt.figure()  
	plt.bar(X, Y, 40, color="#0FF0F0")  
	plt.bar(XX,YY,40, color="yellow")  #使用不同颜色  
	plt.title("NN回归 ")
	#使用text显示数值  
	for a,b in zip(X,Y):  
		plt.text(a, b+0.05, '%.5f' % b, ha='center', va= 'bottom',fontsize=10)  
	for a,b in zip(XX,YY):  
		plt.text(a, b+0.05, '%.5f' % b, ha='center', va= 'bottom',fontsize=10)    
	plt.ylim(64.5,65.75)    #设置Y轴上下限  
	

	plt.xlabel("最大迭代次数")
	plt.ylabel("相关系数")
	plt.show()
figure_bar()
'''from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = Axes3D(fig)

x = [0,1,2,3,4,5,6]
for i in x:
	y = [0,1,2,3,4,5,6,7,8,9]
	z = abs(np.random.normal(1,10,10))
	ax.bar(y,z,i,zdir="y", color='g')
plt.show()
'''
'''
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for c, z in zip(['r', 'g', 'b', 'y'], [30, 20, 10, 0]):
    xs = np.arange(20)
    ys = np.random.rand(20)
 
    # You can provide either a single color or an array. To demonstrate this,
    # the first bar of each set will be colored cyan.
    cs = [c] * len(xs)
    cs[0] = 'c'
    ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8)
 
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
 
plt.show()
'''