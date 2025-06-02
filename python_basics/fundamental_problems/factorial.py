def factRecurrsion(value:int) -> int:
    if value < 0:
        raise ValueError("Invalid Value : Negative Numbers are not allowed !!")
    if value == 0 or value == 1:
        return 1
    else:
        return value*factRecurrsion(value-1)

print("Factorial : ",factRecurrsion(89))