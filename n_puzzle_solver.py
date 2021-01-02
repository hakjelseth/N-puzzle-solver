import sys


class Node:
    def __init__(self, board, level, road, goal):
        self.board = board
        self.level = level
        self.goal = goal
        self.f = self.h() + level
        self.road = road

    def find(self):
        """ Specifically used to find the position of the blank space """
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    return i, j

    def print(self):
        return self.board

    def generate_child(self):
        x, y = self.find()
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child, r = self.shuffle(x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level + 1, self.road + r, self.goal)
                children.append(child_node)
        return children

    def shuffle(self, x1, y1, x2, y2):
        if 0 <= x2 < len(self.board) and 0 <= y2 < len(self.board):
            puzzle = self.copy()
            temp = puzzle[x2][y2]
            puzzle[x2][y2] = puzzle[x1][y1]
            puzzle[x1][y1] = temp
            if x2 > x1:
                r = 'D'
            elif x2 < x1:
                r = 'U'
            elif y2 > y1:
                r = 'R'
            elif y2 < y1:
                r = 'L'
            return puzzle, r
        else:
            return None, None

    def copy(self):
        newList = []
        for i in range(len(self.board)):
            temp = []
            for j in range(len(self.board)):
                temp.append(self.board[i][j])
            newList.append(temp)
        return newList

    def h(self):
        difference = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] != self.goal[i][j]:
                    difference += 1
        return difference


class Puzzle:
    def __init__(self, n, board, output, goal):
        self.n = n
        self.board = board
        self.output = output
        self.goal = goal

    def process(self):
        node = Node(self.board, 0, "", self.goal)
        start = Node(self.board, 0, "", self.goal)
        # node.print()
        states = 0
        queue = []
        visited = []
        queue.append(node)

        while True:
            current = queue[0]
            if current.h() == 0:
                last = current
                break
            children = current.generate_child()
            for i in children:
                if i.board not in visited:
                    states = states + 1
                    queue.append(i)

            visited.append(current.board)

            queue.pop(0)
            queue.sort(key=lambda x: x.f, reverse=False)

        brett = start.print()
        f = open(self.output, 'w+')
        for i in brett:
            f.write(str(i) + '\n')
        f.write("Solution: " + str(len(last.road)) + ", " + last.road + '\n')
        f.write("States seen: " + str(states) + '\n')


def main():
    filename = sys.argv[1]
    output = sys.argv[2]
    f = open(filename, 'r')

    n = int(f.readline().strip())
    board = [[0] * n for i in range(n)]

    for i in range(n):
        row = f.readline().split()
        for j in range(len(row)):
            board[i][j] = int(row[j])

    eight_problem = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    fifteen_problem = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    if n == 3:
        puzzle = Puzzle(n, board, output, eight_problem)
    elif n == 4:
        puzzle = Puzzle(n, board, output, fifteen_problem)

    # puzzle = Puzzle(n, board, output)
    puzzle.process()


main()
