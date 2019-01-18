import pandas as pd

class VariableElimination:
    @staticmethod
    def inference(factor_list, query_variables,
                  ordered_list_of_hidden_variables, evidence_list):#Node, 字符串类型， 字符串类型， 字典类型
        for ev in evidence_list:#需要将factor_list中的涉及的因子取出来（）删除，得出的有过可能需要加入到factor_list中,
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

    @staticmethod
    def print_factors(factor_list):
        for factor in factor_list:
            factor.print_inf()


class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.var_list = var_list#字符串列表
        self.cpt = {}

    def set_cpt(self, cpt):
        self.cpt = cpt

    def print_inf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.var_list))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        print()

    def multiply(self, factor):
        '''function that multiplies with another factor'''
        data1 = {self.var_list[i]:[value[i] for value in self.cpt.keys()] for i in range(len(self.var_list))}
        data1['Probability1'] = [p for p in self.cpt.values()]
        df1 = pd.DataFrame(data=data1, columns=(self.var_list+['Probability1']))

        # print('df1')
        # print(df1)

        data2 = {factor.var_list[i]:[value[i] for value in factor.cpt.keys()] for i in range(len(factor.var_list))}
        data2['Probability2'] = [p for p in factor.cpt.values()]
        df2 = pd.DataFrame(data=data2, columns=(factor.var_list+['Probability2']))

        # print('df2')
        # print(df2)


        df3 = pd.merge(df1, df2)
        df3['Probability'] = df3['Probability2'] * df3['Probability1']

        collection = self.var_list + factor.var_list
        new_list = set(collection)
        new_list = sorted(list(new_list), key=collection.index)

        # print('df3')
        # print(df3)

        new_cpt = {}
        for _, row in df3.iterrows():
            new_cpt[''.join([row[c] for c in new_list])] = row['Probability']
        
        

        new_node = Node('f' + str(new_list), new_list)#new_line是有关的变量的列表
        new_node.set_cpt(new_cpt)#因子，字典
        return new_node


    def sum_out(self, variable):
        '''function that sums out a variable given a factor'''
        
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

        new_node = Node('f' + str(new_var_list), new_var_list)
        new_node.set_cpt(new_cpt)
        return new_node

    def restrict(self, variable, value):#variable是字符串类型, value是0或者1
        '''function that restricts a variable to some value
        in a given factor'''

        index = self.var_list.index(variable)
        new_var_list = [var for var in self.var_list if var != variable]

        new_cpt = {key[:index]+key[index+1:] : v for key, v in self.cpt.items() if key[index] == str(value)}

        new_node = Node('f' + str(new_var_list), new_var_list)
        new_node.set_cpt(new_cpt)
        return new_node


# Create nodes for Bayes Net
B = Node('B', ['B'])
E = Node('E', ['E'])
A = Node('A', ['A', 'B', 'E'])
J = Node('J', ['J', 'A'])
M = Node('M', ['M', 'A'])

# Generate cpt for each node
B.set_cpt({'0': 0.999, '1': 0.001})
E.set_cpt({'0': 0.998, '1': 0.002})
A.set_cpt({'111': 0.95, '011': 0.05, '110': 0.94, '010': 0.06,
           '101':0.29, '001': 0.71, '100': 0.001, '000': 0.999})
J.set_cpt({'11': 0.9, '01': 0.1, '10': 0.05, '00': 0.95})
M.set_cpt({'11': 0.7, '01': 0.3, '10': 0.01, '00': 0.99})

print("P(J,M) ***********")
VariableElimination.inference([B, E, A, J, M], ['J', 'M'], ['B', 'E', 'A'], {})

print("P(B, E, A, J, M) **********")
VariableElimination.inference([B, E, A, J, M], ['B', 'E', 'A', 'J', 'M'], [], {})

print("P(A | J, M)************" )
VariableElimination.inference([B, E, A, J, M], ['A'], ['B', 'E'], {'J':1, 'M':1})

print("P(J, ~M | ~B)******************")
VariableElimination.inference([B, E, A, J, M], ['J', 'M'], ['E', 'A'], {'B':0})

