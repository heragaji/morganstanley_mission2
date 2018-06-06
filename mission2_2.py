import csv
import copy
dellist = lambda items, indexes: [item for index, item in enumerate(items) if index not in indexes]
max_sisan = 0

def bsk(N,BID,SID,KID,A,B,C,t): ##buy sell keep
    new_N = copy.deepcopy(N)
    if SID == 1:
        new_N[0] += A[t]*N[1]
        new_N[1] = 0
        new_N[4] +=[-1]
    elif SID == 2:
        new_N[0] += B[t]*N[2]
        new_N[2] = 0
        new_N[5] +=[-1]
    elif SID == 3:
        new_N[0] += C[t]*N[3]
        new_N[3] = 0
        new_N[6] +=[-1]
    elif SID == 12:
        new_N[0] += A[t]*N[1] + B[t]*N[2]
        new_N[1] = 0
        new_N[2] = 0
        new_N[4] +=[-1]
        new_N[5] +=[-1]
    elif SID == 13:
        new_N[0] += A[t]*N[1] + C[t]*N[3]
        new_N[1] = 0
        new_N[3] = 0
        new_N[4] +=[-1]
        new_N[6] +=[-1]
    elif SID == 23:
        new_N[0] += B[t]*N[2] + C[t]*N[3]
        new_N[2] = 0
        new_N[3] = 0
        new_N[5] +=[-1]
        new_N[6] +=[-1]
    elif SID == 123:
        new_N[0] += A[t]*N[1] + B[t]*N[2] + C[t]*N[3]
        new_N[1] = 0
        new_N[2] = 0
        new_N[3] = 0
        new_N[4] += [-1]
        new_N[5] +=[-1]
        new_N[6] +=[-1]
    if BID == 1:
        x = new_N[0]//A[t]
        new_N[0] -= A[t]*x
        new_N[1] = x
        new_N[4] += [1]
    elif BID == 2:
        y = new_N[0]//B[t]
        new_N[0] -= B[t]*y
        new_N[2] = y
        new_N[5] += [1]
    elif BID == 3:
        z = new_N[0]//C[t]
        new_N[0] -= C[t]*z
        new_N[3] = z
        new_N[6] += [1]
    if KID == 1:
        new_N[4] += [0]
    elif KID == 2:
        new_N[5] += [0]
    elif KID == 3:
        new_N[6] += [0]
    elif KID == 12:
        new_N[4] += [0]
        new_N[5] += [0]
    elif KID == 13:
        new_N[4] += [0]
        new_N[6] += [0]
    elif KID == 23:
        new_N[5] += [0]
        new_N[6] += [0]
    elif KID == 123:
        new_N[4] += [0]
        new_N[5] += [0]
        new_N[6] += [0]
    return new_N

def keep(N):
    return     [N[0],N[1],N[2],N[3],
        N[4]+[0],N[5]+[0],N[6]+[0]]

