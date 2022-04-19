

import json
from hazm import *
from hazm import stopwords_list
import string
from collections import defaultdict


def create_dectionary(mydict ,stemmer ,mystopwordset):

    with open("IR_data_news_10.json") as f:
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


def intersect(list1, list2):
    i = 0
    j = 0
    result = []
    while i < len(list1) and j < len(list2):
        if list1[i][0] == list2[j][0]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i][0] < list2[j][0]:
            i += 1
        else:
            j += 1
    return result


def subtract(list1, list2):

    newresult = []
    doclist2 = []
    for i in list2:
        doclist2.append(i[0])
    for i in list1:
        if i[0] in doclist2:
            continue
        newresult.append(i)
    
    return newresult

def finish():
    print("There is nothing for you")
    exit()       

if __name__ == "__main__":

    mydict = defaultdict(list)
    stemmer = Stemmer()
    mystopwordset = set(stopwords_list())
    rankdict = defaultdict(int)
    resault = []

    create_dectionary(mydict ,stemmer ,mystopwordset)


    print("enter what you want to search")
    myinput = input()

    if myinput[0] == '"':
        #phrase search
        search_terms =  list(filter(None, myinput.replace('"',' ').split(' ')))
        type_search = 0
    else:
        # seperate words search 
        search_terms =  list(filter(None, myinput.split(' ')))
        intersect_list = []
        subtract_list = []
        is_sub = 0
        for i in search_terms:
            if i == '!':
                is_sub = 1
                continue
            search_resualt = search_dictionary(i , mydict ,stemmer)
            if len(search_resualt) == 0:
                finish()
            if is_sub == 1:
                subtract_list.append(search_dictionary(i , mydict ,stemmer))
                is_sub = 0
                continue
            intersect_list.append(search_dictionary(i , mydict ,stemmer))

        resault = intersect_list.pop()[1]
        for i in intersect_list:
            resault = intersect(i[1], resault)
        for i in subtract_list:
            resault = subtract(resault ,i[1])



        # resault = search_dictionary(search_terms[0] , mydict ,stemmer)

        
        ranked = ranked_results(resault ,rankdict)
        print(ranked)

    
    


