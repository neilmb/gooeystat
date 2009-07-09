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

#from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget,QTableWidget,QTableWidgetItem

from helpers.processable import *
from helpers.templates import *
from helpers.helperwidgets import *

class plugin_5NumSumWidget(DefaultProcessingWidget):
    MENU_LOC="stats:descriptive statistics"
    
    def __init__(self,parent=None):
        DefaultProcessingWidget.__init__(self,["x"],5)

    def getTitle(self):
        return "Five Number Summary"
    
    def isGraphical(self):
        return False
    
    def calcText(self):
        data = self.getData()
        
        mydata = data["x"]["data"]
        
        text = self.getTitle()+"\n\n"

        for i in mydata:
            text+="Column: "+i["name"]+"\n"
            text+=self._formatDict( i["data"].get5NumSum() )
        return text


#class plugin_test(DefaultVarWidget):
#    MENU_LOC="stats:testing"
#    def __init__(self,parent=None):
#        DefaultVarWidget.__init__(self,parent,"Test",1)
#        
#        
#    def run(self,data):
#        text = "Five Num Sum\n"
#        print "data",data
#        for x in data[0]['data']:
#            text+="Column ="+str(x)+"\n"
#            text+=self._formatDict(x.get5NumSum())
#            text+="\n"
#            
#            
#        return text,None
#    
#    
#    
#    
#    
#    
#class plugin_test2(DefaultVarWidget):
#    MENU_LOC="stats:testing"
#    def __init__(self,parent=None):
#        DefaultVarWidget.__init__(self,parent,"Widget",2,4)
#        
#        
#    def run(self,data):
#        return "Done",None
#
#class plugin_test3(DefaultVarWidget):
#    MENU_LOC="stats:testing"
#    def __init__(self,parent=None):
#        DefaultVarWidget.__init__(self,parent,"testing widget",2,4,["x","y"])
#        
#        
#    def run(self,data):
#        return "Done",None


#class stats_FiveNumSumWidget(DefaultOneVarWidget):
#    
#    def __init__(self,parent=None):
#        DefaultOneVarWidget.__init__(self,parent,"Five Number Summary")
#        
#    
#    def run(self,data):
#        dict=data#self.getData()
#        text = ""
#        keys = dict.keys()
#        keys.sort()
#        for key in keys:
#            text+="[Column %s]\n" %str(key)
#            for k,v in dict[key].get5NumSum().items():
#                text+="%s\t%s\n" %(str(k),str(v))
#            text+="\n"
#            
#        
#        return text,None
#
#class stats_StemAndLeafWidget(DefaultOneVarWidget):
#    def __init__(self,parent=None):
#        DefaultOneVarWidget.__init__(self,parent,"Stem and Leaf Summary")
#        
#    def run(self):
#        dict=self.getData()
#        text = ""
#        keys = dict.keys()
#        keys.sort()
#        
#        for k in keys:
#            n=len(str(dict[k][0]))
#            print n
#            stemleaf = {}
#            for item in dict[k]:
#                item = str(item)
#                if stemleaf.has_key(item[:-1]):
#                    stemleaf[item[:-1]].append(item[-1])
#                    stemleaf[item[:-1]].sort()
#                else:
#                    stemleaf[item[:-1]] = [item[-1]]
#            ks=stemleaf.keys()
#            ks.sort()
#            for k in ks:
#                items=stemleaf[k]
#                text +=k+"|"
#                for item in items:
#                    text+=" %s" %str(item)
#                text+="\n"
#            text+="\n"
#        
#        return text,None


#class stats_RegressionWidget(DefaultTwoVarWidget):
#    menu_name = 'Stats:Regression'
#        def __init__(self,parent=None):
#            DefaultTwoVarWidget.__init__(self,parent,"Linear Regression")
#            
#        def run(self):
#            text=""
##            keys = cols.keys()
##            keys.sort()
#            cols = self.getData()
#            xdata = cols["x"]
#            ydata = cols["y"]
#            
##            xdata = cols[ str( int( self.xcol.text() )-1 ) ]
##            ydata = cols[str( int( self.ycol.text() )-1 )]
#            
#            xcols = str(self.xcols.text()).split(",")
#            ycols = str(self.ycols.text()).split(",")
#            
#            xlist = cols['x'][xcols[0]]
#            ylist = cols['y'][ycols[0]]
#            print xlist
#            print ylist
#            cc = r(Processable(xlist),Processable(ylist))
#            text+="r = %0.2f" %cc
#            text+="\nr**2 = %0.2f" %cc**2
#        
#            x=0
#            x2=0
#            y=0
#            y2=0
#            xy=0
#            for i in range(len(xlist )):
#                x+=xlist[i]
#                y+=ylist[i]
#                x2+=xlist[i]**2
#                y2+=ylist[i]**2
#                xy+=xlist[i]*ylist[i]
#            xbar = x/float(len(xlist))
#            ybar = y/float(len(ylist))
#            
#            m = ((xy - (len(xlist) * xbar * ybar))/(x2 - (len(xlist)*xbar**2)))
#            b=(( sum(Processable(ylist).nums) - m*sum(Processable(xlist).nums)) )/float(len(Processable(xlist)))
#            text+="\n"+"y= %0.2fx + %0.2f" %(float(m),float(b))
#            print "\n\n"
#            print wStdDev(xlist,ylist)
#            print "\n\n"
#            return text,None


#class stats_TestingWidget(DefaultOneVarWidget):
#    
#    def __init__(self,parent=None):
#        DefaultOneVarWidget.__init__(self,parent,"Testing Widget")
#        
#    def _format(self, dictionary):
#    for key, val in dictionary.iteritems():
#        print '%s: %s' % (key, val)    
#
#    def run(self,data):
#        dict=data#self.getData()
#        text = ""
#        keys = dict.keys()
#        keys.sort()
#        for key in keys:
#            print key,type(dict[key]),sum(dict[key])
#            text+="Sum: %s" % str(sum(dict[key])) 
#            text+="\n"
#        
#        return text,None


