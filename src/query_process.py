def find_word(x):
    f = open('Index/main')
    dump = f.readlines()
    levels = int(dump[0][:-1])

    for i in range(1,len(dump)):
        if(i<len(dump)-1):
            if(dump[i][:-1].split()[0] <= x and dump[i+1][:-1].split()[0] > x):
                next_num = dump[i][:-1].split()[1]
                flag = 1
                break
        else:
            next_num = dump[i][:-1].split()[1]

    while(levels > 0):
        levels -= 1
        name = 'Index/' + str(levels) + str(next_num)
        f = open(name)
        dump = f.readlines()
        for i in range(0,len(dump)):
            if(i<len(dump)-1):
                if(dump[i][:-1].split()[0] <= x and dump[i+1][:-1].split()[0] > x):
                    next_num = dump[i][:-1].split()[1]
                    flag = 1
                    break
            else:
                next_num = dump[i][:-1].split()[1]

    found = 0
    f = open('Index/' + str(next_num))
    dump = f.readlines()
    for i in range(0,len(dump)):
        if(i<len(dump)-1):
            if(dump[i][:-1].split()[0] == x):
                return dump[i][:-1]
    return 'not_found'

def find_title(x):
    f = open('Title/main')
    dump = f.readlines()
    levels = int(dump[0][:-1])

    for i in range(1,len(dump)):
        if(i<len(dump)-1):
            if(dump[i][:-1].split()[0] <= x and dump[i+1][:-1].split()[0] > x):
                next_num = dump[i][:-1].split()[1]
                flag = 1
                break
        else:
            next_num = dump[i][:-1].split()[1]

    while(levels > 0):
        levels -= 1
        name = 'Title/' + str(levels) + str(next_num)
        f = open(name)
        dump = f.readlines()
        for i in range(0,len(dump)):
            if(i<len(dump)-1):
                if(dump[i][:-1].split()[0] <= x and dump[i+1][:-1].split()[0] > x):
                    next_num = dump[i][:-1].split()[1]
                    flag = 1
                    break
            else:
                next_num = dump[i][:-1].split()[1]

    found = 0
    f = open('Title/' + str(next_num))
    dump = f.readlines()
    for i in range(0,len(dump)):
        if(i<len(dump)-1):
            if(dump[i][:-1].split()[0] == x):
                return dump[i][:-1]
    return 'not_found'




import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import re
doc_dict = {}
score_dict = {}
stemmer = PorterStemmer()
stop = stopwords.words('english')
stop_dict = {}
for i in stop:
    sm = stemmer.stem(i)
    stop_dict[sm] = 1
tokenizer = RegexpTokenizer('\d+\.?\d+|[a-zA-Z0-9]+')
a = ['T','I','X','R','E','C']
score = {'T':300.0,'I':75.0,'X':30.0,'R':55.0,'E':45.0,'C':60}


t = input()
for l in range(int(t)):
    x = raw_input()
    words = x.split()
    word_flag = {}
    flag_arr = [1,1,1,1,1,1]
    for i in range(len(words)):
        if(words[i][0:2] == 't:'):
            words[i] = words[i][2:]
            words[i] = stemmer.stem(words[i])
            try:
                stop_dict[words[i]]
            except:
                word_flag[words[i]] = [1,0,0,0,0,0]
        elif(words[i][0:2] == 'i:'):
            words[i] = words[i][2:]
            words[i] = stemmer.stem(words[i])
            try:
                stop_dict[words[i]]
            except:
                word_flag[words[i]] = [0,1,0,0,0,0]
        elif(words[i][0:2] == 'b:'):
            words[i] = words[i][2:]
            words[i] = stemmer.stem(words[i])
            try:
                stop_dict[words[i]]
            except:
                word_flag[words[i]] = [0,0,1,0,0,0]
        elif(words[i][0:2] == 'r:'):
            words[i] = words[i][2:]
            words[i] = stemmer.stem(words[i])
            try:
                stop_dict[words[i]]
            except:
                word_flag[words[i]] = [0,0,0,1,0,0]
        elif(words[i][0:2] == 'e:'):
            words[i] = words[i][2:]
            words[i] = stemmer.stem(words[i])
            try:
                stop_dict[words[i]]
            except:
                word_flag[words[i]] = [0,0,0,0,1,0]
        elif(words[i][0:2] == 'c:'):
            words[i] = words[i][2:]
            words[i] = stemmer.stem(words[i])
            try:
                stop_dict[words[i]]
            except:
                word_flag[words[i]] = [0,0,0,0,0,1]
        else:
            words[i] = stemmer.stem(words[i])
            try:
                stop_dict[words[i]]
            except:
                word_flag[words[i]] = flag_arr


    main_dict = {}
    for i in words:
        temp = i
        try:
            stop_dict[temp]
        except:
            s = find_word(temp)
            if(s!='not_found'):
                spl = s.split()
                key = spl[0]
                docs = spl[1]
                docs = docs.split('|')
                temp1_dict = {}
                for i in docs:
                    temp_dict = {}
                    curr_doc = i
                    for j in range(len(a)):
                        temp_dict[a[j]] = 0
                    for j in range(len(a)):
                        temp = curr_doc.split(a[len(a)-1-j])
                        if(len(temp)>1):
                            temp_dict[a[len(a)-1-j]] += int(temp[1])
                        curr_doc = temp[0]
                    temp1_dict[curr_doc] = temp_dict
                main_dict[key] = temp1_dict
    dict_count = {}
    for i in word_flag:
        for j in main_dict[i]:
            if(j!=''):
                for k in range(len(a)):
                    try:
                        dict_count[j] += (main_dict[i][j][a[k]]*score[a[k]]*word_flag[i][k])/len(main_dict[i].keys())
                    except:
                        dict_count[j] = (main_dict[i][j][a[k]]*score[a[k]]*word_flag[i][k])/len(main_dict[i].keys())

    deci_store_dict = {}

    for i in dict_count:
        t = int(i,16)
        deci_store_dict[t] = dict_count[i]

    import operator
    sorted_dict = sorted(deci_store_dict.items(), key=operator.itemgetter(1),reverse=True)
    for i in range(10):
        try:
            t = find_title(str(sorted_dict[i][0]))
            if(t!='not_found'):
                print t#,' score = ',sorted_dict[i][1]
        except:
            continue