from __future__ import division
import PyDSTool as dst
#import PyDSTool.Toolbox.phaseplane as pp
import matplotlib.pyplot as plt
import retina.core.axes
import retina.core.layer
import calc_context as cc
import math
import numpy as np


fig = plt.figure()
ax = plt.subplot('111', projection='Fovea2D')
layer = ax.add_layer('test_layer')
tracker = layer.tracker

def make_vel_ics(speed, ang):
    rad = math.pi*(ang)/180.
    return {'vx': speed*math.cos(rad),
            'vy': speed*math.sin(rad)}


def make_shooter():
    # no friction
    # cos(atan(x)) = 1/(sqrt(1+x^2))
    Fx_str = '0' # '-speed_fn()*cos(atan2(vy,vx))'
    Fy_str = '-10'

    DSargs = dst.args()
    DSargs.varspecs = {'vx': Fx_str, 'x': 'vx',
                       'vy': Fy_str, 'y': 'vy',
                       'Fx_out': 'Fx(x,y)', 'Fy_out': 'Fy(x,y)',
                       'speed': 'speed_fn(vx, vy)',
                       'bearing': '90-180*atan2(vy,vx)/pi'}

    auxfndict = {'Fx': (['x', 'y'], Fx_str),
                 'Fy': (['x', 'y'], Fy_str),
                 'speed_fn': (['vx', 'vy'], 'sqrt(vx*vx+vy*vy)'),
                 }
    DSargs.auxvars = ['Fx_out', 'Fy_out', 'speed', 'bearing']

    DSargs.fnspecs = auxfndict
    DSargs.algparams = {'init_step':0.001,
                        'max_step': 0.1,
                        'max_pts': 20000,
                        'maxevtpts': 2,
                        'refine': 5}

    ground_event = dst.Events.makeZeroCrossEvent('y', -1,
                                                 {'name': 'ground',
                                                  'eventtol': 1e-3,
                                                  'precise': True,
                                                  'term': True},
                                                 varnames=['y'],
                                                 targetlang='python')
    peak_event = dst.Events.makeZeroCrossEvent('vy', -1,
                                                 {'name': 'peak',
                                                  'eventtol': 1e-3,
                                                  'precise': True,
                                                  'term': False},
                                                 varnames=['vy'],
                                                 targetlang='python')
    DSargs.events = [ground_event, peak_event]
    DSargs.checklevel = 2
    DSargs.ics = {'x': 0, 'y': 0,
                  'vx': 0, 'vy': 0}
    DSargs.ics.update(make_vel_ics(5,20))
    DSargs.name = 'cannon'
    DSargs.tdomain = [0, 100000]
    DSargs.tdata = [0, 10]
    return dst.embed(dst.Generator.Vode_ODEsystem(DSargs))


shooter = make_shooter()

# sim.model is a PyDSTool Model
sim = dst.args(tracked_objects=[],
               model=shooter,
               name='sim_cannon_traj',
               pts=None)


calc = cc.calc_context(sim, 'cannon_traj')
w = calc.workspace


shot_num = 0
def go(speed, angle, do_tracker=True):
    global shot_num, w
    shot_num += 1
    w.angle = angle
    w.speed = speed
    sim.model.set(ics=make_vel_ics(speed, angle))
    sim.model.compute('shot%i' % shot_num)
    sim.pts = sim.model.sample('shot%i' % shot_num)
    if do_tracker:
        ax.cla()
        ax.plot(sim.pts['x'], sim.pts['y'], 'b-', lw=3)
        ax.hlines(0, 0, max(sim.pts['x']))
        plt.show()
        calc()
        tracker.show()
        plt.show()

# initialize
go(30, 10, do_tracker=False)


# call tracker every loop to show all sim_stub tracked objects
# (= tracker_plotter objects)

#fig = plt.figure(1)
#ax = plt.gca()


# fig, ax = plt.subplots()

max_dist = cc.make_measure('maxdist',
                              'max(sim.pts["x"])')
max_height = cc.make_measure('maxheight',
                              'max(sim.pts["y"])')

calc.attach((max_dist, max_height))

tracker(calc, 2, ('angle', 'maxdist', 'ko'),
        clear_on_refresh=False)
tracker(calc, 2, ('angle', 'maxheight', 'ro'),
        clear_on_refresh=False)



def make_iter_angle():
    for angle in np.linspace(5, 85, 10):
        yield angle

iter_angle = make_iter_angle()

# rerun this ten times!
go(10, iter_angle.__next__())

# or call directly

go(10, 25)

