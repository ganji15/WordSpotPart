# -*- coding: gbk -*-

import os
import sys  

from PyQt4.QtGui import *  
from PyQt4.QtCore import *
from FileDialog import *

from utils.recognize import recognize

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))  



class MyTable(QTableWidget):  
    def __init__(self,parent=None):  
        super(MyTable,self).__init__(parent)  
        self.setColumnCount(9)  
        self.setRowCount(2)
        self.setItem(0,0,QTableWidgetItem(self.tr(u"ҵ��Ʒ��".encode('utf8'))))  
        self.setItem(0,1,QTableWidgetItem(self.tr(u"����".encode('utf8'))))
        self.setItem(0,2,QTableWidgetItem(self.tr(u"����".encode('utf8'))))  
        self.setItem(0,3,QTableWidgetItem(self.tr(u"����".encode('utf8'))))
        self.setItem(0,4,QTableWidgetItem(self.tr(u"���".encode('utf8'))))  
        self.setItem(0,5,QTableWidgetItem(self.tr(u"����".encode('utf8'))))  
        self.setItem(0,6,QTableWidgetItem(self.tr(u"���׶���".encode('utf8'))))  
        self.setItem(0,7,QTableWidgetItem(self.tr(u"����".encode('utf8'))))
        self.setItem(0,8,QTableWidgetItem(self.tr(u"ծȯ����".encode('utf8'))))
        #self.setItem(0,9,QTableWidgetItem(self.tr(u"��ע".encode('utf8'))))
        self.items = []
        for i in xrange(9):
            item = QLabel("")
            self.setCellWidget(1, i, item)
            self.items.append(item)


    def set_content(self, infos):
        for i, cell in enumerate(self.items):
            self.items[i].setText(infos[i])


class CenterWidget(QWidget):
    def __init__(self, parent = None):
        super(CenterWidget, self).__init__(parent)
        self.setWindowTitle(u'sd')

        self.table = MyTable()
        
        self.lineEdit = QLineEdit() 
        
        self.btnRecognize=QPushButton(self.tr(u"ok"))
        self.btnRecognize.clicked.connect(self.doRecognize)

        vLayout=QVBoxLayout(self)
        hLayout=QHBoxLayout()
        hLayout.addWidget(QLabel(self.tr(u'ҵ������'.encode("utf-8"))))
        hLayout.addWidget(self.lineEdit)
        hLayout.addWidget(self.btnRecognize)

        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.table)


    def doRecognize(self):
        text = self.lineEdit.text()
        res = recognize(unicode(text.toUtf8(),'utf8', 'ignore'))
        self.table.set_content(res)
        

class MainWindow(QMainWindow):  
    def __init__(self,parent=None):  
        super(MainWindow,self).__init__(parent)  
        self.setWindowTitle(self.tr("Word Spot"))  
        self.imageLabel=QLabel()  
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)  
        self.setCentralWidget(self.imageLabel)

        centerWin=CenterWidget()  
        self.setCentralWidget(centerWin)

        self.resize(1000, 180)
        

if __name__ == '__main__':
    app=QApplication(sys.argv)  
    main=MainWindow()  
    main.show()  
    app.exec_()  