# Convert string to integer and float safely
str = '123.01'

# safe cast to int
int_var = int(str) if str.isdigit() else None
print(int_var)

try:
    # safe cast to float
    float_var = float(str)
except ValueError:
    float_var = None
print(float_var)