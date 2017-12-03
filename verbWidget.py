#!/usr/bin/env python
# encoding: utf-8
import sys
from utilities import *


class VerbWidget(QMainWindow,QObject):
    textClickSignal = pyqtSignal(QWidget, int, CommonTextEdit)

    def __init__(self):
        super().__init__()
        self.leftWindow = QWidget()
        controlcontents = []
        contentWidth = 150
        tagWidth = 40
        (self.verb,self.verbContent) = addContent(self,'动词', controlcontents, 0 , self.textClickSignal,tagWidth=tagWidth,contentWidth=contentWidth)
        (self.role1,self.roleContent1) = addContent(self,'role1', controlcontents, 1 , self.textClickSignal,tagWidth=tagWidth,contentWidth=contentWidth)
        (self.role2,self.roleContent2) = addContent(self,'role2', controlcontents, 2 , self.textClickSignal,tagWidth=tagWidth,contentWidth=contentWidth)
        (self.role3,self.roleContent3) = addContent(self,'role3', controlcontents, 3 , self.textClickSignal,tagWidth=tagWidth,contentWidth=contentWidth)
        self.allLabels = ['verb', 'role1', 'role2', 'role3']
        self.gridbox = QGridLayout()
        self.gridbox.setHorizontalSpacing(0)
        numOfEachRow = 2
        print(len(controlcontents))
        for (i, tag) in enumerate(controlcontents):
            row = int(i / numOfEachRow)
            col = i - row * numOfEachRow
            self.gridbox.addWidget(tag, row, col)

        self.leftWindow.setLayout(self.gridbox)
       
        leftWindowWidth = self.width() / 4
        if leftWindowWidth < contentWidth + tagWidth:
            pass
        leftWindowWidth = leftWindowWidth
        # self.leftWindow.resize(leftWindowWidth, self.height())
        self.rightWindow = QWidget()
        self.rightWindow.resize(self.width() - leftWindowWidth, self.height())
        self.hsplitter = QSplitter(Qt.Horizontal)
        self.hsplitter.addWidget(self.leftWindow)
        self.hsplitter.addWidget(self.rightWindow)
        self.hsplitter.setStretchFactor(0,2)
        self.hsplitter.setStretchFactor(1,3)
        self.setCentralWidget(self.hsplitter)
        self.resize(self.sizeHint())
        self.initialize()
        self.show()

    def initialize(self):
        self.textClickSignal.connect(textEditSelectionChanged)
        self.selectedRoleContent = None

  

 