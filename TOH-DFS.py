class State:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

class TowerOfHanoi:
    def __init__(self, n):
        self.n = n
        self.goal_state = tuple(range(n, 0, -1))
        self.dead_ends = set()
        self.generate_dead_ends()

    def generate_dead_ends(self):
        for i in range(self.n):
            dead_end = [0] * self.n
            dead_end[i] = self.n
            self.dead_ends.add(tuple(dead_end))

    def is_goal_state(self, state):
        return state.state == self.goal_state

    def is_dead_end(self, state):
        return state.state in self.dead_ends

    def get_successors(self, state):
        successors = []
        for i in range(self.n):
            for j in range(self.n):
                if i != j and (state.state[i] == 0 or state.state[i] > state.state[j]):
                    new_state = list(state.state)
                    new_state[i], new_state[j] = new_state[j], new_state[i]
                    if not self.is_dead_end(State(tuple(new_state))):
                        successors.append(State(tuple(new_state), state, (i, j)))
        return successors

    def dfs(self):
        start_state = State(tuple(range(self.n, 0, -1)))
        stack = [start_state]
        visited = set()
        while stack:
            state = stack.pop()
            if self.is_goal_state(state):
                return self.get_action_plan(state)
            visited.add(state)
            successors = self.get_successors(state)
            for successor in successors:
                if successor not in visited:
                    stack.append(successor)
        return None

    def get_action_plan(self, state):
        action_plan = []
        while state.parent:
            action_plan.append(state.action)
            state = state.parent
        return action_plan[::-1]

    def print_state_space(self):
        for i in range(self.n):
            for j in range(self.n):
                state = [0] * self.n
                state[i] = j + 1
                if tuple(state) == self.goal_state:
                    print("G", end=" ")
                elif tuple(state) in self.dead_ends:
                    print("X", end=" ")
                else:
                    print(".", end=" ")
            print()

if __name__ == "__main__":
    toh = TowerOfHanoi(5)
    print("State space:")
    toh.print_state_space()
    print("Action plan:")
    action_plan = toh.dfs()
    for action in action_plan:
        print(f"Move disk from peg {action[0]+1} to peg {action[1]+1}")
