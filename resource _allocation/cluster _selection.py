import numpy as np
import matplotlib.pyplot as plt
import pylab
from pylab import *

WORKERNUM= 90
FIXEDREWARDS=80
OWNERNUM=10
CLUSTERNUM=3
CMPCOST=0.1
LEARNINGRATE=0.001
TMAX=500

m1workersam=80
m2workersam=100
m3workersam=160
# y=np.random.uniform(80,1600,WORKERNUM)
# x = np.arange(0, WORKERNUM, 1)
# #生成worker sample 的平均分布
#
# y=sort(y)
# m1=y[0:30]
# m2=y[30:60]
# m3=y[60:90]
# #分类
#
# m1workersam=np.mean(m1)
# m2workersam=np.mean(m2)
# m3workersam=np.mean(m3)
#
# plot(m1,'r.')
# plot(m2,'b.')
# plot(m3,'g.')
# show()

# INDEX = np.zeros((WORKERNUM,CLUSTERNUM))
# for i in range(90):
#     j=int(np.random.uniform(1,4,1)[0])
#     INDEX[i][j-1]=1
#初始随机分配

# def countworker(m,j):
#     num=0
#     if m=="m1":
#         for i in range(30):
#             if INDEX[i][j]==1:
#                 num=num+1
#     if m=="m2":
#         for i in range(60)[30:60]:
#             if INDEX[i][j]==1:
#                 num=num+1
#     if m == "m3":
#         for i in range(90)[60:90]:
#             if INDEX[i][j] == 1:
#                 num = num + 1
#     return num

class worker(object):

    def __init__(self,samplenum,tag):
        self.samplenum=samplenum
        self.tag=tag

    # def classify(self):
    #     if y[0]<= self.samplenum< y[30]:
    #         tag="m1"
    #     elif y[30]<= self.samplenum< y[60]:
    #         tag="m2"
    #     else :
    #         tag="m3"


# workers=[]
# for i in range(len(y)):
#     a= worker(y[i],"")
#     a.classify()
#     workers.append(a)


class cluster(object):
    def __init__(self,rewardpool,m1num,m2num,m3num,congestion):
        self.rewardpool=rewardpool
        self.m1num = m1num
        self.m2num = m2num
        self.m3num = m3num
        self.congestion=congestion
    def clustersample(self):
        return self.m1num * m1workersam + self.m2num * m2workersam + self.m3num * m3workersam
    def population(self):
        return self.m1num+self.m2num+self.m3num

cluster1=cluster(int(np.random.uniform(100,300,1)[0]),10,10,10,int(np.random.uniform(10,20,1)[0]))
cluster2=cluster(int(np.random.uniform(100,300,1)[0]),10,10,10,int(np.random.uniform(10,20,1)[0]))
cluster3=cluster(int(np.random.uniform(100,300,1)[0]),10,10,10,int(np.random.uniform(10,20,1)[0]))
#计算毛收益



def pmj(m,cluster):
    if m=="m1":
        mj=cluster.m1num*m1workersam
    elif m=="m2":
        mj=cluster.m2num*m2workersam
    else:
        mj=cluster.m3num*m3workersam

    pmj=cluster.rewardpool*mj/cluster.clustersample() + FIXEDREWARDS
    # print("pmj",pmj)
    return pmj
#计算 通信损耗
def comcost(cluster):
    a=cluster.m1num/30 +cluster.m2num/30 +cluster.m3num/30
    # print("comcost",cluster.congestion*a*a)
    return cluster.congestion*a*a
#计算净收益
def utility(cluster,m):
    umj=pmj(m,cluster)-comcost(cluster)-CMPCOST
    # print("umj",umj)
    return umj
#计算平均净收益
def avgutility(m):
    if m=="m1":
       avg= cluster1.m1num/30 * utility(cluster1,"m1")+cluster2.m1num/30 * utility(cluster2,"m1")+cluster3.m1num/30 * utility(cluster3,"m1")
    elif m=="m2" :
        avg = cluster1.m2num / 30 * utility(cluster1, "m2") + cluster2.m2num / 30 * utility(cluster2,"m2") + cluster3.m2num / 30 * utility(cluster3, "m2")
    else :
        avg = cluster1.m3num / 30 * utility(cluster1, "m3") + cluster2.m3num / 30 * utility(cluster2,"m3") + cluster3.m3num / 30 * utility(cluster3, "m3")
    # print("avg",avg)
    return avg

def changerate(m,cluster):
    if m=="m1":
      rate=cluster.m1num/30*LEARNINGRATE*(utility(cluster,m)-avgutility(m))
    elif m=="m2":
        rate = cluster.m2num / 30 * LEARNINGRATE*(utility(cluster, m) - avgutility(m))
    else :
         rate = cluster.m3num / 30 * LEARNINGRATE*(utility(cluster, m) - avgutility(m))
    # print("rate",rate)
    # print("-"*50)
    return rate

    #计算迭代产生的worker数

state1=[]
state2=[]
state3=[]

clusters=[cluster1,cluster2,cluster3]
rate = np.zeros((3,3))

def iterationT():
    for i in range(len(rate)):
        for j in range(len(rate[0])):
            if i==0:
               rate[i][j]=  changerate("m1",clusters[j])
            elif i==1:
                rate[i][j]= changerate("m2",clusters[j])
            else :
                rate[i][j]= changerate("m3",clusters[j])

    for i in range(len(rate)):
        for j in range(len(rate[0])):
            if i==0:
               clusters[j].m1num=clusters[j].m1num+rate[i][j]*clusters[j].m1num
            elif i==1:
                clusters[j].m2num = clusters[j].m2num + rate[i][j] * clusters[j].m2num
            else :
                clusters[j].m3num = clusters[j].m3num + rate[i][j] * clusters[j].m3num

for t in range(TMAX):
    iterationT()
    state1.append(cluster1.clustersample())
    state2.append(cluster2.clustersample())
    state3.append(cluster3.clustersample())

fig = plt.figure()
ax=fig.add_axes([0.2,0.2,0.6,0.6])
plt.plot(range(TMAX),state1,'bo--')
plt.plot(range(TMAX),state2,'ro--')
plt.plot(range(TMAX),state3,'go--')
plt.title("evolution game")
plt.xlabel('t')
plt.ylabel('population')

ax.legend(labels = ('j1','j2','j3'), loc = 'lower right')
plt.show()


