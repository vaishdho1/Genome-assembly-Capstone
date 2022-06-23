#python3
import itertools
def prefix(pattern):
    return pattern[:-1]

def suffix(pattern):
    return pattern[1:]


def generate_kmers(k):
    l=['0','1']
    lst=["".join(ele) for ele in itertools.product(l,repeat=k)]
    #print("lst",lst)
    return lst
def Eulerian_path(adj):
    #print("adj",adj)
    cur_path=[list(adj.keys())[0]]
    final_path=[]
    if len(adj)==0:
        return

    while cur_path:
        value=cur_path[-1]
        if adj[value]:
            adj_vert=adj[value][0]
            cur_path.append(adj_vert)
            adj[value].remove(adj_vert)
        else:
            final_path.append(cur_path.pop())
    return final_path[::-1]

def create_euler_graph(lst,k):
    adj=dict()

    for pattern in lst:
        adj[prefix(pattern)]=[]

    for pattern in lst:
        adj[prefix(pattern)].append(suffix(pattern))
    path=Eulerian_path(adj)
    k_univ=path[0]
    path1=path[:-(k-1)]
    for i in path1[1:]:
        k_univ=k_univ+i[-1]
    print(k_univ)

    return


k=int(input())
lst=generate_kmers(k)
create_euler_graph(lst,k)



