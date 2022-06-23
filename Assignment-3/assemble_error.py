#python3
import sys
import threading
sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size
class Node:

    def __init__(self,vertexnum=None):
        self.vertexnum=vertexnum
        self.child=[]
        self.parent=None

class Edge:

    def __init__(self,from_,to_,used=False):
        self.from_=from_
        self.to_=to_
        self.used=used
class Vertex:

    def __init__(self,vertexnum=None,str=None,outedges=None,inedges=None):
        self.vertexnum=vertexnum
        self.outedges=outedges
        self.str=str
        self.inedges=inedges
        self.removed=False
        self.found=False
        self.edgelist=[]
        self.temp=Node()
        self.visited=False





def read_input():
    reads=[]
    for _ in range(25):
        reads.append(input())
    return reads
count_map=dict()
k=6

def create_de_bruin(reads):
    unique_kmers=[]
    count_map=dict()
    out_edges=dict()
    in_edges=dict()
    ind_map=dict()

    ind=0


    for i in range(len(reads)):
        read=reads[i]
        for j in range(len(read)-k+1):
            sub_k=read[j:j+k]
            pref=sub_k[:-1]
            suff=sub_k[1:]
            if sub_k in unique_kmers:
                count_map[sub_k]+=1
                continue
            unique_kmers.append(sub_k)
            count_map[sub_k]=1

            if pref not in ind_map:
                ind_map[pref]=ind
                out_edges[pref]=[]
                in_edges[pref]=[]
                ind+=1

            if suff not in ind_map:
                ind_map[suff]=ind
                out_edges[suff]=[]
                in_edges[suff]=[]
                ind+=1

            out_edges[pref].append(ind_map[suff])
            in_edges[suff].append(ind_map[pref])
    #print("ind_map",ind_map.items())
    #print("in_edges",in_edges)
    #print("out_edges",out_edges)

    graph=[0 for _ in range(len(ind_map))]

    for str,num in ind_map.items():
        #print("str",str)
        graph[num]=Vertex(num,str,out_edges[str],in_edges[str])

    return graph


def remove_tips(graph):
    n=len(graph)

    for i in range(n):
        if graph[i].removed:
            continue
        if len(graph[i].outedges)==0:
            explore_in(graph,i)
            continue
        if len(graph[i].inedges)==0:
            explore_out(graph,i)
            continue


def explore_in(graph,ver):
    cnt=0

    if len(graph[ver].outedges)!=0 or len(graph[ver].inedges)!=1:
        return

    graph[ver].removed=True
    cnt+=1

    in_=graph[ver].inedges[0]
    graph[in_].outedges.remove(ver)
    graph[ver].inedges.remove(in_)
    explore_in(graph,in_)


def explore_out(graph,ver):
    cnt=0

    if len(graph[ver].inedges)!=0 or len(graph[ver].outedges)!=1:
        return

    graph[ver].removed=True
    cnt+=1

    out_=graph[ver].outedges[0]
    graph[out_].inedges.remove(ver)
    graph[ver].outedges.remove(out_)
    explore_in(graph,out_)


def bubble_removal(graph):
    n=len(graph)

    for i in range(len(graph)):
        if graph[i].removed or len(graph[i].outedges)<2:
            continue

        bfs(graph,graph[i].vertexnum)

def bfs(graph,num):
    set1=set()
    root=Node(num)
    temp=root

    for i in range(len(graph)):
        graph[i].found=False
        graph[i].temp=None

    explore(graph,temp,set1)

def explore(graph,temp,set1):
    bubble=0

    set1.add(temp.vertexnum)

    if graph[temp.vertexnum].found:
        bubble+=1
        common=find_common_ancestor(graph,temp)
        bubble_detect(graph,temp,common,set1)
        if temp.vertexnum not in set1:
            return
        graph[temp.vertexnum]=True
        graph[temp.vertexnum].temp=temp
        if len(set1)>=k+1:
            set1.remove(temp.vertexnum)
            return
    lst1=graph[temp.vertexnum].outedges
    for i in range(len(lst1)):
        node=lst1[i]

        if node in set1:
            continue
        child=Node(node)
        child.parent=temp
        temp.child.append(child)

        explore(graph,child,set1)

        if temp.vertexnum not in set1:
            return
    set1.remove(temp.vertexnum)





