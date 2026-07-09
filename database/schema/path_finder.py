from collections import deque


class PathFinder:

    def __init__(self, graph):

        self.graph = graph

    # ---------------------------------------------------------

    def find(self, source, target):

        if source == target:

            return []

        visited = set()

        queue = deque()

        queue.append((source, []))

        while queue:

            table, path = queue.popleft()

            if table in visited:

                continue

            visited.add(table)

            for relation in self.graph.from_table(table):

                next_table = relation["target_table"]

                new_path = path + [relation]

                if next_table == target:

                    return new_path

                queue.append(

                    (

                        next_table,

                        new_path

                    )

                )

        return []
