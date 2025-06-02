def fibonaci(n: int) -> int:
    lst = []
    if n <= 1:
        return n
    else:
        return fibonaci(n - 1) + fibonaci(n - 2)


num = 20
for i in range(0,num):
    print(fibonaci(i),end=",")
