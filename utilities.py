#-*- coding:utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTabWidget
from PyQt5.QtWidgets import *
import uuid
import time
from enum import Enum
from singleInstance import *
import traceback
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
import hashlib
import re

class WidgetType(Enum):
    VERB = 0
    CONJUNCTION = 1
    PREPOSITION = 2
    NOUN = 3
    VARIABLE = 4
    PRONOUN = 5

class CONSTANT(Enum):
    noItemID = 0

class CommonTextEdit(QTextEdit):
    __qualname__ = 'CommonTextEdit'

    def __init__(self, obj, signal, num=(0, )):
        super().__init__()
        self.signal = signal
        self.num = num
        self.dependencyObj = obj

        #与文本框对应的词条ID
        self.lexiconID = None
        #单词在原句中的位置
        self.indexOfPlace = None

    def mousePressEvent(self, event):
        self.signal.emit(self.dependencyObj,self.num,self)

    def setLexiconID(self,ID):
        self.lexiconID = ID

    def setIndexOfPlace(self,index):
        self.indexOfPlace = index

class CommonTableWidget(QTableWidget):
    def __init__(self,pApp):
        super().__init__(pApp)
        self.pApp = pApp

    def contextMenuEvent(self,event):
        menu = QMenu(self)
        add = QAction()
        add.setText("选中")
        add.triggered.connect(self.pApp.addSomeWords)
        copyAction = QAction()
        copyAction.setText("复制")
        copyAction.triggered.connect(self.CopyAction)
        clear = QAction()
        clear.setText("清除选中项")
        clear.triggered.connect(self.Clear)

        menu.addAction(add)
        menu.addAction(copyAction)        
        menu.addAction(clear)
        menu.exec_(QtGui.QCursor.pos())

    def CopyAction(self):
        


        clipboard = QApplication.clipboard()
        words = self.pApp.getSelectedWords()
        if isinstance(words,list) or isinstance(words,tuple) :
            words = " ".join(words[0].split("_"))
        else:
            words = " ".join(words.split("_"))            

        clipboard.setText(words)            

    def Clear(self):
        self.clearSelection()

class OriginVerbTableWidget(QTableWidget):
    def __init__(self,pApp):
        super().__init__(pApp)
        self.pApp = pApp

    def contextMenuEvent(self,event):
        menu = QMenu(self)
        add = QAction()
        add.setText("查找")
        add.triggered.connect(self.pApp.SearchButtonClickEvent)
        copyAction = QAction()
        copyAction.setText("复制")
        copyAction.triggered.connect(self.CopyAction)
        clear = QAction()
        clear.setText("清除选中项")
        clear.triggered.connect(self.Clear)
        
        menu.addAction(add)
        menu.addAction(copyAction)        
        menu.addAction(clear)
        menu.exec_(QtGui.QCursor.pos())


    def CopyAction(self):
        clipboard = QApplication.clipboard()
        items = self.selectedItems()
        if not items :
            return
        try:
            clipboard.setText(items[0].text())
        except Exception:
            pass

    def Clear(self):
        self.clearSelection()


class SignalWithHandleButton(QPushButton):
    def __init__(self,signal,connectedWidget):
        super().__init__()
        self.signal = signal
        self.connectedWidget = connectedWidget

    def mousePressEvent(self,event):
        self.signal.emit(self.connectedWidget)

class SaverButton(QPushButton):
    '''
        obj: 父对话框对象,即该Button所属的上层框
        signal: 待发送的信号
        pWidget：最外层的框
        widgetType：信号连接的框的类型
    '''
    def __init__(self,obj,signal,pWidget,widgetType):
        super().__init__()
        self.dependencyObj = obj
        self.signal = signal
        self.pWidget = pWidget
        self.widgetType = widgetType
        

    def mousePressEvent(self,event):
        connectedWidget = self.pWidget.listWidgetDictByWidgetType.get(self.widgetType) 
        tabwidget = self.pWidget.tabWidgetDictByWidgetType.get(self.widgetType)
        
        if connectedWidget is None or tabwidget is None :
            return
        connectedWidget = getattr(self.pWidget,connectedWidget)
        tabwidget = getattr(self.pWidget,tabwidget)
        if connectedWidget is None or tabwidget is None :
            return        
        connectedWidget = connectedWidget.listWindow
        self.signal.emit(self.dependencyObj,connectedWidget,tabwidget.tabWindow)


