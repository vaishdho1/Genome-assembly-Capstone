def assemble(lst,n):
    visited=[0 for _ in range(n)]
    adj=[dict() for _ in range(n)]
    graph=[[-float('inf')]*n for _ in range(n)]
    maxm=dict()
    string1=lst[0]
    new_string=[]
    new_string.append(string1)
    visited[0]=1
    index=0
    count=0
    for _ in range(n):
        #max_len=0
        #lst_co=[]
        #print("visited",visited)
        #count+=1
        pattern=lst[index]
        pattern_index=index
        maxm[pattern]=0
        #print("maxm[pattern]",_)
        for i in range(n):
            if visited[i]:
                continue

            for k in range(len(pattern)-maxm[pattern]):
                #if len(pattern)-k<12:
                #    break
                #print("k",k)
                if lst[i].startswith(pattern[k:],0,len(pattern)-k):
                    if len(pattern[k:])>maxm[pattern]:
                        maxm[pattern]=len(pattern[k:])
                        #print("pattern_index",pattern_index)
                        adj[pattern_index][i]=maxm[pattern]
                        graph[pattern_index][i]=maxm[pattern]
                        overlap=k
                        index=i
                        break

        if maxm[pattern]!=0:
            visited[index]=1
            new_string.append(lst[index][maxm[pattern]:])
    string1="".join(map(str,new_string))
    pattern=lst[index]
    text=new_string[0]
    for i in range(len(pattern)):
        if text.startswith(pattern[i:],0,len(pattern)-i):
            length=len(pattern[i:])
            break
    string1=string1[length:]

    return string1

if __name__=="__main__":
    lst=[]
    for _ in range(1618):
        x=input()
        if x not in lst:
            lst.append(x)
    print(assemble(lst,len(lst)))
