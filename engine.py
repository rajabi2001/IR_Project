

import json
from hazm import *
from hazm import stopwords_list
import string
from collections import defaultdict

stemmer = Stemmer()
mydict = defaultdict(list)

with open("IR_data_news_10.json") as f:
    data = f.read()
jsondata = json.loads(data)

tokenlist = list()
for i in range(len(jsondata)):
    mytoken = word_tokenize(jsondata[str(i)]["content"].translate(str.maketrans('', '', string.punctuation)))
    copymytoken = mytoken.copy()
    for j in copymytoken:
        if j in stopwords_list() or len(j) == 1 :
            mytoken.remove(j)

    for j in range(len(mytoken)):
        mytoken[j] = stemmer.stem(mytoken[j])

    mytoken = list(filter(None, mytoken))
    tokenlist.append(mytoken)

# print(tokenlist)

for i in range(len(tokenlist)):
    for j in range(len(tokenlist[i])):
        thistoken = tokenlist[i][j]
        if len(mydict[thistoken]) == 0 :
            mydict[thistoken].append(1)
            mydict[thistoken].append(list())
            
        else :
            mydict[thistoken][0] += 1
            
        mydict[thistoken][1].append([i,j])  
    

print(mydict['ورزش'])
    