class CommonListWidgetItem(QListWidgetItem) :
    '''
        用来显示已经保存的短语或词等
        itemID:是与词条对应的ID，用来查找相应的词条以获取更多信息
    '''
    def __init__(self,itemID,needCheckState=False,belong=None,isleft=None,indexOfPlace=None):
        super().__init__()
        self.itemID = itemID
        if needCheckState :
            self.setCheckState(Qt.Unchecked)

        
        self.belong = belong
        self.isleft = isleft
        self.indexOfPlace = indexOfPlace

    def setLexiconID(self,ID):
        self.itemID = ID

    def setItemID(self,ID):
        self.itemID = ID

    def setBelong(self,belong):
        self.belong = belong
        print("belong ",belong)
            
    def setIsLeft(self,isleft):
        self.isleft = isleft

    def setIndexOfPlace(self,indexOfPlace) :
        self.indexOfPlace = indexOfPlace

class CommonListWidget(QListWidget):
    '''
        pWidget : 该Widget所属的Widget
    '''
    def __init__(self,pWidget,widget,belong=None,isleft=None):
        '''
            widget:对应的TabWidget在pWidget中的属性名，如verbListwidget对应verbTab
        '''
        super().__init__()
        self.pWidget = pWidget
        self.widget = widget

        self.belong = belong
        self.isleft = isleft

    def mouseDoubleClickEvent(self,event):
        # self.signal.emit()
        items = self.selectedItems()
        if items :
            item = items[0]
            tabwidget = getattr(self.pWidget,self.widget)   #根据属性名获得tabwidget
            if tabwidget is None :
                return
            try:
                tabwidget = tabwidget.tabWindow           #获得tabwidget中的tab控件，前提是要有tabWindow对象
                tabshow = None
                for tabindex in range(tabwidget.count()):
                    tab = tabwidget.widget(tabindex)
                    #判断widgetID 与 item的ID是否一致
                    if tab.widgetID == item.itemID :
                        tabshow = tab
                        break
                if tabshow is None :
                    return
                tabwidget.setCurrentWidget(tabshow)
            except Exception :
                traceback.print_exc()

    def contextMenuEvent(self,event):
        menu = QMenu(self)
        action = QAction()
        action.setText("选中")
        action.triggered.connect(self.actionClicked)
        menu.addAction(action)
        menu.exec_(QtGui.QCursor.pos())

    def actionClicked(self,event):
        TextAddThroughWidget(self)


class ConstantWidget(QListWidget):
    '''
        pWidget : 该Widget所属的Widget
    '''
    def __init__(self,pWidget):
        '''
            widget:对应的TabWidget在pWidget中的属性名，如verbListwidget对应verbTab
        '''
        super().__init__()
        self.pWidget = pWidget
        
        constants = ["None (Any)","Ignored"]
        
        for constant in constants :
            item = CommonListWidgetItem(itemID=CONSTANT.noItemID)
            item.setText(constant)
            self.addItem(item)

    def mouseDoubleClickEvent(self,event):
        # self.signal.emit()
        items = self.selectedItems()
        if items :
            item = items[0]
            TextAddThroughWidget(self)

    def contextMenuEvent(self,event):
        menu = QMenu(self)
        action = QAction()
        action.setText("选中")
        action.triggered.connect(self.actionClicked)
        menu.addAction(action)
        menu.exec_(QtGui.QCursor.pos())

    def actionClicked(self,event):
        TextAddThroughWidget(self)
   

