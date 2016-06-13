"""
GUI module for detecting spikes from waveform data and letting users explore their low-D projections
with principal component analysis.

Data recovered from <http://www2.le.ac.uk/departments/engineering/research/bioengineering/neuroengineering-lab/software>

Based on work described in:
Martinez, J., Pedreira, C., Ison, M. J., Quian Quiroga, R. (2009). Realistic simulation of extracellular recordings.
In J Neurosci Methods, 184(2):285-93, doi: 10.1016/j.jneumeth.2009.08.017.

Bandpass filter code from:
Weckesser, W. (2012). How to implement band-pass Butterworth filter with Scipy.signal.butter. Available at
http://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter.
"""

from PyDSTool import *
import PyDSTool as dst
import PyDSTool.Toolbox.phaseplane as pp
from axes import *
from mdp.nodes import PCANode

from scipy.signal import butter, lfilter, argrelextrema
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

global default_sw
default_sw = 64

global tutorial_on
tutorial_on = True

class spikesorter:
    def __init__(self, title):

        self.fig = plt.figure()
        data = importPointset('simdata1_100000.dat',t=0,sep=',')

        vs = data['vararray'][0]
        vs = self.bandpass_filter(vs, 300, 3000, 32000)
        ts = data['t']

        self.N = len(vs)
        self.traj = numeric_to_traj([vs], 'test_traj', ['x'], ts, discrete=False)

        #Threshold used in martinez et al.
        self.mthresh = 4*(np.median(np.abs(vs))/0.6475)

        self.selected_pcs = []
        self.fovea_setup()

        if tutorial_on:
            print("STEP 1:")
            print("Create a horizontal line of interest by pressing 'l'.")
            print("Once created, this line can be forced to extent by pressing 'm'.")
            print("Enter 'ssort.selected_object.update(name = 'thresh')' to identify the line as a threshold for spike detection")
            print("Once the line is renamed to 'thresh', the arrow keys can be used to move it up and down.")
            self.tutorial = 'step2'
        else:
            self.tutorial = None

    def fovea_setup(self):
        fig.suptitle('Spikesort')
        subplot = plt.subplot('111', projection='Fovea2D')
        plt.xlabel('time')
        plt.ylabel('mV')

        #Setup all layers
        subplot.add_layer('spikes')
        subplot.add_layer('thresh_crosses')
        subplot.add_layer('detected')
        subplot.add_layer('pcs')
        subplot.add_layer('scores')

        self.setup({'11':
                   {'name': 'Waveform',
                    'scale': DOI,
                    'layers':['spikes', 'thresh_crosses'],
                    'callbacks':'*',
                    'axes_vars': ['x', 'y']
                    },
                   '12':
                   {'name': 'Detected Spikes',
                    'scale': [(0, default_sw), (-80, 80)],
                    'layers':['detected'],
                    #'callbacks':'*',
                    'axes_vars': ['x', 'y']
                    },
                   '21':
                    {'name': 'Principal Components',
                     'scale': [(0, default_sw), (-0.5, 0.5)],
                     'layers':['pcs'],
                     #'callbacks':'*',
                     'axes_vars': ['x', 'y']
                     },
                    '22':
                    {'name': 'Projected Spikes',
                     #'scale': [(-100, 100), (-100, 100)],
                     'scale': [(-300, 300), (-300, 300)],
                     'layers':['scores'],
                     'callbacks':'*',
                     'axes_vars': ['firstPC', 'secondPC']
                     }
                   },
                  size=(8, 8), with_times=False, basic_widgets=True)

        #self.plotter.set_text('load_perc', Loading: %d\%'%n, 'loading')

        #Bad code carried over from fovea_game:
        fig_struct, figure = self.plotter._resolve_fig(None)
        #self.ax = fig_struct.arrange['11']['axes_obj']

        coorddict = {'x':
                     {'x':'t', 'layer':'spikes', 'style':'b-'}
                     }
        self.add_data_points(self.traj.sample(), coorddict = coorddict)

        evKeyOn = self.fig.canvas.mpl_connect('key_press_event', self.ssort_key_on)

        self.plotter.auto_scale_domain(subplot= '11', xcushion= 0)

        self.plotter.show()

    def bandpass_filter(self, data, lowcut, highcut, fs, order= 5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype= 'band')
        y = lfilter(b, a, data)
        return y


    def user_pick_func(self, ev):
        if self.selected_object.layer == 'detected' or self.selected_object.layer == 'scores':
            if hasattr(self, 'last_name'):
                self.plotter.set_data_2(self.last_name, layer='scores', markersize= 6, zorder= 1, style=self.default_colors[self.last_name])
                self.plotter.set_data_2(self.last_name, layer='detected', linewidth= 1, zorder= 1, style=self.default_colors[self.last_name])
            self.plotter.set_data_2(self.selected_object.name, layer='scores', markersize= 12, zorder= 10, style='y*')
            self.plotter.set_data_2(self.selected_object.name, layer='detected', linewidth= 2.5, zorder= 10, style='y-')

            self.last_name = self.selected_object.name

        elif self.selected_object.layer == 'pcs':
            self.proj_PCs.insert(0, self.selected_object.name)
            self.proj_PCs = self.proj_PCs[0:2]

            for name in fig_struct['layers']['pcs']['data'].keys():
                if name not in self.proj_PCs:
                    self.plotter.set_data_2(name, layer='pcs', style= fig_struct['layers']['pcs']['data'][name]['style'][0]+'--')

            for pc in self.proj_PCs:
                self.plotter.set_data_2(pc, layer='pcs', style= fig_struct['layers']['pcs']['data'][pc]['style'][0]+'-')

            self.proj_vec1 = fig_struct['layers']['pcs']['handles'][self.proj_PCs[0]].get_ydata()
            self.proj_vec2 = fig_struct['layers']['pcs']['handles'][self.proj_PCs[1]].get_ydata()
            fig_struct.arrange['22']['axes_vars'] = list(reversed(self.proj_PCs))
            self.project_to_PC()

        self.plotter.show()


    def user_update_func(self):
        if self.selected_object.name is 'thresh':
            if self.selected_object.m != 0:
                print("Make 'thresh' a horizontal threshold by pressing 'm'.")
                return

            try:
                self.search_width = self.context_objects['ref_box'].dx
                self.context_objects['ref_box'].remove()
            except KeyError:
                self.search_width = default_sw

            if self.tutorial == 'step2':
                print("STEP 2: ")
                print("When thresh is in place, press 'd' to capture each spike crossing the threshold in a bounding box.")
                print("Each detected spike will be placed in the top right subplot.")
                self.tutorial = 'step3'

            cutoff =  self.selected_object.y1

            traj_samp = self.traj.sample()['x']
            r = traj_samp > cutoff
            above_thresh = np.where(r == True)[0]

            spike = []
            spikes = []
            crosses = []

            last_i = above_thresh[0] - 1
            for i in above_thresh:
                if i - 1 != last_i:
                    crosses.append(i)
                    #Return x value of the highest y value.
                    spikes.append(spike)
                    spike = []
                spike.append(i)
                last_i = i

            self.traj_samp = traj_samp
            self.crosses = crosses
            self.spikes = spikes

            self.plotter.add_data([self.crosses, [cutoff]*len(self.crosses)], layer='thresh_crosses', style='r*', name='crossovers', force= True)

            self.show()

    def compute_bbox(self):

        fig_struct, figs = self.plotter._resolve_fig(None)

        #Clear existing bounding boxes
        rem_names = []
        for con_name, con_obj in self.context_objects.items():
            if isinstance(con_obj, box_GUI) and con_name is not 'ref_box':
                rem_names.append(con_name)
        for name in rem_names:
            self.context_objects[name].remove(draw= False)

        fig_struct['layers']['detected']['data'] = {}

        self.plotter.show(rebuild= True)

        #Create new bounding boxes
        c = 0
        for spike in self.spikes:
            peak = np.where(self.traj_samp == max(list(self.traj_samp[spike])))[0][0]
            tlo = peak - 20
            thi = tlo + self.search_width
            valley = min(self.traj.sample()['x'][tlo:thi])

            box_GUI(self, pp.Point2D(tlo, self.traj.sample()['x'][peak]),
                    pp.Point2D(thi, valley),name= 'spike_box'+str(c), select= False)

            spike_seg = self.traj_samp[tlo:thi]

            try:
                X = np.row_stack((X, spike_seg))
            except NameError:
                X = spike_seg

            c += 1

        return X

    def project_to_PC(self):
        Y = np.dot(self.X, np.column_stack((self.proj_vec1, self.proj_vec2)))

        #If moving to a smaller number of spikes, just forcing out data by reassigning names won't work. Must clear.
        self.clear_data('scores')
        self.show()

        self.default_colors = {}
        #Add spikes as individual lines, so they can be referenced individually.
        c = 0
        for spike in Y:
            name = 'spike'+str(c)
            self.default_colors[name] = 'k'
            self.add_data_points([spike[0], spike[1]], layer='scores', style=self.default_colors[name]+'*', name= name)
            c += 1

        self.plotter.auto_scale_domain(subplot = '22')

        self.show(rebuild = True)

    def ssort_key_on(self, ev):
        self._key = k = ev.key  # keep record of last keypress
        fig_struct, fig = self.plotter._resolve_fig(None)

        class_keys = ['1','2','3','0']

        if k in class_keys:
            if isinstance(self.selected_object, box_GUI):
                for dname, dstruct in fig_struct['layers']['scores']['data'].items():
                    if self.selected_object.x1 < dstruct['data'][0] < self.selected_object.x2 and \
                    self.selected_object.y1 < dstruct['data'][1] < self.selected_object.y2:
                        if k == '1':
                            self.default_colors[dname] = 'r'
                            self.plotter.set_data_2(dname, layer='detected', style= 'r-')
                            self.plotter.set_data_2(dname, layer='scores', style= 'r*')
                        if k == '2':
                            self.default_colors[dname] = 'g'
                            self.plotter.set_data_2(dname, layer='detected', style= 'g-')
                            self.plotter.set_data_2(dname, layer='scores', style= 'g*')

                        if k == '3':
                            self.default_colors[dname] = 'b'
                            self.plotter.set_data_2(dname, layer='detected', style= 'b-')
                            self.plotter.set_data_2(dname, layer='scores', style= 'b*')

                        if k == '0':
                            self.default_colors[dname] = 'k'
                            self.plotter.set_data_2(dname, layer='detected', style= 'k-')
                            self.plotter.set_data_2(dname, layer='scores', style= 'k*')

            self.plotter.show()

        if k== 'd':
            try:
                self.crosses
            except AttributeError:
                print("Can't detect spikes until threshold crossings have been found.")
                return

            self.X = self.compute_bbox()

            self.default_colors = {}

            if len(self.X.shape) == 1:
                self.default_colors['spike0'] = 'k'
                self.add_data_points([list(range(0, len(self.X))), self.X], layer= 'detected', style= self.default_colors['spike0']+'-', name= 'spike0', force= True)

            else:
                c= 0
                for spike in self.X:
                    name = 'spike'+str(c)
                    self.default_colors[name] = 'k'
                    self.add_data_points([list(range(0, len(spike))), spike], layer= 'detected', style= self.default_colors[name]+'-', name= name, force= True)
                    c += 1

            self.plotter.auto_scale_domain(xcushion = 0, subplot = '12')
            self.show()

            if self.tutorial == 'step3':
                print("STEP 3: ")
                print("You can now press 'p' to perform PCA on the detected spikes.")
                print("The bottom right subplot will display the first 3 principal components (in red, green, and yellow respectively.)")
                print("The bottom left subplot will show the detected spikes projected onto the first two PCs")
                self.tutorial = 'step4'

        if k == 'p':
            try:
                X = self.X
            except AttributeError:
                print('Must detect spikes before performing PCA.')
                return

            print('doing PCA...')

            self.p = PCANode(output_dim=0.99, reduce= True, svd= True)
            self.p.train(X)
            self.proj_vec1 = self.p.get_projmatrix()[:, 0]
            self.proj_vec2 = self.p.get_projmatrix()[:, 1]

            self.add_data_points([list(range(0, len(self.proj_vec1))) , self.proj_vec1], style= 'r-', layer= 'pcs', name= 'firstPC', force= True)
            self.add_data_points([list(range(0, len(self.proj_vec2))) , self.proj_vec2], style= 'g-', layer= 'pcs', name= 'secondPC', force= True)

            self.plotter.show()
            self.proj_PCs = ['firstPC', 'secondPC']

            try:
                self.add_data_points([list(range(0, len(self.p.get_projmatrix()))) ,self.p.get_projmatrix()[:,2]],
                                   style= 'y--', layer= 'pcs', name= 'thirdPC', force= True)
            except IndexError:
                pass

            self.add_legend(['r', 'g', 'y'], ['1st PC', '2nd PC', '3rd PC'], '21')

            self.plotter.auto_scale_domain(xcushion = 0, subplot = '21')
            self.show()

            self.project_to_PC()

            if self.tutorial == 'step4':
                print("STEP 4: ")
                print("Use mouse clicks to explore the data.")
                print("Clicking on detected spikes in the top-right will highlight the corresponding projection in the bottom right (and vice versa).")
                print("You can also change the set of PCs onto which the data are projected by clicking the desired projection PCs in the bottom left")

                print("NOTE ALSO: ")
                print("Creating a bounding box in the upper-left plot and renaming it to 'ref_box', will change the search width of the detected spike.")
                print("e.g., if you want detected spikes to be 30 msec long, the box's .dx value must be 30.")
                print("After creating the box, it will be set to the current selected object. You can select the thresh line again by clicking on it.")


ssort = spikesorter("SSort")

fig_struct, figs = ssort.plotter._resolve_fig(None)

halt = True
