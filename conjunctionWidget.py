#-*- coding:utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTabWidget
from PyQt5.QtWidgets import *
from utilities import *

class ConjunctionWidget(QMainWindow,QObject):
    textClickSignal = pyqtSignal(QWidget,int,CommonTextEdit)         #鼠标点击响应信号
    saverButtonSignal = pyqtSignal(QWidget,QWidget,QWidget)

    def __init__(self,pWidget) :
        super().__init__()
        self.pWidget = pWidget

        self.splitWindow()                      
        controlContents = self.ContentAdd()  
        self.gridAddForLeftWindow(controlContents)

      

        self.setCentralWidget(self.splitter)
        self.resize(self.sizeHint())
        self.initialize()
        self.show()

    def splitWindow(self):
        '''
            切分窗口，目前是分成左右两部分
        '''
        self.splitter = QSplitter(Qt.Horizontal)
        self.leftWindow = QWidget()
        self.rightWindow = QWidget()
        self.splitter.addWidget(self.leftWindow)
        self.splitter.addWidget(self.rightWindow)
        self.splitter.setStretchFactor(0,5)
        self.splitter.setStretchFactor(1,4)

    def ContentAdd(self):
        '''
            添加标签和文本输入框
        '''
        controlContents = []
        self.conjunctionLabel , self.conjunctionContent = addContent(self,"连词",controlcontents=controlContents,num=0,signal=self.textClickSignal)
        controlContents.append(None)
        controlContents.append(None)     
        controlContents.append(None)
        self.leftSentenceLabel , self.leftSentenceContent = addContent(self,"子句1",controlcontents=controlContents,num=1,signal=self.textClickSignal,checkBoxHidden=False)
        self.leftSentenceRoleLabel , self.leftSentenceRoleContent = addContent(self,"语义角色",controlcontents=controlContents,num=2,signal=self.textClickSignal,tagWidth=50)
        self.rightSentenceLabel , self.rightSentenceContent = addContent(self,"子句2",controlcontents=controlContents,num=3,signal=self.textClickSignal,checkBoxHidden=False)
        self.rightSentenceRoleLabel , self.rightSentenceRoleContent = addContent(self,"语义角色",controlcontents=controlContents,num=4,signal=self.textClickSignal,tagWidth=50)
        self.allLabels = ['conjunctionLabel', 'leftSentenceLabel', 'leftSentenceRoleLabel', 'rightSentenceLabel','rightSentenceRoleLabel']
        
        return controlContents

    def gridAddForLeftWindow(self,controlContents):
        '''
            把标签和文本输入框按网格方式布局
        '''
        self.gridbox = QGridLayout()
        self.gridbox.setHorizontalSpacing(5)
        numOfEachRow = 6
        for (i, tag) in enumerate(controlContents):
            row = int(i / numOfEachRow)
            col = i - row * numOfEachRow
            if tag is None :
                continue
            self.gridbox.addWidget(tag, row, col)

        self.buttonSaver = SaverButton(self,self.saverButtonSignal,self.pWidget,WidgetType.CONJUNCTION)
        self.buttonSaver.setText("保存")
        vbox = QVBoxLayout()
        vbox.addLayout(self.gridbox)
        # vbox.addStretch(1)
        vbox.addWidget(self.buttonSaver)
        self.leftWindow.setLayout(vbox)

    def initialize(self):
        self.textClickSignal.connect(textEditSelectionChanged)
        self.saverButtonSignal.connect(saveLexicon)
        self.widgetType = WidgetType.CONJUNCTION
        self.widgetID = UnionID()

    def getContent(self):
        return self.conjunctionContent.toPlainText()

    def getSubSentences(self):
        id1 = self.leftSentenceContent.lexiconID
        id2 = self.rightSentenceContent.lexiconID
        sen1 = self.leftSentenceContent.toPlainText()
        sen2 = self.rightSentenceContent.toPlainText()
        return id1 , id2 , sen1 , sen2


