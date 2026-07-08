from collections import deque


class PathFinder:

    def __init__(self, graph):

        self.graph = graph

    # ---------------------------------------------------------

    def find(self, source, target):

        if source == target:

            return [source]

        queue = deque()

        queue.append((source, [source]))

        visited = {source}

        while queue:

            node, path = queue.popleft()

            for neighbor in self.graph.neighbors(node):

                if neighbor == target:

                    return path + [neighbor]

                if neighbor not in visited:

                    visited.add(neighbor)

                    queue.append(

                        (

                            neighbor,

                            path + [neighbor]

                        )

                    )

        return None
