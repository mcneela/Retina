def section(data, num_sections):
    """
    Splits the array 'data' into 'num_sections'
    arrays and returns these "sections."
    """
    increment = data.shape[0] / num_sections
    sections = []
    for i in range(num_sections):
        section = data[i * increment : (i + 1) * increment, :] 
        sections.append(section)
    return sections

def ordered_section(data, num_sections, axis=0):
    """
    Sorts the array 'data' along the column number given by 'axis'
    and returns the data array evenly divided into 'num_sections'
    arrays.
    """
    ordered_sections = section(data[data[:, axis].argsort()], num_sections)
    return ordered_sections

def progressive_segment(data, num_iterations, axis=0):
    """
    Returns segments of the array 'data' sorted along
    the column given by 'axis'. These segments increase
    evenly in size based on 'num_iterations'. Smaller
    values of 'num_iterations' yield larger segments.
    """
    seg_size = data.shape[0] / num_iterations
    segs = []
    sorted_data = data[data[:, axis].argsort()]
    for i in range(num_iterations):
        seg = sorted_data[0:(i + 1)*seg_size, :]
        segs.append(seg)
    return segs

def converge_segment(data, num_iterations, axis=0):
    """
    Returns segments of the array 'data' sorted along
    the column given by 'axis.' These segments start
    along the first and last row and increase in size
    until they converge upon the middle of the 'data'
    array.
    """
    sorted_data = data[data[:, axis].argsort()]
    seg_size = data.shape[0] / num_iterations
    increment = seg_size / 2
    segs = []
    for i in range(num_iterations):
        lower_seg = sorted_data[0:(i + 1) * increment, :]
        upper_seg = sorted_data[-(i + 1) * increment, :]
        seg = np.concatenate(lower_seg, upper_seg)
        segs.append(seg)
    return segs
