from utilities import *

class TreeItem(QTreeWidgetItem):
    def __init__(self, s, parent = None):  
  
        super(TreeItem, self).__init__(parent, [s])  
        
    
    
    
class Tree(QTreeWidget):  
  
    def __init__(self, parent = None , mainWindow=None , windowIndex=0 , mutexAnyItem=False , callback=None):  
  
        super(Tree, self).__init__(parent)  
        self.mainWindow = mainWindow
        self.setMinimumWidth(200)  
        self.setMinimumHeight(200)
        # self.resize(self.sizeHint())
        self.setColumnCount(2)
        #设置头部信息，因为上面设置列数为2，所以要设置两个标识符
        self.setHeaderLabels(['Verb','Description'])
        self.itemClicked.connect(self.ItemClickedEvent)
        self.itemDoubleClicked.connect(self.ItemDoubleClickedEvent)
        self.windowIndex = windowIndex
        self.mutexAnyItem = mutexAnyItem
        self.callback = callback
        # self.addTopLevelItem(root)
        # for s in ['foo', 'bar']:  
        #     MyTreeItem(s, self)  
        # self.connect(self, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.onClick)  

    def addTreeWidgetItems(self,treeRoot,items=[]):
        for item in items :
            if len(item) == 0 :
                continue
            treeitem = QTreeWidgetItem(treeRoot)
            if len(item) == 1 :
                treeitem.setText(0,item[0])
            elif len(item) > 1 :
                treeitem.setText(0,item[0])
                treeitem.setText(1,item[1])
             
            if len(item) > 2 and item[2] == True : 
                treeitem.setCheckState(0,Qt.Checked)
            else:                    
                treeitem.setCheckState(0,Qt.Unchecked)
                
    def addTreeRoots(self,treeRoots,valueDict={}):
        for tr in treeRoots :
            r = QTreeWidgetItem(self)
            r.setText(0,tr)
            r.setExpanded(True)
            self.addTreeWidgetItems(r,valueDict[tr])
            self.addTopLevelItem(r)
        for col in range(self.columnCount()):
            self.resizeColumnToContents(col)
        
    def ItemClickedEvent(self,WidgetItem):
        
        def Clear(clickedItemIndex,obj):
            for index in range(obj.topLevelItemCount()) :
                if index == clickedItemIndex and not self.mutexAnyItem :
                    continue
                item = obj.topLevelItem(index)
                for subItemIndex in range(item.childCount()) :
                    subItem = item.child(subItemIndex)
                    if subItem is WidgetItem :
                        continue
                    subItem.setCheckState(0,Qt.Unchecked)

        if WidgetItem is None :
            return
        if WidgetItem.checkState(0) != Qt.Checked :
            return
        item = QTreeWidgetItem()
        clickedItemIndex = self.indexOfTopLevelItem(WidgetItem.parent())
        if clickedItemIndex == -1 :
            return
        if self.callback is not None :
            self.callback(WidgetItem)
        Clear(clickedItemIndex,self)
        for treeWidget in self.mainWindow.trees :
            if treeWidget.windowIndex == self.windowIndex :
                continue
            Clear(-1,treeWidget)

            
    def ItemChoiceEvent(self):
        '''
            用来响应语义选择按钮的点击事件
        '''
        roles = []
        indexs = []
        pItem = None
        for pitem , item , itemIndex in self.ItemIteration() :
            if item.checkState(0) == Qt.Checked :
                roles.append(item.text(0))
                pItem = pitem
                indexs.append(itemIndex)
        if self.mainWindow is not None and roles :
            if pItem is not None :
                print(pItem.text(0))
                # roles.append(pItem.text(0))
                indexs.append(pItem.text(0))
            else:
                indexs.append(None)
            print(indexs)
            self.mainWindow.roleChoiceSingnal.emit(roles,indexs)

    def ItemIteration(self):
        for index in range(self.topLevelItemCount()) :
            item = self.topLevelItem(index)
            for subItemIndex in range(item.childCount()) :
                subItem = item.child(subItemIndex)
                yield item , subItem , subItemIndex
    
    def ItemDoubleClickedEvent(self,WidgetItem,I):
        if WidgetItem is None :
            return
        if self.indexOfTopLevelItem(WidgetItem) != -1 :
            return
        if WidgetItem.checkState(0) == Qt.Checked :
            WidgetItem.setCheckState(0,Qt.Unchecked)
        else:
            WidgetItem.setCheckState(0,Qt.Checked)
        
        self.itemClicked.emit(WidgetItem,I)

    def onClick(self, item, column):  
  
        print(item.text(0))  
class MainWindow(QMainWindow):  
  
    def __init__(self, parent = None):  
  
        super(MainWindow, self).__init__(parent)  
        self.tree = Tree(self) 

class TreeWidget(QMainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        
        self.setWindowTitle('TreeWidget')
        #创建一个Qtree部件
        self.tree = QTreeWidget()
        #设置部件的列数为2
        self.tree.setColumnCount(2)
        #设置头部信息，因为上面设置列数为2，所以要设置两个标识符
        self.tree.setHeaderLabels(['Key','Value'])
        
        #设置root为self.tree的子树，所以root就是跟节点
        root= QTreeWidgetItem(self.tree)
        #设置根节点的名称
        root.setText(0,'root')
        
        #为root节点设置子结点
        child1 = QTreeWidgetItem(root)
        child1.setText(0,'child1')
        child1.setText(1,'name1')
        child2 = QTreeWidgetItem(root)
        child2.setText(0,'child2')
        child2.setText(1,'name2')
        child3 = QTreeWidgetItem(root)
        child3.setText(0,'child3')
        child4 = QTreeWidgetItem(child3)
        child4.setText(0,'child4')
        child4.setText(1,'name4')
        
        self.tree.addTopLevelItem(root)
        #将tree部件设置为该窗口的核心框架
        self.setCentralWidget(self.tree)