#PegsState class contains needfull data
class PegsState:
    def __init__(self, state, parent_data=None, source_peg=None, dest_peg=None, cost=0, heuristic_value=0):
        self.state = state
        self.parent_data = parent_data
        self.source_peg = source_peg
        self.dest_peg = dest_peg
        self.cost = cost
        self.heuristic_value = heuristic_value

    def __str__(self):
        return f"State: {self.state}\nSourcePeg: {self.source_peg}\nDestPeg: {self.dest_peg}\nCost: {self.cost}\nHeuristicValue: {self.heuristic_value}"

#NodeState class is used for store pegs data
class PegsData:
    def __init__(self, pegs):
        self.pegs = pegs

    def __hash__(self):
        return hash(str(self.pegs))

    def __eq__(self, other):
        return self.pegs == other.pegs

    def __str__(self):
        return str(self.pegs)

def print_move_disk(source_peg, dest_peg):
    return f"Move disk from peg {source_peg} to peg {dest_peg}"

def print_unsafe_state(state, move):
    return f"state {state} , move {move}"

def get_possible_moves_from_state(state):
    pegs = state.pegs
    moves = []

    #getting possible moves with compare other pegs
    for i, selected_peg in enumerate(pegs):
        if selected_peg:
            for j, dest_peg in enumerate(pegs):
                #compare top most disk with selected and destinate peg
                #also check for destinate peg is empty or not
                if i != j and (not dest_peg or selected_peg[-1] < dest_peg[-1]):
                    moves.append((i, j))
                elif selected_peg[-1] and dest_peg[-1] and selected_peg[-1] > dest_peg[-1] and [pegs, (i, j)] not in unsafe_or_dead_state_a_star:
                    unsafe_or_dead_state_a_star.append([state.pegs, (i, j)])    
    return moves


#copy pegs data to temp peg
#remove disk from source peg and add to destinate peg and return as new Node
def apply_move_to_state(current_state, move):
    source_peg, destinate_peg = move
    temp_peg = [peg.copy() for peg in current_state.pegs]
    disk = temp_peg[source_peg].pop()
    temp_peg[destinate_peg].append(disk)
    return PegsData(temp_peg)

def get_heuristic_value(current_state):
    pegs = current_state.pegs
    #we can also use num_disk as static '5'
    disks_count = sum(len(peg) for peg in pegs)
    #subtract 1 from value cause moving disk cost 1
    return disks_count - len(pegs[-1]) - 1

def dfs_algorithm(disks_count):
    tower_of_hanoi_with_dfs_search(disks_count, "0", "1", "2",dfs_depth)

    if dfs_action_plan:
        for step in dfs_action_plan:
            print(step)
    else:
        print("No solution found.")

    print("\nState space:")
    for state in state_space:
        print(state)

    print("\nUnsafe or Dead-end state:")
    for state in unsafe_or_dead_state_dfs:
        print(state)    

def tower_of_hanoi_with_dfs_search(n, source_peg, auxiliary_peg, destination_peg, depth):
    state = (n, source_peg, auxiliary_peg, destination_peg)
    state_space.add(state)

    if n > depth:
        return False

    if n == 1:
        dfs_action_plan.append(print_move_disk(source_peg, destination_peg))
        return 
    
    unsafe_or_dead_state_dfs.append(state)
    
    if (n-1, destination_peg, auxiliary_peg, source_peg) in dfs_action_plan:
            unsafe_or_dead_state_dfs.remove((n-1, destination_peg, auxiliary_peg, source_peg))

    if (n-1, source_peg, auxiliary_peg, destination_peg) in dfs_action_plan:
        unsafe_or_dead_state_dfs.remove((n-1, source_peg, auxiliary_peg, destination_peg))

    if (n-1, auxiliary_peg, destination_peg, source_peg) in dfs_action_plan:
        unsafe_or_dead_state_dfs.remove((n-1, auxiliary_peg, destination_peg, source_peg))

    tower_of_hanoi_with_dfs_search(n - 1, source_peg, destination_peg, auxiliary_peg, depth-1)
    dfs_action_plan.append(print_move_disk(source_peg, destination_peg))
    tower_of_hanoi_with_dfs_search(n - 1, auxiliary_peg, source_peg, destination_peg, depth-1)

def tower_of_hanoi_with_a_star_search(initial_state):
    open_list = [PegsState(initial_state)]
    closed_set = set()
    goal_state = PegsData([[], [], initial_state.pegs[0]])
    #print("goal_state",goal_state)

    while open_list:
        #choose minimum value node.
        current_node = min(open_list, key=lambda n: n.cost + n.heuristic_value)
        #print("current_node",current_node)

        if current_node.state == goal_state:
            return current_node

        open_list.remove(current_node)
        closed_set.add(current_node.state)

        possible_moves = get_possible_moves_from_state(current_node.state)
        for move in possible_moves:
            new_state = apply_move_to_state(current_node.state, move)
            if is_dead_end(new_state.pegs) and [new_state.pegs,move] not in unsafe_or_dead_state_a_star:
                unsafe_or_dead_state_a_star.append([new_state.pegs, move])

            #print("new-state",new_state)
            new_cost_value = current_node.cost + 1
            new_heuristic_value = get_heuristic_value(new_state)
            #print("new_heuristic",new_heuristic, end="")
            if new_state not in closed_set:
                #print("new_state",new_state);
                # if is_dead_end(new_state):
                #     dead_ends.append([new_state, move])
                new_node = PegsState(new_state, current_node, move[0], move[1], new_cost_value, new_heuristic_value)
                open_list.append(new_node)
       
    return None

# def is_dead_end(state):
#     pegs = state.pegs
#     for peg in pegs:
#         if len(peg) > 1:
#             for i in range(1, len(peg)):
#                 if peg[i] < peg[i - 1]:
#                     return True
#     return False
def is_dead_end(state):
    for i in range(len(state)):
        if i == 0:
            continue
        if state[i] < state[i-1]:
            return True
    return False

def a_start_algorithm(disks_count):
    initial_pegs = [list(range(disks_count, 0, -1)), [], []]
    initial_state = PegsData(initial_pegs)
    goal_state = PegsData([[], [], list(range(disks_count, 0, -1))])

    solution_node = tower_of_hanoi_with_a_star_search(initial_state)
    solution_step = []

    if solution_node:
        solution_steps = []

        while solution_node.parent_data:
            solution_steps.append(print_move_disk(solution_node.source_peg, solution_node.dest_peg))
            solution_node = solution_node.parent_data

        solution_steps.reverse()
        #print(solution_steps)
        solution_step = solution_steps
    else:
        solution_step = None
    
    if solution_step:
        for step in solution_step:
            print(step)
    else:
        print("No solution found.")

    print("\nUnsafe or Dead-end state:")
    for state in unsafe_or_dead_state_a_star:
        print(print_unsafe_state(state[0], state[1]))
    
disks_count = 5
state_space = set()
dfs_action_plan = []
unsafe_or_dead_state_dfs = []

print('*Tower of Hanoi* (5 disks)')
dfs_depth = int(input("Enter the depth limit: "))
print(f"Solution for Tower of Hanoi with {disks_count} disks:")
print("\nSolution with DFS algorithm")
dfs_algorithm(disks_count)

unsafe_or_dead_state_a_star = []

print("\nSolution with A* algorithm")
a_start_algorithm(disks_count)