import sys

sys.path.insert(0, '../src')

from cfg import cfg, cfg2graphml
from sim import cfg_paths, sim


def run(filename):
    # create CFG
    graph = cfg.CFG(filename)
    graph.make_cfg()

    # create graphml
    graphml = cfg2graphml.CFG2Graphml()
    graphml.make_graphml(graph, file_name='opa.graphml', yed_output=True)

    simulate()

def simulate():
    cfgpaths = cfg_paths.CFGPaths()
    simulate = sim.SimDVFS(deadline, freqs_volt)

    # get worst path for current proposal, valentin and koreans
    wpath = cfgpaths.find_worst_path(graph)
    write_path(wpath)
    worst_result = simulate.start_sim(wpath, init_freq,
            valentin=False, koreans=False)
    worst_vresult = simulate.start_sim(wpath, init_freq,
            valentin=True, koreans=False)
    worst_kresult = simulate.start_sim(wpath, 0,
            valentin=False, koreans=True)

    print_result(wpath.get_path_rwcec(), worst_result, worst_vresult,
            worst_kresult)

    # get best path for current proposal, valentin and koreans
    bpath = cfgpaths.find_best_path(graph)
    write_path(bpath)
    best_result = simulate.start_sim(bpath, init_freq,
            valentin=False, koreans=False)
    best_vresult = simulate.start_sim(bpath, init_freq,
            valentin=True, koreans=False)
    best_kresult = simulate.start_sim(bpath, 0,
            valentin=False, koreans=True)

    print_result(bpath.get_path_rwcec(), best_result, best_vresult,
            best_kresult)

    # get middle path for current proposal, valentin and koreans
    mpath = cfgpaths.find_mid_path(graph, wpath.get_path_rwcec(),
            bpath.get_path_rwcec())
    while mpath is not None:
        write_path(mpath)
        mpath = cfgpaths.find_mid_path(graph, mpath.get_path_rwcec(),
                bpath.get_path_rwcec())

def write_path(path):
    sys.stdout.write('RWCEC: %d\n' % path.get_path_rwcec())
    sys.stdout.write('Path: ')
    for node, wcec in path.get_path():
        sys.stdout.write(str(node.get_start_line()) + ', ')
    sys.stdout.write('\n')

def print_result(path_rwcec, result, vresult, kresult):
    # print results for current valentin and koreans proposals
    simulate.print_results(path_rwcec, result)
    simulate.print_results(path_rwcec, vresult)
    simulate.print_results(path_rwcec, kresult)

    simulate.compare_result_to_worst_freq(path_rwcec, result)
    simulate.compare_result_to_worst_freq(path_rwcec, vresult)
    simulate.compare_result_to_worst_freq(path_rwcec, kresult)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Too few arguments')
    else:
        run(sys.argv[1])
