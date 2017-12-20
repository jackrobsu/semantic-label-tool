#!/usr/bin/env python
# encoding: utf-8
import sys
from utilities import *
from TreeWidget import Tree
from search import *


class VerbWidget(QMainWindow,QObject):
    textClickSignal = pyqtSignal(QWidget, int, CommonTextEdit)
    saverButtonSignal = pyqtSignal(QWidget,QWidget,QWidget)
    roleChoiceSingnal = pyqtSignal(list,list)
    def __init__(self,pWidget):
        super().__init__()
        self.pWidget = pWidget

        self.initializeVariables()

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
        self.originVerbWidget , self.originVerbLabel , self.originVerbTable = self._AddTableWithLabel("原形",self.lemmatizationWidget)
        # self.VerbingWidget , self.VerbingLabel , self.VerbingTable = self._AddTableWithLabel("按进行时",self.lemmatizationWidget)
        # self.pastVerbWidget , self.pastVerbLabel , self.pastVerbbTable = self._AddTableWithLabel("按过去时",self.lemmatizationWidget)
        # self.VerbesWidget , self.VerbesLabel , self.VerbesTable = self._AddTableWithLabel("按第三人称",self.lemmatizationWidget)
        

        self.searchButton = getButton("查找")
        self.searchButton.clicked.connect(self.SearchButtonClickEvent)
        
        vws = []
        vws.append(self.originVerbWidget)
        # vws.append(self.VerbingWidget)
        # vws.append(self.pastVerbWidget)
        # vws.append(self.VerbesWidget)
        vws.append(self.searchButton)
        self.middleWindow.setLayout(self._addWidgetInVBoxLayout(vws))
        middleWindowWidth = self.width() / 4

        #==========================================rightWindow==============================================        


        self.rightWindow = QWidget(self)
        self.rightWindow.resize(self.width() - leftWindowWidth - middleWindowWidth, self.height())

        self.treeItemChoiceButton = getButton("确定")

        for i in range(self.treeWidgetNum) :
            tree = Tree(self.rightWindow,self,i)
            self.treeItemChoiceButton.clicked.connect(tree.ItemChoiceEvent)
            self.trees.append(tree)
        if self.trees :
            buttonHeight = self.trees[0].height()
        else:
            buttonHeight = 100
        # self.tree = Tree(self.rightWindow,self)
        # self.rightTree = Tree(self.rightWindow,self)
        # self.tree.addTreeRoots(["root","berh"],{"root":[("A","a"),("PAG","pag")],"berh":[("b","b")]})
        # self.treeItemChoiceButton.clicked.connect(self.tree.ItemChoiceEvent)
        # self.treeItemChoiceButton.clicked.connect(self.rightTree.ItemChoiceEvent)
        middlewidget = self._addWidgetInVBoxLayout([self._addWidgetInHBoxLayout(self.trees,True),self.treeItemChoiceButton],True)
        self.preButton = getButton("上翻",40,buttonHeight,event=self.preButtonClickEvent)
        self.nextButton = getButton("下翻",40,buttonHeight,event=self.nextButtonClickEvent)
        self.rightWindow.setLayout(self._addWidgetInHBoxLayout([self.preButton,middlewidget,self.nextButton]))

        self.bigRightWindow = QMainWindow()
        vsplitter = QSplitter(Qt.Vertical)
        vsplitter.addWidget(self.middleWindow)
        vsplitter.addWidget(self.rightWindow)
        self.bigRightWindow.setCentralWidget(vsplitter)


        self.hsplitter = QSplitter(Qt.Horizontal)
        self.hsplitter.addWidget(self.leftWindow)
        # self.hsplitter.addWidget(self.middleWindow)
        # self.hsplitter.addWidget(self.rightWindow)
        self.hsplitter.addWidget(self.bigRightWindow)
        self.hsplitter.setStretchFactor(0,2)
        self.hsplitter.setStretchFactor(1,8)
        # self.hsplitter.setStretchFactor(2,5)
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
        self.preButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        

    def initializeVariables(self):
        self.treeWidgetNum = 2
        self.trees = []
        self.TreeItemMaximum = 9        
        self.currentPage = 1
        self.existedPages = [0]        
        self.roleRoots = []
        self.roleContents = {}
        self.curChoosedItemsInTreeWidget = []                      #用来保存当前TreeWidget中被选中的Items，用于翻页过程中的显示
        self.defaultRole = "-"

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
        table.setColumnCount(20)
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
  
    def _addWidgetInVBoxLayout(self,vws,widgetRequire=False) :
        vbox = QVBoxLayout()
        for vw in vws :
            vbox.addWidget(vw)
        if widgetRequire :
            widget = QWidget()
            widget.setLayout(vbox)
            return widget
        return vbox
    
    def _addWidgetInHBoxLayout(self,hws,widgetRequire=False) :
        hbox = QHBoxLayout()
        for hw in hws :
            hbox.addWidget(hw)
        if widgetRequire :
            widget = QWidget()
            widget.setLayout(hbox)
            return widget
        return hbox
        
    def updateRoleLabel(self,roles,indexs):
        '''
            用于更新role label的文本内容，响应“选择角色窗口”中的“确定”按钮
        '''
        
        def update():
            Roles = ["-"] * self.roleNum
            Roles[0:len(roles)] = roles
            for i , role in enumerate(Roles) :
                getattr(self,"role{}".format(i+1)).setText(role)
            self.curChoosedItemsInTreeWidget = indexs

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
            role , roleContent = addContent(self,self.defaultRole,controlcontents,rolenum+existedRoleNum,self.textClickSignal,tagWidth=self.tagWidth,contentWidth=self.contentWidth,checkBoxHidden=False)
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
            QMessageBox.warning(self,"警告",self.tr("没有找到动词 {} 可能的现在时态").format(verb),QMessageBox.Ok,QMessageBox.Ok)
            print("not found")
            

    def SearchButtonClickEvent(self):
        flag = False
        verb = None
        for table in self.lemmatizationWidget :
            items = table.selectedItems()
            if items is not None and items :
                flag = True
                verb = items[0].text().strip()
    
                break
        if not flag and self.lemmatizationWidget :
            table = self.lemmatizationWidget[0]
            # table = QTableWidget()
            item = table.itemAt(QPoint(0,0))
            if item is not None :
                verb = item.text().strip()
        if verb is None or verb == "" :
            return
        verbroles = extractXML(verb)
        if verbroles :
            self.showRoles(verbroles)
        else:
            QMessageBox.warning(self,"警告",self.tr("没有找到动词 {} 对应的词条信息").format(verb),QMessageBox.Ok,QMessageBox.Ok)
            print("not found in PropBank")
            
            

    def showRoles(self,roleset):
        def add(contents,word,roles):
            contents[word] = []
            Roles = sorted(roles,key=lambda x:x['num'])
            for r in Roles :
                contents[word].append((r['role'],r['descr']))
        # self.tree.clear()
        self.TreeWidgetClear(True)
        roots = []
        contents = {}
        for role in roleset :
            roots.append(role['word'])
            add(contents,role['word'],role['roles'])
        # self.tree.addTreeRoots(["root","berh"],{"root":[("A","a"),("PAG","pag")],"berh":[("b","b")]})
        self.roleRoots = roots
        self.roleContents = contents
        self.showPage()
        # self.tree.addTreeRoots(roots,contents)
    
    def getRoles(self):
        roles = []
        for rolenum in range(self.roleNum) :
            role = getattr(self,"role{}".format(rolenum+1)).text()
            content = getattr(self,"roleContent{}".format(rolenum+1)).toPlainText()
            if role == self.defaultRole :
                continue
            roles.append((role,content))
        return roles

    def showPage(self):
        '''
            用于分页显示
        '''
        def show(num,existedItemNum,role,content):
            size = len(content) + 1
            if size + existedItemNum > self.TreeItemMaximum :
                existedItemNum = 0
                num += 1
            if num >= self.treeWidgetNum :
                return False , 0 , 0
            
            if role in self.curChoosedItemsInTreeWidget :
                for i in self.curChoosedItemsInTreeWidget[:-1] :
                    existedContent = list(content[i])
                    existedContent.append(True)
                    content[i] = tuple(existedContent)
                    
            self.trees[num].addTreeRoots([role],{role:content})
            return True , num , size + existedItemNum


        currentTreeNum = 0
        existedItemNum = 0

        if not self.roleRoots :
            return
        flag = False

        roleRoots = None
        if self.currentPage >= len(self.existedPages) :
            roleRoots = self.roleRoots[self.existedPages[-1]:]
        else:
            roleRoots = self.roleRoots[self.existedPages[self.currentPage-1]:self.existedPages[self.currentPage]]
            flag = True

        if roleRoots is not None :
            if roleRoots :
                self.TreeWidgetClear()
            else:
                return
        else:
            return
        # print("currentPage ",self.currentPage)

        for index , root in enumerate(roleRoots) :
            c , currentTreeNum , existedItemNum = show(currentTreeNum,existedItemNum,root,list(self.roleContents[root]))
            if c == False :
                self.existedPages.append(self.existedPages[-1]+index)
                # print(self.existedPages)
                flag = True
                break
        if not flag :
            self.existedPages.append(self.existedPages[-1]+len(roleRoots))
         
            # print(self.existedPages)
        if len(self.roleRoots) > self.existedPages[-1] :
            self.nextButton.setEnabled(True)
        else:
            self.nextButton.setEnabled(False)
            
        

    def TreeWidgetClear(self,allClear=False):
        '''
            用于清空TreeWidget的Items，如果allClear为真，还会初始化分页现实的参数
        '''
        for tree in self.trees :
            tree.clear()

        if allClear :
            self.currentPage = 1
            self.existedPages = [0]    
            self.preButton.setEnabled(False)

    def preButtonClickEvent(self):
        '''
            前翻按钮
        '''
        if self.currentPage == 1 :
            return
        self.currentPage -= 1
        # print("pre ",self.currentPage)
        self.showPage()
        if self.currentPage == 1 :
            self.preButton.setEnabled(False)
        self.nextButton.setEnabled(True)

    def nextButtonClickEvent(self):
        '''
            后翻按钮
        '''
        self.currentPage += 1        
        if len(self.roleRoots) <= self.existedPages[-1] :
            if self.currentPage >= len(self.existedPages) :
                self.currentPage = len(self.existedPages) - 1
        
        self.showPage()
        self.preButton.setEnabled(True)


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



 