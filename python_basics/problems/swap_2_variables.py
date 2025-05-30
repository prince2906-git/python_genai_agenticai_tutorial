# Using 3 variables
a=2
b=3
temp = a
a = b
b = temp
print(f"Using 3 variables: a={a}, b={b}")

# Using 2 variabless
a=2
b=3
a = a + b
b = a - b
print(f"Using 2 variables: a={a}, b={b}")

# Pythonic way
a=2
b=5
a,b = b,a
print(f"Pythonic way: a={a}, b={b}")