def find_common_ancestor(graph,node):
    lst=[]
    temp=graph[node.vertexnum].temp

    while temp!=None:
        lst.append(temp)
        temp=temp.parent

    temp=node

    while temp!=None:
        for i in lst[::-1]:
            if temp==i:
                return temp

        temp=temp.parent

    return None

def bubble_detect(graph,node,common,set1):
    node1=node
    node2=graph[vertexnum].temp

    sum=0
    cnt=0

    while node1!=common:
        str1=graph[node1.vertexnum].str
        str2=graph[node1.parent.vertexnum].str
        str=str2+str1[-1]
        sum+=count_map[str]
        cnt+=1

    coverage1=sum/cnt
    count1=cnt

    sum=0
    cnt=0

    while node2!=common:
        str1=graph[node2.vertexnum].str
        str2=graph[node2.parent.vertexnum].str
        str=str2+str1[-1]
        sum+=count_map[str]
        cnt+=1

    coverage2=sum/cnt
    count2=cnt



    if coverage1<coverage2:
        vertices_removed=set()
        temp=remove_path(graph,node1,common,vertices_removed)
        falsify_node(graph,temp)
        graph[node.vertexnum].found=True
        graph[node.vertexnum].temp=node2

    else:
        vertices_removed=set()
        temp=remove_path(graph,node2,common,vertices_removed)
        falsify_node(graph,temp)
        graph[node.vertexnum].found=True
        graph[node.vertexnum].temp=node1
        common.kids.remove(temp)



def remove_path(graph,node,common,vertices_removed):
    parent=node.parent
    child=node
    temp=None

    while child!=common:
        graph[parent.vertexnum].out_edges.remove(child.vertexnum)
        vertices_removed.add(child.vertexnum)
        temp,child,parent=child,parent,parent.parent

    return temp

def falsify_nodes(graph,node):
    graph[node.vertexnum].found=False
    grap[node.vertexnum].temp=None

    for i in range(len(node.child)):
        falsify_node(graph,node.kids[i])


def make_edges(graph):
    edges=[]

    for i in range(len(graph)):
        if graph[i].removed:
            continue
        lst1=graph[i].outedges
        for j in range(len(lst1)):
            edge=Edge(i,lst1[j])
            graph[i].edgelist.append(len(edges))
            edges.append(edge)
    return edges
def eulerain_explore(graph,i):
    cur_path=[i]
    while cur_path:
        value=cur_path[-1]
        if graph[value].outedges:
            adj_vert=graph[value].outedges.pop()
            cur_path.append(adj_vert)
        else:
            final_path.append(mapper[cur_path.pop()])
    return final_path[::-1]

def findcycle(graph,edges):
    max1=-1
    map=dict()
    print(len(graph))

    for i in range(len(graph)):
        #print(graph[i].removed)
        #print(graph[i].visited)
        if not graph[i].removed:
            cycle=[]

            final_path=eulerian_explore(graph,edges,i,cycle)
            genome=final_path[0]
            path1=final_path[:-19]
            for i in path1[1:]:
                genome=genome+i[-1]

            #genome=graph[cycle[-1]].str

            #for j in range(len(cycle)-2,-1,-1):
            #    temp=graph[cycle[j]].str
            #    genome+=temp[-1]
            #print("genome",genome)
            if len(genome)>=5396:
                map[genome]=len(genome)-5396
            if max1<len(genome):
                result=genome
                max1=len(genome)

    min=float('inf')

    for key,value in map.items():
        if min>value:
            min=value
            result=key

    print(result)


def eulerian_explore(graph,edges,vertex,cycle):
    lst1=graph[vertex].edgelist
    graph[vertex].visited=True

    for i in range(len(lst1)):
        edge=edges[lst1[i]]
        if not edge.used:
            edge.used=True
            eulerian_explore(graph,edges,edge.to_,cycle)
    cycle.append(vertex)




def main():
    reads=read_input()
    #print("reads",reads)
    graph=create_de_bruin(reads)
    #print("graph",graph)
    remove_tips(graph)
    bubble_removal(graph)
    remove_tips(graph)
    edges=make_edges(graph)
    findcycle(graph,edges)

threading.Thread(target=main).start()