class CheckBox(QCheckBox):
    def __init__(self,pWidget,textedit,tagTextEdit=None,num=-1):
        '''
            tagTextEdit: 对应的用来填指代所指内容的文本框
            num: 对应roleLabel和content的编号
        '''
        super().__init__(pWidget)
        self.pWidget = pWidget
        self.textedit = textedit
        self.clicked.connect(self.ItemClickedEvent)
        self.tagTextEdit = tagTextEdit
        self.num = num
    def ItemClickedEvent(self,event):
        '''
            主要用来设置是否是代词
        '''

        def setPronoun(isPronoun):
            word = searchLexiconByID(self.textedit.lexiconID)

            if word is not None :
                word.belongID = self.pWidget.widgetID
                word.isPronoun = isPronoun
            else:
                try:
                    lexicon = Lexicon(self.pWidget.widgetID,WTYPE.CONSTANT,self.textedit.toPlainText(),indexOfPlace=self.textedit.indexOfPlace)
                    setLexicon(WTYPE.CONSTANT,lexicon)
                except Exception :
                    pass

        if self.checkState() == Qt.Checked :
            messagecontainer = MessageContainer()
            messagecontainer.setMessage("nextRoleLableNum",None)
            text = self.textedit.toPlainText()
            if text is None or text == "" :
                return
            try:
                if text.index("?") != 0 :
                    self.textedit.setText("?"+text)
                    setPronoun(True)
                    if self.tagTextEdit is not None :
                        self.tagTextEdit.setEnabled(True)
            except Exception :
                self.textedit.setText("?"+text)
                setPronoun(True)
                if self.tagTextEdit is not None :
                    self.tagTextEdit.setEnabled(True)
            textEditSelectionChanged(self.pWidget,self.num,self.tagTextEdit)
        else:
            text = self.textedit.toPlainText()
            if text is None or text == "" :
                return
            try:
                if text.index("?") == 0 :
                    self.textedit.setText(text[1:])
                    setPronoun(False)                    
                    if self.tagTextEdit is not None :
                        self.tagTextEdit.setEnabled(False)
            except Exception :
                pass
            if self.num+1 < len(self.pWidget.allContents) :
                textEditSelectionChanged(self.pWidget,self.num+1,getattr(self.pWidget,self.pWidget.allContents[self.num+1]))
            
    def addTagTextEdit(self,textedit):
        self.tagTextEdit = textedit

class CheckBoxForNegativeVerb(QCheckBox):
    def __init__(self,pWidget,connectedLabel=None):
        super().__init__(pWidget)
        self.pWidget = pWidget
        self.connectedLabel = connectedLabel
        self.clicked.connect(self.ItemClickedEvent)
     
    def ItemClickedEvent(self):
        if self.checkState() == Qt.Checked :
             self.pWidget.isNegative = True
             if self.connectedLabel is not None :
                 self.connectedLabel.setStyleSheet("color:red;")
        else:
            self.pWidget.isNegative = False
            if self.connectedLabel is not None :
                self.connectedLabel.setStyleSheet("color:black;")

class CheckBoxForIgnored(QCheckBox):
    def __init__(self,pWidget):
        super().__init__(pWidget)
        self.pWidget = pWidget
        self.clicked.connect(self.ItemClickedEvent)
     
    def ItemClickedEvent(self):
        if self.checkState() == Qt.Checked :
            self.pWidget.conjunctionContent.setText("Ignored")
        else:
            self.pWidget.conjunctionContent.setText("")
            


class CommonEventHandle :
    
    def __init__(self):
        return
    
    # def pronounCheckBoxClickEvent(self):
    #     if hasattr(self,"gridbox") :
    #         for row in range(self.gridbox.rowCount()) :
    #             for col in range(self.gridbox.columnCount()) :
    #                 item = self.gridbox.itemAtPosition(row,col)
    #                 if not hasattr(item,"checkState") :
    #                     print(" It's not a checkbox.")
    #                     continue
    #                 if item.isHidden() :
    #                     print("({},{}) hidden".format(row,col))
    #                     continue
    #                 if item.checkState() == Qt.Checked :
    #                     try:
    #                         edittext = self.gridbox.itemAtPosition(row,col-1)
    #                         if not isinstance(edittext,QTextEdit) :
    #                             print("It's not an textedit.")
    #                             continue
    #                         text = edittext.toPlainText()
    #                         if "?" not in text :
    #                             edittext.setText("?"+text)
    #                     except Exception :
    #                         print("no edittext exists")
                    

