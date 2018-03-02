
# coding: utf-8


from sklearn.cluster import KMeans
import numpy as np

files = ['b_should_be_easy', 'c_no_hurry', 'd_metropolis', 'e_high_bonus']

for fff in files[2:3]:
    if fff == "c_no_hurry":
        continue
    if True:
        #fff = 'b_should_be_easy'
        fname = fff+'.in'
        with open(fname) as f:
            content = f.readlines()
        content = [x.strip().lower() for x in content] 

        R,C,F,N,B,T = [int(i) for i in content[0].split(' ')]
        print('bonus',B,'cars',F,'Rides',R,'time',T)

        rides = [[int(i) for i in j.split(' ')]+[q] for q,j in enumerate(content[1:])]
       
        ridesS = sorted(rides,key=lambda tup: tup[4])#4-5

        X = np.array(rides)[:,:4]
        X = X.reshape((-1,2))
    
    for k in range(1,3,1):
        print('run',fff,k)
        kmeans = KMeans(n_clusters=k, random_state=0).fit(X)

        cl = kmeans.predict(np.array([0,0]))[0]
        cars = [[0,0,0,i,cl] for i in range(F)]
        out = {i:[] for i in range(F)}

        q = 0
        nr = 5
        total = 0
        best = B*R
        for a,b,x,y,s,f,rid in ridesS:
            q+=1
            cl = kmeans.predict(np.array([a,b]))[0]
            dis = abs(b-y)+abs(a-x)
            best+=dis
            last = f-dis
            pos = []
            for i,[xx,yy,tt,cid,clc] in enumerate(cars):
                d = (abs(b-yy)+abs(a-xx))
                if (clc==cl or q <= F) and d+tt<last:
                    pos.append([i,max(d+tt,s)])
                if xx==0 and yy==0 and d+tt<last:
                    #pos = []
                    pos.append([i,max(d+tt,s)])
                    if  np.random.rand()<-0.2:
                        break
                if len(pos)>nr and  np.random.rand()<0.8 :
                    pos = sorted(pos,key=lambda tup: tup[1])[:nr]
            if len(pos)>0:
                r = 0
                if len(pos)>1 and np.random.rand()<0.1:
                    r = np.random.randint(len(pos))
                if max(pos[r][1],s)+dis<=T:
                    if pos[r][1]<=s:
                        total+=B
                    total+= dis
                p = pos[r][0]
                out[cars[p][3]].append(rid)
                cars[p][:3] = [x,y,pos[r][1]+dis]
                cle = kmeans.predict(np.array([x,y]))[0]
                cars[p][4] = cle

        print('total:',total,'from',best)
        f = open('11'+fff+'-t:'+str(total)+"-k-"+str(k)+'.out','w')
        for (u,v) in out.items(): 
            f.write(str(len(v))+' ')
            for i in v:
                f.write(str(i)+' ')
            f.write('\n')
        f.close()
        print('done')