def check(T):
    global max_sisan
    global A,B,C
    if len(T) == 1:
        return T
    app = T.pop()
    t = len(app[4])-1
    app_sisan = app[0] + app[1]*A[t] + app[2]*B[t] + app[3]*C[t]
    if app[0] < 0 or app_sisan < max_sisan /2 :
        return T
    del_lst = []
    flag = 1
    for i,N in enumerate(T):
        if N[0] <= app[0] and N[1] <= app[1] and N[2] <= app[2] and N[3] <= app[3]:
            del_lst.append(i)
        if N[0] >= app[0] and N[1] >= app[1] and N[2] >= app[2] and N[3] >= app[3]:
            flag = 0
            break
    dT = dellist(T,del_lst)
    if flag == 1:
        dT.append(app)
        if max_sisan < app_sisan:
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
        [bsk(N_init,1,0,23,A,B,C,0)],
        [bsk(N_init,2,0,13,A,B,C,0)],
        [bsk(N_init,3,0,12,A,B,C,0)],
        [dummy],
        [dummy],
        [dummy],
        [dummy]]
        ]
    last = Time[len(Time)-1]
    for t in Time[1:last+1]:
        print(t)
        new_T = [[]]*8
        ## 0.0.0
        for N in T[t-1][0]:
            new_T[0].append(keep(N))
            new_T[0] = check(new_T[0])
            if(N[0]//A[t]!= 0):
                new_T[1].append(bsk(N,1,0,23,A,B,C,t))
                new_T[1] = check(new_T[1])
            if(N[0]//B[t]!= 0):
                new_T[2].append(bsk(N,2,0,13,A,B,C,t))
                new_T[2] = check(new_T[2])
            if(N[0]//C[t]!= 0):
                new_T[3].append(bsk(N,3,0,12,A,B,C,t))
                new_T[3] = check(new_T[3])
        ## 1.0.0
        for N in T[t-1][1]:
            new_T[0].append(bsk(N,0,1,23,A,B,C,t))
            new_T[0] = check(new_T[0])
            new_T[2].append(bsk(N,2,1,3,A,B,C,t))
            new_T[2] = check(new_T[2])
            new_T[3].append(bsk(N,3,1,2,A,B,C,t))
            new_T[3] = check(new_T[3])
            new_T[1].append(keep(N))
            new_T[1] = check(new_T[1])
            if(N[0]//B[t]!= 0):
                new_T[4].append(bsk(N,2,0,13,A,B,C,t))
                new_T[4] = check(new_T[4])
            if(N[0]//C[t]!= 0):
                new_T[5].append(bsk(N,3,0,12,A,B,C,t))
                new_T[5] = check(new_T[5]) 
            
        ## 0.1.0
        for N in T[t-1][2]:
            new_T[0].append(bsk(N,0,2,13,A,B,C,t))
            new_T[0] = check(new_T[0])
            new_T[1].append(bsk(N,1,2,3,A,B,C,t))
            new_T[1] = check(new_T[1])
            new_T[3].append(bsk(N,3,2,1,A,B,C,t))
            new_T[3] = check(new_T[3])
            new_T[2].append(keep(N))
            new_T[2] = check(new_T[2])
            if(N[0]//A[t]!=0):
                new_T[4].append(bsk(N,1,0,23,A,B,C,t))
                new_T[4] = check(new_T[4])
            if(N[0]//C[t]!=0):
                new_T[6].append(bsk(N,3,0,12,A,B,C,t))
                new_T[6] = check(new_T[6])

        ## 0.0.1
        for N in T[t-1][3]:
            new_T[0].append(bsk(N,0,3,12,A,B,C,t))
            new_T[0] = check(new_T[0])
            new_T[1].append(bsk(N,1,3,2,A,B,C,t))
            new_T[1] = check(new_T[1])
            new_T[2].append(bsk(N,2,3,1,A,B,C,t))
            new_T[2] = check(new_T[2])
            new_T[3].append(keep(N))
            new_T[3] = check(new_T[3])
            if(N[0]//A[t]!=0):
                new_T[5].append(bsk(N,1,0,23,A,B,C,t))
                new_T[5] = check(new_T[5])
            if(N[0]//B[t]!=0):
                new_T[6].append(bsk(N,2,0,13,A,B,C,t))
                new_T[6] = check(new_T[6])
        ## 1.1.0
        for N in T[t-1][4]:
            new_T[1].append(bsk(N,0,2,13,A,B,C,t))
            new_T[1] = check(new_T[1])
            new_T[5].append(bsk(N,3,2,1,A,B,C,t))
            new_T[5] = check(new_T[5])
            new_T[2].append(bsk(N,0,1,23,A,B,C,t))
            new_T[2] = check(new_T[2])
            new_T[6].append(bsk(N,3,1,2,A,B,C,t))
            new_T[6] = check(new_T[6])
            new_T[0].append(bsk(N,0,12,3,A,B,C,t))
            new_T[0] = check(new_T[0])
            new_T[3].append(bsk(N,3,12,0,A,B,C,t))
            new_T[3] = check(new_T[3])            
            new_T[4].append(keep(N))
            new_T[4] = check(new_T[4])
            if(N[0]//C[t]!= 0):
                new_T[7].append(bsk(N,3,0,12,A,B,C,t))
                new_T[7] = check(new_T[7])

            
        ## 1.0.1
        for N in T[t-1][5]:
            new_T[1].append(bsk(N,0,3,12,A,B,C,t))
            new_T[1] = check(new_T[1])
            new_T[4].append(bsk(N,2,3,1,A,B,C,t))
            new_T[4] = check(new_T[4])
            new_T[3].append(bsk(N,0,1,23,A,B,C,t))
            new_T[3] = check(new_T[3])
            new_T[6].append(bsk(N,2,1,3,A,B,C,t))
            new_T[6] = check(new_T[6])
            new_T[0].append(bsk(N,0,13,2,A,B,C,t))
            new_T[0] = check(new_T[0])
            new_T[2].append(bsk(N,2,13,0,A,B,C,t))
            new_T[2] = check(new_T[2])
            new_T[5].append(keep(N))
            new_T[5] = check(new_T[5])
            if(N[0]//B[t]!= 0):
                new_T[7].append(bsk(N,2,0,13,A,B,C,t))
                new_T[7] = check(new_T[7])
        ## 0.1.1
        for N in T[t-1][6]:
            new_T[2].append(bsk(N,0,3,12,A,B,C,t))
            new_T[2] = check(new_T[2])
            new_T[4].append(bsk(N,1,3,2,A,B,C,t))
            new_T[4] = check(new_T[4])
            new_T[3].append(bsk(N,0,2,13,A,B,C,t))
            new_T[3] = check(new_T[3])
            new_T[5].append(bsk(N,1,2,3,A,B,C,t))
            new_T[5] = check(new_T[5])
            new_T[0].append(bsk(N,0,23,1,A,B,C,t))
            new_T[0] = check(new_T[0])
            new_T[1].append(bsk(N,1,23,0,A,B,C,t))
            new_T[1] = check(new_T[1])
            new_T[6].append(keep(N))
            new_T[6] = check(new_T[6])
            if(N[0]//A[t]!=0):
                new_T[7].append(bsk(N,1,0,23,A,B,C,t))
                new_T[7] = check(new_T[7])
        ## 1.1.1
        for N in T[t-1][7]:
            new_T[4].append(bsk(N,0,3,12,A,B,C,t))
            new_T[4] = check(new_T[4])
            new_T[5].append(bsk(N,0,2,13,A,B,C,t))
            new_T[5] = check(new_T[5])
            new_T[6].append(bsk(N,0,1,23,A,B,C,t))
            new_T[6] = check(new_T[6])
            new_T[3].append(bsk(N,0,12,3,A,B,C,t))
            new_T[3] = check(new_T[3])
            new_T[2].append(bsk(N,0,13,2,A,B,C,t))
            new_T[2] = check(new_T[2])
            new_T[1].append(bsk(N,0,23,1,A,B,C,t))
            new_T[1] = check(new_T[1])
            new_T[0].append(bsk(N,0,123,0,A,B,C,t))
            new_T[0] = check(new_T[0])
            new_T[7].append(keep(N))
            new_T[7] = check(new_T[7])
        T.append(new_T)
    max_N = []
    max_m = 0
    for Nodes in T[last]:
        for N in Nodes:
            m = N[0] + N[1]*A[last] + N[2]*B[last] + N[3]*C[last]
            if  max_m < m:
                max_N = N
                max_m = m
    print(max_m)
    print(max_N)
    X = max_N[4]
    Y = max_N[5]
    Z = max_N[6]
    for t in Time[0:last+1]:
        if X[t] == -1:
            print("sell(0,"+str(t)+")")
        if Y[t] == -1:
            print("sell(1,"+str(t)+")")
        if Z[t] == -1:
            print("sell(2,"+str(t)+")")
        if X[t] == 1:
            print("buy(0,"+str(t)+")")
        if Y[t] == 1:
            print("buy(1,"+str(t)+")")
        if Z[t] == 1:
            print("buy(2,"+str(t)+")")
