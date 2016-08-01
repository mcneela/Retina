from __future__ import division, absolute_import

import importlib
import PyDSTool as dst
import math, numpy, scipy
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

