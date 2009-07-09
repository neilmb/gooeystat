#!/usr/bin/env python

# Copyright (C) 2008, 2009  Spencer Herzberg <spencer.herzberg@gmail.com>

# This file is part of GooeyStat

# GooeyStat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from plugins.helpers.processable import Processable
from math import *
from scipy.stats import *
import time

from gooeylib import trace

def adddict(dict1, dict2):
    return dict(dict1, **dict2)


class GooeyMDI(QMdiArea):
    def __init__(self,parent=None):
        QMdiArea.__init(self,parent)
        
    def fileNew(self):
        self.addWidget( GooeyEdit() )
    
    def fileOpen(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "./", "GooeyEdit Files (*.gef *.csv )")
        if fileName != "":
            self.addWidget( GooeyEdit(fileName) )
    
    def fileSave(self):
        self.getCurrentWidget().save()
    
    def fileSaveAs(self):
        pass
    
    def getCurrentWidget(self):
        return self.currentSubWindow().widget()
    
    def addWidget(self,widget=None):
        if not what:
            what = Qwidget()
        self.addSubWindow(what)
        if len( self.subWindowList() ) == 1:
            what.showMaximized()
        else:
            what.show()

        
class Cell(QTableWidgetItem):
    def __init__(self,item=""):
        QTableWidgetItem.__init__(self,item,1000)
        #self.setBackground( QBrush( QColor('orange') ) )

    def setFormula(self,formula):
        self.setData(Qt.EditRole, formula)


class HeaderCell(QTableWidgetItem):
    def __init__(self, parent=None):
        QTableWidgetItem.__init__(self,1001)
        self.setTextAlignment(Qt.AlignCenter)
        self.setToolTip("This is a header name, do not put raw data here...")
        self.setFlags( Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled )
        self.setBackground( QBrush( QColor('grey') ) )


