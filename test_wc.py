# Unit tests for wordcount.py

import wordcount
import unittest

class wcKnownCounts(unittest.TestCase):
    emptyString = ""
    string1 =   ("Meditation brings wisdom; lack of meditation leaves ignorance. "
                    "Know well what leads you forward and what holds you back.")
    string2 =   ("Some books are to be tasted, others to be swallowed, and some few "
                    "to be chewed and digested.")
    string3 = "You can't direct the wind, but you can adjust your sails."
    string4 =   ("The bureaucracy is expanding to meet the needs of the expanding "
                    "bureaucracy.")
    string5 = "the the the the the"

    strings = [emptyString, string1, string2, string3, string4, string5]
    theTwentyFive = [string5, string5, string5, string5, string5]

    def testCount(self):
        """
        Testing to see if wordcount can count the number of occurrences of a word in
        an article.
        """
        wcDict = wordcount.wordcount(self.emptyString)
        self.assertEqual(wcDict["what"], 0)

        wcDict = wordcount.wordcount(self.string1)
        self.assertEqual(wcDict["what"], 2)

        wcDict = wordcount.wordcount(self.string2)
        self.assertEqual(wcDict["to"], 3)

        wcDict = wordcount.wordcount(self.string3)
        self.assertEqual(wcDict["what"], 0)

        wcDict = wordcount.wordcount(self.string4)
        self.assertEqual(wcDict["bureaucracy"], 1)
        self.assertEqual(wcDict["bureaucracy."], 1)

        wcDict = wordcount.wordcount(self.string5)
        self.assertEqual(wcDict["bureaucracy."], 0)
        self.assertEqual(wcDict["the"], 5)

    def testBulkCount(self):
        """
        Testing to see if the reduce function can count the occurrence of a word
        over a list of articles.
        """
        articleList = []
        for string in self.strings:
            articleList.append(wordcount.wordcount(string))

        wcBulkDict = wordcount.reduce(articleList)

        self.assertEqual(wcBulkDict["bureaucracy"], 1)
        self.assertEqual(wcBulkDict["bureaucracy."], 1)
        self.assertEqual(wcBulkDict["bureaucracy;"], 0)
        self.assertEqual(wcBulkDict["The"], 1)
        self.assertEqual(wcBulkDict["the"], 8)
        self.assertEqual(wcBulkDict["You"], 1)
        self.assertEqual(wcBulkDict["you"], 3)
        self.assertEqual(wcBulkDict["to"], 4)
        self.assertEqual(wcBulkDict["be"], 3)

    def testTotalCount(self):
        """
        Testing to see if the reduce function returns an accurate count of the
        total number of words in all articles.
        """
        articleList = []
        for string in self.strings:
            articleList.append(wordcount.wordcount(string))

        theList = []
        for string in self.theTwentyFive:
            theList.append(wordcount.wordcount(string))

        emptyCount = wordcount.wordcount(self.emptyString)
        wcBulkDict = wordcount.reduce(articleList)
        wcTheDict = wordcount.reduce(theList)

        self.assertEqual(sum(emptyCount.values()), 0)
        self.assertEqual(sum(wcBulkDict.values()), 65)
        self.assertEqual(sum(wcTheDict.values()), 25)
            

        
if __name__ == '__main__':
    unittest.main()

