

#1. find second largest number
l = [2,4,3,9,10,12,14,2]
lar = sec = l[0]
for i in range(len(l[1:])):
     #tmp = 0
     ii = i+1
     if l[ii] > lar and l[ii] == sec:
         lar = l[ii]
     elif l[ii] < lar and l[ii] > sec:
         sec = l[ii]
     elif l[ii] > lar and l[ii] > sec:
         sec = lar
         lar = l[ii]
     else:
         pass
     

#2. sort the names in list based on second last index
l = ["vijay","pankaj","rahul","viney","mamta"]
sorted(l,key = lambda  s : s[-2] )






#3. sort list of dictonary based on specific key

from operator import itemgetter
d = [{"name":"ram","age":14,"marks":56},{"name":"radha","age":11,"marks":59},{"name":"manish","age":16,"marks":90},{"name":"arun","age":16,"marks":56}]
sorted(d, key=itemgetter('age'))

#OR

sorted(d, key = lambda x : x.get('age'))
