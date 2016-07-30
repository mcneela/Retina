import numpy as np
import time, warnings
from retina.mlearn.hopfield.hopfield_network import *
from retina.core.axes import Fovea3D
from matplotlib.pyplot import *
from matplotlib import gridspec
from matplotlib.widgets import Button
from sklearn.decomposition import PCA
from scipy.interpolate import griddata as gd

neuron_radius = 1

class VisualNeuron(object):
    """
    Class creates a visual representation of a neuron in a generic Hopfield Network.

    The VisualHopfieldNetwork class presents a collection of visual neurons in a circular
    arrangement, and thus the VisualNeuron position is initialized with polar coordinates.
    """
    def __init__(self, theta, r):
        """
        theta   the polar angle of the neuron's position
        r       the polar radius of the neuron's position
        """
        self.theta = theta
        self.r = r
        self.x = r * np.cos(theta)
        self.y = r * np.sin(theta)
        self.connections = {}

    def __repr__(self):
        """
        Defines a string representation for a neuron giving its position in Cartesian coordinates.
        """
        return "Visual Neuron at " + str((self.x, self.y))

    def draw(self, axes):
        """
        Draws a neuron to the provided Matplotlib axes.
        """
        self.body = Circle((self.x, self.y), radius=neuron_radius, fill=False)
        axes.add_patch(self.body)

    def draw_connection(self, neuron, connection_color, axes):
        """
        Draws a connection between two neurons.

        neuron              the terminal neuron of the connection
        connection_color    the color of the connection line to be drawn
        axes                the Matplotlib axes to which the connection should be drawn
        """
        connection = Line2D((self.x, neuron.x), (self.y, neuron.y), color=connection_color)
        self.connections.update({ neuron :  connection })
        neuron.connections.update({ self : connection })
        axes.add_line(self.connections[neuron])

    def delete_connection(self, neuron):
        """
        Delete the connection between self and neuron. The connection will no longer
        be drawn in the network diagram and will be cleared from memory.

        neuron      the terminal neuron of the connection
        """
        network_lines = self.main_network.lines
        del network_lines[network_lines.index(self.connections[neuron])]

