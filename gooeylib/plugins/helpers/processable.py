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


import math
from scipy.stats import *
from gooeylib import trace


def wAverage(m=None,f=None):
    s=0
    for i in range(len(f)):
        s+=f[i]*m[i]
    n=len(f)
    return s/float(sum(f))


def wStdDev(m,f):
    sfi = sum(f)
    xbar = wAverage(m,f)
    s = 0
    for i in range(len(m)):
        tmp = ((m[i]-xbar)**2) * f[i]
        s+=tmp
    return math.sqrt((s/float(sfi-1)))


class DummyProcessable(object):
    def __init__(self):
        self.mean = 0
        self.std = 1
        
    def setMean(self,mean):
        self.mean = mean

    def setStd(self,std):
        self.std = std
        
    def mean(self):
        return std

    def std(self):
        return std


class Processable(object):
    
    def __init__(self,nums=[]):
        if type(nums) == type(self):
            self.nums=nums.nums
        else:
            self.nums = nums

    def add(self,num):
        if type(num)==type([]):
            for i in num:
                self.nums.append(eval(i))
        elif type(num) == type(9999) or type(num) == type(3.14159):
            self.nums.append(num)
        else:
            self.nums.append( eval(num) )

    def iterate(self):
        for num in self.nums:
            yield num

    def mean(self):
        x = 0
        for i in self.nums:
            x+=i
        return x/float(len(self.nums))

    def median(self):
        self.nums.sort()
        if self.size() % 2 == 0:
            #even
#            print self[self.size()/2-1],self[self.size()/2]
            return sum( [ self[self.size()/2-1] , self[self.size()/2] ] )/2.0
        else:
            #odd
            return self[self.size()/2]

    def calcSampleVariance(self):
        temp = 0
        for i in self.nums:
            temp+=(i-self.mean())**2

        return temp/(len(self.nums)-1.)
        
    def std(self):
        return self.standardDeviation()

    def standardDeviation(self):
        return math.sqrt(self.calcSampleVariance())        
    
    def size(self):
        return len(self.nums)

    def get(self,i):
        return self.nums[i]

    def __iter__(self):
        for i in self.nums:
            yield i

    def __repr__(self):
        return str(self.nums)
    
    def __getitem__(self,i):
        return self.nums[i]
    
    def __len__(self):
        return len(self.nums)
    
    def __sub__(self,other):
        p = Processable([])
        for i in range(self.size()):
            p.add( self[i]-other[i])
        return p

    def getP(self,p):
        i=int(p*(self.size()+1))
        trace.mutter("IN PROC %s", type(self.nums))
        self.nums.sort()
        return (self.nums[i-1]+self.nums[i+1-1])/2.0 #adjusted
    
    def getQ1(self):
        p=.25
        return self.getP(p)

    def getQ3(self):
        p=.75
        return self.getP(p)

    def getOutliers(self):
        pass

    def getMin(self):
        return min(self.nums)

    def getMax(self):
        return max(self.nums)
    
    def get5NumSum(self):
        return {"min":self.getMin() ,
            "q1":self.getQ1(),
            "median":self.median(),
            "q3":self.getQ3(),
            "max":self.getMax(),
            "mean":self.mean(),
            "StdDev":self.standardDeviation()
            }


#if __name__=="__main__":
#    p=Processable([1,2,3,4])
#    p2=Processable([34,5,6,7])
#    
#    print p
#    print p2
#print dir(Stat([1,2,3]))


def zScore(x,xbar,s):
    return (x-xbar)/float(s)


#def m(x,y):
#    
#    if len(x)!= len(y): return None
#    stddevx = x.standardDeviation()
#    stddevy = y.standardDeviation()
#    xbar = x.mean()
#    print "xbar",xbar
#    ybar = y.mean()
#    print "ybar",ybar
#    n=len(x)
#    x2,y2,xy=0,0,0
#    zx=0
#    zy=0
#    for i in range(len(x)):
#        x2+=x[i]**2
#        y2+=y[i]**2
#        xy+=x[i]*y[i]
#        zx+=zScore(x[i],xbar,stddevx)
#        zy+=zScore(y[i],ybar,stddevy)
#    
#    
#    
#    return (zx*zy)/float(n-1)

#x=Stat([579,509,527,516,592,503,511,517,538])
#y=Stat([594,513,566,588,584,510,535,514,582])


def r(x,y):
    
    if len(x)!= len(y): return None
    stddevx = x.std()
    print "stddevx",stddevx
    stddevy = y.std()
    print "stddevy",stddevy
    xbar = x.mean()
    print "xbar",xbar
    ybar = y.mean()
    print "ybar",ybar
    n=len(x)
