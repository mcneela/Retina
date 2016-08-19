"""
Adapted from the swiss_roll.py example
packaged with Scikit-Learn.
"""
import matplotlib.pyplot as plt
import retina.core.axes
import retina.nldr as nldr
import numpy as np
from matplotlib import gridspec
from sklearn import manifold, datasets
from sklearn.neighbors import NearestNeighbors, kneighbors_graph
from scipy.linalg import eigh, svd, qr, solve
from scipy.sparse import eye, csr_matrix
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import check_random_state, check_array
from sklearn.utils.arpack import eigsh
from sklearn.utils.validation import check_is_fitted
from sklearn.utils.validation import FLOAT_DTYPES

def barycenter_weights(X, Z, reg=1e-3):
    """Compute barycenter weights of X from Y along the first axis

    We estimate the weights to assign to each point in Y[i] to recover
    the point X[i]. The barycenter weights sum to 1.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_dim)

    Z : array-like, shape (n_samples, n_neighbors, n_dim)

    reg: float, optional
        amount of regularization to add for the problem to be
        well-posed in the case of n_neighbors > n_dim

    Returns
    -------
    B : array-like, shape (n_samples, n_neighbors)

    Notes
    -----
    See developers note for more information.
    """
    X = check_array(X, dtype=FLOAT_DTYPES)
    Z = check_array(Z, dtype=FLOAT_DTYPES, allow_nd=True)

    n_samples, n_neighbors = X.shape[0], Z.shape[1]
    B = np.empty((n_samples, n_neighbors), dtype=X.dtype)
    v = np.ones(n_neighbors, dtype=X.dtype)

    # this might raise a LinalgError if G is singular and has trace
    # zero
    for i, A in enumerate(Z.transpose(0, 2, 1)):
        C = A.T - X[i]  # broadcasting
        G = np.dot(C, C.T)
        trace = np.trace(G)
        if trace > 0:
            R = reg * trace
        else:
            R = reg
        G.flat[::Z.shape[1] + 1] += R
        w = solve(G, v, sym_pos=True)
        B[i, :] = w / np.sum(w)
    return B

def barycenter_kneighbors_graph(X, n_neighbors, reg=1e-3, n_jobs=1):
    """Computes the barycenter weighted graph of k-Neighbors for points in X

    Parameters
    ----------
    X : {array-like, sparse matrix, BallTree, KDTree, NearestNeighbors}
        Sample data, shape = (n_samples, n_features), in the form of a
        numpy array, sparse array, precomputed tree, or NearestNeighbors
        object.

    n_neighbors : int
        Number of neighbors for each sample.

    reg : float, optional
        Amount of regularization when solving the least-squares
        problem. Only relevant if mode='barycenter'. If None, use the
        default.

    n_jobs : int, optional (default = 1)
        The number of parallel jobs to run for neighbors search.
        If ``-1``, then the number of jobs is set to the number of CPU cores.

    Returns
    -------
    A : sparse matrix in CSR format, shape = [n_samples, n_samples]
        A[i, j] is assigned the weight of edge that connects i to j.

    See also
    --------
    sklearn.neighbors.kneighbors_graph
    sklearn.neighbors.radius_neighbors_graph
    """
    knn = NearestNeighbors(n_neighbors + 1, n_jobs=n_jobs).fit(X)
    X = knn._fit_X
    n_samples = X.shape[0]
    ind = knn.kneighbors(X, return_distance=False)[:, 1:]
    data = barycenter_weights(X, X[ind], reg=reg)
    indptr = np.arange(0, n_samples * n_neighbors + 1, n_neighbors)
    return csr_matrix((data.ravel(), ind.ravel(), indptr),
                      shape=(n_samples, n_samples))

