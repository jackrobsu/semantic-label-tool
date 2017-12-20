#!/usr/bin/env python
# encoding: utf-8
import sys
from utilities import *
from TreeWidget import Tree
from search import *


class VerbWidget(QMainWindow,QObject):
    textClickSignal = pyqtSignal(QWidget, int, CommonTextEdit)
    saverButtonSignal = pyqtSignal(QWidget,QWidget,QWidget)
    roleChoiceSingnal = pyqtSignal(list)
    def __init__(self,pWidget):
        super().__init__()
        self.pWidget = pWidget


        #==========================================leftWindow========================================
        
        self.leftWindow = QWidget()
        self.lemmatization = getButton("词形还原")
        self.lemmatization.clicked.connect(self.lemmatizationButtonClickEvent)
        controlcontents = []
        self.contentWidth = 150
        self.tagWidth = 40
        (self.verb,self.verbContent) = addContent(self,'动词', controlcontents, 0 , self.textClickSignal,tagWidth=self.tagWidth,contentWidth=self.contentWidth)
        
        # (self.role1,self.roleContent1) = addContent(self,'role1', controlcontents, 1 , self.textClickSignal,tagWidth=tagWidth,contentWidth=contentWidth)
        # (self.role2,self.roleContent2) = addContent(self,'role2', controlcontents, 2 , self.textClickSignal,tagWidth=tagWidth,contentWidth=contentWidth)
        # (self.role3,self.roleContent3) = addContent(self,'role3', controlcontents, 3 , self.textClickSignal,tagWidth=tagWidth,contentWidth=contentWidth)

        self.roleNum = 0
        self.allLabels = ['verb']
        
        self.addRoleContent(self.roleNum,self.allLabels,controlcontents)
        # roles = range(self.roleNum)
        # for rolenum in roles :
        #     rolename = "role{}".format(rolenum+1)
        #     role , roleContent = addContent(self,"-",controlcontents,rolenum+1,self.textClickSignal,tagWidth=tagWidth,contentWidth=contentWidth)
        #     setattr(self,rolename,role)
        #     setattr(self,"roleContent{}".format(rolenum+1),roleContent)

        # self.allLabels.extend([ "role"+str(i+1) for i in roles ])
        self.gridbox = QGridLayout()
        self.gridbox.setHorizontalSpacing(0)
        # print(len(controlcontents))
        self.AddElementIntoGridBox(controlcontents,3)

        self.buttonSaver = SaverButton(self,self.saverButtonSignal,self.pWidget,WidgetType.VERB)
        self.buttonSaver.setText("保存")

        vbox = QVBoxLayout()
        vbox.addLayout(self.gridbox)
        # vbox.addStretch(1)
        subhbox = QHBoxLayout()
        
        subhbox.addWidget(self.buttonSaver)
        subhbox.addWidget(self.lemmatization)
        vbox.addLayout(subhbox)
        self.leftWindow.setLayout(vbox)  #self.gridbox

        leftWindowWidth = self.width() / 4
        if leftWindowWidth < self.contentWidth + self.tagWidth:
            pass
        leftWindowWidth = leftWindowWidth
        # self.leftWindow.resize(leftWindowWidth, self.height())


        #==========================================middleWindow===============================================

        self.middleWindow = QWidget()
        self.lemmatizationWidget = []        
        self.originVerbWidget , self.originVerbLabel , self.originVerbTable = self._AddTableWithLabel("按原形",self.lemmatizationWidget)
        self.VerbingWidget , self.VerbingLabel , self.VerbingTable = self._AddTableWithLabel("按进行时",self.lemmatizationWidget)
        self.pastVerbWidget , self.pastVerbLabel , self.pastVerbbTable = self._AddTableWithLabel("按过去时",self.lemmatizationWidget)
        self.VerbesWidget , self.VerbesLabel , self.VerbesTable = self._AddTableWithLabel("按第三人称",self.lemmatizationWidget)
        

        self.searchButton = getButton("查找")
        self.searchButton.clicked.connect(self.SearchButtonClickEvent)
        
        vws = []
        vws.append(self.originVerbWidget)
        vws.append(self.VerbingWidget)
        vws.append(self.pastVerbWidget)
        vws.append(self.VerbesWidget)
        vws.append(self.searchButton)
        self.middleWindow.setLayout(self._addWidgetInVBoxLayout(vws))
        middleWindowWidth = self.width() / 4

        #==========================================rightWindow==============================================        


        self.rightWindow = QWidget(self)
        self.rightWindow.resize(self.width() - leftWindowWidth - middleWindowWidth, self.height())

        self.tree = Tree(self.rightWindow,self)
        # self.tree.addTreeRoots(["root","berh"],{"root":[("A","a"),("PAG","pag")],"berh":[("b","b")]})
        self.treeItemChoiceButton = getButton("确定")
        self.treeItemChoiceButton.clicked.connect(self.tree.ItemChoiceEvent)
        self.rightWindow.setLayout(self._addWidgetInVBoxLayout([self.tree,self.treeItemChoiceButton]))

        
        self.hsplitter = QSplitter(Qt.Horizontal)
        self.hsplitter.addWidget(self.leftWindow)
        self.hsplitter.addWidget(self.middleWindow)
        self.hsplitter.addWidget(self.rightWindow)
        self.hsplitter.setStretchFactor(0,2)
        self.hsplitter.setStretchFactor(1,3)
        self.hsplitter.setStretchFactor(2,5)
        self.setCentralWidget(self.hsplitter)
        self.resize(self.sizeHint())
        self.initialize()
        self.show()

    def getContent(self):
        return self.verbContent.toPlainText()

    def initialize(self):
        self.textClickSignal.connect(textEditSelectionChanged)
        self.saverButtonSignal.connect(saveLexicon)
        self.roleChoiceSingnal.connect(self.updateRoleLabel)
        self.selectedRoleContent = None
        self.widgetID = UnionID()
        self.widgetType = WidgetType.VERB

        # self.pWidget.verbListwidget.itemDoubleClicked.connect()

    def _AddTableWithLabel(self,text,Container=None):
        '''
            用于创建中间窗口的标签和表格
        '''
        widget = QWidget()
        label = QLabel()
        label.setText(text)
        label.setFixedWidth(70)
        table = QTableWidget()
        table.setRowCount(1)
        table.setColumnCount(5)
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setShowGrid(False)
        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(table)
        widget.setLayout(hbox)
        widget.setFixedHeight(70)
        if Container is not None :
            Container.append(table)
        return widget , label , table
  
    def _addWidgetInVBoxLayout(self,vws) :
        vbox = QVBoxLayout()
        for vw in vws :
            vbox.addWidget(vw)
        return vbox
        
    def updateRoleLabel(self,roles):
        '''
            用于更新role label的文本内容，响应右窗口的“确定”按钮
        '''
        
        def update():
            Roles = ["-"] * self.roleNum
            Roles[0:len(roles)] = roles
            for i , role in enumerate(Roles) :
                getattr(self,"role{}".format(i+1)).setText(role)

        if len(roles) <= self.roleNum :
            update()
        else:
            rolelength = len(roles)
            addedRoleNum = rolelength - self.roleNum
            controlcontents = []
            self.addRoleContent(addedRoleNum,self.allLabels,controlcontents)
            self.AddElementIntoGridBox(controlcontents,initialRow=self.gridbox.rowCount())
            print(len(controlcontents),addedRoleNum)

            self.roleNum += addedRoleNum
            update()


    def addRoleContent(self,num,labels,controlcontents):
        '''
            用于增加role label和role content
        '''
        roles = range(num)
        existedRoleNum = len(labels)
        for rolenum in roles :
            rolename = "role{}".format(rolenum+existedRoleNum)
            role , roleContent = addContent(self,"-",controlcontents,rolenum+existedRoleNum,self.textClickSignal,tagWidth=self.tagWidth,contentWidth=self.contentWidth,checkBoxHidden=False)
            setattr(self,rolename,role)
            setattr(self,"roleContent{}".format(rolenum+existedRoleNum),roleContent)
            print("roleContent{}".format(rolenum+existedRoleNum))
            labels.append(rolename)

    def AddElementIntoGridBox(self,controlcontents,numOfEachRow=3,initialRow=0):
        for (i, tag) in enumerate(controlcontents):
            row = int(i / numOfEachRow) + initialRow
            col = i - ( row - initialRow ) * numOfEachRow
            self.gridbox.addWidget(tag, row, col)

        self.gridbox.setHorizontalSpacing(5)
        

    def lemmatizationButtonClickEvent(self):
        '''
            词形还原按钮点击事件
        '''
        verb = self.verbContent.toPlainText()
        if verb is "" :
            return
        # print(verb)
        verbs = searchVerb(verb)
        if verbs is not None and isinstance(verbs,set) and verbs :
            verbs = list(verbs)
            showContentInTableWidget(self.originVerbTable,verbs)
            # print(extractXML(verbs[0]))
        else:
            print("not found")

    def SearchButtonClickEvent(self):
        for table in self.lemmatizationWidget :
            items = table.selectedItems()
            if items is not None and items :
                verb = items[0].text().strip()
                if verb == "" :
                    break
                verbroles = extractXML(verb)
                if verbroles :
                    self.showRoles(verbroles)
                else:
                    print("not found in PropBank")
                break

    def showRoles(self,roleset):
        def add(contents,word,roles):
            contents[word] = []
            Roles = sorted(roles,key=lambda x:x['num'])
            for r in Roles :
                contents[word].append((r['role'],r['descr']))
        self.tree.clear()
        roots = []
        contents = {}
        for role in roleset :
            roots.append(role['word'])
            add(contents,role['word'],role['roles'])
        # self.tree.addTreeRoots(["root","berh"],{"root":[("A","a"),("PAG","pag")],"berh":[("b","b")]})
        self.tree.addTreeRoots(roots,contents)
    
    def getRoles(self):
        roles = []
        for rolenum in range(self.roleNum) :
            role = getattr(self,"role{}".format(rolenum+1)).text()
            content = getattr(self,"roleContent{}".format(rolenum+1)).toPlainText()
            roles.append((role,content))
        return roles

