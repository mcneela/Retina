from __future__ import division, absolute_import

import importlib
from matplotlib import pyplot as plt
import math, numpy, scipy
from PyDSTool import * #Need Events from here.

from PyDSTool import args, numeric_to_traj, Point, Points
import PyDSTool.Toolbox.phaseplane as pp
# for potentially generalizable functions and classes to use
import PyDSTool as dst
import matplotlib.pyplot as plt
# for convenience and compatibility
import numpy as np
import scipy as sp

class workspace(dst.args):
    # override to ensure name and simpler repr
    def __init__(self, name, **kw):
        self.__dict__ = kw
        self._name = name

    def __repr__(self):
        return self._infostr(0, 'Workspace ' + self._name,
                             ignore_underscored=True)

    __str__ = __repr__


class calc_context(object):
    """
    __init__ method for concrete sub-class should insert any core parameters
    that are needed into 'shared' attribute

    _update_order list attribute can be edited later to ensure correct order of
    calculations in case of inter-dependence
    """
    def __init__(self, sim, name, *args, **kwargs):
        self.name = name
        self.sim = sim
        self._update_order = []
        self.workspace = workspace(name)
        self._refresh_init_args = []
        # one function to one workspace variable
        self._functions_to_workspace = {}
        try:
            self.local_init(*args, **kwargs)
        except:
            print("local_init could not complete at initialization")

    def __call__(self, *args, **kwargs):
        """
        Refresh workspace after update in attached simulator.
        Option to pass positional or keyword arguments that will be used
        to refresh the local_init() method for this context.

        Returns the updated workspace.
        """
        if len(args) + len(kwargs) == 0:
            self.local_init(*self._refresh_init_args)
        else:
            self.local_init(*args, **kwargs)
        for fn_name in self._update_order:
            f = getattr(self, fn_name)
            # discard result but keep side-effects on workspace update
            f()
        return self.workspace


    def local_init(self, *args, **kwargs):
        """
        Optionally override in concrete sub-class
        """
        pass

    def declare(self, module_name, alias):
        """
        Inject module into global namespace for later reference.
        Equivalent to "import <module_name> as <alias>"
        """
        mod = importlib.import_module(module_name)
        globals()[alias] = mod

    def attach(self, fn_seq):
        """Expect each function to have been decorated using
        @prep(<attr_name>)
        """
        if callable(fn_seq):
            # make a singleton list, for simplicity
            fn_seq = [fn_seq]
        for fn in fn_seq:
            self._attach(fn)


    def _attach(self, fn):
        """
        Seems that functions need to be wrapped individually
        in their own closure to avoid weird sharing of wrapped_fn
        """
        def wrapped_fn():
            val = fn(self)
            self.workspace[fn.attr_name] = val
            #print("Set workspace for value of %s is"%fn.attr_name, val)
            return val
        self.__setattr__(fn.__name__, wrapped_fn)
        self._functions_to_workspace[fn.__name__] = (wrapped_fn, fn.attr_name)

        # default to adding new function to end of update order
        self._update_order.append(fn.__name__)

        try:
            val = getattr(self, fn.__name__)() #fn(self)
        except Exception as e:
            print("Could not compute value at attachment time for function %s"%fn.__name__)
            print("  Problem was: %s" % str(e))
             # initialize with None now, to declare in the meantime
            self.workspace[fn.attr_name] = None


class general_context(calc_context):
    """
    General purpose context
    """
    pass


def make_measure(fn_name, fn_spec, **defs):
    """Dynamically create a python function for use with calculation
    context.
    """
    all_defs = defs.copy()
    q = dst.QuantSpec('_dummy_', fn_spec, treatMultiRefs=False)
    import PyDSTool.parseUtils as pu
    mapping = pu.symbolMapClass()
    assumed_modules = []
    tokens = q.parser.tokenized
    for sym in q.freeSymbols:
        # Hack, for now: if first (therefore, assumed all)
        # occurrences of symbol are in quotes, then don't convert.
        # Better solution would be to make parser create "x" as a single
        # symbol, at least with a detect quote option
        first_ix = tokens.index(sym)
        if first_ix == 0 or (first_ix > 0 and tokens[first_ix-1] not in ['"', "'"]):
            if pu.isHierarchicalName(sym):
                parts = sym.split('.')
                if parts[0] == 'sim':
                    mapping[sym] = 'con.'+sym
