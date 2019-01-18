#include<iostream>
#include<vector>
#include<cmath>
#include<string.h>
#include<limits.h>
#include<ctime>
#include<fstream>
#include<cmath>
using namespace std;

double bound = 0;
bool is_find = false;
int length = 0;
vector<int> shift(100);
vector<int> direction(100);
int moves[][2] = {{0,1}, {1, 0}, {-1, 0}, {0,-1}};
int target[][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12},
    {13, 14, 15, 0}
};
int puzzle1[][4] = {
    {11, 3, 1, 7},
    {4, 6, 8, 2},
    {15, 9, 10, 13},
    {14, 12, 5, 0}
};
int puzzle2[][4] = {
    {14, 10, 6, 0},
    {4, 9, 1, 8},
    {2, 3, 5, 11},
    {12, 13, 7, 15}
};
int puzzle3[][4] = {
    {0, 5, 15, 14},
    {7, 9, 6, 13},
    {1, 2, 12, 10},
    {8, 11, 4, 3}
};
int puzzle4[][4] = {
    {6, 10, 3, 15},
    {14, 8, 7, 11},
    {5, 1, 0, 2},
    {13, 12, 9, 4}
};
// int puzzle1[][4] = { {2,   6,   3,   4},
//                     {1,   0,   7,   8},
//                     {5,  10,  15,  11},
//                     {9,  13,  14,  12}};
// int puzzle2[][4] = {{5,   1,   3,   4},
//                     {9,   6,   7,   2},
//                     {10,  14,   0,   8},
//                     {13,  15,  11,  12}};
// int puzzle3[][4] = {{2,   3,   7,   4},
//                     {6,  10,   8,  15},
//                     {1,  13,  14,   0},
//                     {5,   9,  12,  11}};
// int puzzle4[][4] = {{2,   5,   4,   8},
//                     {1,  10,   6,   3},
//                     {13,   0,   7,  12},
//                     {14,   9,  11,  15}};
int cur_puzzle[4][4];


bool solvable(int puzzle[4][4]){
    int ni = 0;
    vector<int> num;
    int zx = -1;
    int zy = -1;
    for(int i = 0; i < 4; i++){
        for(int j = 0; j < 4; j++){
            num.push_back(puzzle[i][j]);
            if(puzzle[i][j] == 0){
                zx = i;
                zy = j;
            }
        }
    }
    for(int i = 0; i < 16; i++){
        if(num[i] == 0) continue;
        for(int j = i+1; j < 16; j++){
            if(num[j] !=0 && num[i] > num[j]){
                ni++;
            }
        }
    }
    int dif = abs(3 - zx);
    if((dif + ni) % 2 == 0){
        return true;
    }
    else{
        return false;
    }
}

int calc_h(int puzzle[4][4]){
    double h = 0;
    for(int i = 0; i < 4; i++){
        for(int j = 0; j < 4; j++){
            if(puzzle[i][j] != 0){
                int r = (puzzle[i][j] - 1) / 4;
                int c = (puzzle[i][j] - 1) % 4;
                h += abs(i - r) + abs(j - c);
            }
        }
    }
    return h;
}

double calc_h_not_inside(int puzzle[4][4]){
    double h = 0;
    for(int i = 0; i < 4; i++){
        for(int j = 0; j < 4; j++){
            if(puzzle[i][j] != 0){
                if(puzzle[i][j] != i*4+j+1)
                	h += 1;
            }
        }
    }
    return h;
}

double calc_h_greatest(int puzzle[4][4]){
	double h = 0;
    for(int i = 0; i < 4; i++){
        for(int j = 0; j < 4; j++){
            if(puzzle[i][j] != 0){
                int r = (puzzle[i][j] - 1) / 4;
                int c = (puzzle[i][j] - 1) % 4;
                h += max(abs(i - r), abs(j - c));
            }
        }
    }
    return h;
}

double calc_h_euclidean(int puzzle[4][4]){
	double h = 0;
    for(int i = 0; i < 4; i++){
        for(int j = 0; j < 4; j++){
            if(puzzle[i][j] != 0){
                int r = (puzzle[i][j] - 1) / 4;
                int c = (puzzle[i][j] - 1) % 4;
                h += sqrt((i - r)*(i-r)+ (j-c)*(j - c));
            }
        }
    }
    return h;
}

bool check_legel(int zx, int zy){
    if(zx>=0 && zx <= 3 && zy >= 0 && zy <= 3){
        return true;
    }
    else{
        return false;
    }
}

