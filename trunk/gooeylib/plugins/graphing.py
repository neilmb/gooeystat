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

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from helpers.templates import *

#class plugin_TestingWidget(DefaultProcessingWidget):
#    MENU_LOC="stats:descriptive statistics"
#    TYPE=ROWPROCESSING
#    def __init__(self,parent=None):
#        DefaultProcessingWidget.__init__(self,parent,2,2,['x','y'])
#
#    def getTitle(self):
#        return "This is from a different File!"
#    
#    def run(self,data):
#    print data
#        text = "Five Num Sum\n"
#        print "data",data
#        for x in data[0]['data']:
#            text+="Column ="+str(x)+"\n"
#            text+=self._formatDict(x.get5NumSum())
#            text+="\n"
#
#        return text,None



#
#
#class BoxPlot(Graph):
#    
#    def compute_initial_figure(self,lst):
#        if type(lst) == type([]):
#            for l in lst:
#                self.axes.boxplot(l)
#                
#        else: self.axes.boxplot(lst)
#        
#class ScatterPlot(Graph):
#    
#    def compute_initial_figure(self,lsts):
#        self.axes.scatter(lsts[0],lsts[1])
#
#class HistPlot(Graph):
#    
#    def compute_initial_figure(self,lst):
#        import numpy as np
#        import matplotlib.mlab as mlab
#
#        if type(lst) == type([]):
#            for l in lst:
#                n,bins,patches = self.axes.hist(l)
#                
#        else: n,bins,patches = self.axes.hist(lst)
#
#        mu, sigma = 100, 15
#        x = mu + sigma*np.random.randn(10000)
#
#
#        y = mlab.normpdf( bins, mu, sigma)
#        l = self.axes.plot(bins, y, 'r--', linewidth=1)
#        
