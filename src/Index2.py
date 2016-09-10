import xml.sax
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
from nltk import PorterStemmer
import sys

file_counter = 0
file_name = "../Index/Output_files/output"
abc =0

class WikipediaContenthandler(xml.sax.ContentHandler):
    def __init__(self):
        self.regex = re.compile(r'\d+\.?\d+|[a-zA-Z0-9]+')
        self.stopwords = {}
        self.doc_map={}
        self.counter = 0 # counter for mapping docID to number


#------------------------- Preparing Dictionary for stop words ------------------------#

        words = stopwords.words('english')
        words.append("ref")
        words.append("/ref")
        words.append("references")
        words.append("reflist")
        for i in words:
            self.stopwords[i] = 1

#---------------------------------------------------------------------------------------#

        self.tag = ""

        self.docID = ""
        self.title = []
        self.infobox = []
        self.externallinks = []
        self.references = []
        self.categories = []
        self.body_text = []

        self.dic = {}
        self.Infobox_tag = 0
        self.Reference_tag = 0
        self.External_tag = 0


#------------------------------------------------------ Create Postlist for content between tags ------------------------------------- #

    def createPostList(self,content,index):
        #tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
        r = self.regex
        min_len = 0
        for i in content:
            #temp = tokenizer.tokenize(i)
            temp = r.findall(i)
            filtered_words = []

#---------------------------------------------- Removing stop words ------------------------------#
            for w in temp:
                s = w
                try:
                    self.stopwords[s]
                except:
                    filtered_words.append(s)
#-------------------------------------------------------------------------------------------------#
            for word in filtered_words:
                #s = word
                s = PorterStemmer().stem_word(word) # Obtaining the root form of the token
                try:
                    self.dic[s][self.docID]
                    self.dic[s][self.docID][index] += 1
                except:
                    try:
                        self.dic[s]
                        self.dic[s][self.docID]=[0,0,0,0,0,0]
                        self.dic[s][self.docID][index] = 1
                    except:
                        self.dic[s] = {}
                        self.dic[s][self.docID]=[0,0,0,0,0,0]
                        self.dic[s][self.docID][index] = 1

#----------------------------------------------------------------------------------------------------------------------------------------------#

    def startElement(self, name, attrs):
        self.tag = name
        if(name == "page"):
            self.title = []
            self.infobox = []
            self.externallinks = []
            self.categories = []
            self.body_text = []
            self.references = []

        self.Infobox_tag = 0
        self.Reference_tag = 0
        self.External_tag = 0

    def get_val(self,field,count):
        if(int(count) == 0):
            return ""
        else:
            return field + str(count)

    def file_write(self):
        global file_counter
        file_counter += 1
        f = file_name+str(file_counter)+".txt"
        output = open(f,"w")
        s = ""
        for word in sorted(self.dic):
            s = word + " "
            for docID in self.dic[word]:
                s += str(format(int(self.doc_map[docID]),'02x'))
                s += self.get_val("T",self.dic[word][docID][0])
                s += self.get_val("X",self.dic[word][docID][1])
                s += self.get_val("i",self.dic[word][docID][2])
                s += self.get_val("C",self.dic[word][docID][3])
                s += self.get_val("L",self.dic[word][docID][4])
                s += self.get_val("R",self.dic[word][docID][5])
                s += "|"
            s = s[:-1]
            output.write(s+"\n")
        output.close()


    def endElement(self, name):
        self.tag = ""

        if(name == "page"):
            self.createPostList(self.title,0)
            self.createPostList(self.body_text,1)
            self.createPostList(self.infobox,2)
            self.createPostList(self.categories,3)
            self.createPostList(self.externallinks,4)
            self.createPostList(self.references,5)
            if(sys.getsizeof(self.dic) > 1000*1000 ):
                global abc
                abc += len(self.dic.keys())
                print abc
                self.file_write()

                self.dic = {}
        elif(name == "file"):
            b = 1
            abc += len(self.dic.keys())
            print abc
            self.file_write()


    def infotag(self,content):
        if(self.Infobox_tag == 0):
            if(content.find("{{Infobox") != -1):
                return 1
            else:
                return 0
        else:
            if(content == "}}"):
                return 0
            else:
                return 1

    def reftag(self,content):
        if(self.Reference_tag == 0):
            if(content == "==References=="):
                return 1
            else:
                return 0
        else:
            if(content.find("{{") != -1 or content.find("==") != -1 or content.find("[[") !=-1):
                return 0
            else:
                return 1

    def exttag(self,content):
        if(self.External_tag == 0):
            if(content.find("==External links==") != -1):
                return 1
            else:
                return 0
        else:
            if(content[0] != "*"):
                return 0
            else:
                return 1

    def characters(self, content):
        content = content.encode(encoding='UTF-8',errors='strict')
        stripped = content.strip()

        if((len(stripped) == 0 or len(content) <= 1)):
            return

        cat_tag = 0

        if(self.tag == "title"):
            self.title.append(content.lower())

        elif(self.tag == "id" and len(content) < 7 and content[0]=="1"):
            self.docID = content
            self.counter += 1
            self.doc_map[self.docID] = self.counter

        elif(self.tag == "text"):

            self.Infobox_tag = self.infotag(content)
            self.Reference_tag = self.reftag(content)
            self.External_tag = self.exttag(content)
            cat_tag = content[11:-2] if(content.find("[[Category:") != -1) else 0

            if(self.Infobox_tag == 1):
                if(content.find("{{Infobox") != -1):
                    self.infobox.append(content[9:].lower())
                else:
                    self.infobox.append(content.lower())
            elif(self.External_tag == 1):
                if(content.find("==External links==") == -1):
                    self.externallinks.append(content.lower())
            elif(cat_tag != 0):
                self.categories.append(cat_tag.lower())
            elif(self.Reference_tag == 1):
                self.references.append(content.lower())
                #print content,self.docID
            else:
                self.body_text.append(content.lower())


def main(sourceFileName):
    source = open(sourceFileName)
    xml.sax.parse(source, WikipediaContenthandler())

if __name__ == "__main__":
    #timeit.Timer(main("sample.xml")).timeit()
    main("../Index/sample.xml")