def null_space(M, k, k_skip=1, eigen_solver='arpack', tol=1E-6, max_iter=100,
               random_state=None):
    """
    Find the null space of a matrix M.

    Parameters
    ----------
    M : {array, matrix, sparse matrix, LinearOperator}
        Input covariance matrix: should be symmetric positive semi-definite

    k : integer
        Number of eigenvalues/vectors to return

    k_skip : integer, optional
        Number of low eigenvalues to skip.

    eigen_solver : string, {'auto', 'arpack', 'dense'}
        auto : algorithm will attempt to choose the best method for input data
        arpack : use arnoldi iteration in shift-invert mode.
                    For this method, M may be a dense matrix, sparse matrix,
                    or general linear operator.
                    Warning: ARPACK can be unstable for some problems.  It is
                    best to try several random seeds in order to check results.
        dense  : use standard dense matrix operations for the eigenvalue
                    decomposition.  For this method, M must be an array
                    or matrix type.  This method should be avoided for
                    large problems.

    tol : float, optional
        Tolerance for 'arpack' method.
        Not used if eigen_solver=='dense'.

    max_iter : maximum number of iterations for 'arpack' method
        not used if eigen_solver=='dense'

    random_state: numpy.RandomState or int, optional
        The generator or seed used to determine the starting vector for arpack
        iterations.  Defaults to numpy.random.

    """
    if eigen_solver == 'auto':
        if M.shape[0] > 200 and k + k_skip < 10:
            eigen_solver = 'arpack'
        else:
            eigen_solver = 'dense'

    if eigen_solver == 'arpack':
        random_state = check_random_state(random_state)
        # initialize with [-1,1] as in ARPACK
        v0 = random_state.uniform(-1, 1, M.shape[0])
        try:
            eigen_values, eigen_vectors = eigsh(M, k + k_skip, sigma=0.0,
                                                tol=tol, maxiter=max_iter,
                                                v0=v0)
        except RuntimeError as msg:
            raise ValueError("Error in determining null-space with ARPACK. "
                             "Error message: '%s'. "
                             "Note that method='arpack' can fail when the "
                             "weight matrix is singular or otherwise "
                             "ill-behaved.  method='dense' is recommended. "
                             "See online documentation for more information."
                             % msg)

        return eigen_vectors[:, k_skip:], np.sum(eigen_values[k_skip:])
    elif eigen_solver == 'dense':
        if hasattr(M, 'toarray'):
            M = M.toarray()
        eigen_values, eigen_vectors = eigh(
            M, eigvals=(k_skip, k + k_skip - 1), overwrite_a=True)
        index = np.argsort(np.abs(eigen_values))
        return eigen_vectors[:, index], np.sum(eigen_values)
    else:
        raise ValueError("Unrecognized eigen_solver '%s'" % eigen_solver)

