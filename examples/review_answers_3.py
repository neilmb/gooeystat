import numpy as np
import scipy.stats as stats

def t_interval(x, confidence_level=0.95):
    xbar = x.mean()
    s = x.std(ddof=1)
    n = len(x)
    return t_interval_summary(xbar, s, n, confidence_level)

def t_interval_summary(xbar, s, n, confidence_level=0.95):
    alpha = 1 - confidence_level
    margin_of_error = stats.t.ppf(1 - alpha/2.,n) * s / np.sqrt(n)
    return (xbar - margin_of_error, xbar + margin_of_error)

def z_interval(x, sigma, confidence_level=0.95):
    xbar = x.mean()
    n = len(x)
    return t_interval_summary(xbar, sigma, n, confidence_level)

def z_interval_summary(xbar, sigma, n, confidence_level=0.95):
    alpha = 1 - confidence_level
    margin_of_error = stats.norm.ppf(1 - alpha/2.) * sigma / np.sqrt(n)
    return (xbar - margin_of_error, xbar + margin_of_error)

print '1) ',
x = np.array([172,168,170,173,172,173,171,175,173,171,169,173])
print '(t0, p) =', stats.ttest_1samp(x,170)

print '2) ',
z0 = (731 - 694)/(212/np.sqrt(40))
print 'p =', stats.norm.sf(z0)

print '3) ',
p1 = 431/1134. 
p2 = 408/1134.
z0 = (p1 - p2)/np.sqrt(p1*(1-p1)/1134 + p2*(1-p2)/1134)
print 'p =', stats.norm.sf(z0)

print '4a) ',
print t_interval_summary(35.1, 8.7, 40, .90)
print '4b) ',
print t_interval_summary(35.1, 8.7, 100, .90)

print '5a) ',
t0 = (38.9 - 40.7)/(9.6/np.sqrt(32))
print 'p =', 2*stats.t.cdf(t0, 31)

print '5b) ',
print t_interval_summary(38.9, 9.6, 32, .95)

print '6a) ',
x1 = np.array([.582,.481,.841,.267,.685,.450])
x2 = np.array([.408,.407,.542,.402,.456,.533])
print '(t0, p) = ', stats.ttest_rel(x1, x2)

print '6b) ',
print t_interval(x1-x2, .98)
x3=x1-x2
s=x3.std()
xbar=x3.mean()
n=len(x3)
print "SPNCR",t_interval_summary(xbar, s, n, .98)

print '7) ',
print t_interval_summary(1.21, .65, 1120, .90)

print '8) ',
print t_interval_summary(13.36, 0.22, 14, .99)

print '9) ',
print '(t0, p) =', stats.ttest_rel([59.5, 69, 77, 59.5, 74.5, 63, 61.5, 67.5, 73, 69],
                      [62, 65.5, 76, 63, 74, 66, 61, 69, 70, 71])

print '10) ',
print t_interval_summary(54, 8, 40, .95)

print '11) ',
print z_interval_summary(93.43, 15, 57, .90)

print '12a) ',
z0 = (191/500. - .394)/np.sqrt(.394*(1-.394)/500)
print 'p =', stats.norm.cdf(z0)
print '12b) ',
margin_of_error = stats.norm.ppf(.95)*np.sqrt(191/500.*(1-191/500.)/500)
print (191/500. - margin_of_error, 191/500. + margin_of_error)

print '13) ',
t0 = (326 - 300)/(342/np.sqrt(404))
print 'p =', stats.t.sf(t0, 403)

print '14) ',
t, p = stats.ttest_ind([118, 126, 126, 120, 129],
                       [124, 98, 110, 140, 110])
print 'p =', p/2.

print '15) ',
print t_interval_summary(114.9, 9.3, 27, .95)

