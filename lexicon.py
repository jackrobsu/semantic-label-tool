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
        WTYPE.PRONOUN:"Pronoun",
        WTYPE.CONSTANT:"Constant"
    }
    def __init__(self,wordID,wtype,mainWord,roles={},indexOfPlace=None):
        self.WType = wtype
        self.mainWord = mainWord
        self.roles = roles
        self.wordID = wordID

        #原句中的位置，如果是多个词构成的，则用第一个单词在原句中的位置来表示
        self.indexOfPlace = indexOfPlace
        #表示在连词中的位置，只有当该词多短语属于连词的某一成分时有效
        self.indexInConjunction = None
        #属于哪个词或短语
        self.belong = None
        
        #与belong属性连用
        self.isleft = None
        
        #for verb
        self.originVerb = None
        self.isNegative = False

        # for conjunction
        self.formerSentence = None
        self.latterSentence = None
        self.formerSentenceID = None
        self.latterSentenceID = None
        self.conjunctionRole = {}

        #for constant
        self.isPronoun = False
        self.ref = None

    def __str__(self):
        return "wordType {} , mainWord {} , roles {} , wordID {} , isPronoun {} , ref {} , isNegative {}".format(self.typedict[self.WType],self.mainWord,self.roles,self.wordID,self.isPronoun,self.ref,self.isNegative)
        
    def getFormatString(self,IDs=[]):
        from singleInstance import searchLexiconByID
        
        def getString(ID,text,existedIDs=[]):
            
            lexicon = searchLexiconByID(ID)
            print("In getFormatString, ID {} , searchID {} , lexicon {} , text {}".format(self.wordID,ID,lexicon,text))
            if lexicon is None :
                return text
            if self.wordID in existedIDs :
                return text
            else:
                # print("in searched word ",lexicon.wordID," mainword ", lexicon.mainWord)
                existedIDs.append(lexicon.wordID)
                return lexicon.getFormatString(IDs=existedIDs)
                # return lexicon.mainWord
        if self.WType == WTYPE.VERB :

            rolestring = None
            if self.roles :
                rolestring = ",".join(["{}"]*len(self.roles))
                String = []
                for role in self.roles :
                    if self.wordID not in IDs :
                        IDs.append(self.wordID)
                    string = getString(role[2],role[1],IDs)
                    String.append(string)
                    IDs = [self.wordID]
                rolestring = rolestring.format(*String)
                # rolestring = rolestring.format(*[ getString(role[2],role[1],IDs) for role in self.roles] )
            if self.isNegative :
                mainWord = "¬" + self.mainWord
            else:
                mainWord = self.mainWord
            if rolestring is not None :
                return "{}({})".format(mainWord,rolestring)
            else:
                return "{}".format(mainWord)
        elif self.WType == WTYPE.CONJUNCTION :
            if self.wordID not in IDs :
                IDs.append(self.wordID)
            substring1 = getString(self.formerSentenceID,self.formerSentence,IDs)
            IDs = [self.wordID]
            substring2 = getString(self.latterSentenceID,self.latterSentence,IDs)
            return "{}({},{})".format(self.mainWord,substring1,substring2)
        elif self.WType == WTYPE.NOUN :
            return "{}".format(self.mainWord)
        elif self.WType == WTYPE.CONSTANT :
            if self.isPronoun :
                return "?"+self.mainWord
            else:
                return self.mainWord
        else:
            return ""

    def getFormat(self,results={},IDs=[]):
        from singleInstance import searchLexiconByID
        # print("jinru ",self)
        # print("@@@@@@@@" , IDs , self.wordID in IDs)
        if self.wordID not in IDs :
            IDs.append(self.wordID)
        else:
            return
        if "verb" not in results :
            results['verb'] = {}
        if "conjunction" not in results :
            results['conjunction'] = {}
        if "variable" not in results :
            results['variable'] = {}
        if self.WType == WTYPE.VERB :
            verb = "{}#{}".format(self.mainWord,self.wordID)
            if self.mainWord not in results['verb'] :
                results['verb'][verb] = {"ID":self.wordID,"roles":[],"word":self.mainWord,"originVerb":self.originVerb,"indexOfPlace":self.indexOfPlace,"belong":self.belong,"isleft":self.isleft}
            for role in self.roles :
                results['verb'][verb]['roles'].append((role[0],role[1]))
            for role in self.roles :
                lexicon = searchLexiconByID(role[2])
                if lexicon is None :
                    continue
                # print("roles ",lexicon.mainWord)
                lexicon.getFormat(results,IDs)
        elif self.WType == WTYPE.CONJUNCTION :
            conjunction = "{}#{}".format(self.mainWord,self.wordID)
            if conjunction not in results['conjunction'] :
                results['conjunction'][conjunction] = {"ID":self.wordID,"role":self.conjunctionRole,"word":self.mainWord,"indexOfPlace":self.indexOfPlace,"belong":self.belong,"isleft":self.isleft}
            leftlexicon = searchLexiconByID(self.formerSentenceID)
            rightlexicon = searchLexiconByID(self.latterSentenceID)
            # print("leftlexicon is ",leftlexicon)
            # print("rightlexicon is ",rightlexicon)
            
            if leftlexicon is not None :
                # print("leftlexicon ",leftlexicon.mainWord)                
                leftlexicon.getFormat(results,IDs)
            if rightlexicon is not None :
                # print("rightlexicon ",rightlexicon.mainWord)
                rightlexicon.getFormat(results,IDs)
        elif self.WType == WTYPE.CONSTANT :
            if self.isPronoun :
                pronoun = "{}#{}".format(self.mainWord,self.wordID)
                if pronoun not in results['variable'] :
                    results['variable'][pronoun] = {"ID":self.wordID,"word":self.mainWord,"ref":self.ref,"indexOfPlace":self.indexOfPlace,"belong":self.belong}
        else:
            return
                
                
            


if __name__ == "__main__" :
    lexicon = Lexicon(0,0)