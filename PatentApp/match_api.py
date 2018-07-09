# -*- coding: utf-8 -*-
from heapq import nlargest
import pickle
from .api import API
import pandas as pd 
import functools
import os
api = API()

class Match_API:
    def __init__(self):
        currentPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '')
        pickle_in = open(currentPath + "companies_dict.pickle","rb")
        self.companies_dict = pickle.load(pickle_in)
        handle = open(currentPath + 'sectors_fields_w.pickle', 'rb')
        self.comp_fields_dic = pickle.load(handle)
    
    def sim(self, v1 ,v2):
        #return -1*sum([abs(x[0]-x[1]) for x in zip(v1, v2)])
        return sum([1 if x[0]>0 and x[1]>0 else 0 for x in zip(v1, v2)])

    def getMatches(self , txt , num_of_results=10):
        features = api.get_features(txt)
        distances = nlargest(num_of_results , list(map(lambda c1:(c1[0] , c1[2] , c1[3] , self.sim(c1[1] , features)) , self.companies_dict)) , key=lambda x:x[3])
        fields = api.predict(txt)
        all_nodes = []
        all_edges = []
        for d in distances:
            if d[0] not in all_nodes: all_nodes.append(d[0])
            for f in fields:
                if f[0] not in all_nodes: all_nodes.append(f[0])
                all_edges.append((f[0],d[0], self.comp_fields_dic.get(d[1]+"_"+f[0] , -1)*f[1]))
        
        for d in distances:
            sum_d = sum([x[2] for x in all_edges if x[1]==d[0]])
            all_edges = [(f0 , d0 , int(v*100/sum_d)) if d0==d[0] else (f0 , d0 , v) for (f0 , d0 , v) in all_edges]
        all_edges = [x for x in all_edges if x[2]>1]
        
        all_nodes = list(set(functools.reduce(lambda a,b: a+b , [ [x[0],x[1]] for x in all_edges])))
        return (all_nodes , all_edges)
    
    def reTrain(self , xlsfile):
        df = pd.read_excel(xlsfile)
        name = df['Name']
        desc = df['Company Description']
        sector = df['Sector']
        industry = df['industry']
        
        companies_dict = []
        for i in range(0,len(name)):
            try:
                result = api.get_features(str(desc[i]))
                companies_dict.append((name[i] , result , sector[i] , industry[i]))
                print(i,len(name))
            except:
                print("Error!")
        pickle_out = open("companies_dict.pickle","wb")
        pickle.dump(companies_dict, pickle_out)
        pickle_out.close()
           
        
        dic = dict()
        companies_dict = []
        for i in range(0,len(name)):
            try:
                result = api.predict(desc[i])
                for r in result:
                    key = sector[i]+"_"+r[0]
                    dic[key] = dic.get(key , 0) + r[1]
                print("=>",i)
            except:
                print("Error")
            
            
        
        with open('sectors_fields_w.pickle', 'wb') as handle:
            pickle.dump(dic, handle)


# txt = '''Robust Biomimetic Diiron Catalysts for Hydrogen Production.'''
# matcher = Match_API()
# distances = matcher.getMatches(txt , 3)
# print(distances)


#print(fields)
