import sys

sys.path.insert(0, '../src')

from cfg import cfg, cfg2graphml
from sim import cfg_paths, sim


def run(filename):
    """ Run simulation of path executions on the given file name.

        Args:
            filename (string): name of C file
    """
    # create CFG
    graph = cfg.CFG(filename)
    graph.make_cfg()

    # create graphml
    graphml = cfg2graphml.CFG2Graphml()
    graphml.make_graphml(graph, file_name='opa.graphml', yed_output=True)

    simulate(graph)

def simulate(graph):
    """ Simulate execution of all paths of the CFG

        Args:
            graph (CFG): control flow graph of the given C file
    """
    deadline, init_freq, freqs_volt = read_config_file()
    cfgpaths = cfg_paths.CFGPaths()
    simulate = sim.SimDVFS(deadline, freqs_volt)

    #simulate_worst_path(cfgpaths, simulate, init_freq, graph, valentin=False,
            #koreans=False)
    #simulate_worst_path(cfgpaths, simulate, init_freq, graph, valentin=True,
            #koreans=False)
    #simulate_worst_path(cfgpaths, simulate, init_freq, graph, valentin=False,
            #koreans=True)

    simulate_best_path(cfgpaths, simulate, init_freq, graph, valentin=False,
            koreans=False)
    #simulate_best_path(cfgpaths, simulate, init_freq, graph, valentin=True,
            #koreans=False)
    #simulate_best_path(cfgpaths, simulate, init_freq, graph, valentin=False,
            #koreans=True)

    #simulate_mid_path(cfgpaths, simulate, init_freq, graph)

def read_config_file(config_file_name='sim.config'):
    deadline = 0
    freqs_volt = {}
    freqs = []
    volts = []
    with open(config_file_name, 'rU') as f:
        lines = f.readlines()
        try:
            deadline = float(lines[0].split()[0])

            for freq in lines[1].split():
                freqs.append(float(freq))
            init_freq = max(freqs)

            for volt in lines[2].split():
                volts.append(float(volt))

            for i in range(0, len(freqs)):
                freqs_volt[freqs[i]] = volts[i]
        except ValueError, IndexError:
            print 'Invalid data in config file'
            sys.exit(1)

    return deadline, init_freq, freqs_volt

def simulate_worst_path(cfgpaths, simulate, init_freq, graph, valentin=False,
        koreans=False):
    """ Start simulation for worst path.

        Args:
            simulate (SimDVFS): object to simulate path execution
            init_freq (int): initial frequency to be used
            graph (CFG): control flow graph of the given C file
    """
    # get worst path for current proposal, valentin and koreans
    wpath = cfgpaths.find_worst_path(graph)
    write_path(wpath)

    # simulate path execution
    worst_result = simulate.start_sim(wpath, init_freq, valentin, koreans)

    # show results
    if isinstance(worst_result, list):
        simulate.print_results(wpath.get_path_rwcec(), worst_result,
                valentin, koreans)
        simulate.compare_result_to_worst_freq(wpath.get_path_rwcec(),
                worst_result, 0, 0, valentin, koreans)

def simulate_best_path(cfgpaths, simulate, init_freq, graph, valentin=False,
        koreans=False):
    """ Start simulation for best path.

        Args:
            simulate (SimDVFS): object to simulate path execution
            init_freq (int): initial frequency to be used
            graph (CFG): control flow graph of the given C file
    """
    # get best path for current proposal, valentin and koreans
    bpath = cfgpaths.find_best_path(graph)
    write_path(bpath)

    # simulate path execution
    best_result = simulate.start_sim(bpath, init_freq, valentin, koreans)

    # show results
    if isinstance(best_result, list):
        simulate.print_results(bpath.get_path_rwcec(), best_result,
                valentin, koreans)
        simulate.compare_result_to_worst_freq(bpath.get_path_rwcec(),
                best_result, 0, 0, valentin, koreans)

def simulate_mid_path(cfgpaths, simulate, init_freq, graph, wpath, bpath):
    """ Start simulation for middle path.

        Args:
            simulate (SimDVFS): object to simulate path execution
            init_freq (int): initial frequency to be used
            graph (CFG): control flow graph of the given C file
            wpath (list): graph worst path
            bpath (list): graph best path
    """
    # get middle path for current proposal, valentin and koreans
    mpath = cfgpaths.find_mid_path(graph, wpath.get_path_rwcec(),
            bpath.get_path_rwcec())

    mid_result = compute_mid_path_avrg(mpath, valentin=False, koreans=False)
    avrg_rwcec = 0
    for freq, wcec in mid_result:
        avrg_rwcec += wcec
    print_result(simulate, avrg_rwcec, mid_result)
    #        valentin=True, koreans=False)

    mid_vresult = compute_mid_path_avrg(mpath, valentin=True, koreans=False)
    avrg_rwcec = 0
    for freq, wcec in mid_vresult:
        avrg_rwcec += wcec
    print_result(simulate, avrg_rwcec, mid_vresult)
    #        valentin=True, koreans=False)

    mid_kresult = compute_mid_path_avrg(mpath, valentin=False, koreans=True)
    avrg_rwcec = 0
    for freq, wcec in mid_kresult:
        avrg_rwcec += wcec
    print_result(simulate, avrg_rwcec, mid_kresult)
    #        valentin=True, koreans=False)

def compute_mid_path_avrg(mpath, valentin=False, koreans=False):
    """ Compute the average case by following all possible middle paths.

        For each used frequency, in order of appearance, store accumulative
        WCEC and how many times this frequency was used. These information will
        be used to take the average path.

        Args:
            mpath (list): first middle path which RWCEC is the greatest number
                less than worst path's RWCEC.
            valentin (boolean): set Valentin's approach
            koreans (boolean): set Koreans's approach

        Returns:
            list of tuples where each element is composed by the frequency and
            WCEC consumed.
    """
    mpaths_count = 0
    while mpath is not None:
        mpaths_count += 1
        write_path(mpath)
        mid_result = simulate.start_sim(mpath, init_freq,
                valentin=False, koreans=False)

        # initialize missing elements
        for i in range(0, len(mid_result) - len(avrg)):
            avrg.append({})

        # store accumulative WCEC and how many times a frequency was used
        for i in range(0, len(mid_result)):
            freq = mid_result[i][0]
            wcec = mid_result[i][1]
            if freq not in avrg[i]:
                avrg[i][freq] = [0, 0]
            avrg[i][freq][0] += wcec
            avrg[i][freq][1] += 1

        mpath = cfgpaths.find_mid_path(graph, mpath.get_path_rwcec(),
                bpath.get_path_rwcec())

    avrg_result = []
    for i in avrg:
        set_freq = 0
        set_wcec = 0
        greatest_used_times = 0
        for freq in avrg[i]:
            if avrg[i][freq][1] > greatest_used_times:
                set_freq = freq
                set_wcec = avrg[i][freq][0]
                greatest_used_times = avrg[i][freq][1]
        if set_freq != 0:
            data = (set_freq, set_wcec / mpaths_count)
            avrg_result.append(data)

    return avrg_result

def write_path(path):
    """ Print RWCEC and the start line of each node of the given path

        Args:
            path (list): each element is a tuple(CFGNode, WCEC)
    """
    sys.stdout.write('RWCEC: %d\n' % path.get_path_rwcec())
    sys.stdout.write('Path: ')
    for node, wcec in path.get_path():
        sys.stdout.write(str(node.get_start_line()) + ', ')
    sys.stdout.write('\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Too few arguments')
    else:
        run(sys.argv[1])