class VisualHopfield(HopfieldNetwork):
    def __init__(self, num_neurons):
        """
        Initializes a VisualHopfield network of num_neurons.
        """
        HopfieldNetwork.__init__(self, num_neurons)
        d_theta = (2 * np.pi) / num_neurons
        self.neurons = [VisualNeuron(i * d_theta, num_neurons) for i in range(num_neurons)]
        self.cs_plot = None

    def run_visualization(self, training_data, recall_data=None):
        """
        Runs the Hopfield Network visualization. Trains the network on training_data and
        recalls on recall_data.
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ion()
            self.training_data = training_data
            self.recall_data = recall_data
            self._setup_display()
            self._draw_network()
            self._plot_state([-1 for i in range(self.num_neurons)])
            self._plot_weights()
            print("Training...")
            self._set_mode("Training")
            self.train(training_data, inject=self._train_inject)
            self._normalize_network()
            self._plot_energy()
            print("Learning...")
            self._set_mode("Learning")
            for state in recall_data:
                self.recall([state], inject=self._recall_inject)
            print("Finished.")
            self._set_mode("Finished")

    def _train_inject(self, prev_weights, iteration, delay=.01):
        """
        Provides drawing capabilities for the superclass train() method.

        prev_weights        The network weight matrix before a round of recalling
                            is undergone
        iteration           The current iteration count
        delay               The time delay between each iteration. Larger delays
                            slow the rate of visualization and vice versa.
        """
        self.cmap.set_data(self._weights)
        self._update_iter(iteration)
        new_weights = self._train_act(self.weights())
        colors = ['green', 'blue', 'red']
        for ((row, column), value) in np.ndenumerate(new_weights):
            if self.neurons[row] is self.neurons[column]:
                continue
            elif new_weights[row,column] != prev_weights[row,column]:
                connection = self.neurons[row].connections[self.neurons[column]]
                setp(connection, linewidth='4')
                setp(connection, color=colors[new_weights[row,column]])
            else:
                connection = self.neurons[row].connections[self.neurons[column]]
                setp(connection, linewidth='1')
        pause(delay)

    def _set_mode(self, mode):
        """
        Sets the current mode of the network to be displayed in the visualization.

        mode        The current mode. Should be one of "Learning" or "Training."
        """
        self.mode.set_text("Current Mode: " + mode)

    def _update_iter(self, num):
        """
        Update the current network iteration.

        num         The current iteration count.
        """
        self.iteration.set_text("Current Iteration: " + str(num))

    def _recall_inject(self, state, iteration, delay=.05):
        """
        Provides drawing capabilities for the superclass recall() method.

        state       The current state of the network. Provided at each step in the
                    recall process.
        iteration   The current iteration count.
        delay       The time delay between successive iterations of recalling.
        """
        state = np.array(state)
        self.state_plot.set_data(state.reshape(5, 5))
        currentenergy = self.energy(state)
        current_state = self.pca.transform(state)
        if self.cs_plot:
            self.cs_plot.remove()
        self.cs_plot = self.energy_diagram.scatter(current_state[:,0], current_state[:,1], currentenergy,
                                                s=80, c='b', marker='o')
        self._update_iter(iteration)
        pause(delay)

    def _setup_display(self):
        """
        Sets up the Matplotlib figures and axes required for the visualization.
        """
        self.network_fig = figure(figsize=(20, 20))
        self.network_fig.canvas.set_window_title("Hopfield Network Visualization")
        gs = gridspec.GridSpec(2, 4)
        self.main_network = subplot(gs[:,:2])
        self.main_network.set_title("Network Diagram")
        self.main_network.get_xaxis().set_ticks([])
        self.main_network.get_yaxis().set_ticks([])
        self.energy_diagram = subplot(gs[0,2], projection='Fovea3D')
        self.energy_diagram.set_title("Energy Function")
        self.contour_diagram = subplot(gs[0,3])
        self.contour_diagram.set_title("Energy Contours")
        self.state_diagram = subplot(gs[1,2])
        self.state_diagram.set_title("Current Network State")
        self.state_diagram.get_xaxis().set_ticks([])
        self.state_diagram.get_yaxis().set_ticks([])
        self.weight_diagram = subplot(gs[1,3])
        self.weight_diagram.set_title("Weight Matrix Diagram")
        self.weight_diagram.get_xaxis().set_ticks([])
        self.weight_diagram.get_yaxis().set_ticks([])
        self.network_fig.suptitle("Hopfield Network Visualization", fontsize=14)
        self.mode = self.network_fig.text(0.4, 0.95, "Current Mode: Initialization",
                                          fontsize=14, horizontalalignment='center')
        self.iteration = self.network_fig.text(0.6, 0.95, "Current Iteration: 0",
                                               fontsize=14, horizontalalignment='center')

        # Widget Functionality
        view_wf = axes([.53, 0.91, 0.08, 0.025])
        self.view_wfbutton = Button(view_wf, 'Wireframe')
        view_attract = axes([.615, 0.91, 0.08, 0.025])
        self.view_attractbutton = Button(view_attract, 'Attractors')

    def _draw_network(self):
        """
        Draws the network diagram to the Matplotlib canvas.
        """
        connections = set()
        colors = ['green', 'blue', 'red']
        for (index1, neuron) in enumerate(self.neurons):
            neuron.draw(self.main_network)
            connections.add(neuron)
            for (index2, neuron_two) in enumerate(self.neurons):
                if neuron_two in connections:
                    continue
                else:
                    connection_color = colors[int(self.weights()[index1, index2])]
                    neuron.draw_connection(neuron_two, connection_color, self.main_network)
            self.main_network.autoscale(tight=False)

    def _plot_energy(self, num_samples=4, path_length=20):
        """
        Plots the energy function of the network.

        num_samples         The number of samples to be used in the computation of the energy function.
                            The greater the number of samples, the higher the accuracy of the resultant plot.
        path_length         The number of steps to compute in calculating each sample's path of convergence
                            toward the network's attractors.
        """
        attractors = self.training_data
        states = [[np.random.choice([-1, 1]) for i in range(self.num_neurons)] for j in range(num_samples)]
        self.pca = PCA(n_components=2)
        self.pca.fit(attractors)
        paths = [attractors]
        for i in range(path_length):
            states = self.recall(states, steps=1)
            paths.append(states)
        x = y = np.linspace(-1, 1, 100)
        X,Y = np.meshgrid(x, y)
        meshpts = np.array([[x, y] for x, y in zip(np.ravel(X), np.ravel(Y))])
        mesh = self.pca.inverse_transform(meshpts)
        grid = np.vstack((mesh, np.vstack(paths)))
        energies = np.array([self.energy(point) for point in grid])
        grid = self.pca.transform(grid)
        gmin, gmax = grid.min(), grid.max()
        xi, yi = np.mgrid[gmin:gmax:100j, gmin:gmax:100j]
        zi = gd(grid, energies, (xi, yi), method='nearest')
        wireframe = self.energy_diagram.add_layer("wireframe")
        mesh_plot = self.energy_diagram.add_layer("mesh_plot")
        attracts = self.energy_diagram.add_layer("attractors")
        wireframe.add_data(xi, yi, zi)
        mesh_plot.add_data(xi, yi, zi)
        self.energy_diagram.build_layer(wireframe.name, plot=self.energy_diagram.plot_wireframe,
                                        colors=(0.5, 0.5, 0.5, 0.5), alpha=0.2)
        self.energy_diagram.build_layer(mesh_plot.name, plot=self.energy_diagram.plot_surface, cmap=cm.coolwarm)
        self.contour_diagram.contour(xi, yi, zi)
        grid = self.pca.transform(attractors)
        z = np.array([self.energy(state) for state in attractors])
        attracts.add_data(grid[:,0], grid[:,1], z)
        self.energy_diagram.build_layer("attractors", plot=self.energy_diagram.scatter, s=80, c='g', marker='o')
        wireframe.hide()
        attracts.hide()

        def wireframe_click(event):
            wireframe.toggle_display()
            mesh_plot.toggle_display()

        def attractor_click(event):
            attracts.toggle_display()

        self.view_wfbutton.on_clicked(wireframe_click)
        self.view_attractbutton.on_clicked(attractor_click)

    def _normalize_network(self):
        """
        Normalizes the line width of each visual connection in the network.

        To be called between the training and recall steps of the visualization.
        """
        for neuron in self.neurons:
            for line in neuron.connections.values():
                if line.get_linewidth() != 1:
                    setp(line, linewidth=1)

    def _plot_state(self, state):
        """
        Plot state to the state_diagram.
        """
        state = np.array(state)
        self.state_plot = self.state_diagram.imshow(state.reshape(5, 5),
                                                    cmap=cm.binary,
                                                    interpolation='nearest')
        self.state_plot.norm.vmin, self.state_plot.norm.vmax = -1, 1

    def _plot_weights(self):
        """
        Draws a heatmap of the network's weight matrix.
        """
        self.cmap = self.weight_diagram.imshow(self._train_act(self.weights()),
                                               vmin=-1, vmax=1, cmap='viridis',
                                               aspect='auto')
        self.cbar_axes = axes([0.91, 0.1, .017, .3625])
        cbar = self.network_fig.colorbar(self.cmap, cax=self.cbar_axes)
