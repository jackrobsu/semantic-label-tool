#-*- coding:utf-8 -*-
import sys
from utilities import *

class BasicWidget(QMainWindow,QObject):
    textClickSignal = pyqtSignal(QWidget,int,CommonTextEdit)         #鼠标点击响应信号
    saverButtonSignal = pyqtSignal(QWidget,QWidget,QWidget)
    def __init__(self,pWidget,widgetType):
        super(BasicWidget,self).__init__()
        self.pWidget = pWidget
        self.widgetType = widgetType
    def splitWindow(self,leftwidth=1,rightwidth=1):
        '''
            切分窗口，目前是分成左右两部分
        '''
        self.splitter = QSplitter(Qt.Horizontal)
        self.leftWindow = QWidget()
        self.rightWindow = QWidget()
        self.splitter.addWidget(self.leftWindow)
        self.splitter.addWidget(self.rightWindow)
        self.splitter.setStretchFactor(0,leftwidth)
        self.splitter.setStretchFactor(1,rightwidth)

    def gridAddForLeftWindow(self,controlContents,numOfEachRow=2):
        gridbox = QGridLayout()
        gridbox.setHorizontalSpacing(0)
        for (i, tag) in enumerate(controlContents):
            row = int(i / numOfEachRow)
            col = i - row * numOfEachRow
            if tag is None :
                continue
            gridbox.addWidget(tag, row, col)

        return gridbox

    def addSaverButtonInLayout(self,layout):
        self.buttonSaver = SaverButton(self,self.saverButtonSignal,self.pWidget,self.widgetType)
        self.buttonSaver.setText("保存")
        layout.addWidget(self.buttonSaver)

    def initialize(self):
        self.textClickSignal.connect(textEditSelectionChanged)
        self.saverButtonSignal.connect(saveLexicon)
        self.widgetID = UnionID()
