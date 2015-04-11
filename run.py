import sys

sys.path.insert(0, '../src')

from cfg import cfg, cfg2graphml
from sim import cfg_paths


def run(filename):
    # create CFG
    graph = cfg.CFG(filename)
    graph.make_cfg()

    # create graphml
    graphml = cfg2graphml.CFG2Graphml()
    graphml.make_graphml(graph, file_name='opa.graphml', yed_output=True)

    # CFG paths
    cfgpaths = cfg_paths.CFGPaths()

    # get worst path
    wpath = cfgpaths.find_worst_path(graph)
    sys.stdout.write('RWCEC: ' + str(wpath.get_path_rwcec()) + '\n')
    sys.stdout.write('Path: ')
    for node, wcec in wpath.get_path():
        sys.stdout.write(str(node.get_start_line()) + ', ')
    sys.stdout.write('\n')

    # get best path
    bpath = cfgpaths.find_best_path(graph)
    sys.stdout.write('RWCEC: ' + str(bpath.get_path_rwcec()) + '\n')
    sys.stdout.write('Path: ')
    for node, wcec in bpath.get_path():
        sys.stdout.write(str(node.get_start_line()) + ', ')
    sys.stdout.write('\n')

    # get middle path
    while True:
        mpath = cfgpaths.find_mid_path(graph, wpath.get_path_rwcec(),
                bpath.get_path_rwcec())
        if mpath is None:
            break
        sys.stdout.write('RWCEC: ' + str(mpath.get_path_rwcec()) + '\n')
        sys.stdout.write('Path: ')
        for node, wcec in mpath.get_path():
            sys.stdout.write(str(node.get_start_line()) + ', ')
        sys.stdout.write('\n')
        wpath = mpath


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Too few arguments')
    else:
        run(sys.argv[1])

