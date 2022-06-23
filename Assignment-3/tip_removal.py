#python 3
import sys
def explore(adj,x,stack,scc_count,count):
    #print("adj",adj)
    global used
    used[x]=1

    for i in adj[x]:
        if not used[i]:
                explore(adj,i,stack,scc_count,count)

    stack.append(x)
    scc_count[x]=count
    return

def dfs(adj,stack,scc_count,count):
    #write your code here
    global pre,post,res,used
    res=0
    order=[]
    pre=[0 for _ in range(len(adj))]
    post=[0 for _ in range(len(adj))]
    used=[0 for _ in range(len(adj))]
    for x in range(len(adj)):
        if not used[x]:
                explore(adj,x,stack,scc_count,count)
            #print("stack",stack)


def number_of_strongly_connected_components(adj,adj_r):
    #global stack
    result = 0
    comp=[]
    global pre
    global post,used
    used=[0 for _ in range(len(adj))]
    scc_count=[0 for _ in range(len(adj))]
    l=[0 for _ in range(len(adj))]
    stack=[]
    #post_use=[]
    #out=[]
    count=0
    #rev=dict()
    dfs(adj_r,stack,l,0)
    used=[0 for _ in range(len(adj))]
    #print(stack)
    while stack:
        lst=[]
        #print("stack",stack)
        value=stack.pop()
        #print("value",value)
        if not used[value]:
            #print("value",value)
            explore(adj,value,lst,scc_count,count)
            count+=1
            #print("lst",lst)
            comp.append(lst)
    #write your code here
    return comp,scc_count

def create_de_bruin(lst,n_kmers):
    kmer_lst=set()
    dict1=dict()
    dict2=dict()
    cnt=0
    for reads in lst:
        for i in range(len(reads)-n_kmers+1):
            kmer_lst.add(reads[i:i+n_kmers])

    kmer=sorted(kmer_lst)
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

        if len(adj_inv[i])==0: #NO inedges
            explore_in(adj,adj_inv,i)
    print(count)

def explore_out(adj,adj_inv,i):
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



#n=int(input())
lst=[]

for _ in range(1618):
    lst.append(input())
#lst=sys.stdin.readline
#lst=[x.strip() for x in lst]
adj,adj_inv=create_de_bruin(lst,15)
remove_tips(adj,adj_inv)
#comp,scc_count=number_of_strongly_connected_components(adj,adj_inv)


