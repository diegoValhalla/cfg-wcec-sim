import os, sys

sys.path.insert(0, './tools/cfg-wcec')

from cfg import cfg
from sim import cfg_paths, sim, sim_manager


def run(config_file='sim.config', study='wfreq', time_slice=20):
    """ Run simulation by first getting the task CFG, then simulating path
        execution on the given C file.

        Args:
            filename (string): name of C file
    """
    print 'start', study

    # create simulation manager and set its configuration
    time_slice = float(time_slice)
    simManager = reset_config(config_file, time_slice)

    # run simulation for worst, middle and approximated best paths
    if study == 'wfreq': # sim.config wfreq
        simManager.run_sim('w', valentin=True, show_result='data/consumption-worst-wfreq.csv')

        simManager = reset_config(config_file, time_slice)
        simManager.run_sim('m', valentin=True, show_result='data/consumption-mid-wfreq.csv')

        simManager = reset_config(config_file, time_slice)
        simManager.run_sim('a', valentin=True, show_result='data/consumption-approx-wfreq.csv')

    elif study == 'valentin': # sim.config valentin
        simManager.run_sim('w', valentin=True, show_result='data/consumption-worst-v.csv')

        simManager = reset_config(config_file, time_slice)
        simManager.run_sim('m', valentin=True, show_result='data/consumption-mid-v.csv')

        simManager = reset_config(config_file, time_slice)
        simManager.run_sim('a', valentin=True, show_result='data/consumption-approx-v.csv')

    else: # sim-mine.config mine
        simManager.run_sim('w', valentin=False, show_result='data/consumption-worst-m.csv')

        simManager = reset_config(config_file, time_slice)
        simManager.run_sim('m', valentin=False, show_result='data/consumption-mid-m.csv')

        simManager = reset_config(config_file, time_slice)
        simManager.run_sim('a', valentin=False, show_result='data/consumption-approx-m.csv')

    print 'end', study

def reset_config(config_file, time_slice):
    # create simulation manager and set its configuration
    simManager = sim_manager.SimManager(time_slice)
    set_simulation_config(simManager, config_file)
    return simManager

def set_simulation_config(simManager, config_file):
    """ Get task and environment information of a configuration file.

        Args:
            simManager (SimManager): simulation manager object
            config_file_name (string): configuration file name

        Returns:
            (float) task's WCEC
            (float) task's deadline
            (float) initial frequency to be used
            (dic) freqs_volt: dictionary where key is the frequency and supply
                voltage to use the given frequency is the value
    """
    freqs = []
    volts = []
    freqs_volt = {}
    with open(config_file, 'rU') as f:
        lines = f.readlines()
        try:
            for freq in lines[0].split():
                freqs.append(float(freq))

            for volt in lines[1].split():
                volts.append(float(volt))

            for i in range(0, len(freqs)):
                freqs_volt[freqs[i]] = volts[i]

            for task in lines[2:]:
                data = task.split()
                wcec = float(data[1])
                deadline = float(data[2])
                period = float(data[3])
                jitter = float(data[4])
                init_freq = float(data[5])

                cfile = data[0]
                cfile = _find_file(config_file, cfile)
                graph = cfg.CFG(cfile)
                graph.make_cfg()
                simManager.add_task_sim(
                        graph, wcec, deadline, period, jitter,
                        init_freq, freqs_volt, 0.15)
        except ValueError, IndexError:
            print 'Invalid data in config file'
            sys.exit(1)

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

def _find_file(config_file, cfile):
    """ Find a c file by name, taking into account the current dir can be
        in a couple of typical places
    """
    config_dir = os.path.dirname(config_file)
    cfile = os.path.join(config_dir, cfile)
    return cfile


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Arguments not valid'
    else:
        run(sys.argv[1], sys.argv[2], sys.argv[3])
