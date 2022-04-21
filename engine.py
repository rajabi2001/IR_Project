
# 1.combine two way searching -> done
# 2.buil valid output


import chunk
import json
from hazm import *
from hazm import stopwords_list
import string
from collections import defaultdict


def create_dectionary(mydict ,stemmer ,mystopwordset):

    with open("IR_data_news_10.json") as f:
        data = f.read()
    jsondata = json.loads(data)

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

            if list1[i][1] >= list2[j][1]:
                result.append(list1[i])
            else:
                result.append(list2[j])

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

def normelizer(text,stemmer ,mystopwordset):

    text = word_tokenize(text.translate(str.maketrans('', '', string.punctuation)))
    text = list(filter(None, text))
    return_list = []
    for i in range(len(text)):
        if text[i] in mystopwordset:
            continue
        return_list.append([text[i],i])
    
    return return_list


def intersect2(list1, list2, index):
    i = 0
    j = 0
    result = []
    isfinish1 = False
    isfinish2 = False
    while i < len(list1) and j < len(list2) and (isfinish1 == False and isfinish2 == False):

        if list1[i][0] == list2[j][0]:
            
            isfinish1 = False
            isfinish2 = False
            docid = list1[i][0]

            while (list1[i][0] == docid and isfinish1 == False) or  (list2[j][0] == docid and isfinish2 == False) :

                if list1[i][0] == docid and  list2[j][0] == docid and (isfinish1 == False and isfinish2 == False):

                    list1[i].append(index)
                    result.append(list1[i])
                    result.append(list2[j])

                    if i == (len(list1) - 1):
                        isfinish1 = True
                    else:
                        i += 1

                    if j == (len(list2) - 1):
                        isfinish2 = True
                    else:
                        j += 1

                    continue

                if list2[j][0] == docid and isfinish2 == False :

                    result.append(list2[j])
                    if j == (len(list2) - 1):
                        isfinish2 = True
                    else:
                        j += 1
                    continue

                if list1[i][0] == docid and isfinish1 == False:

                    list1[i].append(index)
                    result.append(list1[i])
                    if i == (len(list1) - 1):
                        isfinish1 = True
                    else:
                        i += 1
                    continue

        elif list1[i][0] < list2[j][0]:
            i += 1
        else:
            j += 1

    
    return result 

if __name__ == "__main__":

    mydict = defaultdict(list)
    stemmer = Stemmer()
    mystopwordset = set(stopwords_list())
    rankdict = defaultdict(int)
    resault = []
    isphrase = False

    create_dectionary(mydict ,stemmer ,mystopwordset)


    print("enter what you want to search")
    myinput = input()

    if myinput[0] == '"':
        isphrase = True

    myinput = list(filter(None, myinput.split('"')))

    if isphrase == True:
        #phrase search
        search_terms =  myinput.pop(0)
        print(search_terms)
        search_terms = normelizer(search_terms,stemmer ,mystopwordset)
        chunklist = []
        for i in range(1,len(search_terms)):
            chunklist.append(search_terms[i][1] - search_terms[i-1][1])
        

        search_list = []
        for i in search_terms:
            search_resualt = search_dictionary(i[0] , mydict ,stemmer)
            if len(search_resualt) == 0:
                finish()
            search_list.append(search_resualt[1])

        index = 0
        intersect_list = search_list.pop(0)
        for i in intersect_list:
            i.append(index)

        # print(intersect_list)
        for i in search_list:
            index += 1
            intersect_list = intersect2(i, intersect_list , index)
            

        intersect_list.sort(key=lambda x: [x[0],x[1]] ,reverse=False)

        whichunk = 0
        predoc = intersect_list[0][0]

        for i in range(1,len(intersect_list)):

            if predoc != intersect_list[i][0] or intersect_list[i][2] == intersect_list[i-1][2] :
                predoc = intersect_list[i][0]
                whichunk = 0
                continue

            
            predoc == intersect_list[i][0]

            if intersect_list[i][1] - intersect_list[i-1][1] != chunklist[whichunk]:
                whichunk = 0
                continue

            if whichunk == (len(chunklist) - 1):
                resault.append(predoc)
                whichunk = 0
                continue
            
            whichunk += 1
        print(resault)
                    


    if len(myinput) > 0:
        # seperate words search 
        search_terms = myinput.pop(0)
        print(search_terms)
        search_terms =  list(filter(None, search_terms.split(' ')))
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
        
        print(resault)



    # resault = search_dictionary(search_terms[0] , mydict ,stemmer)

    # print(resault)
    # ranked = ranked_results(resault ,rankdict)
    # print(ranked)

    
    


