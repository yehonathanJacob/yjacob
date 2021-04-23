def range_temp(*args):
    if len(args) == 1:
        return _range_temp(0, args[0], 1)
    elif len(args) == 3:
        return _range_temp(*args)
    else:
        raise SyntaxError(f"Expected 1 or 3 arguments, got {len(args)}")

def _range_temp(start, stop, step):
    counter = start
    while check_step(counter,stop,step):
        yield counter
        counter+=step

def check_step(start, stop, step):
    if step>0:
        return stop>start
    else:
        return start>stop


print(list(range_temp(0,10,1)))
print(list(range_temp(10)))
print(list(range_temp(10,0,-1)))
print(list(range_temp(1, 2, 3, 4)))