def locally_linear_embedding(
        X, n_neighbors, n_components, reg=1e-3, eigen_solver='auto', tol=1e-6,
        max_iter=100, method='standard', hessian_tol=1E-4, modified_tol=1E-12,
        random_state=None, n_jobs=1):
    """Perform a Locally Linear Embedding analysis on the data.

    Read more in the :ref:`User Guide <locally_linear_embedding>`.

    Parameters
    ----------
    X : {array-like, sparse matrix, BallTree, KDTree, NearestNeighbors}
        Sample data, shape = (n_samples, n_features), in the form of a
        numpy array, sparse array, precomputed tree, or NearestNeighbors
        object.

    n_neighbors : integer
        number of neighbors to consider for each point.

    n_components : integer
        number of coordinates for the manifold.

    reg : float
        regularization constant, multiplies the trace of the local covariance
        matrix of the distances.

    eigen_solver : string, {'auto', 'arpack', 'dense'}
        auto : algorithm will attempt to choose the best method for input data

        arpack : use arnoldi iteration in shift-invert mode.
                    For this method, M may be a dense matrix, sparse matrix,
                    or general linear operator.
                    Warning: ARPACK can be unstable for some problems.  It is
                    best to try several random seeds in order to check results.

        dense  : use standard dense matrix operations for the eigenvalue
                    decomposition.  For this method, M must be an array
                    or matrix type.  This method should be avoided for
                    large problems.

    tol : float, optional
        Tolerance for 'arpack' method
        Not used if eigen_solver=='dense'.

    max_iter : integer
        maximum number of iterations for the arpack solver.

    method : {'standard', 'hessian', 'modified', 'ltsa'}
        standard : use the standard locally linear embedding algorithm.
                   see reference [1]_
        hessian  : use the Hessian eigenmap method.  This method requires
                   n_neighbors > n_components * (1 + (n_components + 1) / 2.
                   see reference [2]_
        modified : use the modified locally linear embedding algorithm.
                   see reference [3]_
        ltsa     : use local tangent space alignment algorithm
                   see reference [4]_

    hessian_tol : float, optional
        Tolerance for Hessian eigenmapping method.
        Only used if method == 'hessian'

    modified_tol : float, optional
        Tolerance for modified LLE method.
        Only used if method == 'modified'

    random_state: numpy.RandomState or int, optional
        The generator or seed used to determine the starting vector for arpack
        iterations.  Defaults to numpy.random.

    n_jobs : int, optional (default = 1)
        The number of parallel jobs to run for neighbors search.
        If ``-1``, then the number of jobs is set to the number of CPU cores.

    Returns
    -------
    Y : array-like, shape [n_samples, n_components]
        Embedding vectors.

    squared_error : float
        Reconstruction error for the embedding vectors. Equivalent to
        ``norm(Y - W Y, 'fro')**2``, where W are the reconstruction weights.

    References
    ----------

    .. [1] `Roweis, S. & Saul, L. Nonlinear dimensionality reduction
        by locally linear embedding.  Science 290:2323 (2000).`
    .. [2] `Donoho, D. & Grimes, C. Hessian eigenmaps: Locally
        linear embedding techniques for high-dimensional data.
        Proc Natl Acad Sci U S A.  100:5591 (2003).`
    .. [3] `Zhang, Z. & Wang, J. MLLE: Modified Locally Linear
        Embedding Using Multiple Weights.`
        http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.382
    .. [4] `Zhang, Z. & Zha, H. Principal manifolds and nonlinear
        dimensionality reduction via tangent space alignment.
        Journal of Shanghai Univ.  8:406 (2004)`
    """
    if eigen_solver not in ('auto', 'arpack', 'dense'):
        raise ValueError("unrecognized eigen_solver '%s'" % eigen_solver)

    if method not in ('standard', 'hessian', 'modified', 'ltsa'):
        raise ValueError("unrecognized method '%s'" % method)

    nbrs = NearestNeighbors(n_neighbors=n_neighbors + 1, n_jobs=n_jobs)
    nbrs.fit(X)
    X = nbrs._fit_X
    N, d_in = X.shape

    if n_components > d_in:
        raise ValueError("output dimension must be less than or equal "
                         "to input dimension")
    if n_neighbors >= N:
        raise ValueError("n_neighbors must be less than number of points")

    if n_neighbors <= 0:
        raise ValueError("n_neighbors must be positive")

    M_sparse = (eigen_solver != 'dense')

    if method == 'standard':
        W = barycenter_kneighbors_graph(
            nbrs, n_neighbors=n_neighbors, reg=reg, n_jobs=n_jobs)

        # we'll compute M = (I-W)'(I-W)
        # depending on the solver, we'll do this differently
        if M_sparse:
            M = eye(*W.shape, format=W.format) - W
            M = (M.T * M).tocsr()
        else:
            M = (W.T * W - W.T - W).toarray()
            M.flat[::M.shape[0] + 1] += 1  # W = W - I = W - I

    elif method == 'hessian':
        dp = n_components * (n_components + 1) // 2

        if n_neighbors <= n_components + dp:
            raise ValueError("for method='hessian', n_neighbors must be "
                             "greater than "
                             "[n_components * (n_components + 3) / 2]")

        neighbors = nbrs.kneighbors(X, n_neighbors=n_neighbors + 1,
                                    return_distance=False)
        neighbors = neighbors[:, 1:]

        Yi = np.empty((n_neighbors, 1 + n_components + dp), dtype=np.float64)
        Yi[:, 0] = 1

        M = np.zeros((N, N), dtype=np.float64)

        use_svd = (n_neighbors > d_in)

        for i in range(N):
            Gi = X[neighbors[i]]
            Gi -= Gi.mean(0)

            # build Hessian estimator
            if use_svd:
                U = svd(Gi, full_matrices=0)[0]
            else:
                Ci = np.dot(Gi, Gi.T)
                U = eigh(Ci)[1][:, ::-1]

            Yi[:, 1:1 + n_components] = U[:, :n_components]

            j = 1 + n_components
            for k in range(n_components):
                Yi[:, j:j + n_components - k] = (U[:, k:k + 1] *
                                                 U[:, k:n_components])
                j += n_components - k

            Q, R = qr(Yi)

            w = Q[:, n_components + 1:]
            S = w.sum(0)

            S[np.where(abs(S) < hessian_tol)] = 1
            w /= S

            nbrs_x, nbrs_y = np.meshgrid(neighbors[i], neighbors[i])
            M[nbrs_x, nbrs_y] += np.dot(w, w.T)

        if M_sparse:
            M = csr_matrix(M)

    elif method == 'modified':
        if n_neighbors < n_components:
            raise ValueError("modified LLE requires "
                             "n_neighbors >= n_components")

        neighbors = nbrs.kneighbors(X, n_neighbors=n_neighbors + 1,
                                    return_distance=False)
        neighbors = neighbors[:, 1:]

        # find the eigenvectors and eigenvalues of each local covariance
        # matrix. We want V[i] to be a [n_neighbors x n_neighbors] matrix,
        # where the columns are eigenvectors
        V = np.zeros((N, n_neighbors, n_neighbors))
        nev = min(d_in, n_neighbors)
        evals = np.zeros([N, nev])

        # choose the most efficient way to find the eigenvectors
        use_svd = (n_neighbors > d_in)

        if use_svd:
            for i in range(N):
                X_nbrs = X[neighbors[i]] - X[i]
                V[i], evals[i], _ = svd(X_nbrs,
                                        full_matrices=True)
            evals **= 2
        else:
            for i in range(N):
                X_nbrs = X[neighbors[i]] - X[i]
                C_nbrs = np.dot(X_nbrs, X_nbrs.T)
                evi, vi = eigh(C_nbrs)
                evals[i] = evi[::-1]
                V[i] = vi[:, ::-1]

        # find regularized weights: this is like normal LLE.
        # because we've already computed the SVD of each covariance matrix,
        # it's faster to use this rather than np.linalg.solve
        reg = 1E-3 * evals.sum(1)

        tmp = np.dot(V.transpose(0, 2, 1), np.ones(n_neighbors))
        tmp[:, :nev] /= evals + reg[:, None]
        tmp[:, nev:] /= reg[:, None]

        w_reg = np.zeros((N, n_neighbors))
        for i in range(N):
            w_reg[i] = np.dot(V[i], tmp[i])
        w_reg /= w_reg.sum(1)[:, None]

        # calculate eta: the median of the ratio of small to large eigenvalues
        # across the points.  This is used to determine s_i, below
        rho = evals[:, n_components:].sum(1) / evals[:, :n_components].sum(1)
        eta = np.median(rho)

        # find s_i, the size of the "almost null space" for each point:
        # this is the size of the largest set of eigenvalues
        # such that Sum[v; v in set]/Sum[v; v not in set] < eta
        s_range = np.zeros(N, dtype=int)
        evals_cumsum = np.cumsum(evals, 1)
        eta_range = evals_cumsum[:, -1:] / evals_cumsum[:, :-1] - 1
        for i in range(N):
            s_range[i] = np.searchsorted(eta_range[i, ::-1], eta)
        s_range += n_neighbors - nev  # number of zero eigenvalues

        # Now calculate M.
        # This is the [N x N] matrix whose null space is the desired embedding
        M = np.zeros((N, N), dtype=np.float64)
        for i in range(N):
            s_i = s_range[i]

            # select bottom s_i eigenvectors and calculate alpha
            Vi = V[i, :, n_neighbors - s_i:]
            alpha_i = np.linalg.norm(Vi.sum(0)) / np.sqrt(s_i)

            # compute Householder matrix which satisfies
            #  Hi*Vi.T*ones(n_neighbors) = alpha_i*ones(s)
            # using prescription from paper
            h = alpha_i * np.ones(s_i) - np.dot(Vi.T, np.ones(n_neighbors))

            norm_h = np.linalg.norm(h)
            if norm_h < modified_tol:
                h *= 0
            else:
                h /= norm_h

            # Householder matrix is
            #  >> Hi = np.identity(s_i) - 2*np.outer(h,h)
            # Then the weight matrix is
            #  >> Wi = np.dot(Vi,Hi) + (1-alpha_i) * w_reg[i,:,None]
            # We do this much more efficiently:
            Wi = (Vi - 2 * np.outer(np.dot(Vi, h), h) +
                  (1 - alpha_i) * w_reg[i, :, None])

            # Update M as follows:
            # >> W_hat = np.zeros( (N,s_i) )
            # >> W_hat[neighbors[i],:] = Wi
            # >> W_hat[i] -= 1
            # >> M += np.dot(W_hat,W_hat.T)
            # We can do this much more efficiently:
            nbrs_x, nbrs_y = np.meshgrid(neighbors[i], neighbors[i])
            M[nbrs_x, nbrs_y] += np.dot(Wi, Wi.T)
            Wi_sum1 = Wi.sum(1)
            M[i, neighbors[i]] -= Wi_sum1
            M[neighbors[i], i] -= Wi_sum1
            M[i, i] += s_i

        if M_sparse:
            M = csr_matrix(M)

    elif method == 'ltsa':
        neighbors = nbrs.kneighbors(X, n_neighbors=n_neighbors + 1,
                                    return_distance=False)
        neighbors = neighbors[:, 1:]

        M = np.zeros((N, N))

        use_svd = (n_neighbors > d_in)

        for i in range(N):
            Xi = X[neighbors[i]]
            Xi -= Xi.mean(0)

            # compute n_components largest eigenvalues of Xi * Xi^T
            if use_svd:
                v = svd(Xi, full_matrices=True)[0]
            else:
                Ci = np.dot(Xi, Xi.T)
                v = eigh(Ci)[1][:, ::-1]

            Gi = np.zeros((n_neighbors, n_components + 1))
            Gi[:, 1:] = v[:, :n_components]
            Gi[:, 0] = 1. / np.sqrt(n_neighbors)

            GiGiT = np.dot(Gi, Gi.T)

            nbrs_x, nbrs_y = np.meshgrid(neighbors[i], neighbors[i])
            M[nbrs_x, nbrs_y] -= GiGiT
            M[neighbors[i], neighbors[i]] += 1

    return null_space(M, n_components, k_skip=1, eigen_solver=eigen_solver,
                      tol=tol, max_iter=max_iter, random_state=random_state)

