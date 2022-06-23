#python3
import sys
from eulerian_cycle import *
def explore(adj,x,from_,to_,thresh,stack):
    #print("thresh",thresh)
    global count
    global pre
    global path_dict
    global used
    #print("x",x)
    if thresh==0:
        return
    if x in to_ and x!=from_ and thresh==1:
        #print("x",x)
        #print("from_",from_)
        #print("prev",pre)
        stack=[]
        t=x
        while t!=from_:
            stack.append(t)
            #print("stack1",stack)
            t=pre[t]
        stack.append(from_)

        path_dict[(from_,x)].append(stack)
        used[x]=0
        return

    for i in adj[x]:
        #if not used[i]:
            #print("i",i)
            pre[i]=x
            explore(adj,i,from_,to_,thresh-1,stack)
    #print("path_dict",path_dict)

    #stack.append(x)
    return
def dfs(adj,from_,nodes_to,thresh,stack):
    #write your code here
    global count
    count=0
    global pre,post,res,used
    res=0
    order=[]
    pre=[0 for _ in range(len(adj))]
    post=[0 for _ in range(len(adj))]
    used=[0 for _ in range(len(adj))]
    for x in adj[from_]:
        pre[x]=from_
        explore(adj,x,from_,nodes_to,thresh,stack)

def bubble_detect(adj,thresh):
    global path_dict

    nodes_from=[]
    nodes_to=[]
    stack=[]
    nodes_from+=[i for i in range(len(adj)) if len(adj[i])>1]
    nodes_to+=[i for i in range(len(adj_inv)) if len(adj_inv[i])>1]


    for j in nodes_from:
        for k in nodes_to:
            if j!=k:
                path_dict[(j,k)]=[]
    for j in nodes_from:
        dfs(adj,j,nodes_to,thresh,stack)

    bubble_count=0
    for key in path_dict:
        for i in range(len(path_dict[key])-1):
            for j in range(i+1,len(path_dict[key])):
                if len(set(path_dict[key][i]).intersection(set(path_dict[key][j])))==1:
                    bubble_count+=1

    return bubble_count
def cover_calc(paths,kmer_mul,mapper):
    n=len(paths)
    coverage=[0 for _ in range(n)]
    for i in range(n):
        lst=paths[i]
        mul=0
        edge_cnt=0
        for j,value in enumerate(lst[::-1]):
            child=lst[j]
            parent=lst[j+1]
            k_mer=mapper[parent+child[-1]]
            mul+=kmer_mul[k_mer]
            edge_cnt+=1
        coverage[i]=mul/edge_cnt
    return coverage

def remove_path(adj,adj_inv,key,coverage):
    m=len(coverage)

    for i in range(m):
        path=path_dict[key][i]
        for j in range(len(path)-1):
            child=path[j]
            parent=path[j+1]
            adj[parent].remove(child)
            adj_inv[child].remove(parent)


def bubble_removal(adj,adj_inv,kmer_mul,mapper,thresh):
    global path_dict
    path_dict=dict()
    bubble_cnt=bubble_detect(adj,thresh)
    if bubble_cnt==0:
        return

    for key,value in path_dict.items():
            coverage=cover_calc(value,kmer_mul,mapper)
            coverage.remove(max(coverage)) #Removing max coverage
            remove_path(adj,adj_inv,key,coverage) #Removing paths other than max coverage


def create_de_bruin(lst,n_kmers):
    kmer_lst=set()
    dict1=dict()
    dict2=dict()
    kmer_mul=dict()
    cnt=0
    for reads in lst:
        for i in range(len(reads)-n_kmers+1):
            sub_k=reads[i:i+n_kmers]
            if sub_k not in kmer_mul:
                kmer_mul[sub_k]=1
            else:
                kmer_mul[sub_k]+=1
            kmer_lst.add(sub_k)

    kmer=sorted(kmer_lst)
    #print("kmer_mul",kmer_mul)
    #print("kmer",kmer)
    for pattern in kmer:
        pref=pattern[:-1]
        suf=pattern[1:]
        if pref not in dict1:
            dict1[pref]=cnt
            cnt+=1
        if suf not in dict1:
            dict1[suf]=cnt
            cnt+=1
    #print("dict1",dict1)
    for key,value in dict1.items():
        dict2[value]=key
    adj=[[] for _ in range(len(dict1))]
    adj_inv=[[] for _ in range(len(dict1))]


    for pattern in kmer:
        pref=dict1[pattern[:-1]]
        suf=dict1[pattern[1:]]
        if pref!=suf:
            adj[pref].append(suf)
            adj_inv[suf].append(pref)


    return adj,adj_inv,kmer_mul,dict2
def remove_tips(adj,adj_inv):
    global count
    global removed
    count=0
    removed=[0 for _ in range(len(adj))]

    for i in range(len(adj)):
        if removed[i]:
            continue

        if len(adj[i])==0: #No outedges
            explore_out(adj,adj_inv,i)
            continue

        if len(adj_inv[i])==0: #NO inedges
            explore_in(adj,adj_inv,i)
            continue
    #print(count)

def explore_out(adj,adj_inv,i):
    #print("explore_out")
    #print("i",i)
    #print("adj",adj)
    #print("adj_inv",adj_inv)

    global count
    global removed
    if len(adj[i])!=0 or len(adj_inv[i])!=1:
        return
    removed[i]=1
    count+=1
    temp=adj_inv[i][0]
    adj[temp].remove(i)
    adj_inv[i].remove(temp)

    explore_out(adj,adj_inv,temp)


def explore_in(adj,adj_inv,i):
    #print("explore_in")
    #print("i",i)
    #print("adj",adj)
    #print("adj_inv",adj_inv)
    global count
    global removed
    if len(adj_inv[i])!=0 or len(adj[i])!=1:
        return
    removed[i]=1
    count+=1
    temp=adj[i][0]
    adj_inv[temp].remove(i)
    adj[i].remove(temp)

    explore_in(adj,adj_inv,temp)

def Eulerian_path(adj,mapper):

    final_path=[]
    if len(adj)==0:
        return

    for i in range(len(adj)):
        if len(adj[i])!=0:
            cur_path=[i]
            break


    while cur_path:
        value=cur_path[-1]
        if adj[value]:
            adj_vert=adj[value].pop()
            cur_path.append(adj_vert)
        else:
            final_path.append(mapper[cur_path.pop()])
    return final_path[::-1]

lst=sys.stdin.readlines()
lst=[x.strip() for x in lst]
adj,adj_inv,kmer_mul,str_int_map=create_de_bruin(lst,20)  #Create de-bruin graph
remove_tips(adj,adj_inv) #Remove tips
#print("adj",adj)
bubble_removal(adj,adj_inv,kmer_mul,str_int_map,20)
#x=is_Euleriancycle(adj,adj_inv)
#print("x",x)
final_path=Eulerian_path(adj,str_int_map)

#print("final_path",final_path)

k_univ=final_path[0]
path1=final_path[:-19]
for i in path1[1:]:
    k_univ=k_univ+i[-1]
print(k_univ)


