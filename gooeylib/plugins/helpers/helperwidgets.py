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


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gooeylib import trace
import sys
from string import *


class GooeyWidget(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
    
    def place(self,layout,col=1):
        raise NotImplementedError
    
    def text(self):
        raise NotImplementedError
    
    def getData(self):
        raise NotImplementedError
    
    def getLabel(self):
        raise NotImplementedError
    
    def validate(self):
        raise NotImplementedError
    

class DefaultChoicePicker(GooeyWidget):
    def __init__(self):
        GooeyWidget.__init__(self)
        self.mylayout = QGridLayout()
        self.setLayout(self.mylayout)

        self.option = OptionGroup()
        self.inputs = {}
        self.optional = []

    def addOption(self,label,tooltip, inputs=[]):
        tooltip = tooltip if tooltip!="" else label
        self.option.addOption(label,tooltip, inputs)

    def addInputs(self,label,tooltip="", inputs=[]):
        tooltip = tooltip if tooltip!="" else label
        self.label = QLabel(label)
        self.label.setToolTip(tooltip)
        
        self.inputsorder = []
        self.inputs = {}
        for i in inputs:
            
            self.inputs[i.getLabel()] = i
            self.inputsorder.append(i)
        
    
    def addOptional(self,label,tooltip, inputs):
        optional = GCheckBoxGroup(label,tooltip, inputs)
        self.optional.append(optional)
        
    def place(self,layout):
        
        self.option.place(layout)
        
        if self.inputs != {}:
            layout.addWidget( self.label, layout.rowCount(), 0)
            for input in self.inputsorder:
                input.place(layout,1)
        
        for option in self.optional:
            option.place(layout,0)

    def getData(self):
        trace.mutter("\n\ngetting data!\n"+"-"*30)
            
        if self["summerized data"]:
            trace.mutter("summerized data: True")
            trace.mutter("mean: %s", self["mean"])
        else:#sampledata
            trace.mutter("sample data: True")
            trace.mutter("input 1: %s",self["input 1"])
            
        trace.mutter("inputs:")
        for i in ["confidence interval","sample size"]:
            trace.mutter("\t %s %s",i,self[i])
            
        if self["hypoth test"]:
            trace.mutter("hypoth test")
            for i in ["alternative","hypoth mean"]:
                trace.mutter("\t %s %s",i,self[i])
                
    def __getitem__(self,key):
        if self.option[key]:
            return self.option[key]
        
        
        if self.inputs.has_key(key):
            return self.inputs[key].getData()
        
        for option in self.optional:
            if option[key]:
                return option[key]
        
        
        return None
    
    def validate(self):
        goods = []
        
        goods.append( self.option.validate() )
        
        for input in self.inputs.itervalues():
            goods.append(input.validate())
            
        for option in self.optional:
            goods.append(option.validate())
            
        return goods.count( False) == 0


class GInput(GooeyWidget):
    def __init__(self,label,tooltip="",defaultvalue="",parent=None):
        GooeyWidget.__init__(self,parent)
        
        self.label = QLabel( label)
        
        self.input = QLineEdit()
        self.input.setText(str(defaultvalue))
        self.input.selectAll()
        
        self.input.setToolTip(tooltip)
        self.label.setToolTip(tooltip)
    
    def setValidator(self,validator):
        self.input.setValidator(validator)
        
    def setDisabled(self,bool=True):
        self.label.setDisabled(bool)
        self.input.setDisabled(bool)
    
    def text(self):
        return str(self.input.text())
    
    def getLabel(self):
        return str(self.label.text())
    
    def getData(self):
        return  str(self.label.text()) 
        
    def place(self,layout,col=1):
        row = layout.rowCount()
        layout.addWidget(self.label,row,col)
        layout.addWidget(self.input,row,col+1)
        
    def validate(self):
        return len(self.text()) != 0
    
class GInputFloat(GInput):
    def __init__(self,label,tooltip="",defaultvalue=""):
        GInput.__init__(self,label,tooltip,defaultvalue )
        self.setValidator( QDoubleValidator(-9999.0,9999.0,4,self) )
        
    def getData(self):
        return float( str(self.text()) )

class GInputDecimal(GInput):
    def __init__(self,label,tooltip="",defaultvalue=""):
        GInput.__init__(self, label, tooltip  , defaultvalue)
        self.setValidator( QDoubleValidator( 0.0,99.0,4,self) )
    
    def getData(self):
        return float( str( self.text() ) )
        
class GInputInteger(GInput):
    def __init__(self,label,tooltip="",defaultvalue=""):
        GInput.__init__(self, label, tooltip, defaultvalue)
        self.setValidator( QIntValidator( -9999,9999, self) )
        
    def getData(self):
        return int( str( self.text() ) )
    
class GInputString(GInput):
    def __init__(self,label,tooltip="",defaultvalue=""):
        GInput.__init__(self, label, tooltip, defaultvalue)
    
    def getData(self):
        return str(self.text())
    
        
#class TextEdit(GooeyWidget):
#    def __init__(self,label,tooltip=""):    
#        GooeyWidget.__init__(self)
#        tooltip = tooltip if tooltip != "" else label
#        
#        self.label = QLabel( label)
#        self.input = QLineEdit()
#
#        self.label.setToolTip(capwords(label))
#        self.input.setToolTip(tooltip)
#    
#    def place(self,layout,col=1):
#        row = layout.rowCount()
#        layout.addWidget( self.label, row, col )
#        layout.addWidget( self.input, row, col+1 )
#
#    def setDisabled(self,bool=True):
#        for w in [self.label,self.input]:
#            w.setDisabled(bool)    
#
#    
#    def text(self):
#        return self.input().text()
#    def getLabel(self):
#        return str( self.label.text() )
        
        
class OptionGroup(GooeyWidget):
    def __init__(self):
        GooeyWidget.__init__(self)
        
        self.options = {}
        self.optionOrder = []
        
    def __getitem__(self,key):
        
        if self.getChecked().text() == key:
            return True
        
        for input in self.options[self.getChecked()]:
            if input.getLabel() == key:
                return input.getData()
        return None
        
    def disableOptions(self):
        for option,widgets in self.options.iteritems():
            for w in widgets:
                w.setDisabled(True)
                    
        for option in self.options.keys():
            if option.isChecked():
                for w in self.options[option]:
                    w.setDisabled(False)
                break
        
    def addOption(self,label,tooltip="",inputs=[]):

        if type(inputs)==type([]):
            btn = QRadioButton( label) 
            btn.setToolTip(tooltip)
            self.connect( btn, SIGNAL("clicked()"), self.disableOptions)
            self.options[btn] = []
            self.optionOrder.append(btn)
            
            for input in inputs:
                self.options[btn].append(input)
                    
            if len(self.options.keys()) ==1:
                btn.setChecked(True)
            if len(self.options.keys()) >1:
                for w in self.options[btn]:
                    w.setDisabled(True)
                        
    def getChecked(self):
        for btn in self.options.keys():
            if btn.isChecked():
                return btn
            
    def getData(self):
        data = {}

        option = self.getChecked()
        name = str(option.text())
        data[name] = {}
        for w in self.options[ option ]:
            try:
                label = w.getLabel()
                text = w.getText()
            except:
                pass#################################### TODO TODO TODO TODO TODO TODO TODO TODO TODO
             
            data[name][label] = text
            
        return data

    def validate(self):
        goods=[]
        for w in self.options[ self.getChecked() ]:
            goods.append( w.validate() )
        return goods.count( False) == 0

    def place(self,layout,col=0):
        for radiobtn in self.optionOrder:
            inputs = self.options[radiobtn]
            layout.addWidget( radiobtn, layout.rowCount(), col )
            for input in inputs:
#                layout.addWidget( input, layout.rowCount(), col+1)
                input.place(layout,col+1)


class GComboBox(GooeyWidget):
    def __init__(self,label,tooltip="",options=["1"],parent=None):
        GooeyWidget.__init__(self,parent)
        
        tooltip = tooltip if tooltip != "" else label
        
        self.label = QLabel(label)
        self.combobox = QComboBox()
        for option in options:
            self.combobox.addItem(option)
        
    def setDisabled(self,bool=True):
        for w in [self.label,self.combobox]:
            w.setDisabled(bool)
            
    def getLabel(self):
        return str(self.label.text())        
    def text(self):
        return str(self.combobox.currentText())
    
    def place(self,layout,col=1):
        row = layout.rowCount()
        layout.addWidget( self.label , row, col)
        layout.addWidget( self.combobox, row, col+1)
        
    def getData(self):
        return self.text()
        
    def validate(self):
        return self.text() !=""
        

class GCheckBoxGroup(GooeyWidget):
    def __init__(self,label,tooltip="",inputs=[]):
        GooeyWidget.__init__(self)
        tooltip = tooltip if tooltip != "" else label

        self.cb = QCheckBox(label)
        self.connect(self.cb,SIGNAL("clicked()"),self._clicked)
        self.cb.setToolTip(tooltip)

        self.inputs = {}
        for i in inputs:
            self.inputs[i.getLabel()] = i

        self._clicked()
    
    def __getitem__(self,key):
        if self.isChecked() and self.cb.text() == key:
            return True
        
        if self.isChecked():
            
            for label,input in self.inputs.iteritems():
                trace.mutter(input.getLabel(),"|",key)
                if input.getLabel() == key:
                    return input.getData()
            
            
    def _clicked(self):
        bool = self.cb.isChecked()
        self.setDisabled( bool)
    
    def setDisabled(self,bool=True):
        for w in self.inputs.itervalues():
            w.setDisabled(not bool)
        
    def addWidget(self,gwidget):
        self.inputs[gwidget.getLabel()] = widget
        self._clicked()
        
    def isChecked(self):
        return self.cb.isChecked()
    
    def validate(self):
        if self.isChecked():
            goods = []
            for input in self.inputs.itervalues():
                goods.append( input.validate() )
            return goods.count(False) == 0
        
        return True
        
    def getData(self):
        data = {}
        data[ str(self.cb.text()) ] = {}
        if self.isChecked():
            for w in self.inputs:
                data[ str(self.cb.text()) ][w.getLabel()] = w.text()
        trace.mutter(data)
        return data
    
    def text(self):
        return self.getData()
    def getLabel(self):
        return str(self.cb.text())
    
    def place(self,layout,col=1):
        row = layout.rowCount()
        layout.addWidget(self.cb, row,col )
        for i in self.inputs.itervalues():
            i.place(layout,col+1)
    
 
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    window = QWidget()
    layout = QGridLayout()
    window.setLayout(layout)
    
#    t1 = TextEdit("Fisher Price","Enter information about your children",layout,2)
    #layout.addWidget( t1,1,1 )
    
#    t2 = TextEdit("Confidence Interval",None,layout)
    #layout.addWidget( t2 ,2,1)
    
    
    btn2 = QPushButton("Click me!")
#    window.connect( btn2, SIGNAL("clicked()"),cb.getData)
    layout.addWidget(btn2,layout.rowCount(),3)
    
    dp = DefaultChoicePicker()
    
    option1Inputs = [    GInputFloat("input 1","This is an input..."),
                GInputFloat("input 2","This is an input...")]
    option2Inputs = [    GInputFloat("mean","This is an input..."),
                GInputFloat("std dev 2","This is an input...")]
    
    inputs = [    GInputFloat("confidence interval",defaultvalue=.95),
                GInputInteger("sample size","only an integer please")]
    
    dp.addOption("sample data","Enter the sample data...", option1Inputs)
    dp.addOption("summerized data","Enter the summerized data",option2Inputs)
    
    dp.addInputs("inputs","These are mandatory inputs", inputs)

    hypothInputs = [    GInputFloat("hypoth mean","Enter the hypothesized mean"),
                        GComboBox("alternative","select an alternaive hypothesis", ["> greater than","< less than", "!= not equal to"])
                        ]
    dp.addOptional("hypoth test","Click to perform a hypothesis test",hypothInputs)
    dp.place(layout)
    


    btn = QPushButton("Click me!")
    window.connect( btn, SIGNAL("clicked()"),dp.getData)
    layout.addWidget(btn,layout.rowCount(),layout.columnCount()-1)
    


    dp2 = DefaultChoicePicker()
    dp2.addInputs("Pick your data", tooltip, inputs)

    
    window.show()
    app.exec_()
