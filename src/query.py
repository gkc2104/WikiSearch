#--------------------------------------Import Libraries----------------------------------------------------------------#
import math
import operator
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
from nltk import PorterStemmer
from nltk.corpus import wordnet as wn
import time

#----------------------------------------------------------------------------------------------------------------------#


#--------------------------------------Global Initializations----------------------------------------------------------#
map_fields = { "T":0 , "X":1 , "i":2 , "C":3 , "L":4 , "R":5}
reverse_fields = { "0":"T" , "1":"X" , "2":"i" , "3":"C" , "4":"L" , "5":"R"}
map = { "t":"T" , "b":"X" , "i":"i" , "c":"C" , "e":"L" , "r":"R"}
map_weight = { "0":350.0 , "1":10.0 , "2":100.0 , "3":75.0 , "4":50.0 , "5":60.0}
Index_dir = "../Index/Split1/"
main = open(Index_dir + "main").readlines()
N = 200000 # Total number of documents
words = stopwords.words('english')
stopwords_dict = {}
for i in words:
    stopwords_dict[i] = 1
#----------------------------------------------------------------------------------------------------------------------#


#------------------------Remove stop words and stem the tokens in the given query--------------------------------------#
def process_query(q):
    temp = q.split(" ")
    a = []
    categories = []
    for word1 in temp:
        t = word1.split(":")
        if(len(t) == 1):
            word = t[0].lower()
            try:
                stopwords_dict[word]
            except:
                s = PorterStemmer().stem_word(word)
                a.append(s)
                categories.append("NA")
        else:
            word = t[1]
            cat = t[0]
            try:
                stopwords_dict[word]
            except:
                s = PorterStemmer().stem_word(word)
                a.append(s)
                categories.append(cat)
    return [a,categories]
#----------------------------------------------------------------------------------------------------------------------#


#-------------------------Find for the given word in the document------------------------------------------------------#
def binary_search(Index_lines,word,start,end):
    if(start > end):
        return "Not Found"
    mid = (start + end )/2
    temp = Index_lines[mid].split(" ")
    if(word > temp[0]):
        return binary_search(Index_lines,word,mid+1,end)
    elif (word < temp[0]):
        return binary_search(Index_lines,word,start,mid-1)
    else:
        return temp[1]
#----------------------------------------------------------------------------------------------------------------------#


#---------------------------Find the appropriate leaf file from the multi-level index setup-------------------#
def find_file(word,root):
    Index_lines = root
    while(Index_lines[0].find("NotLeaf") != -1):
        line = 0
        while (line < (len(Index_lines)-1)):
            temp = Index_lines[line].split(" ")
            if(temp[0] <= word and Index_lines[line+1].split(" ")[0] > word):
                Index_lines = open(Index_dir + temp[1]).readlines()
                break
            line += 1
        if(line == (len(Index_lines)-1)):
            Index_lines = open(Index_dir + Index_lines[line].split(" ")[1]).readlines()
    return binary_search(Index_lines,word,0,len(Index_lines)-1)
#----------------------------------------------------------------------------------------------------------------------#


#--------------------------------Split the post list into DocID and field count--------------------------------#
def get_docID(document):
    docID = ""
    list = ""
    flag = 0
    count_list = []
    for c in document:
        if(c.isupper() or c == "i"):
            flag = 1
        if(flag == 0):
            docID += c
        else:
            if(c.isalpha()):
                list+= " " + c + " "
            else:
                list += c
    count_list = [0,0,0,0,0,0]
    list = list[1:]
    splitList = list.split(" ")
    j = 0
    while(j < len(splitList)):
        count_list[map_fields[splitList[j]]] += int(splitList[j+1])
        j = j + 2
    return [docID,count_list,list]
#----------------------------------------------------------------------------------------------------------------------#


#------------Calculate the relevance of each document with the given query using T.F * I.D.F as the heuristic----------#
def RankDocuments(query_words):
    for i in range(len(query_words)):
        postlist = find_file(query_words[i],main)
        Rank_document = {}
        if(postlist != "Not Found"):
            postlist = postlist.split("|")
            postlist[-1] = postlist[-1][:-1]
            doc_freq = {}
            term_freq = 0
            for x in postlist:
                temp = get_docID(x)
                doc_freq[temp[0]] = temp[1]
                term_freq += 1
            for doc in doc_freq:
                weight = 0
                for field in range(len(doc_freq[doc])):
                    if(categories[i] == "NA"):
                        weight += doc_freq[doc][field]*map_weight[str(field)] * math.log(N/(term_freq*1.0))
                    else:
                        if(map[categories[i]] == reverse_fields[str(field)]):
                            weight += doc_freq[doc][field]*map_weight[str(field)] * math.log(N/(term_freq*1.0))
                try:
                    Rank_document[doc] += weight
                except:
                    Rank_document[doc] = weight
    try:
        return Rank_document
    except:
        return -1
#----------------------------------------------------------------------------------------------------------------------#



#-----------------------------Search the title of the corresponding DOC ID---------------------------------------------#
def binary_search_title(Index_lines,word,start,end):
    mid = (start + end )/2
    temp = Index_lines[mid].split(" ",1)
    if(int(word) > int(temp[0])):
        return binary_search_title(Index_lines,word,mid+1,end)
    elif (int(word) < int(temp[0])):
        return binary_search_title(Index_lines,word,start,mid-1)
    else:
        return temp[1]
#----------------------------------------------------------------------------------------------------------------------#


#---------------------------Find the appropriate title from the multi-level index setup--------------------------------#
def find_file_title(word,root):
    Index_lines = root
    while(Index_lines[0].find("NotLeaf") != -1):
        line = 0
        while (line < (len(Index_lines)-1)):
            temp = Index_lines[line].split(" ")
            if(int(temp[0]) <= int(word) and int(Index_lines[line+1].split(" ")[0]) > int(word)):
                Index_lines = open(Index_dir + temp[1]).readlines()
                #print word,Index_dir + temp[1],temp[0]
                break
            line += 1
        if(line == (len(Index_lines)-1)):
            Index_lines = open(Index_dir + Index_lines[line].split(" ")[1]).readlines()

    return binary_search_title(Index_lines,word,0,len(Index_lines)-1)
#----------------------------------------------------------------------------------------------------------------------#



#-----------------------------------------------------MAIN PROGRAM-----------------------------------------------------#
Query = raw_input()
start = time.clock()
processedQuery = process_query(Query)
query_words = processedQuery[0]
categories = processedQuery[1]
Rank_document = RankDocuments(query_words)
if(Rank_document != -1):
    Index_dir = "../Index/Title/"
    main = open(Index_dir + "main").readlines()
    sorted_x = sorted(Rank_document.items(), key=operator.itemgetter(1),reverse = True)
    if(len(sorted_x) == 0):
        print "No documents found"
    else:
        count = 0
        for i in range(len(sorted_x)):
            count += 1
            if(count > 10):
                break
            docID = sorted_x[i][0]
            title = find_file_title(docID,main)
            print title[:-1]
else:
    print "No documents found"
#----------------------------------------------------------------------------------------------------------------------#

elapsed = (time.clock() - start)
print "TIME TAKEN"
print "%.2gs" %elapsed

