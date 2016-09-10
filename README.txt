Name : Kamal Gurala (201201127)


1- Requirements:
----------------
 Operating System               :       LINUX ( tested on LinuxMint)

 Compiler/Interpreter/Librarie(s):      Python,NLTK,NLTK stopwords corpus

2- Directory Structure:
-----------------------

.Phase1
├── bin
├── Index
│   └── Output_files
├── run.sh
├── runWmerge.sh
└── src
    ├── Externalmerge.py
    ├── Index1.py
    └── Index2.py



3- About the Upload 
---------------
   
   ---> src - 
   Indexing Segement -----------------------------------------------------------------------------------------------------------------------

	 Contains Index1.py , Index2.py , Externalmerge.py 

	Index1.py : It parses the entire XML file , stores it in a dictionary and then writes it onto an outputfile

	Index2.py : It parses the XML file 1MB at a time and writes it onto seperate output files

	Externalmerge.py : The Externalmerge.py merges the seperate output files into one final output file

	Format of the Datastructure Used:
	dic[word][docID] = [Title_count , Bodytext_count , Infobox_count , Categories_count , Externallinks_count , References_count ]
	
	About the code:
	
	1.) The code reads the sample XML file line by line. The WikipediaContenthandler takes appropriate actions when it encounters a start tag, end tag or content in between.
	2.) Content between Infobox,References,External links,Titles and Categories are isolated appropriately and stored seperately
	3.) The Regex "[a-zA-Z0-9]+" is used to tokenize the content. The Regex removes all special characters and punctuations.
	4.) The tokens obtained via the above regular expression are further filtered using the nltk stopwords corpus. This corpus of very frequently occuring english words which are of not much significance. All these words are stored as keys in a dictionary which is then used to check if a particular token is a stop word or not. The significance of this method is that the checking can be done in constant time.
	5.) Then the root form of the word is obtained by using the NLTK porter stemmer which is then saved in the final dic ( Structure of the dictionary is mentioned above).

	Salient Features
	-> The code removes all kinds of special characters
	-> It writes the output in a very constricted yet legible fashion. As a result the index file is very less but still can be utilized to the full extent.
	-> The index file is sorted in an alphabetical order	
	-> The code runs the entire sample.xml file in about 4 minutes
	-> The index2.py fares beter with huge datasets because it splits the dataset in segments on 1MB, processes it individually , stores them in seperate files. The Externalmerge.py merges this output files into one final index file. This method allows us to index any kind of dataset (no matter how huge) because the RAM always deals with datastructures of 1MB size (So no memory exceeded errors).
	->The docID is first mapped to a counter which starts from 1 and then converted to hexadecimal to conserve space.

	Indexfile format : Word docIDT(count)X(count)i(count)C(count)L(count)R(count)...
	T -> Title
	X -> Body Text
	i -> Infobox
	C -> Categories
	L -> External Links
	R -> References

	---------------------------------------------------------------------------------------------------------------------------------------------------------------

	Query Segment--------------------------------------------------------------------------------------------------------------------------------------------------

	Comprises of MultiIndex_DOC.py,MultiIndex_Title.py,Query.py

	The MultiIndex_DOC.py creates a multi-level index for the index obtained on 43GB wiki corpus. We split the entire sorted Index into files of 500 lines of each , 
	create index for these files and keep doing it until the number of index files obatined are less than 200. We then create a "main" index file for the top most index files. This could be visualized as a tree structure where the leaf nodes are the actual files of index and the rest of the nodes are index files on the files below them. The MultiIndex_Title.py does the same thing on the DocID - Title map file.

	The Query.py searches for the query words in the Index file , retieves the post list and calcualates the relevance of every document-word pair using T.F * I.D.F
	weight. It then prints the titles of the top 10 relevant documents.


	---------------------------------------------------------------------------------------------------------------------------------------------------------------

   
   ---> Index 

	The Index folder contains the output index files
	The folder ./Index/Split contains the Index broken into files of 500 lines each with index built on them.
	The folder ./Index/Title contains the title-docID map file broken into files of 500 lines each with index built on them.


4- NOTE :
--------------
	Please make sure that you have NLTK stopwords corpus and the NLTK package are installed before running the bash scripts
	

5 - OUTPUT :-
		./run.sh "Link to the XML document" - Gives the index file in the Index folder
		./runQuery.sh "Link to the Index file" < "Link to the query file" first buils a Multi-level Index on the index file and then runs the query file

----------------------------------------------
