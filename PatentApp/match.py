# -*- coding: utf-8 -*-
'''
import pandas as pd 
from api import API
from match_api import Match_API 
import operator
import pickle

matcher = Match_API()

api = API()
print('--------------------')
processed_file = open("data.csv","w")  
file = r'Companies.xlsx'
df = pd.read_excel(file)
name = df['Name']
desc = df['Company Description']
sector = df['Sector']
industry = df['industry']

dic = dict()

print('--------------------')
companies_dict = []
for i in range(0,len(name)):
    try:
        distances = matcher.getMatches(desc[i])
        result = api.predict(desc[i])
        for r in result:
            key = sector[i]+"_"+r[0]
            dic[key] = dic.get(key , 0) + r[1]
        print("=>",i)
    except:
        print("Error")
    
    

with open('sectors_fields_w.pickle', 'wb') as handle:
    pickle.dump(dic, handle)

with open('sectors_fields_w.pickle', 'rb') as handle:
    dic = pickle.load(handle)


sorted_d = sorted(dic.items(), key=operator.itemgetter(1) ,  reverse=True)
print(sorted_d)
processed_file.close() 
'''
