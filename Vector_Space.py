
import json
from hazm import *
from hazm import stopwords_list
import string
from collections import defaultdict
from parsivar import FindStems
import math


def create_dectionary(mydict ,stemmer ,mystopwordset , jsondata):

    for i in range(len(jsondata)):
        mytoken = word_tokenize(jsondata[str(i)]["content"].translate(str.maketrans('', '', string.punctuation)))
        mytoken = list(filter(None, mytoken))

        for j in range(len(mytoken)):
            # i -> doc , j -> position
            thistoken = mytoken[j]

            if thistoken in mystopwordset or len(thistoken) == 1 :
                continue

            thistoken = stemmer.convert_to_stem(thistoken)
            
            if len(thistoken) == 0 :
                continue
            
            # if len(mydict[thistoken]["nt"]) == 0:
            #     mydict[thistoken]["nt"].append(1) 
            # else :
            #     mydict[thistoken]["nt"][0] += 1
            
            # print(thistoken)
            if len(mydict[thistoken][i]) == 0 :
                mydict[thistoken][i].append(1)
                
            else :
                mydict[thistoken][i][0] += 1


def tf_idf(mydict , N):

    for i in mydict.keys():

        nt = len(mydict[i].keys())
        idf = math.log(N/nt)

        for j in mydict[i].keys():
            
            # if type(j) == str:
            #     continue

            f = mydict[i][j][0]
            tf = 1 + math.log(f) 

            w = tf * idf
            mydict[i][j].append(w)

            


    

if __name__ == "__main__":

    with open("IR_data_news_10.json") as f:
        data = f.read()
    jsondata = json.loads(data)

    mydict = defaultdict(lambda: defaultdict(list))
    # stemmer = Stemmer()
    stemmer = FindStems()
    mystopwordset = set(stopwords_list())

    create_dectionary(mydict ,stemmer ,mystopwordset , jsondata)

    tf_idf(mydict ,len(jsondata))
    

    

    