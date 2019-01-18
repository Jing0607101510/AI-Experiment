void DFS(int zx, int zy, int depth, int move_index){
    int h = calc_h(cur_puzzle);
    if(h + depth > bound){
        return;
    }
    if(h == 0){
        is_find = true;
        length = depth;
        return;
    }
    for(int i = 0; i < 4; i++){
        if(i+move_index == 3) continue;//如果移动方向与上一次相同，则继续；
        int nzx = zx + moves[i][0];
        int nzy = zy + moves[i][1];
        if(check_legel(nzx, nzy)){
            int shift_num = cur_puzzle[nzx][nzy];
            cur_puzzle[zx][zy] = shift_num;
            cur_puzzle[nzx][nzy] = 0;
            if(calc_h(cur_puzzle)+depth+1 <= bound){
                shift[depth] = shift_num;
                direction[depth] = i;
                DFS(nzx, nzy, depth+1, i);
                if(is_find == true){
                    return;
                }
            }            
            cur_puzzle[nzx][nzy] = shift_num;
            cur_puzzle[zx][zy] = 0;
        }
    }
}