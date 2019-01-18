开启列表：open
关闭列表：close
将起始状态加入开始列表中
while open列表非空 && 未找到目标状态:
    从open列表中取出f值最小的一个状态s
    从open列表中删除状态s
    并将状态s加入到关闭列表close中
    if s 是目标节点:
        标志已找到目标状态
    else:
        计算这个状态的4个子状态，还有它们的f，g，h值
        if 子状态在关闭列表close中：
            continue
        if 子状态在open列表中：
            更新该状态在open列表中的f，g，h值
        else:
            将这些状态加入open列表中


设置阈值bound
从起始节点开始
DFS过程：
    计算当前节点的h值
    if h+g值超过了bound：
        return
    if h == 0：
        找到了目标节点
        return
    for 当前状态的4个子状态：
        if 如果该子状态的f值不超过bound：
            递归DFS过程
if 在当前bound下还没有找到目标状态：
    将bound增1
    从起始节点开始，重新开始DFS过程
