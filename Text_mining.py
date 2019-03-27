# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 00:31:40 2019

@author: gaura
"""
#importing all the required libraries
import nltk
import glob
import errno
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.probability import FreqDist
import string
import pandas as pd

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')
# importing all the file links into a common file
import glob
files=glob.glob('C:/Users/gaura/Desktop/stat 656/week 9/assignment/TextFiles/*.txt')

# importing all the text files into a dataframe
Doc = pd.DataFrame(index=range(8),columns=['Story'])
k=0
for file in files:
    text = open(file, 'r').read()
    Doc['Story'][k]=text
    k=k+1
 
    
# defining a function to punctuate the  data in correct form   
def punctuate(df,column):
    df[column] = df[column].apply(lambda x: x.lower())
    df[column] = df[column].apply(lambda x: x.replace('-' , ' '))
    df[column] = df[column].apply(lambda x: x.replace('_' , ' '))
    df[column] = df[column].apply(lambda x: x.replace(',' , ' '))
    df[column] = df[column].apply(lambda x: x.replace('nt','not'))    

# punctuate     
punctuate(Doc,'Story')    


#defining functions to do all the operations on data
def tokenize(Document,i):
    tokens = word_tokenize(Document['Story'][i])
    tokens = [word.replace(',', '') for word in tokens]
    tokens = [word for word in tokens if ('*' not in word) and ("''" != word) and ("``" != word) and \
                 (word!='description') and (word !='dtype') and (word != 'object') and (word!="'s")]
    return(tokens)

def tag(tokens):
    tagged_tokens = nltk.pos_tag(tokens)
    return(tagged_tokens)

def remove_stop_words(tagged_tokens):
    stop = stopwords.words('english') + list(string.punctuation)
    stop_tokens = [word for word in tagged_tokens if word[0] not in stop]
    stop_tokens = [word for word in stop_tokens if len(word) > 1]
    stop_tokens = [word for word in stop_tokens if (not word[0].replace('.','',1).isnumeric()) and word[0]!="'s" ]
    return(stop_tokens)
    
def stemmer(stop_tokens):
    ps=PorterStemmer()
    stemmed_tokens=[]
    for word in stop_tokens:
       stemmed_tokens.append(ps.stem(word[0]))
    return(stemmed_tokens)
    
def merge_tokens(Stemmed_tokens, final_token):
    final_token.extend(Stemmed_tokens)
    print("\nDocument",str(i+1) ,"contains a total of", len(Stemmed_tokens), " terms.")
    if i==7:
        print("\nCorpus","has total", len(final_token), "words.")
    return(final_token)
                
def output(Token):
    freq = FreqDist(Token)
    freq
    Scenario_1_20=[]
    for pos, frequency in freq.most_common(freq.N())[0:20]:
        Scenario_1_20.append(pos)
        print(pos ,'---',frequency)
        
#scenario 1
        
Token1=[]
for i in range(8):
    tokens=tokenize(Doc,i)
    tagged_tokens=tag(tokens)
    stop_tokens=remove_stop_words(tagged_tokens)
    stemmed_tokens=stemmer(stop_tokens)
    merge_tokens(stemmed_tokens, Token1)

output(Token1)

# scenario 2
def remove_stop_words(tagged_tokens):
    stop = stopwords.words('english') + list(string.punctuation)
    stop_tokens = [word for word in tagged_tokens if word not in stop]
    stop_tokens = [word for word in stop_tokens if len(word) > 1]
    stop_tokens = [word for word in stop_tokens if (not word[0].replace('.','',1).isnumeric()) and word[0]!="'s" ]
    return(stop_tokens)
Token2=[]
for i in range(8):
    tokens=tokenize(Doc,i)      
    stop_tokens=remove_stop_words(tokens)
    stemmed_tokens=stemmer(stop_tokens)
    merge_tokens(stemmed_tokens, Token2)
output(Token2)


# Scenario 3
Token3=[]
for i in range(8):
    tokens=tokenize(Doc,i)
    stop_tokens=remove_stop_words(tokens)
    merge_tokens(stop_tokens, Token3)
output(Token3)

#scenario 4
Token4=[]
for i in range(8):
    tokens=tokenize(Doc,i)
    merge_tokens(tokens, Token4)

output(Token4)
