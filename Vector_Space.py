
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

            

def normelizer(text,stemmer ,mystopwordset):

    
    text = list(filter(None, text))
    return_list = []
    for i in range(len(text)):

        if text[i] in mystopwordset:
            continue
        stemm = stemmer.convert_to_stem(text[i])
        # return_list.append([stemm,i])
        return_list.append(stemm)

    
    return return_list
    
def search_dictionary(term , mydict ,stemmer):
    
    term = stemmer.convert_to_stem(term)
    return mydict[term]

if __name__ == "__main__":

    with open("IR_data_news_10.json") as f:
        data = f.read()
    jsondata = json.loads(data)

    mydict = defaultdict(lambda: defaultdict(list))
    stemmer = FindStems()
    mystopwordset = set(stopwords_list())

    create_dectionary(mydict ,stemmer ,mystopwordset , jsondata)

    tf_idf(mydict ,len(jsondata))

    print("enter what you want to search")
    myinput = input()

    myinput = list(filter(None, myinput.split(' ')))

    search_terms = normelizer(myinput ,stemmer ,mystopwordset)

    query_w = []
    query_dict = defaultdict(list)

    for i in search_terms:
        if len(query_dict[i]) == 0:
            query_dict[i].append(1)
        else:
            query_dict[i][0] += 1

    
    for i in query_dict.keys():
        
        nt = len(mydict[i].keys())
        idf = math.log(len(jsondata)/nt)
        tf = 1 + math.log(query_dict[i][0]) 
        w = tf * idf
        query_dict[i].append(w)
    
    

    

    

    