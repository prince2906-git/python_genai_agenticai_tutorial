"""

How to create numpy arrays?
-- From list
    lst = [10,20,30,40,50]
    arr = np.array(lst)

-- dot function available in numpy library
    np.dot(arr1,arr2)

Performance Comparison between Python List and NumPy Array.
    As per below performance we can see numpy is very past, taking almost 50% less
    time than Python List

Example Prof for Performance between ND array and Python List

import numpy as np
from functools import reduce
from datetime import datetime
import time

lst1 = [10, 20, 30, 40, 50,60]
arr1 = np.array(lst1)
print(type(arr1))  # -- numpy.ndarray

lst2 = [1, 2, 3, 4, 5,6]
arr2 = np.array(lst2)

## Find dot product [Multiply Corresponding Elements]
## Sum of product of array element
## E.g. 10*1+20*2+30*3+40*4+50*5 = 550

## a.b = sigma(i=1,n)[a(i)*b(i)]

## Traditional Python code to find dot product

def dotproduct(lst1,lst2):

    if len(lst1) != len(lst2):
        raise ValueError("List should be of same length for dot product")

    isNumeric = reduce(lambda a,b: a and b,[isinstance(i,int) and isinstance(j,int) for i,j in zip(lst1,lst2)])

    if not isNumeric:
        raise ValueError("List should be numeric only")

    dotp = reduce(lambda x,y:x+y,[i*j for i,j in zip(lst1,lst2)])
    #print("Dot Product : ",dotp)

print("Using Traditional List")
start = datetime.now()
print("Start : ",start)
for i in range(100000000):
    dotproduct(lst1, lst2)
end = datetime.now()
print("End : ",end)
execution_time=end-start
print("Execution time : ",execution_time.total_seconds()," seconds")


## Using Numpy.
print("Using Numpy")
start = datetime.now()
print("Start : ",start)
for i in range(100000000):
    np.dot(arr1,arr2)
end = datetime.now()
print("End : ",end)
execution_time=end-start
print("Execution time : ",execution_time.total_seconds()," seconds")

"""
###################################################################################
"""
Array - An indexed collection of Homogenous element.
It is the most commonly used concept in programming languages like C,C++,Java etc

By default array concept is not available in Python, instead we use inbuilt List.
(But make sure list and array both are not same)

But in Python, we can create arrays using 2 module
1. array 
2. numpy

## array is not widely use. 
Highly recommended is numpy : Much library support

import array

lst = [1, 2, 3, 4, 5]
arr = array.array('i', lst)  # TypeError: array() argument 1 must be a unicode character, not list
# i > Represents integer
print(type(arr), arr)


import numpy as np
# Printing numpy array one by one, Just like List
arr = np.array([1,2,3,4,5])
for val in arr:
    print(val)


import numpy as np
# Printing numpy array one by one, Just like List or using array comprehension also work
arr = np.array([1,2,3,4,5])
even = [i for i in arr if i%2==0]
print(even) # [np.int64(2), np.int64(4)] i will be off numpy integer type
print(type(even)) # list type
print(np.array(even)) # Value of numpy

"""
#####################################################################################3
"""
Similarities b/w List and NP Array
-----------------------------------
    1. Both can be used to store data.
    2. Order will be preserved in both, Access by using index.
    3. Slicing is also applicable for both.
    4. Both are mutable, is once we create list or array, we can change its elements.
    
Differences b/w List and NP Array
-----------------------------------
    1. List is inbuilt data type, but numpy is not inbuilt.
        To use numpy arrays, we have to install numpy explicitly and import numpy library explicitly.
        
    2. List can hold heterogeneous data, but array can hold homogeneous elements.
    3. On arrays we can perform vector operations.  
        Operations which can be perform on every element of array.
        But we can not perform vector operation on list operation.
        
e.g.

import numpy as np

arr = np.array([1,2,3,4,5])

print(arr+1)
# This is valid operation and provide o/p [2 3 4 5 6],
# 1 is added to each element of array

# If List can do same :
lst = [1,2,3,4,5]
lst = lst+1 # Raise TypeError: can only concatenate list (not "int") to list
print(lst)

    4. Array consume more memory when compared to list.
e.g.


import numpy as np
import sys

lst = [1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]
arr = np.array([1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5])
print(f"Size of List {lst} : ",sys.getsizeof(lst))
print("")
print(f"Size of NumPy Array {arr} : ",sys.getsizeof(arr))

    5. NumPy Arrays are superfast.
    6. More convenient to use numpy array's for mathematical operations.
"""
