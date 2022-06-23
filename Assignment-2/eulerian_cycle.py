#python3
'''
Finding whether a Eulerian graph exists and printing the path of the vertices
Checking whether a single strongly connected component exists by calling DFS once: if any vertex is not visited returns false
Uses Heirholzer's algorithm to find Eulerian path
'''
import sys
import threading
sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size

def previsit(v):
    global res
    global pre
    pre[v]=res
    res=res+1
    return
def postvisit(v):
    global res
    global post
    post[v]=res
    res=res+1
    return

def explore(adj,x):
    global used
    used[x]=1

    for i in adj[x]:
        if not used[i]:
            explore(adj,i)
    return

def dfs(adj):
    #write your code here
    global pre,post,res,used
    res=0
    order=[]
    pre=[0 for _ in range(len(adj))]
    post=[0 for _ in range(len(adj))]
    used=[0 for _ in range(len(adj))]
    for x in range(len(adj)):
        if not used[x]:
            explore(adj,x)
            #print("stack",stack)
    print("used",used)
    for x in range(len(adj)):
       if not used[x]:
           return False
    return True

def is_Euleriancycle(adj,adj_r):
    flag=0
    for i in range(len(adj)):
            if len(adj[i])!=len(adj_r[i]):
                return False
    if not dfs(adj):
        return False
    return True
def Eulerian_path(adj):
    cur_path=[0]
    final_path=[]
    if len(adj)==0:
        return

    while cur_path:
        value=cur_path[-1]
        if adj[value]:
            adj_vert=adj[value].pop()
            cur_path.append(adj_vert)
        else:
            final_path.append(cur_path.pop())
    return final_path[::-1]


def main():

    n,m=map(int,input().split())
    adj=[[] for _ in range(n)]
    adj_r=[[] for _ in range(n)]
    for _ in range(m):
        i,j=map(int,input().split())
        adj[i-1].append(j-1)
        adj_r[j-1].append(i-1)

    if is_Euleriancycle(adj,adj_r):
        path=Eulerian_path(adj)
        print(1)
        for x in path[:-1]:
            print(x+1,end=" ")
    else:
        print(0)



#threading.Thread(target=main).start()






