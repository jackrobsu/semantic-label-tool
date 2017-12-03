#-*- coding:utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow , QApplication , QPushButton , QTabWidget 
from PyQt5.QtWidgets import *
from verbWidget import VerbWidget
from conjunctionWidget import ConjunctionWidget


'''
    加载ui文件
'''
qtCreatorFile = "gui/untitled.ui"
# Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        # Ui_MainWindow.__init__(self)
        # self.setupUi(self)
        rows = 3
        cols = 30
        self.MainWindowWidth = 1000
        lenghtOfWord = 10
        defaultLength = 100
        sentencewidget = QWidget()
        hbox = QVBoxLayout()

        #显示原始句子的Widght
        self.sentenceshow = QTableWidget()
        # cols = int(widgetWidth/defaultLength) - 1        
        # self.setTableWidgetColumns(self.sentenceshow,itemWidth=defaultLength)
        self.sentenceshow.setRowCount(rows)
        self.sentenceshow.setColumnCount(cols)
        self.sentenceshow.setSelectionMode(QAbstractItemView.MultiSelection)
        self.sentenceshow.setShowGrid(False)
        # self.sentenceshow.columnWidth(defaultLength)
        # self.sentenceshow.setItem(0,0,QTableWidgetItem("dgaghrehrehreherherheeheherher"))

        self.showSentence("You can go to play with them.")

        self.sentenceshow.resizeRowsToContents()
        self.sentenceshow.resizeColumnsToContents()
        self.sentenceshow.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sentenceshow.resize(self.MainWindowWidth,100)
        # self.sentenceshow.addItem("dgagerr")

        self.buttonAddSomeWords = QPushButton()
        self.buttonAddSomeWords.setText("确定")
        self.buttonAddSomeWords.clicked.connect(self.addSomeWords)
        self.buttonAddSomeWords.resize(self.buttonAddSomeWords.sizeHint())
        hbox.addWidget(self.sentenceshow)
        hbox.addWidget(self.buttonAddSomeWords)
        sentencewidget.setLayout(hbox)
        sentencewidget.resize(self.MainWindowWidth,300)

        #显示已生成的短语的Widget
        self.typeGroupssplitter = QSplitter(Qt.Horizontal)
        self.verbwidget = QScrollArea()
        self.conjunctionwidget = QScrollArea()
        self.prepositionwidget = QScrollArea()
        self.nounwidget = QScrollArea()
        self.typeGroupssplitter.addWidget(self.verbwidget)
        self.typeGroupssplitter.addWidget(self.conjunctionwidget)
        self.typeGroupssplitter.addWidget(self.prepositionwidget)
        self.typeGroupssplitter.addWidget(self.nounwidget)
        
        # self.typeGroups.addItem("garh")

        #用于设置动词、连词、介词、名词等相应内容的Widget
        self.contentTabs = QTabWidget()
        
        self.verbTab = VerbWidget()
        self.conjunctionTab = ConjunctionWidget()
        self.prepositionTab = QWidget()
        self.nounTab = QWidget()
        self.contentTabs.addTab(self.verbTab,"Verb")
        self.contentTabs.addTab(self.conjunctionTab,"conjunction")
        self.contentTabs.addTab(self.prepositionTab,"preposition")
        self.contentTabs.addTab(self.nounTab,"noun")
        
        self.contentTabs.resize(self.MainWindowWidth,400)

        self.verticalSplitter = QSplitter(Qt.Vertical)
        self.verticalSplitter.addWidget(sentencewidget)
        self.verticalSplitter.addWidget(self.typeGroupssplitter)
        self.verticalSplitter.addWidget(self.contentTabs)

        self.verticalSplitter.setStretchFactor(0,3)
        self.verticalSplitter.setStretchFactor(1,3)
        self.verticalSplitter.setStretchFactor(2,5)
        self.setCentralWidget(self.verticalSplitter)
        


        # self.horizon = QVBoxLayout()

        # self.qbt = QPushButton(self)
        # self.qbt.setText("button")
        # self.qbt.setFixedSize(QSize(50,50))

        # self.qbt1 = QPushButton(self)
        # self.qbt1.setText("button1")
        # self.qbt1.setFixedSize(QSize(50,50))


        # self.qtab = QTabWidget(self)
        # self.qtab.resize(100,100)
        # self.qtab.addTab(self.qbt,"a")
        # self.qtab.addTab(self.qbt1,"b")
        
        # self.qbt2 = QPushButton(self)
        # self.qbt2.setText("button2")
        # self.qbt2.setFixedSize(QSize(50,50))

        # self.horizon.addWidget(self.qtab)
        # self.horizon.addWidget(self.qbt2)
        
        # self.setLayout(self.horizon)

        # self.setGeometry(300,300,300,150)
        self.resize(self.MainWindowWidth,700)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setTableWidgetColumns(self,table,itemWidth=100,eachWidth=None):
        
        def setColumns(items):
            
            for col in items :
                pass

        minWidth = 10
        if eachWidth is None :
            cols = int(self.MainWindowWidth/itemWidth)
            items = [itemWidth] * cols
            diff = self.MainWindowWidth - itemWidth * cols
            if diff >= minWidth :
                items.append(diff)

        setColumns(items)
            
    def showSentence(self,sentence):
        row = 0
        col = 0
        for word in sentence.split(" "):
            self.sentenceshow.setItem(row,col,QTableWidgetItem(word+" "))
            col += 1
            if col >= self.sentenceshow.columnCount() :
                row += 1
                col = 0
            if row >= self.sentenceshow.rowCount() :
                self.sentenceshow.insertRow(row)
        
    def addSomeWords(self):
        items = self.sentenceshow.selectedItems()
        items = sorted(items,key=lambda x : ( x.row(),x.column() ))
        s = "_".join([ item.text().strip() for item in items ])
        if self.verbTab.selectedRoleContent is not None :
            self.verbTab.selectedRoleContent.setText(s)
        


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyApp()

    sys.exit(app.exec_())