##############################################################

def addContent(obj,text,controlcontents,num=0,signal=None,tagHeight=30,tagWidth=30,contentHeight=30,contentWidth=100,needCheckBox=False,checkBoxHidden=True,needTagTextEdit=False,noCheckBox=False,noTagTextEdit=False,needIgnored=False,pWidget=None):
    '''
        用于给页面添加基本的标签和文本编辑框
        noCheckBox和noTagTextEdit如果为真，表示不要添加到controlcontents中去
    '''
    # widget = QWidget()
    # hbox = QHBoxLayout()
    tag = QLabel()
    tag.setAlignment(Qt.AlignCenter)
    if signal is None :
        content = QTextEdit()
    else:
        content = CommonTextEdit(obj,signal, num)
    tag.setText(text)
    tag.setMaximumWidth(tagWidth)
    content.setMaximumHeight(contentHeight)
    content.setMaximumWidth(contentWidth)
    
    # hbox.addWidget(tag)
    # hbox.addWidget(content)
    # hbox.setStretch(1, 5)
    # hbox.setContentsMargins(1, 1, 1, 1)
    # widget.setLayout(hbox)
    if not noCheckBox :
        checkbox = CheckBox(obj,content,num=num)
        checkbox.setHidden(checkBoxHidden)
    else:
        if needIgnored :
            if pWidget is None :
                checkbox = CheckBox(obj,content,num=num)
            else:
                checkbox = CheckBoxForIgnored(pWidget)
            # checkbox.setHidden(checkBoxHidden)
            needCheckBox = True
        else:
            needCheckBox = False

    
    if signal is None :
        reftag = QTextEdit()
    else:
        reftag = CommonTextEdit(obj,signal, -1)
    reftag.setEnabled(False)
    reftag.setMaximumWidth(150)
    reftag.setMaximumHeight(40)
    if not noCheckBox :
        checkbox.addTagTextEdit(reftag)

    controlcontents.append(tag)
    controlcontents.append(content)
    if not noCheckBox :
        controlcontents.append(checkbox)
    else:
        if needIgnored :
            controlcontents.append(checkbox)

    if not noTagTextEdit :
        if needTagTextEdit :
            controlcontents.append(reftag)
        else:
            if needIgnored :
                controlcontents.append(QLabel("是否忽略"))
            else:
                controlcontents.append(None)
    
    
    if needCheckBox and needTagTextEdit :
        return tag, content , checkbox , reftag
    elif needCheckBox :
        return tag, content , checkbox
    elif needTagTextEdit :
        return tag, content , reftag                
    else:
        return tag, content         

def addWordsToSelectedTextEdit(text,itemID,indexOfPlace=None):
    '''
        用于把选中的一些词送入被选中的文本编辑框中，一般通过“确定”按钮触发
    '''
    messagecontainer = MessageContainer()
    selectedRoleContent = messagecontainer.getMessage("selectedRoleContent")
    print("selectedRoleContent ",selectedRoleContent)
    if selectedRoleContent is not None :
        selectedRoleContent.setText(text)
        selectedRoleContent.setLexiconID(itemID)
        selectedRoleContent.setIndexOfPlace(indexOfPlace)
        
        if itemID == CONSTANT.noItemID :
            ID = UnionID()
            selectedRoleContent.setLexiconID(ID)
            lexicon = Lexicon(ID,WTYPE.CONSTANT,text,indexOfPlace=indexOfPlace)
            setLexicon(WTYPE.CONSTANT,lexicon)
        
            print("selected constant itemID",ID)
        
        messagecontainer = MessageContainer()
        nextRoleLabelNum = messagecontainer.getMessage("nextRoleLableNum")
        curWidget = messagecontainer.getMessage("curWidget")
        if nextRoleLabelNum is not None and curWidget is not None :
            print("jinlaile",nextRoleLabelNum,len(curWidget.allContents))
            print(curWidget.allContents)
            if nextRoleLabelNum < len(curWidget.allContents) :
                textobj = getattr(curWidget,curWidget.allContents[nextRoleLabelNum])
                # curWidget.focusNextChild()
                textEditSelectionChanged(curWidget,nextRoleLabelNum,textobj)
        

        return True
    return False

