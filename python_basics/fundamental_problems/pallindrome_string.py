def check_pallindrome(string: str) -> bool:
    reverse_string = string[::-1]
    return True if string == reverse_string else False

print(check_pallindrome("121"))