class EventSystem(object):
    def __init__(self, fig):
        self.fig = fig
        self.hover_sec = None
        self.click_sec = None
        self.fig.canvas.mpl_connect('motion_notify_event', self.mouse_over)
        self.fig.canvas.mpl_connect('button_press_event', self.mouse_click)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.points = None
        self.scatters = None

    def mouse_over(self, event):
        ax = event.inaxes
        try:
            sec = nld.get_layer(ax.title._text)
            axl = ax.get_layer(ax.title._text + ' proj')
        except:
            return
        if sec is not self.hover_sec and self.hover_sec:
            self.hover_sec.unbound()
        sec.set_prop('alpha', 1)
        axl.set_prop('alpha', 1)
        sec.bound()
        for ax in self.fig.get_axes():
            try:
                nonhover_sec = nld.get_layer(ax.title._text)
                two_layer = ax.get_layer(ax.title._text + ' proj')
                """
                twod_axes = self.fig.get_axes()
                twod_secs = []
                for pickax in twod_axes:
                    twod_sec = pickax.get_layer(pickax.title._text + ' proj')
                    print(twod_sec)
                    twod_secs.append(twod_sec)
                """
                if nonhover_sec is not sec:
                    nonhover_sec.set_prop('alpha', 0.2)
                if two_layer is not axl:
                    two_layer.set_prop('alpha', 0.2)
            except:
                pass
        self.hover_sec = sec

    def mouse_click(self, event):
        ax = event.inaxes
        try:
            sec = nld.get_layer(ax.title._text)
        except:
            return
        if sec is not self.click_sec and self.click_sec:
            nld.showcase(sec.name)
        self.click_sec = sec

    def on_pick(self, event):
        ind = event.ind[0]
        arty = event.artist
        for key in nld.layers.keys():
            layer = nld.layers[key]
            for plot in layer.plots:
                if plot is arty:
                    self.neighb_sec = key
                    break
        nbrs = NearestNeighbors(n_neighbors=50, n_jobs=1).fit(X)
        distances, indices = nbrs.kneighbors(X)
        #nbrs.fit(X)
        #W = barycenter_kneighbors_graph(
        #    nbrs, n_neighbors=50, reg=1e-3, n_jobs=1)
        #knn = kneighbors_graph(X, 10).to_array()
        try:
            self.scatters.remove()
            self.two_scatters.remove()
        except:
            pass
        self.points = indices[ind]
        neighb_layer = nld.get_layer(self.neighb_sec)
        self.points = X[self.points]
        # self.points = [neighb_layer.x_data[0][ind], neighb_layer.y_data[0][self.points], neighb_layer.z_data[0][self.points]]
        section_num = int(self.neighb_sec[-1])
        section_ax = self.fig.get_axes()[section_num + 1]
        section_layer = section_ax.get_layer(section_ax.title._text + ' proj')
        self.scatters = nld.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2], c='yellow', s=80)
        two_mat = np.column_stack((section_layer.x_data[0], section_layer.y_data[0]))
        two_nbrs = NearestNeighbors(n_neighbors=50, n_jobs=1).fit(two_mat)
        two_dists, two_inds = two_nbrs.kneighbors(two_mat)
        two_points = two_mat[two_inds[ind]] 
        self.two_scatters = section_ax.scatter(two_points[:, 0], two_points[:, 1], c='green', s=80)
        
