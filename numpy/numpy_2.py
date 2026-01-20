"""
    Ways to Create numpy arrays.
    1.array()
    2.arange()      :   Array Range
    3.linspace()    :   linearly spaced
    4.zeroes()      :   array only with zeros
    5.ones()        :   array only with ones
    6.full()        :   array only with specific digit.
    7.eye()         :   To create identity matrix.
    8.identity()    :   To create identity matrix.
    9.empty()       :   Empty array
    10.numpy.random :   Array of random elements
                        - randInt()
                        - rand()
                        - uniform()
                        - random()
                        - normal()
                        - shuffle()

    Difference between eye() and identity()
"""

# Create numpy array using array()
# For given list or tupple if you want to create array

import numpy as np
print(help(np.array))

"""
array(object, dtype=None, *, copy=True, order='K', subok=False, ndmin=0,like=None)
object : array_like
        An array, any object exposing the array interface, an object whose
        ``__array__`` method returns an array, or any (nested) sequence.
        If object is a scalar, a 0-dimensional array containing object is
        returned.
dtype : data-type, optional
        The desired data-type for the array. If not given, NumPy will try to use
        a default ``dtype`` that can represent the values (by applying promotion
        rules when necessary.)
copy : bool, optional
        If ``True`` (default), then the array data is copied. If ``None``,
        a copy will only be made if ``__array__`` returns a copy, if obj is
        a nested sequence, or if a copy is needed to satisfy any of the other
        requirements (``dtype``, ``order``, etc.). Note that any copy of
        the data is shallow, i.e., for arrays with object dtype, the new
        array will point to the same objects. See Examples for `ndarray.copy`.
        For ``False`` it raises a ``ValueError`` if a copy cannot be avoided.
        Default: ``True``.
order : {'K', 'A', 'C', 'F'}, optional
        Specify the memory layout of the array. If object is not an array, the
        newly created array will be in C order (row major) unless 'F' is
        specified, in which case it will be in Fortran order (column major).
        If object is an array the following holds.
        
         ===== ========= ===================================================
        order  no copy                     copy=True
        ===== ========= ===================================================
        'K'   unchanged F & C order preserved, otherwise most similar order
        'A'   unchanged F order if input is F and not C, otherwise C order
        'C'   C order   C order
        'F'   F order   F order
        
subok : bool, optional
        If True, then sub-classes will be passed-through, otherwise
        the returned array will be forced to be a base-class array (default).
    ndmin : int, optional
        Specifies the minimum number of dimensions that the resulting
        array should have.  Ones will be prepended to the shape as
        needed to meet this requirement.


## 1D Array
import numpy as np

arr = np.array(1)
print(arr) # Dimension 1 X 1 - [1]
print(arr.ndim) # Return dimension of nd array : 1
print(arr.shape) ## shape of array : (1,1)
print(arr.size) ## Size of Array : How many elements -> 1*1 = 1

arr = np.array([1,2,3,4,5])
print(arr) # 1 X 5 - [1 2 3 4 5]
print(arr.ndim) # Dimension : 1
print(arr.shape) ## shape of array : (1,5)
print(arr.size) ## Size of Array : How many elements -> 1*5 = 5
### Check Type of element
print(arr.dtype) # Returns type of element in array : int64



# 2D Array
nested_list = [[1,2,3],[4,5,6],[7,8,9]]
print(nested_list)
# Creating 2D List
array2d = np.array(nested_list)
print(array2d)
'''
[[1 2 3]
 [4 5 6]
 [7 8 9]]
'''
print(array2d.ndim) # Dimension - 2
print(array2d.dtype) # int64
print(array2d.shape) ## Shape of Array : (3,3)
print(array2d.size) ## Size of Array : How many elements -> 3*3 = 9

"""

"""
Array only contains homogenous elements,
if list contains heterogeneous elements then upcasting will be performed
e.g.
import numpy as np
lst = [1,2,4.5,6]
arr = np.array(lst)
print(arr.ndim) # 1
print(arr.dtype) # float64
print(arr) # [1. 2. 4.5 6.]
print(arr.shape) # (1,1)
print(arr.size) # 6


## Same example with adding str to list
lst = [1,2,'A',6]
arr = np.array(lst)
print(arr.ndim) # 1
print(arr.dtype) # object or string
print(arr) # [1. 2. 4.5 6.]
print(arr.shape) # (1,1)
print(arr.size) # 6

# Creating array with providing type
import numpy as np

lst = [1,2,3,4.5]
arr = np.array(lst,dtype=int)
print(arr) ## It will be loss of information : [1 2 3 4] -> 4.5 became 4

lst = [1,2,3,4.5]
arr = np.array(lst,dtype=bool) ## [True True True]
print(arr)
print(arr)

lst = [1,2,3,4.5]
arr = np.array(lst,dtype=complex) ## No Error
print(arr)
print(arr)

lst = [1,2,3,4.5]
arr = np.array(lst,dtype=str) ## No Error
print(arr)
print(arr)

lst = [1,2,'A',5]
arr = np.array(lst,dtype=int) # ValueError: invalid literal for int() with base 10: 'A'
print(arr)

"""