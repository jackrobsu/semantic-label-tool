#-*- coding:utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTabWidget
from PyQt5.QtWidgets import *
from utilities import *
from TreeWidget import Tree
import codecs

class ConjunctionWidget(QMainWindow,QObject):
    textClickSignal = pyqtSignal(QWidget,int,CommonTextEdit)         #鼠标点击响应信号
    saverButtonSignal = pyqtSignal(QWidget,QWidget,QWidget)

    def __init__(self,pWidget) :
        super().__init__()
        self.pWidget = pWidget
        self.initializeVariables()
        self.splitWindow()                      
        controlContents = self.ContentAdd()  
        self.gridAddForLeftWindow(controlContents)

        self.addWidgetInRightWindow()
      

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
        self.conjunctionLabel , self.conjunctionContent = addContent(self,"连词",controlcontents=controlContents,num=0,signal=self.textClickSignal,tagWidth=50)
        # self.conjunctionRoleLabel , self.conjunctionRoleContent = addContent(self,"语义角色",controlcontents=controlContents,num=1,signal=self.textClickSignal,tagWidth=50)
       
        self.leftSentenceLabel , self.leftSentenceContent , self.leftRefTag= addContent(self,"子句1",controlcontents=controlContents,num=1,signal=self.textClickSignal,tagWidth=50,checkBoxHidden=False,needTagTextEdit=True)
        # self.addPadding(controlContents,3)
        # self.leftSentenceRoleLabel , self.leftSentenceRoleContent = addContent(self,"语义角色",controlcontents=controlContents,num=2,signal=self.textClickSignal,tagWidth=50)
        self.rightSentenceLabel , self.rightSentenceContent , self.rightRefTag = addContent(self,"子句2",controlcontents=controlContents,num=2,signal=self.textClickSignal,tagWidth=50,checkBoxHidden=False,needTagTextEdit=True)
        # self.addPadding(controlContents,3)
        # self.rightSentenceRoleLabel , self.rightSentenceRoleContent = addContent(self,"语义角色",controlcontents=controlContents,num=4,signal=self.textClickSignal,tagWidth=50)
        self.allLabels = ['conjunctionLabel', 'leftSentenceLabel', 'rightSentenceLabel']
        self.allContents = ['conjunctionContent','leftSentenceContent','rightSentenceContent']
        return controlContents

    def gridAddForLeftWindow(self,controlContents):
        '''
            把标签和文本输入框按网格方式布局
        '''
        self.gridbox = QGridLayout()
        self.gridbox.setHorizontalSpacing(15)
        numOfEachRow = 4
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
        self.conjunctionRole = None
        # textEditSelectionChanged(self,0,self.conjunctionContent)
  

    def initializeVariables(self):
        self.trees = []
        self.conjunctionTypes = []
        self.conjunctionDict = {}   

    def getContent(self):
        return self.conjunctionContent.toPlainText()

    def getSubSentences(self):
        id1 = self.leftSentenceContent.lexiconID
        id2 = self.rightSentenceContent.lexiconID
        sen1 = self.leftSentenceContent.toPlainText()
        sen2 = self.rightSentenceContent.toPlainText()
        return id1 , id2 , sen1 , sen2

    def addPadding(self,controlContents,num) :
        for _ in range(num) :
            controlContents.append(None)


    def addWidgetInRightWindow(self):
        self.tree = Tree(self.rightWindow,self,mutexAnyItem=True,callback=self.callback)
        self.tree.setMinimumWidth(self.rightWindow.width())
        self.tree.setMinimumHeight(self.rightWindow.height())
        self.tree.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)  

        self.trees.append(self.tree)
        self.parseConjunctionFile()
        self.tree.addTreeRoots(self.conjunctionTypes,self.conjunctionDict)

    def resizeEvent(self,event):
        self.tree.setMinimumWidth(self.rightWindow.width())
        self.tree.setMinimumHeight(self.rightWindow.height())


    def parseConjunctionFile(self):
        filename = "res/conjunction.txt"
        try:
            with open(filename,'r',encoding="utf-8") as f :
                curConjunction = None
                for line in f :
                    if "@" in line and line.index("@") == 0 :
                        curConjunction = line[1:].strip()
                        self.conjunctionTypes.append(curConjunction)
                        self.conjunctionDict[curConjunction] = []
                    else:
                        if curConjunction is None :
                            continue
                        arr = line.strip().split("#")
                        if len(arr) == 2 :
                            self.conjunctionDict[curConjunction].append(tuple(arr))
        except Exception :
            print("加载连词资源文件出错,可能不存在该文件")
            QMessageBox.warning(self,"错误","加载连词资源文件出错，可能不存在该文件",QMessageBox.Ok,QMessageBox.Ok)
            sys.exit(0)

            # print(self.conjunctionTypes)
            # print(self.conjunctionDict)
            # exit(0)

    def callback(self,selectedItem):
        if selectedItem is None :
            return
        self.conjunctionRole = {"role_ch-zh":selectedItem.text(0),"role":selectedItem.text(1)}
        # print(selectedItem.text(0),selectedItem.text(1))

    def showEvent(self,event):
        textEditSelectionChanged(self,0,self.conjunctionContent)