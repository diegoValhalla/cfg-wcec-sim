import sys, math

sys.path.insert(0, '../../src')

from cfg_paths import CFGPaths
from sim import SimDVFS


class SimManager(object):

    def __init__(self):
        self._tasks_sims = {}
        self._running_stack = []
        self._ready_queue = []
        self._priority_count = 0

    def add_task_sim(
            self, graph, wcec, deadline, jitter, init_freq,
            freqs_volt, approx_percent):
        self._priority_count += 1
        simulate = SimDVFS(
                wcec, self._priority_count, deadline, jitter, init_freq,
                freqs_volt)
        cfg_paths = CFGPaths()
        wpath = cfg_paths.find_worst_path(graph)
        mpath = cfg_paths.find_middle_path(graph)
        abpath = cfg_paths.find_approximate_best_path(graph, approx_percent)
        if abpath is None:
            print 'approximate best path is not available'
            sys.exit(1)
        self._tasks_sims[self._priority_count] = (
                simulate, wpath, mpath, abpath)

    def run_sim(self, path_name='w', valentin=False, show_result=True):
        priorities = sorted(self._tasks_sims.keys())
        # by the end, all tasks will have runned at least once. The last
        # task will run only once
        for prio in priorities:
            sim = self._tasks_sims[prio][0]
            if path_name == 'w':
                path = self._tasks_sims[prio][1]
            elif path_name == 'm':
                path = mpath = self._tasks_sims[prio][2]
            elif path_name == 'a':
                path = self._tasks_sims[prio][3]
            result = sim.start_sim(path, valentin)

            # show results only for the first time each task runs
            if isinstance(result, list) and show_result:
                sim.compare_result_to_worst_freq(
                        path_name, path.get_path_rwcec(), result,
                        0, 0, valentin, False)
                sim.print_results(
                        path_name, path.get_path_rwcec(), result,
                        valentin, False)
                sim.print_to_csv(
                        path_name, path.get_path_rwcec(), result, valentin)
