def is_symmetric(string: str) -> bool:
    brackets ={
        ")": "(",
        "]": "[",
        "}": "{"
    }
    
    # У якості стеку використовуємо можливості звичайного списку, яких в даному випадку достатньо
    stek = []

    for ch in string:
        if ch in brackets.values():
            stek.append(ch) # наповнюємо стек відкриваючими скобками
        if stek:
            # Якщо символ строки має відповідний ключ як закриваюча скобка і цей ключ відповідає останньому запису в стеку, то забираємо зі стеку цею скобку
            if stek[-1] == brackets.get(ch): 
                stek.pop() 
        # Якщо стек пустий (тобто відкриваючих скобок не було), а ми потрапили вже на закриваючу, значить далі немає сенсу продовжувати
        elif ch in brackets.keys():
            return False            
    # Якщо в кінці в нас в стеку залишилися відкриваючі скобки, значить їм не було закритих
    if stek:
        return False

    return True


if __name__ == "__main__":
    test = "(2+3 [dfg \{dfdfg\} df (df) 1+3 ] bqwe )"
    string = input(f"Enter a sequence (default '{test}'): ")
    if not string:
        string = test
    print(is_symmetric(string))