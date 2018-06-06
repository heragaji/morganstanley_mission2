import csv
# class Node:
#     def __init__(self,s,m,x,y,z,alg,blg,clg):
#         self.s = s
#         self.m = m
#         self.x = x
#         self.y = y
#         self.z = z
#         self.alg = alg
#         self.blg = blg
#         self.clg = clg
dellist = lambda items, indexes: [item for index, item in enumerate(items) if index not in indexes]
max_sisan = 0
def buy(N,ID,A,B,C,t):
    if ID == 1:
        return [N[0]-A[t]*(N[0]//A[t]),N[0]//A[t],N[2],N[3],
        N[4]+[1],N[5]+[0],N[6]+[0]]
    if ID == 2:
        return [N[0]-B[t]*(N[0]//B[t]),N[1],N[0]//B[t],N[3],
        N[4]+[0],N[5]+[1],N[6]+[0]]
    if ID == 3:
        return [N[0]-C[t]*(N[0]//C[t]),N[1],N[2],N[0]//C[t],
        N[4]+[0],N[5]+[0],N[6]+[1]]

def sell(N,ID,A,B,C,t):
    if ID == 1:
        return [N[0]+A[t]*N[1],0,N[2],N[3],
        N[4]+[-1],N[5]+[0],N[6]+[0]]
    if ID == 2:
        return [N[0]+B[t]*N[2],N[1],0,N[3],
        N[4]+[0],N[5]+[-1],N[6]+[0]]
    if ID == 3:
        return [N[0]+C[t]*N[3],N[1],N[2],0,
        N[4]+[0],N[5]+[0],N[6]+[-1]]
    if ID == 12:
        return [N[0]+A[t]*N[1] + B[t]*N[2],0,0,N[3],
        N[4]+[-1],N[5]+[-1],N[6]+[0]]
    if ID == 13:
        return [N[0]+A[t]*N[1] + C[t]*N[3],0,N[2],0,
        N[4]+[-1],N[5]+[-1],N[6]+[0]]
    if ID == 23:
        return [N[0]+C[t]*N[3] + B[t]*N[2],N[1],0,0,
        N[4]+[0],N[5]+[-1],N[6]+[-1]]
    if ID == 123:
        return [N[0]+A[t]*N[1] + B[t]*N[2] + C[t]*N[3] ,0,0,0,
        N[4]+[-1],N[5]+[-1],N[6]+[-1]]

def keep(N):
    return     [N[0],N[1],N[2],N[3],
        N[4]+[0],N[5]+[0],N[6]+[0]]

def check(T):
    global max_sisan
    global A,B,C
    if len(T) == 1:
        return T
    app = T.pop()
    app_sisan = app[0] + app[1]*A[last] + app[2]*B[last] + app[3]+C[last]
    if app[0] < 0 and app_sisan < max_sisan / 2:
        return
    del_lst = []
    flag = 1
    for i,N in enumerate(T):
        if N[0] <= app[0] and N[1] <= app[1] and N[2] <= app[2] and N[3] <= app[3]:
            del_lst.append(i)
        if N[0] > app[0] and N[1] > app[1] and N[2] > app[2] and N[3] > app[3]:
            flag = 0
            break
    dT = dellist(T,del_lst)
    if flag == 1:
        dT.append(app)
        if app_sisan > max_sisan:
            max_sisan = app_sisan
    dT.sort(key = lambda x:x[0])
    return dT



        
with open('mission2.csv','r') as f:
    m_init = 10000
    reader = csv.reader(f)
    header = next(reader)
    lst = list(reader)
    Time = [int(x[0]) for x in lst]
    A = [int(x[1]) for x in lst]
    B = [int(x[2]) for x in lst]
    C = [int(x[3]) for x in lst]
    N_init = [m_init,0,0,0,[],[],[]]
    dummy = [0,0,0,0,[],[],[]]
    T = [
        [[keep(N_init)],
        [buy(N_init,1,A,B,C,0)],
        [buy(N_init,2,A,B,C,0)],
        [buy(N_init,3,A,B,C,0)],
        [dummy],
        [dummy],
        [dummy],
        [dummy]]
        ]
    last = Time[len(Time)-1]
    for t in Time[1:last+1]:
        print(t)
        new_T = [[],[],[],[],[],[],[],[]]
        ## 0.0.0
        for N in T[t-1][0]:
            new_T[0].append(keep(N))
            new_T[0] = check(new_T[0])
            if(N[0]//A[t]!= 0):
                new_T[1].append(buy(N,1,A,B,C,t))
                new_T[1] = check(new_T[1])
            if(N[0]//B[t]!= 0):
                new_T[2].append(buy(N,2,A,B,C,t))
                new_T[2] = check(new_T[2])
            if(N[0]//C[t]!= 0):
                new_T[3].append(buy(N,3,A,B,C,t))
                new_T[3] = check(new_T[3])
        ## 1.0.0
        for N in T[t-1][1]:
            new_T[0].append(sell(N,1,A,B,C,t))
            new_T[1].append(keep(N))
            if(N[0]//B[t]!= 0):
                new_T[4].append(buy(N,2,A,B,C,t))
                new_T[4] = check(new_T[4])
            if(N[0]//C[t]!= 0):
                new_T[5].append(buy(N,3,A,B,C,t))
                new_T[5] = check(new_T[5])
            new_T[0] = check(new_T[0])
            new_T[1] = check(new_T[1])
        ## 0.1.0
        for N in T[t-1][2]:
            new_T[0].append(sell(N,2,A,B,C,t))
            new_T[2].append(keep(N))
            if(N[0]//A[t]!=0):
                new_T[4].append(buy(N,1,A,B,C,t))
                new_T[4] = check(new_T[4])
            if(N[0]//C[t]!=0):
                new_T[6].append(buy(N,3,A,B,C,t))
                new_T[6] = check(new_T[6])
            new_T[0] = check(new_T[0])
            new_T[2] = check(new_T[2])
        ## 0.0.1
        for N in T[t-1][3]:
            new_T[0].append(sell(N,3,A,B,C,t))
            new_T[3].append(keep(N))
            if(N[0]//A[t]!=0):
                new_T[5].append(buy(N,1,A,B,C,t))
                new_T[5] = check(new_T[5])
            if(N[0]//B[t]!=0):
                new_T[6].append(buy(N,2,A,B,C,t))
                new_T[6] = check(new_T[6])
            new_T[0] = check(new_T[0])
            new_T[3] = check(new_T[3])
        ## 1.1.0
        for N in T[t-1][4]:
            new_T[1].append(sell(N,2,A,B,C,t))
            new_T[2].append(sell(N,1,A,B,C,t))
            new_T[4].append(keep(N))
            if(N[0]//C[t]!= 0):
                new_T[7].append(buy(N,3,A,B,C,t))
                new_T[7] = check(new_T[7])
            new_T[1] = check(new_T[1])
            new_T[2] = check(new_T[2])
            new_T[4] = check(new_T[4])
            new_T[0].append(sell(N,12,A,B,C,t))
            new_T[0] = check(new_T[0])
        ## 1.0.1
        for N in T[t-1][5]:
            new_T[1].append(sell(N,3,A,B,C,t))
            new_T[3].append(sell(N,1,A,B,C,t))
            new_T[5].append(keep(N))
            if(N[0]//B[t]!= 0):
                new_T[7].append(buy(N,2,A,B,C,t))
                new_T[7] = check(new_T[7])
            new_T[1] = check(new_T[1])
            new_T[3] = check(new_T[3])
            new_T[5] = check(new_T[5])
            new_T[0].append(sell(N,13,A,B,C,t))
            new_T[0] = check(new_T[0])
        ## 0.1.1
        for N in T[t-1][6]:
            new_T[2].append(sell(N,3,A,B,C,t))
            new_T[3].append(sell(N,2,A,B,C,t))
            new_T[6].append(keep(N))
            if(N[0]//A[t]!=0):
                new_T[7].append(buy(N,1,A,B,C,t))
                new_T[7] = check(new_T[7])
            new_T[2] = check(new_T[2])
            new_T[3] = check(new_T[3])
            new_T[6] = check(new_T[6])
            new_T[0].append(sell(N,23,A,B,C,t))
            new_T[0] = check(new_T[0])
        ## 1.1.1
        for N in T[t-1][7]:
            new_T[4].append(sell(N,3,A,B,C,t))
            new_T[5].append(sell(N,2,A,B,C,t))
            new_T[6].append(sell(N,1,A,B,C,t))
            new_T[7].append(keep(N))
            new_T[4] = check(new_T[4])
            new_T[5] = check(new_T[5])
            new_T[6] = check(new_T[6])
            new_T[7] = check(new_T[7])
            new_T[3].append(sell(N,12,A,B,C,t))
            new_T[3] = check(new_T[3])
            new_T[2].append(sell(N,13,A,B,C,t))
            new_T[2] = check(new_T[2])
            new_T[1].append(sell(N,23,A,B,C,t))
            new_T[1] = check(new_T[1])
            new_T[0].append(sell(N,123,A,B,C,t))
            new_T[0] = check(new_T[0])
        T.append(new_T)
    max_N = []
    max_s = 0
    for Nodes in T[last]:
        for N in Nodes:
            s = N[0] + N[1]*A[last] + N[2]*B[last] + N[3]+C[last]
            if  max_s < s:
                max_N = N
                max_s = s
    print(max_s)
    print(max_N)
    X = max_N[4]
    Y = max_N[5]
    Z = max_N[6]
    for i,x in enumerate(X):
        if x == 1:
            print("buy(0,"+str(i)+")")
        if x == -1:
            print("sell(0,"+str(i)+")")

    for i,x in enumerate(Y):
        if x == 1:
            print("buy(1,"+str(i)+")")
        if x == -1:
            print("sell(1,"+str(i)+")")

    for i,x in enumerate(Z):
        if x == 1:
            print("buy(2,"+str(i)+")")
        if x == -1:
            print("sell(2,"+str(i)+")")