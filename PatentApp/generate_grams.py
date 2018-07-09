# -*- coding: utf-8 -*-import codecs
from random import randint
import codecs
import csv
from collections import Counter
import numpy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag,sent_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
lemmatiser = WordNetLemmatizer()
from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def ngrams(input, n):
  output = []
  for i in range(len(input)-n+1):
    output.append(''.join(input[i:i+n]))
  return output

gramsnn = dict()



def preprocess(record):
    sent_text = sent_tokenize(record)
    output = []
    for sent in sent_text:
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(sent)
        pos = pos_tag(word_tokens)
        output += [lemmatiser.lemmatize(x[0], pos=get_wordnet_pos(x[1])) if  x[0] not in stop_words else '#' for x in pos if get_wordnet_pos(x[1])!='']
        output += ['.']
    return ' '.join(output).replace(' .','.')

f = codecs.open("cleanedDataWithCateg.csv", "r", "utf-8")
lines = f.readlines()
lines = [line.split('\t') for line in lines]
col = 1
inputs = [preprocess(line[col].lower()) for line in lines]

categ = [preprocess(line[3].lower()) for line in lines]

ids = [line[0] for line in lines]
i = 0
for nn in [3,4,5,6,7]:
    for input in inputs:
        i = i + 1
        chrs = [c for c in input]
        grams = list(set(ngrams(chrs , nn)))
        for g in grams:
            gramsnn[g] = gramsnn.get(g , 0) + 1
    gramsnn = { k:v for k, v in gramsnn.items() if v < 0.2*len(inputs) and v > 0.005*len(inputs)  }
    
    outfile = codecs.open( 'grams'+str(nn)+'.csv', 'w' , "utf-8" )
    for key, value in gramsnn.items():
        outfile.write( str(key) + '\t' + str(value) + '\n' )
    outfile.close()
    print(str(nn)+">"+str(len(gramsnn.keys())))
ii= 0
for key in gramsnn:
    gramsnn[key] = ii
    ii += 1
first = True
ai = 0
co = 0
idx = ""
f = open('55_input_features.csv','w')
for i in range(0,len(inputs)):
    txt = inputs[i]
    #if randint(1, 100) <95:
    #    continue
    if co%1000==0:
        print(str(co)+"From"+str(len(lines)))
    co += 1
    output = '0'#line [3]
    chrs = [c for c in txt]
    grams = []
    for nn in [3,4,5,6,7]:
        grams += ngrams(chrs , nn)
        row_v =  ['0'] * len(gramsnn.keys())
    for key in grams:
        if key in gramsnn:
            row_v[ gramsnn[key] ] = '1'
    
    if first:
        listg = list(gramsnn)
        for xx in range(0,len(row_v)):
            row_v[xx]='A'+str(xx)
            idx += row_v[xx] + "->"+ listg[xx] +"\n"
        print(txt)
        print(grams)
    row = ','.join(row_v)
    first = False
    f.write(row+','+str(ids[i])+','+str(categ[i])+"\n")
    #if co > 0.1*len(lines):
    #    break
f.close()

findex = codecs.open('indexBook.csv','w',"utf-8")
findex.write(idx)
findex.close()

