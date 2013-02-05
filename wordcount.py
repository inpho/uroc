from collections import defaultdict
from multiprocessing import Pool
from BeautifulSoup import BeautifulSoup
import re
import sys
import os
import datetime

def extract_article_body(filename):
    """
    Extracts the article body from the SEP article at the given filename. Some
    error handling is done to guarantee that this function returns at least the
    empty string. Check the error log.
    """
    print filename
    with open(filename) as f:
        doc = f.read()
    soup = BeautifulSoup(doc, convertEntities=["xml", "html"])

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
    words = string.split()
    count = defaultdict(int)
    for word in words:
        count[word] += 1
    return count

def reduce(dictlist):
    count = defaultdict(int)
    for d in dictlist:
        for key,value in d.iteritems():
            count[key] += value
    return count

# 1. inpho.corpus.sep.extract_article_body can get just the text
# 2. actually getting the list of all articles: inpho.corpus.sep.get_titles()

if __name__ == '__main__':
    entriesDir = sys.argv[-1]
    dictionaryList = []

    for path, dirs, files in os.walk(entriesDir):
        for f in files:
            if f.endswith(".html"):
                filePath = path + "/" + f
                data = extract_article_body(filePath)
            
                #Threading disabled for my virtual test machine
                #pool = Pool()
                #results = pool.map(wordcount, data.split())

                #Non pooled:
                results = map(wordcount, data.split())

                subDict = reduce(results)
                maxvalue = max(subDict.values())

                tfDict = defaultdict(int)

                for key,value in subDict:
                    tfDict[key] = value / maxvalue
                
                print tfDict.items()
                dictionaryList.append(subDict)
                tfList.append(tfDict)
    
    #data = extract_article_body(filename)    
    #pool = Pool()
    #results = pool.map(wordcount, data.split())

    finalDict = reduce(dictionaryList)

    timestamp = str(datetime.datetime.now()) + "\n"

    with open('wc_output.txt', 'a+') as f:
        f.write(timestamp)
        f.write("---------------------------\n\n")
        f.write(str(finalDict.items()))
        f.write("\n")

    #print(finalDict.items())    
