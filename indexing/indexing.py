import pandas as pd
import sklearn as sk
import math 

first_sentence = "Data Science is the sexiest job of the 21st century"
second_sentence = "machine learning is the key for data science"#split so each word have their own string
print("doc1:\n",first_sentence,'\ndoc2:\n',second_sentence)
print("\n")

first_sentence = first_sentence.split(" ")
second_sentence = second_sentence.split(" ")#join them to remove common duplicate words


total= set(first_sentence).union(set(second_sentence))
print("Total words:")
print(total)

wordDictA = dict.fromkeys(total, 0) 
wordDictB = dict.fromkeys(total, 0)

for word in first_sentence:
    wordDictA[word]+=1
    
for word in second_sentence:
    wordDictB[word]+=1

def computeTF(wordDict, doc):
    tfDict = {}
    corpusCount = len(doc)
    for word, count in wordDict.items():
        tfDict[word] = count/float(corpusCount)
    return(tfDict)

#running our sentences through the tf function:

tfFirst = computeTF(wordDictA, first_sentence)
tfSecond = computeTF(wordDictB, second_sentence)
#Converting to dataframe for visualization

tf = pd.DataFrame([tfFirst, tfSecond])
print("\nTF:")
print(tf)

def computeIDF(docList):
    idfDict = {}
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / (float(val) + 1))
        
    return(idfDict)

#inputing our sentences in the log file
idfs = computeIDF([wordDictA, wordDictB])
print('\nIDF:')
print(idfs)
def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return(tfidf)
#running our two sentences through the IDF:

idfFirst = computeTFIDF(tfFirst, idfs)
idfSecond = computeTFIDF(tfSecond, idfs)
#putting it in a dataframe


idf= pd.DataFrame([idfFirst, idfSecond])
print("\nTF IDF:")
print(idf)



from sklearn.feature_extraction.text import TfidfVectorizer
firstV= "Data Science is the sexiest job of the 21st century"
secondV= "machine learning is the key for data science"

vectorize= TfidfVectorizer()

response= vectorize.fit_transform([firstV, secondV])
print(response) 
