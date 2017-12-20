#-*- coding:utf-8 -*-
from basicWidget import BasicWidget
from utilities import *

class NounWidget(BasicWidget):
    
    def __init__(self,pWidget):
        super(NounWidget,self).__init__(pWidget,WidgetType.NOUN)
        self.splitWindow()                      
        controlContents = self.ContentAdd()  
        self.gridAdd(controlContents)

      
        self.setCentralWidget(self.splitter)
        self.resize(self.sizeHint())
        self.initialize()
        self.show()

    def ContentAdd(self):
        controlContents = []
        self.nounLabel , self.nounContent = addContent(self,"名词",controlcontents=controlContents,num=0,signal=self.textClickSignal)
        self.allLabels = ["nounLabel"]
        return controlContents
    
    def gridAdd(self,controlContents):
        self.gridbox = self.gridAddForLeftWindow(controlContents)
        vbox = QVBoxLayout()
        vbox.addLayout(self.gridbox)
        self.addSaverButtonInLayout(vbox)
        self.leftWindow.setLayout(vbox)
        
    def getContent(self):
        return self.nounContent.toPlainText()