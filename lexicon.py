from enum import Enum
from utilities import *

class WTYPE(Enum):
    VERB = 0
    CONJUNCTION = 1
    PROPOSITION = 2
    NOUN = 3
    VARIABLE = 4
    PRONOUN = 5
    CONSTANT = 6

class Lexicon():
    typedict = {
        WTYPE.VERB:"Verb",
        WTYPE.CONJUNCTION:"Conjunction",
        WTYPE.PROPOSITION:"ProPosition",
        WTYPE.NOUN:"Noun",
        WTYPE.VARIABLE:"Variable",
        WTYPE.PRONOUN:"Pronoun"
    }
    def __init__(self,wordID,wtype,mainWord,roles={}):
        self.WType = wtype
        self.mainWord = mainWord
        self.roles = roles
        self.wordID = wordID

        # for conjunction
        self.formerSentence = None
        self.latterSentence = None
        self.formerSentenceID = None
        self.latterSentenceID = None

    def __str__(self):
        return "wordType {} , mainWord {} , roles {} , wordID {}".format(self.typedict[self.WType],self.mainWord,self.roles,self.wordID)
        
    def getFormatString(self,leftexistedIDs=[],rightexistedIDs=[]):
        from singleInstance import searchLexiconByID
        
        def getStringInConjunction(ID,text,existedIDs=[]):
            
            lexicon = searchLexiconByID(ID)
            print("ID {} , searchID {} , lexicon {} , text {}".format(self.wordID,ID,lexicon,text))
            if lexicon is None :
                return text
            if self.wordID in existedIDs :
                return text
            else:
                # print("in searched word ",lexicon.wordID," mainword ", lexicon.mainWord)
                existedIDs.append(lexicon.wordID)
                return lexicon.getFormatString(existedIDs)
                # return lexicon.mainWord
        if self.WType == WTYPE.VERB :
            rolestring = None
            if self.roles :
                rolestring = ",".join(["{}"]*len(self.roles))
                rolestring = rolestring.format(*[ role[1] for role in self.roles] )
            if rolestring is not None :
                return "{}({})".format(self.mainWord,rolestring)
            else:
                return "{}".format(self.mainWord)
        elif self.WType == WTYPE.CONJUNCTION :
            substring1 = getStringInConjunction(self.formerSentenceID,self.formerSentence,leftexistedIDs)
            substring2 = getStringInConjunction(self.latterSentenceID,self.latterSentence,rightexistedIDs)
            return "{}({},{})".format(self.mainWord,substring1,substring2)
        elif self.WType == WTYPE.NOUN :
            return "{}".format(self.mainWord)
        else:
            return "None"
            


if __name__ == "__main__" :
    lexicon = Lexicon(0,0)