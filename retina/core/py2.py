import matplotlib.pyplot as plt
import sys

python2 = False
if sys.version_info[0] == 2:
    python2 = True

def py2plot(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        if python2:
            plt.show()
    return wrapper
