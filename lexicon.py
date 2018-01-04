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
        self.belongID = None
        #与belong属性连用，一般在连词中起作用
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
        from singleInstance import searchLexiconByID
        
        if self.WType == WTYPE.CONJUNCTION :
            formerSentence = searchLexiconByID(self.formerSentenceID)
            if formerSentence is not None :
                formerString = formerSentence.getFormatString()
            else:
                formerString = None
            latterSentence = searchLexiconByID(self.latterSentenceID)
            if latterSentence is not None : 
                latterString = latterSentence.getFormatString()
            else:
                latterString = None
            return "wordType {} , mainWord {} , indexOfPlace {} , roles {} , wordID {} , formerSentenceID {} , latterSentenceID {} , formerSentence {} , latterSentence {}".format(self.typedict[self.WType],self.mainWord,self.indexOfPlace,self.roles,self.wordID,self.formerSentenceID,self.latterSentenceID,formerString,latterString)
            
        return "wordType {} , mainWord {} , indexOfPlace {} , roles {} , wordID {} , isPronoun {} , ref {} , isNegative {}".format(self.typedict[self.WType],self.mainWord,self.indexOfPlace,self.roles,self.wordID,self.isPronoun,self.ref,self.isNegative)
        
    def getFormatString(self,IDs=[]):
        from singleInstance import searchLexiconByID
        
        def getString(ID,text,existedIDs=[]):
            
            lexicon = searchLexiconByID(ID)
            print("In getFormatString, ID {} , searchID {} , lexicon {} , text {}".format(self.wordID,ID,lexicon,text))
            if lexicon is None :
                return text
            if lexicon.wordID in existedIDs :
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
            # if self.isNegative :
            #     mainWord = "¬" + self.mainWord
            # else:
            #     mainWord = self.mainWord
            mainWord = self.getVerbMainWordFormat()
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
            return self.getPronounFormat()
        else:
            return ""
        
    def getPronounFormat(self):
        if self.isPronoun :
            if "?" not in self.mainWord or ( "?" in self.mainWord and "?" != self.mainWord[0] ) :
                return "?"+self.mainWord
            else:
                return self.mainWord
        else:
            return self.mainWord

    def getVerbMainWordFormat(self):
        if self.isNegative :
            mainWord = "¬" + self.mainWord
        else:
            mainWord = self.mainWord
        return mainWord

    def getBelongFormat(self):
        from singleInstance import searchLexiconByID
        
        if self.belong is not None :
            belong = self.belong
        elif self.belongID is not None :
            word = searchLexiconByID(self.belongID)
            if word is not None :
                if word.WType == WTYPE.VERB :
                    belong = "{}.{}".format(word.originVerb,word.indexOfPlace)
                elif word.WType == WTYPE.CONJUNCTION :
                    belong = "{}.{}".format(word.mainWord,word.indexOfPlace)
                else:
                    belong = "{}.{}".format(word.mainWord,word.indexOfPlace)
            else:
                belong = None
        else:
            belong = None
        return belong

    def getFormat(self,results={},IDs=[]):
        from singleInstance import searchLexiconByID

        def isExists(words):
            #有问题，由于ID不一样，导致一样的词也会认为不一样
            w = self.originVerb if self.WType == WTYPE.VERB else self.mainWord
            for word in words :
                word = words[word]
                Word = word['word'].split("#")[0]
                if w != Word :
                    continue
                if int(self.indexOfPlace) != int(word['indexOfPlace']) :
                    continue
                belong = self.getBelongFormat()
                if belong is None :
                    belong = self.belong
                if "belong" in word and belong != word['belong'] :
                    continue
                return True
            return False
            # if self.mainWord not in words :
            #     print("ggreghr ",self.mainWord)
            #     return False
            # word = words[self.mainWord]
            # if int(self.indexOfPlace) != int(word['indexOfPlace']) :
            #     print("word ",word,self.indexOfPlace,word['indexOfPlace'])
            #     return False
            
            # belong = self.getBelongFormat()
            # if belong is None :
            #     belong = self.belong
            # if "belong" in word and belong != word['belong'] :
            #     return False
            # return True

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
            verb = "{}#{}".format(self.originVerb,self.wordID)
            if isExists(results['verb']) :
                return
            # if self.mainWord not in results['verb'] :
            results['verb'][verb] = {"ID":self.wordID,"roles":[],"word":self.mainWord,"originVerb":self.originVerb,"indexOfPlace":self.indexOfPlace,"belong":self.belong,"isleft":self.isleft,"isNegative":self.isNegative}
            for role in self.roles :
                results['verb'][verb]['roles'].append((role[0],role[1]))
            for role in self.roles :
                lexicon = searchLexiconByID(role[2])
                if lexicon is None :
                    continue
                # print("roles ",lexicon.mainWord)
                lexicon.getFormat(results,IDs)
        elif self.WType == WTYPE.CONJUNCTION :
            if isExists(results['conjunction']) :
                return
            conjunction = "{}#{}".format(self.mainWord,self.wordID)
            # if conjunction not in results['conjunction'] :
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
                if isExists(results['variable']) :
                    return
                else:
                    print("##########################")                    
                    print(self)
                    print(results['variable'])
                    print("##########################")
                pronoun = "{}#{}".format(self.mainWord,self.wordID)
                # if pronoun not in results['variable'] :
                belong = self.getBelongFormat()
                results['variable'][pronoun] = {"ID":self.wordID,"word":self.getPronounFormat(),"ref":self.ref,"indexOfPlace":self.indexOfPlace,"belong":belong}
        else:
            return
                
                
            


if __name__ == "__main__" :
    lexicon = Lexicon(0,0)