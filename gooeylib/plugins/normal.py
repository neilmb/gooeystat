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


class plugin_normal_distribution(DefaultTestWidget):
    MENU_LOC="calculate:probability distributions"
    
    def __init__(self,parent=None):
        
        self.dp = DefaultChoicePicker()
        
        self.dp.addOption("Probability Density","Calculates the probability density of a normal distribution")
        self.dp.addOption("Cumulative Probability","Calculates the cumulative probability of a normal distribution")
        self.dp.addOption("Inverse Cumulative Probability","Calculates 1- cumulative probability of a normal distribution")

        inputs = [
                    GInputFloat("Mean","Enter the sample mean",0),
                    GInputFloat("Standard Deviation","Enter the sample standard deviation",1),
                    GInputFloat("Value","Enter the value")
                ]

        self.dp.addInputs("Inputs","These are mandatory inputs", inputs)
        
        DefaultTestWidget.__init__(self, self.dp)
        
    def isGraphical(self):
        return False
    
    def getTitle(self):
        return "Normal"
    
    def calcText(self):
        text = ""
        
        mean = self.dp["Mean"]
        std = self.dp["Standard Deviation"]
        value = self.dp["Value"]
        d=norm(mean,std)
        
        if self.dp["Probability Density"]:
            text+="Normal Cumulative Probability\n"
            text+="mean: %s\nstd dev: %s\nvalue: %s\n" %( str(mean),str(std),str(value) )
            
            result = d.ppf(value)
            text+="\nprob density: %s" % str(result)

        elif self.dp["Cumulative Probability"]:
            text+="Normal Cumulative Probability\n"
            text+="mean: %s\nstd dev: %s\nvalue: %s\n" %( str(mean),str(std),str(value) )
            
            result = d.cdf(value)
            text+="\ncdf: %s" % str(result)
            
        else:
            text+="Normal Inverse Cumulative Probability\n"
            text+="mean: %s\nstd dev: %s\nvalue: %s\n" %( str(mean),str(std),str(value) )
            
            result = d.sf(value)
            text+="\n1-cdf: %s" % str(result)
            
        return text

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
    
    
class plugin_normal_onesampttest(DefaultTestWidget):
    MENU_LOC="calculate:distributions:normal"
    
    def __init__(self,parent=None):
        
        self.dp = DefaultChoicePicker()
        option1Inputs = [    GInputString("Sample","Enter the column name of the sample you want")     ]
        option2Inputs = [    GInputFloat("Mean","Enter the Mean"),
                            GInputFloat("Standard Deviation","Enter the Sample Standard Deviation")]
    
        self.dp.addOption("Sample Data","Enter the sample data columns", option1Inputs)
        self.dp.addOption("Summerized Data","Enter the summerized data",option2Inputs)
        
        inputs = [    GInputInteger("Sample Size","Enter the sample size (n)"),
                    GInputFloat("Confidence Level","Enter the confidence level as a fraction",.95),
                    ]

        self.dp.addInputs("Inputs","These are mandatory inputs", inputs)
    
    
        hypothInputs = [    GInputFloat("Hypothesized Mean","Enter the hypothesized mean"),
                            GComboBox("Alternative","Select an alternative hypothesis", ["> greater than", "!= not equal to","< less than"])
                            ]
        
        self.dp.addOptional("Hypothesis Test","Click to perform a hypothesis test",hypothInputs)
                
        DefaultTestWidget.__init__(self, self.dp)
    
    def getTitle(self):
        return "1 Sample t Test"
    
    def calcText(self):
        text = self.getTitle()+"\n"
        dp = self.dp
        dict = {}
        
        
        if dp["Summerized Data"]:
            mean = dp["Mean"]
            std = dp["Standard Deviation"]
        else:
            data = self.getProcessable( dp["Sample"] )
            mean = data.mean()
            std = data.std()
            
        n = dp["Sample Size"]
        ci=dp["Confidence Interval"]
        
        interval = t_interval(mean,std,n,ci=0.95)
        dict["interval"] = interval
        
        if dp["Hypothesis Test"]:
            hmean= dp["Hypothesized Mean"]
            alt = dp["Alternative"][0]
            p = one_samp_t_test(mean,std,n,hmean,alt)
            dict["p"] = p

        return text +self._formatDict(dict)


