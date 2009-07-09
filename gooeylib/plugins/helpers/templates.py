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


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from processable import Processable
from helperwidgets import *
from string import capwords


class DoingWidget(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        
        self.setupWidget()
        
    def _formatDict(self,data):
        text = ""
        text+="-"*15+"\n"
        for key,value in data.iteritems():
            if type(value) == type(1.1): #float
                value = round(value,4)
            elif type(value) == type( () ):#tuple
                try:
                    value = ( round(value[0],4), round(value[0],4) )
                except:
                    pass
            text+="%s\t%s\n" %(str(key),str(value))
            
        text+="-"*15+"\n"
        return text
    
    def setupWidget(self):
        self.setWindowTitle(self.getTitle())
        self.setLayout(QVBoxLayout())
        
        grp_mainwidget = QWidget()#QGroupBox(self.getTitle())
        grp_mainwidget.setLayout(QVBoxLayout())
        self.layout().addWidget(grp_mainwidget)
        
        self.row1 = QWidget(self)
        self.row1.setLayout( QHBoxLayout() )
        
        self.nonEmptyCols = QListWidget(self)
        self.nonEmptyCols.setFixedWidth(150)
        
        self.connect(self.nonEmptyCols,SIGNAL("itemDoubleClicked(QListWidgetItem*)"),self.addCol)
        
        grp_cols = QGroupBox("Columns:")
        grp_cols.setLayout(QVBoxLayout())
        grp_cols.layout().addWidget(self.nonEmptyCols)
        
        self.row1.layout().addWidget( grp_cols )
        
        grp_mainwidget.layout().addWidget( self.row1 )        
        
        grp_options=QGroupBox("Options:")
        grp_options.setLayout(QHBoxLayout())
        
        
        self.cb_text = QCheckBox("Text Output")
        self.cb_text.setChecked(True)
        self.cb_graph = QCheckBox("Graphical Output")
        if self.isTextual(): self.cb_graph.setDisabled(True)
        
        grp_options.layout().addWidget(self.cb_text)
        grp_options.layout().addWidget(self.cb_graph)
        
        self.layout().addWidget(grp_options)
        
        defaultButtons = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )
        
        self.connect(defaultButtons,SIGNAL("accepted()"),self.validate)
        self.connect(defaultButtons,SIGNAL("rejected()"),self.reject)
        
        self.layout().addWidget(defaultButtons)
    
    def setGooeyEdit(self,ge):
        self.gooeyedit = ge
        self.setNonEmptyCols()
        
    def getGooeyEdit(self):
        return self.gooeyedit
    
    def setNonEmptyCols(self):
        self.nonEmptyCols.clear()
        for col in self.getGooeyEdit().getNonEmpty():
            self.nonEmptyCols.addItem( QListWidgetItem("%s [%s]" %(str(col+1),str(self.getGooeyEdit().getName(col)))  ) )
        
    def getProcessable(self,colname):
        return self.gooeyedit.getColDataFromName(colname)
    
    def getData(self):
        vars = {}

        for varname,l in self.getCols().iteritems():
            trace.mutter("varname %s %s",varname,l)
            var={}
            var["name"] = varname
            var["data"] = []
            
            for name in l:
                trace.mutter("NAME: %s %s",name,type(name))
                data={}
                data["col"]=self.gooeyedit.getColFromName(name)
                data["name"]=name
                data["data"] = Processable( self.gooeyedit.getColData( int(data["col"]) ) ) 
                
                var["data"].append(data)
    
            vars[varname]=var
        """print
        for key,value in vars.iteritems():
            print key
            for k,v in value.iteritems():
                print "\t",k,v
                if k=="data":
                    for data in v:
                        print "\t\t",data
        print"""
        return vars
    
    def setPluginWidget(self,pluginw):
        self.row1.layout().addWidget(pluginw)
        
    def validate(self):
        if not self.validateMe():
            pass
