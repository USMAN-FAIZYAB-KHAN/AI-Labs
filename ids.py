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

