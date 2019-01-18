边界节点的集合：boundary
从起点到边界节点的对应的花费集合：g
预计的花费：f
while 还没有找到目标节点：
    从边界节点集合中寻找f花费最小的节点
    if 这个节点为目标节点：
        返回
    else：
        for 这个节点的所有合法且未被访问的子节点：
            if 这个子节点不再boundary之中：
                把这个节点加入到boundary，并将它的花费加入到f和g中
            elif 这个子节点的f花费比在boundary要小：
                则更新在boundary中的f花费以及g花费


边界节点的集合：boundary
从起点到边界节点的对应的花费集合：cost
while 还没有找到目标节点：
    从边界节点集合中寻找花费最小的节点
    if 这个节点为目标节点：
        返回
    else：
        for 这个节点的所有合法且未被访问的子节点：
            if 这个子节点不再boundary之中：
                把这个节点加入到boundary，并将它的花费加入到cost中
            elif 这个子节点的花费比在boundary要小：
                则更新在boundary中的花费




深度界限 max_deep
初始化深度界限为 max_deep = 1
while 没有找到目标节点：
    在设定最大深度界限的条件下使用深度优先寻找目标节点
    如果找到目标节点，则返回
    否则，最大深度界限增加1




从起点开始的宽度优先搜索队列：queue_start
从终点开始的宽度优先搜索队列：queue_end
while 两个搜索的节点没有相交：
    从起点开始的宽度优先搜索一层
    if 有相交的节点：
        返回
    else：
        将这个节点标价为已被访问
    从终点开始的宽度优先搜索一层
    if 有相交的节点：
        返回
    else：
        将这个节点标记为已被访问


queue：存放父节点
while queue非空且未找到目标：
    top = 从queue中弹出第一个元素
    对 top 的所有合法且未被访问的子节点：
        如果不是目标则加入queue中
        否则找到目标，返回


dfs:
    判断当前节点是否未目标节点，若是则返回
    for 对该节点的所有合法且未被访问的子节点：
        递归使用dfs算法
