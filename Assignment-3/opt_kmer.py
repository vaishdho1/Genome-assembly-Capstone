#python3
def prefix(value):
    return value[:-1]

def suffix(value):
    return value[1:]

def opt_k(n,nreads):
    k_mer=set()
    pref=set()
    suff=set()

    for x in nreads:
        for i in range(len(x)-n+1):
            k_mer.add(x[i:i+n])

    #print("kmer",sorted(k_mer))

    for k in k_mer:
        pref.add(k[:-1])
        suff.add(k[1:])
        #print(pref)
        #print(suff)
    sorted(pref)
    sorted(suff)
    return sorted(pref)==sorted(suff)

lst=[]
for i in range(25):
    lst.append(input())

length=len(lst[0])

for n in range(length,1,-1):
    if opt_k(n,lst):
        print(n)
        break

