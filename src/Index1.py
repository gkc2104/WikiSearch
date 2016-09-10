import xml.sax
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
from nltk import PorterStemmer
import timeit
import sys 
output = open("../Index/index_B.txt","w")
output1 = open("../Index/TitleMap_B","w")

class WikipediaContenthandler(xml.sax.ContentHandler):
    def __init__(self):
        self.doc_flag = 0
        self.doc_title = {}
        self.regex = re.compile(r'\d+\.?\d+|[a-zA-Z0-9]+')
        self.stopwords = {}
        self.doc_map={} # dic for mapping docID to integer
        self.counter = 0 # counter for mapping docID to integer
#------------------------- Preparing Dictionary for stop words ------------------------#
        words = stopwords.words('english')
        for i in words:
            self.stopwords[i] = 1
#---------------------------------------------------------------------------------------#
        self.tag = ""

        self.docID = "" # for storing the document ID of the document
        self.title = []	# for storing the content between titels
        self.infobox = [] # for storing the content in infobox
        self.externallinks = [] # for storing the content in external links
        self.references = [] # for storing the content in references
        self.categories = [] # for storing the content in categories
        self.body_text = [] # for storing the content in body text

        self.dic = {}
        self.Infobox_tag = 0 # flag for infobox
        self.Reference_tag = 0 #flag for references
        self.External_tag = 0 #flag for external links

#------------------------------------------------------ Create Postlist for content between tags ------------------------------------- #

    def createPostList(self,content,index):
        #tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
        r = self.regex
        min_len = 0
        for i in content:
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
        if(name == "title"):
            self.doc_flag= 1


        self.Infobox_tag = 0
        self.Reference_tag = 0
        self.External_tag = 0

    def get_val(self,field,count):
        if(int(count) == 0):
            return ""
        else:
            return field + str(count)

    def endElement(self, name):
        self.tag = ""
        if(name == "page"):
            self.createPostList(self.title,0)
            self.createPostList(self.body_text,1)
            self.createPostList(self.infobox,2)
            self.createPostList(self.categories,3)
            self.createPostList(self.externallinks,4)
            self.createPostList(self.references,5)
        elif(name == "file"):
            for documentID in sorted(self.doc_title):
                output1.write(documentID + "  " + (" ").join(self.doc_title[documentID]) + "\n")
#----------------------------------------------------- Writing the final dictionary into the output file ---------------------------#
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
#-------------------------------------------------------------------------------------------------------------------------------#

#------------------------------ Set unset infotag for isolating content in infoxbox --------------------------------------------
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
#------------------------------ Set unset reftag for isolating content in References --------------------------------------------
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

#---------------------------------- Set unset exttag for isolating content in External links--------------------------------------------
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

        elif(self.tag == "id" and self.doc_flag == 1):
            self.docID = content
            self.counter += 1
            self.doc_map[self.docID] = self.counter
            self.doc_title[str(format(int(self.counter),'02x'))] = self.title
            self.doc_flag = 0
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
            else:
                self.body_text.append(content.lower())


def main(sourceFileName):
    source = open(sourceFileName)
    xml.sax.parse(source, WikipediaContenthandler())

if __name__ == "__main__":
    #timeit.Timer(main("sample.xml")).timeit()
    main("../Index/evaluate.xml")
