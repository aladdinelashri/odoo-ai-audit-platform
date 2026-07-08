from collections import deque


class PathFinder:

    def __init__(self, graph):

        self.graph = graph

    # ---------------------------------------------------------

    def find(self, source, target):

        if source == target:

            return []

        queue = deque()

        queue.append(

            (

                source,

                []

            )

        )

        visited = {source}

        while queue:

            table, path = queue.popleft()

            for relation in self.graph.neighbors(table):

                next_table = relation["table"]

                if next_table in visited:

                    continue

                new_path = path + [relation]

                if next_table == target:

                    return new_path

                visited.add(next_table)

                queue.append(

                    (

                        next_table,

                        new_path

                    )

                )

        return None