class GooeyEdit(QTableWidget):
    
    def __init__(self, fileName="Untitled", parent=None):
        QTableWidget.__init__(self,parent)
        
        self._initWidget()
        self._initActions()
        self.fileName = fileName
        self.setWindowTitle(self.fileName)
        
        self.dirty=False

    def _initWidget(self):
        self.setColumnCount(50)
        self.setRowCount(2000)

        vh = QStringList()
        vh.append("Name")
        for i in range(1,self.columnCount()+1):
            vh.append( str(i) )
        self.setVerticalHeaderLabels( vh )
        

        for x in range(self.columnCount()):
            self.setItem(0,x,HeaderCell(self) )

        for y in range(1, self.rowCount() +1 ):
            for x in range(self.columnCount() +1 ):
                self.setItem(y,x,Cell())


        self.connect(self,SIGNAL("itemChanged(QTableWidgetItem*)"),self.somethingChanged)

    def _initActions(self):

        self.pasteAction = QAction("Paste",  self)
        self.pasteAction.setShortcut("Ctrl+V")
        self.addAction(self.pasteAction)
        self.connect(self.pasteAction, SIGNAL("triggered()"), self.paste) 

        self.copyAction = QAction("Copy", self)
        self.copyAction.setShortcut("Ctrl+C")
        self.addAction(self.copyAction)
        self.connect(self.copyAction, SIGNAL("triggered()"), self.copy)
        
        self.cutAction= QAction("Cut", self)
        self.cutAction.setShortcut("Ctrl+X")
        self.addAction(self.cutAction)
        self.connect(self.cutAction,SIGNAL("triggered()"),self.cut)


        self.deleteAction = QAction("Delete",self)
        self.deleteAction.setShortcut("Delete")
        self.addAction(self.deleteAction)
        self.connect(self.deleteAction,SIGNAL("triggered()"),self.delete)
        
    def paste(self):
        trace.mutter("Paste")
        cb = QApplication.clipboard()
        clipText = cb.text()
        t0 = time.time()
        clip2paste = self.splitClipboard(clipText)
       
        selRange  = self.selectedRanges()[0]#just take the first range
        topRow = selRange.topRow()
        bottomRow = selRange.bottomRow()
        rightColumn = selRange.rightColumn()
        leftColumn = selRange.leftColumn()

        #test to ensure pasted area fits in table
        t1 = time.time()
        #print "Clipboard split time:",  (t1-t0)
        if (len(clip2paste)+topRow) >= self.rowCount():
            self.setRowCount(len(clip2paste)+topRow)
        t2 = time.time()
        #print "Row set time:",  (t2-t1)
       
        if (len(clip2paste[0])+rightColumn) >= self.columnCount():
            self.setColumnCount(len(clip2paste[0])+rightColumn)
        t3 = time.time()
        #print "Column set time:", (t3-t2)
        self.addData(clip2paste, topRow,  leftColumn)
        #print "Data Add Time:", (time.time()-t3)
   
    def splitClipboard(self,  clipText):
        #create list to be returned
        returnClip = []
        #split by carriage return which makes the rows
        clipList = clipText.split("\r\n")
        #split each item by tab (aka columns)
        for item in clipList:
            returnClip.append(item.split("\t"))
       
        return returnClip
           
    def copy(self):
        trace.mutter("Copy")
        selRange  = self.selectedRanges()[0]#just take the first range
        topRow = selRange.topRow()
        bottomRow = selRange.bottomRow()
        rightColumn = selRange.rightColumn()
        leftColumn = selRange.leftColumn()
        #item = self.tableWidget.item(topRow, leftColumn)
        clipStr = QString()
        for row in xrange(topRow, bottomRow+1):
            for col in xrange(leftColumn, rightColumn+1):
                cell = self.item(row, col)
                if cell:
                    clipStr.append(cell.text())
                else:
                    clipStr.append(QString(""))
                clipStr.append(QString("\t"))
            clipStr.chop(1)
            clipStr.append(QString("\r\n"))
       
        cb = QApplication.clipboard()
        cb.setText(clipStr)
    
    def cut(self):
        trace.mutter("Cut")
        self.copy()
        self.delete()
        
    def delete(self):
        for cell in self.selectedItems():
            cell.setText("")

        self.setCurrentCell( self.currentRow()-1,self.currentColumn())
    
    def addData(self, data, startrow=None,  startcol = None):
        if startcol:
            sc = startcol#start column
        else:
            sc = 0 # n is for columns
        if startrow:
            sr = startrow
        else:
            sr = 0
       
        m = sr
        #print "Row, Col Commit:", sr, n
        for row in data:
            n = sc
            for item in row:
                #print repr(str(item))
                #newitem = QTableWidgetItem(item) #old
                #self.setItem(m,  n,  newitem) #old
                self.item(m,n).setText(item)
                n+=1
            m+=1 

    def isDirty(self):
        return self.dirty
    
    def somethingChanged(self,something):
        self.dirty=True
        self.setCurrentCell(  self.currentRow()+1 , self.currentColumn() )

    def getFileName(self):
        return self.fileName

    def load(self,fileName):
        fileName=str(fileName)
        if fileName.find(".gef")>0:
            for y,line in enumerate(open(fileName).readlines()):
                for x,item in enumerate(line.split("\t")):
                    if item!="\n":
                        #print "\t\t\t|",item
                        item=item.strip()
                        self.item(y,x).setText(item)
                    
            self.fileName = fileName[str(fileName).rfind("/")+1:]
            self.setWindowTitle(self.fileName)

        elif fileName.find(".csv")>0:
            for y,line in enumerate(open(fileName).readlines()):
                for x,item in enumerate(line.split(",")):
                    if item!="\n":
                        item=item.strip()
                        self.item(y+1,x).setText(item)
                    
            self.fileName = fileName[str(fileName).rfind("/")+1:]
            self.setWindowTitle(self.fileName)    
        
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error!")
            msg.setText("The file %s is invalid. \n\nPlease use files with the 'gef' extension." %fileName)
            msg.exec_()
        self.dirty=False

    def saveAs(self,fileName):
        output=""

        if self.dirty:
            for y in range( self.rowCount() ):
                count=0
                foundSomethin=False
                for x in range( self.columnCount() ):
                    item=self.item(y,x)
                    if item:
                        if item.text()!="":
                            foundSomethin=True
