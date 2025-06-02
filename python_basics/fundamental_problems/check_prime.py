import math
def check_prime(value:int) -> int:
    for i in range(2,math.floor(math.sqrt(value))+1):
        if value%i == 0:
            return "Not Prime"
    else:
        return "Prime"

print(check_prime(20))