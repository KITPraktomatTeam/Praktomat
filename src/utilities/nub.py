# http://stackoverflow.com/a/480227/946226
def nub(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
