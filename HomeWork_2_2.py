from collections import deque


def is_polindrome(string: str) -> bool:
    '''
    Функція перевіряє рядок на поліндром
    '''
    string = string.replace(" ", "").lower()
    string = deque(string)
    while len(string) > 1:
        if string.popleft() != string.pop():
            return False
    return True


if __name__ == "__main__":
    string = input("Enter a string to check: ")
    print(is_polindrome(string))