def textEditSelectionChanged(widgetObj,num, textobj):
    '''
        用于高亮某个标签，同时把焦点放到对应的文本框中
    '''
    if not hasattr(widgetObj,"allLabels") or textobj is None :
        return
    if num == -1 :
        widgetObj.selectedRoleContent = textobj
        messagecontainer = MessageContainer()
        messagecontainer.setMessage("selectedRoleContent",textobj)
        messagecontainer.setMessage("nextRoleLableNum",None)        
        messagecontainer.setMessage("curWidget",None)
        return
    for (i, label) in enumerate(widgetObj.allLabels):
        obj = getattr(widgetObj, label)
        if obj is None :
            continue
        if i == num:
            obj.setStyleSheet('color:green;')
            widgetObj.selectedRoleContent = textobj
            messagecontainer = MessageContainer()
            # messagecontainer.setMessage("selectedRoleContent",textobj)
            # messagecontainer.setMessage("curWidget",widgetObj)
            
            print("textobj ",textobj)

            if i < len(widgetObj.allLabels) - 1 :
                messagecontainer.setMessage("nextRoleLableNum",i+1)
                messagecontainer.setMessage("curWidget",widgetObj)
                messagecontainer.setMessage("selectedRoleContent",textobj)
                
                print("set nextRoleLabelNum {} in {}".format(i+1,widgetObj))
                # messagecontainer.setMessage("nextRoleContent",widgetObj.allContents[i+1])
            else:
                messagecontainer.setMessage("nextRoleLableNum",i)
                messagecontainer.setMessage("curWidget",widgetObj)
                messagecontainer.setMessage("selectedRoleContent",textobj)
                
                print("set nextRoleLabelNum {} in {}".format(i,widgetObj))
                
            continue
        obj.setStyleSheet('color:black')

def TextAddThroughWidget(widget) :
    '''
        选择已经生成的语义形式时会调用该方法
    '''
    if widget is None :
        return
    item = widget.currentItem()
    if item is None :
        return
    text = item.text()
    text = re.sub(r'\s+\(.+?\)',"",text)
    addWordsToSelectedTextEdit(text,item.itemID)


def saveLexicon(obj,showWidget,tabwidget) :
    '''
        对应界面中的“保存”词条的按钮，词条ID与Tab ID需要一致,是通过signal触发的
        showWidget:对应要展示相应词条的那个Widget
    '''
    content , indexOfPlace = obj.getContent()
    print("index ",indexOfPlace,content)

    if obj.widgetType == WidgetType.CONJUNCTION :
        if content == "" :
            QMessageBox.warning(obj,"警告","您还没有选择连词",QMessageBox.Ok,QMessageBox.Ok)
            return
        if obj.conjunctionRole is None :
            QMessageBox.warning(obj,"警告","您还没有选择相应的连词语义",QMessageBox.Ok,QMessageBox.Ok)
            return
      
            

    lexicon = getLexicon(obj.widgetType,obj.widgetID)

    typedict = {
        WidgetType.VERB:WTYPE.VERB,
        WidgetType.CONJUNCTION:WTYPE.CONJUNCTION,
        WidgetType.NOUN:WTYPE.NOUN
    }

    if lexicon is None :
        #通过按钮触发的一般没有位置信息
        lexicon = Lexicon(obj.widgetID,typedict[obj.widgetType],content,indexOfPlace=indexOfPlace)
    else:
        lexicon.mainWord = content
        lexicon.indexOfPlace = indexOfPlace

    
    if obj.widgetType == WidgetType.CONJUNCTION :
        #填补连词的成分
        id1 , id2 , subsen1 , subsen2 = obj.getSubSentences()
        lexicon.formerSentence = subsen1
        lexicon.latterSentence = subsen2
        lexicon.formerSentenceID = id1
        lexicon.latterSentenceID = id2
        subsen = searchLexiconByID(id1)
        if subsen is not None :
            subsen.belong = "{}.{}".format(lexicon.mainWord,lexicon.indexOfPlace)
            subsen.isleft = True
        subsen = searchLexiconByID(id2)
        if subsen is not None :
            subsen.belong = "{}.{}".format(lexicon.mainWord,lexicon.indexOfPlace)
            subsen.isleft = False
        
        lexicon.conjunctionRole = obj.conjunctionRole
        print("subsen1 {} , subsen2 {}".format(subsen1,subsen2))
    elif obj.widgetType == WidgetType.VERB :
        roles = obj.getRoles()
        lexicon.roles = roles
        lexicon.originVerb = obj.originVerb
        lexicon.isNegative = obj.isNegative
        obj.checkRefTag()
        print("dgerwgr ",lexicon)
        # exit(0)

    #添加到列表框中
    if hasattr(obj,"belong") and hasattr(obj,"isleft"):
        addItemToListWidget(showWidget,lexicon,obj.belong,obj.isleft)
    else:
        addItemToListWidget(showWidget,lexicon)
        
    #更新词条
    setLexicon(obj.widgetType,lexicon)
    
    # showWidget.addItem(content)

    # verb = Verbs()
    # verb.PrintVerbs()

    tabwidget.setTabText(tabwidget.currentIndex(),content)



