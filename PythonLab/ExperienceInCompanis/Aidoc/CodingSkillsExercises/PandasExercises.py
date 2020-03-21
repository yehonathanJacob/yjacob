__author__ = "Yehonathan Jacob"
__version__ = "0"
__date__ = "05/03/2020"
__email__ = "YehonathanJ@aidoc.com"

# https://www.machinelearningplus.com/python/101-pandas-exercises-python/

import numpy as np
import pandas as pd


# Q3
mylist = list('abcedfghijklmnopqrstuvwxyz')
myarr = np.arange(26)
mydict = dict(zip(mylist, myarr))
ser = pd.Series(mydict)

# Q4
ser1 = pd.Series(list('abcedfghijklmnopqrstuvwxyz'))
ser2 = pd.Series(np.arange(26))
df = pd.concat([ser1, ser2], axis=1)
# or
df = pd.DataFrame({'col1': ser1, 'col2': ser2})

# Q8
ser = pd.Series(np.random.normal(10, 5, 25))
np.percentile(ser, q=[0, 25, 50, 75, 100])

# Q12
ser = pd.Series(np.random.randint(1, 10, 35))
df = pd.DataFrame(ser.values.reshape(7,5))

# Q13
ser = pd.Series(np.random.randint(1, 10, 7))
np.argwhere(ser % 3==0)

# Q14
ser1 = pd.Series(range(5))
ser2 = pd.Series(list('abcde'))
# Vertical
ser1.append(ser2)
# Horizontal
df = pd.concat([ser1, ser2], axis=1)

# Q18
ser = pd.Series(['how', 'to', 'kick', 'ass?'])
ser.map(lambda x: x[0].upper() + x[1:])

# Q21
from dateutil.parser import parse
ser = pd.Series(['01 Jan 2010', '02-02-2011', '20120303', '2013/04/04', '2014-05-05', '2015-06-06T12:20'])
ser.map(lambda x: parse(x))

# Q23
ser = pd.Series(['Jan 2010', 'Feb 2011', 'Mar 2012'])
ser_ts = ser.map(lambda x: parse(x))
ser_datestr = ser_ts.dt.year.astype('str') + '-' + ser_ts.dt.month.astype('str') + '-' + '04'
[parse(i).strftime('%Y-%m-%d') for i in ser_datestr]

# Q25
import re
emails = pd.Series(['buying books at amazom.com', 'rameses@egypt.com', 'matt@t.co', 'narendra@modi.com'])
pattern ='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,4}'
mask = emails.map(lambda x: bool(re.match(pattern, x)))
emails[mask]

# Q27
p = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
q = pd.Series([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
sum((p - q)**2)**.5


# Q27
ser = pd.Series([2, 10, 3, 4, 9, 10, 2, 7, 3])
[i for i in range(1,len(ser)-1,1) if ser[i]>max(ser[i-1],ser[i+1])]
# answer:
dd = np.diff(np.sign(np.diff(ser)))
peak_locs = np.where(dd == -2)[0] + 1
peak_locs

# Q30
ser = pd.Series(np.random.randint(1,10,10), pd.date_range('2000-01-01', periods=10, freq='W-SAT'))