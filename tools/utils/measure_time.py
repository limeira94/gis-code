import time


def measuare_execution_time(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    function_name = func.__name__
    
    print(f"Function {function_name} execute in {execution_time:.4f} seconds.")
    