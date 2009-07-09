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


class plugin_t_distribution(DefaultTestWidget):
    MENU_LOC="calculate:probability distributions"
    
    def __init__(self,parent=None):
        
        self.dp = DefaultChoicePicker()
        
        self.dp.addOption("Probability Density","Calculates the probability density of a t distribution")
        self.dp.addOption("Cumulative Probability","Calculates the cumulative probability of a t distribution")
        self.dp.addOption("Inverse Cumulative Probability","Calculates 1- cumulative probability of a t distribution")

        inputs = [
                    GInputInteger("Degrees of Freedom","Enter the degrees of freedom (n-1)"),
                    GInputFloat("Value","Enter the value")
                ]

        self.dp.addInputs("Inputs","These are mandatory inputs", inputs)
        
        DefaultTestWidget.__init__(self, self.dp)
        
    def isGraphical(self):
        return False
    
    def getTitle(self):
        return "t"
    
    def calcText(self):
        text = ""
        
        n = self.dp["Degrees of Freedom"]
        value = self.dp["Value"]
        d=chi2(n-1)
        
        if self.dp["Probability Density"]:
            text+="t Cumulative Probability\n"
            text+="n: %s\nvalue: %s\n" %( str(n),str(value) )
            
            result = d.ppf(value)
            text+="\nprob density: %s" % str(result)

        elif self.dp["Cumulative Probability"]:
            text+="t Cumulative Probability\n"
            text+="n: %s\nvalue: %s\n" %( str(n),str(value) )
            
            result = d.cdf(value)
            text+="\ncdf: %s" % str(result)
            
        else:
            text+="t Inverse Cumulative Probability\n"
            text+="n: %s\nvalue: %s\n" %( str(n),str(value) )
            
            result = d.sf(value)
            text+="\n1-cdf: %s" % str(result)
            
        return text
