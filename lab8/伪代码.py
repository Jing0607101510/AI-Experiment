AlphaBeta:
    输入：棋盘board, 下棋一方color, 剩余的深度depth, alpha的值a, beta的值b
    输出：子节点的最大值
    max = 负无穷
    if color 是我方:
        设置sign = 1
    else:
        设置sign = -1
    if depth <= 0:
        return 对当前棋盘状态的估价*sign
    if 当前一方不能下棋：
        if 对方也不能下棋：
            return 对当前棋盘状态的估计*sign
        return -AlphaBeta(board, -b, -a, -color, depth)
    for 对每一个能够下棋的合法位置move：
        将棋盘board的move位置放下color方颜色的棋子
        val = -AlphaBeta(board, -b, -a, -color, depth-1)
        将棋盘board原来的move位置恢复
        if val > a:
            if val >= b:
                return val
            a = val
        max = max(val, max)
    return max


evalute:
    输入：棋盘board
    输出：估价值
    初始化黑棋的估价值black_value=0
    初始化白旗的估价值white_value=0
    for 棋盘上的每一个位置pos：
        if pos 上的棋子是黑棋：
            black_value += 这个位置的稳定度对应的权重
        elif pos上的棋子是白棋：
            white_value += 这个位置上稳定度对应的权重
    white_value += 这个棋盘状态下白棋的行动力
    black_value += 这个棋盘状态下黑棋的行动力
    return black_value - white_value

evalute:
    输入：棋盘board
    输出：估计值
    初始化黑棋的估价值black_value=0
    初始化白旗的估价值white_value=0
    统计棋盘上的黑棋数量 赋值给black_value
    统计棋盘上的白旗的数量 赋值给white_value
    return black_value - white_value

evalute:
    输入：棋盘board
    输出：估价值
    初始化黑棋的估价值black_value=0
    初始化白旗的估价值white_value=0
    for 棋盘上每一个位置pos:
        if 这个位置是棋盘的是个角：
            if 有黑棋：
                black_value += 5
            elif 有白旗：
                white_value += 5
        elif 这个位置是棋盘的边：
            if 有黑棋：
                black_value += 2
            elif 有白旗：
                white_value += 2
        else：
            if 有黑棋：
                black_value += 1
            elif 有白旗：
                white_value += 1
    black_value = 2*black_value + 黑棋的行动力
    white_value = 2*white_value + 白旗的行动力
    return black_value - white_value
