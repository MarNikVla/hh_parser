from codetiming import Timer


def execution_time_decorator(func):
    timer = Timer()

    def wrapper(*args, **kwargs):
        timer.start()
        print('Executing...')
        func(*args, **kwargs)
        print('Stop execution')
        timer.stop()

    return wrapper
