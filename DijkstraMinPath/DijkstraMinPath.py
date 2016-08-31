global MINIMUM
MINIMUM = 999999


class Edge():
    """Defines and edge, with a length d and connected to two vertexes, v1 and v2
    v1 and v2 are just the indexes of a list with all vertexes
    """
    def __init__(self, v1, v2, d):
        self.v1 = v1
        self.v2 = v2
        self.d = d


class Vertex():
    """defines a vertex and some other properties for the Dijkstra algorithm
    .distance : distance from the current vertex to the
                initial vertex, which is user defined
    .unvisited: boolean flag for Dijkstra algorithm
    .nearest  : index of the nearest vertex to the current one.
                this is used to show the full path with minimum distance
                from the initical vertex to the target vertex
    .edges    : list with all edges connected to this vertex
    .otherVert: list of the vertex on the other side of the connected
                edges.
    """
    def __init__(self, distance, unvisited, nearest):
        self.distance = distance
        self.unvisited = unvisited
        self.nearest = nearest
        self.edges = []
        self.otherVert = []


def nextVertex(vertexes):
    """sub-function of the dijkstraGraph. returns the index of the next vertex to
    be worked by the algorithm, which is the unvisited vertex with the overall minimum
    distance from the initial vertex
    """
    min = MINIMUM
    for i, v in enumerate(vertexes):
        if v.unvisited and v.distance < min:
            min = v.distance
            imin = i
    return imin


def updateDistances(vertexes, edges, icurVertex):
    """sub-function of the dijkstraGraph for a given current vertex, goes through
    all its still unvisited connected vertexes, and check if the path through the current vertex
    is smaller than the path actually stored
    -> does not return anything since updates are done directly in the list of vertexes
    """
    for i, v in enumerate(vertexes[icurVertex].otherVert):
        if vertexes[v].unvisited:
            alt = (vertexes[icurVertex].distance +
                   edges[vertexes[icurVertex].edges[i]].d)
            if alt < vertexes[v].distance:
                vertexes[v].distance = alt
                vertexes[v].nearest = icurVertex


def dijkstraGraph(vertexes, edges, initialVertex, verbose=False):
    """main Dijkstra algorithm for min path finding for a given starting vertex, calculates the
    minimum distances to all the other vertexes. these minimum distances are saved in the vertexes
    themselves by accessing vertex[i].distance
    -> does not return anything since updates are done directly in the list of vertexes
    """
    # initial setup
    vertexes[initialVertex].distance = 0
    left = 1
    while left:
        if verbose: print(left)
        icur = nextVertex(vertexes)
        vertexes[icur].unvisited = False
        # check all neighbors and update distances
        updateDistances(vertexes, edges, icur)
        left = sum([_.unvisited for _ in vertexes])


if __name__ == '__main__':
    # MAIN

    # define the lengths of the edges and at
    # which vertex they are connected
    # !!!
    # NOTE see attached example.pdf for the graph of this example
    # !!!
    NumVertexes = 11
    MyEdges = [Edge(0, 1, 1), Edge(0, 2, 999), Edge(0, 3, 555), Edge(1, 4, 1),
               Edge(1, 5, 444), Edge(2, 5, 1), Edge(3, 5, 1), Edge(3, 6, 1),
               Edge(4, 7, 1), Edge(4, 5, 99), Edge(5, 8, 100), Edge(5, 6, 200),
               Edge(6, 9, 1), Edge(7, 10, 1), Edge(7, 8, 55), Edge(8, 10, 1),
               Edge(8, 9, 1), Edge(9, 10, 333)]

    # initialise the list with the vertexes, with a
    # high initial value for minimum distance (MINIMUM),
    # all marked as unvisited and nearest vertexes marked as -1
    MyVertexes = [Vertex(MINIMUM, True, 0) for _ in range(NumVertexes)]

    # loops through all the edges and mark at which
    # vertexes they are connected to.
    # also marks in each vertex what's the vertex
    # on the other side of each edge
    # for example:
    #   V4---E8---V2---E3---V7
    # vertex[2].edges=[3,8]
    # vertex[2].otherVert=[7,4]
    for i in range(len(MyEdges)):
        MyVertexes[MyEdges[i].v1].edges.append(i)
        MyVertexes[MyEdges[i].v1].otherVert.append(MyEdges[i].v2)
        MyVertexes[MyEdges[i].v2].edges.append(i)
        MyVertexes[MyEdges[i].v2].otherVert.append(MyEdges[i].v1)

    # calculate minimum distances to each vertex
    InitialVertex = 0
    dijkstraGraph(MyVertexes, MyEdges, InitialVertex, verbose=True)

    # get the minimum path from InitialVertex to TargetVertex
    TargetVertex = 2
    n = TargetVertex
    MinPath = [n]
    while n:
        n = MyVertexes[n].nearest
        MinPath.append(n)
    MinPath.reverse()

    # show results
    print("Minimum distance from vertex", InitialVertex, "to vertex ", end='')
    print(TargetVertex, "is", MyVertexes[TargetVertex].distance)
    print("The path for minimum distance is through vertexes:")
    print(MinPath)
