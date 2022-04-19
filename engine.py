

import json
from hazm import *
from hazm import stopwords_list
import string
from collections import defaultdict


def create_dectionary(mydict ,stemmer ,mystopwordset):

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
    

def search_dictionary(term , mydict ,stemmer):
    
    term = stemmer.stem(term)
    return mydict[term]


def ranked_results(resault ,rankdict):

    for i in resault:
        rankdict[i[0]] += 1

    newresault = []
    
    for key in rankdict:
        newresault.append([key,rankdict[key]])

    newresault.sort(key=lambda x: x[1],reverse=True)

    return newresault

    
    


if __name__ == "__main__":

    print("enter what you want to search")
    inputlist =  list(filter(None, input().replace('"',' ').split(' ')))
    # print(inputlist)

    mydict = defaultdict(list)
    stemmer = Stemmer()
    mystopwordset = set(stopwords_list())

    create_dectionary(mydict ,stemmer ,mystopwordset)

    resault = search_dictionary(inputlist[0] , mydict ,stemmer)

    rankdict = defaultdict(int)
    ranked = ranked_results(resault[1] ,rankdict)
    print(ranked)

    
    


