# function GRAPH-SEARCH(problem) returns a solution, or failure
# initialize the frontier using the initial state of problem
# initialize the explored set to be empty
# loop do
# if the frontier is empty then return failure
# choose a leaf node and remove it from the frontier
# if the node contains a goal state then return the corresponding solution
# add the node to the explored set
# expand the chosen node, adding the resulting nodes to the frontier
# only if not in the frontier or explored set

# function CHILD-NODE(problem, parent, action) returns a node
# return a node with
# STATE = problem.RESULT(parent.STATE, action),
# PARENT = parent, ACTION = action,
# PATH-COST = parent.PATH-COST + problem.STEP-COST(parent.STATE, action)

# function DEPTH-LIMITED-SEARCH(problem, limit) returns a solution, or failure/cutoff
# return RECURSIVE-DLS(MAKE-NODE(problem.INITIAL-STATE), problem, limit)
# function RECURSIVE-DLS(node, problem, limit) returns a solution, or failure/cutoff
# if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
# else if limit = 0 then return cutoff
# else
# cutoff occurred?←false
# for each action in problem.ACTIONS(node.STATE) do
# child ← CHILD-NODE(problem, node, action)
# result ← RECURSIVE-DLS(child, problem, limit − 1)
# if result = cutoff then cutoff occurred?← true
# else if result != failure then return result
# if cutoff occurred? then return cutoff else return failure

# function ITERATIVE-DEEPENING-SEARCH(problem) returns a solution, or failure
# for depth = 0 to ∞ do
# result ← DEPTH-LIMITED-SEARCH(problem, depth)
# if result != cutoff then return result


def depth_limited_search(graph, node, goal, depth):
    print(node, end=" ")
    if node == goal:
        return [node]
    if depth == 0:
        return None
    for neighbor in graph.get(node, []):
        result = depth_limited_search(graph, neighbor, goal, depth - 1)
        if result is not None:
            return [node] + result
    return None

def iterative_deepening_search(graph, start, goal):
    depth = 0
    while True:
        print()
        print(f"Depth: {depth}")
        result = depth_limited_search(graph, start, goal, depth)
        if result is not None:
            return result
        depth += 1

graph = {
    'S': ['A', 'D'],
    'A': ['B', 'C'],
    'B': ['C', 'E'],
    'C': ['G'],
    'D': ['B', 'E'],
    'E': ['G'],
    'G': []
}

solution = iterative_deepening_search(graph, 'S', 'G')
print("\nSolution:")
print(" --> ".join(solution))