#    x2,y2,xy=0,0,0
    zx=0
    zy=0
    
    for i in range(len(x)):
        
        print "zx %f\ttotal %f" %(zScore(x[i],xbar,stddevx),zx)
#        x2+=x[i]**2
#        y2+=y[i]**2
#        xy+=x[i]*y[i]
        
        zx+=zScore(x[i],xbar,stddevx)*zScore(y[i],ybar,stddevy)
        #zy+=zScore(y[i],ybar,stddevy)
    
    
#    print (zx)*(1/float(n-1))
    return (zx)*(1/float(n-1))


#print r(x,y)
#print "\n"*8    
#def main():
#    stat=Stat([13,14,15,16,17,18])
#    print "Mean",stat.mean()
#    print "Variance",stat.calcSampleVariance()
#    print "Standard Deviation",stat.standardDeviation()
#
#    print "\n\n"
#    stat=Stat([15.47, 15.48, 15.49, 15.51, 15.52, 15.53])
#    print "Mean",stat.mean()
#    print "Variance",stat.calcSampleVariance()
#    print "Standard Deviation",stat.standardDeviation()

#main()


#f=[11,0,5,6,1,2,1,2]
#m=[2.5,8,13,18,23,28,33,38]
#
#f=[31,39,17,6,4,2,1]
#m=[5,15,25,35,45,55,65]
#
#f=[1,308,1519,1626,503,11]
#m=[55,65,75,85,95,105]
#
#m=[100,93,86,85]
#f=[5,10,60,25]
#
#m=[1.3,4.5,3.75]
#f=[2.5,4,2]

#f=[4,3,2]
#m=[3.5,2.75,2.25]
#m=[1,3,5,7,9,11,13,15]
#f=[2,5,6,8,9,6,3,1]

#  
#print wAverage(m,f)
#print
#print wStdDev(m,f)


def _alpha(ci=.95):
    lower=(1-ci)/2.
    upper=1-lower
    return (lower,upper)


def proportion_interval(x,n,ci=0.95):
    p = x/float(n)
    
    sigma = math.sqrt( p*(1-p)/float(n) )
    
    d=norm(p,sigma)
    
    lower,upper = _alpha(ci)
    
    tup = ( float(d.ppf(lower) ) , float(d.ppf(upper)) )
    return tup


def z_interval(mean,s,n,ci=0.95):
    '''
        calculates the z interval of given data
    '''
    d = norm(mean, s/math.sqrt(n))
    
    lower,upper = _alpha(ci)
    
    s = (s/math.sqrt(n))
    #print "%s +- %s * %s" %(str(mean), str(abs(d.ppf(lower))) , str(s) )
    
    tup = ( float(d.ppf(lower)) , float(d.ppf(upper)) )
    
    return tup


def t_interval(mean,s,n,ci=0.95):
    '''
        calculates the t interval of given data
    '''
    d = t(n-1)
    
    lower,upper = _alpha(ci)

    se = (s/math.sqrt(n))
    #print "%s +- %s * %s" %(str(mean), str(abs(d.ppf(lower))) , str(s) )
    tup = ( float(mean + d.ppf(lower)*se), float(mean + d.ppf(upper)*se) )
    
    return tup


#def norm_ht(xbar,mean,s,n,which):
#    '''
#        performs a hypothesis test
#    '''
#    d=norm(mean,s/math.sqrt(n))
#    
#    if which==">":
#        p=d.sf(xbar) #neat
#    elif which =="<":
#        p= d.cdf(xbar)#1-sf
#    else:
#        p= d.cdf(xbar)*2
#    return p


def one_samp_t_test(mean,s,n,hmean,alt=">"):
    t0 = (mean-float(hmean)) / (s/math.sqrt(n))
    d=t(n-1)
    if alt==">":
        p = d.sf(t0)
    elif alt=="<":
        p=d.cdf(t0)
    else:#"!="
        p=d.cdf( - abs(t0) ) * 2
        
    return p


    
def one_samp_z_test(mean,sigma,n,hmean,alt=">"):
    z0 = (mean-float(hmean)) / (sigma/math.sqrt(n))
    d=norm
    if alt==">":
        p = d.sf(z0)
    elif alt=="<":
        p=d.cdf(z0)
    else:#"!="
        p=d.cdf( - abs(z0) ) * 2
        
    return p


def one_prop_z_test(x,n,p,alt=">"):
    p0= x/float(n)
    z0= (p0-p) / math.sqrt(p*(1-p)/n)
    
    d=norm
    if alt==">":
        p = d.sf(z0)
    elif alt=="<":
        p=d.cdf(z0)
    else:#"!="
        p=d.cdf( - abs(z0) ) * 2
        
    return float(p)
    

