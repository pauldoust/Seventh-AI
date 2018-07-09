# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag,sent_tokenize
from nltk.stem import WordNetLemmatizer
lemmatiser = WordNetLemmatizer()
from nltk.corpus import wordnet
import pickle, math
import os

class API:
    def __init__(self):
        currentPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '')
        file = open(currentPath + 'indexBook.obj',"r")
        lines = file.readlines()
        self.features = dict()
        for line in lines:
            arr = line.strip('\n').split('->')
            self.features[ arr[1] ] = arr[0]
        
        file = open(currentPath + "Template.obj","r") 
        lines = file.readlines()
        self.pca_features_template = []
        i = 0
        for line in lines:
            arr = line.replace('-','|-').replace('+','|+').split('|')
            arr = [a.strip('\n') for a in arr if len(a.strip())>0]
            self.pca_features_template.append([a.split('A') for a in arr])
            i += 1 
        
        pickle_in = open(currentPath + "clf.pickle","rb")
        self.clf = pickle.load(pickle_in)
        

    def get_wordnet_pos(self , treebank_tag):
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
    
    def ngrams(self , input, n):
      output = []
      for i in range(len(input)-n+1):
        output.append(''.join(input[i:i+n]))
      return output
    
    def preprocess(self , record):
        sent_text = sent_tokenize(record)
        output = []
        for sent in sent_text:
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(sent)
            pos = pos_tag(word_tokens)
            output += [lemmatiser.lemmatize(x[0], pos=self.get_wordnet_pos(x[1])) if  x[0] not in stop_words else '#' for x in pos if self.get_wordnet_pos(x[1])!='']
            output += ['.']
        return ' '.join(output).replace(' .','.')
    
    def get_features(self , txt):
        txt = self.preprocess(txt.lower())
        chrs = [c for c in txt]
        grams = []
        for nn in [3,4,5,6,7]:
            grams += self.ngrams(chrs , nn)
        
        grams = list(set(grams))
        ex_features = []
        for g in grams:
            if g in self.features:
                ex_features.append(self.features[g])
        
        row_v = []
        for ex in self.pca_features_template:
            v = sum(list(map(lambda x:float(x[0]) if ('A'+x[1]) in ex_features else 0 , ex)))
            row_v.append(v)
        return row_v
    
    def predict(self , txt):
        row_v = self.get_features(txt)
        results = self.clf.predict_proba([row_v])[0]
        # gets a dictionary of {'class_name': probability}
        prob_per_class_dictionary = dict(zip(self.clf.classes_, results))
        results_ordered_by_probability = map(lambda x: (x[0].strip(".\n"),math.floor(x[1]*1000)/10), sorted(zip(self.clf.classes_, results), key=lambda x: x[1], reverse=True))
        results_ordered_by_probability_list = list(results_ordered_by_probability)
        return results_ordered_by_probability_list

txt = '''tech genomic assay reagent tool bioanalytical assay chemistry device manufacturing construction mechnical proteomic assay reagent tool molecular array allow scientist perform large scale quantitative biological analysis biomarker discovery immunomonitoring epitope mapping making molecular array difficult though sensitive distinct parameter including nature biochemical molecule present array process apply solution directly surface result puddling highly heterogeneous array many method process forming array fail yield large quantity molecular array consistently high quality researcher biodesign institute arizona state university developed novel device method consistently making superior molecular array device specialized instrument facilitate homogeneous coupling reaction array method pertains way using device performing chemical reaction surface array device method able maintain even distribution material constant concentration make consistently high quality array device method enable improved thermal control consistent production high quality molecular array large quantity bio technology device method making molecular array'''
'''
api = API()
result = api.predict(txt)
print(result[:15])'''