##                elif parts[0] == 'bombardier':
##                    # special case as this factory function is defined in that
##                    # module so that reference will fail at runtime: remove
##                    # 'bombardier' prefix
##                    rest_sym = '.'.join(parts[1:])
##                    mapping[sym] = rest_sym
##                    scope = globals()
##                    # locals override
##                    scope.update(locals())
##                    if parts[1] in scope:
##                        all_defs[parts[1]] = scope[parts[1]]
##                    else:
##                        raise ValueError("Cannot resolve scope of symbol '%s'"%sym)
                else:
                    # assume module reference
                    assumed_modules.append(parts[0])
                    # record here to ensure inclusion in dyn_dummy
                    mapping[sym] = 'self.'+sym
            else:
                mapping[sym] = 'con.workspace.'+sym
        elif first_ix > 0 and tokens[first_ix-1] in ['"', "'"]:
            # put this symbol in the mapping values to ensure not included
            # as an argument to the function
            mapping[sym] = sym
    q.mapNames(mapping)
    import types
    for module_name in assumed_modules:
        global_scope = globals()
        # test if module name in scope
        if module_name in global_scope:
            _mod = global_scope[module_name]
            if isinstance(_mod, types.ModuleType):
                all_defs[module_name] = _mod

    # dyn_dummy contains dummy mappings but declares symbols to leave
    # evaluating until runtime
    dyn_dummy = dict(zip(mapping.values(), ['']*len(mapping)))
    funq = dst.expr2fun(q, ensure_args=['con'], ensure_dynamic=dyn_dummy,
                   for_funcspec=False, fn_name=fn_name,
                   **all_defs)

    # decorate output
    funq.attr_name = fn_name
    return funq


# depecrated to make_measure
def prep(attr_name):
    """
    Create decorator of a new measure [DEPRECATED -- see make_measure]
    """
    def decorator(fn):
        fn.attr_name = attr_name
        return fn
    return decorator

def map_workspace(con, pts, *args):
    """
    Returns a list of dictionaries, each representing the state of the
    calc_context workspace for each of the points given. Optional
    positional arguments will be passed first to the calc_context when
    calling it.

    This assumes the calc_context local_init accepts `pt` as an argument.
    """
    wseq = []
    for pt in pts:
        con(*args, pt=pt)
        wseq.append(dst.filteredDict(con.workspace.__dict__, ['_name'], neg=True))
    return wseq

def extract_variable_from_wseq(varname, wseq):
    return [w[varname] for w in wseq]
class tracker_GUI(object):
    """
    Abstract base class
    """
    pass


class tracker_textconsole(tracker_GUI):
    """
    Auto-updating text consoles that are connected to a diagnostic GUI.
    """
    def __init__(self):
        self.figs = {}
        self.sim = None
        self.calc_context = None

    def __call__(self, calc_context, fignum, attribute_name):
        self.sim = calc_context.sim
        self.calc_context = calc_context
        old_toolbar = plt.rcParams['toolbar']
        plt.rcParams['toolbar'] = 'None'
        fig = plt.figure(fignum, figsize=(2,6)) #, frameon=False)
        plt.rcParams['toolbar'] = old_toolbar
        if fignum in self.figs:
            self.figs[fignum].tracked.append(attribute_name)
        else:
            self.figs[fignum] = args(figure=fig, tracked=[attribute_name])
        self.sim.tracked_objects.append(self)

    def show(self):
        for fignum, figdata in self.figs.items():
            fig = plt.figure(fignum)
            ax = plt.axes([0., 0., 1., 1.], frameon=False, xticks=[],yticks=[])
            #figdata.figure.clf()
            ax.cla()
            ax.set_frame_on(False)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            wspace = self.calc_context.workspace
            for tracked_attr in figdata.tracked:
                for i, (obj_name, obj) in enumerate(wspace.__dict__.items()):
                    if obj_name[0] == '_':
                        # internal name, ignore
                        continue
                    try:
                        data = getattr(obj, tracked_attr)
                    except Exception as e:
                        print("No attribute: '%s' in object in workspace '%s'" % (tracked_attr, wspace._name))
                        raise
                    plt.text(0.05, 0.05+i*0.04, '%s: %s = %.4g' % (obj_name, tracked_attr, data))
            plt.title('%s measures of %s (workspace: %s)'%(self.calc_context.sim.name, tracked_attr,
                                                           _escape_underscore(self.calc_context.workspace._name)))
            fig.canvas.set_window_title("Fig %i, Workspace %s" % (fignum, self.calc_context.workspace._name))
        #plt.show()



