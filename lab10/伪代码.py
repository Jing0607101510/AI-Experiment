
node_can_visited = []
选择第一个节点作为合并的初始节点
将这个节点的cpt涉及到的变量加入到node_can_visited中

for 剩下的还没被访问的节点：
    if 这个节点的名字在node_can_visited中：
        将这个节点的cpt和初始的cpt合并
        将这个节点的cpt涉及到的变量加入到node_can_visited中

最后得到的cpt就是联合概率表


variable:需要约束的变量
value：需要约束的变量的取值
new_var_list = 原来的var_list中去掉variable之后形成的列表
new_cpt = 选取原来的cpt中varible的值为value的项组成的新的cpt

varible:需要sumout的变量名
new_var_list = 与拿来的var_list中去掉variable之后形成的新的列表
new_cpt = {}
for cpt中的每一项i：
    if 这一项没有被标记过：
        for 这一项后面的其他项j：
            if i项和j项除了variable的取值不同，其他的变量取值相同：
                将i项和j项标记
                将它们的概率相加，加入到new_cpt中


df1 = 将cpt转化为DataFrame
df2 = 另一个节点的cpt转化为DataFrame格式
df3 = pd.merge(df1, df2)
df3['probability'] = df1['probility1'] * df2['probability2']
new_list = 两个节点的var_list的合并
new_cpt = {df3中各个变量对应的取值合并成的字符串 ： df3中的'probility'}

def restrict(self, variable, value):
    index = self.var_list.index(variable)
    new_var_list = [var for var in self.var_list if var != variable]
    new_cpt = {key[:index]+key[index+1:] : v for key, v in self.cpt.items() if key[index] == str(value)}
    new_node = Node('f' + str(new_var_list), new_var_list)
    new_node.set_cpt(new_cpt)
    return new_node

index = self.var_list.index(variable)
new_var_list = [var for var in self.var_list if var != variable]
new_cpt = {}
flag = [0] * len(self.cpt)
for i in range(len(self.cpt)):
    if flag[i] == 0:
        for j in range(i+1, len(self.cpt)):
            if (int(list(self.cpt.keys())[i],2)^int(list(self.cpt.keys())[j],2)) - (1<<(len(self.var_list)-index-1)) == 0:
                flag[j] = 1
                flag[i] = 1
                new_cpt[list(self.cpt.keys())[i][:index]+list(self.cpt.keys())[i][index+1:]] = self.cpt[list(self.cpt.keys())[i]]+self.cpt[list(self.cpt.keys())[j]]
                break

df3 = pd.merge(df1, df2)
df3['Probability'] = df3['Probability2'] * df3['Probability1']
collection = self.var_list + factor.var_list
new_list = set(collection)
new_list = sorted(list(new_list), key=collection.index)

new_cpt = {}
for _, row in df3.iterrows():
    new_cpt[''.join([row[c] for c in new_list])] = row['Probability']

    def inference(factor_list, query_variables,
                  ordered_list_of_hidden_variables, evidence_list):
        for ev in evidence_list:
            new_factor_list = []
            for factor in factor_list:
                if ev not in factor.var_list:
                    new_factor_list.append(factor)
                else:
                    new_factor = factor.restrict(ev, evidence_list[ev])
                    if len(new_factor.var_list):
                        new_factor_list.append(new_factor)
            factor_list = new_factor_list
        
        # for factor in factor_list:
        #     print(factor.name, factor.var_list, factor.cpt)

        #变量消除
        for var in ordered_list_of_hidden_variables:#含有var的因子相乘后再sumout#将factor_list中的因子按照var的顺序进行消除
            new_factor_list = []
            flag = 0
            for i in range(len(factor_list)):
                if var in factor_list[i].var_list and flag == 0:
                    first_factor = factor_list[i]
                    flag = 1
                elif var in factor_list[i].var_list and flag == 1:
                    first_factor = first_factor.multiply(factor_list[i])
                else:
                    new_factor_list.append(factor_list[i])
            if flag:
                new_factor = first_factor.sum_out(var)
                if len(new_factor.var_list):
                    new_factor_list.append(new_factor)
            factor_list = new_factor_list


        factor_list.sort(key=lambda factor:factor.var_list)
    
        print("RESULT: ")
        res = factor_list[0];
        for factor in factor_list[1:]:
            res = res.multiply(factor)#factor是一个Node对象
        total = sum(res.cpt.values())
        res.cpt = {k: v / total for k, v in res.cpt.items()}
        res.print_inf()

for ev in evidence_list:
    new_factor_list = []
     for factor in factor_list:
        if ev not in factor.var_list:
            new_factor_list.append(factor)
        else:
            new_factor = factor.restrict(ev, evidence_list[ev])
            if len(new_factor.var_list):
                new_factor_list.append(new_factor)
    factor_list = new_factor_list


for var in ordered_list_of_hidden_variables:
    new_factor_list = []
    flag = 0
    for i in range(len(factor_list)):
        if var in factor_list[i].var_list and flag == 0:
            first_factor = factor_list[i]
            flag = 1
        elif var in factor_list[i].var_list and flag == 1:
            first_factor = first_factor.multiply(factor_list[i])
        else:
            new_factor_list.append(factor_list[i])
    if flag:
        new_factor = first_factor.sum_out(var)
        if len(new_factor.var_list):
            new_factor_list.append(new_factor)
    factor_list = new_factor_list

for ev in evidence_list:
    new_factor_list = []
    for factor in factor_list:
        if ev在factor.var_list中：
            new_factor = 对这个factor调用sumout函数
            if new_factor.var_list不为空：
                将new_factor加入到new_factor_list中
        else:
            将factor加入到new_factor_list中
        factor_list = newe_factor_list
for var in ordered_list_of_hidden_variables:
    new_factor_list = []
    for factor_list中的每一个factor：
        if var 在factor.var_list中：
            if 这个是第一次发现var在某个factor.var_list中：
                first_factor = factor
            else:
                first_factor = first_factor.multiply(factor)
        else:
            将factor加入到new_factor_list中
    if first_factor存在：
        new_factor = 调用first_factor的对ev的sumout函数
        if new_factor.var_list非空：
            将new_factor加入到new_factor_list中
    factor_list = new_factor_list

