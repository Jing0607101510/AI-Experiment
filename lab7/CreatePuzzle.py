import random
move_x = [0, -1, 0, 1]
move_y = [-1, 0, 1, 0]
origin_puzzle = "123456789abcdef0"
depth = 25

class CreatePuzzle:

    def swap(self, string, i, j):
        if i > j:
            i, j = j, i
        return string[:i] + string[j] + string[i+1:j] + string[i] + string[j+1:]

    def print_puzzle(self, string, split):
        for i in range(len(string)):
            print("%3d" % int(string[i], 16), end=' ')
            if (i+1) % split == 0:
                print()

    def create(self):
        move = []
        path = [origin_puzzle]
        for i in range(depth):
            current_puzzle = path[-1]
            zero_index = current_puzzle.index('0')
            current_x = zero_index // 4
            current_y = zero_index % 4
            while True:
                direction = random.randint(0, 3)
                next_x = current_x + move_x[direction]
                next_y = current_y + move_y[direction]
                if next_x < 0 or next_y < 0 or next_x > 3 or next_y > 3:
                    continue
                next_puzzle = self.swap(current_puzzle, current_x * 4 + current_y, next_x * 4 + next_y)
                if next_puzzle in path:
                    continue
                move.append(current_puzzle[next_x * 4 + next_y])
                path.append(next_puzzle)
                break
        move.reverse()
        return path[-1], move

if __name__ == "__main__":
    create_puzzle = CreatePuzzle()
    random_puzzle, move = create_puzzle.create()
    create_puzzle.print_puzzle(random_puzzle, 4)
    create_puzzle.print_puzzle(move, 20)
    print(random_puzzle)