#class plugin_normal_twosampttest(DefaultTestWidget):
#    MENU_LOC="calculate:distributions:normal"
#    
#    def __init__(self,parent=None):
#        
#        self.dp = DefaultChoicePicker()
#        option1Inputs = [    GInputString("Sample 1","Enter the column name of the sample you want"),
#                            GInputString("Sample 1","Enter the column name of the sample you want")    ]
#        option2Inputs = [    GInputFloat("Mean 1","Enter the mean for sample 1"),
#                            GInputFloat("Standard Deviation 1 ","Enter the standard deviation for sample 1"),
#                            GInputFloat("Mean 2","Enter the mean for sample 2"),
#                            GInputFloat("Standard Deviation 2 ","Enter the standard deviation for sample 2")]
#    
#        self.dp.addOption("Sample Data","Enter the sample data columns", option1Inputs)
#        self.dp.addOption("Summerized Data","Enter the summerized data",option2Inputs)
#        
#        inputs = [    GInputInteger("Sample Size","Enter the sample size (n)"),
#                    GInputFloat("Confidence Level","Enter the confidence level as a fraction",.95),
#                    ]
#
#        self.dp.addInputs("Inputs","These are mandatory inputs", inputs)
#    
#    
#        hypothInputs = [    GInputFloat("Hypothesized Mean","Enter the hypothesized mean"),
#                            GComboBox("Alternative","Select an alternative hypothesis", ["> greater than", "!= not equal to","< less than"])
#                            ]
#        
#        self.dp.addOptional("Hypothesis Test","Click to perform a hypothesis test",hypothInputs)
#                
#        DefaultTestWidget.__init__(self, self.dp)
#    
#    def getTitle(self):
#        return "2 Sample t Test"
#    
#    def calcText(self):
#        text = self.getTitle()+"\n"
#        dp = self.dp
#        dict = {}
#        
#        
#        if dp["Summerized Data"]:
#            mean1 = dp["Mean 1"]
#            std1 = dp["Standard Deviation 1"]
#            mean2 = dp["Mean 1"]
#            std2 = dp["Mean 2"]
#        else:
#            data1 = self.getProcessable( dp["Sample 1"] )
#            mean1 = data1.mean()
#            std1 = data1.std()
#            
#            data2 = self.getProcessable( dp["Sample 2"] )
#            mean2 = data2.mean()
#            std2 = data2.std()
#            
#        n = dp["Sample Size"]
#        ci=dp["Confidence Interval"]
#        
#        interval = t_interval(mean,std,n,ci=0.95)
#        dict["interval"] = interval
#        
#        if dp["Hypothesis Test"]:
#            hmean= dp["Hypothesized Mean"]
#            alt = dp["Alternative"][0]
#            p = one_samp_t_test(mean,std,n,hmean,alt)
#            dict["p"] = p
#
#        return text +self._formatDict(dict)
    
    
class plugin_normal_pairedttest(DefaultTestWidget):
    MENU_LOC="calculate:distributions:normal"
    
    def __init__(self,parent=None):
        
        self.dp = DefaultChoicePicker()
        option1Inputs = [    GInputString("Sample 1","Enter the column name of sample 1"),
                            GInputString("Sample 2","Enter the column name of sample 2")     ]
#        option2Inputs = [    GInputFloat("Mean","Enter the Mean"),
#                            GInputFloat("Standard Deviation","Enter the Sample Standard Deviation")]
    
        self.dp.addOption("Sample Data","Enter the sample data columns", option1Inputs)
#        self.dp.addOption("Summerized Data","Enter the summerized data",option2Inputs)
        
        inputs = [    GInputInteger("Sample Size","Enter the sample size (n)"),
                    GInputFloat("Confidence Level","Enter the confidence level as a fraction",.95),
                    ]

#        self.dp.addInputs("Inputs","These are mandatory inputs", inputs)
    
    
#        hypothInputs = [    GInputFloat("Hypothesized Mean","Enter the hypothesized mean"),
#                            GComboBox("Alternative","Select an alternative hypothesis", ["> greater than", "!= not equal to","< less than"])
#                            ]
        
#        self.dp.addOptional("Hypothesis Test","Click to perform a hypothesis test",hypothInputs)
                
        DefaultTestWidget.__init__(self, self.dp)
    
    def getTitle(self):
        return "Paired t Test"
    
    def calcText(self):
        text = self.getTitle()+"\n"
        dp = self.dp
        dict = {}
        
        
        if dp["Summerized Data"]:
            pass
        else:
            x1 = self.getProcessable( dp["Sample 1"] )
            x2 = self.getProcessable( dp["Sample 2"] )
            
        dict["p"] = paired_t_test(x1.nums,x2.nums)
        
#        if dp["Hypothesis Test"]:
#            hmean= dp["Hypothesized Mean"]
#            alt = dp["Alternative"][0]
#            p = one_samp_t_test(mean,std,n,hmean,alt)
#            dict["p"] = p

        return text +self._formatDict(dict)


#class plugin_normal_zscore(DefaultTestWidget):
#    MENU_LOC="calculate:distributions:normal"
#    
#    def __init__(self,parent=None):
#        DefaultTestWidget.__init__(self,optionInputs={ "sample from columns":["sample:Enter the column to use for the sample data:2"],
#                                        "summerized data":[    "sample size:Enter the sample size (n)",
#                                                        "mean:Enter the sample mean (xbar)",
#                                                        "standard dev:Enter the sample standard deviation (sigma)" ]},
#                        
#                        inputHeaders=["value 1"],
#                        optionalHeaders=["value 2"] )
#    
#    def getTitle(self):
#        return "Normal CDF"
#    
#    def calcText(self):
#        text = "1-Sample T Test\n"
#        data = self.getData()
#        return self._formatDict(data)
#
#        return text














