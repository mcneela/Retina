from scipy import integrate
from matplotlib.widgets import Slider
import retina.core.axes
import matplotlib.pyplot as plt
import numpy as np
import scipy

class DiscreteSlider(Slider):
    """A matplotlib slider widget with discrete steps."""
    def __init__(self, *args, **kwargs):
        """Identical to Slider.__init__, except for the "increment" kwarg.
        "increment" specifies the step size that the slider will be discritized
        to."""
        self.inc = kwargs.pop('increment', 1)
        Slider.__init__(self, *args, **kwargs)

    def set_val(self, val):
        discrete_val = int(val / self.inc) * self.inc
        xy = self.poly.xy
        xy[2] = discrete_val, 1
        xy[3] = discrete_val, 0
        self.poly.xy = xy
        self.valtext.set_text(self.valfmt % discrete_val)
        if self.drawon: 
            self.ax.figure.canvas.draw()
        self.val = val
        if not self.eventson: 
            return
        for cid, func in self.observers.items():
            func(discrete_val)

def taylor_series(n):
    return lambda x: sum([(x ** i) / scipy.math.factorial(i) for i in range(n)])


fig = plt.figure(figsize=(20, 20))
main_plot = plt.subplot('111', projection='Fovea2D') 
plt.xlabel('x')
plt.ylabel('y')
plt.title('Uniform Convergence and Integration')

x = np.linspace(-2, 3)
y = np.exp(x)

e = main_plot.add_layer('exponential')
e.add_data(x, y)

approx = main_plot.add_layer('approximation')
plt.axhline(0, color='black')
plt.axvline(0, color='black')

main_plot.set_ylim([-5, np.exp(3)])

main_plot.build_layer(layer='exponential', lw=2, color='green', label='e^x')

exp = lambda x: np.exp(x)
e_int = integrate.quad(exp, -2, 3)[0]
print("The integral of e^x for -2 <= x <= 3 is " + str(e_int) + ".\n")

def update(val):
    taylor_number = int(degree.val)
    approx.delete()
    ts = taylor_series(taylor_number)
    approx.add_data(x, ts(x))
    fig.canvas.draw()
    main_plot.build_layer(layer='approximation', lw=2, color='red')
    approx.plots.append(main_plot.fill_between(x, 0, approx.y_data[0], alpha=0.5))
    approx.plots.append(main_plot.fill_between(x, approx.y_data[0], e.y_data[0], color='purple', alpha=0.5))
    ts_int = integrate.quad(ts, -2, 3)[0]
    print("The integral of the degree " + str(taylor_number) + " Taylor approximation is " + str(ts_int) + ".\n")
    print("The error in the integral is " + str(e_int - ts_int) + ".\n")
    


axdegree = plt.axes([0.2, 0.03, 0.65, 0.03], axisbg='purple')
degree = DiscreteSlider(axdegree, 'Taylor Polynomial Degree', 1, 10, valinit=1) 
degree.on_changed(update)

def plot_convergence(num_steps=10):
    exp = lambda x: np.exp(x)
    def taylor_series(n):
        return lambda x: sum([(x ** i) / scipy.math.factorial(i) for i in range(n)])
    for i in range(num_steps):
        f_i = taylor_series(i)
        integral = integrate.quad(f_i, -2, 3)[0]
    return