#            self.reject()
        else:
            QDialog.accept(self)
    
    def pluginIsTextual(self):
        return self.cb_text.isChecked()
    
    def pluginIsGraphical(self):
        return self.cb_graph.isChecked()
    
    def __repr__(self):
        return "[plugin: %s]" %( self.getTitle() )
    
    def addCol(self,item):
        raise NotImplementedError
    
    def getCols(self):
        '''
            must return a dictionary of var names and column indexes with of data to get
                ex: { "x": [0,2], "y": [2,3] }
        '''
        raise NotImplementedError
    
    def getTitle(self):
        '''
            must return the title of the widget
        '''
        raise NotImplementedError
    
    def calcText(self):
        '''
            calculates the textual part of the plugin
        '''
        raise NotImplementedError
    
    def calcGraph(self):
        '''
            calculates the graphical part of the plugin
        '''
        raise NotImplementedError
    
    def run(self):
        '''
            starts the execution of the plugin and called
            when validation of inputs is complete.
        '''
        raise NotImplementedError


class DefaultProcessingWidget(DoingWidget):
    
    def __init__(self,headers=["Var 1"],rows=5):
        DoingWidget.__init__(self)

        layout = QVBoxLayout()
        groupBox = QGroupBox("Choices")
        groupBox.setLayout(layout)

        self.cols = QTableWidget(rows,len(headers),self)
        for y in range(self.cols.rowCount()):
            for x in range(self.cols.columnCount()):
                self.cols.setItem(y,x,QTableWidgetItem(""))

        self.cols.setHorizontalHeaderLabels(headers)
        layout.addWidget(self.cols)

        self.setPluginWidget(groupBox)

    def addCol(self,col):
        for y in range(self.cols.rowCount()):
            for x in range(self.cols.columnCount()):
                if self.cols.item(y,x).text()=="":
                    self.cols.setItem(y,x,QTableWidgetItem( str(col.text()).split()[1][1:-1] ) )
                    return
    
    def validateMe(self):
        goods=[]
        for y in range(self.cols.rowCount()):
            good = []
            for x in range(self.cols.columnCount()):
                trace.mutter("%s %s %s",x,y,self.cols.item(y,x).text())
                if self.cols.item(y,x).text() !="":
                    good.append(True)
                else:
                    good.append(False)

            goods.append( good.count(False) == self.cols.columnCount() or good.count(True) == self.cols.columnCount())
        trace.mutter("Validation: %s",goods)
        return not goods.count(False)>0

    def getCols(self):
        cols = {}
        for x in range( self.cols.columnCount() ):
            name=str( self.cols.horizontalHeaderItem(x).text() )
            cols[ name ]= []
            for y in range( self.cols.rowCount() ):
                if str(self.cols.item(y,x).text()) !="":
                    cols[name].append( str( self.cols.item(y,x).text() ) )  
                
        return cols

    def isTextual(self):
        return True
    def isGraphical(self):
        return True
    
    def run(self):
        text,graph = "Nothing to do...",None
        if self.isTextual() and self.pluginIsTextual():
            text=self.calcText()
            
        if self.isGraphical() and self.pluginIsGraphical():
            graph=self.calcGraph()
            
        return text,graph


class DefaultTestWidget(DoingWidget):
    
    
    def __init__(self,dp ):
        
        DoingWidget.__init__(self)

        self.dp = dp
        
        dataInputs = QGroupBox("Input Options:")
        self.mylayout = QGridLayout()
        dataInputs.setLayout( self.mylayout )
        
        self.dp.place(self.mylayout)
        
        self.setPluginWidget(dataInputs)


    def addCol(self,col):
        
        col = str(col.text()).split()[-1][1:-1]
        
        self.dp.addCol(col)

    def validateMe(self):
        return self.dp.validate()

    def isTextual(self):
        return True
    def isGraphical(self):
        return True
    
    
    
    def run(self):
        text,graph = "Nothing to do...",None
        if self.isTextual() and self.pluginIsTextual():
            text=self.calcText()
            
        if self.isGraphical() and self.pluginIsGraphical():
            graph=self.calcGraph()
            
        return text,graph
        
  
#class Graph(FigureCanvas):
#    
#    def __init__(self, what=None, parent=None, width=5, height=4, dpi=100):
#        fig = Figure(figsize=(width,height), dpi=dpi)
#        self.axes = fig.add_subplot(111)
#        self.axes.hold(False)
#        
#        self.compute_initial_figure(what)
#
#        FigureCanvas.__init__(self,fig)
#        self.setParent(parent)
#
#        FigureCanvas.setSizePolicy(self,
#                                   QSizePolicy.Expanding,
#                                   QSizePolicy.Expanding)
#        FigureCanvas.updateGeometry(self)
#
#    def compute_initial_figure(self,what=None):
#        '''
#        must add things to self.axes like self.axes.boxplot()
#        '''
#        pass
        
        
        
        
