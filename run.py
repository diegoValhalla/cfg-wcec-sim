import sys

sys.path.insert(0, '../src')

from cfg import cfg
from sim import cfg_paths, sim


def run(filename):
    """ Run simulation by first getting the task CFG, then simulating path
        execution on the given C file.

        Args:
            filename (string): name of C file
    """
    # create CFG
    graph = cfg.CFG(filename)
    graph.make_cfg()

    # get and initialize data for simulation
    deadline, init_freq, freqs_volt = read_config_file()
    cfgpaths = cfg_paths.CFGPaths()
    simulate = sim.SimDVFS(deadline, freqs_volt)

    simulation(graph, init_freq, cfgpaths, simulate)

def simulation(graph, init_freq, cfgpaths, simulate):
    """ Simulate execution of worst, best and average paths of the given graph.

        Args:
            graph (CFG): control flow graph of the given C file
            init_freq (float): initial frequency to start path execution
            cfgpaths (CFGPaths): object to find worst, best and middle paths
            simulate (SimDVFS): object to simulate path execution and print
                results.
    """
    #simulate_worst_path(graph, init_freq, cfgpaths, simulate, valentin=False,
            #koreans=False, show_result=True)
    #simulate_worst_path(graph, init_freq, cfgpaths, simulate, valentin=True,
            #koreans=False, show_result=True)
    #simulate_worst_path(graph, init_freq, cfgpaths, simulate, valentin=False,
            #koreans=True, show_result=True)

    #simulate_best_path(graph, init_freq, cfgpaths, simulate, valentin=False,
            #koreans=False, show_result=True)
    #simulate_best_path(graph, init_freq, cfgpaths, simulate, valentin=True,
            #koreans=False, show_result=True)
    #simulate_best_path(graph, init_freq, cfgpaths, simulate, valentin=False,
            #koreans=True, show_result=True)

    simulate_mid_path(graph, init_freq, cfgpaths, simulate, valentin=False,
            koreans=False, show_result=True)
    #simulate_mid_path(graph, init_freq, cfgpaths, simulate, valentin=True,
            #koreans=False, show_result=True)
    #simulate_mid_path(graph, init_freq, cfgpaths, simulate, valentin=False,
            #koreans=True, show_result=True)

def read_config_file(config_file_name='sim.config'):
    """ Get task and environment information of a configuration file.

        Args:
            config_file_name (string): configuration file name

        Returns:
            (float) task's deadline
            (float) initial frequency to be used
            (dic) freqs_volt: dictionary where key is the frequency and supply
                voltage to use the given frequency is the value
    """
    deadline = 0
    freqs_volt = {}
    freqs = []
    volts = []
    with open(config_file_name, 'rU') as f:
        lines = f.readlines()
        try:
            deadline = float(lines[0].split()[0])
            init_freq = float(lines[0].split()[1])

            for freq in lines[1].split():
                freqs.append(float(freq))

            for volt in lines[2].split():
                volts.append(float(volt))

            for i in range(0, len(freqs)):
                freqs_volt[freqs[i]] = volts[i]
        except ValueError, IndexError:
            print 'Invalid data in config file'
            sys.exit(1)

    return deadline, init_freq, freqs_volt

def simulate_worst_path(graph, init_freq, cfgpaths, simulate, valentin=False,
        koreans=False, show_result=False):
    """ Start simulation of worst path.

        Args:
            graph (CFG): control flow graph of the given C file
            init_freq (float): initial frequency to start path execution
            cfgpaths (CFGPaths): object to find worst, best and middle paths
            simulate (SimDVFS): object to simulate path execution and print
                results.
            valentin (boolean): if Valentin's idea should be used
            koreans (boolean): if Koreans' idea should be used
            show_result (boolean): if result information should be print in
                standard output.
    """
    wpath = cfgpaths.find_worst_path(graph)
    #if show_result:
        #write_path(wpath)

    # simulate path execution
    worst_result = simulate.start_sim(wpath, init_freq, valentin, koreans)

    # show results
    if isinstance(worst_result, list) and show_result:
        simulate.print_results('worst', wpath.get_path_rwcec(), worst_result,
                valentin, koreans)
        simulate.compare_result_to_worst_freq('worst', wpath.get_path_rwcec(),
                worst_result, 0, 0, valentin, koreans)

def simulate_best_path(graph, init_freq, cfgpaths, simulate, valentin=False,
        koreans=False, show_result=False):
    """ Start simulation of best path.

        Args:
            graph (CFG): control flow graph of the given C file
            init_freq (float): initial frequency to start path execution
            cfgpaths (CFGPaths): object to find worst, best and middle paths
            simulate (SimDVFS): object to simulate path execution and print
                results.
            valentin (boolean): if Valentin's idea should be used
            koreans (boolean): if Koreans' idea should be used
            show_result (boolean): if result information should be print in
                standard output.
    """
    bpath = cfgpaths.find_best_path(graph)
    #if show_result:
        #write_path(bpath)

    # simulate path execution
    best_result = simulate.start_sim(bpath, init_freq, valentin, koreans)

    # show results
    if isinstance(best_result, list) and show_result:
        simulate.print_results('best', bpath.get_path_rwcec(), best_result,
                valentin, koreans)
        simulate.compare_result_to_worst_freq('best', bpath.get_path_rwcec(),
                best_result, 0, 0, valentin, koreans)

def simulate_mid_path(graph, init_freq, cfgpaths, simulate, valentin=False,
        koreans=False, show_result=False):
    """ Start simulation of middle path.

        Args:
            graph (CFG): control flow graph of the given C file
            init_freq (float): initial frequency to start path execution
            cfgpaths (CFGPaths): object to find worst, best and middle paths
            simulate (SimDVFS): object to simulate path execution and print
                results.
            valentin (boolean): if Valentin's idea should be used
            koreans (boolean): if Koreans' idea should be used
            show_result (boolean): if result information should be print in
                standard output.
    """
    wpath = cfgpaths.find_worst_path(graph)
    bpath = cfgpaths.find_best_path(graph)
    mpath = cfgpaths.find_mid_path(graph, wpath.get_path_rwcec(),
                bpath.get_path_rwcec())
    #if show_result:
        #write_path(bpath)

    # simulate path execution
    mid_result = simulate.start_sim(mpath, init_freq, valentin, koreans)

    # show results
    if isinstance(mid_result, list) and show_result:
        simulate.print_results('middle', mpath.get_path_rwcec(), mid_result,
                valentin, koreans)
        simulate.compare_result_to_worst_freq('middle', mpath.get_path_rwcec(),
                mid_result, 0, 0, valentin, koreans)

def write_path(path):
    """ Print RWCEC and the start line of each node of the given path in
        standard output.

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
