#python 3
import sys
#lst=[]
def prefix(pattern):
    return pattern[:-1]

def suffix(pattern):
    return pattern[1:]
def explore(adj,x,from_,to_,thresh,stack):
    #print("thresh",thresh)
    global count
    global pre
    global path_dict
    global used
    #print("x",x)
    if thresh==0:
        return
    if x in to_ and x!=from_ and thresh!=0:
        stack=[]
        t=x
        while t!=from_:
            stack.append(t)
            #print("stack1",stack)
            t=pre[t]
        stack.append(from_)

        path_dict[(from_,x)].append(stack)
        used[x]=0

    #print("adj",adj)

    #used[x]=1

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
    #print("stack",stack)

def read_data():
    global path_dict
    cnt=0
    path_dict=dict()
    nodes_from=[]
    nodes_to=[]
    stack=[]
    #lst=[]

    #print("lst",lst)
    #lst=sys.stdin.readline().split()
    #n_kmers=int(lst[0])
    #thresh=int(lst[1])

    lst=sys.stdin.readlines()
    lst=[x.strip() for x in lst]
    n_kmers=int(lst[0].split()[0])
    thresh=int(lst[0].split()[1])
    #for _ in range(1618):
    #    lst.append(input().split())
    create_de_bruin(lst,n_kmers)
    adj,adj_inv=create_de_bruin(lst,n_kmers)
    nodes_from+=[i for i in range(len(adj)) if len(adj[i])>1]
    nodes_to+=[i for i in range(len(adj_inv)) if len(adj_inv[i])>1]
    #print(nodes_from)
    #print(nodes_to)


    for j in nodes_from:
        for k in nodes_to:
            if j!=k:
                path_dict[(j,k)]=[]
                #print("j",j)
                #print("k",k)
    #            stack=[]
                #print("count",count)
    #for j in nodes_from:
    #    for k in nodes_to:
    #        if j!=k:
    #            if len(path_dict)==0 or (j,k) not in path_dict.keys():
    #               dfs(adj,j,k,thresh,stack)
    for j in nodes_from:
        dfs(adj,j,nodes_to,thresh,stack)

    print("path_dict",path_dict)
    #print(cnt)
    bubble_count=0
    for key in path_dict:
        for i in range(len(path_dict[key])-1):
            for j in range(i+1,len(path_dict[key])):
                if len(set(path_dict[key][i]).intersection(set(path_dict[key][j])))==1:
                    bubble_count+=1

    print(bubble_count)




def create_de_bruin(lst,n_kmers):
    kmer_lst=set()
    dict1=dict()
    dict2=dict()
    cnt=0
    for reads in lst[1:]:
        for i in range(len(reads)-n_kmers+1):
            kmer_lst.add(reads[i:i+n_kmers])

    kmer=sorted(kmer_lst)

    for pattern in kmer:
        pref=pattern[:-1]
        suf=pattern[1:]
        if pref not in dict1:
            dict1[pref]=cnt
            cnt+=1
        if suf not in dict1:
            dict1[suf]=cnt
            cnt+=1
    adj=[[] for _ in range(len(dict1))]
    adj_inv=[[] for _ in range(len(dict1))]

    #print("adj",adj)

    for pattern in kmer:
        pref=dict1[pattern[:-1]]
        suf=dict1[pattern[1:]]
        if pref!=suf:
            adj[pref].append(suf)
            adj_inv[suf].append(pref)

    #print("dict1",dict1)
    #print("kmer",kmer)
    #print("adj",adj)
    #print("adj_inv",adj_inv)

    return adj,adj_inv


read_data()