# class VerbTabWidget(QMainWindow):
#     '''
#         基本Tab框，内部包含若干个VerbWidget
#     '''
#     tabAddSignal = pyqtSignal(QWidget)
#     def __init__(self,pWidget):
#         super(VerbTabWidget,self).__init__()
#         self.pWidget = pWidget        
#         self.splitWindow()
        
#         self.setCentralWidget(self.hsplitter)
#         self.resize(self.sizeHint())
#         self.initialize()        
#         self.show()

#     def splitWindow(self):
#         self.hsplitter = QSplitter(Qt.Horizontal)
#         #left window
#         self.leftWindow = QWidget()
#         self.tabAddButton = SignalWithHandleButton(self.tabAddSignal,self)
#         self.tabAddButton.setText("添加标签")
#         self.vboxOfLeftWindow = QVBoxLayout()
        
#         self.vboxOfLeftWindow.addWidget(self.tabAddButton)
#         self.vboxOfLeftWindow.addStretch(1)
        
#         self.leftWindow.setLayout(self.vboxOfLeftWindow)

#         self.rightWindow = QTabWidget()
#         self.defaultTab = "未命名标签"
#         self.rightWindow.addTab(VerbWidget(self.pWidget),self.defaultTab)

#         self.tabWindow = self.rightWindow
        
#         self.hsplitter.addWidget(self.leftWindow)
#         self.hsplitter.addWidget(self.rightWindow)
#         self.hsplitter.setStretchFactor(0,0.5)
#         self.hsplitter.setStretchFactor(1,8)

#     def initialize(self) :
#         self.tabAddSignal.connect(tabAdd)



 