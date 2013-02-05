import string


punctuation = string.punctuation
words = []
filename = raw_input("Filename Please: ")
with open(filename) as text_:
    for line in text_:
        words.append(line)

word_string = ''.join(words)
for item in string.punctuation:
    word_string = word_string.replace(item,"")
word_string.lower()

words = word_string.split()
print words

        

stop_words_place = "stop.txt"
g = open(r'%s' % stop_words_place, 'r')
stop_words = g.readlines()
g.close()



## goes through and removes \n from each stop word

for i in range(len(stop_words)):
    stop_words[i] = stop_words[i].rstrip()



## goes through words list and removes all stop words
x = 0
while x < len(words):
    if words[x] in stop_words:
        print x
        del words[x]
    print x
    x += 1
        
            
print words


