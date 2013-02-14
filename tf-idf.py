
from collections import defaultdict
from multiprocessing import Pool
from bs4 import BeautifulSoup
import re
import sys
import os
import datetime
import math

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

def tf(string):
    total = 0
    words = string.split()
    wordcount = defaultdict(int)
    for word in words:
        wordcount[word] += 1
        total += 1
    for key,value in wordcount.items():
        wordcount[key] = value/total
    return wordcount

def idf(dictlist):
    numArticles = len(dictlist)
    articleCount = defaultdict(int)
    for d in dictlist:
        for key,value in d.items():
            if articleCount[key] == None:
                articleCount[key] = 0
            else:
                articleCount[key] += 1
    for key,value in articleCount.items():
        articleCount[key] = math.log10(numArticles / value)
    return articleCount

def tfidf(idfDict, tfDictList):
    tfidfList = []
    for article in tfDictList:
        for key,value in article.items():
            article[key] = idfDict[key] * value
        tfidfList.append(article)
    return tfidfList
        
if __name__ == '__main__':
    entriesDir = sys.argv[-1]
    dictionaryList = []

    # Limiting the Pool to 4 processes to prevent excess memory usage
    # pool = Pool(processes=4)
    articles = []
    for path, dirs, files in os.walk(entriesDir):
        for f in files:
            if f == "index.html":
                filePath = path + "/" + f
                data = extract_article_body(filePath)
                
                articles.append(data)
                

                
    
    tfResults = list(map(tf, articles))
    idfResults = idf(tfResults)

    tfidfList = tfidf(idfResults, tfResults)

    timestamp = str(datetime.datetime.now()) + "\n"

    with open('tfidf_output.txt', 'a+') as f:
        f.write(timestamp)
        f.write("---------------------------\n\n")
        for d in tfidfList:
            f.write(str(d.items()))
        f.write("\n")
  
