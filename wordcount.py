from collections import defaultdict
from multiprocessing import Pool
from bs4 import BeautifulSoup
import re
import sys
import os
import datetime
import time

# Logging is disabled since it is not available
def extract_article_body(filename):
    """
    Extracts the article body from the SEP article at the given filename. Some
    error handling is done to guarantee that this function returns at least the
    empty string. Check the error log.
    """
    print(filename)
    with open(filename) as f:
        # Some files are not properly encoded in UTF-8, this ignores them
        try:
            doc = f.read()
        except UnicodeDecodeError:
            return ''

    # ConvertEntities is not available in BeautifulSoup4 so it has been removed
    soup = BeautifulSoup(doc)

    # rip out bibliography
    biblio_root = soup.findAll('h2', text='Bibliography')
    if biblio_root:
        biblio_root = biblio_root[-1].findParent('h2')
        if biblio_root:
            biblio = [biblio_root]
            biblio.extend(biblio_root.findNextSiblings())
            biblio = [elm.extract() for elm in biblio]
        #else:
            #logging.error('Could not extract bibliography from %s' % filename)

    # grab modified body 
    body = soup.find("div", id="aueditable")
    if body is not None:
        # remove HTML escaped characters
        body = re.sub("&\w+;", "", body.text)
    
        return body
    else:
        #logging.error('Could not extract text from %s' % filename)

        return ''

def wordcount(string):
    """
    Takes a string as input and returns a defaultdict containing each word
    in the string associated with the number of times it occurs in the string.
    """
    words = string.split()
    count = defaultdict(int)
    for word in words:
        count[word] += 1
    return count

def reduce(dictlist):
    """
    Takes a list of defaultdicts as input and returns a single defaultdict
    containing each word in the entireity of the corpus associated with the
    number of times each word occurs in the corpus.
    """
    count = defaultdict(int)
    for d in dictlist:
        for key,value in d.items():
            count[key] += value
    return count

# 1. inpho.corpus.sep.extract_article_body can get just the text
# 2. actually getting the list of all articles: inpho.corpus.sep.get_titles()

if __name__ == '__main__':
    entriesDir = sys.argv[-1]

    #Start timing
    startTime = time.clock()    
    dictionaryList = []

    # Limiting the Pool to 4 processes to prevent excess memory usage
    pool = Pool(processes=4)
    articles = []
    for path, dirs, files in os.walk(entriesDir):
        for f in files:
            if f == "index.html":
                filePath = path + "/" + f
                data = extract_article_body(filePath)
                articles.append(data)           
    
    results = pool.map(wordcount, articles)

    finalDict = reduce(results)

    # Finish timing
    endTime = time.clock()
    timestamp = str(datetime.datetime.now()) + "\n"   
    elapsedTime = str(endTime - startTime) + " seconds \n"

    with open('wc_output.txt', 'a+') as f:
        f.write(timestamp + elapsedTime)
        f.write("---------------------------\n\n")
        for key,value in sorted(finalDict.items(), key=lambda x:x[1], reverse=True):
            line = key + " , " + str(value) + "\n"
            f.write(line)
  
