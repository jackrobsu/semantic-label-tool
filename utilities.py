#-*- coding:utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTabWidget
from PyQt5.QtWidgets import *

class CommonTextEdit(QTextEdit):
    __qualname__ = 'CommonTextEdit'

    def __init__(self, obj, signal, num=(0, )):
        super().__init__()
        self.signal = signal
        self.num = num
        self.dependencyObj = obj

    def mousePressEvent(self, event):
        self.signal.emit(self.dependencyObj,self.num,self)


def addContent(obj,text,controlcontents,num=0,signal=None,tagHeight=30,tagWidth=30,contentHeight=30,contentWidth=100):
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
    controlcontents.append(tag)
    controlcontents.append(content)
    return tag, content

def textEditSelectionChanged(widgetObj,num, textobj):
    if not hasattr(widgetObj,"allLabels") :
        return
    for (i, label) in enumerate(widgetObj.allLabels):
        obj = getattr(widgetObj, label)
        if i == num:
            obj.setStyleSheet('color:green;')
            widgetObj.selectedRoleContent = textobj
            continue
        obj.setStyleSheet('color:black')