Backtracking(level):
输入：level 深度优先搜索的深度（也就是已被赋值的变量个数+1）

    if 所有的变量都被赋值了:
        return 这些变量的取值
    选取某一个还未被赋值的变量v
    标记v变量已经被赋值

    for v 变量值域中的每一个取值d：
        将v变量赋值为d
        定义一个标记变量flag = True
        for 每一个于变量v有关的约束：
            if v变量赋值为d后不满足某个约束：
                flag = False
        if flag == True：
            BT(level+1)
    
    标记v变量还没被赋值
    retutn