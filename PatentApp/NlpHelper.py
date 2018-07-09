import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re

ps = PorterStemmer()
lemma = WordNetLemmatizer()
exclude = set(string.punctuation)


class PreProcessing:

    # Perfom tokenization (by word or sentence) on an input sentence
    @staticmethod
    def tokenize(sentence, tokenizing="word"):
        sentence = sentence.lower()
        if(tokenizing == "word"):
            return word_tokenize(sentence)
        else:
            return sent_tokenize(sentence)

    # Prform filtering on a sentence using default stopwords for each language (default english)
    # customStopWords (optional): custom set of user defined stop words
    @staticmethod
    def filterStopWords(sentence, customStopWords=[], lang="english"):
        stop_words = set(stopwords.words(lang))
        filtered_sentence = []

        if not isinstance(sentence, str):
            return filtered_sentence
        tokenizedWords = PreProcessing.tokenize(sentence)
        filtered_sentence = [
            w for w in tokenizedWords if w not in stop_words and w not in customStopWords]
        return filtered_sentence

    # s Perform Stemming for the inpur word
    @staticmethod
    def stem(wordsToStem):
        if isinstance(wordsToStem, list):
            stemmed_words = [ps.stem(w) for w in wordsToStem]
            return stemmed_words
        elif isinstance(wordsToStem, str):
            # print(wordsToStem)
            return ps.stem(wordsToStem)

    # Perform pos tagging for an input sentence
    @staticmethod
    def posTagging(sentence):
        try:
            tokenizedWords = PreProcessing.tokenize(sentence)
            taggedTokens = nltk.pos_tag(tokenizedWords)
            # print(taggedTokens)
            return taggedTokens
        except Exception as e:
            print(str(e))

    # Perform Chunking according to grammar and a posTagged sentence
    @staticmethod
    def chunk(taggedSentence, grammar):
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(taggedSentence)
        # result.draw()
        return result

    @staticmethod
    def shallowParsing(sentence, customToExclude):
        if isinstance(sentence, float):
            return ""
        sentence = ' '.join([i for i in sentence.split() if i not in customToExclude])
        grammar = r"""
            NP: {<NN.*|JJ>*<NN.*>}
            J:  {<JJ*|RB*>+}
                {<JJ*>+<TO><V*>} 
            NP: {<NN.*><IN><NN.*>}
            NR: {<NP>}
                {<NP><IN><NP>}
        """
        taggedSent = PreProcessing.posTagging(sentence)
        chunked = PreProcessing.chunk(taggedSent, grammar)
        result = PreProcessing.extract_entity(chunked, "NR")
        return result

    @staticmethod
    def ngrams(text, n=2):
        tokenizedWords = PreProcessing.tokenize(text)
        grams = ngrams(tokenizedWords, n)
        return grams

    @staticmethod
    def countFrequency(ngrm, top=1):
        fdist = nltk.FreqDist(ngrm)
        return fdist.most_common(top)

    @staticmethod
    def clean(doc, customStopWords=[], withStemming=False):
        if isinstance(doc, float):
            return ""
        tokeniziedWords = PreProcessing.tokenize(doc)
        # customStopWords = customStopWords.append(exclude)
        # stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        stop_free = " ".join(PreProcessing.filterStopWords(
            " ".join(tokeniziedWords), customStopWords))
        # punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        punc_free = ''.join(
            ch if ch not in exclude else ' ' for ch in stop_free)
        normalized = " ".join(lemma.lemmatize(word)
                              for word in punc_free.split())
        if(withStemming):
            stemmed = " ".join(PreProcessing.stem(normalizedWord)
                               for normalizedWord in normalized.split())
            return stemmed
        else:
            return normalized

    @staticmethod
    def leaves(tree, tag):
        for subtree in tree.subtrees(filter=lambda t: hasattr(t, 'label') and t.label() == tag):
            yield subtree.leaves()

    @staticmethod
    def extract_entity(tree, tag):
        roles = []
        # merge these phrases and store them as a possible role
        for leaf in PreProcessing.leaves(tree, tag):
            term = [w for w, t in leaf]
            roles.append(" ".join(term))
        return roles


# print(PreProcessing.shallowParsing("hello Computer Science"))
# test = PreProcessing.shallowParsing("hello Computer Science")
# print(extract_entity(test,"NR"))
# # test = PreProcessing.shallowParsing("hello Computer Science")
# # for r in test:
# #     if type(r) == nltk.tree.Tree:
# #         print('NP:', ' '.join([x[0] for x in r.leaves()]))


# s = "o Fello world. how are you ? are you doing fine !!"
# print(re.sub(r'o ([A-Z]+)',r'. \1',s))