class tracker_plotter(tracker_GUI):
    """
    Auto-updating plots that are connected to a diagnostic GUI.
    """
    def __init__(self, clear_on_refresh=True):
        self.figs = {}
        self.sim = None
        self.calc_context = None
        self.clear_on_refresh = clear_on_refresh
        self.ever_shown = False

    def __call__(self, calc_context, fignum, xstr, ystr, style):
        self.sim = calc_context.sim
        self.calc_context = calc_context
        fig = plt.figure(fignum)
        new_track = args(xstr=xstr, ystr=ystr, style=style)
        if fignum in self.figs:
            self.figs[fignum].tracked.append(new_track)
        else:
            self.figs[fignum] = args(figure=fig, tracked=[new_track])
        self.sim.tracked_objects.append(self)

    def show(self):
        for fignum, figdata in self.figs.items():
            fig = plt.figure(fignum)
            ax = plt.gca()
            #figdata.figure.clf()
            if self.clear_on_refresh:
                ax.cla()
            wspace = self.calc_context.workspace
            for tracked in figdata.tracked:
                try:
                    xdata = getattr(wspace, tracked.xstr)
                except Exception as e:
                    print("Failed to evaluate: '%s' in workspace '%s'" % (tracked.xstr, wspace._name))
                    raise
                try:
                    ydata = getattr(self.calc_context.workspace, tracked.ystr)
                except Exception as e:
                    print("Failed to evaluate: '%s' in workspace '%s'" % (tracked.ystr, wspace._name))
                    raise
                if self.clear_on_refresh or not self.ever_shown:
                    # only show labels once
                    ax.plot(xdata, ydata,
                            tracked.style, label=_escape_underscore(tracked.ystr))
                else:
                    ax.plot(xdata, ydata, tracked.style)
            if not self.ever_shown:
                plt.legend()
                plt.title('%s measures vs %s (workspace: %s)'%(self.calc_context.sim.name, tracked.xstr,
                                                           _escape_underscore(self.calc_context.workspace._name)))
                fig.canvas.set_window_title("Fig %i, Workspace %s" % (fignum, self.calc_context.workspace._name))
                self.ever_shown = True
        #plt.show()

class tracker_manager(object):
    """
    Track different quantities from different calc contexts in different
    figures. Cannot re-use same figure with different contexts.
    """
    def __init__(self):
        self.tracked = {}
        # currently, all_figs does not automatically release figures if
        # contexts are deleted or replaced
        self.all_figs = []

    def __call__(self, calc_context, fignum, plot_metadata=None,
                 text_metadata=None, clear_on_refresh=True):
        """
        plot_metadata (default None) = (xstr, ystr, style)
        *or*
        text_metadata (default None) = attribute_name

        If text_metadata used, the tracker object is assumed to be a
        textconsole type that accesses declared python objects to access an
        attribute

        clear_on_refresh (default True) causes track plots to clear on refresh
           per subplot axes
        """
        valid_input = plot_metadata is None or text_metadata is None
        if not valid_input:
            raise ValueError("Only use one of plot or text metadata arguments")
        try:
            xstr, ystr, style = plot_metadata
        except TypeError:
            # None is not iterable
            track_plot = False
            attribute_name = text_metadata
        else:
            track_plot = True
        if calc_context in self.tracked:
            if track_plot:
                # tracker_plotter type
                self.tracked[calc_context](calc_context, fignum, xstr, ystr, style)
            else:
                # tracker_textconsole type
                self.tracked[calc_context](calc_context, fignum, attribute_name)
            if fignum not in self.all_figs:
                self.all_figs.append(fignum)
        else:
            if fignum in self.all_figs:
                raise ValueError("Figure number %i already in use" % fignum)
            if track_plot:
                tp = tracker_plotter(clear_on_refresh=clear_on_refresh)
                tp(calc_context, fignum, xstr, ystr, style)
            else:
                tp = tracker_textconsole()
                tp(calc_context, fignum, attribute_name)
            self.tracked[calc_context] = tp


    def show(self):
        for tp in self.tracked.values():
            tp.show()

def _escape_underscore(text):
    """
    Internal utility to escape any TeX-related underscore ('_') characters in mpl strings
    """
    return text.replace('_', '\_')
