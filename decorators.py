from codetiming import Timer


# Just simple decorator fo evaluate execution time
def execution_time_decorator(func):
    timer = Timer()

    def wrapper(*args, **kwargs):
        timer.start()
        print('Executing...')
        func(*args, **kwargs)
        print('Stop execution')
        timer.stop()

    return wrapper
