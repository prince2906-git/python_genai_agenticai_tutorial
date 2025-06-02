def reverse_string(value:str) -> str:
    str_len = len(value)
    reverse_string = ""
    for i in range(str_len-1,-1,-1):
        reverse_string+=value[i]

    return reverse_string

print("Reverse String : ",reverse_string("Hello World"))

## Using Slicing

value = "Prince"
print("Reverse String : ",value[::-1])