def UnionID():
    uid = str(uuid.uuid1())
    return str(int(time.time())) + uid

def getLexicon(widgetType,widgetID) :
    '''
        获取词条
    '''
    if widgetType == WidgetType.VERB :
        verb = Verbs()
        lexicon = verb.getItem(widgetID)
        return lexicon

    if widgetType == WidgetType.VERB :
        conjunction = Conjunctions()        
        lexicon = conjunction.getItem(widgetID)
        return lexicon
    
def setLexicon(widgetType,content):
    '''
        添加词条，根据不同的WidgetType类型往不同的词条对象中添加
    '''
    if widgetType == WidgetType.VERB :
        verb = Verbs()
        verb.setItem(content)
        verb.PrintVerbs()
    elif widgetType == WidgetType.CONJUNCTION :
        conjunction = Conjunctions()
        conjunction.setItem(content)
        conjunction.PrintConjunctions()
    elif widgetType == WTYPE.CONSTANT :
        constant = Constants()
        constant.setItem(content)


def addItemToListWidget(ListWidget,lexicon,belong=None,isleft=None):
    '''
        往列表框中添加元素，添加时会根据元素ID检查是否已经存在，如果存在，则直接替换
    '''
    def search():
        for i in range(ListWidget.count()) :
            item = ListWidget.item(i)
            if item.itemID == lexicon.wordID :
                return item
        return None
    

    item = search()
    if item is not None :
        item.setText(lexicon.getFormatString())
        item.setLexiconID(lexicon.wordID)
        print(lexicon.wordID+" grehr "+item.itemID)
    else:
        if lexicon.WType == WTYPE.CONJUNCTION :
            item = CommonListWidgetItem(lexicon.wordID,True)
        else:
            item = CommonListWidgetItem(lexicon.wordID)
            
        item.setText(lexicon.getFormatString())
        item.setBelong(belong)
        item.setIsLeft(isleft)
        ListWidget.addItem(item)

