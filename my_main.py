from collections import deque
import math


class Graph:
    def __init__(self):
        self.vertices = {}  # Dictionary to store vertices

    def add_vertex(self, label):
        if not isinstance(label, str):
            raise ValueError("Label must be a string")

        if label in self.vertices:
            print(f"Vertex '{label}' already exists.")
        else:
            # Use a dictionary to store edges and weights for the vertex
            self.vertices[label] = {}
        return self

    def add_edge(self, src, dest, w):
        if src not in self.vertices or dest not in self.vertices:
            raise ValueError("Source or destination vertex not found")

        if not isinstance(w, (int, float)):
            raise ValueError("Weight must be an integer or a float")

        # Add an edge from src to dest with weight w
        self.vertices[src][dest] = w
        return self

    def get_weight(self, src, dest):
        if src not in self.vertices or dest not in self.vertices:
            raise ValueError("Source or destination vertex not added to graph")

        # Return the weight or inf if no edge exists
        return self.vertices[src].get(dest, float('inf'))

    def dfs(self, starting_vertex):
        if starting_vertex not in self.vertices:
            raise ValueError("Starting vertex does not exist")

        visited = set()

        def dfs_helper(vertex):
            visited.add(vertex)
            yield vertex

            neighbors = sorted(self.vertices[vertex])

            for neighbor in neighbors:
                if neighbor not in visited:
                    yield from dfs_helper(neighbor)

        yield from dfs_helper(starting_vertex)

    def bfs(self, starting_vertex):
        if starting_vertex not in self.vertices:
            raise ValueError("Starting vertex does not exist")

        visited = set()
        queue = deque([starting_vertex])

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                yield vertex

                neighbors = sorted(self.vertices[vertex])
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append(neighbor)

    def dijkstra(self, src):
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[src] = 0
        previous = {vertex: None for vertex in self.vertices}

        queue = list(self.vertices.keys())
        while queue:
            current_vertex = min(queue, key=lambda vertex: distances[vertex])
            queue.remove(current_vertex)

            for neighbor in self.vertices[current_vertex]:
                alternative = distances[current_vertex] + \
                    self.vertices[current_vertex][neighbor]
                if alternative < distances[neighbor]:
                    distances[neighbor] = alternative
                    previous[neighbor] = current_vertex

        return {vertex: self._construct_path(previous, src, vertex) for vertex in self.vertices}


# ==============================================================================================================


    def dsp(self, src, dest):
        if src not in self.vertices or dest not in self.vertices:
            raise ValueError("Source or destination vertex not added to graph")

        distances = {vertex: math.inf for vertex in self.vertices}
        distances[src] = 0
        previous = {vertex: None for vertex in self.vertices}

        visited = set()
        while visited != set(self.vertices):
            current_vertex = min(
                (v for v in distances if v not in visited), key=lambda v: distances[v]
            )
            visited.add(current_vertex)

            for neighbor, weight in self.vertices[current_vertex].items():
                alternative = distances[current_vertex] + weight
                if alternative < distances[neighbor]:
                    distances[neighbor] = alternative
                    previous[neighbor] = current_vertex

        path = []
        current = dest
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        if path[0] != src:
            return math.inf, []
        if dest == "F":
            print(f"({round(distances[dest])}, {path})")
        return round(distances[dest]), path

    # def dsp(self, src, dest):
    #     if src not in self.vertices or dest not in self.vertices:
    #         raise ValueError("Source or destination vertex not added to graph")

    #     distances = {vertex: math.inf for vertex in self.vertices}
    #     distances[src] = 0
    #     previous = {vertex: None for vertex in self.vertices}

    #     visited = set()
    #     while visited != set(self.vertices):
    #         current_vertex = min(
    #             (v for v in distances if v not in visited), key=lambda v: distances[v]
    #         )
    #         visited.add(current_vertex)

    #         for neighbor, weight in self.vertices[current_vertex].items():
    #             alternative = distances[current_vertex] + weight
    #             if alternative < distances[neighbor]:
    #                 distances[neighbor] = alternative
    #                 previous[neighbor] = current_vertex

    #     path = []
    #     current = dest
    #     while current is not None:
    #         path.append(current)
    #         current = previous[current]
    #     path.reverse()

    #     if path[0] != src:
    #         return math.inf, []
    #     return f"({round(distances[dest])}, {path})"

    def _construct_path(self, previous, src, dest):
        path = []
        current = dest
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        if path[0] != src:
            return []
        return path

    def dsp_all(self, src):
        if src not in self.vertices:
            raise ValueError("Source vertex not added to graph")

        return self.dijkstra(src)

    def __str__(self):
        output = "digraph G {\n"

        for vertex, edges in self.vertices.items():
            for neighbor, weight in edges.items():
                label = weight
                output += f'   {vertex} -> {neighbor} [label="{label:.1f}",weight="{weight:.1f}"];\n'

        output += "}"

        return output


def main():
    # ==================================Print it to the console in GraphViz notation as shown in Figure 1. ===============================================================================
    G = Graph()
    G.add_vertex("A").add_vertex("B").add_vertex(
        "C").add_vertex("D").add_vertex("E").add_vertex("F")

    G.add_edge("A", "B", 2.0)
    G.add_edge("A", "F", 9.0)
    G.add_edge("B", "C", 8.0)
    G.add_edge("B", "D", 15.0)
    G.add_edge("B", "F", 6.0)
    G.add_edge("C", "D", 1.0)
    G.add_edge("E", "D", 3.0)
    G.add_edge("E", "C", 7.0)
    G.add_edge("F", "B", 6.0)
    G.add_edge("F", "E", 3.0)

    print(G)

# =========================================Print results of DFS starting with vertex "A" as shown in Figure 2.================================================
    print("starting BFS with vertex A")
    for vertex in G.bfs("A"):
        print(vertex, end="")
    print()

# ===========================================Figure 2. Example of Breadth-First Traversal on example graph G.========================================================
    print("starting DFS with vertex A")
    for vertex in G.dfs("A"):
        print(vertex, end="")
    print()

# =====Print the path from vertex "A" to vertex "F" (not shown here) using Djikstra's shortest path algorithm (DSP) as a string like #3 and #4.======================
    print("Dijkstar's shortest path from 'A' to 'F'")
    for vertex in G.dsp("A", "F"):
        print(vertex, end="")
    print()


# ==============================================USING DSP_ALL()==================================================

    print("DSP_ALL() STARTING AT 'A'")
    for vertex in G.dsp_all("A"):
        print(vertex)
    print()

    print("DSP_ALL() STARTING AT 'A'")
    # for vertex in G.dsp_all("A"):
    #     print(vertex)
    # print()

    display_all = G.dsp_all("A")

    for key, value in display_all.items():
        results = f"{key}: {value}"

        print(f"{{{results}}}")


if __name__ == "__main__":
    main()
