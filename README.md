# Hoff

```

module main

public:

fun fibonacci(n):
    if n < 2
        then n
        else 
            let n1 = n-1
            and n2 = n-2
            in 
                fibonacci(n1) + fibonacci(n2) 
            tel
    fi
    
private:

fun internal(a, b, c):
    a + b + c
    
const pi = 3.14

```
