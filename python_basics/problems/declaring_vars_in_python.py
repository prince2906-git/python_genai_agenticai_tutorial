# Declare variables of types int, float, str, and bool in Python.
# Python is loosely typed, so you can declare variables without specifying their type.
# Python interpreter automatically infers the type of the variable based on the value assigned to it.

# Declare an integer variable
int_var = 42
print(int_var,type(int_var),type(int_var).__name__)  # type() prints the type of the variable
# type() prints the type of the variable
# __name__ is a special attribute that returns the name of the type as a string

# Declare a float variable
float_var = 3.14
print(float_var, type(float_var), type(float_var).__name__)

# Declare a string variable
str_var = "Hello, World!"
print(str_var, type(str_var), type(str_var).__name__)

# Declare a boolean variable
bool_var = True
print(bool_var, type(bool_var), type(bool_var).__name__)

# we can also explicitly convert types using the built-in functions int(), float(), str(), and bool()

# Convert float to int
int_from_float = int(float_var)
print(int_from_float, type(int_from_float), type(int_from_float).__name__)
# Convert int to float
float_from_int = float(int_var)
print(float_from_int, type(float_from_int), type(float_from_int).__name__)
# Convert int to str
str_from_int = str(int_var)
print(str_from_int, type(str_from_int), type(str_from_int).__name__)
# Convert float to str
str_from_float = str(float_var)
print(str_from_float, type(str_from_float), type(str_from_float).__name__)
# Convert boolean to int
int_from_bool = int(bool_var)
print(int_from_bool, type(int_from_bool), type(int_from_bool).__name__)

# Convert boolean to float
float_var = float(bool_var)
print(float_var, type(float_var), type(float_var).__name__)


# We can also define datatype explicitl using : operator, called type hinting.
# # Declaring a variable with a type hint does not enforce the type at runtime
# Declare an integer variable with explicit type
int_var: int = 42
print(int_var, type(int_var), type(int_var).__name__)

# Declare a float variable with explicit type
float_var: float = 3.14
print(float_var, type(float_var), type(float_var).__name__)

# Let's try to assign float to int variable for explicit type,
try:
    int_var: int = 3.14  # This will not raise an error
    print(int_var, type(int_var), type(int_var).__name__)
except TypeError as e:
    print(f"Error: {e}")

# However, this will not raise an error because Python is dynamically typed

# Allowed operations on different types
# Adding an int and a float Allowed
# Adding a float and a string will raise an error
# Adding a boolean and an int will be allowed, but the boolean will be converted to an int (True becomes 1, False becomes 0)
# Division of an int by a float will result in a float
# Concatenating a string with another string is allowed
# Concatenating a string with an int will raise an error
# Concatenating a string with a float will raise an error
# Concatenating a string with a boolean will raise an error
# Multiplying an int by a float will result in a float
# Multiplying a string by an int will repeat the string
# Multiplying a string by a float will raise an error
# Multiplying a boolean by an int will convert the boolean to an int (True becomes 1, False becomes 0)