def tabAdd(tabWidget,widget=None):
    '''
        添加标签页,参数tabWidget一般是主页面，即它的tabWindow对象才是QTabWidget
    '''

    def Add(tabobj,tab,string):
        tabobj.addTab(tab,string)

    def remove(tabobj,index=-1):
        if tabobj.count() == 0 :
            return
        if index == -1 or index >= tabobj.count() :
            tabobj.removeTab(tabobj.count()-1)
        else:
            tabobj.removeTab(index)
        

    from verbWidget import VerbWidget
    from conjunctionWidget import ConjunctionWidget
    print("add")
    remove(tabWidget.tabWindow)
    showWidget = None
    if tabWidget.widgetType == WidgetType.VERB :
        if widget is not None :
            showWidget = widget
        else:
            showWidget = VerbWidget(tabWidget.pWidget,tabWidget.tabWindow.count())
        tabWidget.tabWindow.addTab(showWidget,tabWidget.defaultTab)
        Add(tabWidget.tabWindow,QWidget(),"+")
        
    elif tabWidget.widgetType == WidgetType.CONJUNCTION :
        tabWidget.tabWindow.addTab(ConjunctionWidget(tabWidget.pWidget),tabWidget.defaultTab)
        Add(tabWidget.tabWindow,QWidget(),"+")
    
    tabWidget.tabWindow.setCurrentIndex(tabWidget.tabWindow.count()-2)



def getButton(text,width=None,height=None,event=None):
    button = QPushButton()
    button.setText(text)
    if width is not None :
        button.setFixedWidth(width)
    if height is not None :
        button.setFixedHeight(height)
    
        
    if event is not None :
        button.clicked.connect(event)
    return button


def showContentInTableWidget(tableWidget,contents,row=0,col=0,isClear=True) :
    if isClear :
        tableWidget.clear()
    for word in contents :
        item = QTableWidgetItem(word)
        item.setTextAlignment(Qt.AlignCenter)
        tableWidget.setItem(row,col,item)
        col += 1
        if col >= tableWidget.columnCount() :
            row += 1
            col = 0
        if row >= tableWidget.rowCount() :
            tableWidget.insertRow(row)
    tableWidget.resizeRowsToContents()            
    tableWidget.resizeColumnsToContents()

def addWidgetInHBoxLayout(hws,widgetRequire=False) :
    hbox = QHBoxLayout()
    for hw in hws :
        hbox.addWidget(hw)
    if widgetRequire :
        widget = QWidget()
        widget.setLayout(hbox)
        return widget
    return hbox