def two_prop_z_test(x1,n1,x2,n2,alt=">"):
    '''
        x1-x2
        x1 is _____ then x2
    '''
    p1=x1/float(n1)
    p2=x2/float(n2)
    
    z0 = (p1 - p2)/math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    d=norm
    if alt==">":
        p = d.sf(z0)
    elif alt=="<":
        p=d.cdf(z0)
    else:#"!="
        p=d.cdf( - abs(z0) ) * 2
        
    return float(p)


def paired_t_test(x1,x2):
    '''
        returns the p value for a paired t test
    '''
    return ttest_rel( x1, x2 )[-1]


def two_samp_t_test(x1,x2,alt=">"):
    p0 = stats.ttest_ind(x1,x2)[-1]
    if alt==">" or alt=="<":
        p=p0/2.
    else:#"!="
        p=p0
    return float(p)
    
    
def chisquared_1var(observed):
    expected = [ sum(observed) * 1./len(observed) ]*len(observed)
    
    return chisquared_2var(observed, expected)


def chisquared_2var(observed,expected):
    sum = 0
    for i in range( len(observed) ):
        sum += ((observed[i] - expected[i])**2)/float(expected[i])
    return sum


if __name__=="__main__":
    print z_interval(0, 1, 10, .90)
    print
    print  "Should be (43.042,55.14) :",t_interval(49.09, 13.8, 16, .90)
    print
    print "Should be (1.6,8.40) :",t_interval(5, math.sqrt(7.5), 5, .95)
    print
    print 
    print "Should be (66.48,113.52) :",z_interval(90, 36, 9, .95)
    print
    print z_interval(101.82, 1.2, 6, .95)
    print
    print "\n\n\n"
    #print "Example #4:",norm_ci(35.1,  40, 90)
    
    x=Processable([172,168,170,173,172,173,171,175,173,171,169,173])
    print "Review #1:", one_samp_t_test(x.mean(), x.standardDeviation(), len(x), 170, "!=")
    print
    print "Review #2:", one_samp_z_test(731,212,40,694,">")
    print
    print "Review #3:", two_prop_z_test( 408, 1134,431, 1134, "<")
    print
    print "Review #4a:", t_interval(35.1, 8.7, 40, .90)
    print "Review #4b:", t_interval(35.1, 8.7, 100, .90)
    print
    print "Review #5a:", one_samp_t_test(38.9, 9.6, 32, 40.7, "!=")
    print "Review #5b:", t_interval(38.9, 9.6, 32, .95)
    print
    x1 = Processable([.582,.481,.841,.267,.685,.450])
    x2 = Processable([.408,.407,.542,.402,.456,.533])
    xdiff = x1-x2
    print xdiff.mean(),xdiff.std(),len(xdiff)
    print "Review #6a:",paired_t_test(x1, x2)
    print "Review #6b:", t_interval(xdiff.mean(), xdiff.std(), len(xdiff), .98)
    print
    print "Review #7:", t_interval(1.21, .65, 1120, .9)
    print
    print "Review #8:", t_interval(13.36,.22,14,.99)
    print
    x1 = Processable([59.5, 69, 77, 59.5, 74.5, 63, 61.5, 67.5, 73, 69])
    x2 = Processable([62, 65.5, 76, 63, 74, 66, 61, 69, 70, 71])
    print "Review #9:", paired_t_test(x1, x2)
    print
    print "Review #10:", t_interval(54,8,40,.95)
    print
    print "Review #11:", z_interval(93.43,15,57,.90)
    print
    print "Review #12b:", one_prop_z_test(191, 500, .394, "<")
    print "Review #12b:", proportion_interval(191, 500, .90)
    print
    print "Review #13:", one_samp_t_test(326, 342, 404, 300, ">")
    print
    x1 = Processable([118, 126, 126, 120, 129])
    x2 = Processable([124, 98, 110, 140, 110])
    print "Review #14:", two_samp_t_test(x1, x2, "<")
    print
    print "Review #15:", t_interval(114.9,9.3,27,.95)
    
    print
    print
    o = Processable( [4,9,12,4])
    e = Processable( [7.25]*4 )
    
    print "Should be 5.827:",chisquared_1var(o)
    print "Should be 5.827:",chisquared_2var(o, e)
    
    
    print
    print
    print chisquared_2var([233,237,30],[237,237,26])
    print
    print r(Processable([.15,.35,.1,1.25,1.75,2]),Processable([.15,.35,1.,1.35,1.5,2]))
