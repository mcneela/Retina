def get_sections(data, num_sections):
    increment = data.shape[0] / num_sections
    sections = []
    for i in range(num_sections):
        section = data[i * increment : (i + 1) * increment, :] 
        sections.append(section)
    return sections

def section(data, num_sections, axis='x'):
    axes = {'x': 0, 'y': 1, 'z': 2}
    try:
        ax = axes[axis]
    except:
        print(axis + " is not a valid axis.")
    sections = get_sections(data[data[:, ax].argsort()], num_sections)
    return sections

def progressive_segment(data, num_iterations, axis=0):
    seg_size = data.shape[0] / num_iterations
    segs = []
    for i in range(num_iterations):
        sorted_data = data[data[:, axis].argsort()]
        seg = data[0:(i + 1)*seg_size, :]
        segs.append(seg)
    return segs
