#-*- coding:utf-8 -*-
import sys
import os
import re
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow , QApplication , QPushButton , QTabWidget 
from PyQt5.QtWidgets import *
from verbWidget import VerbWidget
from conjunctionWidget import ConjunctionWidget 
from singleInstance import *
import traceback
from utilities import *
from basicTabWidget import *
from comListWidget import *
from nounWidget import NounWidget
from xmlParse import extractXMLData
# import pandas as pd

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

        self.initializeVariables()

        rows = 3
        cols = 20
        self.rows = rows
        self.columns = cols
        self.MainWindowWidth = 1000
        lenghtOfWord = 10
        defaultLength = 100
        self.sentencewidget = QWidget()
        hbox = QVBoxLayout()

        #显示原始句子的Widght
        self.sentenceshow = CommonTableWidget(self)
        # cols = int(widgetWidth/defaultLength) - 1        
        # self.setTableWidgetColumns(self.sentenceshow,itemWidth=defaultLength)
        self.sentenceshow.setRowCount(rows)
        self.sentenceshow.setColumnCount(cols)
        self.sentenceshow.verticalHeader().setVisible(False)
        
        self.sentenceshow.setSelectionMode(QAbstractItemView.MultiSelection)
        self.sentenceshow.setShowGrid(False)
        self.sentenceshow.doubleClicked.connect(self.doubleClickedOnTableWidget)
        
        # self.sentenceshow.columnWidth(defaultLength)
        # self.sentenceshow.setItem(0,0,QTableWidgetItem("dgaghrehrehreherherheeheherher"))

        # self.showSentence("Tim bought Eric a gecko, because he followed him.")

        self.sentenceshow.resizeRowsToContents()
        self.sentenceshow.resizeColumnsToContents()
        self.sentenceshow.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.sentenceshow.resize(self.MainWindowWidth,150)
        self.sentenceshow.setMinimumHeight(100)
        # self.sentenceshow.addItem("dgagerr")

        self.buttonAddSomeWords = QPushButton(self)
        self.buttonAddSomeWords.setText("确定")
        self.buttonAddSomeWords.clicked.connect(self.addSomeWords)
        self.buttonAddSomeWords.resize(self.buttonAddSomeWords.sizeHint())
        hbox.addWidget(self.sentenceshow)
        hbox.addWidget(self.buttonAddSomeWords)
        self.sentencewidget.setLayout(hbox)
        self.sentencewidget.resize(self.MainWindowWidth,300)

        #显示已生成的短语的Widget
        self.typeGroupssplitter = QSplitter(Qt.Horizontal)
        self.verbListwidget = ComListWidget(self,"verbTab",WidgetType.VERB)                              #CommonListWidget(self,"verbTab")
        self.conjunctionwidget = ComListWidget(self,"conjunctionTab",WidgetType.CONJUNCTION)
        # self.prepositionwidget = ComListWidget(self,"prepositionTab",WidgetType.PREPOSITION)
        # self.nounwidget = ComListWidget(self,"nounTab",WidgetType.NOUN)
        # self.pronounwidget = ComListWidget(self,"pronounTab",WidgetType.PRONOUN)
        
        self.typeGroupssplitter.addWidget(self.verbListwidget)
        self.typeGroupssplitter.addWidget(self.conjunctionwidget)
        self.typeGroupssplitter.setFixedHeight(150)
        # self.typeGroupssplitter.addWidget(self.prepositionwidget)
        # self.typeGroupssplitter.addWidget(self.nounwidget)
        # self.typeGroupssplitter.addWidget(self.pronounwidget)
        
        #用来连接列表框和tab框
        self.listWidgetDictByWidgetType = {
            WidgetType.VERB:"verbListwidget",
            WidgetType.CONJUNCTION:"conjunctionwidget",
            WidgetType.NOUN:"nounwidget"
            }
        # self.typeGroups.addItem("garh")

        #用于设置动词、连词、介词、名词等相应内容的Widget
        self.contentTabs = QTabWidget(self)
        
        self.verbTab = VerbTabWidget(self)
        self.conjunctionTab = ConjunctionTabWidget(self)
        # self.prepositionTab = QWidget()
        # self.nounTab = BasicTabWidget(self,WidgetType.NOUN)
        # self.pronounTab = QWidget()
        # self.contentTabs.addTab(self.prepositionTab,"介词")        
        self.contentTabs.addTab(self.verbTab,"动词")
        self.contentTabs.addTab(self.conjunctionTab,"连词")
        # self.contentTabs.addTab(self.nounTab,"名词")        
        # self.contentTabs.addTab(self.pronounTab,"代词")
        

        self.tabWidgetDictByWidgetType = {
            WidgetType.VERB:"verbTab",
            WidgetType.CONJUNCTION:"conjunctionTab",
            WidgetType.NOUN:"nounTab"
            }

        self.contentTabs.resize(self.MainWindowWidth,400)

        self.preButton = getButton("上一句",width=140,event=self.preButtonClickedEvent)
        self.sureButton = getButton("保存",width=140,event=self.sureButtonClickedEvent)
        self.tempSureButton = getButton("跳过",width=140,event=self.tempSureButtonClickedEvent)
        self.nextButton = getButton("下一句",width=140,event=self.nextButtonClickedEvent)
        

        self.verticalSplitter = QSplitter(Qt.Vertical)
        self.verticalSplitter.addWidget(self.sentencewidget)
        self.verticalSplitter.addWidget(self.typeGroupssplitter)
        self.verticalSplitter.addWidget(self.contentTabs)
        self.verticalSplitter.addWidget(addWidgetInHBoxLayout([self.preButton,self.tempSureButton,self.sureButton,self.nextButton],True))

      

        # self.verticalSplitter.addWidget()

        # self.verticalSplitter.setStretchFactor(0,3)
        # self.verticalSplitter.setStretchFactor(1,6)
        # self.verticalSplitter.setStretchFactor(2,5)
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
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        self.show()
        self.run()

    def initializeVariables(self):
        self.currentSentence = None

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def run(self):
        
        self.sentenceStores = []
        self.storeIndex = 0               #当前值代表待存储的位置，取前一句话要减一，如果变成负的，则表示要从已经标注的文件中取，此次的内存中已经到最前面了
        self.currentSavedFile = None      #当前处理的句子保存到外存中的文件名

        self.currnetHandledFile = None

        self.sentenceGenerator = self.readFile()    

        try:    
            self.sentence = self.sentenceGenerator.__next__()
        except StopIteration :
            QMessageBox.information(self,"提示","没有可以标注的数据了，辛苦您了!",QMessageBox.Ok,QMessageBox.Ok)

        self.nextButtonClickedEvent()
         

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

    def resizeEvent(self,event):
        self.sentenceshow.resize(self.sentencewidget.width(),self.sentencewidget.height()*0.8) 

    def showSentence(self,sentence=None):
        # row = 0
        # col = 0
        # for word in sentence.split(" "):
            # self.sentenceshow.setItem(row,col,QTableWidgetItem(word+" "))
            # col += 1
            # if col >= self.sentenceshow.columnCount() :
            #     row += 1
            #     col = 0
            # if row >= self.sentenceshow.rowCount() :
            #     self.sentenceshow.insertRow(row)
        if sentence is not None :
            showContentInTableWidget(self.sentenceshow,sentence.split(" "))

                
    def getSelectedWords(self):
        s = ""
        items = self.sentenceshow.selectedItems()
        items = sorted(items,key=lambda x : ( x.row(),x.column() ))
        index = None
        if items :
            index = self.sentenceshow.row(items[0]) * self.rows + self.sentenceshow.column(items[0]) + 1
            
            s = "_".join([ item.text().strip() for item in items ])
            s = s.replace(",","").replace(".","").replace("?","")       
        return s , index

    def addSomeWords(self):
        s , index = self.getSelectedWords()
        if s == "" :
            return
        isSelected = addWordsToSelectedTextEdit(s,CONSTANT.noItemID,index)
        if isSelected :
            self.sentenceshow.clearSelection()
        # messagecontainer = MessageContainer()
        # selectedRoleContent = messagecontainer.getMessage("selectedRoleContent")
        # if selectedRoleContent is not None :
        #     selectedRoleContent.setText(s)

    def doubleClickedOnTableWidget(self):
        self.addSomeWords()
        
    def sureButtonClickedEvent(self):
        listWindow = self.conjunctionwidget.listWindow
        count = listWindow.count()
        results = {}
        formalSentences = []
        if count == 1 :
            directFlag = True
        else:
            directFlag = False
        for index in range(count) :
            item = listWindow.item(index)
            if not (item.checkState() or directFlag) :
                continue
            lexicon = searchLexiconByID(item.itemID)

            print("string ",lexicon.getFormatString())
            # continue
            if lexicon is None :
                print("not found")
                continue
            lexicon.getFormat(results,[])
            formalSentences.append(lexicon.getFormatString())
            
        # print("results ",results)
        if results :
            results['formalSentences'] = formalSentences
            results['rawSentence'] = self.currentSentence

            sentenceMD5 = hashlib.md5(self.currentSentence.encode("utf-8")).hexdigest()
            sentenceSHA1 = hashlib.sha1(self.currentSentence.encode("utf-8")).hexdigest()
            filename = "result/{}.xml".format(sentenceMD5 + sentenceSHA1)
            # flag = True
            # if filename not in self.multifiles['hashFile'].tolist() :
            #     print("not exists")
            #     pass
            # else:
            #     if self.currentSentence in self.multifiles['sentence'].tolist() :
            #         filename = self.multifiles.loc[self.multifiles['sentence']==self.currentSentence]['hashFile'].tolist()[0]
            #         print("exists")
            #         flag = False
            #     else:
            #         filename += str(int(time.time()))
            # if flag :
            #     self.multifiles = self.multifiles.append(pd.Series({"sentence":self.currentSentence,"hashFile":filename}),ignore_index=True)
            #     self.multifiles.to_csv("res/sentenceFileMap.csv")
            self.checkDefault(filename)
            # print("results   ",results)
            results['filename'] = filename
            self.currentSavedFile = filename
            writeFile(results)
            open("usedDatas/{}".format(self.currnetHandledFile),'a+').write(self.currentSentence+"\n")            
        else:
            QMessageBox.warning(self,"警告","您还没有选择将要保存的连词语义表示",QMessageBox.Ok,QMessageBox.Ok)

    def checkUsingPandas(self,filename):
        flag = True
        if filename not in self.multifiles['hashFile'].tolist() :
            print("not exists")
            pass
        else:
            if self.currentSentence in self.multifiles['sentence'].tolist() :
                filename = self.multifiles.loc[self.multifiles['sentence']==self.currentSentence]['hashFile'].tolist()[0]
                print("exists")
                flag = False
            else:
                filename += str(int(time.time()))
        if flag :
            self.multifiles = self.multifiles.append(pd.Series({"sentence":self.currentSentence,"hashFile":filename}),ignore_index=True)
            self.multifiles.to_csv("res/sentenceFileMap.csv")

    def checkDefault(self,filename):
        flag = True
        if filename not in self.multifiles['hashFile'] :
            print("not exists")
            pass
        else:
            if self.currentSentence in self.multifiles['sentence'] :
                index = self.multifiles['sentence'].index(self.currentSentence)
                filename = self.multifiles['hashFile'][index]
                print("exists")
                flag = False
            else:
                filename += str(int(time.time()))
        if flag :
            self.multifiles['sentence'] = self.currentSentence
            self.multifiles['hashFile'] = filename
            open(self.sentenceFilePair,'a+').write(self.currentSentence+"\t"+filename+"\n")

    def tempSureButtonClickedEvent(self):
        if self.currentSentence not in self.sentencesNotSure :
            self.sentencesNotSure.append(self.currentSentence)
            open(self.notsureFile,'a+').write(self.currentSentence+"\n")
            #需要检查暂存中的是否已经标注过了
        self.currentSavedFile = None
        self.nextButtonClickedEvent()

    def preButtonClickedEvent(self):
        
        def verbWidgetInitialize(widgetIndex,verb,signalEmit=True,Datas=None):
            widget = self.verbTab.tabWindow.widget(widgetIndex)
            widget.verbContent.setText(verb[0])
            roles = []
            contents = []
            for role in verb[1] :
                roles.append(role[0])   
                contents.append(role[1])        
            print(contents)
            if Datas is not None :
                ref = Datas['variables'] if "variables" in Datas else None
                widget.updateRoleLabel(roles,contents=contents,ref=ref)
            else:
                widget.updateRoleLabel(roles,contents=contents)
            attrib = verb[2]
            if "belong" in attrib :
                widget.belong = attrib['belong']
            if "isleft" in attrib :
                widget.isleft = attrib['isleft']
            if len(verb) >= 4 :
                widget.originVerb = verb[3]
            if signalEmit :
                widget.buttonSaver.clicked.emit()

        # def AddVerbWidget(verbs):
        #     verbIndex = 0
        #     for widgetIndex in range(self.verbTab.tabWindow.count()-1) :
        #         print(widgetIndex)
        #         verbWidgetInitialize(widgetIndex,verbs[verbIndex])
        #         verbIndex += 1

        #     if verbIndex < len(verbs) :
        #         N = len(verbs)-verbIndex
        #         for _ in range(N) :
        #             self.verbTab.addTab()
        #             widgetIndex = self.verbTab.tabWindow.count()-2
        #             verbWidgetInitialize(widgetIndex,verbs[verbIndex])
        #             verbIndex += 1

        def conjunctionWidgetInitialize(widgetIndex,conjunction,signalEmit=True) :
            widget = self.conjunctionTab.tabWindow.widget(widgetIndex)
            widget.initializeContents(conjunction,self.verbListwidget)
            print("set conjunction")

        def AddWidgets(datas,attrib,Datas=None):
            obj = getattr(self,attrib)
            index = 0
            for widgetIndex in range(obj.tabWindow.count()-1) :
                print(widgetIndex)
                if attrib == "verbTab" :
                    verbWidgetInitialize(widgetIndex,datas[index],Datas=Datas)
                elif attrib == "conjunctionTab" :
                    conjunctionWidgetInitialize(widgetIndex,datas[index])
                index += 1

            if index < len(datas) :
                N = len(datas)-index
                for _ in range(N) :
                    if attrib == "verbTab" :
                        self.verbTab.addTab()
                        widgetIndex = obj.tabWindow.count()-2
                        verbWidgetInitialize(widgetIndex,datas[index],Datas=Datas)
                    elif attrib == "conjunctionTab" :
                        widgetIndex = obj.tabWindow.count()-2                        
                        conjunctionWidgetInitialize(widgetIndex,datas[index])
                        
                    index += 1


        self.storeIndex = 1
        self.storeIndex -= 1
        if self.storeIndex < 0 :
            QMessageBox.warning(self,"警告","没有句子了")
            self.storeIndex = 0
        else:
            # if self.storeIndex >= len(self.sentenceStores) :
            #     print("wrong in get data from sentenceStores for out of the length")
            #     return
            # sentence = self.sentenceStores[self.storeIndex]
            sentence = ["agaerwgew","result/32c7dd219ea12a810e94aa221cb1e583c458e366a2e692ca92829f095c07459420e33d19.xml"]
            if sentence[1] is not None :
                results = extractXMLData(sentence[1])
                if results is None :
                    self.resetWidget()
                    self.showSentence(sentence[0])

                    return
                print(results)
                self.resetWidget()
                print("count ",self.verbTab.tabWindow.count())
                # AddVerbWidget(results['verbs'])
                # AddConjunctionWidget(results['conjunctions'])
                AddWidgets(results['verbs'],"verbTab",results)
                AddWidgets(results['conjunctions'],"conjunctionTab")
                


                

                
                            


    def nextButtonClickedEvent(self):
        try:
            if self.storeIndex >= len(self.sentenceStores) :
                if self.currentSentence is not None :
                    self.sentenceStores.append((self.currentSentence,self.currentSavedFile))
                    self.currentSavedFile = None
                    self.storeIndex += 1
                sentence = self.sentence.__next__()            
                self.currentSentence = self.wordsFilter(sentence)
                self.showSentence(self.currentSentence)
                self.resetWidget()
            else:
                self.storeIndex += 1
                print("current store index ",self.storeIndex)
          
     
        except StopIteration :
            self.run()

    def readFile(self):
        
        def read(filename,exists=False):
            if exists :
                try:
                    with open("usedDatas/{}".format(filename)) as f :
                        sentences = f.read().strip().split("\n")
                    print("exists sentences ",sentences)
                except Exception :
                    pass
            else:
                sentences = []
            with open("datas/{}".format(filename),'r',encoding='utf-8') as f :
                for line in f :
                    line = line.strip()
                    line = self.wordsFilter(line)
                    if line in sentences or line in self.sentencesNotSure :
                        continue
                    yield line

        if not os.path.exists("datas/") :
            return
        if not os.path.exists("usedDatas") :
            os.mkdir("usedDatas")
        dataDir = os.listdir("datas")
        usedDataDir = os.listdir("usedDatas")
        for filename in dataDir :
            self.currnetHandledFile = filename
            self.resetResFile()
            if filename not in usedDataDir :
                yield read(filename)
            else:
                yield read(filename,True)

        # print(dataDir,usedDataDir)
    
    def wordsFilter(self,sentence):
        sentence = re.sub(r'\d+\.\s+',"",sentence)
        return sentence

    def resetResFile(self):

        def readSentenceFileMap(filename):
            try:
                with open(filename,'r') as f :
                    contents = {'sentence':[],"hashFile":[]}
                    for line in f :
                        arr = line.strip().split("\t")
                        contents['sentence'].append(arr[0])
                        contents['hashFile'].append(arr[1])
                    
                    return contents
            except Exception :
                QMessageBox.warning(self,"警告","读取配置文件出错")
                traceback.print_exc()

        def read(filename):
            try:
                with open(filename,'r') as f :
                    contents = []
                    for line in f :
                        contents.append(line.strip())
                    return contents
            except Exception :
                QMessageBox.warning(self,"警告","读取配置文件出错")
                traceback.print_exc()
                    
        filename = re.sub(r'\.txt',"",self.currnetHandledFile)

        # filename = "res/sentenceFileMap.csv"
        # filename = "res/sentenceFileMap.txt"
        self.sentenceFilePair = "res/{}_sentence_file_pair.txt".format(filename)
        if not os.path.exists(self.sentenceFilePair) :
            # self.multifiles = pd.DataFrame({"sentence":[],"hashFile":[]})
            self.multifiles = {"sentence":[],"hashFile":[]}
        else:
            # self.multifiles = pd.read_csv(filename,index_col=0)
            self.multifiles = readSentenceFileMap(self.sentenceFilePair)
        # print(self.multifiles)
            # print(self.multifiles.loc[self.multifiles['hashFile']=="result/a.xml"]['sentence'].tolist())

                    
        self.notsureFile = "res/{}_notsure.txt".format(filename)
        if not os.path.exists(self.notsureFile) :
            self.sentencesNotSure = []
        else:
            self.sentencesNotSure = read(self.notsureFile)  
        # print(self.sentencesNotSure)




    def resetWidget(self):
        self.verbListwidget.resetWidget()
        self.conjunctionwidget.resetWidget()
        self.verbTab.resetWidget()        
        self.conjunctionTab.resetWidget()
        self.conjunctionTab.addTab()
        self.verbTab.addTab()
        self.contentTabs.setCurrentIndex(0)
        # self.verbTab.getFocus()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MyApp()
    try:
        sys.exit(app.exec_())
    except Exception :
        traceback.print_exc()