X, color = datasets.samples_generator.make_swiss_roll(n_samples=1500)
X_r, err = locally_linear_embedding(X, n_neighbors=12,
                                    n_components=2)

fig = plt.figure(figsize=(20, 20))
gs = gridspec.GridSpec(2, 3)
nld = plt.subplot(gs[0,0], projection='Fovea3D')

num_sections = 5
sections = nldr.mapping.ordered_section(X, num_sections, axis=0)
color = color[X[:, 0].argsort()]
colors = [color[i*len(color)/num_sections:(i+1)*len(color)/num_sections] for i in range(num_sections)]

for i, j, sec, clr in zip([0, 0, 1, 1, 1], range(num_sections), sections, colors):
    swiss_sec = nld.add_layer('section ' + str(j))
    swiss_sec.add_data(sec[:, 0], sec[:, 1], sec[:, 2])
    nld.build_layer(swiss_sec.name, plot=nld.scatter, c=clr, cmap=plt.cm.Spectral, picker=True)
    ax = plt.subplot(gs[i, (j + 1) % 3], projection='Fovea2D')
    X_r, err = locally_linear_embedding(sec, n_neighbors=50,
                                        n_components=2)
    proj = ax.add_layer('section ' + str(j) + ' proj')
    proj.add_data(X_r[:, 0], X_r[:, 1])
    ax.build_layer(proj.name, plot=ax.scatter, c=clr, cmap=plt.cm.Spectral)
    ax.set_title('section ' + str(j))



handler = EventSystem(fig)
print("Hover over a projected data plot to see the corresponding segment in the original Swiss Roll.")
print("Click on a subplot to see the corresponding segment of the original Swiss Roll be showcased.")
nld.set_title("Original data")
plt.axis('tight')
plt.xticks([]), plt.yticks([])
plt.show()