def writeFile(results=None):
    if results is None :
        return
    print("aegawgwerg ",results)

    

    root_xml = Element('root')
    sentence_xml = SubElement(root_xml, 'sentence')
    variables_xml = SubElement(root_xml, 'variables')

    variaDic = results.get("variable")
    if variaDic is not None :
        #有重复现象
        for varia in variaDic:
            variable = variaDic[varia]
            key_xml=SubElement(variables_xml,'key')
            if "indexOfPlace" in variable and "belong" in variable :
                if variable['indexOfPlace'] is not None and variable['belong'] is not None :          
                    key_xml.attrib={'name':variable['word'],'indexOfPlace':str(variable['indexOfPlace']),'belong':variable['belong']}
                elif variable['indexOfPlace'] is not None :
                    key_xml.attrib={'name':variable['word'],'indexOfPlace':str(variable['indexOfPlace'])}
                elif variable['belong'] is not None :
                    key_xml.attrib={'name':variable['word'],'belong':variable['belong']}
                else:
                    key_xml.attrib={'name':variable['word']}
                    
            elif "indexOfPlace" in variable :
                if variable['indexOfPlace'] is not None :
                    key_xml.attrib={'name':variable['word'],'indexOfPlace':str(variable['indexOfPlace'])}
                else:
                    key_xml.attrib={'name':variable['word']}
                    
            elif "belong" in variable :
                if variable['belong'] is not None :
                    key_xml.attrib={'name':variable['word'],'belong':variable['belong']}
                else:
                    key_xml.attrib={'name':variable['word']}                    
            else:                                 
                key_xml.attrib={'name':variable['word']}
            ref_xml=SubElement(key_xml,'ref')
            ref_xml.text=variable['ref']
    # preposition_xml = SubElement(root_xml, 'preposition')
    verb_xml = SubElement(root_xml, 'verb')
    conjunction_xml = SubElement(root_xml,"conjunction")
    # getTrans()
    translate_xml = SubElement(root_xml, 'translate')
    translate_xml.text = "#".join(results['formalSentences'])
    # translate_xml.text=transRst.strip('\n')
    # getType()
    # type_xml = SubElement(root_xml, 'type')
    # type_xml.text=typeRst.strip('\n')
    tree = ElementTree(root_xml)
    sentence = results['rawSentence']
    sentence_xml.text = sentence

    # for prep in prepRst:
    #     tempPrep = SubElement(preposition_xml, prep)
    #     SubElement(tempPrep, 'role').text = prepRst[prep]
    verbRst = results.get('verb')
    if verbRst is not None :
        for verb in verbRst:
            verb = verbRst[verb]
            if verb['originVerb'] is None :
                return False
            verb_item = SubElement(verb_xml, verb['originVerb'])
            attrib = {}
            if "indexOfPlace" in verb and "belong" in verb :
                if verb['indexOfPlace'] is not None and verb['belong'] is not None :
                    attrib = {'indexOfPlace':str(verb['indexOfPlace']),'belong':verb['belong']}
                elif verb['indexOfPlace'] is not None  :
                    attrib = {'indexOfPlace':str(verb['indexOfPlace'])}
                elif verb['belong'] is not None :
                    attrib = {'belong':verb['belong']} 
            elif "indexOfPlace" in verb :
                if verb['indexOfPlace'] is not None :
                    attrib['indexOfPlace'] = str(verb['indexOfPlace'])                
            elif "belong" in verb :
                if verb['belong'] is not None :
                    attrib['belong'] = verb['belong']   
            if "isleft" in verb and verb['isleft'] is not None :
                attrib['isleft'] = str(verb['isleft'])
            if "isNegative" in verb and verb['isNegative'] is not None :
                attrib['isNegative'] = str(verb['isNegative'])
            # print(attrib)
            verb_item.attrib = attrib           
            # print(verb_item.attrib)
            source_xml = SubElement(verb_item, 'source')
            source_xml.text = 'propbank'
            word_xml = SubElement(verb_item,"wordInSentence")
            word_xml.text = verb['word']
            # num_xml = SubElement(verb_item, 'num')
            # num_xml.text = re.findall(r'.*\.(.*)', verb_num)[0]
            if "roles" in verb and verb['roles'] :
                thema_xml = SubElement(verb_item, 'thematicRoles')
                i = 0
                for r in verb['roles']:
                    argn = SubElement(thema_xml, 'arg' + str(i))
                    role = SubElement(argn, 'role')
                    role.text = r[0]
                    content = SubElement(argn,'content')
                    content.text = r[1]
                    # descr = SubElement(argn, 'descr')
                    # descr.text = dic['descr']
                    i += 1
    conjunctionRst = results.get("conjunction")
    if conjunctionRst is not None :
        for conjunction in conjunctionRst :
            conjunction = conjunctionRst[conjunction]
            conjunction_item = SubElement(conjunction_xml, conjunction['word'])
            if "indexOfPlace" in conjunction and "belong" in conjunction :
                if conjunction['indexOfPlace'] is not None and conjunction['belong'] is not None :
                    conjunction_item.attrib = {'indexOfPlace':str(conjunction['indexOfPlace']),'belong':conjunction['belong']}
                elif conjunction['indexOfPlace'] is not None  :
                    conjunction_item.attrib = {'indexOfPlace':str(conjunction['indexOfPlace'])}
                elif conjunction['belong'] is not None :
                    conjunction_item.attrib = {'belong':conjunction['belong']} 
            elif "indexOfPlace" in conjunction :
                if conjunction['indexOfPlace'] is not None  :
                    conjunction_item.attrib = {'indexOfPlace':str(conjunction['indexOfPlace'])}                
            elif "belong" in conjunction :
                if conjunction['belong'] is not None :
                    conjunction_item.attrib = {'belong':conjunction['belong']}  
            role_xml = SubElement(conjunction_item, 'thematic')
            role_xml.text = conjunction['role']['role']
            
            
    
    # translate_xml.text = transRst.strip('\n')
    # type_xml.text = typeRst.strip('\n')

    filename = results['filename']
    # f = open('./result/%s.xml' % filename,'a+')
    tree.write(filename, encoding='utf-8')
    return True