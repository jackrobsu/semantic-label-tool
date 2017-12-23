from lexicon import *

class SingleInstance(object):
    def __init__(self):
        pass

    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,"_instance"):
            orgclass = super(SingleInstance,cls)
            cls._instance = orgclass.__new__(cls,*args,**kwargs)
        return cls._instance

    def getItem(self,ID):
        if ID in self.vocabs :
            # print(id(self.vocabs[ID]))
            return self.vocabs[ID]
        else:
            return None

    def setItem(self,content):
        if not isinstance(content,Lexicon) :
            return
        if content.wordID in self.vocabs :
            del self.vocabs[content.wordID]
        self.vocabs[content.wordID] = content

    def searchByID(self,ID):
        for w in self.vocabs :
            if w.wordID == ID :
                return w
        return None

class Verbs(SingleInstance):
    vocabs = {}
    def __init__(self):
        super(Verbs,self).__init__()

    def PrintVerbs(self):
        for w in self.vocabs.values() :
            print("w ",w)


class Conjunctions(SingleInstance):
    vocabs = {}
    def __init__(self):
        super(Conjunctions,self).__init__()

    def PrintConjunctions(self):
        for w in self.vocabs.values() :
            print("w ",w)

class Constants(SingleInstance):
    vocabs = {}
    def __init__(self):
        super(Constants,self).__init__()

    def PrintConstants(self):
        for w in self.vocabs.values() :
            print("w ",w)
            
class MessageContainer(SingleInstance):
    '''
        用來在不同类之间通信
    '''
    def __init__(self):
        super(MessageContainer,self).__init__()

    def setMessage(self,messageName,message):
        setattr(self,messageName,message)
        
    def getMessage(self,messageName):
        if hasattr(self,messageName) :
            return getattr(self,messageName)
        return None

def searchLexiconByID(lexiconID):
    if lexiconID is None :
        return None
    objects = [Verbs(),Conjunctions(),Constants()]
    for obj in objects :
        w = obj.getItem(lexiconID)
        if w is not None :
            return w
    return None


if __name__ == "__main__" :
    
    # v = Verbs()
    # c = Conjunctions()
    # print(id(v.datas))
    # print(id(c.datas))

    # v.A()
    # c.A()
    # exit(0)

    v = Verbs()
    v.setItem(Lexicon(WTYPE.VERB,0,0))
    print(v.vocabs)
    print("verbs ",id(v.vocabs))
    item = v.getItem(list(v.vocabs.keys())[0])

    vv = Verbs()
    print(vv.vocabs)
    print("verbs ",id(vv.vocabs))
    
    print("id ",id(item))

    c = Conjunctions()
    c.setItem(Lexicon(WTYPE.CONJUNCTION,0,0))
    print(c.vocabs)

    m = MessageContainer()
    m.setMessage("a",{"a":1})
    print(m.getMessage("a"))
    mm = MessageContainer()
    print(mm.getMessage("a"))
    
