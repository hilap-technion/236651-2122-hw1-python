import unittest
import ast
import Refactor

class TestExtractToVariable(unittest.TestCase):
    code = """def dijkstra(self, start_vertex):
        D = {v:float('inf') for v in range(self.v)}
        D[start_vertex] = 0

        pq = PriorityQueue()
        pq.put((0, start_vertex))

        while not pq.empty():
            (dist, current_vertex) = pq.get()
            self.visited.append(current_vertex)

            for neighbor in range(self.v):
                if self.edges[current_vertex][neighbor] != -1:
                    distance = self.edges[current_vertex][neighbor]
                    if neighbor not in self.visited:
                        old_cost = D[neighbor]
                        new_cost = D[current_vertex] + distance
                        if new_cost < old_cost:
                            pq.put((new_cost, neighbor))
                            D[neighbor] = new_cost
        return D"""
    maxDiff = None
    def testExtractSimpleExpr(self):
        funcDef = ast.parse(self.code).body[0]
        changed = Refactor.extract(funcDef,((6,15),(6,32)),"init")
        self.assertTrue(changed)
        self.assertEqual("""def dijkstra(self, start_vertex):
    D = {v: float('inf') for v in range(self.v)}
    D[start_vertex] = 0
    pq = PriorityQueue()
    init = (0, start_vertex)
    pq.put(init)
    while not pq.empty():
        (dist, current_vertex) = pq.get()
        self.visited.append(current_vertex)
        for neighbor in range(self.v):
            if self.edges[current_vertex][neighbor] != -1:
                distance = self.edges[current_vertex][neighbor]
                if neighbor not in self.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
    return D""",ast.unparse(funcDef))

    def testExtractInConditional(self):
        code = """def foo():
    if b: bar(x,y,a[0]+b)"""
        funcDef = ast.parse(code).body[0]
        changed = Refactor.extract(funcDef, ((2, 18), (2, 22)), "deref")
        self.assertTrue(changed)
        self.assertEqual(
            """def foo():
    if b:
        deref = a[0]
        bar(x, y, deref + b)""",ast.unparse(funcDef))

    def testAlreadyAVariable(self):
        funcDef = ast.parse(self.code).body[0]
        changed = Refactor.extract(funcDef, ((5, 13), (5, 28)), "init")
        self.assertFalse(changed)
        self.assertEqual("""def dijkstra(self, start_vertex):
    D = {v: float('inf') for v in range(self.v)}
    D[start_vertex] = 0
    pq = PriorityQueue()
    pq.put((0, start_vertex))
    while not pq.empty():
        (dist, current_vertex) = pq.get()
        self.visited.append(current_vertex)
        for neighbor in range(self.v):
            if self.edges[current_vertex][neighbor] != -1:
                distance = self.edges[current_vertex][neighbor]
                if neighbor not in self.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
    return D""", ast.unparse(funcDef))

    def testExtractBadRange(self):
        funcDef = ast.parse(self.code).body[0]
        changed = Refactor.extract(funcDef, ((5, 13), (5, 24)), "init")
        self.assertFalse(changed)
        self.assertEqual("""def dijkstra(self, start_vertex):
    D = {v: float('inf') for v in range(self.v)}
    D[start_vertex] = 0
    pq = PriorityQueue()
    pq.put((0, start_vertex))
    while not pq.empty():
        (dist, current_vertex) = pq.get()
        self.visited.append(current_vertex)
        for neighbor in range(self.v):
            if self.edges[current_vertex][neighbor] != -1:
                distance = self.edges[current_vertex][neighbor]
                if neighbor not in self.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
    return D""", ast.unparse(funcDef))


if __name__ == '__main__':
    unittest.main()
