

import json
from hazm import *
from hazm import stopwords_list
import string
from collections import defaultdict

stemmer = Stemmer()
mydict = defaultdict(list)
mystopwordset = set(stopwords_list())

with open("IR_data_news_12k.json") as f:
    data = f.read()
jsondata = json.loads(data)

tokenlist = list()
for i in range(len(jsondata)):
    mytoken = word_tokenize(jsondata[str(i)]["content"].translate(str.maketrans('', '', string.punctuation)))
    mytoken = list(filter(None, mytoken))

    for j in range(len(mytoken)):
        # i -> doc , j -> position
        thistoken = mytoken[j]

        if thistoken in mystopwordset or len(thistoken) == 1 :
            continue

        thistoken = stemmer.stem(thistoken)
        
        if len(thistoken) == 0 :
            continue

        # print(thistoken)
        if len(mydict[thistoken]) == 0 :
            mydict[thistoken].append(1)
            mydict[thistoken].append(list())
            
        else :
            mydict[thistoken][0] += 1
        
        mydict[thistoken][1].append([i,j]) 
    

print("enter what you want to search")
searchterm = stemmer.stem(input())
print(mydict[searchterm])
    


