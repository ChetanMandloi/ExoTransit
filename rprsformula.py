def rprs(fmax, fmin, rod):
    # fmax = 24
    fmin = fmin + rod
    return ((fmax-fmin)/fmax)**0.5

print(rprs(28,24,1))