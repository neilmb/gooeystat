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


class plugin_chisquared_distribution(DefaultTestWidget):
    MENU_LOC="calculate:probability distributions"
    
    def __init__(self,parent=None):
        
        self.dp = DefaultChoicePicker()
        
        self.dp.addOption("Probability Density","Calculates the probability density of a chi-squared distribution")
        self.dp.addOption("Cumulative Probability","Calculates the cumulative probability of a chi-squared distribution")
        self.dp.addOption("Inverse Cumulative Probability","Calculates 1- cumulative probability of a chi-squared distribution")

        inputs = [
                    GInputInteger("Degrees of Freedom","Enter the degrees of freedom (n-1)"),
                    GInputFloat("Value","Enter the value")
                ]

        self.dp.addInputs("Inputs","These are mandatory inputs", inputs)
        
        DefaultTestWidget.__init__(self, self.dp)
        
    def isGraphical(self):
        return False
    
    def getTitle(self):
        return "Chi Squared"
    
    def calcText(self):
        text = ""
        
        n = self.dp["Degrees of Freedom"]
        value = self.dp["Value"]
        d=chi2(n-1)
        
        if self.dp["Probability Density"]:
            text+="chi-squared Cumulative Probability\n"
            text+="n: %s\nvalue: %s\n" %( str(n),str(value) )
            
            result = d.ppf(value)
            text+="\nprob density: %s" % str(result)

        elif self.dp["Cumulative Probability"]:
            text+="chi-squared Cumulative Probability\n"
            text+="n: %s\nvalue: %s\n" %( str(n),str(value) )
            
            result = d.cdf(value)
            text+="\ncdf: %s" % str(result)
            
        else:
            text+="chi-squared Inverse Cumulative Probability\n"
            text+="n: %s\nvalue: %s\n" %( str(n),str(value) )
            
            result = d.sf(value)
            text+="\n1-cdf: %s" % str(result)
            
        return text

"""
class plugin_normal_onesampztest(DefaultTestWidget):
    MENU_LOC="calculate:distributions:normal"
    
    def __init__(self,parent=None):
        
        self.dp = DefaultChoicePicker()
        option1Inputs = [    GInputString("Sample","Enter the column name of the sample you want")     ]
        option2Inputs = [    GInputFloat("Sample Size","Enter the Sample Size"),
                            GInputFloat("Mean","Enter the Mean")]
    
        self.dp.addOption("Sample Data","Enter the sample data columns", option1Inputs)
        self.dp.addOption("Summerized Data","Enter the summerized data",option2Inputs)
        
        inputs = [    GInputInteger("Standard Deviation","Enter the population standard deviation (sigma)"),
                    GInputFloat("Confidence Level","Enter the confidence level as a fraction",.95),
                    ]

        self.dp.addInputs("Inputs","These are mandatory inputs", inputs)
    
    
        hypothInputs = [    GInputFloat("Hypothesized Mean","Enter the hypothesized mean"),
                            GComboBox("Alternative","Select an alternative hypothesis", ["> greater than", "!= not equal to","< less than"])
                            ]
        
        self.dp.addOptional("Hypothesis Test","Click to perform a hypothesis test",hypothInputs)
                
        DefaultTestWidget.__init__(self, self.dp)
    
    def getTitle(self):
        return "1 Sample Z Test"
    
    def calcText(self):
        text = self.getTitle()+"\n"
        dp = self.dp
        dict = {}
        
        
        if dp["Summerized Data"]:
            mean = dp["Mean"]
            n = dp["Sample Size"]
        else:
            data = self.getProcessable( dp["Sample"] )
            mean = data.mean()
            n = len(data)
            
        sigma = dp["Standard Deviation"]
        ci=dp["Confidence Interval"]
        
        interval = z_interval(mean,sigma,n,ci=0.95)
        dict["interval"] = interval
        
        if dp["Hypothesis Test"]:
            hmean= dp["Hypothesized Mean"]
            alt = dp["Alternative"][0]
            p = one_samp_z_test(mean,sigma,n,hmean,alt)
            dict["p"] = p

        return text +self._formatDict(dict)
"""
