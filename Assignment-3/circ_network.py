# python3
import numpy as np
from collections import deque
class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]
        self.source=0
        self.sink=n-1
        self.demand=[]
        self.DD=0
        self.dv=[0 for _ in range(n)]
        self.to_=[0 for _ in range(n-1)]

        self.store=[-1 for _ in range(n)]

    def add_edge(self, from_, to, value):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        #print("from",from_)
        #print("to",to)




        forward_edge = Edge(from_, to, value)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)



    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count+2)
    #graph.demand=[]
    for _ in range(edge_count):
        u, v,demand,capacity = map(int, input().split())
        graph.add_edge(u , v ,capacity-demand)
        graph.demand.append(demand)
        #print("demand",demand)
        graph.dv[u]+=demand
        graph.dv[v]-=demand
    #print("graph",graph.from_)
    #print(graph.to_)
    graph.len=len(graph.edges)
    for x in range(1,vertex_count+1):
        if graph.dv[x]<0:
            graph.add_edge(0,x,-graph.dv[x])
        else:
            graph.add_edge(x,vertex_count+1,graph.dv[x])
            graph.DD+=graph.dv[x]
    #graph.add_edge(vertex_count+1,0,float('inf'))




    return graph

def path_graph(graph,edges,s):
        global prev
        global cap
        global prev_id
        Q=deque()
        dist=[float('inf') for _ in range(len(graph))]

        prev_id=[-1 for _ in range(len(graph))]

        dist[s]=0
        Q.append(s)
        while Q:
            #print("Q",Q)
            #print("dist",dist)
            q=Q.popleft()
            #print("graph[q]",graph)
            #print("q",q)
            for x in graph[q]:
                if edges[x].capacity>0:
                    #if x%2==0:
                        if dist[edges[x].v]==float('inf'):
                            Q.append(edges[x].v)
                            dist[edges[x].v]=dist[q]+1
                            prev[edges[x].v]=q
                            prev_id[edges[x].v]=x
                            #cap[edges[x].v]=edges[x].capacity
        return

def distance(adj,edges,s,t):
        global cap
        global prev_id
        #write your code here
        #print("s",s)
        #print("t",t)
        min_val=float('inf')
        global prev
        prev=[-1 for _ in range(len(adj))]
        #s=0
        path_graph(adj,edges,s)
        #print("prev",prev)
        #print("cap",cap)
        u=t
        lst=[]
        id_l=[]
        if prev[u]==-1:
            return lst,0
        else:
            while u!=s:
                #print("here")
                lst.append(u)
                min_val=min(min_val,edges[prev_id[u]].capacity)
                id_l.append(prev_id[u])
                #print("prev_id",prev_id[u])
                u=prev[u]

        lst.append(s)
        #print("min_val",min_val)
        #print("lst",lst)

        return id_l[::-1],min_val

def max_flow(graph, from_, to):
    flow = 0
    j=0
    res=[]

    while True:
        path,min_val=distance(graph.graph,graph.edges,from_, to)
        if len(path)==0:
            #print("flow",flow)
            #print("graph.from_",graph.from_)
            if flow!=graph.DD:
                return res
            #print(graph.len)
            for x in range(0,graph.len,2):
                        #print("x",x)
                        #print(graph.edges[x].u,graph.edges[x].v,graph.edges[x].flow)
                        res.append(graph.edges[x].flow)
            return res

        for id in path:
            graph.add_flow(id,min_val)
            graph.edges[id].capacity-=min_val
            graph.edges[id^1].capacity+=min_val
        flow+=min_val







    # your code goes here

if __name__ == '__main__':
    graph = read_data()
    #print("graph",graph.graph)
    #print("graph.store",graph.store)
    res=max_flow(graph, 0, graph.size() - 1)
    if len(res)==0:
        print("NO")
    else:
        print("YES")
        sum1=[res[i]+graph.demand[i] for i in range(len(res))]
        for x in sum1:
         print(x)






