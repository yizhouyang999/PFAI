from copy import deepcopy
class EightPuzzle:
    def __init__(self, initial_state):
        self.state = initial_state
        self.goal_state = [['e', 1, 2], [3, 4, 5], [6, 7, 8]]
        self.action = ['u', 'd', 'l', 'r']

    def move(self, action):
        if action == 'u':
            dc = deepcopy(self)
            if dc.u():
                return dc
        elif action == 'd':
            dc = deepcopy(self)
            if dc.d():
                return dc
        elif action == 'l':
            dc = deepcopy(self)
            if dc.l():
                return dc
        elif action == 'r':
            dc = deepcopy(self)
            if dc.r():
                return dc


    def h1(self):
        # Heuristic 1: Number of tiles out of place
        count = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != self.goal_state[i][j]:
                    count += 1
        return count

    def h2(self):
        # Heuristic 2: Manhattan distance
        distance = 0
        for i in range(3):
            for j in range(3):
                tile = self.state[i][j]
                goal_position1,goal_position2 = self.find_goal_position(tile)
                distance += abs(i - goal_position1) + abs(j - goal_position2)
        return distance

    def u(self):
        # Move the empty tile up
        empty_row = 0
        empty_col = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 'e':
                    empty_row = i
                    empty_col = j
        if empty_row == 0:
            return None
        else:
            temp1=self.state[empty_row][empty_col]
            temp2=self.state[empty_row-1][empty_col]
            self.state[empty_row][empty_col]=temp2
            self.state[empty_row-1][empty_col]=temp1
            return True

    def d(self):
        # Move the empty tile down
        empty_row = 0
        empty_col = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 'e':
                    empty_row = i
                    empty_col = j
        if empty_row == 2:
            return None
        else:
            temp1=self.state[empty_row][empty_col]
            temp2=self.state[empty_row+1][empty_col]
            self.state[empty_row][empty_col]=temp2
            self.state[empty_row+1][empty_col]=temp1
            return True

    def l(self):
        # Move the empty tile left
        empty_row = 0
        empty_col = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 'e':
                    empty_row = i
                    empty_col = j
        if empty_col == 0:
            return None
        else:
            temp1=self.state[empty_row][empty_col]
            temp2=self.state[empty_row][empty_col-1]
            self.state[empty_row][empty_col]=temp2
            self.state[empty_row][empty_col-1]=temp1
            return True

    def r(self):
        # Move the empty tile right
        empty_row = 0
        empty_col = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 'e':
                    empty_row = i
                    empty_col = j
        if empty_col == 2:
            return None
        else:
            temp1=self.state[empty_row][empty_col]
            temp2=self.state[empty_row][empty_col+1]
            self.state[empty_row][empty_col]=temp2
            self.state[empty_row][empty_col+1]=temp1
            return True


    def find_goal_position(self, tile):
        for i in range(3):
            for j in range(3):
                if self.goal_state[i][j] == tile:
                    return i, j

    def pretty_print(self):
        # Implement a method to print the current state in a readable format
        print("Current frontier: ")
        for i in range(3):
            print(" ".join(str(x) for x in self.state[i]))

    def check_goal(self):
        # Implement a method to check if the current state is the goal state
        if self.state == self.goal_state:
            return True
        else:
            return False


