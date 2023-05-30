# -*- coding: utf-8 -*-
"""Копия блокнота "Копия блокнота "Untitled0.ipynb""

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Il49tBdHTVhiLL-iR0VCYWQDsQ77Th3L
"""

import collections
import random
import statistics
import matplotlib.pyplot
import pandas as pd
import math


def quantiles(l, n=0, method=''):
    l.sort()
    r = []
    for i in range(n):
        r.append(l[len(l)*i//n])
    r.append(l[-1])
    return r

statistics.quantiles = quantiles


class Opinion:
    def __init__(self, x):
        self.x = x

    def clone():
        return Opinion(self.x)

    def diff(self, o):
        return self.x - o.x

    def communicate(self, o,pow1,pow2):
        diff = self.diff(o)
        abs_diff = abs(diff)
        k = 1 - abs_diff
        K = 0.1
        speed=diff * k / 2 * K
        k2=1
        if pow1>pow2:
            divis=abs(speed)*(1-(pow2/pow1))
            diff1=abs(speed)-k2*divis
            diff2=abs(speed)+k2*divis
        if pow2>pow1:
            divis=abs(speed)*(1-(pow1/pow2))
            diff1=abs(speed)+k2*divis
            diff2=abs(speed)-k2*divis
        if pow1==pow2:
            diff1=abs(speed)
            diff2=abs(speed)
        if speed<0:
            diff1=0-diff1
            diff2=0-diff2
        
        new_op1 = Opinion(self.x - diff1)
        new_op2 = Opinion(o.x + diff2)
        return new_op1, new_op2

    def replaceWithAverage(self, opinions):
        s = 0
        c = 0
        for o in opinions:
            s += o.x
            c += 1
        self.x = s/c


class Connection:
    def __init__(self, person, strength):
        self.person = person
        self.strength = strength

    def active(self):
        return random.random() < (self.strength)

class Person:
    def __init__(self, opinion,power,prof):
        self.connections = []
        self.connections2 = []
        self.opinion = opinion
        self.power=power
        self.prof=prof
        self.prof2=0

    def addConnection(self, connection):
        self.connections.append(connection)

    def communicate(self):
        new_ops = []
        self.connections2 = self.connections
        self.prof2=self.prof
        K=1
        for c in self.connections2:
            if c.active():
                new_ops.append((c.person, *self.opinion.communicate(c.person.opinion,self.power,c.person.power)))


                K2=(1-self.prof)
               # K2=0
                diff = abs(self.opinion.diff(c.person.opinion))
                k = ((1-diff)*10 - 8.5) # -1 большое расхождение
                dopstrength=c.strength
                if k < 0:
                    speed = k*c.strength*K
                    #if k*c.strength*K>0:
                        #print('ty ne prav')
                    speed +=(K2*speed)
                    c.strength+=speed
                else:
                    speed = k*(1-c.strength)*K
                    speed -=(K2*speed)
                    c.strength+=speed
                
                self.prof2+=(dopstrength-c.strength)
                if self.prof2<0:
                    self.prof2=0.00000000000000001
                if self.prof2>1:
                    self.prof2=0.99
                
        return new_ops

    def updateConnections(self):
           self.connections=self.connections2
           self.prof=self.prof2

          
 

            

def randomOpinion():
    return Opinion(random.random())


def cycle():
    ops = []
    for p in people:
        ops.append((p, p.communicate()))

    m = collections.defaultdict(list)
    for p, new_ops in ops:
        for p2, x, y in new_ops:
            m[id(p2)].append(y)
            m[id(p)].append(x)

    for p in people:
        if id(p) in m:
            assert m[id(p)]
            p.opinion.replaceWithAverage(m[id(p)])

    for p in people:
        p.updateConnections()


def round_list(l, n):
    return [round(x, n) for x in l]

def stats():
    opinions_numbers = []
    connections_strengths = []
    for p in people:
        opinions_numbers.append(p.opinion.x)
        connections_strengths.append(sum([c.strength for c in p.connections])/len(p.connections))
    print(round_list(statistics.quantiles(opinions_numbers, n=20, method='inclusive'), 3))
    print(round_list(statistics.quantiles(connections_strengths, n=20, method='inclusive'), 3))
    print('------')


def stats2(x):
    opinions_numbers = []
    connections_strengths = []
    for p in people:
        opinions_numbers.append(p.opinion.x)
        connections_strengths.append(sum([c.strength for c in p.connections])/len(p.connections))
    matplotlib.pyplot.hist(opinions_numbers, bins=40, range=(0.0,1.0))
    #matplotlib.pyplot.hist(connections_strengths, bins=20)
    matplotlib.pyplot.savefig(str(x)+'.png')
    matplotlib.pyplot.close()

def stat_table(x):
    opinions_numbers = []
    #connections_strengths = []
    source=[]
    target=[]
    connections = []
    weight=[]
    typ=[]
    for p in people:
        opinions_numbers.append(p.opinion.x)
    for p1 in range(len(people)):
        for p2 in range(len(people)):
            if people[p1].connections[p2].strength>0.1:
                source.append(x[p1])
                target.append(x[p2])
                connections.append(people[p1].connections[p2].strength)
                weight.append(1)
                typ.append('undirected')
            
    
    dic={'country':x,'ppc':opinions_numbers}
    data=pd.DataFrame(dic)
    print(sum(connections))
    dic={'Source':source,'Target':target,'Weight':weight,'Color':connections,'Type':typ}
    data2=pd.DataFrame(dic)
    return (data,data2)


#people = [Person(randomOpinion()) for _ in range(1000)]
people=[]
climdata=pd.read_csv('climate_norm.csv',sep=';')
tradedata=pd.read_csv('trade_sharev_norm.csv',sep=';')
power2=pd.read_csv('gdp.csv',sep=';')
for i in range(climdata.shape[0]):
    people.append(Person(Opinion(climdata['norm_ppc'][i]),power2['gdp'][i],0.5))

counttrade=0
for p in people:
    for p2 in people:
        #p.addConnection(Connection(p2, random.random()/100))
        p.addConnection(Connection(p2, tradedata['sharev_norm'][counttrade]))
        counttrade=counttrade+1

#for p in people[:20]:
 #   p.opinion.x = 1

#for p in people[100:200]:
#    p.opinion.x = 0


for i in range(1000):
    print(i)
    stats2(i)
    cycle()
    stat_table(climdata['country'].tolist())[0].to_csv(str(i)+'.csv',sep=';',index=False)
    table=stat_table(climdata['country'].tolist())[0]
   # stats()
    if (i == 10)or(i==50)or(i==99)or(i==0)or(i==150)or(i==199)or(i==500)or(i==999):
        dic={'Id':table['country'],'Opinion':table['ppc']}
        gephiop=pd.DataFrame(dic)
        gephiop.to_csv(str(i)+' op.csv',sep=';',index=False)
        stat_table(climdata['country'].tolist())[1].to_csv(str(i)+' con.csv',sep=';',index=False)
        
    #print(table[(table['country']=='United Kingdom')|(table['country']=='USA, Puerto Rico and US Virgin Islands')])
    #USA, Puerto Rico and US Virgin Islands

people[0].opinion.x

collections.Counter(round_list([c.strength for c in people[0].connections], 3))
