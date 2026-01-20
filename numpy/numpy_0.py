"""
Numpy - Introduction

   Q. What is the need of NumPy?
   A. As a part of Data Science, Machine Learning and Deep Learning very common requirement
    to perform complex mathematics operation
    e.g. Creation of arrays or Matrices
         Perform several operations on arrays/matrices
         Or Solving
            Statistical Operation
            Trigonometric Operations,
            Liner Operations,
            Calculus
            Differential Equations
         Basic python won't have inbuilt library, hence we need Numpy

   Q. What is Numpy and History?
   A. NumPy : [Numerical Python Library]
      Fundamental Python Library to perform complex numerical operations.
      NumPy developed on top of Numeric Library.

      Numeric Library developed by Jim Hugunin.
      Numpy developed by Travis Oliphant and multiple contributors.
      Numpy is freeware and open source library developed in 2005.

   Q. In which language Numpy is written?
   A. Python and C.

   Q. What is the purpose of Numpy?
   A. Since Most of Numpy is written in C, hence its performance is good as compared to Python List.
      Because of high speed performance, numpy is best for ML algorithms than python in built data structures like list.

   Q. What are the various features of Numpy?
   A. > NumPy is superfast because it is written in C Language.
      > NumPy acts as backbone for Data Science Libraries like pandas, scikit-learn, seaborn etc.
      > Pandas internally use 'nd array' to store data, which is NumPy data structure.
      > NumPy has vectorization feature which improves performance while iterating elements.

      ** Vectorization **
        Vectorization in NumPy refers to the ability to perform operations on entire arrays or matrices
        without the need for explicit loops. This feature improves performance by leveraging optimized C-based implementations under the hood,
        making computations faster and more efficient compared to traditional Python loops.

    ****
        1D array by default considered as Vector.
        2D array considered as Matrix.
    ****

   Q. What is nd array in Numpy?
   A. In NunPy, we can hold data by using Array Data Structure.
    The arrays which are created by using numpy are called nd arrays.
    nd array --> N Dimensional Array --> NumPy array.
    It is most commonly used in data science libraries.

    Array : Indexed collection of Homogenous[same datatype] elements.
    Python List : Indexed Collection of Homogenous or Heterogeneous elements.

    NumPy is 'mandatory' to Learn pandas.
    NumPy's library contains several functions to create nd array and to perform several required operations.

    Q. What is advantage of numpy array over python's inbuilt list ?
    A. >> Performance is very high.

   Q. Is it helpful for web development ?
   A. No, it's not related to web development. It is helpful for data science, ML and Deep Learning..

   Q. What are various application areas of Numpy?
   A. - To perform linear algebra functions.
      - To perform linear regression.
      - To perform Logistic regression.
      - Deep Neural Networks.
      - k-mean clustering.
      - Control systems.
      - Operational Research etc.
      -- In Data Science Area [ML, Deep Learning, Data Engineering]
   ** Numpy basic fundamental compulsory required library ***

   Q. What topics will be covered in as a part of Numpy?
   A.   1.Creation of Numpy Array.
        2. Array Operations.
        3.Array Attributes.
        4.Array Indexing and Slicing.
        5.Broadcasting.
        6.Iterating over array.
        7.Binary condition.
        8.Copy and view.
        9.Sort and search.
        10. Statistics related operations.
        11. Linear Algebra Operations.
        etc.
   Q. How to install Numpy?
        -- Python is required.
        1- By using Anaconda distribution. [In built numpy library]
        2-  pip install numpy

   Q. Check if package is installed.
   A. import package | If ImportError: then not installed.
"""
from functools import reduce

lst1 = [10, 20, 30, 40, 50,60]
 # -- numpy.ndarray
lst2 = [1, 2, 3, 4, 5,6]

print([isinstance(i,int) and isinstance(j,int) for i,j in zip(lst1,lst2)])

val = reduce(lambda a,b: a and b,[isinstance(i,int) and isinstance(j,int) for i,j in zip(lst1,lst2)])
print(val)

