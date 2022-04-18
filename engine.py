

import json
from hazm import *
from hazm import stopwords_list


with open("IR_data_news_10.json") as f:
    data = f.read()
jsondata = json.loads(data)

tokenlist = list()
for i in range(len(jsondata)):
    mytoken = word_tokenize(jsondata[str(i)]["content"])
    copymytoken = mytoken.copy()
    for j in copymytoken:
        if j in stopwords_list() or len(j) == 1:
            mytoken.remove(j)

    tokenlist.append(mytoken)
    break

print(tokenlist)