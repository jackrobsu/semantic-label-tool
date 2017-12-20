#-*- coding:utf-8 -*-
from basicWidget import BasicWidget
from utilities import *

class NounWidget(BasicWidget):
    
    def __init__(self,pWidget):
        super(NounWidget,self).__init__(pWidget,WidgetType.NOUN)
        self.splitWindow(2,4)                      
        controlContents = self.ContentAdd()  
        self.gridAdd(controlContents)

      
        self.setCentralWidget(self.splitter)
        self.resize(self.sizeHint())
        self.initialize()
        self.show()

    def ContentAdd(self):
        controlContents = []
        self.nounLabel , self.nounContent = addContent(self,"中心词",controlcontents=controlContents,num=0,signal=self.textClickSignal,tagWidth=50)
        self.possLabel , self.possContent = addContent(self,"所有格",controlcontents=controlContents,num=0,signal=self.textClickSignal,tagWidth=50,checkBoxHidden=False)
        
        self.allLabels = ["nounLabel"]
        return controlContents
    
    def gridAdd(self,controlContents):
        self.gridbox = self.gridAddForLeftWindow(controlContents,3)
        self.gridbox.setHorizontalSpacing(5)
        vbox = QVBoxLayout()
        vbox.addLayout(self.gridbox)
        self.addSaverButtonInLayout(vbox)
        self.leftWindow.setLayout(vbox)
        
    def getContent(self):
        return self.nounContent.toPlainText()