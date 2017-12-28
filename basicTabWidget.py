from utilities import *
from verbWidget import VerbWidget
from conjunctionWidget import ConjunctionWidget
from nounWidget import NounWidget

class BasicTabWidget(QMainWindow):
    '''
        基本Tab框，内部包含若干个VerbWidget
    '''
    tabAddSignal = pyqtSignal(QWidget)
    def __init__(self,pWidget,widgetType):
        super(BasicTabWidget,self).__init__()
        self.pWidget = pWidget        
        self.widgetType = widgetType
        
        self.splitWindow()
        
        self.setCentralWidget(self.hsplitter)
        self.resize(self.sizeHint())
        self.initialize()        
        self.show()

    def splitWindow(self):
        self.hsplitter = QSplitter(Qt.Horizontal)
        #left window
        self.leftWindow = QWidget()
        self.tabAddButton = SignalWithHandleButton(self.tabAddSignal,self)
        self.tabAddButton.setText("添加标签")
        self.vboxOfLeftWindow = QVBoxLayout()
        
        self.vboxOfLeftWindow.addWidget(self.tabAddButton)
        self.vboxOfLeftWindow.addStretch(1)
        
        self.leftWindow.setLayout(self.vboxOfLeftWindow)
        self.leftWindow.setHidden(True)  #暂时隐藏


        self.rightWindow = QTabWidget()
        self.defaultTab = "未命名标签"
        # if self.widgetType == WidgetType.VERB :
        #     self.rightWindow.addTab(VerbWidget(self.pWidget),self.defaultTab)
        # elif self.widgetType == WidgetType.CONJUNCTION :
        #     self.rightWindow.addTab(ConjunctionWidget(self.pWidget),self.defaultTab)
        # elif self.widgetType == WidgetType.NOUN :
        #     self.rightWindow.addTab(NounWidget(self.pWidget),self.defaultTab)
        

            

        self.tabWindow = self.rightWindow
        
        self.hsplitter.addWidget(self.leftWindow)
        self.hsplitter.addWidget(self.rightWindow)
        self.hsplitter.setStretchFactor(0,0.5)
        self.hsplitter.setStretchFactor(1,8)

    def initialize(self) :
        self.tabAddSignal.connect(tabAdd)

    def resetWidget(self):
        self.tabWindow.clear()
        # pass
    def addTab(self):
        tabAdd(self)

class CommonTabBar(QTabBar):
    def __init__(self,pWidget):
        super().__init__()
        self.pWidget = pWidget

    def mousePressEvent(self,event):
        tabid = self.tabAt(event.pos())
        if tabid == self.pWidget.tabWindow.count() - 1 :
            self.pWidget.addTab()
            # super().mousePressEvent(event)
            
        else:
            print(tabid)
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self,event):
        '''
            双击关闭标签页
        '''
        tabid = self.tabAt(event.pos())
        if tabid == self.pWidget.tabWindow.count() - 1 :
            super().mouseDoubleClickEvent(event)
        else:
            self.pWidget.tabWindow.removeTab(tabid)
    

class VerbTabWidget(BasicTabWidget):
    def __init__(self,pWidget):
        super(VerbTabWidget,self).__init__(pWidget,WidgetType.VERB)
        self.tabWindow.setTabBar(CommonTabBar(self))
        # self.tabWindow.setTabsClosable(True)
        self.tabWindow.setCurrentIndex(0)



class ConjunctionTabWidget(BasicTabWidget) :
    def __init__(self,pWidget):
        super(ConjunctionTabWidget,self).__init__(pWidget,WidgetType.CONJUNCTION)
        self.tabWindow.setTabBar(CommonTabBar(self))