#                            print "x:%d y:%d ==%s" %(x,y,item.text())
                            
                            output+= "\t"*count+item.text()
                            count=1
                        else:
                            count+=1
                if foundSomethin: output+="\n"
    
            
            try:
                outfile = open(fileName,"w")
                outfile.write(output)
                outfile.close()
                self.fileName = fileName[str(fileName).rfind("/")+1:]
                self.setWindowTitle(self.fileName)
                self.dirty=False
            except:
                pass
            
        else:
            pass

    def getNonEmpty(self):#getDataCols
        nonEmpty = {}
        for x in range(self.columnCount()):
            col = self.getColData(x)
            
            if len( col ) != 0:
                nonEmpty[x]= self.getName(x)
        
        return nonEmpty
    
    def getColDataFromName(self,name):
        return self.getColData(self.getColFromName(name))
        
    def getColData(self,col):
        p=Processable([])
        y=1
        item=self.item(y,col)
        while item.text() != "":
            p.add( str(item.text()) )
            y+=1
            item=self.item(y,col)
        return p
    
    def getName(self,col):
        name=str(self.item(0,col).text())
        if name=="":
            return str(col+1)
        else:
            return name
    
    def getColFromName(self,name):
        if name.strip()=="":
            return -1
        for x in range(self.columnCount()):
            if str(self.item(0,x).text()) == name:
                return x
        try:
            col=eval(name)-1
            return col
        except:
            pass
        return -1


class CommandLine(QLineEdit):
    
    def __init__(self,parent=None):
        QLineEdit.__init__(self,parent)
        self.history = [None]
        self.pointer = -1 #always points to the last thing
        
    def keyPressEvent(self,event):
    
        if event.key() == Qt.Key_Enter    or    event.key()==Qt.Key_Return:
            self.history.append(str(self.text()))
            self.pointer=len(self.history)-1
            if (len(self.history) == 1):
                self.pointer = 0
            
        
#        elif event.key() == Qt.Key_:
#            print
#            print "history:",self.history
#            print "pointer:",self.pointer,self.history[self.pointer]
            
        elif event.key() == Qt.Key_Up:
            '''
            key up
            '''
            p = self.pointer
            if p==0: #special case
                self.setText( self.history[p] )
            elif p>0:
                
                self.setText( self.history[p] )
                self.pointer-=1
                
                
        elif event.key() == Qt.Key_Down:
            '''
            key down
            '''
            p = self.pointer
            if len(self.history)==0:
                return
            elif p+1>=len(self.history):
                self.setText("")
            else:
                self.pointer+=1
                self.setText( self.history[self.pointer] )            
                
                
                
                
        QLineEdit.keyPressEvent(self,event)
        
    def grabOutput(self):
        txt = str( self.text() )
        self.clear()
        try:
            answer = eval(txt)
        except:
            return "Invalid Expression"
        return answer


class Console(QWidget):
    
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setLayout(QVBoxLayout())
        
        self.input = QLineEdit(self)
        self.connect(self.input,SIGNAL("returnPressed()"),self.handleConsole)
        
        self.history = [""]
        self.pointer = 0
        
        self.layout().addWidget(self.input)
        
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        
        self.layout().addWidget(self.output)
        
        btn_clear = QPushButton("Clear")
        self.connect( btn_clear, SIGNAL("clicked()"),self.clearOutput )
        self.layout().addWidget(btn_clear)
        
    def handleConsole(self):
        text = str( self.input.text() )
        self.input.setText("")
        trace.mutter(text)
        try:
            result = eval(text)
        except:
            result = "Invalid Expression"
        
        self.history.append(text)
        self.pointer = len(self.history) -1
        
        for i in self.history:
            trace.mutter("\t %s",i)
            
        trace.mutter(self.pointer)
        self.log(result)
    
    def log(self,text):
        if text:
            self.output.append(str(text)+"\n")

    def clearOutput(self):
        self.output.clear()

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Up and self.pointer > 0 :
            trace.mutter("Key UP")
            
            self.input.setText( self.history[self.pointer] )
            self.pointer -= 1
        
        if event.key() == Qt.Key_Down and self.pointer < len(self.history)-1:
            trace.mutter("Key DOWN")
            self.pointer += 1
            self.input.setText( self.history[self.pointer] )
            
        
        QWidget.keyPressEvent(self,event)


if __name__=="__main__":
    import sys
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import QPixmap,QSplashScreen,QApplication
    
    trace.debug_on()
    app = QApplication(sys.argv)
    
    splash = QSplashScreen( QPixmap("splash.png"),Qt.WindowStaysOnTopHint )
    splash.show()
    
    window = GooeyEdit()
    window.load("examples/loader.gef")
    window.show()
    trace.mutter("%s\n" * 9, window.getColData(0),
                             window.getName(0),
                             window.getColFromName(window.getName(2)),
                             window.getColFromName("sdfsd"),
                             '',
                             window.getColData(0),
                             window.getColDataFromName("x"),
                             '',
                             ''
                )
    
    splash.finish(window)
    
    app.exec_()