void DFS(int zx, int zy, int depth, int move_index){
    double h = calc_h(cur_puzzle);
    if(h + depth > bound){
        //return h+depth;
        return;
    }
    if(h == 0){
        is_find = true;
        cout << "depth"<< depth << endl;
        length = depth;
        return;
        //return depth;
    }
    //int min_cost = INT_MAX;
    for(int i = 0; i < 4; i++){
        if(i+move_index == 3) continue;//如果移动方向与上一次相同，则继续；
        int nzx = zx + moves[i][0];
        int nzy = zy + moves[i][1];
        if(check_legel(nzx, nzy)){
            int shift_num = cur_puzzle[nzx][nzy];
            cur_puzzle[zx][zy] = shift_num;
            cur_puzzle[nzx][nzy] = 0;
            //min_cost = min(calc_h(cur_puzzle)+depth+1, min_cost);
            if(calc_h(cur_puzzle)+depth+1 <= bound){
                shift[depth] = shift_num;
                direction[depth] = i;
                //int b = DFS(nzx, nzy, depth+1, i);
                DFS(nzx, nzy, depth+1, i);
                if(is_find == true){
                    //return b;
                    return;
                }
                //min_cost = min(b, min_cost);
            }            
            cur_puzzle[nzx][nzy] = shift_num;
            cur_puzzle[zx][zy] = 0;
        }
    }
    //return min_cost;
}

int IDA_star(){
    //shift.clear();
    //direction.clear();
    bound = calc_h(cur_puzzle);
    is_find = false;
    length = 0;
    int zx = -1;
    int zy = -1;
    for(int i = 0; i < 4; i++){
        bool flag = false;
        for(int j = 0; j < 4; j++){
            if(cur_puzzle[i][j] == 0){
                zx = i;
                zy = j;
                flag = true;
                break;
            }
        }
        if(flag) break;
    }
    while(!is_find && bound < 70){
        DFS(zx, zy, 0, -1);
        if(!is_find){
            bound += 1;
        }
    }
}

int main(void){
    cout << "not_in_side!" << endl;
    fstream file;
    file.open("result_greatest.txt", ios::out);
    
    memcpy(&cur_puzzle[0][0], &puzzle1[0][0], 64);
    clock_t start1 = clock();
    IDA_star();
    clock_t end1 = clock();
    for(int i = 0; i < length; i++){
        cout << shift[i] << " ";
        file << shift[i] << " ";
    }
    cout << endl;
    file << endl;
    for(int i = 0; i < length; i++){
        cout << direction[i] << " ";
        file << direction[i] << "";
    }
    cout << endl;
    file << endl;
    cout << "time used:" << (end1 - start1) * 1.0 / CLOCKS_PER_SEC << "s" << endl;
    file << "time used:" << (end1 - start1) * 1.0 / CLOCKS_PER_SEC << "s" << endl;
    cout << endl;
    file << endl;

    memcpy(&cur_puzzle[0][0], &puzzle2[0][0], 64);
    clock_t start2 = clock();
    IDA_star();
    clock_t end2 = clock();
    for(int i = 0; i < length; i++){
        cout << shift[i] << " ";
        file << shift[i] << " ";
    }
    cout << endl;
    file << endl;
    for(int i = 0; i < length; i++){
        cout << direction[i] << " ";
        file << direction[i] << " ";
    }
    cout << endl;
    file << endl;
    cout << "time used:" << (end2 - start2) * 1.0 / CLOCKS_PER_SEC << "s" << endl;
    file << "time used:" << (end2 - start2) * 1.0 / CLOCKS_PER_SEC << "s" << endl;
    cout << endl;
    file << endl;

    memcpy(&cur_puzzle[0][0], &puzzle3[0][0], 64);
    clock_t start3 = clock();
    IDA_star();
    clock_t end3 = clock();
    for(int i = 0; i < length; i++){
        cout << shift[i] << " ";
        file << shift[i] << " ";
    }
    cout << endl;
    file << endl;
    for(int i = 0; i < length; i++){
        cout << direction[i] << " ";
        file << direction[i] << " ";
    }
    cout << endl;
    file << endl;
    cout << "time used:" << (end3 - start3) * 1.0 / CLOCKS_PER_SEC << "s" << endl;
    file << "time used:" << (end3 - start3) * 1.0 / CLOCKS_PER_SEC << "s" << endl;
    cout << endl;
    file << endl;

    memcpy(&cur_puzzle[0][0], &puzzle4[0][0], 64);
    clock_t start4 = clock();
    IDA_star();
    clock_t end4 = clock();
    for(int i = 0; i < length; i++){
        cout << shift[i] << " ";
        file << shift[i] << " ";
    }
    cout << endl;
    file << endl;
    for(int i = 0; i < length; i++){
        cout << direction[i] << " ";
        file << direction[i] << " ";
    }
    cout << endl;
    file << endl;
    cout << "time used:" << (end4 - start4) * 1.0 / CLOCKS_PER_SEC << "s" << endl;
    file << "time used:" << (end4 - start4) * 1.0 / CLOCKS_PER_SEC << "s" << endl;
    cout << endl;
    file << endl;
    file.close();
    return 0;
}
