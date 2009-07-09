import scipy as sp
import scipy.stats as stats
import numpy as np

def _sample_proportion_sd(n, p):
    return np.sqrt(np.float(p)*(1-p)/n)

print '1a)',
print .08, _sample_proportion_sd(1136, .6)

print '1b)',
print stats.binom.pmf(0,10,.08)

print '1c)',
print 1-stats.binom.pmf([0,1],10,.08).sum()

print '2)',
print 1-1/2.-1/4.-1/8., np.dot([1,2,3,4],[1/2.,1/4.,1/8.,1/8.])

print '3)',
x=stats.norm(280,40)
print x.cdf(300) - x.cdf(275)

print '4)',
print stats.norm.ppf(.25,loc=80,scale=6)

print '5)',
print stats.norm.cdf(75, 81.7, 6.9/np.sqrt(8))

print '6b)',
mu = np.dot([175,-5],[1/38.,37/38.])
print mu

print '6c)',
print 1000*mu

print '7)',
x = stats.binom(15,.7)
print x.pmf(10), x.pmf([11, 12, 13, 14, 15]).sum()

print '8)',
z = stats.norm()
print '(%g, %g), (%g, %g)' % (z.ppf(.025), z.ppf(.975),
                              z.ppf(.05), z.ppf(.95))

print '9a)',
x = stats.norm(25,.07)
print x.cdf(24.9)
print '9b)',
print 2*x.cdf(24.85)

print '10a)',
x = stats.norm(4.35,.59)
print x.sf(5)
print '10b)',
print x.cdf(4) - x.cdf(3)

print '11)',
x = stats.binom(16,1/12.)
print 1 - x.pmf(0) - x.pmf(1)

print '12)',
print 1-(.124+.248+.496+.066), np.dot([1,2,3,4,5],[.124,.248,.496, .066,.066])

print '13)',
print stats.norm.sf(.18, .15, _sample_proportion_sd(120,.15))

print '14)',
print stats.norm.cdf(25/500., .06, _sample_proportion_sd(500, .06))
