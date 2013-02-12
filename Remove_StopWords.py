import string

def remove_stop(filename):
    """Takes in a file name and removes all stop words from the file"""
    ## Removes punctuation and changes it from a string to a list
    punctuation = string.punctuation
    words = []
    with open(filename) as text_:
        for line in text_:
            words.append(line)
    
    word_string = ''.join(words)
    for item in string.punctuation:
        word_string = word_string.replace(item,"")
    word_string.lower()
    
    words = word_string.split()
    words = [element.lower() for element in words]
    
    ## opens stop file and reads the stop words in
    
    stop_words_place = "stop.txt"
    g = open(r'%s' % stop_words_place, 'r')
    stop_words = g.readlines()
    g.close()
    


    ## goes through and removes \n from each stop word
    
    for i in range(len(stop_words)):
        stop_words[i] = stop_words[i].rstrip()
    
    
    
    ## goes through words list and removes all stop words
    x = 0
    for word in words[:]:
        if word in stop_words:
            words.remove(word)
       
                
    print (words)
