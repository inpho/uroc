# Unit test for tf-idf.py

import tfidf
import unittest
import math

class tfKnownStrings(unittest.TestCase):
    emptyString = ""
    string1 =   ("Meditation brings wisdom; lack of meditation leaves ignorance. "
                    "Know well what leads you forward and what holds you back.")
    string2 =   ("Some books are to be tasted, others to be swallowed, and some few "
                    "to be chewed and digested.")
    string3 = "You can't direct the wind, but you can adjust your sails."
    string4 =   ("The bureaucracy is expanding to meet the needs of the expanding "
                    "bureaucracy.")
    string5 = "the the the the the"

    def testLength(self):
        """
        Testing the lengths of the dictionaries to see if they hold an
        accurate count of unique words.
        """
        tfDict = tfidf.tf(self.emptyString)
        self.assertEqual(len(tfDict), 0)

        tfDict = tfidf.tf(self.string1)
        self.assertEqual(len(tfDict), 17)

        tfDict = tfidf.tf(self.string2)
        self.assertEqual(len(tfDict), 13)

        tfDict = tfidf.tf(self.string3)
        self.assertEqual(len(tfDict), 11)

        tfDict = tfidf.tf(self.string4)
        self.assertEqual(len(tfDict), 10)

        tfDict = tfidf.tf(self.string5)
        self.assertEqual(len(tfDict), 1)

    def testKnownTF(self):
        tfDict = tfidf.tf(self.string1)
        self.assertEqual(tfDict["meditation"], (1/19))

        tfDict = tfidf.tf(self.string2)
        self.assertEqual(tfDict["be"], (3/18))

        tfDict = tfidf.tf(self.string3)
        self.assertEqual(tfDict["dog"], (0/11))

        tfDict = tfidf.tf(self.string4)
        self.assertEqual(tfDict["bureaucracy."], (1/12))

        tfDict = tfidf.tf(self.string5)
        self.assertEqual(tfDict["the"], (5/5))

class idfKnownDictList(unittest.TestCase):
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

    articleList = []
    theList = []

    for string in strings:
        articleList.append(tfidf.tf(string))

    for string in theTwentyFive:
        theList.append(tfidf.tf(string))

    def testKnownIDF(self):
        idfDict = tfidf.idf(self.articleList)

        self.assertEqual(idfDict["the"], math.log10(6/3))
        self.assertEqual(idfDict["books"], math.log10(6/1))
        self.assertEqual(idfDict["dog"], 0.0)

        idfDict = tfidf.idf(self.theList)
        self.assertEqual(idfDict[""], 0.0)
        self.assertEqual(idfDict["the"], math.log10(5/5))

class tfidfKnownValues(unittest.TestCase):
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
    
    def testArticleOrder(self):
        articleList = []

        for string in self.strings:
            articleList.append(tfidf.tf(string))

        self.assertEqual(articleList[1]["Meditation"], (1/19))
        self.assertEqual(articleList[2]["be"], (3/18))
        self.assertEqual(articleList[3]["can't"], (1/11))
        self.assertEqual(articleList[4]["bureaucracy."], (1/12))
        self.assertEqual(articleList[5]["the"], (5/5))

    def testKnownTFIDF(self):
        articleList = []
        theList = []

        for string in self.strings:
            articleList.append(tfidf.tf(string))

        for string in self.theTwentyFive:
            theList.append(tfidf.tf(string))

        idfArtDict = tfidf.idf(articleList)
        idfTheDict = tfidf.idf(theList)

        tfidfArtList = tfidf.tfidf(idfArtDict, articleList)
        tfidfTheList = tfidf.tfidf(idfTheDict, theList)

        self.assertEqual(tfidfArtList[1]["Meditation"], math.log10(6/1) * (1/19))
        self.assertEqual(tfidfArtList[2]["books"], math.log10(6/1) * (1/18))
        self.assertEqual(tfidfArtList[5]["the"], math.log10(6/3) * (5/5))
        
        self.assertEqual(tfidfTheList[3]["the"], math.log10(5/5) * (5/5))
        

if __name__ == '__main__':
    unittest.main()

