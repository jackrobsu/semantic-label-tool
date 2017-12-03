#-*- coding:utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTabWidget
from PyQt5.QtWidgets import *
from utilities import *

class ConjunctionWidget(QMainWindow,QObject):
    textClickSignal = pyqtSignal(QWidget,int,CommonTextEdit)         #鼠标点击响应信号

    def __init__(self) :
        super().__init__()
         
        self.splitWindow()                      
        controlContents = self.ContentAdd()  
        self.gridAdd(controlContents)

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
        self.splitter.setStretchFactor(1,2)

    def ContentAdd(self):
        '''
            添加标签和文本输入框
        '''
        controlContents = []
        self.conjunctionLabel , self.conjunctionContent = addContent(self,"连词",controlcontents=controlContents,num=0,signal=self.textClickSignal)
        controlContents.append(None)
        controlContents.append(None)        
        self.leftSentenceLabel , self.leftSentenceContent = addContent(self,"子句1",controlcontents=controlContents,num=1,signal=self.textClickSignal)
        self.leftSentenceRoleLabel , self.leftSentenceRoleContent = addContent(self,"语义角色",controlcontents=controlContents,num=2,signal=self.textClickSignal,tagWidth=50)
        self.rightSentenceLabel , self.rightSentenceContent = addContent(self,"子句2",controlcontents=controlContents,num=3,signal=self.textClickSignal)
        self.rightSentenceRoleLabel , self.rightSentenceRoleContent = addContent(self,"语义角色",controlcontents=controlContents,num=4,signal=self.textClickSignal,tagWidth=50)
        self.allLabels = ['conjunctionLabel', 'leftSentenceLabel', 'leftSentenceRoleLabel', 'rightSentenceLabel','rightSentenceRoleLabel']
        
        return controlContents

    def gridAdd(self,controlContents):
        '''
            把标签和文本输入框按网格方式布局
        '''
        self.gridbox = QGridLayout()
        self.gridbox.setHorizontalSpacing(0)
        numOfEachRow = 4
        for (i, tag) in enumerate(controlContents):
            row = int(i / numOfEachRow)
            col = i - row * numOfEachRow
            if tag is None :
                continue
            self.gridbox.addWidget(tag, row, col)
        self.leftWindow.setLayout(self.gridbox)

    def initialize(self):
        self.textClickSignal.connect(textEditSelectionChanged)
