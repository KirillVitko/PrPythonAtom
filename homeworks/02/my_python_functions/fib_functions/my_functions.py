def cache_decorator(function):
    mem_cache = {}
    
    def cached_function(argument):
        if argument in mem_cache:
            print('I used cache!')
            print('local and non local atributes here:', dir())
            return mem_cache[argument]
        else:
            print('i dont use cache!')
            mem_cache[argument] = function(argument)
            return mem_cache[argument]
    
    return cached_function

@cache_decorator
def fib(n):
    if n==1 or n==2:
        return 1
    return fib(n-1) + fib(n-2)

